#!/usr/bin/env python3
"""v0.3.3 standalone Demo tests with behavior-oriented distribution assertions."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parents[2]
LEGACY_PATH = SCRIPT_DIR / "selftest_demo_output_legacy.py"

spec = importlib.util.spec_from_file_location("listing_demo_output_selftest_legacy", LEGACY_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load legacy Demo tests: {LEGACY_PATH}")
legacy = importlib.util.module_from_spec(spec)
sys.modules["listing_demo_output_selftest_legacy"] = legacy
spec.loader.exec_module(legacy)

MIGRATED = {"test_distribution_requires_demo_validator_and_reference"}


def test_distribution_requires_demo_validator_and_reference() -> None:
    package_text = (REPO_ROOT / ".agents" / "skills" / "japan-listing-demo" / "scripts" / "package_skill.py").read_text(encoding="utf-8")
    overlay_text = (REPO_ROOT / ".agents" / "skills" / "japan-listing-demo" / "scripts" / "validate_overlay.py").read_text(encoding="utf-8")
    for path in [
        SKILL_DIR / "references" / "demo-output.md",
        SCRIPT_DIR / "validate_demo_html.py",
        SCRIPT_DIR / "validate_demo_runtime.py",
    ]:
        assert path.is_file(), path
    for phrase in ["collect_files", "internal-skills", "validate_install.py", "write_deterministic_zip"]:
        assert phrase in package_text, phrase
    for filename in ["demo-output.md", "validate_demo_html.py", "selftest_demo_output.py"]:
        assert filename in overlay_text, ("overlay", filename)


def main() -> int:
    tests = []
    for name, value in vars(legacy).items():
        if name.startswith("test_") and callable(value) and name not in MIGRATED:
            tests.append((name, value))
    for name, value in globals().items():
        if name.startswith("test_") and callable(value):
            tests.append((name, value))
    for name, test in sorted(tests):
        test()
    print(f"PASS: {len(tests)} standalone-demo-output tests (v0.3.3)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
