#!/usr/bin/env python3
"""v0.3.3 hardening regression suite with complete fail-closed Demo fixtures."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LEGACY_PATH = SCRIPT_DIR / "selftest_hardening_legacy.py"
VALIDATOR_PATH = SCRIPT_DIR / "validate_delivery_state.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


legacy = load(LEGACY_PATH, "listing_hardening_selftest_legacy")
validator = load(VALIDATOR_PATH, "listing_hardening_v033_validator")

# Preserve the fixture helper API consumed by cross-layer adversarial tests.
minimal_valid_state = legacy.minimal_valid_state
verified_pre_demo_evidence = legacy.verified_pre_demo_evidence

MIGRATED = {
    "test_pre_demo_audit_remains_mandatory_when_required",
    "test_delivery_state_v02_requires_complete_production_freeze_before_pre_demo",
    "test_complete_production_freeze_and_verified_assets_pass_both_gates",
    "test_production_freeze_requires_exact_required_asset_id_set",
}


def complete_v033_state() -> dict:
    state = legacy.minimal_valid_state("0.2")
    state["audit_checkpoints"] = {"post_6_5_required": False, "pre_9_required": True}
    state["production_freeze"] = {
        "expected_assets": 1,
        "required_asset_ids": ["A01"],
        "user_approved_assets": ["A01"],
        "blocked_assets": [],
        "revision_pending": [],
        "approved_outputs": {"A01": {"candidate_id": "A01-v1", "output_ref": "file:a01"}},
        "set_qa_status": "CLEAR",
        "ready_for_hardening": True,
    }
    state["auditor_evidence"] = legacy.verified_pre_demo_evidence()

    frontend = {
        "mode": "CHANNEL_NATIVE",
        "evidence_refs": ["frontend:capture-1"],
        "shell_supported": True,
        "section_order_supported": True,
        "regions_distinguished": True,
        "desktop_structure_known": True,
        "mobile_behavior": "KNOWN",
        "interactions_supported": True,
        "content_regions_verified": True,
        "unsupported_ui_fabricated": False,
        "approval_id": "AP-FRONTEND",
    }
    payload_hash = validator.canonical_hash(validator._frontend_fidelity_payload(frontend))
    state["approval_events"].append({
        "approval_id": "AP-FRONTEND",
        "actor": "user",
        "source_ref": "checkpoint:frontend",
        "scope": "frontend_fidelity",
        "stage": "8.5",
        "approved_hash": payload_hash,
    })
    state["frontend_fidelity"] = frontend

    demo_sha = "d" * 64
    state["demo"] = {"sha256": demo_sha, "path": "demo/final.html"}
    state["demo_runtime_evidence"] = {
        "validator": "browser-runtime",
        "demo_sha256": demo_sha,
        "network_requests": 0,
        "viewports": {
            "1440": {"horizontal_overflow": False, "broken_images": 0, "clipped_primary_elements": 0},
            "390": {"horizontal_overflow": False, "broken_images": 0, "clipped_primary_elements": 0},
        },
        "carousel": {"present": True, "next_verified": True, "prev_verified": True},
    }
    return state


def test_pre_demo_audit_remains_mandatory_when_required() -> None:
    state = complete_v033_state()
    state.pop("auditor_evidence")
    result = validator.validate_state(state)
    assert result["overall_status"] != "PASS"
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] in {"UNVERIFIED", "FAIL"}


def test_delivery_state_v02_requires_complete_production_freeze_before_pre_demo() -> None:
    state = complete_v033_state()
    state["production_freeze"] = {
        "expected_assets": 1,
        "required_asset_ids": ["A01"],
        "user_approved_assets": [],
        "blocked_assets": [],
        "revision_pending": ["A01"],
        "approved_outputs": {},
        "set_qa_status": "MISSING",
        "ready_for_hardening": False,
    }
    result = validator.validate_state(state)
    assert result["gates"]["SCHEMA_GATE"]["status"] == "PASS"
    assert result["gates"]["PRODUCTION_FREEZE_GATE"]["status"] == "FAIL"
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] == "PASS"


def test_complete_production_freeze_and_verified_assets_pass_both_gates() -> None:
    state = complete_v033_state()
    result = validator.validate_state(state)
    assert result["overall_status"] == "PASS", result
    for name in [
        "PRODUCTION_FREEZE_GATE", "PRE_DEMO_ASSET_GATE", "FRONTEND_FIDELITY_GATE",
        "DEMO_RUNTIME_GATE", "ASSET_SLOT_GATE", "DELIVERY_PARITY_GATE",
    ]:
        assert result["gates"][name]["status"] == "PASS", (name, result["gates"][name])


def test_production_freeze_requires_exact_required_asset_id_set() -> None:
    state = complete_v033_state()
    state["production_freeze"]["user_approved_assets"] = ["WRONG-ID"]
    state["production_freeze"]["approved_outputs"] = {
        "WRONG-ID": {"candidate_id": "WRONG-v1", "output_ref": "file:wrong"}
    }
    result = validator.validate_state(state)
    gate = result["gates"]["PRODUCTION_FREEZE_GATE"]
    assert gate["status"] == "FAIL"
    assert any("required" in message.casefold() for message in gate["messages"])


def main() -> int:
    tests = []
    for name, value in vars(legacy).items():
        if name.startswith("test_") and callable(value) and name not in MIGRATED:
            tests.append((name, value))
    for name, value in globals().items():
        if name.startswith("test_") and callable(value):
            tests.append((name, value))
    for name, test in sorted(tests):
        test()
    print(f"PASS: {len(tests)} listing-hardening tests (v0.3.3)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
