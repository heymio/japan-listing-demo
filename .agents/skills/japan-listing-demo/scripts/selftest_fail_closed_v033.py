#!/usr/bin/env python3
"""Adversarial RED-first regressions for v0.3.3 fail-closed hardening."""

from __future__ import annotations

import importlib.util
import struct
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

MAIN_SKILL = Path(__file__).resolve().parents[1]
REPO_ROOT = MAIN_SKILL.parents[2]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
HARDENING_DIR = SKILLS_ROOT / "listing-hardening"
PRODUCTION_DIR = SKILLS_ROOT / "listing-production"
AUDITOR_DIR = SKILLS_ROOT / "listing-evidence-auditor"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, path
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


hardening = load_module(HARDENING_DIR / "scripts" / "validate_delivery_state.py", "v033_hardening")
hardening_fixtures = load_module(HARDENING_DIR / "scripts" / "selftest_hardening.py", "v033_hardening_fixtures")
production = load_module(PRODUCTION_DIR / "scripts" / "production_state.py", "v033_production")
auditor = load_module(AUDITOR_DIR / "scripts" / "fingerprint_assets.py", "v033_auditor")
demo = load_module(HARDENING_DIR / "scripts" / "validate_demo_html.py", "v033_demo")


def valid_freeze_old_shape() -> dict:
    return {
        "expected_assets": 1,
        "user_approved_assets": ["A01"],
        "approved_output_refs": ["file:a01"],
    }


def valid_demo() -> str:
    return """<!doctype html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>img{max-width:100%;height:auto}@media(max-width:600px){body{margin:0}}</style></head>
<body><section data-carousel><button data-carousel-prev>Prev</button>
<div data-carousel-slide><img src="data:image/png;base64,iVBORw0KGgo="></div>
<div data-carousel-slide><img src="data:image/png;base64,iVBORw0KGgo="></div>
<button data-carousel-next>Next</button></section>
<script>document.querySelector('[data-carousel-prev]').addEventListener('click',()=>{});document.querySelector('[data-carousel-next]').addEventListener('click',()=>{});</script>
</body></html>"""


def test_pre9_audit_cannot_be_disabled_for_demo_delivery() -> None:
    state = hardening_fixtures.minimal_valid_state("0.2")
    state["audit_checkpoints"] = {"post_6_5_required": False, "pre_9_required": False}
    state["production_freeze"] = valid_freeze_old_shape()
    state["auditor_evidence"] = hardening_fixtures.verified_pre_demo_evidence()
    result = hardening.validate_state(state)
    assert result["overall_status"] != "PASS", result
    assert result["gates"]["PRODUCTION_FREEZE_GATE"]["status"] != "N/A", result
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] != "N/A", result


def test_empty_demo_asset_set_cannot_pass() -> None:
    state = {
        "schema_version": "0.2",
        "channel": {"id": "amazon-jp", "enhanced_content": {"tier": "premium", "declared_max_modules": 7}},
        "approval_events": [],
        "assets": [],
        "locked_module_plan": {},
        "asset_slot_contract": [],
        "implementation": {},
        "audit_checkpoints": {"post_6_5_required": False, "pre_9_required": True},
        "production_freeze": {"expected_assets": 0, "user_approved_assets": [], "approved_output_refs": []},
        "auditor_evidence": {"checkpoint": "pre-9", "asset_set_gate": {"status": "PASS", "messages": []}, "assets": {}},
    }
    result = hardening.validate_state(state)
    assert result["overall_status"] != "PASS", result


def test_required_asset_set_is_union_not_contract_override() -> None:
    state = hardening_fixtures.minimal_valid_state("0.2")
    module2 = {
        "module_id": "M02",
        "native_type": "premium_full_image",
        "interaction": "static",
        "asset_ids": ["A02"],
        "approved_stage": "7",
    }
    state["locked_module_plan"]["modules"].append(module2)
    plan_hash = hardening.canonical_hash({"modules": state["locked_module_plan"]["modules"]})
    state["locked_module_plan"]["plan_hash"] = plan_hash
    state["approval_events"][1]["approved_hash"] = plan_hash
    state["implementation"]["plan_hash"] = plan_hash
    state["implementation"]["slots"].append({
        "slot_id": "M02",
        "module_id": "M02",
        "native_type": "premium_full_image",
        "interaction": "static",
        "asset_ids": ["A02"],
    })
    state["audit_checkpoints"] = {"post_6_5_required": False, "pre_9_required": True}
    state["production_freeze"] = valid_freeze_old_shape()
    state["auditor_evidence"] = hardening_fixtures.verified_pre_demo_evidence()
    result = hardening.validate_state(state)
    assert result["overall_status"] != "PASS", result
    text = str(result).casefold()
    assert "a02" in text, result


def test_freeze_cannot_pass_with_blockers_stale_setqa_or_not_ready() -> None:
    state = hardening_fixtures.minimal_valid_state("0.2")
    state["audit_checkpoints"] = {"post_6_5_required": False, "pre_9_required": True}
    state["production_freeze"] = {
        **valid_freeze_old_shape(),
        "blocked_assets": ["A01"],
        "revision_pending": ["A01"],
        "set_qa_status": "STALE",
        "ready_for_hardening": False,
    }
    state["auditor_evidence"] = hardening_fixtures.verified_pre_demo_evidence()
    result = hardening.validate_state(state)
    assert result["gates"]["PRODUCTION_FREEZE_GATE"]["status"] == "FAIL", result


def test_production_freeze_binds_asset_candidate_and_output_ref() -> None:
    handoff = {
        "asset_set": [{"asset_id": "A01"}],
        "page_visual_system": {"asset_directions": [{"asset_id": "A01"}]},
    }
    ledger = {
        "assets": {
            "A01": {
                "status": "USER_APPROVED",
                "selected_candidate_id": "A01-v2",
                "current_output_ref": "file:a01-v2",
            }
        },
        "set_qa": {
            "status": "CLEAR",
            "reviewed_asset_ids": ["A01"],
            "reviewed_output_refs": {"A01": "file:a01-v2"},
            "visual_review_ref": "contact-sheet:final",
        },
    }
    freeze = production.build_production_freeze(handoff, ledger)
    assert freeze.get("approved_outputs") == {
        "A01": {"candidate_id": "A01-v2", "output_ref": "file:a01-v2"}
    }, freeze


def test_frontend_fidelity_and_demo_runtime_are_canonical_gates() -> None:
    state = hardening_fixtures.minimal_valid_state("0.2")
    state["audit_checkpoints"] = {"post_6_5_required": False, "pre_9_required": True}
    state["production_freeze"] = valid_freeze_old_shape()
    state["auditor_evidence"] = hardening_fixtures.verified_pre_demo_evidence()
    result = hardening.validate_state(state)
    assert "FRONTEND_FIDELITY_GATE" in result["gates"], result
    assert "DEMO_RUNTIME_GATE" in result["gates"], result
    assert result["gates"]["FRONTEND_FIDELITY_GATE"]["status"] != "PASS", result
    assert result["gates"]["DEMO_RUNTIME_GATE"]["status"] != "PASS", result


def test_truncated_png_is_not_physically_valid() -> None:
    truncated = b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", 1, 1)
    assert len(truncated) == 24
    with TemporaryDirectory() as directory:
        root = Path(directory)
        path = root / "truncated.png"
        path.write_bytes(truncated)
        result = auditor.fingerprint_asset(path, root)
    assert result["errors"], result


def test_svg_external_image_and_inline_style_url_are_rejected() -> None:
    html = valid_demo().replace(
        "<body>",
        '<body><svg><image href="https://example.com/external.png"></image></svg><div style="background:url(https://example.com/bg.png)">x</div>',
        1,
    )
    result = demo.validate_html_text(html)
    assert result["status"] == "FAIL", result


def test_dead_carousel_keywords_do_not_count_as_hard_interaction_verification() -> None:
    html = valid_demo().replace(
        "document.querySelector('[data-carousel-prev]').addEventListener('click',()=>{});document.querySelector('[data-carousel-next]').addEventListener('click',()=>{});",
        "const unused = \"data-carousel data-carousel-prev data-carousel-next addEventListener 'click'\";",
    )
    result = demo.validate_html_text(html)
    assert result.get("checks", {}).get("carousel_contract") != "PASS", result


def test_proof_visual_without_claim_source_binding_is_rejected() -> None:
    packet = {
        "audit_version": "1",
        "project_id": "fixture",
        "checkpoint": "pre-9",
        "assets": [{
            "asset_id": "P01",
            "path": "assets/P01.png",
            "claimed_role": "proof-visual",
            "allowed_slots": ["gallery-02"],
            "claimed_approval_event_id": None,
            "claimed_parent_asset_id": None,
            "claimed_transform": None,
            "evidence_mode": "PROOF_VISUAL",
        }],
        "slots": [{"slot_id": "gallery-02", "required_asset_ids": ["P01"]}],
        "approval_events": [],
        "prior_locked_assets": [],
        "expected_visual_roles": [{"asset_id": "P01", "role": "proof-visual"}],
    }
    try:
        auditor.validate_audit_packet(packet)
    except ValueError as exc:
        assert "claim" in str(exc).casefold() or "source" in str(exc).casefold(), exc
    else:
        raise AssertionError("PROOF_VISUAL without claim/source binding must fail closed")


def test_ambiguous_chinese_phrases_are_not_stage_transition_commands() -> None:
    text = (MAIN_SKILL / "SKILL.md").read_text(encoding="utf-8")
    transition_line = next(line for line in text.splitlines() if line.startswith("Treat `继续`"))
    assert "`先这样`" not in transition_line, transition_line
    assert "`这张先过`" not in transition_line, transition_line


def main() -> int:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} v0.3.3 fail-closed adversarial tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
