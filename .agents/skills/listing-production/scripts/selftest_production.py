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

from production_state import build_production_freeze  # noqa: E402

MIGRATED = {
    "test_freeze_refuses_revision_pending_asset",
}


def test_freeze_refuses_revision_pending_asset() -> None:
    handoff = {
        "page_plan": {"gallery": ["A1", "A2"], "enhanced_content": [], "other_required_regions": []},
        "asset_set": [{"asset_id": "A1"}, {"asset_id": "A2"}],
        "page_visual_system": {"asset_directions": [{"asset_id": "A1"}, {"asset_id": "A2"}]},
    }
    ledger = {
        "assets": {
            "A1": {"status": "USER_APPROVED", "selected_candidate_id": "A1-v1", "current_output_ref": "file:a1"},
            "A2": {"status": "REVISE"},
        }
    }
    freeze = build_production_freeze(handoff, ledger)
    assert freeze["ready_for_hardening"] is False
    assert freeze["revision_pending"] == ["A2"]
    assert freeze["approved_outputs"] == {"A1": {"candidate_id": "A1-v1", "output_ref": "file:a1"}}


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
