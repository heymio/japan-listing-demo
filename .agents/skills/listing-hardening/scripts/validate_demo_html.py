#!/usr/bin/env python3
"""Validate a final listing Demo as one standalone responsive HTML file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


RESOURCE_ATTRS = {
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "object": ("data",),
    "source": ("src",),
    "track": ("src",),
    "video": ("src", "poster"),
}


class DemoHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.viewport_contents: list[str] = []
        self.styles: list[str] = []
        self.scripts: list[str] = []
        self._capture_style = False
        self._capture_script = False
        self.images: list[dict[str, str]] = []
        self.srcsets: list[tuple[str, str]] = []
        self.script_srcs: list[str] = []
        self.stylesheet_hrefs: list[str] = []
        self.resource_refs: list[tuple[str, str, str]] = []
        self.carousel_roots = 0
        self.carousel_slides = 0
        self.carousel_prev_buttons = 0
        self.carousel_next_buttons = 0

    @staticmethod
    def _attrs(attrs: Iterable[tuple[str, str | None]]) -> dict[str, str]:
        return {key.casefold(): value or "" for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.casefold()
        values = self._attrs(attrs)

        if tag == "meta" and values.get("name", "").casefold() == "viewport":
            self.viewport_contents.append(values.get("content", ""))

        if tag == "style":
            self._capture_style = True

        if tag == "script":
            self._capture_script = True
            if values.get("src"):
                self.script_srcs.append(values["src"])

        if tag == "link":
            rel_tokens = {token.casefold() for token in values.get("rel", "").split()}
            if "stylesheet" in rel_tokens and values.get("href"):
                self.stylesheet_hrefs.append(values["href"])

        if tag == "img":
            self.images.append(values)

        if tag in {"img", "source"} and values.get("srcset"):
            self.srcsets.append((tag, values["srcset"]))

        for attr in RESOURCE_ATTRS.get(tag, ()):
            value = values.get(attr)
            if value:
                self.resource_refs.append((tag, attr, value))

        if "data-carousel" in values:
            self.carousel_roots += 1
        if "data-carousel-slide" in values:
            self.carousel_slides += 1
        if tag == "button" and "data-carousel-prev" in values:
            self.carousel_prev_buttons += 1
        if tag == "button" and "data-carousel-next" in values:
            self.carousel_next_buttons += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag == "style":
            self._capture_style = False
        elif tag == "script":
            self._capture_script = False

    def handle_data(self, data: str) -> None:
        if self._capture_style:
            self.styles.append(data)
        if self._capture_script:
            self.scripts.append(data)


def _is_embedded_uri(value: str) -> bool:
    folded = value.strip().casefold()
    return folded.startswith("data:") or folded.startswith("blob:")


def _is_embedded_image(value: str) -> bool:
    return value.strip().casefold().startswith("data:image/")


def _srcset_urls(value: str) -> list[str]:
    """Extract candidate URLs while treating the first comma in a data URI as data syntax.

    Image data URIs used by the Demo are expected to be compact (normally
    base64), so a later comma is the candidate separator. Descriptors such as
    `1x`, `2x`, or `640w` are skipped.
    """
    urls: list[str] = []
    index = 0
    length = len(value)
    while index < length:
        while index < length and (value[index].isspace() or value[index] == ","):
            index += 1
        if index >= length:
            break

        start = index
        if value[index:index + 5].casefold() == "data:":
            data_comma = value.find(",", index)
            if data_comma < 0:
                urls.append(value[start:].strip())
                break
            index = data_comma + 1
            while index < length and not value[index].isspace() and value[index] != ",":
                index += 1
            urls.append(value[start:index].strip())
        else:
            while index < length and not value[index].isspace() and value[index] != ",":
                index += 1
            urls.append(value[start:index].strip())

        while index < length and value[index] != ",":
            index += 1
        if index < length and value[index] == ",":
            index += 1
    return [url for url in urls if url]


def _css_urls(style_text: str) -> list[str]:
    return [
        match.group(2).strip()
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", style_text, flags=re.I | re.S)
    ]


def validate_delivery_path(path: Path) -> dict[str, object]:
    errors: list[str] = []
    if path.suffix.casefold() != ".html":
        errors.append("Final Demo delivery must be exactly one .html file; ZIP/package delivery is not accepted.")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


def validate_html_text(text: str) -> dict[str, object]:
    errors: list[str] = []
    parser = DemoHTMLParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:  # pragma: no cover - HTMLParser rarely raises on malformed HTML
        errors.append(f"HTML parsing failed: {exc}")
        return {"status": "FAIL", "errors": errors}

    for image in parser.images:
        src = image.get("src", "").strip()
        if not src:
            errors.append("Every <img> must have an embedded data:image source.")
        elif not _is_embedded_image(src):
            errors.append(f"Image source must be embedded as data:image; external/local image dependency found: {src}")

    for tag, srcset in parser.srcsets:
        candidates = _srcset_urls(srcset)
        if not candidates or any(not _is_embedded_image(candidate) for candidate in candidates):
            errors.append(
                f"<{tag}> srcset must contain only embedded data:image candidates; external/local srcset dependency found."
            )

    if parser.script_srcs:
        errors.append("All JavaScript must be inline; <script src> dependencies are not allowed.")
    if parser.stylesheet_hrefs:
        errors.append("All CSS must be inline; external/local stylesheet dependencies are not allowed.")

    for tag, attr, value in parser.resource_refs:
        if not _is_embedded_uri(value):
            errors.append(
                f"Standalone Demo cannot depend on external/local media: <{tag}> {attr}={value!r} must be embedded."
            )

    style_text = "\n".join(parser.styles)
    if re.search(r"@import\b", style_text, flags=re.I):
        errors.append("All CSS must be inline without @import dependencies.")
    for target in _css_urls(style_text):
        if target and not _is_embedded_uri(target) and not target.startswith("#"):
            errors.append(f"CSS url() dependency must be embedded as data:/blob:; found: {target}")

    viewport_ok = any("width=device-width" in content.replace(" ", "").casefold() for content in parser.viewport_contents)
    if not viewport_ok:
        errors.append("Mobile validation requires a viewport meta tag with width=device-width.")

    responsive_css_ok = bool(re.search(r"@media\s*\([^)]*(?:max-width|min-width)[^)]*\)", style_text, flags=re.I))
    if not responsive_css_ok:
        errors.append("Mobile validation requires responsive CSS with an explicit @media width breakpoint.")

    if parser.images and not re.search(r"max-width\s*:\s*100%", style_text, flags=re.I):
        errors.append("Responsive image contract requires max-width: 100% in inline CSS.")

    carousel_structure_ok = (
        parser.carousel_roots >= 1
        and parser.carousel_slides >= 2
        and parser.carousel_prev_buttons >= 1
        and parser.carousel_next_buttons >= 1
    )
    script_text = "\n".join(parser.scripts)
    carousel_wiring_ok = all(
        token in script_text
        for token in ["data-carousel", "data-carousel-prev", "data-carousel-next", "addEventListener"]
    ) and bool(re.search(r"['\"]click['\"]", script_text))

    if not carousel_structure_ok:
        errors.append(
            "Carousel validation requires a data-carousel root, at least two data-carousel-slide elements, "
            "and button controls for data-carousel-prev/data-carousel-next."
        )
    elif not carousel_wiring_ok:
        errors.append("Carousel controls exist but inline JavaScript wiring for click interaction is not verifiable.")

    return {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": {
            "single_file_dependencies": "PASS" if not any("dependency" in item.casefold() or "inline" in item.casefold() for item in errors) else "FAIL",
            "embedded_images": "PASS" if not any(("image" in item.casefold() or "srcset" in item.casefold()) and "embedded" in item.casefold() for item in errors) else "FAIL",
            "carousel_contract": "PASS" if carousel_structure_ok and carousel_wiring_ok else "FAIL",
            "mobile_contract": "PASS" if viewport_ok and responsive_css_ok else "FAIL",
        },
    }


def validate_file(path: Path) -> dict[str, object]:
    path_result = validate_delivery_path(path)
    if path_result["status"] != "PASS":
        return path_result
    if not path.is_file():
        return {"status": "FAIL", "errors": [f"Demo HTML file not found: {path}"]}
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"status": "FAIL", "errors": ["Demo HTML must be UTF-8 text."]}
    return validate_html_text(text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="final standalone .html Demo")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    result = validate_file(args.html)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['status']}: standalone Demo HTML validation")
        for error in result.get("errors", []):
            print(f"- {error}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
