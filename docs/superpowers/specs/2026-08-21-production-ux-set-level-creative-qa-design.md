# v0.3.2 Production UX & Set-level Creative QA Design

**Status:** Proposed for user review
**Target version:** 0.3.2
**Base:** v0.3.1 / `b664ea345feaa73504d4add4c85cd0e35909b4c5`

## 1. Problem statement

The Light Bars pilot produced a strong final Amazon.co.jp review demo, but the path to that result exposed recurring production-friction that v0.3.1 does not address well.

The key lesson is that the remaining problems are primarily **creative-production system problems**, not validator/governance problems:

1. individually acceptable assets converged into the same visual template across adjacent modules;
2. user-selected candidates were not strongly locked as the current final version;
3. Creative Mock assets were sometimes held to Proof Visual evidence standards;
4. account-level channel capabilities were re-asked as project-level questions;
5. production-scope changes were not explicitly versioned;
6. cleanup could expand into unnecessary rework instead of using the smallest sufficient intervention.

v0.3.2 must improve the first-pass creative path without undoing the v0.3.0 context firewall or adding more Hardening gates.

## 2. Non-goals

v0.3.2 will **not**:

- redesign the Planning → Production → Hardening architecture;
- add a new formal numbered Stage;
- add a new Hardening/validator gate;
- weaken Stage 8.5 evidence verification;
- move final-file provenance or SHA checks into Production;
- hard-code any private brand/account capability into the public repository;
- claim proven Japan-market output quality; Golden Set / Team Pilot remains the outcome-validation track.

## 3. Design principles

1. **Same art direction ≠ same composition.**
2. **Single-asset quality ≠ page/set quality.**
3. **User selection is a state transition, not conversational context.**
4. **Missing source evidence lowers evidence entitlement; it does not automatically force creative rework.**
5. **Account-level capability should be reused until stale/conflicted.**
6. **Cleanup uses the smallest sufficient intervention.**
7. **Production still receives only minimal set context, never the full Planning/Hardening control plane.**

## 4. Change A — Page Visual System in Planning Handoff

Stage 7 remains Stage 7. There is no Stage 7.25 gate.

Before Production begins, Planning must add a lightweight `page_visual_system` to the Production Handoff. It defines deliberate differences across the complete required asset set.

Minimum per-asset fields:

```yaml
page_visual_system:
  asset_directions:
    - asset_id: A05-01
      visual_role: color-mood
      scene_family: dark-living-space
      composition_family: wide-lifestyle
      tone: saturated-dark
      product_scale: medium
      proof_form: lifestyle
```

Supported conceptual fields:

- `visual_role`
- `scene_family`
- `composition_family`
- `tone`
- `product_scale`
- `proof_form`
- optional `neighbor_contrast_note`

The system should be intentionally concise. It is an art-direction matrix, not another project-management manifest.

### Planning rule

Adjacent assets must not accidentally share the same combination of scene, composition, tone, product scale, and proof form unless repetition is intentional and documented.

## 5. Change B — Evidence Mode per Asset

Each required final asset gets one `evidence_mode`:

```text
SOURCE_FAITHFUL
CREATIVE_MOCK
PROOF_VISUAL
```

### SOURCE_FAITHFUL

Use for packshots, product hero, offer/package representation, or other assets whose job depends on faithful product identity.

Expectation:

- geometry, color/material, included objects, packaging, and visible controls must stay source-faithful;
- missing authoritative source may block production when the visual cannot be represented safely.

### CREATIVE_MOCK

Use for lifestyle, atmosphere, spatial use, or concept scenes.

Expectation:

- product cannot be materially distorted or gain contradictory structure;
- generated scene/placement details do not become Product Truth;
- lack of white-background/installation source does not automatically force rework if the product remains commercially credible and the image is not used as proof of those details.

### PROOF_VISUAL

Use for installation structure, dimensions, interfaces, mechanism, compatibility proof, UI, or other factual visual proof.

Expectation:

- must have suitable authoritative source evidence;
- missing proof source is `BLOCKED` rather than creatively invented.

### Core rule

`source insufficiency != automatic creative rework`

Instead:

`source insufficiency -> reduced evidence entitlement or BLOCKED, depending on evidence_mode`

Hardening remains responsible for final evidence safety.

## 6. Change C — Minimal set context in Asset Packet

The one-job rule stays unchanged: one Asset Packet = one Asset ID, one role, one primary shopper task, quantity 1.

The Asset Packet adds only the current asset's page-level direction plus a small neighbor context:

```yaml
set_context:
  page_visual_direction:
    scene_family: daylight-study
    composition_family: medium-product
    tone: bright-neutral
    product_scale: medium
    proof_form: lifestyle
  nearest_neighbors:
    - asset_id: A05-01
      scene_family: dark-living-space
      composition_family: wide-lifestyle
      tone: saturated-dark
```

This is the minimum context required to avoid visual convergence. It must not include Stage history, auditor reports, Project State, parity, or full page research.

## 7. Change D — Two-layer Creative QA

### Asset-level QA

Keep the existing seven dimensions:

1. message clarity;
2. product prominence;
3. visual proof;
4. composition;
5. realism;
6. benchmark/pattern match;
7. channel readiness.

### Set-level QA

Add a separate lightweight check across adjacent/current approved assets:

1. `scene_repetition`
2. `composition_repetition`
3. `tone_brightness_rhythm`
4. `product_scale_repetition`
5. `proof_form_diversity`
6. `message_role_redundancy`

Set-level QA must be behavioral, not keyword-only.

### Check cadence

Production should run set-level QA automatically at natural clusters rather than asking the user after every asset:

- after the first 2–3 assets of a region;
- when Gallery is complete;
- after each logical enhanced-content cluster/module group;
- before Production Freeze as a final contact-sheet/set review.

Set-level QA does not create a new formal gate name. It returns `REVIEW`, `REVISE`, or `CLEAR` as creative guidance.

## 8. Change E — Asset Selection Lock and candidate versions

Creative production must represent candidate identity explicitly.

Example:

```yaml
assets:
  A05-01:
    candidates:
      - candidate_id: A05-01-v1
        output_ref: file:...
        status: REJECTED
      - candidate_id: A05-01-v2
        output_ref: file:...
        status: USER_SELECTED
    selected_candidate_id: A05-01-v2
    status: USER_APPROVED
```

### Lock semantics

Once an exact candidate is `USER_SELECTED` / `USER_APPROVED`:

- default next action is the next required asset;
- the selected candidate remains current;
- generation of another candidate for that Asset ID requires explicit reopen intent such as `重做`, `修改这张`, `换一个版本`, or equivalent;
- reopening preserves candidate history rather than silently replacing the prior choice.

`current_output_ref` may no longer be silently overwritten after user approval.

This is a creative-state lock only. It does not replace later physical SHA/evidence verification.

## 9. Change F — Scope Delta

When the required production set changes after Stage 7, do not silently mutate the list.

Record a concise `scope_revision`:

```yaml
scope_revision: 2
scope_delta:
  added: []
  removed:
    - G08
  changed: []
  reason:
    - offer-clarity message merged into another approved Gallery role
```

Production progress and Production Freeze must always recompute from the current authoritative required asset set.

A scope delta is not a new stage and does not reopen unrelated approved assets.

## 10. Change G — Minimal Cleanup policy

When a production problem is detected, classify it before deciding the repair scope.

Problem classes:

```text
SINGLE_ASSET_DEFECT
SET_REPETITION
WRONG_MESSAGE_ROLE
EVIDENCE_LIMITATION
CLAIM_ERROR
PRODUCT_DISTORTION
```

Apply **Smallest Sufficient Intervention**:

- preserve already-good/user-approved assets;
- reopen only the minimum asset subset needed to restore the page/set;
- an `EVIDENCE_LIMITATION` on a Creative Mock does not automatically trigger visual redesign;
- `SET_REPETITION` should first identify which smallest subset can be changed to restore rhythm.

Targeted Cleanup must never convert a set-level issue into blanket re-generation without explicit reason.

## 11. Change H — Account Capability Profile hook

Channel planning may consume a persistent account-level capability profile when available.

Public contract example:

```yaml
account_capability_profile:
  channel: amazon-jp
  account_scope: brand-account
  capabilities:
    premium_a_plus: true
    brand_story: true
  verified_at: 2026-08-01
  source_ref: team-private-context
```

### Decision order

1. if a capability profile exists, is sufficiently recent, and has no conflicting evidence: reuse it;
2. if missing, stale, or contradicted: ask/verify;
3. never infer account access from competitors.

The public repository contains only the generic hook/schema and behavior. Brand-specific capability values belong in private team context or project input, never in public runtime defaults.

## 12. UX behavior changes

### Transition acknowledgement

When the user says `继续 / 下一步 / OK / 对` and nothing material changed, the normal acknowledgement should be concise (target <= 3 lines) and immediately advance.

Do not re-explain the stage model or gate theory unless:

- a state changed materially;
- the workflow is BLOCKED/PARTIAL;
- the user asks for detail.

### Candidate selection acknowledgement

When the user selects an exact image, acknowledge the selected candidate ID/output and move to the next asset. Do not generate another version of the selected asset unless explicitly reopened.

## 13. Data-flow summary

```text
Stage 7 Planning
  ├─ Complete required asset set
  ├─ Page Visual System
  ├─ Evidence Mode per asset
  └─ Account capability reference when available
        ↓
Production Handoff
        ↓
One-job Asset Packet
  ├─ one shopper task
  ├─ one visual direction
  ├─ evidence mode
  └─ minimal neighbor/set context
        ↓
Generate one candidate
        ↓
Asset-level Creative QA
        ↓
Set-level Creative QA when cadence requires
        ↓
User selects exact candidate
        ↓
Selection Lock
        ↓
Next asset / explicit reopen only
        ↓
Final set/contact-sheet QA
        ↓
Production Freeze
        ↓
Stage 8.5 Hardening unchanged
```

## 14. Files expected to change during implementation

Planning:

- `.agents/skills/listing-planning/SKILL.md`
- `.agents/skills/listing-planning/templates/production-handoff.example.yaml`
- `.agents/skills/listing-planning/references/planning-qa.md`
- `.agents/skills/listing-planning/profiles/channels/amazon-jp.md`
- `.agents/skills/listing-planning/scripts/validate_planning_contracts.py`
- `.agents/skills/listing-planning/scripts/selftest_planning.py`

Production:

- `.agents/skills/listing-production/SKILL.md`
- `.agents/skills/listing-production/templates/asset-packet.example.yaml`
- `.agents/skills/listing-production/templates/asset-ledger.example.yaml`
- `.agents/skills/listing-production/references/production-qa.md`
- `.agents/skills/listing-production/references/visual-production.md`
- `.agents/skills/listing-production/scripts/project_asset_packet.py`
- `.agents/skills/listing-production/scripts/production_state.py`
- `.agents/skills/listing-production/scripts/selftest_production.py`

Router/distribution docs may receive minimal wording/version updates after behavior is proven. Hardening core should not require architecture changes.

## 15. TDD acceptance criteria

Implementation must first add failing regressions for the Light Bars failure classes, then make them green.

Required behavioral regressions:

1. **Visual repetition:** adjacent assets with the same scene/composition/tone/product-scale/proof-form combination are flagged by set-level QA.
2. **Art-direction diversity:** same brand style with materially different composition is allowed.
3. **Selection lock:** a USER_APPROVED selected candidate cannot be silently replaced by `set_creative_status`/new output without explicit reopen.
4. **Candidate history:** reopening creates/preserves a new candidate rather than erasing the selected one.
5. **Evidence mode:** CREATIVE_MOCK with missing proof-grade source can remain creatively usable; PROOF_VISUAL with missing required proof source is BLOCKED.
6. **Scope delta:** removing an asset from the current required set updates production progress/freeze without reopening unaffected assets.
7. **Minimal cleanup:** SET_REPETITION returns the smallest candidate subset to reconsider rather than all assets.
8. **Capability reuse:** valid account capability avoids a repeated project-level access question; stale/conflicting capability requires re-verification.
9. **Context firewall:** Asset Packet projection contains minimal set context but still excludes Stage/Gate/Auditor/Project State controls.
10. **Packaging parity:** repository and compatibility ZIP include the new Production/Planning behavior.

Existing v0.3.1 validator integrity tests must remain green.

## 16. Release boundary

Target release is `v0.3.2 — Production UX & Set-level Creative QA` only after:

- all new RED→GREEN regressions pass;
- all v0.3.1 tests remain green;
- both package modes pass smoke tests;
- Draft PR review is complete;
- explicit user approval is given before merge.

Formal tag/Release remains a separate action after merge, consistent with v0.3.1 release policy.
