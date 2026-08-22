#!/usr/bin/env python3
"""Regression tests for standalone final Demo HTML delivery."""

from __future__ import annotations

import importlib.util
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_DIR / "scripts" / "validate_demo_html.py"


def load_validator():
    assert VALIDATOR.is_file(), "validate_demo_html.py must exist"
    spec = importlib.util.spec_from_file_location("validate_demo_html", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_demo_html() -> str:
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
img { display: block; max-width: 100%; height: auto; }
.demo { width: 100%; max-width: 1200px; margin: 0 auto; }
[data-carousel] { overflow: hidden; width: 100%; }
[data-carousel-slide] { width: 100%; }
@media (max-width: 600px) { .demo { padding: 8px; } }
</style>
</head>
<body>
<main class="demo">
  <section data-carousel>
    <button type="button" data-carousel-prev aria-label="Previous slide">Previous</button>
    <div data-carousel-slide><img alt="Demo one" src="data:image/png;base64,iVBORw0KGgo="></div>
    <div data-carousel-slide hidden><img alt="Demo two" src="data:image/png;base64,iVBORw0KGgo="></div>
    <button type="button" data-carousel-next aria-label="Next slide">Next</button>
  </section>
</main>
<script>
document.querySelectorAll('[data-carousel]').forEach((root) => {
  root.querySelector('[data-carousel-prev]').addEventListener('click', () => {});
  root.querySelector('[data-carousel-next]').addEventListener('click', () => {});
});
</script>
</body>
</html>"""


def test_standalone_embedded_responsive_carousel_demo_passes() -> None:
    validator = load_validator()
    result = validator.validate_html_text(valid_demo_html())
    assert result["status"] == "PASS", result
    assert result["errors"] == []


def test_external_asset_dependencies_fail() -> None:
    validator = load_validator()
    html = valid_demo_html().replace(
        'src="data:image/png;base64,iVBORw0KGgo="', 'src="assets/hero.png"', 1
    ).replace("<script>", '<script src="assets/app.js">', 1)
    result = validator.validate_html_text(html)
    assert result["status"] == "FAIL"
    folded = "\n".join(result["errors"]).casefold()
    assert "image" in folded and "embedded" in folded
    assert "script" in folded and "inline" in folded


def test_carousel_requires_controls_slides_and_inline_wiring() -> None:
    validator = load_validator()
    html = valid_demo_html().replace("addEventListener('click'", "noop('click'")
    result = validator.validate_html_text(html)
    assert result["status"] == "FAIL"
    assert any("carousel" in message.casefold() for message in result["errors"])


def test_mobile_contract_requires_viewport_and_responsive_css() -> None:
    validator = load_validator()
    html = valid_demo_html().replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1">', ""
    ).replace("@media (max-width: 600px)", ".mobile-placeholder")
    result = validator.validate_html_text(html)
    assert result["status"] == "FAIL"
    folded = "\n".join(result["errors"]).casefold()
    assert "viewport" in folded
    assert "responsive" in folded or "@media" in folded


def test_non_html_delivery_path_fails() -> None:
    validator = load_validator()
    result = validator.validate_delivery_path(Path("demo.zip"))
    assert result["status"] == "FAIL"
    assert any(".html" in message.casefold() for message in result["errors"])


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} standalone-demo-output tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
