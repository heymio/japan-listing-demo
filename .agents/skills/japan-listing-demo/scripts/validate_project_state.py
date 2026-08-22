#!/usr/bin/env python3
"""Compatibility shim for the canonical listing-hardening validator.

Delivery State 0.2 uses v0.3.3 fail-closed Demo gates automatically. Legacy
Project State 0.1 keeps its historical opt-in pre-9 audit behavior when the
state explicitly requests it.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[4]
TARGET = REPO_ROOT / ".agents" / "skills" / "listing-hardening" / "scripts" / "validate_delivery_state.py"
SPEC = importlib.util.spec_from_file_location("listing_hardening_validate_delivery_state", TARGET)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load hardening validator: {TARGET}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

canonical_hash = MODULE.canonical_hash


def _recompute_overall(result: dict[str, Any]) -> None:
    statuses = {gate.get("status") for gate in result.get("gates", {}).values() if isinstance(gate, dict)}
    if "FAIL" in statuses:
        result["overall_status"] = "FAIL"
    elif "UNVERIFIED" in statuses:
        result["overall_status"] = "UNVERIFIED"
    else:
        result["overall_status"] = "PASS"


def validate_state(state: Any, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    result = MODULE.validate_state(state, policy)
    if (
        isinstance(state, dict)
        and state.get("schema_version") == "0.1"
        and isinstance(state.get("audit_checkpoints"), dict)
        and state["audit_checkpoints"].get("pre_9_required") is True
        and result.get("gates", {}).get("SCHEMA_GATE", {}).get("status") == "PASS"
    ):
        # Project State 0.1 never gets the new automatic Demo gate, but an
        # explicit historical pre-9 request must still be honored rather than N/A.
        result["gates"]["PRE_DEMO_ASSET_GATE"] = MODULE._core._pre_demo_asset_gate(state)
        _recompute_overall(result)
        result["note"] += "; legacy v0.1 explicit pre-9 audit preserved by compatibility shim"
    return result


main = MODULE.main

if __name__ == "__main__":
    raise SystemExit(main())
