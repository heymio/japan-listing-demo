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
        "evidence_mode": "SOURCE_FAITHFUL",
        "product_sources": {"identity_required": ["SRC-P01"], "proof_required": []},
        "benchmark": {"references": ["BENCH-01"], "learn_from": ["product prominence"], "reuse_asset": False},
        "composition": {"product_role": "hero", "environment": "residential", "information_density": "low", "one_image_focus": True},
        "set_context": {
            "page_visual_direction": {
                "asset_id": "AMZ-G1",
                "visual_role": "hero-positioning",
                "scene_family": "clean-stage",
                "composition_family": "centered",
                "tone": "bright",
                "product_scale": "large",
                "proof_form": "product",
            },
            "nearest_neighbors": [],
        },
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


def asset_direction(asset_id: str, *, scene: str, composition: str, tone: str, scale: str, proof: str, message_role: str = "") -> dict:
    return {
        "asset_id": asset_id,
        "scene_family": scene,
        "composition_family": composition,
        "tone": tone,
        "product_scale": scale,
        "proof_form": proof,
        "message_role": message_role,
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


def test_v032_packet_requires_evidence_mode_and_set_context() -> None:
    packet = base_packet()
    packet.pop("evidence_mode")
    packet.pop("set_context")
    errors = validate_asset_packet(packet)
    assert any("evidence_mode" in error for error in errors)
    assert any("set_context" in error for error in errors)


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
    projected = project_generation_context(packet)
    assert projected["evidence_mode"] == "SOURCE_FAITHFUL"
    assert projected["set_context"]["page_visual_direction"]["scene_family"] == "clean-stage"


def test_evidence_mode_distinguishes_identity_from_proof_sources() -> None:
    from project_asset_packet import evaluate_source_readiness

    packet = base_packet()
    packet["product_sources"] = {
        "identity_required": ["SRC-ID"],
        "proof_required": ["SRC-PROOF"],
    }
    packet["evidence_mode"] = "CREATIVE_MOCK"

    missing_identity = evaluate_source_readiness(packet, available_source_ids={"SRC-PROOF"})
    assert missing_identity["status"] == "BLOCKED"
    assert missing_identity["missing_identity_source_ids"] == ["SRC-ID"]

    missing_proof = evaluate_source_readiness(packet, available_source_ids={"SRC-ID"})
    assert missing_proof["status"] == "READY_WITH_LIMITATION"
    assert missing_proof["missing_proof_source_ids"] == ["SRC-PROOF"]

    packet["evidence_mode"] = "PROOF_VISUAL"
    proof = evaluate_source_readiness(packet, available_source_ids={"SRC-ID"})
    assert proof["status"] == "BLOCKED"

    packet["evidence_mode"] = "SOURCE_FAITHFUL"
    faithful = evaluate_source_readiness(packet, available_source_ids={"SRC-ID"})
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


def test_user_selected_candidate_cannot_be_silently_replaced() -> None:
    from production_state import add_candidate, select_candidate

    ledger = add_candidate({}, "A05-01", "A05-01-v1", "file:v1")
    ledger = select_candidate(ledger, "A05-01", "A05-01-v1", "chat:42")
    try:
        set_creative_status(ledger, "A05-01", "USER_APPROVED", output_ref="file:v2")
    except ValueError as exc:
        assert "reopen" in str(exc).casefold()
    else:
        raise AssertionError("selected candidate must not be silently replaced")


def test_selected_candidate_lock_blocks_new_candidate_until_reopen() -> None:
    from production_state import add_candidate, select_candidate

    ledger = add_candidate({}, "A05-01", "A05-01-v1", "file:v1")
    ledger = select_candidate(ledger, "A05-01", "A05-01-v1")
    try:
        add_candidate(ledger, "A05-01", "A05-01-v2", "file:v2")
    except ValueError as exc:
        assert "reopen" in str(exc).casefold()
    else:
        raise AssertionError("locked asset must reject new candidate before explicit reopen")


def test_selected_candidate_lock_blocks_status_change_until_reopen() -> None:
    from production_state import add_candidate, select_candidate

    ledger = add_candidate({}, "A05-01", "A05-01-v1", "file:v1")
    ledger = select_candidate(ledger, "A05-01", "A05-01-v1")
    try:
        set_creative_status(ledger, "A05-01", "REVISE")
    except ValueError as exc:
        assert "reopen" in str(exc).casefold()
    else:
        raise AssertionError("locked asset status must not change before explicit reopen")


def test_reopen_preserves_candidate_history() -> None:
    from production_state import add_candidate, reopen_asset, select_candidate

    ledger = add_candidate({}, "A05-01", "A05-01-v1", "file:v1")
    ledger = select_candidate(ledger, "A05-01", "A05-01-v1")
    ledger = reopen_asset(ledger, "A05-01", "user requested another version")
    ledger = add_candidate(ledger, "A05-01", "A05-01-v2", "file:v2")
    row = ledger["assets"]["A05-01"]
    assert [candidate["candidate_id"] for candidate in row["candidates"]] == ["A05-01-v1", "A05-01-v2"]
    assert row["selected_candidate_id"] == "A05-01-v1"
    assert row["status"] == "REVIEW"


def test_duplicate_candidate_id_is_rejected() -> None:
    from production_state import add_candidate

    ledger = add_candidate({}, "A05-01", "A05-01-v1", "file:v1")
    try:
        add_candidate(ledger, "A05-01", "A05-01-v1", "file:v1-other")
    except ValueError as exc:
        assert "duplicate" in str(exc).casefold()
    else:
        raise AssertionError("duplicate candidate_id must be rejected")


def test_identical_adjacent_visual_signatures_are_flagged() -> None:
    from set_level_qa import evaluate_set

    rows = [
        asset_direction("A1", scene="dark-living", composition="wide", tone="dark", scale="medium", proof="lifestyle"),
        asset_direction("A2", scene="dark-living", composition="wide", tone="dark", scale="medium", proof="lifestyle"),
    ]
    result = evaluate_set(rows)
    assert result["status"] == "REVISE"
    assert any(issue["type"] == "composition_repetition" for issue in result["issues"])


def test_same_brand_style_with_materially_different_composition_can_clear() -> None:
    from set_level_qa import evaluate_set

    rows = [
        asset_direction("A1", scene="home", composition="wide", tone="brand-warm", scale="medium", proof="lifestyle"),
        asset_direction("A2", scene="home", composition="close-up", tone="brand-warm", scale="close-up", proof="mechanism"),
    ]
    assert evaluate_set(rows)["status"] == "CLEAR"


def test_three_same_proof_forms_trigger_review() -> None:
    from set_level_qa import evaluate_set

    rows = [
        asset_direction("A1", scene="s1", composition="c1", tone="t1", scale="large", proof="lifestyle"),
        asset_direction("A2", scene="s2", composition="c2", tone="t2", scale="medium", proof="lifestyle"),
        asset_direction("A3", scene="s3", composition="c3", tone="t3", scale="close", proof="lifestyle"),
    ]
    result = evaluate_set(rows)
    assert result["status"] == "REVIEW"
    assert any(issue["type"] == "proof_form_diversity" for issue in result["issues"])


def test_adjacent_same_message_role_triggers_review() -> None:
    from set_level_qa import evaluate_set

    rows = [
        asset_direction("A1", scene="s1", composition="c1", tone="t1", scale="large", proof="lifestyle", message_role="daily-light"),
        asset_direction("A2", scene="s2", composition="c2", tone="t2", scale="medium", proof="mechanism", message_role="daily-light"),
    ]
    result = evaluate_set(rows)
    assert result["status"] == "REVIEW"
    assert any(issue["type"] == "message_role_redundancy" for issue in result["issues"])


def test_removed_asset_keeps_scope_plan_and_visual_system_aligned() -> None:
    from production_state import apply_scope_delta

    handoff = visual_handoff()
    updated = apply_scope_delta(handoff, {
        "added": [], "removed": ["G3"], "changed": [],
        "reason": ["message merged into G2"],
    })
    assert [row["asset_id"] for row in updated["asset_set"]] == ["G1", "G2", "A1"]
    assert updated["page_plan"]["gallery"] == ["G1", "G2"]
    assert [row["asset_id"] for row in updated["page_visual_system"]["asset_directions"]] == ["G1", "G2", "A1"]


def test_scope_delta_add_or_change_requires_revised_planning_handoff() -> None:
    from production_state import apply_scope_delta

    handoff = visual_handoff()
    for delta in [
        {
            "added": [{"asset_id": "G4", "evidence_mode": "CREATIVE_MOCK"}],
            "removed": [], "changed": [], "reason": ["new shopper task"],
        },
        {
            "added": [], "removed": [],
            "changed": [{"asset_id": "G2", "evidence_mode": "PROOF_VISUAL"}],
            "reason": ["role changed"],
        },
    ]:
        try:
            apply_scope_delta(handoff, delta)
        except ValueError as exc:
            assert "planning" in str(exc).casefold() or "handoff" in str(exc).casefold()
        else:
            raise AssertionError("added/changed scope must require a revised Planning handoff")


def test_removed_asset_no_longer_counts_toward_progress_or_freeze() -> None:
    from production_state import apply_scope_delta

    handoff = {"asset_set": [{"asset_id": "G1"}, {"asset_id": "G2"}, {"asset_id": "G3"}]}
    ledger = {"assets": {
        "G1": {"status": "USER_APPROVED", "current_output_ref": "file:g1"},
        "G2": {"status": "USER_APPROVED", "current_output_ref": "file:g2"},
    }}
    updated = apply_scope_delta(handoff, {
        "added": [], "removed": ["G3"], "changed": [],
        "reason": ["message merged into G2"],
    })
    progress = production_progress(updated, ledger)
    freeze = build_production_freeze(updated, ledger)
    assert progress == {"expected": 2, "approved": 2, "remaining": 0, "complete": True}
    assert freeze["ready_for_hardening"] is True
    assert ledger["assets"]["G1"]["status"] == "USER_APPROVED"


def test_v032_freeze_requires_current_set_level_visual_review() -> None:
    handoff = visual_handoff()
    ledger = {
        "assets": {
            asset_id: {"status": "USER_APPROVED", "current_output_ref": f"file:{asset_id.lower()}"}
            for asset_id in ["G1", "G2", "G3", "A1"]
        }
    }
    pending = build_production_freeze(handoff, ledger)
    assert pending["ready_for_hardening"] is False
    assert pending["set_qa_status"] == "MISSING"

    ledger["set_qa"] = {
        "status": "CLEAR",
        "reviewed_asset_ids": ["G1", "G2", "G3", "A1"],
        "visual_review_ref": "contact-sheet:final-v1",
    }
    ready = build_production_freeze(handoff, ledger)
    assert ready["ready_for_hardening"] is True
    assert ready["set_qa_status"] == "CLEAR"


def test_scope_delta_rejects_unknown_removed_asset() -> None:
    from production_state import apply_scope_delta

    try:
        apply_scope_delta({"asset_set": [{"asset_id": "G1"}]}, {
            "added": [], "removed": ["MISSING"], "changed": [], "reason": ["test"]
        })
    except ValueError as exc:
        assert "unknown" in str(exc).casefold()
    else:
        raise AssertionError("unknown removed asset must fail")


def test_set_repetition_cleanup_reopens_smallest_nonapproved_subset() -> None:
    from cleanup_policy import plan_cleanup

    result = plan_cleanup(
        "SET_REPETITION",
        affected_assets=["A05-01", "A05-02", "A05-03", "A06"],
        approved_assets=["A05-01", "A05-02"],
    )
    assert result["preserve"] == ["A05-01", "A05-02"]
    assert result["reopen"] == ["A05-03"]


def test_creative_mock_evidence_limitation_does_not_force_visual_rework() -> None:
    from cleanup_policy import plan_cleanup

    result = plan_cleanup(
        "EVIDENCE_LIMITATION",
        affected_assets=["A04"],
        approved_assets=["A04"],
        evidence_modes={"A04": "CREATIVE_MOCK"},
    )
    assert result["reopen"] == []
    assert result["preserve"] == ["A04"]


def test_single_asset_defect_only_reopens_that_asset() -> None:
    from cleanup_policy import plan_cleanup

    result = plan_cleanup(
        "SINGLE_ASSET_DEFECT",
        affected_assets=["A06"],
        approved_assets=["A05", "A06", "A07"],
    )
    assert result["reopen"] == ["A06"]
    assert "A05" not in result["reopen"] and "A07" not in result["reopen"]


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-production tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
