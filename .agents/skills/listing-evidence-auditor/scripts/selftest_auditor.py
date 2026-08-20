#!/usr/bin/env python3
"""RED-first regression tests for listing-evidence-auditor."""

from __future__ import annotations

import hashlib
import importlib
import struct
import sys
import zlib
from pathlib import Path
from tempfile import TemporaryDirectory

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from fingerprint_assets import fingerprint_asset  # noqa: E402
from reconcile_evidence import reconcile_evidence  # noqa: E402

reconcile_module = importlib.import_module("reconcile_evidence")


def make_png(width: int, height: int) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    chunk = b"IHDR" + ihdr_data
    ihdr = struct.pack(">I", len(ihdr_data)) + chunk + struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)
    return signature + ihdr


def packet_for(asset_id: str, path: str) -> dict:
    return {
        "audit_version": "1",
        "project_id": "fixture",
        "checkpoint": "pre-9",
        "assets": [{
            "asset_id": asset_id,
            "path": path,
            "claimed_role": "gallery-native",
            "allowed_slots": ["gallery-03"],
            "claimed_approval_event_id": None,
            "claimed_parent_asset_id": None,
            "claimed_transform": None,
        }],
        "slots": [{"slot_id": "gallery-03", "required_asset_ids": [asset_id]}],
        "approval_events": [],
        "prior_locked_assets": [],
        "expected_visual_roles": [{"asset_id": asset_id, "role": "gallery-native"}],
    }


def fingerprints_for(asset_id: str, sha: str) -> dict:
    return {
        "assets": {
            asset_id: {
                "asset_id": asset_id,
                "exists": True,
                "path_allowed": True,
                "sha256": sha,
                "byte_size": 123,
                "signature_family": "png",
                "extension_family": "png",
                "width": 2000,
                "height": 2000,
                "errors": [],
            }
        }
    }


def semantic_match(asset_id: str, actual_role: str, review_source: str = "independent_context") -> dict:
    status = "ROLE_MATCH" if actual_role == "gallery-native" else "ROLE_MISMATCH"
    return {
        "assets": {
            asset_id: {
                "asset_id": asset_id,
                "review_source": review_source,
                "actual_role": actual_role,
                "role_status": status,
                "notes": "fixture",
            }
        }
    }


def test_png_fingerprint_recomputes_sha_and_dimensions() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        image = root / "asset.png"
        image.write_bytes(make_png(3, 2))
        result = fingerprint_asset(image, root)
        assert result["exists"] is True
        assert result["sha256"] == hashlib.sha256(image.read_bytes()).hexdigest()
        assert result["width"] == 3
        assert result["height"] == 2
        assert result["signature_family"] == "png"
        assert result["path_allowed"] is True


def test_missing_file_is_invalid() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        result = fingerprint_asset(root / "missing.png", root)
        assert result["exists"] is False
        assert "missing file" in result["errors"]


def test_path_escape_is_rejected() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory) / "root"
        root.mkdir()
        outside = Path(directory) / "outside.png"
        outside.write_bytes(make_png(1, 1))
        result = fingerprint_asset(outside, root)
        assert result["path_allowed"] is False


def test_extension_signature_mismatch_is_reported() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        image = root / "asset.jpg"
        image.write_bytes(make_png(1, 1))
        result = fingerprint_asset(image, root)
        assert result["signature_family"] == "png"
        assert result["extension_family"] == "jpeg"
        assert "extension/signature mismatch" in result["errors"]


def test_fake_png_with_non_image_bytes_is_rejected() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        image = root / "asset.png"
        image.write_bytes(b"this is not a png")
        result = fingerprint_asset(image, root)
        assert result["signature_family"] is None
        assert "invalid or unsupported image signature" in result["errors"]


def test_same_name_different_sha_does_not_restore_approval() -> None:
    packet = packet_for("G03", "assets/G03.png")
    packet["prior_locked_assets"] = [{
        "asset_id": "G03",
        "sha256": "a" * 64,
        "approved_role": "gallery-native",
        "approved_slots": ["gallery-03"],
    }]
    result = reconcile_evidence(packet, fingerprints_for("G03", "b" * 64), semantic_match("G03", "gallery-native"), True)
    assert result["assets"]["G03"]["provenance"] != "EXACT_RECOVERY_VERIFIED"
    assert result["assets"]["G03"]["effective_status"] != "VERIFIED"


def test_approval_requires_exact_sha_role_and_scope() -> None:
    packet = packet_for("G03", "assets/G03.png")
    packet["approval_events"] = [{
        "approval_event_id": "APP-1",
        "type": "explicit_user_approval",
        "asset_id": "G03",
        "sha256": "c" * 64,
        "approved_role": "gallery-native",
        "approved_slots": ["gallery-03"],
    }]
    packet["assets"][0]["claimed_approval_event_id"] = "APP-1"
    result = reconcile_evidence(packet, fingerprints_for("G03", "c" * 64), semantic_match("G03", "enhanced-content-board"), True)
    assert result["assets"]["G03"]["approval_match"] is False
    assert result["assets"]["G03"]["effective_status"] == "INVALIDATED"


def test_inline_semantic_review_cannot_self_certify() -> None:
    packet = packet_for("G03", "assets/G03.png")
    result = reconcile_evidence(packet, fingerprints_for("G03", "d" * 64), semantic_match("G03", "gallery-native", "same_agent_inline"), False)
    assert result["assets"]["G03"]["semantic_role_status"] in {"ROLE_AMBIGUOUS", "NOT_VISUALLY_AUDITED"}
    assert result["assets"]["G03"]["effective_status"] in {"HUMAN_REVIEW_REQUIRED", "UNVERIFIED"}


def test_reconciler_has_real_file_entrypoint() -> None:
    assert callable(getattr(reconcile_module, "reconcile_from_files", None))


def test_real_file_entrypoint_rejects_forged_nonexistent_asset() -> None:
    reconcile_from_files = getattr(reconcile_module, "reconcile_from_files", None)
    assert callable(reconcile_from_files)
    packet = packet_for("G03", "assets/G03.png")
    packet["approval_events"] = [{
        "approval_event_id": "APP-1",
        "type": "explicit_user_approval",
        "asset_id": "G03",
        "sha256": "f" * 64,
        "approved_role": "gallery-native",
        "approved_slots": ["gallery-03"],
    }]
    packet["assets"][0]["claimed_approval_event_id"] = "APP-1"
    with TemporaryDirectory() as directory:
        root = Path(directory)
        result = reconcile_from_files(
            packet,
            root,
            semantic_match("G03", "gallery-native"),
            independent_semantic=True,
        )
    assert result["assets"]["G03"]["physical_identity_ok"] is False
    assert result["assets"]["G03"]["effective_status"] == "INVALIDATED"


def test_cli_does_not_accept_external_fingerprint_payload_or_self_asserted_independence() -> None:
    text = (SCRIPT_DIR / "reconcile_evidence.py").read_text(encoding="utf-8")
    assert 'parser.add_argument("fingerprints"' not in text
    assert 'parser.add_argument("project_root"' in text
    assert '--independent-semantic' not in text


def test_required_asset_set_fails_when_one_member_invalidated() -> None:
    packet = packet_for("G1", "assets/G1.png")
    packet["assets"] = []
    packet["slots"] = []
    fingerprints = {"assets": {}}
    semantic = {"assets": {}}
    for asset_id in ["G1", "G2", "G3"]:
        asset = packet_for(asset_id, f"assets/{asset_id}.png")["assets"][0]
        asset["allowed_slots"] = [f"gallery-{asset_id[-1]}"]
        packet["assets"].append(asset)
        packet["slots"].append({"slot_id": f"gallery-{asset_id[-1]}", "required_asset_ids": [asset_id]})
        fingerprints["assets"][asset_id] = fingerprints_for(asset_id, asset_id.lower().encode().hex().ljust(64, "0")[:64])["assets"][asset_id]
        actual_role = "enhanced-content-board" if asset_id == "G3" else "gallery-native"
        semantic["assets"][asset_id] = semantic_match(asset_id, actual_role)["assets"][asset_id]
    result = reconcile_evidence(packet, fingerprints, semantic, True)
    assert result["asset_set_gate"]["status"] == "FAIL"


def test_skill_contract_forbids_trusting_planner_claims() -> None:
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").casefold()
    for phrase in [
        "do not trust filenames",
        "do not trust asset ids",
        "do not trust agent-authored hashes",
        "independent context",
        "human_review_required",
        "must not repair",
    ]:
        assert phrase in skill


def main() -> int:
    tests = [name for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for name in sorted(tests):
        globals()[name]()
    print(f"PASS: {len(tests)} listing-evidence-auditor tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
