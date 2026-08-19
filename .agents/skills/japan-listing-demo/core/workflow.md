# Workflow reference

## Execution control

**Continuous execution by default.** Execute every non-blocked stage required to reach the deliverable requested by the user.

A **Gate is not a pause point**. Gates validate whether evidence may flow into later outputs; they do not require a user reply before the workflow can continue automatically.

Use these rules across all stages:

- Progress updates are informational and non-blocking.
- Missing or conditional evidence blocks only dependent claims or assets, not the whole workflow.
- Preserve unresolved items as `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items as appropriate.
- Do not ask for “continue”, “go”, “confirm”, or equivalent approval after a normal stage.
- Stop at an explicit checkpoint when the user requests one.
- Stop for a **Hard Blocker** only when the next output would otherwise become materially invalid or misleading, such as an unresolved authoritative fact conflict, an unresolved channel/offer/page-target decision that changes architecture, or missing real product/UI evidence that cannot be represented safely.
- A normal review opportunity is not a Hard Blocker. Produce a reviewable snapshot and continue automatically unless the user requested a checkpoint.

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

If one field is uncertain but the uncertainty does not change the requested downstream architecture, mark it open and continue. Pause only if the unresolved choice is a Hard Blocker.

## Stage 1 — Source Intake

Collect product marketing documents, specifications, project approvals, pricing decisions, research, VOC, competitor pages, earlier-generation references, brand guidance, product renders, UI sources, and videos.

VOC remains an independent evidence stream. A competitor URL does not make VOC complete.

**Output:** Project Input Pack.

Continue automatically into source normalization unless the user explicitly requested an intake-only checkpoint.

## Stage 2 — Source Normalization & Coverage Gate

For every source record product, offer, version, authority, freshness, completeness, allowed usage, and downstream dependencies.

Separate product-fact authority, commercial-decision authority, marketing-decision authority, consumer evidence, localization reference, channel reference, and visual reference.

Classify missing information by downstream impact.

**Output:** Source Registry, Missing Coverage, and `SOURCE_GATE`.

`SOURCE_GATE` is an internal validation result, not a mandatory approval step. Continue every output that the available evidence supports.

## Stage 3 — Fact Lock

Create:

- Fact Ledger
- Conflict Ledger
- Missing Evidence
- Claim Readiness
- Gate Result

For successor products, distinguish `INHERITED-PENDING`, `UPGRADED`, `NEW`, `CONFLICT`, and `MISSING`. An earlier product never proves a new product fact without explicit inheritance evidence.

**Gate:** Consumer copy cannot use `CONFLICT`, `MISSING`, `PROHIBITED`, or an unqualified `CONDITIONAL` fact.

A blocked claim does not block unrelated strategy, IA, module planning, or demo work. Continue automatically with safe boundaries unless the conflict is required to determine the next architecture.

## Stage 4 — Consumer Strategy

Draft Target User, JTBD, Pain Points, Purchase Barriers, Benefits, Reasons to Believe, Differentiators, and Message Priority from the evidence.

Do not derive needs from the country name alone.

The strategy must be easy for the user to review, confirm, or override, but reviewability does not create a mandatory pause.

**Output:** Draft Consumer Strategy and **Reviewable Strategy Snapshot**.

If the user did not request a strategy checkpoint, continue automatically into Market & Localization Enrichment and later stages. If the user later overrides the strategy, reconcile affected downstream work.

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

Unresolved non-critical market hypotheses remain labeled and do not stop the workflow.

## Stage 5 — Message Architecture

Define the Core Promise, reasons to buy, trust evidence, objections, and message priority. Build shared product messages once, then fork by offer and page target.

**Output:** Message House and Message Priority.

Continue automatically unless the user explicitly asked to approve message architecture before page planning.

## Stage 5.5 — Channel Template Mapping

Load the selected channel profile and verify the actual account or retailer capabilities. Map messages to the editable slots and module families available for the project.

Do not convert a message list directly into an equal number of static banners.

**Output:** Channel Capability Map and Message-to-Slot Matrix.

If a specific module is unverified, mark it `UNKNOWN` or `PENDING` and use a safe alternative where possible. Pause only when the unknown capability changes the page architecture and no safe branch exists.

## Stage 6 — Channel-specific Listing IA

Define reader sequence inside the real channel structure. The same message may appear in several slots when its role changes, such as identity, summary, proof, scenario, comparison, or objection handling.

**Output:** Page IA for every page target.

## Stage 6.5 — Asset Intake & Audit

Accept static assets and design sources. Build an Asset Manifest containing object, source, quality, evidence supported, usable slots, status, and replacement requirement.

Classify gaps as render, photography, design, UI export, AI background, video, copy, or blocked.

**Output:** Asset Manifest and Asset Gap Analysis.

Missing assets do not stop module planning. Use `DEMO ASSET` or `PROVISIONAL UI` only where that label does not misrepresent product truth.

## Stage 7 — Channel Slot / Module Planning

For every slot or module define message role, interaction, evidence, existing asset, asset to create, copy status, and claim gate.

**Output:** Channel Slot / Module Plan.

## Stage 7.5 — Visual Production Brief

Specify composition, visual subject, evidence object, product placement, UI placement, text safe area, responsive behavior, asset source, and prohibited reconstruction.

**Output:** Visual Production Brief and Visual Evidence Matrix.

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

**Output:** Master visuals and channel adaptations.

When several approved modules remain, produce them as a batch rather than asking for approval after each image. Stop between visuals only if the user explicitly requested per-asset review or if a Hard Blocker emerges.

## Stage 9 — Interactive Demo Assembly

Implement only the interactions required to review the proposed page: gallery, tabs, carousel, hotspot, storyboard or video, comparison, Q&A, variants, responsive layout, and review mode.

When downloaded-file previews may restrict JavaScript, use native HTML or CSS-safe controls for essential interactions.

**Output:** Interactive Review Demo.

## Stage 10 — Final QA

Run Product, Claim, Channel, Market/Locale, Visual, Mobile, Technical, Review Mode, and Execution Flow QA. Report passed checks and open items separately.

**Output:** Final QA Result and Open Items.
