---
name: listing-evidence-auditor
description: Use when independently reconciling listing assets against physical files, provenance, exact-hash approvals, semantic visual roles, slot scope, and required asset-set completeness.
---

# Listing Evidence Auditor

## Purpose

Audit evidence, not creative intent. This sibling Skill answers one question:

> Are these exact physical artifacts really what the listing workflow says they are?

It does not decide consumer strategy, copy, channel module architecture, or visual creative direction.

## Separation of duties

Prefer an **independent context** from the planner/producer. The audit packet must contain only the evidence needed to verify the assets, not the planner's desired conclusion or prior PASS statements.

If an independent context is unavailable, deterministic physical checks may still run, but semantic visual-role judgments remain `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless a human explicitly approves the exact file hash plus role/scope. Loading this Skill in the same reasoning context does not convert same-agent review into independent review.

## Trust boundary

- **Do not trust filenames** as evidence of identity or prior approval.
- **Do not trust Asset IDs** as evidence that the file is the approved artifact.
- **Do not trust agent-authored hashes**; recompute SHA-256 from the real file.
- Do not trust claimed dimensions, provenance, role, `LOCKED` status, or exact-recovery flags without independent evidence.
- The auditor **must not repair** an asset, crop it, regenerate it, rename it, reassign it, or silently rewrite the candidate registry.
- The auditor cannot create an `explicit_user_approval` event itself.

## Inputs

Read `references/audit-contract.md` and accept an audit packet containing:

- candidate assets and exact paths;
- expected page/offer/slot scope;
- approval events already created by the user-facing workflow;
- prior locked hashes when exact recovery is claimed;
- expected visual role/evidence requirements;
- semantic review results only when they came from `independent_context` or `human` review.

All `claimed_*` fields are assertions to test, not trusted facts.

## Required process

```text
Audit packet
→ fingerprint_assets.py
→ physical-fingerprints.json
→ independent/human semantic review when required
→ reconcile_evidence.py
→ evidence-audit.json
→ verified-asset-registry.json / Effective State
```

### Physical verification

Recompute from the real file system:

- path containment under the allowed project root;
- existence;
- SHA-256;
- byte size;
- file signature family;
- image width/height for supported PNG/JPEG/WebP;
- extension/signature mismatch.

### Provenance verification

Classify:

- `ORIGINAL_VERIFIED`;
- `DERIVATIVE_VERIFIED`;
- `EXACT_RECOVERY_VERIFIED`;
- `PROVENANCE_CONFLICT`;
- `PROVENANCE_UNKNOWN`.

Same filename is never exact recovery unless the physical SHA-256 matches the previously locked SHA-256 and the approved role/scope still match.

A deterministic crop, resize, recomposition, text/background replacement, or role change remains a derivative. Repeatability is not approval.

### Approval binding

User approval binds to exact:

```text
SHA-256
+ approved visual role
+ approved slot/page/offer scope
```

If the bytes, role, or scope change, prior approval does not automatically carry over.

### Semantic visual-role verification

Visually classify the artifact against the expected role, for example:

- gallery-native;
- enhanced-content board;
- product packshot;
- lifestyle scene;
- UI screenshot;
- mechanism diagram;
- comparison visual;
- packaging;
- frontend-reference capture.

Return one of:

- `ROLE_MATCH`;
- `ROLE_MISMATCH`;
- `ROLE_AMBIGUOUS`;
- `NOT_VISUALLY_AUDITED`.

A same-agent inline semantic check cannot final-PASS role. Use `HUMAN_REVIEW_REQUIRED` when the semantic role matters and independent review is unavailable.

### Asset-set verification

Audit the whole required set, not only individual files. Check missing required assets, invalidated members, unexpected members entering a locked set, slot scope, and required ordering/bindings where specified.

## Effective statuses

- `VERIFIED` — physical identity, provenance, approval/scope, and independent semantic-role checks satisfy the checkpoint.
- `HUMAN_APPROVED` — physical identity is verified and human review explicitly approves the exact hash + role/scope.
- `PHYSICALLY_VERIFIED_ONLY` — physical file is known but final evidence assurance is incomplete; not final-consumable.
- `INVALIDATED` — an evidence conflict exists.
- `UNVERIFIED` — evidence is insufficient.
- `HUMAN_REVIEW_REQUIRED` — semantic evidence is material and cannot be independently resolved in the current runtime.

## Output ownership

Write auditor results into a separate evidence namespace. Never overwrite the planner's Candidate State.

When Candidate State conflicts with audited evidence, audited evidence determines downstream asset eligibility.

## Gate semantics

For post-6.5 audit, `EVIDENCE_RECONCILIATION_GATE` may be `PARTIAL` for continued planning, but final Asset-to-Slot locking cannot use non-final-consumable assets.

For pre-demo audit, `PRE_DEMO_ASSET_GATE` passes only when every required asset in the locked Demo plan is `VERIFIED` or `HUMAN_APPROVED` and the required set is complete.
