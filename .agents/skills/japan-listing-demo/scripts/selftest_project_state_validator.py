#!/usr/bin/env python3
"""Regression tests for validate_project_state.py."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate_project_state import canonical_hash, validate_state  # noqa: E402


def approval(approval_id: str, scope: str, approved_hash: str, stage: str = "7") -> dict:
    return {
        "approval_id": approval_id,
        "actor": "user",
        "source_ref": f"checkpoint:{approval_id}",
        "scope": scope,
        "stage": stage,
        "approved_hash": approved_hash,
    }


def base_state() -> dict:
    asset_payload = {
        "asset_id": "A01",
        "canonical_source": "assets/a01.png",
        "sha256": "a" * 64,
        "role": "enhanced-content",
        "page_offer_scope": ["single"],
        "allowed_slots": ["M01"],
    }
    asset_hash = canonical_hash(asset_payload)

    module = {
        "module_id": "M01",
        "native_type": "premium_full_image",
        "interaction": "static",
        "asset_ids": ["A01"],
        "approved_stage": "7",
    }
    plan_payload = {"modules": [module]}
    plan_hash = canonical_hash(plan_payload)

    state = {
        "schema_version": "0.1",
        "channel": {
            "id": "amazon-jp",
            "enhanced_content": {"tier": "premium", "declared_max_modules": 7},
        },
        "approval_events": [
            approval("AP-ASSET-A01", "asset_lock:A01", asset_hash, "6.5"),
            approval("AP-MODULE-PLAN", "module_plan", plan_hash, "7"),
        ],
        "assets": [
            {
                **asset_payload,
                "status": "LOCKED",
                "approval_id": "AP-ASSET-A01",
            }
        ],
        "locked_module_plan": {
            "status": "LOCKED",
            "approval_id": "AP-MODULE-PLAN",
            "plan_hash": plan_hash,
            "modules": [module],
        },
        "asset_slot_contract": [
            {
                "slot_id": "M01",
                "module_id": "M01",
                "required_asset_ids": ["A01"],
                "interaction": "static",
            }
        ],
        "implementation": {
            "plan_hash": plan_hash,
            "slots": [
                {
                    "slot_id": "M01",
                    "module_id": "M01",
                    "native_type": "premium_full_image",
                    "interaction": "static",
                    "asset_ids": ["A01"],
                }
            ],
        },
        "declared_gate_results": {"CHANNEL_MODULE_BUDGET_GATE": "PASS"},
    }
    return state


def assert_status(result: dict, gate: str, expected: str) -> None:
    actual = result["gates"][gate]["status"]
    if actual != expected:
        raise AssertionError(f"{gate}: expected {expected}, got {actual}: {result['gates'][gate]}")


def test_valid_state_passes() -> None:
    result = validate_state(base_state())
    for gate in [
        "CHANNEL_MODULE_BUDGET_GATE",
        "APPROVAL_PROVENANCE_GATE",
        "MODULE_ORIGIN_GATE",
        "TRANSFORM_AUTH_GATE",
        "ASSET_SLOT_GATE",
        "DELIVERY_PARITY_GATE",
    ]:
        assert_status(result, gate, "PASS")
    if result["overall_status"] != "PASS":
        raise AssertionError(result)


def test_ten_premium_modules_fail_budget_even_if_declared_pass() -> None:
    state = base_state()
    modules = []
    slots = []
    for i in range(1, 11):
        module_id = f"M{i:02d}"
        modules.append({
            "module_id": module_id,
            "native_type": "premium_full_image",
            "interaction": "static",
            "asset_ids": [],
            "approved_stage": "7",
        })
        slots.append({
            "slot_id": module_id,
            "module_id": module_id,
            "native_type": "premium_full_image",
            "interaction": "static",
            "asset_ids": [],
        })
    payload = {"modules": modules}
    plan_hash = canonical_hash(payload)
    state["locked_module_plan"].update({"modules": modules, "plan_hash": plan_hash})
    state["approval_events"][1]["approved_hash"] = plan_hash
    state["implementation"] = {"plan_hash": plan_hash, "slots": slots}
    state["asset_slot_contract"] = []
    state["declared_gate_results"] = {"CHANNEL_MODULE_BUDGET_GATE": "PASS"}
    result = validate_state(state)
    assert_status(result, "CHANNEL_MODULE_BUDGET_GATE", "FAIL")


def test_unplanned_module_fails_origin() -> None:
    state = base_state()
    state["implementation"]["slots"].append({
        "slot_id": "M02",
        "module_id": "M02",
        "native_type": "premium_full_image",
        "interaction": "static",
        "asset_ids": [],
    })
    result = validate_state(state)
    assert_status(result, "MODULE_ORIGIN_GATE", "FAIL")


def test_interaction_drift_fails_origin_and_parity() -> None:
    state = base_state()
    state["implementation"]["slots"][0]["interaction"] = "navigation_carousel"
    result = validate_state(state)
    assert_status(result, "MODULE_ORIGIN_GATE", "FAIL")
    assert_status(result, "DELIVERY_PARITY_GATE", "FAIL")


def test_derivative_without_transform_approval_fails() -> None:
    state = base_state()
    derivative_payload = {
        "asset_id": "A01-C1",
        "canonical_source": "assets/a01-c1.png",
        "sha256": "b" * 64,
        "role": "enhanced-content-pane",
        "page_offer_scope": ["single"],
        "allowed_slots": ["M01"],
    }
    state["assets"].append({
        **derivative_payload,
        "status": "LOCKED",
        "derivative_of": "A01",
        "transform": {"type": "crop", "target_slot": "M01"},
        "approval_id": "AP-ASSET-A01",
    })
    state["locked_module_plan"]["modules"][0]["asset_ids"] = ["A01-C1"]
    payload = {"modules": state["locked_module_plan"]["modules"]}
    new_hash = canonical_hash(payload)
    state["locked_module_plan"]["plan_hash"] = new_hash
    state["approval_events"][1]["approved_hash"] = new_hash
    state["implementation"]["plan_hash"] = new_hash
    state["implementation"]["slots"][0]["asset_ids"] = ["A01-C1"]
    state["asset_slot_contract"][0]["required_asset_ids"] = ["A01-C1"]
    result = validate_state(state)
    assert_status(result, "TRANSFORM_AUTH_GATE", "FAIL")


def test_missing_asset_lock_approval_fails_provenance() -> None:
    state = base_state()
    state["assets"][0].pop("approval_id")
    result = validate_state(state)
    assert_status(result, "APPROVAL_PROVENANCE_GATE", "FAIL")


def test_exact_hash_recovery_passes_without_new_creative_approval() -> None:
    state = base_state()
    state["assets"][0].pop("approval_id")
    state["assets"][0]["recovery"] = {
        "type": "recovered_exact",
        "previous_locked_sha256": "a" * 64,
        "matches_previous_locked_sha": True,
    }
    result = validate_state(state)
    assert_status(result, "APPROVAL_PROVENANCE_GATE", "PASS")


def test_filename_similarity_is_not_exact_recovery() -> None:
    state = base_state()
    state["assets"][0].pop("approval_id")
    state["assets"][0]["recovery"] = {
        "type": "recovered_exact",
        "previous_locked_sha256": "c" * 64,
        "matches_previous_locked_sha": False,
        "note": "same filename",
    }
    result = validate_state(state)
    assert_status(result, "APPROVAL_PROVENANCE_GATE", "FAIL")


def main() -> int:
    tests = [name for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for name in sorted(tests):
        globals()[name]()
    print(f"PASS: {len(tests)} executable project-state validator tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
