#!/usr/bin/env python3
"""Regression tests for the listing-planning Skill."""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from validate_planning_contracts import (  # noqa: E402
    validate_creative_strategy,
    validate_production_handoff,
    validate_project_brief,
)


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


def test_deep_strategy_references_exist() -> None:
    required = {
        "source-authority.md": ["product fact", "conflict", "claim"],
        "market-research.md": ["voc", "competitor", "evidence", "inference"],
        "localization.md": ["locale", "ja-jp", "evidence"],
        "channel-planning.md": ["primary reference", "platform capability", "frontend visual"],
        "module-fit.md": ["content_coverage", "module_fit_gate", "message != module"],
        "planning-qa.md": ["complete demo-required production set", "gallery", "enhanced-content"],
    }
    for filename, phrases in required.items():
        text = read(SKILL_DIR / "references" / filename).casefold()
        for phrase in phrases:
            assert phrase in text, (filename, phrase)


def test_planning_references_do_not_own_final_hardening() -> None:
    joined = "\n".join(
        read(path) for path in sorted((SKILL_DIR / "references").glob("*.md"))
    ).casefold()
    for forbidden in ["provenance_conflict", "exact_recovery_verified", "delivery_parity_gate"]:
        assert forbidden not in joined


def test_planning_templates_validate() -> None:
    templates = SKILL_DIR / "templates"
    cases = [
        ("project-brief.example.yaml", validate_project_brief),
        ("creative-strategy.example.yaml", validate_creative_strategy),
        ("production-handoff.example.yaml", validate_production_handoff),
    ]
    for filename, validator in cases:
        errors = validator(read(templates / filename))
        assert errors == [], (filename, errors)


def test_production_handoff_rejects_control_plane_fields() -> None:
    text = """production_handoff:\n  project:\n  asset_set: []\n  project_state_manifest: {}\n"""
    errors = validate_production_handoff(text)
    assert any("project_state_manifest" in error for error in errors)


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-planning tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
