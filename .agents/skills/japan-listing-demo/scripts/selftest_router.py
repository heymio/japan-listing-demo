#!/usr/bin/env python3
"""Regression tests for the thin japan-listing-demo router."""

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_router_is_materially_smaller_than_v026_budget() -> None:
    text = read(SKILL_DIR / "SKILL.md")
    assert len(text) <= 8000, len(text)


def test_default_prompt_is_thin() -> None:
    text = read(SKILL_DIR / "agents" / "openai.yaml")
    assert len(text) <= 2200, len(text)
    folded = text.casefold()
    for forbidden in [
        "sha-256", "provenance_conflict", "pre_demo_asset_gate",
        "delivery_parity_gate", "declared_gate_results",
    ]:
        assert forbidden not in folded


def test_router_maps_stage_planes() -> None:
    text = read(SKILL_DIR / "references" / "routing.md").casefold()
    for phrase in [
        "stage 0–7", "listing-planning",
        "stage 7.5–8", "listing-production",
        "stage 8.5–10", "listing-hardening",
    ]:
        assert phrase in text


def test_router_preserves_checkpoint_transition_and_retry() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    for phrase in ["major stage checkpoint", "transition command", "retry budget", "context firewall"]:
        assert phrase in text


def test_default_checkpoint_is_concise() -> None:
    text = read(SKILL_DIR / "references" / "routing.md")
    assert "Done:" in text and "Open:" in text and "Next:" in text
    assert "full Stage Completion Manifest" in text
    assert "PARTIAL" in text and "BLOCKED" in text


def test_router_uses_five_formal_state_objects() -> None:
    text = read(SKILL_DIR / "references" / "routing.md")
    for phrase in [
        "Project Brief", "Creative Strategy Kernel", "Production Handoff",
        "Asset Ledger", "Production Freeze", "Delivery State",
    ]:
        assert phrase in text


def test_one_install_archive_has_embedded_skill_resolution() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "internal-skills" in text
    assert "single-context" in text
    assert "listing-planning" in text and "listing-production" in text and "listing-hardening" in text


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} thin-router tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
