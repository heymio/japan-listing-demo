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


def _validate_asset_objects(items: object, label: str) -> list[dict]:
    if not isinstance(items, list):
        raise ValueError(f"{label} must be a list")
    result: list[dict] = []
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"{label}[{index}] must be a complete asset mapping")
        asset_id = _require_non_empty_string(item.get("asset_id"), f"{label}[{index}].asset_id")
        if asset_id in seen:
            raise ValueError(f"duplicate {label} asset_id: {asset_id}")
        seen.add(asset_id)
        result.append(item)
    return result


def apply_scope_delta(handoff: dict, delta: dict) -> dict:
    """Return a new authoritative handoff after an explicit production-scope revision.

    `added` and `changed` contain complete asset mappings so downstream role,
    slot, message and evidence-mode information cannot disappear. The stored
    scope_delta remains concise and records only affected Asset IDs.
    """
    if not isinstance(handoff, dict):
        raise ValueError("handoff must be a mapping")
    if not isinstance(delta, dict):
        raise ValueError("delta must be a mapping")

    current_assets = handoff.get("asset_set")
    if not isinstance(current_assets, list):
        raise ValueError("handoff.asset_set must be a list")
    current_by_id: dict[str, dict] = {}
    current_order: list[str] = []
    for index, item in enumerate(current_assets):
        if not isinstance(item, dict):
            raise ValueError(f"handoff.asset_set[{index}] must be a mapping")
        asset_id = _require_non_empty_string(item.get("asset_id"), f"handoff.asset_set[{index}].asset_id")
        if asset_id in current_by_id:
            raise ValueError(f"duplicate current asset_id: {asset_id}")
        current_by_id[asset_id] = item
        current_order.append(asset_id)

    removed = delta.get("removed", [])
    if not isinstance(removed, list) or any(not isinstance(value, str) or not value for value in removed):
        raise ValueError("delta.removed must be a list of Asset IDs")
    if len(set(removed)) != len(removed):
        raise ValueError("delta.removed contains duplicate Asset IDs")
    unknown_removed = [asset_id for asset_id in removed if asset_id not in current_by_id]
    if unknown_removed:
        raise ValueError("unknown removed Asset IDs: " + ", ".join(unknown_removed))

    added = _validate_asset_objects(delta.get("added", []), "delta.added")
    changed = _validate_asset_objects(delta.get("changed", []), "delta.changed")

    reason = delta.get("reason")
    if not isinstance(reason, list) or not reason or any(not isinstance(value, str) or not value.strip() for value in reason):
        raise ValueError("delta.reason must be a non-empty list of strings")

    added_ids = [item["asset_id"] for item in added]
    changed_ids = [item["asset_id"] for item in changed]
    if any(asset_id in current_by_id and asset_id not in removed for asset_id in added_ids):
        raise ValueError("delta.added cannot duplicate an existing current Asset ID")
    unknown_changed = [asset_id for asset_id in changed_ids if asset_id not in current_by_id or asset_id in removed]
    if unknown_changed:
        raise ValueError("delta.changed references unknown/removed Asset IDs: " + ", ".join(unknown_changed))
    if set(added_ids) & set(changed_ids):
        raise ValueError("an Asset ID cannot be both added and changed")

    result = _copy(handoff)
    remove_set = set(removed)
    changed_by_id = {item["asset_id"]: item for item in changed}
    next_assets: list[dict] = []
    for asset_id in current_order:
        if asset_id in remove_set:
            continue
        next_assets.append(_copy(changed_by_id.get(asset_id, current_by_id[asset_id])))
    next_assets.extend(_copy(item) for item in added)
    result["asset_set"] = next_assets

    previous_revision = result.get("scope_revision", 1)
    if not isinstance(previous_revision, int) or isinstance(previous_revision, bool) or previous_revision < 1:
        previous_revision = 1
    result["scope_revision"] = previous_revision + 1
    result["scope_delta"] = {
        "added": added_ids,
        "removed": list(removed),
        "changed": changed_ids,
        "reason": list(reason),
    }
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
