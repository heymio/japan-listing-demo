#!/usr/bin/env python3
"""Validate the fail-closed five-Skill japan-listing-demo v0.3.3 distribution."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MAIN_SKILL = Path(__file__).resolve().parents[1]
REPO_ROOT = MAIN_SKILL.parents[2]
SKILLS_ROOT = REPO_ROOT / ".agents" / "skills"
THIS_FILE = Path(__file__).resolve()

SKILL_NAMES = [
    "japan-listing-demo",
    "listing-planning",
    "listing-production",
    "listing-hardening",
    "listing-evidence-auditor",
]
SKILLS = {name: SKILLS_ROOT / name for name in SKILL_NAMES}

REQUIRED_FILES = [
    SKILLS["japan-listing-demo"] / "SKILL.md",
    SKILLS["japan-listing-demo"] / "agents" / "openai.yaml",
    SKILLS["japan-listing-demo"] / "references" / "routing.md",
    SKILLS["japan-listing-demo"] / "references" / "exception-routing.md",
    SKILLS["japan-listing-demo"] / "data" / "channel-policy-limits.json",
    SKILLS["japan-listing-demo"] / "core" / "manifest.yaml",
    SKILLS["japan-listing-demo"] / "scripts" / "selftest_router.py",
    SKILLS["japan-listing-demo"] / "scripts" / "validate_project_state.py",
    SKILLS["japan-listing-demo"] / "scripts" / "selftest_project_state_validator.py",
    SKILLS["japan-listing-demo"] / "scripts" / "selftest_fail_closed_v033.py",
    SKILLS["japan-listing-demo"] / "scripts" / "selftest_distribution_v033.py",
    SKILLS["japan-listing-demo"] / "scripts" / "package_skill.py",
    SKILLS["listing-planning"] / "SKILL.md",
    SKILLS["listing-planning"] / "agents" / "openai.yaml",
    SKILLS["listing-planning"] / "references" / "source-authority.md",
    SKILLS["listing-planning"] / "references" / "market-research.md",
    SKILLS["listing-planning"] / "references" / "localization.md",
    SKILLS["listing-planning"] / "references" / "claim-compliance.md",
    SKILLS["listing-planning"] / "references" / "channel-planning.md",
    SKILLS["listing-planning"] / "references" / "module-fit.md",
    SKILLS["listing-planning"] / "references" / "planning-qa.md",
    SKILLS["listing-planning"] / "templates" / "project-brief.example.yaml",
    SKILLS["listing-planning"] / "templates" / "creative-strategy.example.yaml",
    SKILLS["listing-planning"] / "templates" / "production-handoff.example.yaml",
    SKILLS["listing-planning"] / "scripts" / "validate_planning_contracts.py",
    SKILLS["listing-planning"] / "scripts" / "account_capability.py",
    SKILLS["listing-planning"] / "scripts" / "selftest_planning.py",
    SKILLS["listing-planning"] / "evals" / "planning.md",
    SKILLS["listing-planning"] / "profiles" / "channels" / "amazon-jp.md",
    SKILLS["listing-planning"] / "profiles" / "channels" / "rakuten.md",
    SKILLS["listing-planning"] / "profiles" / "channels" / "yahoo-shopping.md",
    SKILLS["listing-planning"] / "profiles" / "channels" / "dtc.md",
    SKILLS["listing-planning"] / "profiles" / "channels" / "retailer-pdp.md",
    SKILLS["listing-production"] / "SKILL.md",
    SKILLS["listing-production"] / "agents" / "openai.yaml",
    SKILLS["listing-production"] / "references" / "visual-production.md",
    SKILLS["listing-production"] / "references" / "benchmark-policy.md",
    SKILLS["listing-production"] / "references" / "production-qa.md",
    SKILLS["listing-production"] / "references" / "golden-examples.md",
    SKILLS["listing-production"] / "references" / "visual-patterns" / "hero-positioning.md",
    SKILLS["listing-production"] / "references" / "visual-patterns" / "compact-proof.md",
    SKILLS["listing-production"] / "references" / "visual-patterns" / "mechanism-explainer.md",
    SKILLS["listing-production"] / "references" / "visual-patterns" / "automation-flow.md",
    SKILLS["listing-production"] / "references" / "visual-patterns" / "comparison.md",
    SKILLS["listing-production"] / "references" / "visual-patterns" / "installation-decision.md",
    SKILLS["listing-production"] / "references" / "visual-patterns" / "ui-proof.md",
    SKILLS["listing-production"] / "templates" / "asset-packet.example.yaml",
    SKILLS["listing-production"] / "templates" / "asset-ledger.example.yaml",
    SKILLS["listing-production"] / "templates" / "production-freeze.example.yaml",
    SKILLS["listing-production"] / "scripts" / "project_asset_packet.py",
    SKILLS["listing-production"] / "scripts" / "production_state.py",
    SKILLS["listing-production"] / "scripts" / "production_state_legacy.py",
    SKILLS["listing-production"] / "scripts" / "set_level_qa.py",
    SKILLS["listing-production"] / "scripts" / "cleanup_policy.py",
    SKILLS["listing-production"] / "scripts" / "selftest_production.py",
    SKILLS["listing-production"] / "scripts" / "selftest_production_legacy.py",
    SKILLS["listing-production"] / "evals" / "production.md",
    SKILLS["listing-hardening"] / "SKILL.md",
    SKILLS["listing-hardening"] / "agents" / "openai.yaml",
    SKILLS["listing-hardening"] / "references" / "asset-integrity.md",
    SKILLS["listing-hardening"] / "references" / "executable-gates.md",
    SKILLS["listing-hardening"] / "references" / "frontend-fidelity.md",
    SKILLS["listing-hardening"] / "references" / "final-qa.md",
    SKILLS["listing-hardening"] / "references" / "demo-output.md",
    SKILLS["listing-hardening"] / "templates" / "delivery-state.example.json",
    SKILLS["listing-hardening"] / "scripts" / "validate_delivery_state.py",
    SKILLS["listing-hardening"] / "scripts" / "_delivery_state_core.py",
    SKILLS["listing-hardening"] / "scripts" / "validate_demo_html.py",
    SKILLS["listing-hardening"] / "scripts" / "validate_demo_html_legacy.py",
    SKILLS["listing-hardening"] / "scripts" / "validate_demo_runtime.py",
    SKILLS["listing-hardening"] / "scripts" / "selftest_hardening.py",
    SKILLS["listing-hardening"] / "scripts" / "selftest_hardening_legacy.py",
    SKILLS["listing-hardening"] / "scripts" / "selftest_demo_output.py",
    SKILLS["listing-hardening"] / "scripts" / "selftest_demo_output_legacy.py",
    SKILLS["listing-hardening"] / "evals" / "hardening.md",
    SKILLS["listing-evidence-auditor"] / "SKILL.md",
    SKILLS["listing-evidence-auditor"] / "agents" / "openai.yaml",
    SKILLS["listing-evidence-auditor"] / "references" / "audit-contract.md",
    SKILLS["listing-evidence-auditor"] / "scripts" / "fingerprint_assets.py",
    SKILLS["listing-evidence-auditor"] / "scripts" / "fingerprint_assets_legacy.py",
    SKILLS["listing-evidence-auditor"] / "scripts" / "reconcile_evidence.py",
    SKILLS["listing-evidence-auditor"] / "scripts" / "reconcile_evidence_legacy.py",
    SKILLS["listing-evidence-auditor"] / "scripts" / "selftest_auditor.py",
    SKILLS["listing-evidence-auditor"] / "templates" / "audit-input.example.json",
    SKILLS["listing-evidence-auditor"] / "templates" / "semantic-review.example.json",
    REPO_ROOT / "README.md",
    REPO_ROOT / "CHANGELOG.md",
    REPO_ROOT / "VERSION",
    REPO_ROOT / "docs" / "install.md",
    REPO_ROOT / "docs" / "team-gpt-setup.md",
    REPO_ROOT / "docs" / "release-notes-v0.3.3.md",
    REPO_ROOT / "scripts" / "package_common.py",
    REPO_ROOT / "scripts" / "package_codex_bundle.py",
    REPO_ROOT / ".github" / "workflows" / "release-validated.yml",
]

LEGACY_RUNTIME_FILES = [
    MAIN_SKILL / "core" / "workflow.md",
    MAIN_SKILL / "core" / "contracts.md",
    MAIN_SKILL / "core" / "market-research.md",
    MAIN_SKILL / "core" / "localization.md",
    MAIN_SKILL / "core" / "visual-evidence.md",
    MAIN_SKILL / "core" / "qa.md",
    MAIN_SKILL / "references" / "core-snapshot.md",
    MAIN_SKILL / "references" / "japan-market-evidence.md",
    MAIN_SKILL / "references" / "ja-jp-localization.md",
    MAIN_SKILL / "references" / "japan-claim-compliance.md",
    MAIN_SKILL / "references" / "delivery-integrity.md",
    MAIN_SKILL / "references" / "executable-gates.md",
    MAIN_SKILL / "references" / "channel-native-demo.md",
    MAIN_SKILL / "references" / "qa.md",
    MAIN_SKILL / "profiles" / "channels" / "amazon-jp.md",
    MAIN_SKILL / "profiles" / "channels" / "rakuten.md",
    MAIN_SKILL / "profiles" / "channels" / "yahoo-shopping.md",
    MAIN_SKILL / "profiles" / "channels" / "dtc.md",
    MAIN_SKILL / "profiles" / "channels" / "retailer-pdp.md",
]

CATEGORY_LEAKAGE_TERMS = [
    "Switch" + "Bot",
    "Solar" + " PTC",
    "View" + "Station",
    "防犯" + "カメラ",
    "玄" + "関",
    "駐" + "車場",
    "robot " + "vacuum",
    "smart " + "lock",
    "smart " + "lighting",
    "pet " + "tech",
]
PERSONA_LEAKAGE_PATTERNS = [
    r"Japanese consumers prefer",
    r"Japanese users care",
    r"Japanese shoppers usually",
    r"日本ユーザーは",
    r"日本の消費者は",
    r"日本人は.*好む",
]
ROUTER_FORBIDDEN = [
    "sha-256",
    "provenance_conflict",
    "pre_demo_asset_gate",
    "delivery_parity_gate",
    "declared_gate_results",
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


def text_files_under(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and path.resolve() != THIS_FILE
        and path.suffix.lower() in {".md", ".yaml", ".yml", ".json", ".txt", ".py"}
        and "__pycache__" not in path.parts
    ]


def main() -> int:
    missing = [str(path.relative_to(REPO_ROOT)) for path in REQUIRED_FILES if not path.exists()]
    if missing:
        fail(f"missing v0.3.3 distribution files: {', '.join(missing)}")

    if (REPO_ROOT / "x").exists():
        fail("stray root file 'x' must not be present in a release distribution")
    if (REPO_ROOT / ".github" / "workflows" / "release-v0.3.2.yml").exists():
        fail("unsafe legacy release-v0.3.2.yml must be removed")

    legacy = [str(path.relative_to(REPO_ROOT)) for path in LEGACY_RUNTIME_FILES if path.exists()]
    if legacy:
        fail(f"legacy monolithic runtime files still active: {', '.join(legacy)}")

    for name, directory in SKILLS.items():
        frontmatter = parse_frontmatter((directory / "SKILL.md").read_text(encoding="utf-8"))
        if frontmatter.get("name") != name:
            fail(f"{name}: frontmatter name mismatch")
        if not frontmatter.get("description", "").startswith("Use when "):
            fail(f"{name}: description must start with 'Use when '")

    router_text = (MAIN_SKILL / "SKILL.md").read_text(encoding="utf-8")
    router_prompt = (MAIN_SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
    if "standalone" not in router_text.casefold():
        fail("main router must state standalone distribution")
    if len(router_text) > 9000:
        fail(f"main router is too large: {len(router_text)} chars")
    if len(router_prompt) > 2200:
        fail(f"router default prompt is too large: {len(router_prompt)} chars")
    for term in ROUTER_FORBIDDEN:
        if term in router_prompt.casefold():
            fail(f"hardening control-plane term leaked into router default prompt: {term}")

    routing_text = (MAIN_SKILL / "references" / "routing.md").read_text(encoding="utf-8").casefold()
    for phrase in [
        "stage 0–7", "listing-planning", "stage 7.5–8", "listing-production",
        "stage 8.5–10", "listing-hardening", "done:", "open:", "next:",
    ]:
        if phrase.casefold() not in routing_text:
            fail(f"router contract missing: {phrase}")

    version = (REPO_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.3.3":
        fail(f"VERSION must be 0.3.3, found {version!r}")

    manifest = (MAIN_SKILL / "core" / "manifest.yaml").read_text(encoding="utf-8").casefold()
    for phrase in [
        "standalone",
        "listing-planning",
        "listing-production",
        "listing-hardening",
        "listing-evidence-auditor",
        "validator-integrity-v0.3.1",
        "production-ux-set-level-creative-qa-v0.3.2",
        "fail-closed-hard-verification-v0.3.3",
        "frontend_fidelity_gate",
        "demo_runtime_gate",
    ]:
        if phrase not in manifest:
            fail(f"core manifest missing v0.3.3 architecture/integrity marker: {phrase}")

    active_files: list[Path] = []
    for directory in SKILLS.values():
        active_files.extend(text_files_under(directory))

    for term in CATEGORY_LEAKAGE_TERMS:
        offenders = [
            str(path.relative_to(REPO_ROOT))
            for path in active_files
            if term.casefold() in path.read_text(encoding="utf-8").casefold()
        ]
        if offenders:
            fail(f"category/private-project leakage found for {term!r}: " + ", ".join(offenders))

    active_text = "\n".join(path.read_text(encoding="utf-8") for path in active_files)
    planning_locale = "\n".join(
        (SKILLS["listing-planning"] / "references" / name).read_text(encoding="utf-8")
        for name in ["market-research.md", "localization.md"]
    )
    for pattern in PERSONA_LEAKAGE_PATTERNS:
        if re.search(pattern, planning_locale, flags=re.I):
            fail(f"unsupported Japan persona statement found: {pattern}")

    placeholders = re.findall(r"\b(?:TODO|TBD|FIXME)\b", active_text, flags=re.I)
    if placeholders:
        fail(f"placeholder terms found in active Skills: {sorted(set(placeholders))}")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8").casefold()
    install = (REPO_ROOT / "docs" / "install.md").read_text(encoding="utf-8").casefold()
    gpt_guide = (REPO_ROOT / "docs" / "team-gpt-setup.md").read_text(encoding="utf-8").casefold()
    for document_name, document, phrases in [
        ("README.md", readme, ["one repository", "$japan-listing-demo", "listing-planning", "listing-production", "listing-hardening", "0.3.3"]),
        ("docs/install.md", install, ["one repository", "$japan-listing-demo", "listing-evidence-auditor", "0.3.3"]),
        ("docs/team-gpt-setup.md", gpt_guide, ["gpt = optional ux shell", "skills = versioned execution architecture", "auditor/scripts = hard verification"]),
    ]:
        for phrase in phrases:
            if phrase.casefold() not in document:
                fail(f"{document_name} must explain: {phrase}")

    outputs = [
        run_selftest(MAIN_SKILL / "scripts" / "selftest_fail_closed_v033.py", "v0.3.3 fail-closed adversarial"),
        run_selftest(SKILLS["listing-planning"] / "scripts" / "selftest_planning.py", "planning"),
        run_selftest(SKILLS["listing-production"] / "scripts" / "selftest_production.py", "production"),
        run_selftest(SKILLS["listing-hardening"] / "scripts" / "selftest_hardening.py", "hardening"),
        run_selftest(SKILLS["listing-hardening"] / "scripts" / "selftest_demo_output.py", "standalone demo output"),
        run_selftest(SKILLS["listing-evidence-auditor"] / "scripts" / "selftest_auditor.py", "evidence auditor"),
        run_selftest(MAIN_SKILL / "scripts" / "selftest_router.py", "router"),
        run_selftest(MAIN_SKILL / "scripts" / "selftest_project_state_validator.py", "project-state compatibility"),
        run_selftest(MAIN_SKILL / "scripts" / "selftest_distribution_v033.py", "v0.3.3 distribution/release"),
    ]

    print("\n".join(outputs))
    print("PASS: japan-listing-demo v0.3.3 fail-closed distribution is valid")
    print(f"PASS: {len(REQUIRED_FILES)} required files exist across five Skills")
    print("PASS: fail-closed hardening, stage Skills, evidence auditor, runtime Demo contract, packaging and release contract are self-tested")
    return 0


if __name__ == "__main__":
    sys.exit(main())
