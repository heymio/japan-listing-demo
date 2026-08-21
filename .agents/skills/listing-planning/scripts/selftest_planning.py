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
        "claim-compliance.md": ["verification queue", "visual can create a claim", "refresh trigger"],
        "channel-planning.md": ["primary reference", "platform capability", "frontend visual"],
        "module-fit.md": ["content_coverage", "module_fit_gate", "message != module"],
        "planning-qa.md": ["complete demo-required production set", "gallery", "enhanced-content"],
    }
    for filename, phrases in required.items():
        text = read(SKILL_DIR / "references" / filename).casefold()
        for phrase in phrases:
            assert phrase in text, (filename, phrase)


def test_japan_market_and_copy_depth_survives_context_simplification() -> None:
    market = read(SKILL_DIR / "references" / "market-research.md").casefold()
    locale = read(SKILL_DIR / "references" / "localization.md").casefold()
    for phrase in ["market evidence registry", "search and keyword research", "visual localization"]:
        assert phrase in market
    for phrase in ["native review", "search-language research", "numbers and formats", "provisional copy"]:
        assert phrase in locale


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


def test_project_brief_rejects_comment_only_keys() -> None:
    text = """# project:\n# offers:\n# product_truth:\n# claim_boundaries:\n# consumer_evidence_sources:\n# channel_reference:\n# open_business_decisions:\n"""
    errors = validate_project_brief(text)
    assert errors, "comment text must not satisfy the structured contract"


def test_project_brief_rejects_wrong_container_types() -> None:
    text = """project: []\noffers: {}\nproduct_truth: []\nclaim_boundaries: []\nconsumer_evidence_sources: {}\nchannel_reference: []\nopen_business_decisions: {}\n"""
    errors = validate_project_brief(text)
    assert any("project" in error and "mapping" in error for error in errors)
    assert any("offers" in error and "list" in error for error in errors)


def test_creative_strategy_rejects_wrong_nested_types() -> None:
    text = """creative_strategy:\n  target_user: wrong\n  core_tension: ok\n  core_promise: ok\n  primary_purchase_reasons: {}\n  shopper_barriers: []\n  reasons_to_believe: []\n  message_priority: []\n  japan_implications: []\n  proof_principles: []\n  visual_direction: []\n  visual_anti_patterns: []\n"""
    errors = validate_creative_strategy(text)
    assert any("target_user" in error and "list" in error for error in errors)
    assert any("message_priority" in error and "mapping" in error for error in errors)


def test_production_handoff_rejects_wrong_asset_set_type() -> None:
    text = """production_handoff:\n  project: {}\n  page_plan: {}\n  asset_set: not-a-list\n  source_assets: []\n  product_invariants: []\n  creative_strategy_ref: STRAT-1\n  global_visual_direction: []\n  visual_benchmark_refs: []\n  prohibited: []\n  blocked_assets: []\n"""
    errors = validate_production_handoff(text)
    assert any("asset_set" in error and "list" in error for error in errors)


def test_production_handoff_rejects_control_plane_fields() -> None:
    text = """production_handoff:\n  project: {}\n  page_plan: {}\n  asset_set: []\n  source_assets: []\n  product_invariants: []\n  creative_strategy_ref: STRAT-1\n  global_visual_direction: []\n  visual_benchmark_refs: []\n  prohibited: []\n  blocked_assets: []\n  project_state_manifest: {}\n"""
    errors = validate_production_handoff(text)
    assert any("project_state_manifest" in error for error in errors)


def test_malformed_yaml_returns_errors_instead_of_crashing() -> None:
    errors = validate_project_brief("project:\n   child: bad-indent\n")
    assert errors


def test_priority_proof_is_not_complete_asset_set() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "priority proof coverage" in text
    assert "does not" in text and "complete" in text


def test_gallery_and_enhanced_content_are_separate_production_roles() -> None:
    text = read(SKILL_DIR / "references" / "module-fit.md").casefold()
    assert "gallery-native" in text
    assert "enhanced-content" in text
    assert "separate" in text


def test_fresh_project_does_not_require_full_stage_6_5_audit() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "full project-wide audit is not mandatory" in text
    assert "targeted early audit" in text


def test_channel_profiles_are_owned_by_planning() -> None:
    channels = ["amazon-jp.md", "rakuten.md", "yahoo-shopping.md", "dtc.md", "retailer-pdp.md"]
    root = SKILL_DIR / "profiles" / "channels"
    for name in channels:
        text = read(root / name).casefold()
        assert "use when" in text
        assert "platform" in text or "channel" in text
        assert "content" in text or "module" in text


def test_amazon_planning_profile_keeps_module_budget_and_role_separation() -> None:
    text = read(SKILL_DIR / "profiles" / "channels" / "amazon-jp.md").casefold()
    for phrase in ["basic a+", "premium a+", "message != module", "gallery", "enhanced-content", "module_fit_gate"]:
        assert phrase in text
    for forbidden in ["exact_recovery_verified", "delivery_parity_gate", "provenance_conflict"]:
        assert forbidden not in text


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-planning tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
