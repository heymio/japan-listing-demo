#!/usr/bin/env python3
"""Regression tests for the listing-planning Skill."""

from datetime import datetime, timezone
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


def valid_v032_handoff() -> str:
    return """production_handoff:
  project:
    market: JP
    channel: amazon-jp
    locale: ja-JP
    product: Example Product
  page_plan:
    gallery:
      - G1
      - G2
    enhanced_content:
      - A1
    other_required_regions: []
  asset_set:
    - asset_id: G1
      role: gallery-native
      slot: G1
      primary_message: Core positioning
      evidence_mode: SOURCE_FAITHFUL
      status: READY
    - asset_id: G2
      role: gallery-native
      slot: G2
      primary_message: Primary proof
      evidence_mode: PROOF_VISUAL
      status: READY
    - asset_id: A1
      role: enhanced-content
      slot: A1
      primary_message: Lifestyle expansion
      evidence_mode: CREATIVE_MOCK
      status: READY
  source_assets:
    - source_id: SRC-P01
      role: real-product-source
      required_by:
        - G1
        - G2
        - A1
  product_invariants:
    - preserve exact product geometry
  creative_strategy_ref: creative-strategy.yaml
  global_visual_direction:
    - product-first commercial hierarchy
  visual_benchmark_refs:
    - BENCH-01
  prohibited:
    - unsupported claims
  blocked_assets: []
  page_visual_system:
    asset_directions:
      - asset_id: G1
        visual_role: hero-positioning
        scene_family: clean-product-stage
        composition_family: centered-hero
        tone: bright-neutral
        product_scale: large
        proof_form: source-faithful-product
      - asset_id: G2
        visual_role: mechanism-proof
        scene_family: technical-detail
        composition_family: close-up-explainer
        tone: neutral-technical
        product_scale: close-up
        proof_form: mechanism
      - asset_id: A1
        visual_role: lifestyle-use
        scene_family: realistic-home
        composition_family: wide-lifestyle
        tone: warm-natural
        product_scale: medium
        proof_form: lifestyle
"""


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


def test_v032_handoff_rejects_invalid_evidence_mode() -> None:
    text = valid_v032_handoff().replace("evidence_mode: SOURCE_FAITHFUL", "evidence_mode: NOT_A_MODE", 1)
    errors = validate_production_handoff(text)
    assert any("evidence_mode" in error for error in errors)


def test_v032_handoff_rejects_visual_direction_for_unknown_asset() -> None:
    text = valid_v032_handoff().replace("asset_id: A1\n        visual_role: lifestyle-use", "asset_id: MISSING-ASSET\n        visual_role: lifestyle-use", 1)
    errors = validate_production_handoff(text)
    assert any("MISSING-ASSET" in error for error in errors)


def test_v032_handoff_rejects_accidental_adjacent_visual_duplicate() -> None:
    text = valid_v032_handoff()
    text = text.replace("scene_family: technical-detail", "scene_family: clean-product-stage", 1)
    text = text.replace("composition_family: close-up-explainer", "composition_family: centered-hero", 1)
    text = text.replace("tone: neutral-technical", "tone: bright-neutral", 1)
    text = text.replace("product_scale: close-up", "product_scale: large", 1)
    text = text.replace("proof_form: mechanism", "proof_form: source-faithful-product", 1)
    errors = validate_production_handoff(text)
    assert any("adjacent visual direction" in error.casefold() for error in errors)


def test_v032_handoff_allows_intentional_adjacent_visual_duplicate() -> None:
    text = valid_v032_handoff()
    text = text.replace("scene_family: technical-detail", "scene_family: clean-product-stage", 1)
    text = text.replace("composition_family: close-up-explainer", "composition_family: centered-hero", 1)
    text = text.replace("tone: neutral-technical", "tone: bright-neutral", 1)
    text = text.replace("product_scale: close-up", "product_scale: large", 1)
    text = text.replace(
        "proof_form: mechanism",
        "proof_form: source-faithful-product\n        neighbor_contrast_note: Intentional matched pair for comparison",
        1,
    )
    assert validate_production_handoff(text) == []


def test_v032_scope_delta_removed_asset_cannot_remain_current() -> None:
    text = valid_v032_handoff() + """  scope_revision: 2
  scope_delta:
    added: []
    removed:
      - G2
    changed: []
    reason:
      - message merged into G1
"""
    errors = validate_production_handoff(text)
    assert any("removed" in error.casefold() and "G2" in error for error in errors)


def test_recent_account_capability_is_reused() -> None:
    from account_capability import resolve_capability

    profile = {
        "channel": "amazon-jp",
        "capabilities": {"premium_a_plus": True},
        "verified_at": "2026-08-01",
        "source_ref": "team-private-context",
    }
    result = resolve_capability(
        profile,
        "premium_a_plus",
        now=datetime(2026, 8, 21, tzinfo=timezone.utc),
        max_age_days=90,
    )
    assert result == {"status": "REUSE", "value": True, "reason": "recent confirmed capability"}


def test_stale_or_conflicted_account_capability_requires_verification() -> None:
    from account_capability import resolve_capability

    profile = {
        "channel": "amazon-jp",
        "capabilities": {"premium_a_plus": True},
        "verified_at": "2025-01-01",
        "source_ref": "team-private-context",
    }
    stale = resolve_capability(
        profile,
        "premium_a_plus",
        now=datetime(2026, 8, 21, tzinfo=timezone.utc),
        max_age_days=90,
    )
    conflict = resolve_capability(
        profile,
        "premium_a_plus",
        now=datetime(2026, 8, 21, tzinfo=timezone.utc),
        max_age_days=9999,
        conflicting=True,
    )
    assert stale["status"] == "VERIFY"
    assert conflict["status"] == "VERIFY"


def test_invalid_account_capability_profile_requires_verification() -> None:
    from account_capability import resolve_capability

    result = resolve_capability(
        {"capabilities": {"premium_a_plus": "yes"}, "verified_at": "not-a-date"},
        "premium_a_plus",
        now=datetime(2026, 8, 21, tzinfo=timezone.utc),
        max_age_days=90,
    )
    assert result["status"] == "VERIFY"
    assert result["value"] is None


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-planning tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
