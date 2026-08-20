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


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-hardening tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
