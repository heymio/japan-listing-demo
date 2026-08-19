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
- Planned deliverables and completed deliverables are compared explicitly.
- A completed subset does not make the stage complete.
- A Transition Command may lock a `PARTIAL` stage but does not relabel it `COMPLETE`.
- Final completion does not hide missing or blocked planned work unless the user explicitly approved a reduced scope.

## Asset Readiness and Binding QA

- Stage 1 includes an **Asset Readiness Preflight** for asset classes expected later.
- Approved assets have stable Asset IDs, canonical source, dimensions/aspect, page/offer scope, allowed slots, derivative provenance, and transform rules.
- Approved assets are not silently replaced downstream.
- Material crop/recomposition/role changes create a derivative with a new Asset ID and status.
- An **Asset-to-Slot Contract** exists for planned channel slots/modules.
- `ASSET_SLOT_GATE` passes before final adaptation and Demo Assembly.
- Assets do not leak across page/offer/slot classes simply because they visually fit.

## Channel QA

- Editable slots and module families are verified for the current account or retailer.
- Module counts, fields, image rules, and interactions match current channel documentation.
- Platform-generated areas are not designed as brand-controlled content.
- Comparisons match real offer or product relationships.
- Platform Capability evidence is distinct from Frontend Visual evidence when a channel-native demo is requested.
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE` are evaluated separately.
- A complete message list is not treated as proof of native module suitability.
- Interactive native modules are planned before production rather than fabricated from static boards during Demo Assembly.

## Frontend Fidelity QA

For any deliverable intended to resemble a real consumer-facing channel page:

- a current Primary Reference is identified;
- the user was asked whether they had a preferred reference before native demo assembly;
- current consumer-facing visual evidence supports the material shell and section order;
- desktop structure is verified;
- mobile/app-web structure is verified or explicitly scoped out;
- brand-controlled and platform/retailer-controlled regions are separated;
- project content maps only to verified regions;
- Review Mode overlays do not change the Consumer Mode shell;
- internal IA/module/status labels are absent from Consumer Mode page chrome;
- `FRONTEND_FIDELITY_GATE` passes before the result is named a channel-native PDP/demo.

If fidelity evidence is insufficient, use a clearly named `Content Review Demo` instead of inventing a native shell.

## Market and locale QA

- Market insights have category- and project-specific evidence.
- Locale rules contain language and formatting, not personas or product priorities.
- Region overlays do not replace country and locale research.
- Consumer copy is native and channel-appropriate.
- Search language is researched for the selected category, locale, and channel.
- Regulations and legal copy are verified from current authoritative sources.

## Visual Evidence QA

For every module or tab:

1. Main copy contains one primary promise.
2. Visual subject is the object or scenario named by the copy.
3. Evidence object proves the mechanism or benefit.
4. Asset source is approved or explicitly provisional.

## Differentiator Proof QA

- Every visualizable P0 differentiator has a Differentiator Proof Matrix entry.
- Strongest evidence is classified `DIRECT`, `INDIRECT`, `WEAK`, or `NONE`.
- `DIFFERENTIATOR_PROOF_GATE` passes only when priority differentiators have direct proof or an explicitly user-approved alternative proof strategy.
- Generic attractive lifestyle imagery does not pass this gate by itself.

## Planned-to-Implemented Parity QA

Before a demo is called complete:

- `DELIVERY_PARITY_GATE` compares planned vs implemented slot/module;
- planned interaction matches actual interaction;
- source Asset IDs match locked assignments;
- dimensions/aspect/crop rules match the contract;
- message coverage remains intact;
- page/offer ownership remains correct;
- channel region/module mapping remains correct.

A working HTML file is not proof of parity.

## Mobile and Technical QA

- Gallery, tabs, carousel, hotspot, storyboard or video, comparison, Q&A, variants, and review mode work on desktop and mobile when those interactions belong to the verified target channel.
- Asset references resolve.
- Standalone HTML has no unintended local dependencies.
- ZIP archives preserve relative paths.
- Console and page errors are zero.
- Copy remains readable without zooming.
- Wide comparisons have a usable mobile behavior.

## Review Mode QA

Review mode shows module type, status, open claim, provisional asset, stage status, asset/slot problems, and internal notes without changing the underlying verified Consumer Mode geometry.

Consumer mode hides internal terms, placeholder commercial data, module labels, claim gates, and review-only explanations while remaining semantically complete.

## Final Delivery QA

A final listing/demo may be called complete only when:

- required Stage Completion Manifests are truthful;
- planned deliverables exist or reduced scope is explicitly approved;
- `ASSET_SLOT_GATE` passes;
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or has an approved alternative;
- `DELIVERY_PARITY_GATE` passes;
- channel-native work satisfies `FRONTEND_FIDELITY_GATE`;
- open items are separated from passed checks.

## Domain leakage QA

- Core workflow files contain no company-specific product data.
- Channel profiles contain no category selling points.
- Locale profiles contain no consumer stereotypes.
- Region overlays contain no regional persona.
- Category-specific logic appears only in category overlays, examples, evals, private overlays, or project evidence.
