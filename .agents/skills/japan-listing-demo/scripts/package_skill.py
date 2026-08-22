#!/usr/bin/env python3
"""Build the deterministic one-install compatibility package for japan-listing-demo."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

MAIN_SKILL = Path(__file__).resolve().parents[1]
REPO_ROOT = MAIN_SKILL.parents[2]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
DIST_DIR = REPO_ROOT / "dist"
OUTPUT = DIST_DIR / "japan-listing-demo.skill.zip"
PREFIX = Path("japan-listing-demo")

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from package_common import collect_files, reject_symlinks, write_deterministic_zip  # noqa: E402

INTERNAL_SKILL_NAMES = [
    "listing-planning",
    "listing-production",
    "listing-hardening",
    "listing-evidence-auditor",
]

MAIN_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/routing.md",
    "references/exception-routing.md",
    "data/channel-policy-limits.json",
    "core/manifest.yaml",
    "scripts/validate_install.py",
]

LIMITATION_MEMBER = "japan-listing-demo/SINGLE_CONTEXT_LIMITATION.txt"
LIMITATION_TEXT = (
    "This compatibility archive is one model context. Internal stage separation and Context Projection "
    "still apply, but loading the embedded listing-evidence-auditor does not create independent semantic "
    "review. Deterministic file checks may run; unresolved semantic evidence remains UNVERIFIED / "
    "HUMAN_REVIEW_REQUIRED unless resolved by human or genuinely independent review.\n"
)

NORMAL_POLICY_BLOCK = '''SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
DEFAULT_POLICY_PATH = REPO_ROOT / ".agents" / "skills" / "japan-listing-demo" / "data" / "channel-policy-limits.json"'''
EMBEDDED_POLICY_BLOCK = '''SCRIPT_DIR = Path(__file__).resolve().parent
EMBEDDED_MAIN_SKILL = SCRIPT_DIR.parents[2]
DEFAULT_POLICY_PATH = EMBEDDED_MAIN_SKILL / "data" / "channel-policy-limits.json"'''
HARDENING_POLICY_SOURCE = "scripts/_delivery_state_core.py"

EMBEDDED_SHIM = '''#!/usr/bin/env python3
"""Compatibility shim for the embedded listing-hardening validator."""
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any
HERE = Path(__file__).resolve()
MAIN_SKILL = HERE.parents[1]
TARGET = MAIN_SKILL / "internal-skills" / "listing-hardening" / "scripts" / "validate_delivery_state.py"
SPEC = importlib.util.spec_from_file_location("embedded_listing_hardening_validate_delivery_state", TARGET)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load embedded hardening validator: {TARGET}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
canonical_hash = MODULE.canonical_hash

def _recompute(result: dict[str, Any]) -> None:
    statuses = {gate.get("status") for gate in result.get("gates", {}).values() if isinstance(gate, dict)}
    result["overall_status"] = "FAIL" if "FAIL" in statuses else ("UNVERIFIED" if "UNVERIFIED" in statuses else "PASS")

def validate_state(state: Any, policy: dict[str, Any] | None = None) -> dict[str, Any]:
    result = MODULE.validate_state(state, policy)
    if (isinstance(state, dict) and state.get("schema_version") == "0.1"
            and isinstance(state.get("audit_checkpoints"), dict)
            and state["audit_checkpoints"].get("pre_9_required") is True
            and result.get("gates", {}).get("SCHEMA_GATE", {}).get("status") == "PASS"):
        result["gates"]["PRE_DEMO_ASSET_GATE"] = MODULE._core._pre_demo_asset_gate(state)
        _recompute(result)
    return result
MODULE.validate_state = validate_state
main = MODULE.main
if __name__ == "__main__":
    raise SystemExit(main())
'''

REQUIRED_MEMBERS = {
    "japan-listing-demo/SKILL.md",
    "japan-listing-demo/agents/openai.yaml",
    "japan-listing-demo/references/routing.md",
    "japan-listing-demo/references/exception-routing.md",
    "japan-listing-demo/data/channel-policy-limits.json",
    "japan-listing-demo/scripts/validate_project_state.py",
    "japan-listing-demo/scripts/validate_install.py",
    "japan-listing-demo/internal-skills/listing-planning/SKILL.md",
    "japan-listing-demo/internal-skills/listing-planning/scripts/validate_planning_contracts.py",
    "japan-listing-demo/internal-skills/listing-production/SKILL.md",
    "japan-listing-demo/internal-skills/listing-production/scripts/production_state.py",
    "japan-listing-demo/internal-skills/listing-production/scripts/production_state_legacy.py",
    "japan-listing-demo/internal-skills/listing-hardening/SKILL.md",
    "japan-listing-demo/internal-skills/listing-hardening/scripts/validate_delivery_state.py",
    "japan-listing-demo/internal-skills/listing-hardening/scripts/_delivery_state_core.py",
    "japan-listing-demo/internal-skills/listing-hardening/scripts/validate_demo_html.py",
    "japan-listing-demo/internal-skills/listing-hardening/scripts/validate_demo_html_legacy.py",
    "japan-listing-demo/internal-skills/listing-hardening/scripts/validate_demo_runtime.py",
    "japan-listing-demo/internal-skills/listing-evidence-auditor/SKILL.md",
    "japan-listing-demo/internal-skills/listing-evidence-auditor/scripts/fingerprint_assets.py",
    "japan-listing-demo/internal-skills/listing-evidence-auditor/scripts/fingerprint_assets_legacy.py",
    "japan-listing-demo/internal-skills/listing-evidence-auditor/scripts/reconcile_evidence.py",
    "japan-listing-demo/internal-skills/listing-evidence-auditor/scripts/reconcile_evidence_legacy.py",
    LIMITATION_MEMBER,
}


def exclude_dev_test(relative: Path) -> bool:
    return relative.name.startswith("selftest_") or relative.name.startswith("selftest-")


def add_internal_entries(entries: list[tuple[str, bytes]], name: str) -> None:
    source_root = SKILLS_ROOT / name
    if not source_root.is_dir():
        raise SystemExit(f"FAIL: missing internal Skill source: {name}")
    for path in collect_files(source_root, exclude=exclude_dev_test):
        relative = path.relative_to(source_root).as_posix()
        target = (PREFIX / "internal-skills" / name / path.relative_to(source_root)).as_posix()
        data = path.read_bytes()
        if name == "listing-hardening" and relative == HARDENING_POLICY_SOURCE:
            text = data.decode("utf-8")
            if NORMAL_POLICY_BLOCK not in text:
                raise SystemExit("FAIL: hardening core policy block changed; update compatibility patch")
            data = text.replace(NORMAL_POLICY_BLOCK, EMBEDDED_POLICY_BLOCK).encode("utf-8")
        entries.append((target, data))


def smoke_test_archive(output: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        with ZipFile(output) as archive:
            archive.extractall(tmp)
        root = tmp / "japan-listing-demo"
        result = subprocess.run(
            [sys.executable, str(root / "scripts" / "validate_install.py")],
            cwd=root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            raise SystemExit("FAIL: extracted compatibility package validation failed")
        print(result.stdout.strip())


def main() -> None:
    reject_symlinks(MAIN_SKILL)
    for name in INTERNAL_SKILL_NAMES:
        reject_symlinks(SKILLS_ROOT / name)

    entries: list[tuple[str, bytes]] = []
    for relative in MAIN_FILES:
        path = MAIN_SKILL / relative
        if not path.is_file() or path.is_symlink():
            raise SystemExit(f"FAIL: missing/unsafe main router file: {relative}")
        entries.append(((PREFIX / relative).as_posix(), path.read_bytes()))

    entries.append(((PREFIX / "scripts" / "validate_project_state.py").as_posix(), EMBEDDED_SHIM.encode("utf-8")))
    for name in INTERNAL_SKILL_NAMES:
        add_internal_entries(entries, name)
    entries.append((LIMITATION_MEMBER, LIMITATION_TEXT.encode("utf-8")))

    try:
        write_deterministic_zip(OUTPUT, entries)
    except ValueError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc

    with ZipFile(OUTPUT) as archive:
        members = set(archive.namelist())
        missing = sorted(REQUIRED_MEMBERS - members)
        if missing:
            raise SystemExit(f"FAIL: compatibility package is missing: {', '.join(missing)}")
        if any("/selftest_" in name for name in members):
            raise SystemExit("FAIL: repository-only selftests leaked into one-install package")
        note = archive.read(LIMITATION_MEMBER).decode("utf-8")
        if "HUMAN_REVIEW_REQUIRED" not in note or "listing-evidence-auditor" not in note:
            raise SystemExit("FAIL: compatibility archive semantic-audit limitation missing")

    smoke_test_archive(OUTPUT)
    print(f"PASS: deterministic one-install package contains {len(members)} runtime files")
    print(OUTPUT)


if __name__ == "__main__":
    main()
