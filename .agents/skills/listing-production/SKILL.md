---
name: listing-production
description: Use when producing Stage 7.5–8 listing assets from an approved Production Handoff and one-job Asset Packets.
---

# Listing Production

## Core question

Produce the approved artifacts.

## Plane boundary

This Skill owns Stage 7.5–8 only. It consumes the formal Production Handoff and Creative Strategy Kernel. It does not reinterpret Planning and does not perform final physical-file hardening.

## Inputs

Production may use only:

- Production Handoff;
- Creative Strategy Kernel;
- one current Asset Packet;
- referenced source assets;
- approved visual benchmarks/patterns.

Do not traverse the full project history to rebuild planning decisions during ordinary production.

## Artifact-first mode

Once production starts, the default response is the requested final artifact followed by a concise creative status. Do not substitute a workflow diagram, asset map, production plan, status board, or project-management infographic for the requested final asset.

## Creative status

`PLANNED` / `READY` / `REVIEW` / `REVISE` / `USER_APPROVED` / `BLOCKED`

**Creative Approval ≠ Evidence Verification.** `USER_APPROVED` means the creative/marketing output was accepted; it does not mean the file is physically verified or delivery-safe.

## One-job rule

Execute one Asset Packet at a time. One Asset Packet means one Asset ID, one channel role, one primary shopper task/message, and one final output quantity of 1.

Gallery and enhanced-content assets remain separate production jobs even when they communicate the same topic, unless Planning explicitly authorized reuse/derivative intent.

Batch production may begin only after the user approves the visual direction and explicitly asks to continue in that style. **Same art direction ≠ same composition.** Batch continuation preserves brand language, not the previous asset's layout.

## Minimal set context

The v0.3.2 Asset Packet may carry only:

- the current asset's Page Visual System direction;
- the nearest same-region neighbor summaries;
- the current asset's Evidence Mode.

This is enough context to avoid visual convergence without reopening the full Planning corpus.

## Evidence Mode

Use the Planning-assigned mode for each final asset:

- `SOURCE_FAITHFUL` — faithful product/pack/offer identity is intrinsic; missing required identity source may block production;
- `CREATIVE_MOCK` — lifestyle/atmosphere/spatial creative work may proceed with reduced evidence entitlement when commercially credible; generated details are not Product Truth;
- `PROOF_VISUAL` — factual visual proof requires authoritative source evidence and is blocked when that source is missing.

`source insufficiency != automatic creative rework`.

## Candidate identity and Selection Lock

Every generated alternative for one Asset ID is a distinct candidate such as `A05-01-v1`, `A05-01-v2`.

When the user selects an exact candidate:

1. mark that candidate `USER_SELECTED`;
2. store it as `selected_candidate_id` and its exact `current_output_ref`;
3. set the asset creative status to `USER_APPROVED`;
4. default immediately to the next required asset.

A selected candidate is a creative-state lock. Do **not** silently replace `current_output_ref` or generate another candidate for that Asset ID merely because production continues.

A new candidate after approval requires explicit reopen intent such as “重做”, “修改这张”, “换一个版本”, or equivalent. Reopening preserves prior candidate history; a later selection may supersede the old candidate but must not erase it.

This Selection Lock does not replace later exact-file SHA/provenance verification in Hardening.

## Set-level Creative QA

Asset-level quality does not guarantee page-level quality. Use the structured set QA in `references/production-qa.md` and `scripts/set_level_qa.py` to check scene/composition/tone/scale/proof/message rhythm during production and before Freeze.

This is a creative review layer, not a new formal Stage or Hardening gate.

## Scope Delta

When the authoritative required asset set changes, do not silently keep the old count. Apply an explicit scope revision/delta, then recompute progress and Production Freeze from the current `asset_set`.

Removing or changing one asset does not reopen unrelated `USER_APPROVED` assets. Added or changed assets must remain complete production objects with their role/message/evidence decisions intact.

## Smallest Sufficient Cleanup

Classify the observed issue before rework:

`SINGLE_ASSET_DEFECT` / `SET_REPETITION` / `WRONG_MESSAGE_ROLE` / `EVIDENCE_LIMITATION` / `CLAIM_ERROR` / `PRODUCT_DISTORTION`.

Default behavior is the **Smallest Sufficient Intervention**:

- set repetition: preserve approved assets first and reopen the smallest non-approved subset;
- all affected assets already approved: require explicit user choice before reopening one;
- `CREATIVE_MOCK` + evidence limitation: preserve the creative asset and carry the evidence limitation forward;
- intrinsic single-asset/claim/role/product defects: reopen only the explicitly affected asset(s).

Do not turn one set-level problem into broad regeneration by default.

## Context firewall

Build the generation/editing context from the current Asset Packet and referenced sources only. Do not inject Project State, auditor, gate, parity, or stage-status narration into production prompts.

## Missing upstream input

If the current asset lacks a required fact, business decision, or source required by its Evidence Mode, return a structured `BLOCKED` result and identify the missing field. Do not invent or silently rewrite Planning.

## Completion

Stage 8 completion is measured against the complete required `asset_set` in Production Handoff. Priority proof coverage does not make a partial batch complete.

Before Production Freeze, the complete current set must also pass the lightweight set-level Creative QA defined in `references/production-qa.md`; this is creative guidance, not a new Hardening gate.
