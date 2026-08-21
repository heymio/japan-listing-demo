#!/usr/bin/env python3
"""Validate machine-checkable listing delivery state with strict schema fail-fast.

v0.3.1 keeps the v0.3.0 gate logic in `_delivery_state_core.py` and adds a
strict entry boundary around it. Malformed state never reaches semantic gates.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
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
            if "asset_ids" in module and not isinstance(module.get("asset_ids"), list):
                errors.append(f"locked_module_plan.modules[{index}].asset_ids must be a list")

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
            if "asset_ids" in slot and not isinstance(slot.get("asset_ids"), list):
                errors.append(f"implementation.slots[{index}].asset_ids must be a list")

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

    production_freeze = state.get("production_freeze")
    if production_freeze is not None and not isinstance(production_freeze, dict):
        errors.append("production_freeze must be an object when present")

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


def _production_freeze_gate(state: dict[str, Any]) -> dict[str, Any]:
    if state.get("schema_version") != "0.2":
        return _gate("N/A", "production freeze gate applies to Delivery State 0.2")
    checkpoints = state.get("audit_checkpoints") or {}
    if checkpoints.get("pre_9_required") is not True:
        return _gate("N/A", "pre-9 hardening not required")

    freeze = state.get("production_freeze")
    if not isinstance(freeze, dict):
        return _gate("FAIL", "production_freeze missing before pre-demo hardening")

    errors: list[str] = []
    expected = freeze.get("expected_assets")
    approved = freeze.get("user_approved_assets")
    output_refs = freeze.get("approved_output_refs")

    if not isinstance(expected, int) or isinstance(expected, bool) or expected < 0:
        errors.append("production_freeze expected_assets must be a non-negative integer")
    if not isinstance(approved, list) or any(not isinstance(asset_id, str) or not asset_id for asset_id in approved):
        errors.append("production_freeze user_approved_assets must be a list of Asset IDs")
        approved = []
    if len(set(approved)) != len(approved):
        errors.append("production_freeze user_approved_assets must not contain duplicates")
    if not isinstance(output_refs, list) or any(not isinstance(ref, str) or not ref for ref in output_refs):
        errors.append("production_freeze approved_output_refs must be a list of output references")
        output_refs = []

    required_ids = _core._required_asset_ids(state)
    if required_ids:
        if isinstance(expected, int) and not isinstance(expected, bool) and expected != len(required_ids):
            errors.append(
                f"production_freeze expected_assets {expected} does not match required asset count {len(required_ids)}"
            )
        approved_set = set(approved)
        if approved_set != required_ids:
            missing = sorted(required_ids - approved_set)
            unexpected = sorted(approved_set - required_ids)
            details: list[str] = []
            if missing:
                details.append(f"missing required assets: {', '.join(missing)}")
            if unexpected:
                details.append(f"unexpected approved assets: {', '.join(unexpected)}")
            errors.append("production_freeze approved Asset IDs must equal the required asset set" + (f" ({'; '.join(details)})" if details else ""))
    elif isinstance(expected, int) and not isinstance(expected, bool) and len(approved) != expected:
        errors.append(f"production freeze approved {len(approved)} of {expected} expected assets")

    if len(output_refs) != len(approved):
        errors.append("production_freeze approved_output_refs count must match approved assets")

    if errors:
        return _gate("FAIL", *errors)
    return _gate("PASS", f"production freeze contains the exact required set of {len(approved)} creatively approved assets")


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
        "ASSET_SLOT_GATE": _core._asset_slot_gate(state),
        "PRE_DEMO_ASSET_GATE": _core._pre_demo_asset_gate(state),
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
        "note": "creative Production Freeze and auditor Evidence Verification are separate; malformed state fails before semantic gates; declared_gate_results is ignored",
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
