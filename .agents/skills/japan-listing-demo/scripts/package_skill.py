#!/usr/bin/env python3
"""Package and verify japan-listing-demo as a compatibility single-Skill ZIP."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
DIST_DIR = REPO_ROOT / "dist"
OUTPUT = DIST_DIR / "japan-listing-demo.skill.zip"
PREFIX = Path(SKILL_DIR.name)
LIMITATION_MEMBER = "japan-listing-demo/SINGLE_CONTEXT_LIMITATION.txt"
LIMITATION_TEXT = (
    "This compatibility archive contains the main Skill only. It cannot claim an independent "
    "semantic evidence audit. When no independent listing-evidence-auditor context is available, "
    "semantic evidence remains UNVERIFIED / HUMAN_REVIEW_REQUIRED unless the user explicitly "
    "approves the exact asset hash + role/scope.\n"
)

REQUIRED_MEMBERS = {
    "japan-listing-demo/SKILL.md",
    "japan-listing-demo/agents/openai.yaml",
    "japan-listing-demo/core/manifest.yaml",
    "japan-listing-demo/core/workflow.md",
    "japan-listing-demo/core/contracts.md",
    "japan-listing-demo/core/market-research.md",
    "japan-listing-demo/core/localization.md",
    "japan-listing-demo/core/visual-evidence.md",
    "japan-listing-demo/core/qa.md",
    "japan-listing-demo/core/profiles/categories/_template.md",
    "japan-listing-demo/core/evals/core.md",
    "japan-listing-demo/core/evals/cross-category.md",
    "japan-listing-demo/core/evals/multichannel.md",
    "japan-listing-demo/references/core-snapshot.md",
    "japan-listing-demo/references/japan-market-evidence.md",
    "japan-listing-demo/references/ja-jp-localization.md",
    "japan-listing-demo/references/japan-claim-compliance.md",
    "japan-listing-demo/references/channel-native-demo.md",
    "japan-listing-demo/references/delivery-integrity.md",
    "japan-listing-demo/references/executable-gates.md",
    "japan-listing-demo/references/qa.md",
    "japan-listing-demo/profiles/channels/amazon-jp.md",
    "japan-listing-demo/profiles/channels/rakuten.md",
    "japan-listing-demo/profiles/channels/yahoo-shopping.md",
    "japan-listing-demo/profiles/channels/dtc.md",
    "japan-listing-demo/profiles/channels/retailer-pdp.md",
    "japan-listing-demo/evals/delivery-integrity.md",
    "japan-listing-demo/evals/executable-gates.md",
    "japan-listing-demo/evals/evidence-auditor.md",
    "japan-listing-demo/data/channel-policy-limits.json",
    "japan-listing-demo/templates/project-state.example.json",
    "japan-listing-demo/scripts/validate_project_state.py",
    "japan-listing-demo/scripts/selftest_project_state_validator.py",
    LIMITATION_MEMBER,
}


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for path in sorted(SKILL_DIR.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, PREFIX / path.relative_to(SKILL_DIR))
        archive.writestr(LIMITATION_MEMBER, LIMITATION_TEXT)

    with ZipFile(OUTPUT) as archive:
        members = set(archive.namelist())
        missing = sorted(REQUIRED_MEMBERS - members)
        if missing:
            raise SystemExit(f"FAIL: standalone package is missing: {', '.join(missing)}")
        note = archive.read(LIMITATION_MEMBER).decode("utf-8")
        if "HUMAN_REVIEW_REQUIRED" not in note or "listing-evidence-auditor" not in note:
            raise SystemExit("FAIL: compatibility archive is missing semantic-audit limitation text")
        if any(name.endswith("references/public-core.md") for name in members):
            raise SystemExit("FAIL: obsolete runtime dependency file is present")

    print(f"PASS: compatibility single-Skill package contains {len(members)} files")
    print(OUTPUT)


if __name__ == "__main__":
    main()
