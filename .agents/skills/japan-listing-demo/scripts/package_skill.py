#!/usr/bin/env python3
"""Package and verify japan-listing-demo as a standalone Skill ZIP."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
DIST_DIR = REPO_ROOT / "dist"
OUTPUT = DIST_DIR / "japan-listing-demo.skill.zip"
PREFIX = Path(SKILL_DIR.name)

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
    "japan-listing-demo/references/qa.md",
    "japan-listing-demo/profiles/channels/amazon-jp.md",
    "japan-listing-demo/profiles/channels/rakuten.md",
    "japan-listing-demo/profiles/channels/yahoo-shopping.md",
    "japan-listing-demo/profiles/channels/dtc.md",
    "japan-listing-demo/profiles/channels/retailer-pdp.md",
}


def main() -> None:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as archive:
        for path in sorted(SKILL_DIR.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, PREFIX / path.relative_to(SKILL_DIR))

    with ZipFile(OUTPUT) as archive:
        members = set(archive.namelist())
        missing = sorted(REQUIRED_MEMBERS - members)
        if missing:
            raise SystemExit(f"FAIL: standalone package is missing: {', '.join(missing)}")
        if any(name.endswith("references/public-core.md") for name in members):
            raise SystemExit("FAIL: obsolete runtime dependency file is present")

    print(f"PASS: standalone Skill package contains {len(members)} files")
    print(OUTPUT)


if __name__ == "__main__":
    main()
