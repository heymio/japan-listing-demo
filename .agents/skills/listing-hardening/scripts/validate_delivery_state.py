#!/usr/bin/env python3
"""Validate machine-checkable listing delivery state with strict fail-closed gates.

v0.3.3 keeps legacy v0.1 compatibility while making Delivery State 0.2 a hard
verification boundary for Demo delivery. Caller-authored switches cannot disable
mandatory pre-Demo verification and all final gates are recomputed from state.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
CORE_PATH = SCRIPT_DIR / "_delivery_state_core.py"
SPEC = importlib.util.spec_from_file_location("listing_delivery_state_core", CORE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load delivery validator core: {CORE_PATH}")
_core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(_core)

canonical_hash = _core.canonical_hash
DEFAULT_POLICY_PATH = _core.DEFAULT_POLICY_PATH
SUPPORTED_SCHEMA_VERSIONS = _core.SUPPORTED_SCHEMA_VERSIONS
HEX64 = re.compile(r"^[0-9a-f]{64}$")

GATE_NAMES = [
    "SCHEMA_GATE",
    "CHANNEL_MODULE_BUDGET_GATE",
    "APPROVAL_PROVENANCE_GATE",
    "MODULE_ORIGIN_GATE",
    "TRANSFORM_AUTH_GATE",
    "EVIDENCE_RECONCILIATION_GATE",
    "PRODUCTION_FREEZE_GATE",
    "ASSET_SLOT_GATE",
    "PRE_DEMO_ASSET_GATE",
    "FRONTEND_FIDELITY_GATE",
    "DEMO_RUNTIME_GATE",
    "DELIVERY_PARITY_GATE",
]


def _gate(status: str, *messages: str) -> dict[str, Any]:
    return {"status": status, "messages": [message for message in messages if message]}


def _duplicate_values(items: list[Any], key: str, label: str, errors: list[str]) -> None:
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{index}] must be an object")
            continue
        value = item.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or not value:
            errors.append(f"{label}[{index}].{key} must be a non-empty string")
            continue
        if value in seen:
            errors.append(f"duplicate {label} {key}: {value}")
        seen.add(value)


def _schema_gate(state: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(state, dict):
        return _gate("FAIL", "state root must be an object")

    schema_version = state.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append("schema_version must be 0.1 or 0.2")

    channel = state.get("channel")
    if not isinstance(channel, dict):
        errors.append("channel must be an object")
    elif "enhanced_content" in channel and not isinstance(channel.get("enhanced_content"), dict):
        errors.append("channel.enhanced_content must be an object when present")

    assets = state.get("assets")
    if not isinstance(assets, list):
        errors.append("assets must be a list")
        assets = []
    else:
        _duplicate_values(assets, "asset_id", "assets", errors)
        for index, asset in enumerate(assets):
            if not isinstance(asset, dict):
                continue
            for field in ["allowed_slots", "page_offer_scope"]:
                if field in asset and not isinstance(asset.get(field), list):
                    errors.append(f"assets[{index}].{field} must be a list")
            for field in ["transform", "recovery"]:
                if field in asset and asset.get(field) is not None and not isinstance(asset.get(field), dict):
                    errors.append(f"assets[{index}].{field} must be an object when present")

    approvals = state.get("approval_events")
    if not isinstance(approvals, list):
        errors.append("approval_events must be a list")
        approvals = []
    else:
        _duplicate_values(approvals, "approval_id", "approval_events", errors)

    plan = state.get("locked_module_plan")
    if not isinstance(plan, dict):
        errors.append("locked_module_plan must be an object")
        plan = {}
    modules = plan.get("modules", []) if isinstance(plan, dict) else []
    if not isinstance(modules, list):
        errors.append("locked_module_plan.modules must be a list")
        modules = []
    else:
        _duplicate_values(modules, "module_id", "locked_module_plan.modules", errors)
        for index, module in enumerate(modules):
            if not isinstance(module, dict):
                continue
            asset_ids = module.get("asset_ids", [])
            if not isinstance(asset_ids, list) or any(not isinstance(x, str) or not x for x in asset_ids):
                errors.append(f"locked_module_plan.modules[{index}].asset_ids must be a list of Asset IDs")

    implementation = state.get("implementation")
    if not isinstance(implementation, dict):
        errors.append("implementation must be an object")
        implementation = {}
    impl_slots = implementation.get("slots", []) if isinstance(implementation, dict) else []
    if not isinstance(impl_slots, list):
        errors.append("implementation.slots must be a list")
        impl_slots = []
    else:
        _duplicate_values(impl_slots, "slot_id", "implementation.slots", errors)
        _duplicate_values(impl_slots, "module_id", "implementation.slots", errors)
        for index, slot in enumerate(impl_slots):
            if not isinstance(slot, dict):
                continue
            asset_ids = slot.get("asset_ids", [])
            if not isinstance(asset_ids, list) or any(not isinstance(x, str) or not x for x in asset_ids):
                errors.append(f"implementation.slots[{index}].asset_ids must be a list of Asset IDs")

    contracts = state.get("asset_slot_contract", [])
    if not isinstance(contracts, list):
        errors.append("asset_slot_contract must be a list")
        contracts = []
    else:
        _duplicate_values(contracts, "slot_id", "asset_slot_contract", errors)
        for index, contract in enumerate(contracts):
            if not isinstance(contract, dict):
                continue
            required = contract.get("required_asset_ids", [])
            if not isinstance(required, list) or any(not isinstance(asset_id, str) or not asset_id for asset_id in required):
                errors.append(f"asset_slot_contract[{index}].required_asset_ids must be a list of Asset IDs")
            elif len(set(required)) != len(required):
                errors.append(f"asset_slot_contract[{index}].required_asset_ids contains duplicates")

    audit_checkpoints = state.get("audit_checkpoints")
    if audit_checkpoints is not None and not isinstance(audit_checkpoints, dict):
        errors.append("audit_checkpoints must be an object when present")

    auditor_evidence = state.get("auditor_evidence")
    if auditor_evidence is not None and not isinstance(auditor_evidence, dict):
        errors.append("auditor_evidence must be an object when present")
    elif isinstance(auditor_evidence, dict):
        if "assets" in auditor_evidence and not isinstance(auditor_evidence.get("assets"), dict):
            errors.append("auditor_evidence.assets must be an object when present")
        if "asset_set_gate" in auditor_evidence and not isinstance(auditor_evidence.get("asset_set_gate"), dict):
            errors.append("auditor_evidence.asset_set_gate must be an object when present")

    for name in ["production_freeze", "frontend_fidelity", "demo_runtime_evidence", "demo"]:
        value = state.get(name)
        if value is not None and not isinstance(value, dict):
            errors.append(f"{name} must be an object when present")

    return _gate("FAIL" if errors else "PASS", *errors)


def _schema_failure_result(schema_gate: dict[str, Any]) -> dict[str, Any]:
    gates = {"SCHEMA_GATE": schema_gate}
    for name in GATE_NAMES[1:]:
        gates[name] = _gate("N/A", "skipped because SCHEMA_GATE failed")
    return {
        "overall_status": "FAIL",
        "gates": gates,
        "note": "semantic gates were not evaluated because the state schema is invalid",
    }


def _demo_required(state: dict[str, Any]) -> bool:
    # Delivery State 0.2 is the Demo-delivery schema. This is a workflow rule,
    # not a caller-controlled switch; `pre_9_required=false` cannot disable it.
    return state.get("schema_version") == "0.2"


def _required_asset_ids(state: dict[str, Any]) -> set[str]:
    """Union every authoritative place that can require a final asset.

    No non-empty source overrides another. Freeze lists may add blockers/revisions
    so a still-required blocked asset cannot disappear during handoff.
    """
    result: set[str] = set()
    for module in (state.get("locked_module_plan") or {}).get("modules", []):
        if isinstance(module, dict):
            for asset_id in module.get("asset_ids", []):
                if isinstance(asset_id, str) and asset_id:
                    result.add(asset_id)
    for slot in (state.get("implementation") or {}).get("slots", []):
        if isinstance(slot, dict):
            for asset_id in slot.get("asset_ids", []):
                if isinstance(asset_id, str) and asset_id:
                    result.add(asset_id)
    for contract in state.get("asset_slot_contract", []):
        if isinstance(contract, dict):
            for asset_id in contract.get("required_asset_ids", []):
                if isinstance(asset_id, str) and asset_id:
                    result.add(asset_id)
    for asset_id in state.get("required_asset_ids", []):
        if isinstance(asset_id, str) and asset_id:
            result.add(asset_id)
    freeze = state.get("production_freeze") or {}
    if isinstance(freeze, dict):
        for key in ["user_approved_assets", "blocked_assets", "revision_pending"]:
            for asset_id in freeze.get(key, []):
                if isinstance(asset_id, str) and asset_id:
                    result.add(asset_id)
    return result


# Core evidence helpers resolve this symbol dynamically in their own module.
# Replace it so legacy core gates use the fail-closed union as well.
_core._required_asset_ids = _required_asset_ids


def _production_freeze_gate(state: dict[str, Any]) -> dict[str, Any]:
    if not _demo_required(state):
        return _gate("N/A", "production freeze hard gate applies to Demo Delivery State 0.2")

    errors: list[str] = []
    checkpoints = state.get("audit_checkpoints") or {}
    if checkpoints.get("pre_9_required") is not True:
        errors.append("pre_9_required cannot disable mandatory Demo hardening")

    required_ids = _required_asset_ids(state)
    if not required_ids:
        errors.append("Demo delivery requires a non-empty required asset set")

    freeze = state.get("production_freeze")
    if not isinstance(freeze, dict):
        return _gate("FAIL", *(errors + ["production_freeze missing before pre-demo hardening"]))

    expected = freeze.get("expected_assets")
    approved = freeze.get("user_approved_assets")
    blocked = freeze.get("blocked_assets")
    revision_pending = freeze.get("revision_pending")
    set_qa_status = freeze.get("set_qa_status")
    ready = freeze.get("ready_for_hardening")
    approved_outputs = freeze.get("approved_outputs")

    if not isinstance(expected, int) or isinstance(expected, bool) or expected < 1:
        errors.append("production_freeze expected_assets must be a positive integer")
    if isinstance(expected, int) and not isinstance(expected, bool) and expected != len(required_ids):
        errors.append(f"production_freeze expected_assets {expected} does not match required asset count {len(required_ids)}")

    if not isinstance(approved, list) or any(not isinstance(asset_id, str) or not asset_id for asset_id in approved):
        errors.append("production_freeze user_approved_assets must be a list of Asset IDs")
        approved = []
    if len(set(approved)) != len(approved):
        errors.append("production_freeze user_approved_assets must not contain duplicates")
    approved_set = set(approved)
    if approved_set != required_ids:
        missing = sorted(required_ids - approved_set)
        unexpected = sorted(approved_set - required_ids)
        detail = []
        if missing:
            detail.append("missing required assets: " + ", ".join(missing))
        if unexpected:
            detail.append("unexpected approved assets: " + ", ".join(unexpected))
        errors.append("production_freeze approved Asset IDs must equal the required asset set" + (f" ({'; '.join(detail)})" if detail else ""))

    if not isinstance(blocked, list):
        errors.append("production_freeze blocked_assets must be a list")
    elif blocked:
        errors.append("production_freeze contains blocked_assets: " + ", ".join(str(x) for x in blocked))
    if not isinstance(revision_pending, list):
        errors.append("production_freeze revision_pending must be a list")
    elif revision_pending:
        errors.append("production_freeze contains revision_pending assets: " + ", ".join(str(x) for x in revision_pending))
    if set_qa_status not in {"CLEAR", "USER_ACCEPTED"}:
        errors.append(f"production_freeze set_qa_status must be CLEAR or USER_ACCEPTED, got {set_qa_status!r}")
    if ready is not True:
        errors.append("production_freeze ready_for_hardening must be true")

    if not isinstance(approved_outputs, dict):
        errors.append("production_freeze approved_outputs must map each Asset ID to candidate_id/output_ref")
        approved_outputs = {}
    if set(approved_outputs) != required_ids:
        errors.append("production_freeze approved_outputs keys must equal the required asset set")
    seen_refs: set[str] = set()
    for asset_id in sorted(required_ids):
        row = approved_outputs.get(asset_id)
        if not isinstance(row, dict):
            errors.append(f"production_freeze approved_outputs[{asset_id}] must be an object")
            continue
        candidate_id = row.get("candidate_id")
        output_ref = row.get("output_ref")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            errors.append(f"production_freeze approved_outputs[{asset_id}].candidate_id missing")
        if not isinstance(output_ref, str) or not output_ref.strip():
            errors.append(f"production_freeze approved_outputs[{asset_id}].output_ref missing")
        elif output_ref in seen_refs:
            errors.append(f"production_freeze duplicate output_ref without explicit reuse authorization: {output_ref}")
        else:
            seen_refs.add(output_ref)

    return _gate("FAIL" if errors else "PASS", *errors)


def _asset_slot_gate(state: dict[str, Any]) -> dict[str, Any]:
    base = _core._asset_slot_gate(state)
    errors = list(base.get("messages", [])) if base.get("status") == "FAIL" else []
    required_ids = _required_asset_ids(state)
    assets = {
        row.get("asset_id")
        for row in state.get("assets", [])
        if isinstance(row, dict) and isinstance(row.get("asset_id"), str) and row.get("asset_id")
    }
    missing_assets = sorted(required_ids - assets)
    if missing_assets:
        errors.append("required assets missing from Delivery State assets: " + ", ".join(missing_assets))

    contracts = {
        row.get("slot_id")
        for row in state.get("asset_slot_contract", [])
        if isinstance(row, dict) and isinstance(row.get("slot_id"), str) and row.get("slot_id")
    }
    for slot in (state.get("implementation") or {}).get("slots", []):
        if not isinstance(slot, dict) or not slot.get("asset_ids"):
            continue
        slot_id = slot.get("slot_id")
        if isinstance(slot_id, str) and slot_id and slot_id not in contracts:
            errors.append(f"{slot_id}: implemented asset-bearing slot has no asset-slot contract")

    if errors:
        return _gate("FAIL", *errors)
    if base.get("status") == "N/A" and required_ids:
        return _gate("FAIL", "required assets exist but asset-slot contract is empty")
    return base


def _pre_demo_asset_gate(state: dict[str, Any]) -> dict[str, Any]:
    if not _demo_required(state):
        return _gate("N/A", "pre-Demo evidence hard gate applies to Delivery State 0.2")
    errors: list[str] = []
    checkpoints = state.get("audit_checkpoints") or {}
    if checkpoints.get("pre_9_required") is not True:
        errors.append("pre_9_required cannot disable mandatory Demo evidence audit")

    required_ids = _required_asset_ids(state)
    if not required_ids:
        errors.append("Demo delivery requires a non-empty required asset set")

    evidence = state.get("auditor_evidence")
    if not isinstance(evidence, dict):
        return _gate("UNVERIFIED", *(errors + ["pre-9 auditor evidence missing"]))
    if evidence.get("checkpoint") != "pre-9":
        errors.append("auditor evidence checkpoint must be pre-9")
    for asset_id in sorted(required_ids):
        usable, reason = _core._effective_asset_usable(state, asset_id)
        if not usable:
            errors.append(f"{asset_id}: {reason}")
    set_gate = evidence.get("asset_set_gate") or {}
    if set_gate.get("status") != "PASS":
        errors.append(f"auditor asset_set_gate must PASS, got {set_gate.get('status')!r}")
        errors.extend(str(message) for message in set_gate.get("messages", []))
    return _gate("FAIL" if errors else "PASS", *errors)


def _frontend_fidelity_payload(value: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "mode", "evidence_refs", "shell_supported", "section_order_supported",
        "regions_distinguished", "desktop_structure_known", "mobile_behavior",
        "interactions_supported", "content_regions_verified", "unsupported_ui_fabricated",
    ]
    return {key: value.get(key) for key in keys}


def _frontend_fidelity_gate(state: dict[str, Any]) -> dict[str, Any]:
    if not _demo_required(state):
        return _gate("N/A", "frontend fidelity gate applies to Demo Delivery State 0.2")
    value = state.get("frontend_fidelity")
    if not isinstance(value, dict):
        return _gate("UNVERIFIED", "frontend_fidelity evidence missing")
    mode = value.get("mode")
    refs = value.get("evidence_refs")
    if not isinstance(refs, list) or not refs or any(not isinstance(x, str) or not x.strip() for x in refs):
        return _gate("UNVERIFIED", "frontend_fidelity requires non-empty evidence_refs")

    errors: list[str] = []
    if mode == "CHANNEL_NATIVE":
        for key in ["shell_supported", "section_order_supported", "regions_distinguished", "desktop_structure_known", "interactions_supported", "content_regions_verified"]:
            if value.get(key) is not True:
                errors.append(f"frontend_fidelity {key} must be true for CHANNEL_NATIVE")
        if value.get("mobile_behavior") not in {"KNOWN", "SCOPED_OUT"}:
            errors.append("frontend_fidelity mobile_behavior must be KNOWN or SCOPED_OUT")
        if value.get("unsupported_ui_fabricated") is not False:
            errors.append("frontend_fidelity unsupported_ui_fabricated must be false")
    elif mode == "CONTENT_REVIEW":
        if value.get("content_review_labeled") is not True:
            errors.append("CONTENT_REVIEW mode must be explicitly labeled")
        if value.get("channel_native_claimed") is True:
            errors.append("CONTENT_REVIEW mode cannot claim channel-native fidelity")
    else:
        errors.append("frontend_fidelity mode must be CHANNEL_NATIVE or CONTENT_REVIEW")

    approval_id = value.get("approval_id")
    payload_hash = canonical_hash(_frontend_fidelity_payload(value))
    approval = _core._approval_index(state).get(approval_id) if isinstance(approval_id, str) else None
    ok, reason = _core._valid_user_approval(approval, "frontend_fidelity", payload_hash)
    if not ok:
        errors.append(f"frontend_fidelity approval invalid: {reason}")
    return _gate("FAIL" if errors else "PASS", *errors)


def _demo_runtime_gate(state: dict[str, Any]) -> dict[str, Any]:
    if not _demo_required(state):
        return _gate("N/A", "runtime Demo gate applies to Delivery State 0.2")
    demo_info = state.get("demo")
    evidence = state.get("demo_runtime_evidence")
    if not isinstance(demo_info, dict) or not isinstance(demo_info.get("sha256"), str) or not HEX64.match(demo_info.get("sha256", "")):
        return _gate("UNVERIFIED", "Demo exact SHA-256 missing from Delivery State")
    if not isinstance(evidence, dict):
        return _gate("UNVERIFIED", "browser runtime evidence missing")
    errors: list[str] = []
    if evidence.get("demo_sha256") != demo_info.get("sha256"):
        errors.append("runtime evidence demo_sha256 does not match exact Demo SHA-256")
    if evidence.get("validator") != "browser-runtime":
        errors.append("runtime evidence validator must be browser-runtime")
    if evidence.get("network_requests") != 0:
        errors.append("runtime Demo must make zero network requests")
    viewports = evidence.get("viewports")
    if not isinstance(viewports, dict):
        errors.append("runtime evidence viewports missing")
    else:
        for key in ["1440", "390"]:
            row = viewports.get(key)
            if not isinstance(row, dict):
                errors.append(f"runtime viewport {key}px missing")
                continue
            if row.get("horizontal_overflow") is not False:
                errors.append(f"runtime viewport {key}px has horizontal overflow or unknown state")
            if row.get("broken_images") != 0:
                errors.append(f"runtime viewport {key}px has broken images or unknown state")
            if row.get("clipped_primary_elements") != 0:
                errors.append(f"runtime viewport {key}px has clipped primary elements or unknown state")
    carousel = evidence.get("carousel")
    if isinstance(carousel, dict) and carousel.get("present") is True:
        if carousel.get("next_verified") is not True or carousel.get("prev_verified") is not True:
            errors.append("runtime carousel must verify both next and previous transitions")
    return _gate("FAIL" if errors else "PASS", *errors)


def validate_state(state: Any, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    schema_gate = _schema_gate(state)
    if schema_gate["status"] == "FAIL":
        return _schema_failure_result(schema_gate)

    loaded_policy = policy if policy is not None else _core._load_policy()
    gates = {
        "SCHEMA_GATE": schema_gate,
        "CHANNEL_MODULE_BUDGET_GATE": _core._channel_module_budget_gate(state, loaded_policy),
        "APPROVAL_PROVENANCE_GATE": _core._approval_provenance_gate(state),
        "MODULE_ORIGIN_GATE": _core._module_origin_gate(state),
        "TRANSFORM_AUTH_GATE": _core._transform_auth_gate(state),
        "EVIDENCE_RECONCILIATION_GATE": _core._evidence_reconciliation_gate(state),
        "PRODUCTION_FREEZE_GATE": _production_freeze_gate(state),
        "ASSET_SLOT_GATE": _asset_slot_gate(state),
        "PRE_DEMO_ASSET_GATE": _pre_demo_asset_gate(state),
        "FRONTEND_FIDELITY_GATE": _frontend_fidelity_gate(state),
        "DEMO_RUNTIME_GATE": _demo_runtime_gate(state),
        "DELIVERY_PARITY_GATE": _core._delivery_parity_gate(state),
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
        "note": "v0.3.3 fail-closed: Demo audit/Freeze/frontend/runtime gates are recomputed; caller switches and declared results cannot create PASS",
    }


def _print_result(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return
    print(f"OVERALL: {result['overall_status']}")
    for name, gate in result["gates"].items():
        print(f"{name}: {gate['status']}")
        for message in gate["messages"]:
            print(f"  - {message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate listing Delivery State / Project State compatibility")
    parser.add_argument("state", type=Path, help="Path to delivery/project-state JSON")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY_PATH, help="Channel policy limits JSON")
    parser.add_argument("--json", action="store_true", help="Print machine-readable result JSON")
    args = parser.parse_args()

    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = _schema_failure_result(_gate("FAIL", f"invalid state JSON: {exc}"))
        _print_result(result, args.json)
        return 1
    try:
        policy = _core._load_policy(args.policy)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = _schema_failure_result(_gate("FAIL", f"invalid channel policy JSON: {exc}"))
        _print_result(result, args.json)
        return 1

    result = validate_state(state, policy)
    _print_result(result, args.json)
    if result["overall_status"] == "PASS":
        return 0
    if result["overall_status"] == "UNVERIFIED":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
