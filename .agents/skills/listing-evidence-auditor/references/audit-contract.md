# Listing evidence audit contract

## Audit input

The workflow writes `audit-input.json`. It contains candidate assertions and evidence bindings, not gate results.

Minimum asset structure:

```json
{
  "asset_id": "G03",
  "path": "assets/gallery/g03.png",
  "claimed_role": "gallery-native",
  "page_offer_scope": ["offer-a"],
  "allowed_slots": ["gallery-03"],
  "claimed_parent_asset_id": null,
  "claimed_transform": null,
  "claimed_approval_event_id": "APP-017",
  "evidence_mode": "SOURCE_FAITHFUL"
}
```

`checkpoint` is normally `pre-9`; a targeted inherited-asset audit may use `post-6.5`.

### Identifier uniqueness

The audit packet is rejected before fingerprinting or reconciliation if any of these identities repeat:

- `assets[*].asset_id`;
- `approval_events[*].approval_event_id`;
- `prior_locked_assets[*].asset_id`;
- `slots[*].slot_id`;
- `expected_visual_roles[*].asset_id`.

Duplicate identities are not resolved by “last record wins”. Silent dictionary overwrite is forbidden because it can hide missing files, conflicting approvals, or contradictory role/scope evidence.

## PROOF_VISUAL claim/source binding

A `PROOF_VISUAL` is not merely a file with a proof-like visual role. It must declare exactly what factual content it claims and the authoritative evidence objects supporting those facts.

Required per-asset contract:

```json
{
  "asset_id": "P01",
  "evidence_mode": "PROOF_VISUAL",
  "claim_bindings": [
    {
      "claim_id": "CLAIM-01",
      "fact": "The factual statement shown in the visual",
      "authoritative_source_ids": ["SRC-OFFICIAL-01"]
    }
  ]
}
```

Rules:

- `claim_bindings` is required and non-empty for `PROOF_VISUAL`;
- every binding needs a unique `claim_id`, non-empty `fact`, and one or more authoritative source IDs;
- a visual-role match does not prove the claim is true;
- claim/source bindings are assertions until trusted semantic claim review resolves them.

A missing binding fails the audit packet before the asset can enter hard verification.

## Physical evidence boundary

The normal reconciliation path takes the audit packet plus the **real project root** and recomputes physical fingerprints internally:

```bash
python3 .agents/skills/listing-evidence-auditor/scripts/reconcile_evidence.py \
  audit-input.json \
  /absolute/or/relative/project-root \
  --semantic-review semantic-review.json \
  --output evidence-audit.json
```

Do **not** treat a caller-authored fingerprint JSON as the normal trusted input to reconciliation.

`fingerprint_assets.py` remains available for diagnostics and controlled host integrations:

```bash
python3 .agents/skills/listing-evidence-auditor/scripts/fingerprint_assets.py \
  audit-input.json \
  /project/root \
  --output physical-fingerprints.json
```

Per physical asset the tool recomputes path containment, existence, SHA-256, byte size, extension family, detected image family, dimensions, and structural errors.

Supported final image families are PNG, JPEG, and WebP.

### v0.3.3 structural completeness

A recognizable header is not enough for hard physical verification.

PNG validation additionally requires:

- complete PNG signature;
- first complete 13-byte `IHDR`;
- at least one `IDAT`;
- terminal `IEND`;
- no truncated chunk payload;
- valid chunk CRCs;
- decompressible concatenated IDAT zlib stream;
- no unexplained bytes after IEND.

JPEG requires SOI, valid SOF dimensions and terminal EOI. WebP requires RIFF/WEBP structure, consistent declared RIFF size and valid dimensions.

A truncated 24-byte “PNG-looking” file therefore cannot be final-consumable.

## Approval events

The auditor may verify but cannot create user approval.

```json
{
  "approval_event_id": "APP-017",
  "type": "explicit_user_approval",
  "asset_id": "G03",
  "sha256": "...",
  "approved_role": "gallery-native",
  "approved_slots": ["gallery-03"]
}
```

Approval is invalidated when SHA-256, approved role, or approved slot scope changes.

## Prior locked assets

Exact recovery requires the exact prior SHA-256, approved role and approved slot scope. Filename equality is irrelevant.

## Semantic review

A separate semantic reviewer writes `semantic-review.json`.

For ordinary visual-role verification:

```json
{
  "assets": {
    "G03": {
      "asset_id": "G03",
      "review_source": "independent_context",
      "actual_role": "gallery-native",
      "role_status": "ROLE_MATCH"
    }
  }
}
```

For `PROOF_VISUAL`, the trusted reviewer must also resolve the bound claims:

```json
{
  "assets": {
    "P01": {
      "asset_id": "P01",
      "review_source": "human",
      "actual_role": "proof-visual",
      "role_status": "ROLE_MATCH",
      "claim_status": "CLAIM_MATCH",
      "reviewed_claim_ids": ["CLAIM-01"]
    }
  }
}
```

`review_source` may be:

- `independent_context`;
- `human`;
- `same_agent_inline`.

A `same_agent_inline` source cannot produce final semantic verification. For a `PROOF_VISUAL`, trusted review must cover exactly the bound claim IDs. Missing/untrusted/incomplete claim review downgrades a would-be final status to `HUMAN_REVIEW_REQUIRED`; `CLAIM_MISMATCH` invalidates the asset.

The standalone reconciler CLI intentionally does **not** expose `--independent-semantic`. A command-line flag cannot prove that the review actually came from an isolated model context. A host runtime that genuinely controls an isolated context may call the real-file reconciliation API with `independent_semantic=True` programmatically.

## Provenance statuses

- `ORIGINAL_VERIFIED` — physical source exists and no conflicting derivative/recovery claim exists.
- `DERIVATIVE_VERIFIED` — parent physical evidence exists and the derivative is explicitly authorized.
- `EXACT_RECOVERY_VERIFIED` — current physical SHA-256, role, and slot scope exactly match prior locked evidence.
- `PROVENANCE_CONFLICT` — physical/historical evidence contradicts the claim.
- `PROVENANCE_UNKNOWN` — evidence is incomplete.

Deterministic transforms remain transforms. Repeatability does not equal approval.

## Effective statuses

- `VERIFIED` — final-consumable, independently audited, including required claim review for `PROOF_VISUAL`.
- `HUMAN_APPROVED` — final-consumable, human-resolved exact evidence scope.
- `PHYSICALLY_VERIFIED_ONLY` — not final-consumable.
- `INVALIDATED` — not usable.
- `UNVERIFIED` — not final-consumable.
- `HUMAN_REVIEW_REQUIRED` — not final-consumable until trusted semantic resolution.

## Effective state precedence

For asset eligibility:

```text
Auditor Evidence State
> Candidate/Planner Asset Status
```

A planner-authored `LOCKED` or creative `USER_APPROVED` state cannot override `INVALIDATED`, `UNVERIFIED`, or `HUMAN_REVIEW_REQUIRED`.

## Checkpoint semantics

### Targeted post-6.5

`EVIDENCE_RECONCILIATION_GATE` may allow planning with explicit gaps, but Stage 7 cannot final-lock an inherited Asset-to-Slot binding whose exact evidence remains non-final.

### Pre-9

For Delivery State 0.2, pre-9 audit is mandatory by workflow. `PRE_DEMO_ASSET_GATE` passes only when every required asset in the union-derived final required set is final-consumable under auditor evidence and the auditor asset-set result passes. Caller-authored state cannot disable the gate.
