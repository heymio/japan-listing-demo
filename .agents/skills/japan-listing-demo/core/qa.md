# QA checklist

## Product and offer QA

- All P0/P1 messages are covered.
- Every number has a source and condition.
- Earlier-generation capabilities are not silently inherited.
- Offer and page boundaries match the Page Boundary Matrix.
- No page uses hardware, service, UI, storage, or accessories owned by another offer.
- If authoritative evidence changed after a lock, a Change Impact Map identifies `UNAFFECTED`, `REVIEW`, `INVALIDATED`, and `REOPEN` outputs.

## Claim QA

- `CONFLICT`, `MISSING`, and `PROHIBITED` facts do not enter consumer copy.
- Conditional claims include their conditions.
- Price, availability, release date, certification, testing, performance, AI scope, cloud scope, and subscription terms are locked before release.
- No unsupported absolute, comparative, or superlative claim is used.

## Stage Completion QA

- Every advanced numbered stage has a **Stage Completion Manifest**.
- Planned and completed deliverables are compared explicitly.
- A completed subset does not make the stage complete.
- A Transition Command may lock a `PARTIAL` stage but does not relabel it `COMPLETE`.

## Candidate versus Effective State QA

- Stage 6.5A produces a **Candidate Asset Registry**; candidate `LOCKED`, filename, Asset ID, claimed role, claimed provenance, and agent-authored hash are not treated as effective truth.
- A separate **Auditor Evidence State** exists whenever final real assets are required.
- **Effective State** uses Auditor Evidence State over Candidate Asset Status for downstream asset eligibility.
- Planner state cannot overwrite auditor `INVALIDATED`, `UNVERIFIED`, `PHYSICALLY_VERIFIED_ONLY`, or `HUMAN_REVIEW_REQUIRED` results.

## Physical Evidence QA

- `listing-evidence-auditor` recomputes physical SHA-256 from the real file rather than trusting planner metadata.
- File existence, allowed project-root path, byte size, signature family, extension/signature consistency, and supported image dimensions are recomputed from the file.
- Same filename or Asset ID does not prove exact recovery.
- Exact recovery requires physical SHA-256 plus approved role/scope to match the prior locked evidence.
- Missing or path-escaped files are not silently replaced.

## Approval and Provenance QA

- Human approval for an asset is bound to exact physical SHA-256 + approved role + approved slot/page/offer scope.
- If bytes, role, or scope change, prior approval does not automatically carry over.
- A deterministic crop/recomposition/resize/background replacement/role change remains a derivative and needs transform authorization.
- `APPROVAL_PROVENANCE_GATE` and `TRANSFORM_AUTH_GATE` remain active from v0.2.5.
- Auditor provenance is one of `ORIGINAL_VERIFIED`, `DERIVATIVE_VERIFIED`, `EXACT_RECOVERY_VERIFIED`, `PROVENANCE_CONFLICT`, or `PROVENANCE_UNKNOWN`.

## Independent Semantic Audit QA

- Semantic visual-role review prefers an **independent context** or explicit human review.
- The audit packet does not include the planner's desired result or prior PASS conclusion.
- `same_agent_inline` review cannot create final `ROLE_MATCH` for effective-state purposes.
- When independent semantic review is unavailable and role matters, effective status remains `HUMAN_REVIEW_REQUIRED` / `UNVERIFIED` unless the user explicitly approves the exact hash + role/scope.
- Semantic role mismatch overrides planner claims and invalidates downstream final use.

## Post-6.5 Evidence Reconciliation QA

- `EVIDENCE_RECONCILIATION_GATE` is computed after Stage 6.5 whenever real assets will be final-bound.
- Stage 7 may continue planning with explicit evidence gaps.
- Final Asset-to-Slot locking may use only assets whose Effective State is `VERIFIED` or `HUMAN_APPROVED`.
- Planning continuation is not approval.

## Stage 8.5 Pre-Demo Evidence QA

- Stage 8.5 audits the exact final generated/edited files referenced by the locked plan and slot contract.
- Fresh physical SHA-256 is recomputed after edits/transforms.
- Approval carryover, provenance, semantic role, page/offer/slot scope, and complete required asset set are rechecked.
- `PRE_DEMO_ASSET_GATE` passes only when every required asset is `VERIFIED` or `HUMAN_APPROVED` and the auditor asset-set gate passes.
- One invalidated/unverified required member blocks final Stage 9 asset consumption.

## Asset Readiness and Binding QA

- Stage 1 includes an Asset Readiness Preflight for expected asset classes.
- Approved assets have stable Asset IDs, canonical source, dimensions/aspect, page/offer scope, allowed slots, derivative provenance, and transform rules.
- Approved assets are not silently replaced downstream.
- An Asset-to-Slot Contract exists for planned slots/modules.
- `ASSET_SLOT_GATE` checks exact required Asset IDs and, when auditor evidence exists, final effective status and auditor physical SHA-256.
- Gallery-native and enhanced-content assets do not cross roles merely because they visually fit.

## Executable Gate QA

- A machine-readable **Project State Manifest** exists for work that locks modules/assets or assembles a demo.
- The bundled external validator is used rather than agent-authored PASS prose.
- `declared_gate_results` is ignored.
- If validator/auditor execution is unavailable, applicable gates stay `UNVERIFIED`.
- Packaged channel ceilings cannot be raised by project state.
- `CHANNEL_MODULE_BUDGET_GATE` checks locked module count.
- Stage 7 stores one canonical locked plan hash and Stage 9 consumes that exact hash.
- `MODULE_ORIGIN_GATE` fails on unplanned/missing modules, native-type drift, interaction drift, or plan-hash drift.
- `ASSET_SLOT_GATE` and `DELIVERY_PARITY_GATE` use auditor evidence where applicable.
- `EVIDENCE_RECONCILIATION_GATE` and `PRE_DEMO_ASSET_GATE` are computed, not self-declared.

## Channel QA

- Editable slots and module families are verified for the current account or retailer.
- Module counts, fields, image rules, and interactions match current channel evidence.
- Platform-generated areas are not designed as brand-controlled content.
- Platform Capability evidence is distinct from Frontend Visual evidence.
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE` are evaluated separately.
- Interactive native modules are planned before production rather than fabricated from static boards during Demo Assembly.

## Frontend Fidelity QA

For a deliverable intended to resemble a real consumer-facing channel page:

- a current Primary Reference is identified;
- the user was asked whether they had a preferred reference;
- current visual evidence supports material shell and section order;
- desktop is verified;
- mobile/app-web is verified or explicitly scoped out;
- brand-controlled and platform/retailer-controlled regions are separated;
- Review Mode overlays do not change Consumer Mode shell;
- `FRONTEND_FIDELITY_GATE` passes before channel-native naming.

If fidelity evidence is insufficient, use `Content Review Demo` instead of inventing a native shell.

## Market and locale QA

- Market insights have category- and project-specific evidence.
- Locale rules contain language/formatting, not personas or product priorities.
- Consumer copy is native and channel-appropriate.
- Search language is researched for selected category, locale, and channel.
- Regulations/legal copy use current authoritative sources.

## Visual Evidence QA

For every module/tab:

1. Main copy contains one primary promise.
2. Visual subject is the object/scenario named by copy.
3. Evidence object proves mechanism/benefit.
4. Asset source is approved or explicitly provisional.

## Differentiator Proof QA

- Every visualizable P0 differentiator has a Differentiator Proof Matrix entry.
- Strongest evidence is `DIRECT`, `INDIRECT`, `WEAK`, or `NONE`.
- `DIFFERENTIATOR_PROOF_GATE` passes only with direct proof or an explicitly user-approved alternative proof strategy.

## Mobile and Technical QA

- Gallery, carousel, hotspot, storyboard/video, comparison, Q&A, variants, and review interactions work on desktop/mobile when they belong to the verified target channel.
- Asset references resolve.
- Standalone HTML has no unintended local dependencies.
- Console/page errors are zero.
- Copy remains readable without zooming.

## Review Mode QA

Review Mode shows internal status without changing verified Consumer Mode geometry. Consumer Mode hides internal labels, claim gates, evidence statuses, module IDs, and review-only explanations.

## Final Delivery QA

A final listing/demo may be called complete only when:

- Stage Completion Manifests are truthful;
- planned deliverables exist or reduced scope is explicitly approved;
- required auditor evidence is attached;
- `EVIDENCE_RECONCILIATION_GATE` and `PRE_DEMO_ASSET_GATE` pass when required;
- final required assets are `VERIFIED` or `HUMAN_APPROVED`;
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or has an approved alternative;
- external validator output is attached for applicable executable gates;
- executable/auditor gates are not self-declared or silently `UNVERIFIED`;
- channel-native work satisfies `FRONTEND_FIDELITY_GATE`;
- open items are separated from passed checks.

## Domain leakage QA

- Core workflow files contain no company-specific product data.
- Channel profiles contain no category selling points.
- Locale profiles contain no consumer stereotypes.
- Region overlays contain no regional persona.
- Category-specific logic appears only in category overlays, examples, evals, private overlays, or project evidence.
