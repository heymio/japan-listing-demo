#!/usr/bin/env python3
"""v0.3.3 production regression suite with migrated Freeze fixtures."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LEGACY_PATH = SCRIPT_DIR / "selftest_production_legacy.py"
SPEC = importlib.util.spec_from_file_location("listing_production_selftest_legacy", LEGACY_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load legacy production tests: {LEGACY_PATH}")
legacy = importlib.util.module_from_spec(SPEC)
sys.modules["listing_production_selftest_legacy"] = legacy
SPEC.loader.exec_module(legacy)

from production_state import apply_scope_delta, build_production_freeze  # noqa: E402

MIGRATED = {
    "test_freeze_refuses_revision_pending_asset",
    "test_removed_asset_no_longer_counts_toward_progress_or_freeze",
    "test_v032_freeze_requires_current_set_level_visual_review",
    "test_v032_set_qa_becomes_stale_when_approved_output_changes",
}


def approved(asset_id: str, ref: str | None = None) -> dict:
    return {
        "status": "USER_APPROVED",
        "selected_candidate_id": f"{asset_id}-v1",
        "current_output_ref": ref or f"file:{asset_id.lower()}",
    }


def visual_handoff(asset_ids: list[str]) -> dict:
    return {
        "page_plan": {"gallery": list(asset_ids), "enhanced_content": [], "other_required_regions": []},
        "asset_set": [{"asset_id": asset_id} for asset_id in asset_ids],
        "page_visual_system": {"asset_directions": [{"asset_id": asset_id} for asset_id in asset_ids]},
    }


def final_set_qa(asset_ids: list[str], refs: dict[str, str]) -> dict:
    return {
        "status": "CLEAR",
        "reviewed_asset_ids": list(asset_ids),
        "reviewed_output_refs": {asset_id: refs[asset_id] for asset_id in asset_ids},
        "visual_review_ref": "contact-sheet:final",
    }


def test_freeze_refuses_revision_pending_asset() -> None:
    handoff = visual_handoff(["A1", "A2"])
    ledger = {"assets": {"A1": approved("A1", "file:a1"), "A2": {"status": "REVISE"}}}
    freeze = build_production_freeze(handoff, ledger)
    assert freeze["ready_for_hardening"] is False
    assert freeze["revision_pending"] == ["A2"]
    assert freeze["approved_outputs"] == {"A1": {"candidate_id": "A1-v1", "output_ref": "file:a1"}}


def test_removed_asset_no_longer_counts_toward_progress_or_freeze() -> None:
    handoff = visual_handoff(["G1", "G2", "G3"])
    updated = apply_scope_delta(handoff, {
        "added": [], "removed": ["G3"], "changed": [],
        "reason": ["message merged into G2"],
    })
    ledger = {
        "assets": {
            "G1": approved("G1", "file:g1"),
            "G2": approved("G2", "file:g2"),
        },
        "set_qa": final_set_qa(["G1", "G2"], {"G1": "file:g1", "G2": "file:g2"}),
    }
    progress = legacy.production_progress(updated, ledger)
    freeze = build_production_freeze(updated, ledger)
    assert progress == {"expected": 2, "approved": 2, "remaining": 0, "complete": True}
    assert updated["page_plan"]["gallery"] == ["G1", "G2"]
    assert [row["asset_id"] for row in updated["page_visual_system"]["asset_directions"]] == ["G1", "G2"]
    assert freeze["ready_for_hardening"] is True
    assert freeze["required_asset_ids"] == ["G1", "G2"]
    assert "G3" not in freeze["approved_outputs"]


def test_v032_freeze_requires_current_set_level_visual_review() -> None:
    asset_ids = ["G1", "G2", "G3", "A1"]
    handoff = visual_handoff(asset_ids)
    ledger = {"assets": {asset_id: approved(asset_id) for asset_id in asset_ids}}
    pending = build_production_freeze(handoff, ledger)
    assert pending["ready_for_hardening"] is False
    assert pending["set_qa_status"] == "MISSING"

    ledger["set_qa"] = {
        "status": "CLEAR",
        "reviewed_asset_ids": list(asset_ids),
        "visual_review_ref": "contact-sheet:final-v1",
    }
    stale = build_production_freeze(handoff, ledger)
    assert stale["ready_for_hardening"] is False
    assert stale["set_qa_status"] == "STALE"

    refs = {asset_id: f"file:{asset_id.lower()}" for asset_id in asset_ids}
    ledger["set_qa"]["reviewed_output_refs"] = refs
    ready = build_production_freeze(handoff, ledger)
    assert ready["ready_for_hardening"] is True
    assert ready["set_qa_status"] == "CLEAR"
    assert set(ready["approved_outputs"]) == set(asset_ids)


def test_v032_set_qa_becomes_stale_when_approved_output_changes() -> None:
    asset_ids = ["G1", "G2", "G3", "A1"]
    handoff = visual_handoff(asset_ids)
    refs = {asset_id: f"file:{asset_id.lower()}" for asset_id in asset_ids}
    ledger = {
        "assets": {asset_id: approved(asset_id, refs[asset_id]) for asset_id in asset_ids},
        "set_qa": final_set_qa(asset_ids, refs),
    }
    assert build_production_freeze(handoff, ledger)["ready_for_hardening"] is True

    ledger["assets"]["G2"]["current_output_ref"] = "file:g2-v3"
    ledger["assets"]["G2"]["selected_candidate_id"] = "G2-v3"
    stale = build_production_freeze(handoff, ledger)
    assert stale["ready_for_hardening"] is False
    assert stale["set_qa_status"] == "STALE"


def main() -> int:
    tests = []
    for name, value in vars(legacy).items():
        if name.startswith("test_") and callable(value) and name not in MIGRATED:
            tests.append((name, value))
    for name, value in globals().items():
        if name.startswith("test_") and callable(value):
            tests.append((name, value))
    for name, test in sorted(tests):
        test()
    print(f"PASS: {len(tests)} listing-production tests (v0.3.3)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
