#!/usr/bin/env python3
"""Validate japan-listing-demo and its sibling evidence auditor distribution."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
SKILL_FILE = SKILL_DIR / "SKILL.md"
AUDITOR_DIR = REPO_ROOT / ".agents" / "skills" / "listing-evidence-auditor"

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
    SKILL_DIR / "references" / "channel-native-demo.md",
    SKILL_DIR / "references" / "delivery-integrity.md",
    SKILL_DIR / "references" / "executable-gates.md",
    SKILL_DIR / "references" / "qa.md",
    SKILL_DIR / "profiles" / "channels" / "amazon-jp.md",
    SKILL_DIR / "profiles" / "channels" / "rakuten.md",
    SKILL_DIR / "profiles" / "channels" / "yahoo-shopping.md",
    SKILL_DIR / "profiles" / "channels" / "dtc.md",
    SKILL_DIR / "profiles" / "channels" / "retailer-pdp.md",
    SKILL_DIR / "evals" / "core.md",
    SKILL_DIR / "evals" / "cross-category.md",
    SKILL_DIR / "evals" / "channels.md",
    SKILL_DIR / "evals" / "delivery-integrity.md",
    SKILL_DIR / "evals" / "executable-gates.md",
    SKILL_DIR / "evals" / "evidence-auditor.md",
    SKILL_DIR / "data" / "channel-policy-limits.json",
    SKILL_DIR / "templates" / "project-state.example.json",
    SKILL_DIR / "scripts" / "validate_project_state.py",
    SKILL_DIR / "scripts" / "selftest_project_state_validator.py",
    SKILL_DIR / "scripts" / "package_skill.py",
]

REQUIRED_AUDITOR_FILES = [
    AUDITOR_DIR / "SKILL.md",
    AUDITOR_DIR / "agents" / "openai.yaml",
    AUDITOR_DIR / "references" / "audit-contract.md",
    AUDITOR_DIR / "scripts" / "fingerprint_assets.py",
    AUDITOR_DIR / "scripts" / "reconcile_evidence.py",
    AUDITOR_DIR / "scripts" / "selftest_auditor.py",
    AUDITOR_DIR / "templates" / "audit-input.example.json",
    AUDITOR_DIR / "templates" / "semantic-review.example.json",
]

REQUIRED_REPO_FILES = [
    REPO_ROOT / "README.md",
    REPO_ROOT / "CHANGELOG.md",
    REPO_ROOT / "VERSION",
    REPO_ROOT / "docs" / "install.md",
    REPO_ROOT / "scripts" / "package_codex_bundle.py",
]

CATEGORY_LEAKAGE_TERMS = [
    "SwitchBot", "Solar PTC", "ViewStation", "防犯カメラ", "玄関", "駐車場",
    "robot vacuum", "smart lock", "smart lighting", "pet tech",
]

PERSONA_LEAKAGE_PATTERNS = [
    r"Japanese consumers prefer", r"Japanese users care", r"Japanese shoppers usually",
    r"日本ユーザーは", r"日本の消費者は", r"日本人は.*好む",
]

RUNTIME_DEPENDENCY_PATTERNS = [
    r"REQUIRED SUB-SKILL", r"Load `?gtm-listing-demo`? public core",
    r"install .*gtm-listing-demo.*and.*japan-listing-demo", r"install both",
]

GUARDED_FILES = [
    SKILL_FILE,
    SKILL_DIR / "references" / "japan-market-evidence.md",
    SKILL_DIR / "references" / "ja-jp-localization.md",
    SKILL_DIR / "references" / "japan-claim-compliance.md",
    SKILL_DIR / "references" / "channel-native-demo.md",
    SKILL_DIR / "references" / "delivery-integrity.md",
    SKILL_DIR / "references" / "executable-gates.md",
    SKILL_DIR / "references" / "qa.md",
    SKILL_DIR / "profiles" / "channels" / "amazon-jp.md",
    SKILL_DIR / "profiles" / "channels" / "rakuten.md",
    SKILL_DIR / "profiles" / "channels" / "yahoo-shopping.md",
    SKILL_DIR / "profiles" / "channels" / "dtc.md",
    SKILL_DIR / "profiles" / "channels" / "retailer-pdp.md",
    AUDITOR_DIR / "SKILL.md",
    AUDITOR_DIR / "references" / "audit-contract.md",
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


def run_selftest(path: Path, label: str) -> str:
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        fail(f"{label} self-tests failed")
    return result.stdout.strip()


def main() -> int:
    required = REQUIRED_CORE_FILES + REQUIRED_JAPAN_FILES + REQUIRED_AUDITOR_FILES + REQUIRED_REPO_FILES
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

    auditor_text = (AUDITOR_DIR / "SKILL.md").read_text(encoding="utf-8")
    auditor_frontmatter = parse_frontmatter(auditor_text)
    if auditor_frontmatter.get("name") != "listing-evidence-auditor":
        fail("auditor frontmatter name must be listing-evidence-auditor")

    manifest = (SKILL_DIR / "core" / "manifest.yaml").read_text(encoding="utf-8")
    for value in ["heymio/gtm-listing-demo", "0.2.0", "b882526f5a683235d30f562006cf1984a9f0d9f9", "standalone"]:
        if value.casefold() not in manifest.casefold():
            fail(f"core manifest is missing provenance value: {value}")

    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.2.6":
        fail(f"VERSION must be 0.2.6, found {version!r}")

    all_text = "\n".join(path.read_text(encoding="utf-8") for path in required if path.suffix in {".md", ".yaml", ".txt"})
    placeholders = re.findall(r"\b(?:TODO|TBD|FIXME)\b", all_text, flags=re.I)
    if placeholders:
        fail(f"placeholder terms found: {sorted(set(placeholders))}")

    guarded_text = "\n".join(path.read_text(encoding="utf-8") for path in GUARDED_FILES)
    for term in CATEGORY_LEAKAGE_TERMS:
        if term.casefold() in guarded_text.casefold():
            fail(f"category or private-project leakage found in guarded files: {term}")

    locale_and_market_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [SKILL_DIR / "references" / "japan-market-evidence.md", SKILL_DIR / "references" / "ja-jp-localization.md"]
    )
    for pattern in PERSONA_LEAKAGE_PATTERNS:
        if re.search(pattern, locale_and_market_text, flags=re.I):
            fail(f"unsupported Japan persona statement found: {pattern}")

    eval_text = "\n".join(
        (SKILL_DIR / "evals" / name).read_text(encoding="utf-8")
        for name in ["core.md", "cross-category.md", "channels.md", "delivery-integrity.md", "executable-gates.md", "evidence-auditor.md"]
    )
    for scenario in [
        "Candidate Gallery claim loses to auditor visual-role mismatch",
        "Same filename with changed bytes loses prior approval",
        "Inline self-audit cannot unlock Stage 9",
        "One invalidated member fails the complete required set",
    ]:
        if scenario not in eval_text:
            fail(f"missing evidence-auditor evaluation scenario: {scenario}")

    workflow = (SKILL_DIR / "core" / "workflow.md").read_text(encoding="utf-8")
    openai_yaml = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    policy_text = "\n".join([skill_text, workflow, openai_yaml, auditor_text]).casefold()
    for phrase in [
        "checkpointed execution by default",
        "listing-evidence-auditor",
        "evidence_reconciliation_gate",
        "pre_demo_asset_gate",
        "stage 8.5",
        "effective state",
        "human_review_required",
        "independent context",
    ]:
        if phrase not in policy_text:
            fail(f"required v0.2.6 policy is missing: {phrase}")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8").casefold()
    install = (REPO_ROOT / "docs" / "install.md").read_text(encoding="utf-8").casefold()
    for document_name, document in [("README.md", readme), ("docs/install.md", install)]:
        for phrase in ["listing-evidence-auditor", "one repository", "human_review_required", "pre_demo_asset_gate"]:
            if phrase not in document:
                fail(f"{document_name} must explain: {phrase}")

    auditor_selftest = run_selftest(AUDITOR_DIR / "scripts" / "selftest_auditor.py", "evidence auditor")
    project_state_selftest = run_selftest(SKILL_DIR / "scripts" / "selftest_project_state_validator.py", "project-state validator")

    print(auditor_selftest)
    print(project_state_selftest)
    print("PASS: japan-listing-demo v0.2.6 distribution is valid")
    print(f"PASS: {len(required)} required files exist")
    print("PASS: sibling evidence auditor and effective-state gates are packaged and self-tested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
