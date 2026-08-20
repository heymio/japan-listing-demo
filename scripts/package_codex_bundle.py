#!/usr/bin/env python3
"""Package japan-listing-demo plus listing-evidence-auditor for repository/Codex use."""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
MAIN_SKILL = SKILLS_ROOT / "japan-listing-demo"
AUDITOR_SKILL = SKILLS_ROOT / "listing-evidence-auditor"
DIST_DIR = REPO_ROOT / "dist"
OUTPUT = DIST_DIR / "japan-listing-demo-codex-bundle.zip"

REQUIRED_MEMBERS = {
    ".agents/skills/japan-listing-demo/SKILL.md",
    ".agents/skills/japan-listing-demo/scripts/validate_project_state.py",
    ".agents/skills/listing-evidence-auditor/SKILL.md",
    ".agents/skills/listing-evidence-auditor/scripts/fingerprint_assets.py",
    ".agents/skills/listing-evidence-auditor/scripts/reconcile_evidence.py",
}


def add_tree(archive: ZipFile, root: Path) -> None:
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            archive.write(path, path.relative_to(REPO_ROOT))


def main() -> None:
    for directory in [MAIN_SKILL, AUDITOR_SKILL]:
        if not directory.is_dir():
            raise SystemExit(f"FAIL: missing Skill directory: {directory.relative_to(REPO_ROOT)}")

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        add_tree(archive, MAIN_SKILL)
        add_tree(archive, AUDITOR_SKILL)

    with ZipFile(OUTPUT) as archive:
        members = set(archive.namelist())
        missing = sorted(REQUIRED_MEMBERS - members)
        if missing:
            raise SystemExit(f"FAIL: Codex bundle is missing: {', '.join(missing)}")

    print(f"PASS: Codex bundle contains {len(members)} files across two sibling Skills")
    print(OUTPUT)


if __name__ == "__main__":
    main()
