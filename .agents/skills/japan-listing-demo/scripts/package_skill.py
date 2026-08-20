#!/usr/bin/env python3
"""Package one-install compatibility ZIP with embedded creative-first stage Skills."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

MAIN_SKILL = Path(__file__).resolve().parents[1]
REPO_ROOT = MAIN_SKILL.parents[2]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
DIST_DIR = REPO_ROOT / "dist"
OUTPUT = DIST_DIR / "japan-listing-demo.skill.zip"
PREFIX = Path("japan-listing-demo")

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
    "scripts/selftest_router.py",
    "scripts/selftest_project_state_validator.py",
    "evals/creative-first-hardening.md",
    "evals/team-golden-path.md",
]

LIMITATION_MEMBER = "japan-listing-demo/SINGLE_CONTEXT_LIMITATION.txt"
LIMITATION_TEXT = (
    "This compatibility archive is one model context. Internal stage separation and Context Projection "
    "still apply, but loading the embedded listing-evidence-auditor does not create independent semantic "
    "review. Deterministic file checks may run; unresolved semantic evidence remains UNVERIFIED / "
    "HUMAN_REVIEW_REQUIRED unless resolved by human or genuinely independent review.\n"
)

EMBEDDED_SHIM = '''#!/usr/bin/env python3
"""Compatibility shim for the embedded listing-hardening validator."""
from __future__ import annotations
import importlib.util
from pathlib import Path
HERE = Path(__file__).resolve()
MAIN_SKILL = HERE.parents[1]
TARGET = MAIN_SKILL / "internal-skills" / "listing-hardening" / "scripts" / "validate_delivery_state.py"
SPEC = importlib.util.spec_from_file_location("embedded_listing_hardening_validate_delivery_state", TARGET)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load embedded hardening validator: {TARGET}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
canonical_hash = MODULE.canonical_hash
validate_state = MODULE.validate_state
main = MODULE.main
if __name__ == "__main__":
    raise SystemExit(main())
'''

NORMAL_POLICY_BLOCK = '''SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
DEFAULT_POLICY_PATH = REPO_ROOT / ".agents" / "skills" / "japan-listing-demo" / "data" / "channel-policy-limits.json"'''
EMBEDDED_POLICY_BLOCK = '''SCRIPT_DIR = Path(__file__).resolve().parent
EMBEDDED_MAIN_SKILL = SCRIPT_DIR.parents[2]
DEFAULT_POLICY_PATH = EMBEDDED_MAIN_SKILL / "data" / "channel-policy-limits.json"'''

REQUIRED_MEMBERS = {
    "japan-listing-demo/SKILL.md",
    "japan-listing-demo/agents/openai.yaml",
    "japan-listing-demo/references/routing.md",
    "japan-listing-demo/references/exception-routing.md",
    "japan-listing-demo/data/channel-policy-limits.json",
    "japan-listing-demo/scripts/validate_project_state.py",
    "japan-listing-demo/internal-skills/listing-planning/SKILL.md",
    "japan-listing-demo/internal-skills/listing-production/SKILL.md",
    "japan-listing-demo/internal-skills/listing-production/scripts/project_asset_packet.py",
    "japan-listing-demo/internal-skills/listing-hardening/SKILL.md",
    "japan-listing-demo/internal-skills/listing-hardening/scripts/validate_delivery_state.py",
    "japan-listing-demo/internal-skills/listing-evidence-auditor/SKILL.md",
    "japan-listing-demo/internal-skills/listing-evidence-auditor/scripts/fingerprint_assets.py",
    LIMITATION_MEMBER,
}


def add_internal_skill(archive: ZipFile, name: str) -> None:
    source_root = SKILLS_ROOT / name
    if not source_root.is_dir():
        raise SystemExit(f"FAIL: missing internal Skill source: {name}")
    for path in sorted(source_root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        target = PREFIX / "internal-skills" / name / path.relative_to(source_root)
        if name == "listing-hardening" and path.relative_to(source_root).as_posix() == "scripts/validate_delivery_state.py":
            text = path.read_text(encoding="utf-8")
            if NORMAL_POLICY_BLOCK not in text:
                raise SystemExit("FAIL: hardening validator policy block changed; update compatibility patch")
            archive.writestr(target.as_posix(), text.replace(NORMAL_POLICY_BLOCK, EMBEDDED_POLICY_BLOCK))
        else:
            archive.write(path, target)


def smoke_test_archive(output: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        with ZipFile(output) as archive:
            archive.extractall(tmp)
        root = tmp / "japan-listing-demo"
        state = {
            "schema_version": "0.1",
            "channel": {"id": "amazon-jp", "enhanced_content": {"tier": "premium", "declared_max_modules": 7}},
            "approval_events": [],
            "assets": [],
            "locked_module_plan": {},
            "asset_slot_contract": [],
            "implementation": {},
            "audit_checkpoints": {"post_6_5_required": False, "pre_9_required": False},
        }
        state_path = tmp / "state.json"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        commands = [
            [sys.executable, str(root / "scripts" / "selftest_router.py")],
            [sys.executable, str(root / "scripts" / "selftest_project_state_validator.py")],
            [sys.executable, str(root / "scripts" / "validate_project_state.py"), str(state_path), "--json"],
        ]
        for command in commands:
            result = subprocess.run(command, cwd=root, capture_output=True, text=True)
            if result.returncode != 0:
                print(result.stdout)
                print(result.stderr, file=sys.stderr)
                raise SystemExit(f"FAIL: compatibility archive smoke test failed: {' '.join(command)}")


def main() -> None:
    for relative in MAIN_FILES:
        if not (MAIN_SKILL / relative).is_file():
            raise SystemExit(f"FAIL: missing main router file: {relative}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for relative in MAIN_FILES:
            archive.write(MAIN_SKILL / relative, PREFIX / relative)
        archive.writestr((PREFIX / "scripts" / "validate_project_state.py").as_posix(), EMBEDDED_SHIM)
        for name in INTERNAL_SKILL_NAMES:
            add_internal_skill(archive, name)
        archive.writestr(LIMITATION_MEMBER, LIMITATION_TEXT)

    with ZipFile(OUTPUT) as archive:
        members = set(archive.namelist())
        missing = sorted(REQUIRED_MEMBERS - members)
        if missing:
            raise SystemExit(f"FAIL: compatibility package is missing: {', '.join(missing)}")
        note = archive.read(LIMITATION_MEMBER).decode("utf-8")
        if "HUMAN_REVIEW_REQUIRED" not in note or "listing-evidence-auditor" not in note:
            raise SystemExit("FAIL: compatibility archive is missing semantic-audit limitation text")
        if any("core/workflow.md" in name or "references/delivery-integrity.md" in name for name in members):
            raise SystemExit("FAIL: legacy monolithic runtime content leaked into compatibility archive")

    smoke_test_archive(OUTPUT)
    print(f"PASS: one-install compatibility package contains {len(members)} files with four embedded internal Skills")
    print(OUTPUT)


if __name__ == "__main__":
    main()
