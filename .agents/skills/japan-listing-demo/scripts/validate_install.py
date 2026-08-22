#!/usr/bin/env python3
"""Validate an extracted one-install japan-listing-demo v0.3.3 package."""

from __future__ import annotations

import importlib.util
import struct
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERNAL = ROOT / "internal-skills"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    required = [
        ROOT / "SKILL.md",
        ROOT / "scripts" / "validate_project_state.py",
        INTERNAL / "listing-planning" / "scripts" / "validate_planning_contracts.py",
        INTERNAL / "listing-production" / "scripts" / "production_state.py",
        INTERNAL / "listing-production" / "scripts" / "production_state_legacy.py",
        INTERNAL / "listing-hardening" / "scripts" / "validate_delivery_state.py",
        INTERNAL / "listing-hardening" / "scripts" / "validate_demo_html.py",
        INTERNAL / "listing-hardening" / "scripts" / "validate_demo_html_legacy.py",
        INTERNAL / "listing-hardening" / "scripts" / "validate_demo_runtime.py",
        INTERNAL / "listing-evidence-auditor" / "scripts" / "fingerprint_assets.py",
        INTERNAL / "listing-evidence-auditor" / "scripts" / "fingerprint_assets_legacy.py",
        INTERNAL / "listing-evidence-auditor" / "scripts" / "reconcile_evidence.py",
        INTERNAL / "listing-evidence-auditor" / "scripts" / "reconcile_evidence_legacy.py",
    ]
    check(all(path.is_file() for path in required), "runtime member missing")

    hardening = load(required[5], "install_hardening")
    check(
        "FRONTEND_FIDELITY_GATE" in hardening.GATE_NAMES
        and "DEMO_RUNTIME_GATE" in hardening.GATE_NAMES,
        "canonical hard gates missing",
    )
    empty_demo = {
        "schema_version": "0.2",
        "channel": {},
        "approval_events": [],
        "assets": [],
        "locked_module_plan": {},
        "asset_slot_contract": [],
        "implementation": {},
        "audit_checkpoints": {"pre_9_required": False},
    }
    check(hardening.validate_state(empty_demo)["overall_status"] != "PASS", "empty Demo fail-open")

    project = load(ROOT / "scripts" / "validate_project_state.py", "install_project_state")
    legacy = {
        "schema_version": "0.1",
        "channel": {},
        "approval_events": [],
        "assets": [],
        "locked_module_plan": {},
        "asset_slot_contract": [],
        "implementation": {},
        "audit_checkpoints": {"pre_9_required": True},
    }
    check(
        project.validate_state(legacy)["gates"]["PRE_DEMO_ASSET_GATE"]["status"] != "N/A",
        "legacy explicit pre-9 audit lost",
    )

    demo = load(required[6], "install_demo")
    html = (
        '<!doctype html><html><head><meta name="viewport" content="width=device-width">'
        '<style>img{max-width:100%}@media(max-width:600px){body{margin:0}}</style></head>'
        '<body><svg><image href="https://example.com/a.png"></image></svg></body></html>'
    )
    check(demo.validate_html_text(html)["status"] == "FAIL", "external SVG resource escaped standalone validation")

    auditor = load(required[9], "install_fingerprint")
    with tempfile.TemporaryDirectory() as name:
        root = Path(name)
        path = root / "bad.png"
        path.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", 1, 1))
        check(bool(auditor.fingerprint_asset(path, root)["errors"]), "truncated PNG accepted")

    production = load(required[3], "install_production")
    freeze = production.build_production_freeze(
        {
            "page_plan": {"gallery": ["A1"], "enhanced_content": [], "other_required_regions": []},
            "asset_set": [{"asset_id": "A1"}],
            "page_visual_system": {"asset_directions": [{"asset_id": "A1"}]},
        },
        {"assets": {"A1": {"status": "USER_APPROVED", "current_output_ref": "file:a1"}}},
    )
    check(freeze["ready_for_hardening"] is False, "Freeze accepted approval without exact candidate binding")

    print("PASS: extracted one-install package validates its v0.3.3 runtime")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
