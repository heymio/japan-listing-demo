#!/usr/bin/env python3
"""Regression tests for the listing-production Skill."""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from project_asset_packet import project_generation_context, validate_asset_packet  # noqa: E402
from production_state import build_production_freeze, production_progress, set_creative_status  # noqa: E402


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def base_packet() -> dict:
    return {
        "asset_id": "AMZ-G1",
        "role": {"channel": "amazon-jp", "region": "gallery", "slot": "G1", "asset_type": "gallery-native"},
        "objective": {"shopper_task": "understand the core purchase reason", "primary_message": "Compact performance"},
        "strategy_context": {"consumer_barrier": "small can feel basic", "core_tension": "compact vs capability", "proof_principle": "show spatial proof"},
        "evidence": {"allowed": ["confirmed size"], "forbidden": ["unsupported superlative"]},
        "product_sources": {"required": ["SRC-P01"]},
        "benchmark": {"references": ["BENCH-01"], "learn_from": ["product prominence"], "reuse_asset": False},
        "composition": {"product_role": "hero", "environment": "residential", "information_density": "low", "one_image_focus": True},
        "output": {"aspect_ratio": "1:1", "final_role": "Amazon Gallery", "quantity": 1},
        "must_preserve": ["product geometry"],
        "must_not_generate": ["workflow diagram", "fictional product structure"],
    }


def visual_handoff() -> dict:
    return {
        "page_plan": {
            "gallery": ["G1", "G2", "G3"],
            "enhanced_content": ["A1"],
            "other_required_regions": [],
        },
        "asset_set": [
            {"asset_id": "G1", "evidence_mode": "SOURCE_FAITHFUL"},
            {"asset_id": "G2", "evidence_mode": "CREATIVE_MOCK"},
            {"asset_id": "G3", "evidence_mode": "PROOF_VISUAL"},
            {"asset_id": "A1", "evidence_mode": "CREATIVE_MOCK"},
        ],
        "page_visual_system": {
            "asset_directions": [
                {"asset_id": "G1", "scene_family": "clean-stage", "composition_family": "centered", "tone": "bright", "product_scale": "large", "proof_form": "product"},
                {"asset_id": "G2", "scene_family": "daylight-study", "composition_family": "medium-product", "tone": "bright-neutral", "product_scale": "medium", "proof_form": "lifestyle"},
                {"asset_id": "G3", "scene_family": "technical", "composition_family": "close-up", "tone": "neutral", "product_scale": "close-up", "proof_form": "mechanism"},
                {"asset_id": "A1", "scene_family": "home", "composition_family": "wide", "tone": "warm", "product_scale": "medium", "proof_form": "lifestyle"},
            ]
        },
    }


def test_production_skill_is_artifact_first() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    for phrase in [
        "name: listing-production", "stage 7.5", "stage 8",
        "artifact-first", "one asset packet", "user_approved",
    ]:
        assert phrase in text
    for forbidden in [
        "exact_recovery_verified", "provenance_conflict",
        "pre_demo_asset_gate", "delivery_parity_gate",
    ]:
        assert forbidden not in text


def test_production_has_small_status_vocabulary() -> None:
    text = read(SKILL_DIR / "SKILL.md")
    for status in ["PLANNED", "READY", "REVIEW", "REVISE", "USER_APPROVED", "BLOCKED"]:
        assert status in text
    assert "Creative Approval ≠ Evidence Verification" in text


def test_one_job_packet_passes() -> None:
    assert validate_asset_packet(base_packet()) == []


def test_multiple_asset_ids_fail_one_job_rule() -> None:
    packet = base_packet()
    packet["asset_id"] = ["AMZ-G1", "AMZ-G2"]
    errors = validate_asset_packet(packet)
    assert any("one asset_id" in e for e in errors)


def test_quantity_above_one_requires_batch_outside_asset_packet() -> None:
    packet = base_packet()
    packet["output"]["quantity"] = 3
    errors = validate_asset_packet(packet)
    assert any("quantity must be 1" in e for e in errors)


def test_projection_drops_control_plane_fields() -> None:
    packet = base_packet()
    packet["project_state_manifest"] = {"declared_gate_results": {"X": "PASS"}}
    packet["stage_completion_manifest"] = {"status": "COMPLETE"}
    projected = project_generation_context(packet)
    encoded = json.dumps(projected, ensure_ascii=False).casefold()
    for forbidden in ["project_state_manifest", "declared_gate_results", "stage_completion_manifest", "delivery_parity"]:
        assert forbidden not in encoded


def test_user_approval_is_creative_only() -> None:
    ledger = {"assets": {"AMZ-G1": {"status": "REVIEW"}}}
    updated = set_creative_status(ledger, "AMZ-G1", "USER_APPROVED", "file:g1", "chat:approval-1")
    row = updated["assets"]["AMZ-G1"]
    assert row["status"] == "USER_APPROVED"
    assert row["current_output_ref"] == "file:g1"
    assert "VERIFIED" not in json.dumps(row)


def test_three_of_thirteen_is_not_complete() -> None:
    handoff = {"asset_set": [{"asset_id": f"A{i}"} for i in range(13)]}
    ledger = {"assets": {f"A{i}": {"status": "USER_APPROVED"} for i in range(3)}}
    progress = production_progress(handoff, ledger)
    assert progress == {"expected": 13, "approved": 3, "remaining": 10, "complete": False}


def test_freeze_refuses_revision_pending_asset() -> None:
    handoff = {"asset_set": [{"asset_id": "A1"}, {"asset_id": "A2"}]}
    ledger = {"assets": {"A1": {"status": "USER_APPROVED", "current_output_ref": "file:a1"}, "A2": {"status": "REVISE"}}}
    freeze = build_production_freeze(handoff, ledger)
    assert freeze["ready_for_hardening"] is False
    assert freeze["revision_pending"] == ["A2"]


def test_visual_pattern_library_is_complete() -> None:
    names = [
        "hero-positioning.md", "compact-proof.md", "mechanism-explainer.md",
        "automation-flow.md", "comparison.md", "installation-decision.md", "ui-proof.md",
    ]
    for name in names:
        text = read(SKILL_DIR / "references" / "visual-patterns" / name).casefold()
        for phrase in ["when to use", "shopper question", "good composition", "proof object", "information density", "common failure"]:
            assert phrase in text, (name, phrase)


def test_creative_qa_has_seven_dimensions_and_no_hardening_terms() -> None:
    text = read(SKILL_DIR / "references" / "production-qa.md").casefold()
    for phrase in [
        "message clarity", "product prominence", "visual proof", "composition",
        "realism", "benchmark", "channel readiness",
    ]:
        assert phrase in text
    for forbidden in ["sha-256", "exact recovery", "delivery parity"]:
        assert forbidden not in text


def test_benchmark_policy_separates_reference_from_reuse() -> None:
    text = read(SKILL_DIR / "references" / "benchmark-policy.md").casefold()
    assert "benchmark" in text and "reuse" in text
    assert "does not automatically" in text


def test_minimal_set_context_includes_current_direction_and_neighbors() -> None:
    from project_asset_packet import build_set_context

    context = build_set_context(visual_handoff(), "G2")
    assert context["page_visual_direction"]["scene_family"] == "daylight-study"
    assert [row["asset_id"] for row in context["nearest_neighbors"]] == ["G1", "G3"]
    assert set(context["nearest_neighbors"][0]) == {
        "asset_id", "scene_family", "composition_family", "tone", "product_scale", "proof_form"
    }


def test_generation_context_carries_evidence_mode_and_minimal_set_context() -> None:
    packet = base_packet()
    packet["evidence_mode"] = "CREATIVE_MOCK"
    packet["set_context"] = {
        "page_visual_direction": visual_handoff()["page_visual_system"]["asset_directions"][1],
        "nearest_neighbors": [visual_handoff()["page_visual_system"]["asset_directions"][0]],
    }
    projected = project_generation_context(packet)
    assert projected["evidence_mode"] == "CREATIVE_MOCK"
    assert projected["set_context"]["page_visual_direction"]["scene_family"] == "daylight-study"


def test_evidence_mode_controls_missing_source_behavior() -> None:
    from project_asset_packet import evaluate_source_readiness

    packet = base_packet()
    packet["product_sources"] = {"required": ["SRC-P01"]}

    packet["evidence_mode"] = "CREATIVE_MOCK"
    mock = evaluate_source_readiness(packet, available_source_ids=set())
    assert mock["status"] == "READY_WITH_LIMITATION"

    packet["evidence_mode"] = "PROOF_VISUAL"
    proof = evaluate_source_readiness(packet, available_source_ids=set())
    assert proof["status"] == "BLOCKED"

    packet["evidence_mode"] = "SOURCE_FAITHFUL"
    faithful = evaluate_source_readiness(packet, available_source_ids=set())
    assert faithful["status"] == "BLOCKED"


def test_set_context_still_excludes_control_plane() -> None:
    from project_asset_packet import build_set_context

    handoff = visual_handoff()
    handoff["project_state_manifest"] = {"status": "COMPLETE"}
    handoff["auditor_evidence"] = {"G2": "VERIFIED"}
    handoff["declared_gate_results"] = {"X": "PASS"}
    encoded = json.dumps(build_set_context(handoff, "G2"), ensure_ascii=False).casefold()
    for forbidden in ["project_state", "auditor", "gate", "parity"]:
        assert forbidden not in encoded


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-production tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
