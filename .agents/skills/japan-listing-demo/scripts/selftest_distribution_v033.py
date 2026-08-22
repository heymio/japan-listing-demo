#!/usr/bin/env python3
"""Regression tests for v0.3.3 packaging/release integrity."""

from __future__ import annotations

import re
from pathlib import Path

MAIN_SKILL = Path(__file__).resolve().parents[1]
REPO_ROOT = MAIN_SKILL.parents[2]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_version_and_changelog_are_v033() -> None:
    assert read(REPO_ROOT / "VERSION").strip() == "0.3.3"
    assert "## 0.3.3" in read(REPO_ROOT / "CHANGELOG.md")


def test_release_is_triggered_only_by_successful_validation_sha() -> None:
    old = REPO_ROOT / ".github" / "workflows" / "release-v0.3.2.yml"
    workflow = REPO_ROOT / ".github" / "workflows" / "release-validated.yml"
    assert not old.exists(), "fixed v0.3.2 push release workflow must be removed"
    assert workflow.is_file()
    text = read(workflow).casefold()
    for phrase in [
        "workflow_run:",
        "validate japan-listing-demo skill",
        "conclusion == 'success'",
        "github.event.workflow_run.head_sha",
        "persist-credentials: false",
        "contents: read",
        "contents: write",
    ]:
        assert phrase in text, phrase
    assert "push:\n    branches: [main]" not in text
    build_block = text.split("publish:", 1)[0]
    assert "contents: write" not in build_block, "build job must not receive contents write"


def test_release_checksums_use_download_local_basenames() -> None:
    text = read(REPO_ROOT / ".github" / "workflows" / "release-validated.yml")
    assert "cd dist" in text or "(cd dist" in text
    checksum_lines = [line.strip() for line in text.splitlines() if "sha256sum" in line or "SHA256SUMS" in line]
    joined = "\n".join(checksum_lines)
    assert "dist/japan-listing-demo.skill.zip" not in joined
    assert "dist/japan-listing-demo-codex-bundle.zip" not in joined


def test_packagers_are_deterministic_symlink_safe_and_self_validating() -> None:
    compatibility = read(MAIN_SKILL / "scripts" / "package_skill.py")
    codex = read(REPO_ROOT / "scripts" / "package_codex_bundle.py")
    common = read(REPO_ROOT / "scripts" / "package_common.py")
    for text in [compatibility, codex]:
        assert "write_deterministic_zip" in text
        assert "reject_symlinks" in text
    assert "FIXED_ZIP_TIME" in common and "is_symlink" in common
    assert "validate_install.py" in compatibility
    assert "validate_overlay.py" in codex
    for metadata in [
        "README.md", "CHANGELOG.md", "VERSION", "docs/install.md", "docs/team-gpt-setup.md",
        "docs/release-notes-v0.3.3.md", ".github/workflows/release-validated.yml",
    ]:
        assert metadata in codex


def test_ci_executes_real_decoder_and_no_network_browser() -> None:
    workflow = read(REPO_ROOT / ".github" / "workflows" / "validate-japan-listing-demo.yml")
    for phrase in [
        "Pillow",
        "playwright",
        "playwright install --with-deps chromium",
        "selftest_image_decode_v033.py",
        "selftest_demo_runtime_v033.py",
        "persist-credentials: false",
    ]:
        assert phrase in workflow, phrase


def test_docs_use_python3_for_copyable_commands() -> None:
    for relative in ["README.md", "docs/install.md", "docs/team-gpt-setup.md"]:
        text = read(REPO_ROOT / relative)
        offenders = re.findall(r"(?m)^\s*python\s+[^3]", text)
        assert not offenders, (relative, offenders)


def test_manifest_and_overlay_identify_fail_closed_v033() -> None:
    manifest = read(MAIN_SKILL / "core" / "manifest.yaml").casefold()
    overlay = read(MAIN_SKILL / "scripts" / "validate_overlay.py").casefold()
    for phrase in ["fail-closed-hard-verification-v0.3.3", "0.3.3"]:
        assert phrase in manifest or phrase in overlay, phrase
    assert "version != \"0.3.3\"" in overlay


def main() -> int:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} v0.3.3 distribution/release tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
