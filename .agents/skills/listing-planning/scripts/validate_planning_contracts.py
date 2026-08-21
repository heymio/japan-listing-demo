#!/usr/bin/env python3
"""Strict structural validation for planning handoff artifacts.

The public distribution intentionally avoids a YAML runtime dependency. These
machine contracts therefore accept a small, explicit YAML profile: 2-space
indentation, mappings, lists, quoted/unquoted scalars, and inline []/{} values.
Anything outside that profile is rejected instead of being guessed.
"""

from __future__ import annotations

import argparse
import ast
import re
from pathlib import Path
from typing import Any

FORBIDDEN_HANDOFF = {
    "project_state_manifest",
    "auditor_evidence",
    "declared_gate_results",
    "change_impact_map",
    "delivery_parity_gate",
    "pre_demo_asset_gate",
}

_KEY_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


class ContractParseError(ValueError):
    pass


def _tokenize(text: str) -> list[tuple[int, str, int]]:
    tokens: list[tuple[int, str, int]] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw:
            raise ContractParseError(f"line {lineno}: tabs are not allowed")
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise ContractParseError(f"line {lineno}: indentation must use multiples of 2 spaces")
        tokens.append((indent, raw[indent:].rstrip(), lineno))
    return tokens


def _split_mapping(content: str, lineno: int) -> tuple[str, str]:
    if ":" not in content:
        raise ContractParseError(f"line {lineno}: expected mapping entry")
    key, rest = content.split(":", 1)
    key = key.strip()
    if not key or not _KEY_RE.match(key):
        raise ContractParseError(f"line {lineno}: invalid mapping key {key!r}")
    return key, rest.strip()


def _parse_scalar(value: str, lineno: int) -> Any:
    if value == "[]":
        return []
    if value == "{}":
        return {}
    lowered = value.casefold()
    if lowered in {"null", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith(("'", '"')):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ContractParseError(f"line {lineno}: invalid quoted scalar") from exc
        if not isinstance(parsed, str):
            raise ContractParseError(f"line {lineno}: quoted scalar must be a string")
        return parsed
    if re.fullmatch(r"[-+]?\d+", value):
        return int(value)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)", value):
        return float(value)
    if value.startswith("[") or value.startswith("{"):
        raise ContractParseError(f"line {lineno}: only empty inline []/{{}} containers are supported")
    return value


def _parse_mapping(tokens: list[tuple[int, str, int]], index: int, indent: int) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    while index < len(tokens):
        current_indent, content, lineno = tokens[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ContractParseError(f"line {lineno}: unexpected indentation")
        if content == "-" or content.startswith("- "):
            break
        key, rest = _split_mapping(content, lineno)
        if key in result:
            raise ContractParseError(f"line {lineno}: duplicate key {key!r}")
        index += 1
        if rest:
            result[key] = _parse_scalar(rest, lineno)
            if index < len(tokens) and tokens[index][0] > indent:
                raise ContractParseError(f"line {tokens[index][2]}: scalar {key!r} cannot own nested content")
            continue
        if index < len(tokens) and tokens[index][0] > indent:
            if tokens[index][0] != indent + 2:
                raise ContractParseError(f"line {tokens[index][2]}: nested block must indent exactly 2 spaces")
            result[key], index = _parse_block(tokens, index, indent + 2)
        else:
            result[key] = None
    return result, index


def _parse_list(tokens: list[tuple[int, str, int]], index: int, indent: int) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(tokens):
        current_indent, content, lineno = tokens[index]
        if current_indent < indent:
            break
        if current_indent > indent:
            raise ContractParseError(f"line {lineno}: unexpected indentation")
        if not (content == "-" or content.startswith("- ")):
            break
        item_text = content[1:].strip()
        index += 1
        if not item_text:
            if index < len(tokens) and tokens[index][0] == indent + 2:
                item, index = _parse_block(tokens, index, indent + 2)
            else:
                item = None
            result.append(item)
            continue

        if ":" in item_text:
            key, rest = _split_mapping(item_text, lineno)
            if not rest:
                raise ContractParseError(
                    f"line {lineno}: list mapping must start with a scalar/inline value in this YAML profile"
                )
            item: dict[str, Any] = {key: _parse_scalar(rest, lineno)}
            if index < len(tokens) and tokens[index][0] > indent:
                if tokens[index][0] != indent + 2:
                    raise ContractParseError(f"line {tokens[index][2]}: list mapping continuation must indent 2 spaces")
                continuation, index = _parse_mapping(tokens, index, indent + 2)
                duplicate = set(item) & set(continuation)
                if duplicate:
                    raise ContractParseError(f"duplicate key in list mapping: {sorted(duplicate)[0]!r}")
                item.update(continuation)
            result.append(item)
            continue

        result.append(_parse_scalar(item_text, lineno))
        if index < len(tokens) and tokens[index][0] > indent:
            raise ContractParseError(f"line {tokens[index][2]}: scalar list item cannot own nested content")
    return result, index


def _parse_block(tokens: list[tuple[int, str, int]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(tokens):
        raise ContractParseError("unexpected end of document")
    current_indent, content, lineno = tokens[index]
    if current_indent != indent:
        raise ContractParseError(f"line {lineno}: unexpected indentation")
    if content == "-" or content.startswith("- "):
        return _parse_list(tokens, index, indent)
    return _parse_mapping(tokens, index, indent)


def parse_contract_yaml(text: str) -> Any:
    tokens = _tokenize(text)
    if not tokens:
        return {}
    if tokens[0][0] != 0:
        raise ContractParseError(f"line {tokens[0][2]}: document must start at indentation 0")
    parsed, index = _parse_block(tokens, 0, 0)
    if index != len(tokens):
        raise ContractParseError(f"line {tokens[index][2]}: could not parse trailing content")
    return parsed


def _parse_root(text: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        parsed = parse_contract_yaml(text)
    except ContractParseError as exc:
        return None, [f"invalid contract YAML: {exc}"]
    if not isinstance(parsed, dict):
        return None, ["document root must be a mapping"]
    return parsed, []


def _require_type(container: dict[str, Any], key: str, expected: type, errors: list[str], path: str = "") -> Any:
    label = f"{path}.{key}" if path else key
    if key not in container:
        errors.append(f"missing required key: {label}")
        return None
    value = container[key]
    if not isinstance(value, expected) or (expected is int and isinstance(value, bool)):
        typename = {dict: "mapping", list: "list", str: "string", int: "integer"}.get(expected, expected.__name__)
        errors.append(f"{label} must be a {typename}")
        return None
    return value


def _unique_ids(items: list[Any], key: str, errors: list[str], path: str) -> set[str]:
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{path}[{index}] must be a mapping")
            continue
        value = item.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"{path}[{index}].{key} must be a non-empty string")
            continue
        if value in seen:
            errors.append(f"duplicate {path} {key}: {value}")
        seen.add(value)
    return seen


def validate_project_brief(text: str) -> list[str]:
    root, errors = _parse_root(text)
    if root is None:
        return errors
    _require_type(root, "project", dict, errors)
    offers = _require_type(root, "offers", list, errors)
    product_truth = _require_type(root, "product_truth", dict, errors)
    claim_boundaries = _require_type(root, "claim_boundaries", dict, errors)
    _require_type(root, "consumer_evidence_sources", list, errors)
    _require_type(root, "channel_reference", dict, errors)
    _require_type(root, "open_business_decisions", list, errors)
    if isinstance(offers, list):
        _unique_ids(offers, "id", errors, "offers")
    if isinstance(product_truth, dict):
        for key in ["confirmed", "conditional", "prohibited"]:
            _require_type(product_truth, key, list, errors, "product_truth")
    if isinstance(claim_boundaries, dict):
        for key in ["consumer_ready", "pending", "prohibited"]:
            _require_type(claim_boundaries, key, list, errors, "claim_boundaries")
    return errors


def validate_creative_strategy(text: str) -> list[str]:
    root, errors = _parse_root(text)
    if root is None:
        return errors
    strategy = _require_type(root, "creative_strategy", dict, errors)
    if not isinstance(strategy, dict):
        return errors
    for key in [
        "target_user", "primary_purchase_reasons", "shopper_barriers", "reasons_to_believe",
        "japan_implications", "proof_principles", "visual_direction", "visual_anti_patterns",
    ]:
        _require_type(strategy, key, list, errors, "creative_strategy")
    for key in ["core_tension", "core_promise"]:
        _require_type(strategy, key, str, errors, "creative_strategy")
    priority = _require_type(strategy, "message_priority", dict, errors, "creative_strategy")
    if isinstance(priority, dict):
        for key in ["p0", "p1", "p2"]:
            _require_type(priority, key, list, errors, "creative_strategy.message_priority")
    return errors


def _find_forbidden(value: Any, path: str = "") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if str(key).casefold() in FORBIDDEN_HANDOFF:
                errors.append(f"forbidden control-plane key in Production Handoff: {child_path}")
            errors.extend(_find_forbidden(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_find_forbidden(child, f"{path}[{index}]"))
    return errors


def validate_production_handoff(text: str) -> list[str]:
    root, errors = _parse_root(text)
    if root is None:
        return errors
    handoff = _require_type(root, "production_handoff", dict, errors)
    if not isinstance(handoff, dict):
        return errors
    project = _require_type(handoff, "project", dict, errors, "production_handoff")
    page_plan = _require_type(handoff, "page_plan", dict, errors, "production_handoff")
    asset_set = _require_type(handoff, "asset_set", list, errors, "production_handoff")
    source_assets = _require_type(handoff, "source_assets", list, errors, "production_handoff")
    for key in ["product_invariants", "global_visual_direction", "visual_benchmark_refs", "prohibited", "blocked_assets"]:
        _require_type(handoff, key, list, errors, "production_handoff")
    _require_type(handoff, "creative_strategy_ref", str, errors, "production_handoff")
    errors.extend(_find_forbidden(handoff))

    asset_ids: set[str] = set()
    if isinstance(asset_set, list):
        asset_ids = _unique_ids(asset_set, "asset_id", errors, "production_handoff.asset_set")
        for index, asset in enumerate(asset_set):
            if not isinstance(asset, dict):
                continue
            for key in ["role", "slot", "primary_message", "status"]:
                _require_type(asset, key, str, errors, f"production_handoff.asset_set[{index}]")
    if isinstance(source_assets, list):
        _unique_ids(source_assets, "source_id", errors, "production_handoff.source_assets")

    planned_ids: set[str] = set()
    if isinstance(page_plan, dict):
        for region in ["gallery", "enhanced_content", "other_required_regions"]:
            values = _require_type(page_plan, region, list, errors, "production_handoff.page_plan")
            if isinstance(values, list):
                for value in values:
                    if not isinstance(value, str) or not value:
                        errors.append(f"production_handoff.page_plan.{region} entries must be non-empty Asset IDs")
                    else:
                        planned_ids.add(value)
    blocked_ids: set[str] = set()
    blocked = handoff.get("blocked_assets")
    if isinstance(blocked, list):
        for item in blocked:
            if isinstance(item, str) and item:
                blocked_ids.add(item)
            elif isinstance(item, dict) and isinstance(item.get("asset_id"), str):
                blocked_ids.add(item["asset_id"])
    missing_assets = sorted(planned_ids - asset_ids - blocked_ids)
    if missing_assets:
        errors.append(f"page_plan references Asset IDs absent from asset_set/blocked_assets: {', '.join(missing_assets)}")
    if isinstance(project, dict):
        for key in ["market", "channel", "locale", "product"]:
            _require_type(project, key, str, errors, "production_handoff.project")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a planning artifact")
    parser.add_argument("kind", choices=["project-brief", "creative-strategy", "production-handoff"])
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    try:
        text = args.path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"FAIL: could not read contract: {exc}")
        return 1
    validators = {
        "project-brief": validate_project_brief,
        "creative-strategy": validate_creative_strategy,
        "production-handoff": validate_production_handoff,
    }
    errors = validators[args.kind](text)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {args.kind} contract is structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
