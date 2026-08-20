#!/usr/bin/env python3
"""Regression tests for the listing-hardening Skill."""

import importlib.util
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
OLD_VALIDATOR = REPO_ROOT / ".agents" / "skills" / "japan-listing-demo" / "scripts" / "validate_project_state.py"
NEW_VALIDATOR = SKILL_DIR / "scripts" / "validate_delivery_state.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def minimal_valid_state(schema_version: str = "0.1") -> dict:
    validator = load_module(NEW_VALIDATOR, f"validator_fixture_{schema_version.replace('.', '_')}")
    asset_payload = {
        "asset_id": "A01",
        "canonical_source": "assets/a01.png",
        "sha256": "a" * 64,
        "role": "enhanced-content",
        "page_offer_scope": ["single"],
        "allowed_slots": ["M01"],
    }
    asset_hash = validator.canonical_hash(asset_payload)
    module = {
        "module_id": "M01",
        "native_type": "premium_full_image",
        "interaction": "static",
        "asset_ids": ["A01"],
        "approved_stage": "7",
    }
    plan_hash = validator.canonical_hash({"modules": [module]})
    return {
        "schema_version": schema_version,
        "channel": {"id": "amazon-jp", "enhanced_content": {"tier": "premium", "declared_max_modules": 7}},
        "approval_events": [
            {"approval_id": "AP-ASSET", "actor": "user", "source_ref": "checkpoint:asset", "scope": "asset_lock:A01", "stage": "8", "approved_hash": asset_hash},
            {"approval_id": "AP-PLAN", "actor": "user", "source_ref": "checkpoint:plan", "scope": "module_plan", "stage": "7", "approved_hash": plan_hash},
        ],
        "assets": [{**asset_payload, "status": "LOCKED", "approval_id": "AP-ASSET"}],
        "locked_module_plan": {"status": "LOCKED", "approval_id": "AP-PLAN", "plan_hash": plan_hash, "modules": [module]},
        "asset_slot_contract": [{"slot_id": "M01", "module_id": "M01", "required_asset_ids": ["A01"], "interaction": "static"}],
        "implementation": {"plan_hash": plan_hash, "slots": [{"slot_id": "M01", "module_id": "M01", "native_type": "premium_full_image", "interaction": "static", "asset_ids": ["A01"]}]},
    }


def verified_pre_demo_evidence() -> dict:
    return {
        "checkpoint": "pre-9",
        "independent_semantic": True,
        "asset_set_gate": {"status": "PASS", "messages": []},
        "assets": {"A01": {"physical_sha256": "a" * 64, "effective_status": "VERIFIED"}},
    }


def test_hardening_owns_only_final_delivery_plane() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    for phrase in [
        "name: listing-hardening", "stage 8.5", "stage 9", "stage 10",
        "production freeze", "listing-evidence-auditor", "delivery state",
    ]:
        assert phrase in text
    for forbidden in ["consumer strategy", "voc research", "visual generation brief"]:
        assert forbidden not in text


def test_full_audit_is_mandatory_at_stage_8_5_not_fresh_stage_6_5() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "mandatory full audit" in text
    assert "stage 8.5" in text
    assert "targeted early audit" in text
    assert "inherited" in text or "previously approved exact asset" in text


def test_new_validator_exists_and_matches_legacy_api() -> None:
    old = load_module(OLD_VALIDATOR, "legacy_validator")
    new = load_module(NEW_VALIDATOR, "hardening_validator")
    assert callable(new.canonical_hash)
    assert callable(new.validate_state)
    assert new.canonical_hash({"b": 2, "a": 1}) == old.canonical_hash({"b": 2, "a": 1})


def test_fresh_project_does_not_require_post_6_5_audit() -> None:
    validator = load_module(NEW_VALIDATOR, "fresh_project_validator")
    state = minimal_valid_state()
    state["audit_checkpoints"] = {"post_6_5_required": False, "pre_9_required": False}
    result = validator.validate_state(state)
    assert result["gates"]["EVIDENCE_RECONCILIATION_GATE"]["status"] == "N/A"


def test_targeted_inherited_asset_audit_is_enforced_when_requested() -> None:
    validator = load_module(NEW_VALIDATOR, "targeted_audit_validator")
    state = minimal_valid_state()
    state["audit_checkpoints"] = {"post_6_5_required": True}
    result = validator.validate_state(state)
    assert result["gates"]["EVIDENCE_RECONCILIATION_GATE"]["status"] == "UNVERIFIED"


def test_pre_demo_audit_remains_mandatory_when_required() -> None:
    validator = load_module(NEW_VALIDATOR, "pre_demo_validator")
    state = minimal_valid_state()
    state["audit_checkpoints"] = {"pre_9_required": True}
    result = validator.validate_state(state)
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] == "UNVERIFIED"


def test_delivery_state_v02_requires_complete_production_freeze_before_pre_demo() -> None:
    validator = load_module(NEW_VALIDATOR, "delivery_state_validator")
    state = minimal_valid_state("0.2")
    state["audit_checkpoints"] = {"pre_9_required": True}
    state["production_freeze"] = {
        "expected_assets": 1,
        "user_approved_assets": [],
        "approved_output_refs": [],
    }
    state["auditor_evidence"] = verified_pre_demo_evidence()
    result = validator.validate_state(state)
    assert result["gates"]["SCHEMA_GATE"]["status"] == "PASS"
    assert result["gates"]["PRODUCTION_FREEZE_GATE"]["status"] == "FAIL"
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] == "PASS"


def test_complete_production_freeze_and_verified_assets_pass_both_gates() -> None:
    validator = load_module(NEW_VALIDATOR, "delivery_state_complete_validator")
    state = minimal_valid_state("0.2")
    state["audit_checkpoints"] = {"pre_9_required": True}
    state["production_freeze"] = {
        "expected_assets": 1,
        "user_approved_assets": ["A01"],
        "approved_output_refs": ["file:a01"],
    }
    state["auditor_evidence"] = verified_pre_demo_evidence()
    result = validator.validate_state(state)
    assert result["gates"]["PRODUCTION_FREEZE_GATE"]["status"] == "PASS"
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] == "PASS"


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-hardening tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
