#!/usr/bin/env python3
"""Compatibility shim for the canonical listing-hardening validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[4]
TARGET = REPO_ROOT / ".agents" / "skills" / "listing-hardening" / "scripts" / "validate_delivery_state.py"
SPEC = importlib.util.spec_from_file_location("listing_hardening_validate_delivery_state", TARGET)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load hardening validator: {TARGET}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

canonical_hash = MODULE.canonical_hash
validate_state = MODULE.validate_state
main = MODULE.main

if __name__ == "__main__":
    raise SystemExit(main())
