#!/usr/bin/env python3
"""Validate one-job Asset Packets and project production-only context."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_TOP_LEVEL = {
    "asset_id",
    "role",
    "objective",
    "strategy_context",
    "evidence",
    "product_sources",
    "benchmark",
    "composition",
    "output",
    "must_preserve",
    "must_not_generate",
}

PROJECTION_KEYS = [
    "asset_id",
    "role",
    "objective",
    "strategy_context",
    "evidence",
    "product_sources",
    "benchmark",
    "composition",
    "output",
    "must_preserve",
    "must_not_generate",
]


def validate_asset_packet(packet: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(packet.get("asset_id"), str) or not packet.get("asset_id"):
        errors.append("Asset Packet requires exactly one asset_id string")
    if packet.get("output", {}).get("quantity") != 1:
        errors.append("Asset Packet output quantity must be 1; batch control belongs outside the packet")
    if packet.get("composition", {}).get("one_image_focus") is not True:
        errors.append("one_image_focus must be true")
    missing = sorted(REQUIRED_TOP_LEVEL - set(packet))
    errors.extend(f"missing field: {name}" for name in missing)
    return errors


def project_generation_context(packet: dict) -> dict:
    errors = validate_asset_packet(packet)
    if errors:
        raise ValueError("; ".join(errors))
    return {key: packet[key] for key in PROJECTION_KEYS}


def main() -> int:
    parser = argparse.ArgumentParser(description="Project an Asset Packet into production-only JSON context")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    packet = json.loads(args.input.read_text(encoding="utf-8"))
    projected = project_generation_context(packet)
    encoded = json.dumps(projected, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
