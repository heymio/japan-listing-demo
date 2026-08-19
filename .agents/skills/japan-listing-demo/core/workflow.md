# Workflow reference

## Execution control

**Checkpointed execution by default.** Complete one numbered stage to a reviewable state, present its output and open items, then stop at a **Major Stage Checkpoint** before entering the next numbered stage.

Checkpoints are for numbered workflow stages, not every trivial subtask. Within a stage, complete the planned analysis or reviewable batch without asking for approval after every search, table, tool call, frame, or image.

Read `references/delivery-integrity.md` for Stage Completion Manifest, asset binding, module fit, delivery parity, differentiator proof, and change-control rules.

### Stage Completion Manifest

Every numbered stage ends with a **Stage Completion Manifest** containing planned deliverables, completed items, approved/locked items, `NEEDS REVISION`, missing items, blocked items, open items, and `STAGE_STATUS = COMPLETE | PARTIAL | BLOCKED`.

A completed subset does not make the stage complete. If the user advances a `PARTIAL` stage, lock it as `PARTIAL`; do not relabel it `COMPLETE`.

### Transition Command

Treat `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalent wording as a **Transition Command** unless the user explicitly says to continue improving the current artifact.

On a Transition Command:

- stop current-stage retries and regeneration immediately;
- preserve the best current result;
- mark unresolved issues as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items;
- finalize the current Stage Completion Manifest with its real status;
- lock the current stage snapshot;
- advance to the next numbered stage;
- do not reopen the locked stage unless the user asks to return or new authoritative evidence materially invalidates it.

### Retry Budget

For the same artifact and the same identified problem, allow at most **two autonomous attempts** without new user input or new evidence. After the Retry Budget is exhausted, stop the loop and wait at the current Major Stage Checkpoint with the current best result or a blocked status.

A Transition Command overrides the Retry Budget and advances immediately.

### Change Impact and targeted reopen

A locked stage is stable, not immune to newer authoritative evidence.

When an authoritative fact, approved offer/strategy decision, approved asset/UI source, channel capability/reference, or claim/legal decision materially changes, create a **Change Impact Map**.

Classify dependent outputs as `UNAFFECTED`, `REVIEW`, `INVALIDATED`, or `REOPEN`. Preserve unaffected locked work and rerun only impacted stages/items. Do not ignore new evidence because a stage was locked, and do not restart the whole workflow when dependency analysis shows unaffected work remains valid.

### Autonomous Mode

Full continuous execution is opt-in only. If the user explicitly requests no stage checkpoints for the current task, run non-blocked stages continuously for that task. This does not change the default behavior for later work.

Autonomous Mode does not bypass evidence, delivery-integrity, claim, asset-slot, module-fit, parity, or frontend-fidelity gates.

## Stage 0 — Project Definition

Record:

- market country
- locale
- region overlays
- channel type and site
- product category
- product and offer definitions
- page targets
- output type
- review audience
- account or retailer capabilities

**Gate:** Market, locale, region, channel, category, offer, and page target are not collapsed into one field.

If one field is uncertain, record the uncertainty instead of inventing a value.

**Output:** Project Definition and selected profiles.

**Major Stage Checkpoint:** present the definition, assumptions, blockers, and Stage Completion Manifest. Wait for approval or a Transition Command before Stage 1, unless Autonomous Mode is active.

## Stage 1 — Source Intake + Asset Readiness Preflight

Collect product marketing documents, specifications, project approvals, pricing decisions, research, VOC, competitor pages, earlier-generation references, brand guidance, product renders, UI sources, videos, and any user-supplied channel frontend reference URL / ASIN / store page / retailer page / screenshots.

VOC remains an independent evidence stream. A competitor URL does not make VOC complete.

If the user already supplied a channel reference, preserve it as a candidate Primary Reference for Stage 5.5 rather than treating it only as competitor research.

Create an **Asset Readiness Preflight** for the asset classes the current project is expected to need later. Record required-for, received, source, quality/status, needed-by-stage, and blocking impact. Only include asset classes relevant to the project.

**Output:** Project Input Pack + Asset Readiness Preflight.

**Major Stage Checkpoint:** summarize sources received, missing inputs, asset-readiness risks, source-quality risks, and Stage Completion Manifest. Wait for review before Stage 2 unless Autonomous Mode is active.

## Stage 2 — Source Normalization & Coverage Gate

For every source record product, offer, version, authority, freshness, completeness, allowed usage, and downstream dependencies.

Separate product-fact authority, commercial-decision authority, marketing-decision authority, consumer evidence, localization reference, channel capability reference, channel frontend visual reference, and visual asset reference.

Classify missing information by downstream impact. Carry Asset Readiness Preflight gaps forward rather than rediscovering them late.

**Output:** Source Registry, Missing Coverage, and `SOURCE_GATE`.

**Major Stage Checkpoint:** show what is safe to continue, what is blocked, what remains open, and Stage Completion Manifest. `SOURCE_GATE` is a validation result, not permission to invent missing facts.

## Stage 3 — Fact Lock

Create:

- Fact Ledger
- Conflict Ledger
- Missing Evidence
- Claim Readiness
- Gate Result

For successor products, distinguish `INHERITED-PENDING`, `UPGRADED`, `NEW`, `CONFLICT`, and `MISSING`. An earlier product never proves a new product fact without explicit inheritance evidence.

**Gate:** Consumer copy cannot use `CONFLICT`, `MISSING`, `PROHIBITED`, or an unqualified `CONDITIONAL` fact.

**Major Stage Checkpoint:** present locked facts, conflicts, claim gates, affected page scopes, and Stage Completion Manifest. Wait before Stage 4 unless Autonomous Mode is active.

## Stage 4 — Consumer Strategy

Draft Target User, JTBD, Pain Points, Purchase Barriers, Benefits, Reasons to Believe, Differentiators, and Message Priority from the evidence.

Do not derive needs from the country name alone.

Identify P0 purchase reasons/differentiators that later visuals must prove. Mark whether each is visually provable and what type of evidence would count as direct proof.

**Output:** Draft Consumer Strategy and Reviewable Strategy Snapshot.

**Major Stage Checkpoint:** this is a real review point. Let the user confirm, override, or redirect strategy before market enrichment and message architecture. Include Stage Completion Manifest.

## Stage 4.2 — Market & Localization Enrichment

Research the intersection of:

```text
Product / Category
× Market
× Locale
× Channel
× Current evidence
```

External research may add need states, scenarios, terminology, search language, purchase motivation, objections, and channel conventions. It may not overwrite product facts.

Use current authoritative sources for regulations and platform rules. Separate evidence from inference.

**Output:** Market Evidence Registry and Localization Brief.

**Major Stage Checkpoint:** present validated market evidence, hypotheses, localization implications, and Stage Completion Manifest. Wait for review before Stage 5 unless Autonomous Mode is active.

## Stage 5 — Message Architecture

Define the Core Promise, reasons to buy, trust evidence, objections, and message priority. Build shared product messages once, then fork by offer and page target.

Preserve the P0 differentiator proof requirements from Stage 4 so later visual work cannot reduce them to generic lifestyle context.

**Output:** Message House and Message Priority.

**Major Stage Checkpoint:** user reviews message hierarchy, P0 proof requirements, and Stage Completion Manifest before channel mapping.

## Stage 5.5 — Channel Template & Frontend Mapping

Read `references/channel-native-demo.md` whenever the requested output includes a channel-native PDP/demo.

Stage 5.5 has three distinct evidence tasks. Do not collapse them.

### 5.5A — Platform Capability Research

Load the selected channel profile and verify the actual account, marketplace, retailer, or CMS capabilities.

Confirm, as applicable:

- editable fields and regions;
- brand-controlled versus platform/retailer-controlled ownership;
- module/component families;
- current limits and policies;
- account-specific access;
- publishing workflow;
- mobile/app-web constraints.

**Official platform rules prove capability, not frontend fidelity.** Official rules do not substitute for current consumer-facing visual evidence.

### 5.5B — Frontend Reference Intake

If a channel-native demo is requested, explicitly check whether the user has a preferred current **Reference URL**, ASIN, retailer page, store page, screenshot set, or approved frontend capture.

- If supplied, record it as the candidate **Primary Reference** and inspect it to the extent accessible.
- If none is supplied, research 1–3 current comparable consumer-facing pages and recommend a Primary Reference with reasons.
- Secondary references may fill identified gaps but must not silently replace the Primary Reference.
- If live access is blocked, use the normal Retry Budget, then request screenshots/PDF/capture or use a clearly identified secondary reference. Do not invent the missing shell.

### 5.5C — Frontend Visual Capture

Capture or inspect enough current visual evidence to establish:

- desktop shell anatomy;
- mobile/app-web anatomy where relevant;
- material section order;
- gallery/media behavior;
- offer/variation behavior when relevant;
- brand-controlled content entry points;
- enhanced/long-form content placement;
- platform-controlled blocks that affect page order;
- material responsive reordering and interaction patterns.

Text/DOM parsing may support the record but does not by itself prove high frontend fidelity.

**Outputs:**

- Platform Capability Map;
- **Channel Frontend Reference Pack**;
- Message-to-Slot Matrix;
- preliminary frontend fidelity status: `HIGH`, `PARTIAL`, `UNKNOWN`, or `BLOCKED`.

Do not convert a message list directly into an equal number of static banners.

**Major Stage Checkpoint:** present the verified platform capability map, Primary Reference, frontend evidence, fidelity status, open gaps, Message-to-Slot Matrix, and Stage Completion Manifest. The user may replace or approve the reference before Stage 6. A Transition Command locks the current reference pack with its open items.

## Stage 6 — Channel-specific Listing IA

Define reader sequence inside the **verified channel structure**. The same message may appear in several slots when its role changes, such as identity, summary, proof, scenario, comparison, or objection handling.

For channel-native work, build Page IA from the locked Channel Frontend Reference Pack rather than from a generic ecommerce layout or remembered marketplace anatomy.

Brand-controlled and platform-controlled sections must remain visibly distinct in the IA.

**Output:** Page IA for every page target.

**Major Stage Checkpoint:** review narrative order, page boundaries, channel shell assumptions, ownership, and Stage Completion Manifest before asset planning.

## Stage 6.5 — Asset Intake & Audit

Accept static assets and design sources. Reconcile them against the Stage 1 Asset Readiness Preflight.

Build an **Approved Asset Registry** containing stable Asset ID, canonical source, role, dimensions/aspect, page/offer scope, allowed slots, approval status, derivative provenance, and transform rule.

Build the Asset Manifest and Asset Gap Analysis. Classify gaps as render, photography, design, UI export, AI background, video, copy, channel-shell evidence, or blocked.

Approved assets become stable downstream inputs. Cropping, recomposition, role changes, text changes, or other material transformations create a derivative with a new Asset ID when they can affect meaning, evidence, dimensions, or slot suitability. Do not silently replace an approved original.

**Output:** Approved Asset Registry + Asset Manifest + Asset Gap Analysis.

Use `DEMO ASSET` or `PROVISIONAL UI` only where those labels do not misrepresent product truth.

**Major Stage Checkpoint:** review what is reusable, what is approved, what must be created, what cannot safely be represented, and Stage Completion Manifest.

## Stage 7 — Channel Slot / Module Planning

For every slot or module define message role, interaction, evidence, existing Asset ID, asset to create, copy status, claim gate, frontend reference region, ownership, and module-fit rationale.

Create the **Asset-to-Slot Contract** with Slot ID, page/offer, channel region/module, message role, required Asset ID, dimensions/aspect, crop/transform rule, interaction, and ownership.

Run `CONTENT_COVERAGE` and `MODULE_FIT_GATE` separately.

`CONTENT_COVERAGE` checks whether required P0/P1 messages, objections, proof points, and planned topics have valid homes.

`MODULE_FIT_GATE` checks whether each verified native module/component is actually appropriate for the message, evidence, interaction purpose, asset orientation/density, mobile behavior, frontend evidence, and channel constraints.

`CONTENT_COVERAGE = PASS` does not imply `MODULE_FIT_GATE = PASS`.

Independent static boards must not be mechanically grouped or sliced into a carousel/slide interaction later. If a carousel, hotspot, video, comparison, accordion, or other native interaction is selected, design its interaction logic and content packing here.

For channel-native work, the slot/module plan must cite the corresponding verified frontend region or explicitly mark the region as `UNKNOWN`.

**Output:** Channel Slot / Module Plan + Asset-to-Slot Contract + `CONTENT_COVERAGE` + `MODULE_FIT_GATE`.

**Major Stage Checkpoint:** review module packing, evidence assignment, channel-region mapping, interaction logic, asset-slot binding, module-fit results, and Stage Completion Manifest before visual production planning.

## Stage 7.5 — Visual Production Brief

Specify composition, visual subject, evidence object, product placement, UI placement, text safe area, responsive behavior, Asset ID/source, frontend-shell constraints, interaction-specific visual logic, and prohibited reconstruction.

Visual briefs define brand content, not a new marketplace shell. When the channel shell is platform-controlled, do not redesign it as a brand asset.

If Stage 7 selected an interactive native module, design the visual system for that interaction now. Do not postpone carousel/hotspot/slide logic to Demo Assembly.

**Output:** Visual Production Brief and Visual Evidence Matrix.

**Major Stage Checkpoint:** approve production direction, interaction-specific briefs, and Stage Completion Manifest before generating or assembling visuals.

## Stage 8 — Visual Production + Visual Evidence QA

Use:

```text
approved environment or AI background
+ real product asset
+ real UI
+ functional graphic overlay
+ final copy
```

Reject a visual when the subject or evidence object cannot directly prove the message.

Use the planned visual batch, not whichever subset happens to finish first. Compare planned counts/items against completed visuals in the Stage Completion Manifest.

Run `DIFFERENTIATOR_PROOF_GATE` for each visualizable P0 differentiator. Classify strongest proof as `DIRECT`, `INDIRECT`, `WEAK`, or `NONE`. At least one priority visual should provide `DIRECT` proof or the user must explicitly approve another proof strategy.

Within Stage 8, produce the planned reviewable visual batch. Do not ask after every frame unless the user requested per-asset review.

For a problematic frame or asset:

- identify the exact issue;
- make at most two autonomous correction attempts for that same issue;
- after two unsuccessful attempts, stop regenerating and surface the current best result plus `NEEDS REVISION` or blocked status;
- if the user says `继续`, `下一步`, `go next`, `先这样`, or equivalent, stop all further work on that frame immediately and advance to Stage 9 with the issue recorded.

Approved/locked visuals retain their Asset IDs. A later stage may not silently swap them for another slot-class asset or unapproved derivative.

**Output:** Master visuals, channel adaptations, Differentiator Proof Matrix, and `DIFFERENTIATOR_PROOF_GATE`.

**Major Stage Checkpoint:** user reviews the full planned visual batch status and Stage Completion Manifest. Stage 9 begins only after approval or a Transition Command, unless Autonomous Mode is active.

## Stage 9 — Channel-native Demo Assembly

Before assembling a native channel shell, run `FRONTEND_FIDELITY_GATE` using `references/channel-native-demo.md`.

Before and during assembly, run `ASSET_SLOT_GATE` against the locked Asset-to-Slot Contract. Use the exact approved Asset IDs assigned to the slots. Do not substitute an enhanced-content asset into a gallery slot, a gallery asset into another module, or an unapproved derivative merely because the layout appears to fit.

### Frontend Fidelity Gate

For a channel-native demo, verify that:

- a Primary Reference is locked;
- current consumer-facing visual evidence supports the material shell;
- material desktop structure is known;
- material mobile/app-web structure is known or explicitly scoped out by the user;
- material section order is known;
- brand-controlled and platform/retailer-controlled regions are separated;
- project content maps only to verified regions;
- unsupported channel UI is not fabricated.

If these conditions are not met, `FRONTEND_FIDELITY_GATE = FAIL`.

On FAIL, the allowed fallback is a clearly named **Content Review Demo**. A Content Review Demo may present approved messages, visuals, and sequence for review, but it must not be labeled an Amazon PDP Demo, Rakuten native page, retailer-native PDP, or other **channel-native demo**.

Do not invent custom branded navigation, marketplace chrome, buy-box controls, cards, tabs, or generic ecommerce layout and present them as native.

### Native assembly rule

When the gate passes:

1. reproduce the verified consumer-facing channel shell and section order first;
2. preserve evidenced hierarchy, spacing logic, and interaction patterns at the fidelity level supported by the reference;
3. place approved project content only into verified brand-controlled regions;
4. represent channel-controlled regions as evidenced structure or conservative placeholders;
5. keep workflow labels, internal IA names, module IDs, and evidence statuses out of Consumer Mode;
6. expose internal statuses only as Review Mode overlays that do not alter the underlying layout;
7. preserve desktop/mobile behavior evidenced by the reference pack;
8. implement the interaction already designed in Stage 7/7.5 rather than inventing it now.

After assembly, run `DELIVERY_PARITY_GATE`. Compare locked plan versus implemented slot/module, interaction, source Asset ID, dimensions/aspect, message coverage, page/offer ownership, and channel region.

`DELIVERY_PARITY_GATE = FAIL` if a planned carousel/hotspot becomes static, a planned module disappears, a wrong Asset ID is used, dimensions/crop rules change, or a planned message loses its mapped implementation.

A functioning HTML file is not evidence that parity passed.

**Output:** Channel-native Interactive Review Demo, or `Content Review Demo` when the fidelity gate fails, plus `ASSET_SLOT_GATE` and `DELIVERY_PARITY_GATE` results.

**Major Stage Checkpoint:** user reviews the demo, parity result, and Stage Completion Manifest before Final QA.

## Stage 10 — Final QA

Run Product, Claim, Channel, Market/Locale, Visual, Mobile, Technical, Review Mode, Execution Flow, **Frontend Fidelity**, delivery integrity, asset-slot, module-fit, differentiator-proof, parity, and naming QA.

Confirm that:

- Stage Completion Manifests did not turn missing work into success labels;
- required planned deliverables exist or the user explicitly approved reduced scope;
- `ASSET_SLOT_GATE` passes;
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or has an approved alternative;
- `DELIVERY_PARITY_GATE` passes;
- a deliverable called a channel-native PDP/demo actually passed `FRONTEND_FIDELITY_GATE`.

If any authoritative evidence changed after earlier locks, confirm a Change Impact Map was applied and only impacted outputs were reopened.

Report passed checks and open items separately.

**Output:** Final QA Result, Stage Completion Manifest, and Open Items.

Final QA may flag earlier locked-stage issues and trigger a targeted Change Impact Map; it must not silently redo or silently ignore them.
