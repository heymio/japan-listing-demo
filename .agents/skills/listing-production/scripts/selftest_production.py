#!/usr/bin/env python3
"""Regression tests for the listing-production Skill."""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from project_asset_packet import project_generation_context, validate_asset_packet  # noqa: E402


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


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-production tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
