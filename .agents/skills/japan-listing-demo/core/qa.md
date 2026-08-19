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

## Asset Readiness and Binding QA

- Stage 1 includes an Asset Readiness Preflight for expected asset classes.
- Approved assets have stable Asset IDs, canonical source, SHA-256, dimensions/aspect, page/offer scope, allowed slots, derivative provenance, and transform rules.
- Approved assets are not silently replaced downstream.
- Material crop/recomposition/role changes create derivatives with new Asset IDs.
- An Asset-to-Slot Contract exists for planned slots/modules.
- Assets do not leak across page/offer/slot classes simply because they visually fit.

## Executable Gate QA

- A machine-readable **Project State Manifest** exists for work that locks modules/assets or assembles a demo.
- The bundled **external validator** is used rather than agent-authored PASS prose.
- `declared_gate_results` is ignored.
- If validator execution is unavailable, applicable gates stay `UNVERIFIED`.
- Packaged channel ceilings cannot be raised by the project manifest.
- `CHANNEL_MODULE_BUDGET_GATE` checks the locked module count against the effective packaged/account limit.
- `APPROVAL_PROVENANCE_GATE` requires a matching user approval hash or exact prior-lock SHA-256 recovery for each `LOCKED` asset.
- Filename similarity or visual resemblance is not exact recovery.
- A deterministic crop is still a transform; locked derivatives require matching transform authorization and `TRANSFORM_AUTH_GATE`.
- Stage 7 stores one canonical locked module-plan hash.
- Stage 9 consumes that exact hash.
- `MODULE_ORIGIN_GATE` fails on unplanned modules, missing planned modules, native-type drift, interaction drift, or plan-hash drift.
- `ASSET_SLOT_GATE` checks exact Asset IDs against the locked slot contract.
- `DELIVERY_PARITY_GATE` is computed from locked plan and implementation state.

## Channel QA

- Editable slots and module families are verified for the current account or retailer.
- Module counts, fields, image rules, and interactions match current channel documentation.
- Platform-generated areas are not designed as brand-controlled content.
- Platform Capability evidence is distinct from Frontend Visual evidence.
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE` are evaluated separately.
- A complete message list is not treated as proof of native module suitability.
- Interactive native modules are planned before production rather than fabricated from static boards during Demo Assembly.

## Frontend Fidelity QA

For a deliverable intended to resemble a real consumer-facing channel page:

- a current Primary Reference is identified;
- the user was asked whether they had a preferred reference;
- current visual evidence supports material shell and section order;
- desktop is verified;
- mobile/app-web is verified or explicitly scoped out;
- brand-controlled and platform/retailer-controlled regions are separated;
- project content maps only to verified regions;
- Review Mode overlays do not change Consumer Mode shell;
- `FRONTEND_FIDELITY_GATE` passes before the result is named a channel-native PDP/demo.

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
- Generic attractive lifestyle imagery does not pass by itself.

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
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or has an approved alternative;
- external validator output is attached for applicable executable gates;
- executable gates are PASS/N/A, not self-declared or silently `UNVERIFIED`;
- channel-native work satisfies `FRONTEND_FIDELITY_GATE`;
- open items are separated from passed checks.

## Domain leakage QA

- Core workflow files contain no company-specific product data.
- Channel profiles contain no category selling points.
- Locale profiles contain no consumer stereotypes.
- Region overlays contain no regional persona.
- Category-specific logic appears only in category overlays, examples, evals, private overlays, or project evidence.
