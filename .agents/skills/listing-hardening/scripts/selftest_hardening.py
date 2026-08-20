#!/usr/bin/env python3
"""Regression tests for the listing-hardening Skill."""

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-hardening boundary tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
