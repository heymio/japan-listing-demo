#!/usr/bin/env python3
"""Regression tests for the listing-planning Skill."""

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_exists_and_owns_only_planning_plane() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "name: listing-planning" in text
    for phrase in [
        "stage 0", "stage 7", "creative strategy kernel",
        "production handoff", "complete demo-required production set",
    ]:
        assert phrase in text
    for forbidden in [
        "pre_demo_asset_gate", "delivery_parity_gate",
        "provenance_conflict", "exact_recovery_verified",
    ]:
        assert forbidden not in text


def test_stage_6_5_is_lightweight_by_default() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "source asset intake" in text
    assert "targeted early audit" in text
    assert "inherited" in text or "previously approved exact asset" in text
    assert "full project-wide audit is not mandatory" in text


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-planning boundary tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
