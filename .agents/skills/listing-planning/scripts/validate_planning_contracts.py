#!/usr/bin/env python3
"""Lightweight structural validation for planning handoff artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_PROJECT_BRIEF = {
    "project:",
    "offers:",
    "product_truth:",
    "claim_boundaries:",
    "consumer_evidence_sources:",
    "channel_reference:",
    "open_business_decisions:",
}

REQUIRED_CREATIVE = {
    "creative_strategy:",
    "target_user:",
    "core_tension:",
    "core_promise:",
    "primary_purchase_reasons:",
    "shopper_barriers:",
    "reasons_to_believe:",
    "message_priority:",
    "japan_implications:",
    "proof_principles:",
    "visual_direction:",
    "visual_anti_patterns:",
}

REQUIRED_HANDOFF = {
    "production_handoff:",
    "project:",
    "page_plan:",
    "asset_set:",
    "source_assets:",
    "product_invariants:",
    "creative_strategy_ref:",
    "global_visual_direction:",
    "visual_benchmark_refs:",
    "prohibited:",
    "blocked_assets:",
}

FORBIDDEN_HANDOFF = {
    "project_state_manifest",
    "auditor_evidence",
    "declared_gate_results",
    "change_impact_map",
    "delivery_parity_gate",
    "pre_demo_asset_gate",
}


def _missing(text: str, required: set[str]) -> list[str]:
    folded = text.casefold()
    return [f"missing required key: {key}" for key in sorted(required) if key.casefold() not in folded]


def validate_project_brief(text: str) -> list[str]:
    return _missing(text, REQUIRED_PROJECT_BRIEF)


def validate_creative_strategy(text: str) -> list[str]:
    return _missing(text, REQUIRED_CREATIVE)


def validate_production_handoff(text: str) -> list[str]:
    errors = _missing(text, REQUIRED_HANDOFF)
    folded = text.casefold()
    for forbidden in sorted(FORBIDDEN_HANDOFF):
        if forbidden in folded:
            errors.append(f"forbidden control-plane key in Production Handoff: {forbidden}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a planning artifact")
    parser.add_argument("kind", choices=["project-brief", "creative-strategy", "production-handoff"])
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8")
    validators = {
        "project-brief": validate_project_brief,
        "creative-strategy": validate_creative_strategy,
        "production-handoff": validate_production_handoff,
    }
    errors = validators[args.kind](text)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {args.kind} contract is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
