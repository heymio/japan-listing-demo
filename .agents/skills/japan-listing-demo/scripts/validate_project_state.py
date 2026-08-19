#!/usr/bin/env python3
"""Validate machine-checkable listing project state.

The validator computes gate results from source state. It intentionally ignores any
agent-authored `declared_gate_results` field.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_POLICY_PATH = SKILL_DIR / "data" / "channel-policy-limits.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(payload.encode("utf-8")).hexdigest()


def _gate(status: str, *messages: str) -> dict[str, Any]:
    return {"status": status, "messages": [m for m in messages if m]}


def _load_policy(path: Path | None = None) -> dict[str, Any]:
    policy_path = path or DEFAULT_POLICY_PATH
    return json.loads(policy_path.read_text(encoding="utf-8"))


def _approval_index(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for event in state.get("approval_events", []):
        approval_id = event.get("approval_id")
        if isinstance(approval_id, str) and approval_id:
            result[approval_id] = event
    return result


def _valid_user_approval(event: dict[str, Any] | None, scope: str, approved_hash: str) -> tuple[bool, str]:
    if not event:
        return False, "approval event missing"
    if event.get("actor") != "user":
        return False, "approval actor must be user"
    if not isinstance(event.get("source_ref"), str) or not event.get("source_ref", "").strip():
        return False, "approval source_ref missing"
    if event.get("scope") != scope:
        return False, f"approval scope mismatch: expected {scope}"
    if event.get("approved_hash") != approved_hash:
        return False, "approval hash does not match current locked state"
    return True, ""


def _asset_lock_payload(asset: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "asset_id",
        "canonical_source",
        "sha256",
        "role",
        "page_offer_scope",
        "allowed_slots",
    ]
    payload = {key: asset.get(key) for key in keys if key in asset}
    if asset.get("derivative_of"):
        payload["derivative_of"] = asset.get("derivative_of")
    return payload


def _module_payload(module: dict[str, Any]) -> dict[str, Any]:
    keys = ["module_id", "native_type", "interaction", "asset_ids", "approved_stage"]
    return {key: module.get(key) for key in keys if key in module}


def _plan_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {"modules": [_module_payload(module) for module in plan.get("modules", [])]}


def _transform_payload(asset: dict[str, Any]) -> dict[str, Any]:
    transform = asset.get("transform") or {}
    return {
        "asset_id": asset.get("asset_id"),
        "derivative_of": asset.get("derivative_of"),
        "canonical_source": asset.get("canonical_source"),
        "sha256": asset.get("sha256"),
        "type": transform.get("type"),
        "target_slot": transform.get("target_slot"),
    }


def _schema_gate(state: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if state.get("schema_version") != "0.1":
        errors.append("schema_version must be 0.1")
    if not isinstance(state.get("channel"), dict):
        errors.append("channel object missing")
    if not isinstance(state.get("assets", []), list):
        errors.append("assets must be a list")
    if not isinstance(state.get("approval_events", []), list):
        errors.append("approval_events must be a list")
    if not isinstance(state.get("locked_module_plan"), dict):
        errors.append("locked_module_plan object missing")
    if not isinstance(state.get("implementation"), dict):
        errors.append("implementation object missing")
    return _gate("FAIL" if errors else "PASS", *errors)


def _channel_module_budget_gate(state: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    channel = state.get("channel", {})
    channel_id = channel.get("id")
    enhanced = channel.get("enhanced_content", {})
    tier = enhanced.get("tier")
    plan = state.get("locked_module_plan", {})
    modules = plan.get("modules", [])

    if not modules:
        return _gate("N/A", "no enhanced-content modules in locked plan")

    channel_policy = policy.get("channels", {}).get(channel_id, {})
    tier_policy = channel_policy.get("enhanced_content", {}).get(tier)
    if not tier_policy:
        return _gate("UNVERIFIED", f"no packaged executable module budget for channel={channel_id!r}, tier={tier!r}")

    policy_max = tier_policy.get("max_modules")
    declared_max = enhanced.get("declared_max_modules")
    messages: list[str] = []
    failed = False

    if not isinstance(policy_max, int) or policy_max < 1:
        return _gate("UNVERIFIED", "packaged channel policy has no usable max_modules")
    if not isinstance(declared_max, int) or declared_max < 1:
        return _gate("UNVERIFIED", "Project State Manifest lacks declared_max_modules")
    if declared_max > policy_max:
        failed = True
        messages.append(f"declared_max_modules {declared_max} exceeds packaged policy max {policy_max}")
    effective_max = min(declared_max, policy_max)
    if len(modules) > effective_max:
        failed = True
        messages.append(f"locked module count {len(modules)} exceeds executable max {effective_max}")
    if failed:
        return _gate("FAIL", *messages)
    return _gate("PASS", f"locked module count {len(modules)} <= executable max {effective_max}")


def _approval_provenance_gate(state: dict[str, Any]) -> dict[str, Any]:
    approvals = _approval_index(state)
    errors: list[str] = []

    plan = state.get("locked_module_plan", {})
    modules = plan.get("modules", [])
    if modules:
        computed_plan_hash = canonical_hash(_plan_payload(plan))
        if plan.get("status") != "LOCKED":
            errors.append("locked_module_plan status must be LOCKED")
        if plan.get("plan_hash") != computed_plan_hash:
            errors.append("locked_module_plan plan_hash does not match current module plan")
        ok, reason = _valid_user_approval(
            approvals.get(plan.get("approval_id")), "module_plan", computed_plan_hash
        )
        if not ok:
            errors.append(f"module plan approval invalid: {reason}")

    for asset in state.get("assets", []):
        if asset.get("status") != "LOCKED":
            continue
        asset_id = asset.get("asset_id", "<missing>")
        digest = asset.get("sha256")
        if not isinstance(digest, str) or not HEX64.match(digest):
            errors.append(f"{asset_id}: locked asset requires a lowercase SHA-256")
            continue

        approval_id = asset.get("approval_id")
        if approval_id:
            asset_hash = canonical_hash(_asset_lock_payload(asset))
            ok, reason = _valid_user_approval(
                approvals.get(approval_id), f"asset_lock:{asset_id}", asset_hash
            )
            if not ok:
                errors.append(f"{asset_id}: asset approval invalid: {reason}")
            continue

        recovery = asset.get("recovery") or {}
        exact_ok = (
            recovery.get("type") == "recovered_exact"
            and recovery.get("matches_previous_locked_sha") is True
            and recovery.get("previous_locked_sha256") == digest
        )
        if not exact_ok:
            errors.append(
                f"{asset_id}: LOCKED requires user approval provenance or exact SHA recovery"
            )

    return _gate("FAIL" if errors else "PASS", *errors)


def _module_origin_gate(state: dict[str, Any]) -> dict[str, Any]:
    plan = state.get("locked_module_plan", {})
    modules = plan.get("modules", [])
    implementation = state.get("implementation", {})
    slots = implementation.get("slots", [])
    if not modules and not slots:
        return _gate("N/A", "no module plan or implementation")

    errors: list[str] = []
    computed_plan_hash = canonical_hash(_plan_payload(plan))
    if plan.get("status") != "LOCKED":
        errors.append("module plan is not LOCKED")
    if plan.get("plan_hash") != computed_plan_hash:
        errors.append("module plan hash mismatch")
    if implementation.get("plan_hash") != computed_plan_hash:
        errors.append("implementation does not consume the locked plan hash")

    plan_index: dict[str, dict[str, Any]] = {}
    for module in modules:
        module_id = module.get("module_id")
        if not isinstance(module_id, str) or not module_id:
            errors.append("planned module missing module_id")
            continue
        if module_id in plan_index:
            errors.append(f"duplicate planned module_id {module_id}")
        plan_index[module_id] = module
        if str(module.get("approved_stage")) not in {"7", "7.5"}:
            errors.append(f"{module_id}: approved_stage must be 7 or 7.5")

    seen: set[str] = set()
    for slot in slots:
        module_id = slot.get("module_id")
        if not module_id:
            continue
        if module_id not in plan_index:
            errors.append(f"{module_id}: implementation module has no locked planned origin")
            continue
        seen.add(module_id)
        planned = plan_index[module_id]
        if slot.get("native_type") != planned.get("native_type"):
            errors.append(f"{module_id}: native_type drifted from locked plan")
        if slot.get("interaction") != planned.get("interaction"):
            errors.append(f"{module_id}: interaction drifted from locked plan")

    missing = sorted(set(plan_index) - seen)
    if missing:
        errors.append(f"planned modules missing from implementation: {', '.join(missing)}")

    return _gate("FAIL" if errors else "PASS", *errors)


def _transform_auth_gate(state: dict[str, Any]) -> dict[str, Any]:
    approvals = _approval_index(state)
    errors: list[str] = []
    derivatives = [asset for asset in state.get("assets", []) if asset.get("status") == "LOCKED" and (asset.get("derivative_of") or asset.get("transform"))]
    if not derivatives:
        return _gate("PASS", "no locked derivatives require transform authorization")

    for asset in derivatives:
        asset_id = asset.get("asset_id", "<missing>")
        transform = asset.get("transform") or {}
        approval_id = transform.get("approval_id")
        approved_stage = str(transform.get("approved_stage"))
        if approved_stage not in {"7.5", "8"}:
            errors.append(f"{asset_id}: transform approved_stage must be 7.5 or 8")
        transform_hash = canonical_hash(_transform_payload(asset))
        ok, reason = _valid_user_approval(
            approvals.get(approval_id), f"transform:{asset_id}", transform_hash
        )
        if not ok:
            errors.append(f"{asset_id}: transform authorization invalid: {reason}")

    return _gate("FAIL" if errors else "PASS", *errors)


def _asset_slot_gate(state: dict[str, Any]) -> dict[str, Any]:
    assets = {asset.get("asset_id"): asset for asset in state.get("assets", []) if asset.get("asset_id")}
    contracts = state.get("asset_slot_contract", [])
    impl_slots = {slot.get("slot_id"): slot for slot in state.get("implementation", {}).get("slots", []) if slot.get("slot_id")}
    if not contracts:
        return _gate("N/A", "no asset-slot contract")

    errors: list[str] = []
    for contract in contracts:
        slot_id = contract.get("slot_id")
        required = contract.get("required_asset_ids", [])
        impl = impl_slots.get(slot_id)
        if impl is None:
            errors.append(f"{slot_id}: contracted slot missing from implementation")
            continue
        if impl.get("asset_ids", []) != required:
            errors.append(f"{slot_id}: implementation Asset IDs do not match locked slot contract")
        if contract.get("interaction") is not None and impl.get("interaction") != contract.get("interaction"):
            errors.append(f"{slot_id}: interaction does not match slot contract")
        for asset_id in required:
            asset = assets.get(asset_id)
            if not asset:
                errors.append(f"{slot_id}: required asset {asset_id} missing")
                continue
            if asset.get("status") != "LOCKED":
                errors.append(f"{slot_id}: asset {asset_id} is not LOCKED")
            allowed_slots = asset.get("allowed_slots", [])
            if slot_id not in allowed_slots:
                errors.append(f"{slot_id}: asset {asset_id} is not allowed in this slot")

    return _gate("FAIL" if errors else "PASS", *errors)


def _delivery_parity_gate(state: dict[str, Any]) -> dict[str, Any]:
    plan = state.get("locked_module_plan", {})
    plan_index = {m.get("module_id"): m for m in plan.get("modules", []) if m.get("module_id")}
    impl_index = {s.get("module_id"): s for s in state.get("implementation", {}).get("slots", []) if s.get("module_id")}
    if not plan_index and not impl_index:
        return _gate("N/A", "no planned or implemented modules")

    errors: list[str] = []
    if set(plan_index) != set(impl_index):
        errors.append("implemented module IDs differ from locked module plan")
    for module_id in sorted(set(plan_index) & set(impl_index)):
        planned = plan_index[module_id]
        implemented = impl_index[module_id]
        for field in ["native_type", "interaction", "asset_ids"]:
            if implemented.get(field) != planned.get(field):
                errors.append(f"{module_id}: implemented {field} differs from locked plan")
    return _gate("FAIL" if errors else "PASS", *errors)


def validate_state(state: dict[str, Any], policy: dict[str, Any] | None = None) -> dict[str, Any]:
    loaded_policy = policy if policy is not None else _load_policy()
    gates = {
        "SCHEMA_GATE": _schema_gate(state),
        "CHANNEL_MODULE_BUDGET_GATE": _channel_module_budget_gate(state, loaded_policy),
        "APPROVAL_PROVENANCE_GATE": _approval_provenance_gate(state),
        "MODULE_ORIGIN_GATE": _module_origin_gate(state),
        "TRANSFORM_AUTH_GATE": _transform_auth_gate(state),
        "ASSET_SLOT_GATE": _asset_slot_gate(state),
        "DELIVERY_PARITY_GATE": _delivery_parity_gate(state),
    }
    statuses = {gate["status"] for gate in gates.values()}
    if "FAIL" in statuses:
        overall = "FAIL"
    elif "UNVERIFIED" in statuses:
        overall = "UNVERIFIED"
    else:
        overall = "PASS"
    return {
        "overall_status": overall,
        "gates": gates,
        "note": "declared_gate_results is intentionally ignored; results are computed from source state",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate japan-listing-demo Project State Manifest")
    parser.add_argument("state", type=Path, help="Path to project-state JSON")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH, help="Channel policy limits JSON")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result JSON")
    args = parser.parse_args()

    state = json.loads(args.state.read_text(encoding="utf-8"))
    policy = _load_policy(args.policy)
    result = validate_state(state, policy)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"OVERALL: {result['overall_status']}")
        for name, gate in result["gates"].items():
            print(f"{name}: {gate['status']}")
            for message in gate["messages"]:
                print(f"  - {message}")

    if result["overall_status"] == "PASS":
        return 0
    if result["overall_status"] == "UNVERIFIED":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
