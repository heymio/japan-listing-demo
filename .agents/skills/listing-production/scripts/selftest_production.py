#!/usr/bin/env python3
"""Regression tests for the listing-production Skill."""

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-production boundary tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
