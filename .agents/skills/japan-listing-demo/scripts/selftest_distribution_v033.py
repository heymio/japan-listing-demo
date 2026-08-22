#!/usr/bin/env python3
"""Regression tests for v0.3.3 packaging/release integrity."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

MAIN_SKILL = Path(__file__).resolve().parents[1]
REPO_ROOT = MAIN_SKILL.parents[2]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_common():
    path = REPO_ROOT / "scripts" / "package_common.py"
    spec = importlib.util.spec_from_file_location("v033_package_common_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["v033_package_common_test"] = module
    spec.loader.exec_module(module)
    return module


def test_version_and_changelog_are_v033() -> None:
    assert read(REPO_ROOT / "VERSION").strip() == "0.3.3"
    assert "## 0.3.3" in read(REPO_ROOT / "CHANGELOG.md")


def test_release_self_validates_exact_main_sha_before_publish() -> None:
    old = REPO_ROOT / ".github" / "workflows" / "release-v0.3.2.yml"
    workflow = REPO_ROOT / ".github" / "workflows" / "release-validated.yml"
    assert not old.exists(), "fixed v0.3.2 push release workflow must be removed"
    assert workflow.is_file()
    text = read(workflow)
    folded = text.casefold()
    for phrase in [
        "push:",
        "branches: [main]",
        "github.sha",
        "persist-credentials: false",
        "contents: read",
        "contents: write",
        "Pillow",
        "playwright install --with-deps chromium",
        "selftest_fail_closed_v033.py",
        "selftest_demo_runtime_v033.py",
        "selftest_image_decode_v033.py",
        "validate_overlay.py",
        "package_skill.py",
        "package_codex_bundle.py",
        "gh release create",
    ]:
        assert phrase.casefold() in folded, phrase
    build_block = folded.split("\n  publish:", 1)[0]
    assert "contents: write" not in build_block, "validation/build job must not receive contents write"
    publish_block = folded.split("\n  publish:", 1)[1]
    assert "contents: write" in publish_block
    assert "current_main" in folded and "validated_sha" in folded
    assert "test \"$current_main\" = \"$validated_sha\"" in folded


def test_release_checksums_use_download_local_basenames() -> None:
    text = read(REPO_ROOT / ".github" / "workflows" / "release-validated.yml")
    start = text.index("- name: Create download-local checksums and release metadata")
    end = text.index("- uses: actions/upload-artifact@v4", start)
    block = text[start:end]
    assert "(cd dist && sha256sum" in block
    assert "japan-listing-demo.skill.zip" in block
    assert "japan-listing-demo-codex-bundle.zip" in block
    assert "dist/japan-listing-demo.skill.zip" not in block
    assert "dist/japan-listing-demo-codex-bundle.zip" not in block
    assert "> SHA256SUMS.txt" in block


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
        "docs/release-notes-v0.3.3.md", ".github/workflows/validate-japan-listing-demo.yml",
        ".github/workflows/release-validated.yml",
    ]:
        assert metadata in codex


def test_symlink_to_external_file_is_actually_rejected() -> None:
    common = load_common()
    with TemporaryDirectory() as directory:
        root = Path(directory) / "root"
        root.mkdir()
        outside = Path(directory) / "outside-secret.txt"
        outside.write_text("must never enter a package", encoding="utf-8")
        link = root / "leak.txt"
        link.symlink_to(outside)
        try:
            common.reject_symlinks(root)
        except ValueError as exc:
            assert "symlink" in str(exc).casefold(), exc
        else:
            raise AssertionError("external symlink must be rejected before packaging")


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


def test_manifest_declares_hard_verification_runtime_dependencies() -> None:
    manifest = read(MAIN_SKILL / "core" / "manifest.yaml")
    folded = manifest.casefold()
    assert "runtime_dependency: none" not in folded
    for phrase in ["runtime_dependencies:", "Pillow", "playwright", "chromium", "UNVERIFIED/BLOCKED"]:
        assert phrase.casefold() in folded, phrase


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
