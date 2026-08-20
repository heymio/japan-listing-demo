#!/usr/bin/env python3
"""Creative-production state helpers for Asset Ledger and Production Freeze."""

from __future__ import annotations

import json

ALLOWED_STATUSES = {"PLANNED", "READY", "REVIEW", "REVISE", "USER_APPROVED", "BLOCKED"}


def _copy(value: dict) -> dict:
    return json.loads(json.dumps(value))


def _required_ids(handoff: dict) -> list[str]:
    result: list[str] = []
    for item in handoff.get("asset_set", []):
        asset_id = item.get("asset_id") if isinstance(item, dict) else None
        if isinstance(asset_id, str) and asset_id:
            result.append(asset_id)
    return result


def set_creative_status(
    ledger: dict,
    asset_id: str,
    status: str,
    output_ref: str | None = None,
    approval_ref: str | None = None,
) -> dict:
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"invalid creative status: {status}")
    if not isinstance(asset_id, str) or not asset_id:
        raise ValueError("asset_id must be a non-empty string")
    result = _copy(ledger)
    row = result.setdefault("assets", {}).setdefault(asset_id, {})
    row["status"] = status
    if output_ref is not None:
        row["current_output_ref"] = output_ref
    if approval_ref is not None:
        row["approval_ref"] = approval_ref
    return result


def production_progress(handoff: dict, ledger: dict) -> dict:
    required = _required_ids(handoff)
    rows = ledger.get("assets", {})
    approved = sum(1 for asset_id in required if rows.get(asset_id, {}).get("status") == "USER_APPROVED")
    expected = len(required)
    return {
        "expected": expected,
        "approved": approved,
        "remaining": expected - approved,
        "complete": expected == approved,
    }


def build_production_freeze(handoff: dict, ledger: dict) -> dict:
    required = _required_ids(handoff)
    rows = ledger.get("assets", {})
    approved_assets: list[str] = []
    blocked_assets: list[str] = []
    revision_pending: list[str] = []
    approved_output_refs: list[str] = []

    for asset_id in required:
        row = rows.get(asset_id, {})
        status = row.get("status", "PLANNED")
        if status == "USER_APPROVED":
            approved_assets.append(asset_id)
            output_ref = row.get("current_output_ref")
            if output_ref:
                approved_output_refs.append(output_ref)
        elif status == "BLOCKED":
            blocked_assets.append(asset_id)
        else:
            revision_pending.append(asset_id)

    expected = len(required)
    ready = len(approved_assets) == expected and not blocked_assets and not revision_pending
    return {
        "expected_assets": expected,
        "user_approved_assets": approved_assets,
        "blocked_assets": blocked_assets,
        "revision_pending": revision_pending,
        "approved_output_refs": approved_output_refs,
        "ready_for_hardening": ready,
    }
