#!/usr/bin/env python3
"""Validate japan-listing-demo as a standalone public Skill distribution."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
SKILL_FILE = SKILL_DIR / "SKILL.md"

REQUIRED_CORE_FILES = [
    SKILL_DIR / "core" / "manifest.yaml",
    SKILL_DIR / "core" / "workflow.md",
    SKILL_DIR / "core" / "contracts.md",
    SKILL_DIR / "core" / "market-research.md",
    SKILL_DIR / "core" / "localization.md",
    SKILL_DIR / "core" / "visual-evidence.md",
    SKILL_DIR / "core" / "qa.md",
    SKILL_DIR / "core" / "profiles" / "categories" / "_template.md",
    SKILL_DIR / "core" / "evals" / "core.md",
    SKILL_DIR / "core" / "evals" / "cross-category.md",
    SKILL_DIR / "core" / "evals" / "multichannel.md",
]

REQUIRED_JAPAN_FILES = [
    SKILL_FILE,
    SKILL_DIR / "agents" / "openai.yaml",
    SKILL_DIR / "references" / "core-snapshot.md",
    SKILL_DIR / "references" / "japan-market-evidence.md",
    SKILL_DIR / "references" / "ja-jp-localization.md",
    SKILL_DIR / "references" / "japan-claim-compliance.md",
    SKILL_DIR / "references" / "qa.md",
    SKILL_DIR / "profiles" / "channels" / "amazon-jp.md",
    SKILL_DIR / "profiles" / "channels" / "rakuten.md",
    SKILL_DIR / "profiles" / "channels" / "yahoo-shopping.md",
    SKILL_DIR / "profiles" / "channels" / "dtc.md",
    SKILL_DIR / "profiles" / "channels" / "retailer-pdp.md",
    SKILL_DIR / "evals" / "core.md",
    SKILL_DIR / "evals" / "cross-category.md",
    SKILL_DIR / "evals" / "channels.md",
    SKILL_DIR / "scripts" / "package_skill.py",
]

REQUIRED_REPO_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "CHANGELOG.md",
    REPO_ROOT / "VERSION",
    REPO_ROOT / "docs" / "install.md",
]

CATEGORY_LEAKAGE_TERMS = [
    "SwitchBot",
    "Solar PTC",
    "ViewStation",
    "防犯カメラ",
    "玄関",
    "駐車場",
    "robot vacuum",
    "smart lock",
    "smart lighting",
    "pet tech",
]

PERSONA_LEAKAGE_PATTERNS = [
    r"Japanese consumers prefer",
    r"Japanese users care",
    r"Japanese shoppers usually",
    r"日本ユーザーは",
    r"日本の消費者は",
    r"日本人は.*好む",
]

RUNTIME_DEPENDENCY_PATTERNS = [
    r"REQUIRED SUB-SKILL",
    r"Load `?gtm-listing-demo`? public core",
    r"install .*gtm-listing-demo.*and.*japan-listing-demo",
    r"install both",
]

GUARDED_FILES = [
    SKILL_FILE,
    SKILL_DIR / "references" / "japan-market-evidence.md",
    SKILL_DIR / "references" / "ja-jp-localization.md",
    SKILL_DIR / "references" / "japan-claim-compliance.md",
    SKILL_DIR / "references" / "qa.md",
    SKILL_DIR / "profiles" / "channels" / "amazon-jp.md",
    SKILL_DIR / "profiles" / "channels" / "rakuten.md",
    SKILL_DIR / "profiles" / "channels" / "yahoo-shopping.md",
    SKILL_DIR / "profiles" / "channels" / "dtc.md",
    SKILL_DIR / "profiles" / "channels" / "retailer-pdp.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.S)
    if not match:
        fail("SKILL.md is missing YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def main() -> int:
    required = REQUIRED_CORE_FILES + REQUIRED_JAPAN_FILES + REQUIRED_REPO_FILES
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        fail(f"missing standalone files: {', '.join(missing)}")

    skill_text = SKILL_FILE.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(skill_text)
    if frontmatter.get("name") != "japan-listing-demo":
        fail("frontmatter name must be japan-listing-demo")
    if not frontmatter.get("description", "").startswith("Use when "):
        fail("description must start with 'Use when '")
    if "standalone" not in skill_text.casefold():
        fail("SKILL.md must state that this is a standalone distribution")
    for pattern in RUNTIME_DEPENDENCY_PATTERNS:
        if re.search(pattern, skill_text, flags=re.I | re.S):
            fail(f"runtime dependency wording found in SKILL.md: {pattern}")

    manifest = (SKILL_DIR / "core" / "manifest.yaml").read_text(encoding="utf-8")
    for value in [
        "heymio/gtm-listing-demo",
        "0.2.0",
        "b882526f5a683235d30f562006cf1984a9f0d9f9",
        "standalone",
    ]:
        if value.casefold() not in manifest.casefold():
            fail(f"core manifest is missing provenance value: {value}")

    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.2.0":
        fail(f"VERSION must be 0.2.0, found {version!r}")

    all_text = "\n".join(path.read_text(encoding="utf-8") for path in required)
    placeholders = re.findall(r"\b(?:TODO|TBD|FIXME)\b", all_text, flags=re.I)
    if placeholders:
        fail(f"placeholder terms found: {sorted(set(placeholders))}")

    guarded_text = "\n".join(path.read_text(encoding="utf-8") for path in GUARDED_FILES)
    for term in CATEGORY_LEAKAGE_TERMS:
        if term.casefold() in guarded_text.casefold():
            fail(f"category or private-project leakage found in guarded files: {term}")

    locale_and_market_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            SKILL_DIR / "references" / "japan-market-evidence.md",
            SKILL_DIR / "references" / "ja-jp-localization.md",
        ]
    )
    for pattern in PERSONA_LEAKAGE_PATTERNS:
        if re.search(pattern, locale_and_market_text, flags=re.I):
            fail(f"unsupported Japan persona statement found: {pattern}")

    evidence_contract = (SKILL_DIR / "references" / "japan-market-evidence.md").read_text(encoding="utf-8")
    for field in ["source", "date", "category", "channel", "evidence type", "confidence", "allowed usage"]:
        if field not in evidence_contract.casefold():
            fail(f"Japan market evidence contract is missing: {field}")

    eval_text = "\n".join(
        (SKILL_DIR / "evals" / name).read_text(encoding="utf-8")
        for name in ["core.md", "cross-category.md", "channels.md"]
    )
    for scenario in [
        "Standalone Japan team installation",
        "Japan market without category evidence",
        "Japan market with a non-Japanese locale",
        "Rakuten project must not inherit Amazon modules",
        "Category conclusions must not leak across projects",
    ]:
        if scenario not in eval_text:
            fail(f"missing evaluation scenario: {scenario}")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    install = (REPO_ROOT / "docs" / "install.md").read_text(encoding="utf-8")
    for document_name, document in [("README.md", readme), ("docs/install.md", install)]:
        if "one skill" not in document.casefold() and "一个 skill" not in document.casefold():
            fail(f"{document_name} must explain one-Skill installation")

    print("PASS: japan-listing-demo standalone distribution is valid")
    print(f"PASS: {len(required)} required files exist")
    print("PASS: bundled core provenance and version are valid")
    print("PASS: no second-Skill runtime dependency is present")
    print("PASS: category and persona leakage checks passed")
    print("PASS: Japan evidence contract and standalone eval coverage passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
