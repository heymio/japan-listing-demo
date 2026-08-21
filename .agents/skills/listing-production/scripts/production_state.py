#!/usr/bin/env python3
"""Creative-production state helpers for Asset Ledger and Production Freeze."""

from __future__ import annotations

import json

ALLOWED_STATUSES = {"PLANNED", "READY", "REVIEW", "REVISE", "USER_APPROVED", "BLOCKED"}
CANDIDATE_STATUSES = {"REVIEW", "REJECTED", "USER_SELECTED", "SUPERSEDED"}


def _copy(value: dict) -> dict:
    return json.loads(json.dumps(value))


def _require_non_empty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _required_ids(handoff: dict) -> list[str]:
    result: list[str] = []
    for item in handoff.get("asset_set", []):
        asset_id = item.get("asset_id") if isinstance(item, dict) else None
        if isinstance(asset_id, str) and asset_id:
            result.append(asset_id)
    return result


def add_candidate(ledger: dict, asset_id: str, candidate_id: str, output_ref: str) -> dict:
    """Append a review candidate without erasing candidate history."""
    _require_non_empty_string(asset_id, "asset_id")
    _require_non_empty_string(candidate_id, "candidate_id")
    _require_non_empty_string(output_ref, "output_ref")

    result = _copy(ledger)
    row = result.setdefault("assets", {}).setdefault(asset_id, {})
    candidates = row.setdefault("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError("asset candidates must be a list")
    for candidate in candidates:
        if isinstance(candidate, dict) and candidate.get("candidate_id") == candidate_id:
            raise ValueError(f"duplicate candidate_id: {candidate_id}")
    candidates.append({
        "candidate_id": candidate_id,
        "output_ref": output_ref,
        "status": "REVIEW",
    })
    row["status"] = "REVIEW"
    row["latest_candidate_id"] = candidate_id
    return result


def select_candidate(
    ledger: dict,
    asset_id: str,
    candidate_id: str,
    approval_ref: str | None = None,
) -> dict:
    """Lock one exact candidate as the current user-approved creative output."""
    _require_non_empty_string(asset_id, "asset_id")
    _require_non_empty_string(candidate_id, "candidate_id")
    if approval_ref is not None:
        _require_non_empty_string(approval_ref, "approval_ref")

    result = _copy(ledger)
    row = result.setdefault("assets", {}).setdefault(asset_id, {})
    candidates = row.get("candidates", [])
    if not isinstance(candidates, list):
        raise ValueError("asset candidates must be a list")

    selected: dict | None = None
    for candidate in candidates:
        if isinstance(candidate, dict) and candidate.get("candidate_id") == candidate_id:
            selected = candidate
            break
    if selected is None:
        raise ValueError(f"candidate_id not found for {asset_id}: {candidate_id}")

    previous_id = row.get("selected_candidate_id")
    reopened = row.get("reopened") is True
    if isinstance(previous_id, str) and previous_id and previous_id != candidate_id and not reopened:
        raise ValueError("asset must be explicitly reopened before selecting a different candidate")

    if reopened and isinstance(previous_id, str) and previous_id != candidate_id:
        for candidate in candidates:
            if isinstance(candidate, dict) and candidate.get("candidate_id") == previous_id:
                candidate["status"] = "SUPERSEDED"

    selected["status"] = "USER_SELECTED"
    row["selected_candidate_id"] = candidate_id
    row["current_output_ref"] = selected.get("output_ref")
    row["status"] = "USER_APPROVED"
    row["reopened"] = False
    if approval_ref is not None:
        row["approval_ref"] = approval_ref
    return result


def reopen_asset(ledger: dict, asset_id: str, reason: str) -> dict:
    """Reopen a locked creative asset while preserving its selected candidate history."""
    _require_non_empty_string(asset_id, "asset_id")
    _require_non_empty_string(reason, "reason")

    result = _copy(ledger)
    row = result.setdefault("assets", {}).setdefault(asset_id, {})
    if row.get("status") != "USER_APPROVED":
        raise ValueError("only a USER_APPROVED asset can be reopened")
    if not isinstance(row.get("selected_candidate_id"), str) or not row.get("selected_candidate_id"):
        raise ValueError("approved asset has no selected candidate to preserve")
    row["status"] = "REVIEW"
    row["reopened"] = True
    row["reopen_reason"] = reason
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

    selected_candidate_id = row.get("selected_candidate_id")
    locked = row.get("status") == "USER_APPROVED" and isinstance(selected_candidate_id, str) and selected_candidate_id
    if locked and row.get("reopened") is not True and output_ref is not None:
        current = row.get("current_output_ref")
        if current is not None and output_ref != current:
            raise ValueError("asset is locked to a user-selected candidate; reopen before replacing output")

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
