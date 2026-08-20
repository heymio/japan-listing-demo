# Listing evidence audit contract

## Audit input

The planner writes `audit-input.json`. It contains assertions, not gate results.

Minimum structure:

```json
{
  "audit_version": "1",
  "project_id": "project-defined",
  "checkpoint": "pre-9",
  "assets": [
    {
      "asset_id": "G03",
      "path": "assets/gallery/g03.png",
      "claimed_role": "gallery-native",
      "page_offer_scope": ["offer-a"],
      "allowed_slots": ["gallery-03"],
      "claimed_parent_asset_id": null,
      "claimed_transform": null,
      "claimed_approval_event_id": "APP-017"
    }
  ],
  "slots": [
    {
      "slot_id": "gallery-03",
      "required_asset_ids": ["G03"]
    }
  ],
  "approval_events": [],
  "prior_locked_assets": [],
  "expected_visual_roles": [
    {"asset_id": "G03", "role": "gallery-native"}
  ]
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

## Physical evidence boundary

The normal reconciliation path takes the audit packet plus the **real project root** and recomputes physical fingerprints internally:

```bash
python .agents/skills/listing-evidence-auditor/scripts/reconcile_evidence.py \
  audit-input.json \
  /absolute/or/relative/project-root \
  --semantic-review semantic-review.json \
  --output evidence-audit.json
```

Do **not** treat a caller-authored `physical-fingerprints.json` as the normal trusted input to reconciliation.

`fingerprint_assets.py` remains available for diagnostics and controlled host integrations:

```bash
python .agents/skills/listing-evidence-auditor/scripts/fingerprint_assets.py \
  audit-input.json \
  /project/root \
  --output physical-fingerprints.json
```

Per physical asset the tool recomputes:

```json
{
  "asset_id": "G03",
  "resolved_path": "/project/assets/gallery/g03.png",
  "exists": true,
  "path_allowed": true,
  "sha256": "...",
  "byte_size": 12345,
  "signature_family": "png",
  "extension_family": "png",
  "width": 2000,
  "height": 2000,
  "errors": []
}
```

Supported final image families are PNG, JPEG, and WebP. Physical verification requires a valid supported signature, matching extension, positive dimensions, positive byte size, and no physical errors. A file named `.png` that contains non-image bytes is invalid.

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

Exact recovery requires:

```json
{
  "asset_id": "G03",
  "sha256": "...",
  "approved_role": "gallery-native",
  "approved_slots": ["gallery-03"]
}
```

Filename equality is irrelevant.

## Semantic review

A separate semantic reviewer writes `semantic-review.json`:

```json
{
  "assets": {
    "G03": {
      "asset_id": "G03",
      "review_source": "independent_context",
      "actual_role": "gallery-native",
      "role_status": "ROLE_MATCH",
      "notes": "No enhanced-content board layout or repurposed copy detected."
    }
  }
}
```

`review_source` is one of:

- `independent_context`;
- `human`;
- `same_agent_inline`.

A `same_agent_inline` source cannot produce final semantic verification. It is downgraded to `ROLE_AMBIGUOUS` / `HUMAN_REVIEW_REQUIRED` for effective-state purposes.

The standalone reconciler CLI intentionally does **not** expose `--independent-semantic`. A command-line flag cannot prove that the review actually came from an isolated model context. The CLI therefore treats `independent_context` labels conservatively unless a human resolves the review. A host runtime that genuinely controls an isolated context may call the real-file reconciliation API with `independent_semantic=True` programmatically.

Role statuses:

- `ROLE_MATCH`;
- `ROLE_MISMATCH`;
- `ROLE_AMBIGUOUS`;
- `NOT_VISUALLY_AUDITED`.

## Provenance statuses

- `ORIGINAL_VERIFIED` — physical source exists and no conflicting derivative/recovery claim exists.
- `DERIVATIVE_VERIFIED` — parent physical evidence exists and the derivative is explicitly authorized.
- `EXACT_RECOVERY_VERIFIED` — current physical SHA-256, role, and slot scope exactly match prior locked evidence.
- `PROVENANCE_CONFLICT` — physical/historical evidence contradicts the claim.
- `PROVENANCE_UNKNOWN` — evidence is incomplete.

Deterministic transforms remain transforms. Repeatability does not equal approval.

## Effective statuses

- `VERIFIED` — final-consumable, independently audited.
- `HUMAN_APPROVED` — final-consumable, human resolved exact hash + role/scope.
- `PHYSICALLY_VERIFIED_ONLY` — not final-consumable.
- `INVALIDATED` — not usable.
- `UNVERIFIED` — not final-consumable.
- `HUMAN_REVIEW_REQUIRED` — not final-consumable until human resolution.

## Evidence audit output

`reconcile_evidence.py` writes `evidence-audit.json` into a separate evidence namespace. It does not rewrite Candidate State.

Example:

```json
{
  "audit_version": "1",
  "project_id": "project-defined",
  "checkpoint": "pre-9",
  "assets": {
    "G03": {
      "asset_id": "G03",
      "physical_sha256": "...",
      "physical_identity_ok": true,
      "provenance": "ORIGINAL_VERIFIED",
      "approval_match": true,
      "semantic_role_status": "ROLE_MATCH",
      "actual_role": "gallery-native",
      "review_source": "human",
      "effective_status": "HUMAN_APPROVED",
      "allowed_slots": ["gallery-03"]
    }
  },
  "asset_set_gate": {
    "status": "PASS",
    "messages": []
  }
}
```

## Effective state precedence

For asset eligibility:

```text
Auditor Evidence State
> Candidate/Planner Asset Status
```

A planner-authored `LOCKED` value cannot override `INVALIDATED`, `UNVERIFIED`, or `HUMAN_REVIEW_REQUIRED`.

## Checkpoint semantics

### Targeted post-6.5

`EVIDENCE_RECONCILIATION_GATE` may allow planning with explicit gaps, but Stage 7 cannot final-lock an Asset-to-Slot Contract using inherited assets that are not `VERIFIED` or `HUMAN_APPROVED`.

### Pre-9

`PRE_DEMO_ASSET_GATE` passes only when every required asset in the locked Demo plan is `VERIFIED` or `HUMAN_APPROVED`, and the required asset set is complete.
