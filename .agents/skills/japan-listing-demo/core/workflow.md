# Workflow reference

## Execution control

**Checkpointed execution by default.** Complete one numbered stage to a reviewable state, present its output and open items, then stop at a **Major Stage Checkpoint** before entering the next numbered stage.

Checkpoints are for numbered workflow stages, not every trivial subtask. Within a stage, complete the planned analysis or reviewable batch without asking for approval after every search, table, tool call, frame, or image.

### Transition Command

Treat `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalent wording as a **Transition Command** unless the user explicitly says to continue improving the current artifact.

On a Transition Command:

- stop current-stage retries and regeneration immediately;
- preserve the best current result;
- mark unresolved issues as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items;
- lock the current stage snapshot;
- advance to the next numbered stage;
- do not reopen the locked stage unless the user asks to return or new authoritative evidence materially invalidates it.

### Retry Budget

For the same artifact and the same identified problem, allow at most **two autonomous attempts** without new user input or new evidence. After the Retry Budget is exhausted, stop the loop and wait at the current Major Stage Checkpoint with the current best result or a blocked status.

A Transition Command overrides the Retry Budget and advances immediately.

### Autonomous Mode

Full continuous execution is opt-in only. If the user explicitly requests no stage checkpoints for the current task, run non-blocked stages continuously for that task. This does not change the default behavior for later work.

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

**Major Stage Checkpoint:** present the definition, assumptions, and blockers. Wait for approval or a Transition Command before Stage 1, unless Autonomous Mode is active.

## Stage 1 — Source Intake

Collect product marketing documents, specifications, project approvals, pricing decisions, research, VOC, competitor pages, earlier-generation references, brand guidance, product renders, UI sources, and videos.

VOC remains an independent evidence stream. A competitor URL does not make VOC complete.

**Output:** Project Input Pack.

**Major Stage Checkpoint:** summarize sources received, missing inputs, and source-quality risks. Wait for review before Stage 2 unless Autonomous Mode is active.

## Stage 2 — Source Normalization & Coverage Gate

For every source record product, offer, version, authority, freshness, completeness, allowed usage, and downstream dependencies.

Separate product-fact authority, commercial-decision authority, marketing-decision authority, consumer evidence, localization reference, channel reference, and visual reference.

Classify missing information by downstream impact.

**Output:** Source Registry, Missing Coverage, and `SOURCE_GATE`.

**Major Stage Checkpoint:** show what is safe to continue, what is blocked, and what remains open. `SOURCE_GATE` is a validation result, not permission to invent missing facts.

## Stage 3 — Fact Lock

Create:

- Fact Ledger
- Conflict Ledger
- Missing Evidence
- Claim Readiness
- Gate Result

For successor products, distinguish `INHERITED-PENDING`, `UPGRADED`, `NEW`, `CONFLICT`, and `MISSING`. An earlier product never proves a new product fact without explicit inheritance evidence.

**Gate:** Consumer copy cannot use `CONFLICT`, `MISSING`, `PROHIBITED`, or an unqualified `CONDITIONAL` fact.

**Major Stage Checkpoint:** present locked facts, conflicts, claim gates, and affected page scopes. Wait before Stage 4 unless Autonomous Mode is active.

## Stage 4 — Consumer Strategy

Draft Target User, JTBD, Pain Points, Purchase Barriers, Benefits, Reasons to Believe, Differentiators, and Message Priority from the evidence.

Do not derive needs from the country name alone.

**Output:** Draft Consumer Strategy and Reviewable Strategy Snapshot.

**Major Stage Checkpoint:** this is a real review point. Let the user confirm, override, or redirect strategy before market enrichment and message architecture.

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

**Major Stage Checkpoint:** present validated market evidence, hypotheses, and localization implications. Wait for review before Stage 5 unless Autonomous Mode is active.

## Stage 5 — Message Architecture

Define the Core Promise, reasons to buy, trust evidence, objections, and message priority. Build shared product messages once, then fork by offer and page target.

**Output:** Message House and Message Priority.

**Major Stage Checkpoint:** user reviews message hierarchy before channel mapping.

## Stage 5.5 — Channel Template Mapping

Load the selected channel profile and verify the actual account or retailer capabilities. Map messages to the editable slots and module families available for the project.

Do not convert a message list directly into an equal number of static banners.

**Output:** Channel Capability Map and Message-to-Slot Matrix.

If a specific module is unverified, mark it `UNKNOWN` or `PENDING` and surface the impact.

**Major Stage Checkpoint:** review the real channel structure before IA.

## Stage 6 — Channel-specific Listing IA

Define reader sequence inside the real channel structure. The same message may appear in several slots when its role changes, such as identity, summary, proof, scenario, comparison, or objection handling.

**Output:** Page IA for every page target.

**Major Stage Checkpoint:** review narrative order and page boundaries before asset planning.

## Stage 6.5 — Asset Intake & Audit

Accept static assets and design sources. Build an Asset Manifest containing object, source, quality, evidence supported, usable slots, status, and replacement requirement.

Classify gaps as render, photography, design, UI export, AI background, video, copy, or blocked.

**Output:** Asset Manifest and Asset Gap Analysis.

Use `DEMO ASSET` or `PROVISIONAL UI` only where those labels do not misrepresent product truth.

**Major Stage Checkpoint:** review what is reusable, what must be created, and what cannot safely be represented.

## Stage 7 — Channel Slot / Module Planning

For every slot or module define message role, interaction, evidence, existing asset, asset to create, copy status, and claim gate.

**Output:** Channel Slot / Module Plan.

**Major Stage Checkpoint:** review module packing and evidence assignment before visual production planning.

## Stage 7.5 — Visual Production Brief

Specify composition, visual subject, evidence object, product placement, UI placement, text safe area, responsive behavior, asset source, and prohibited reconstruction.

**Output:** Visual Production Brief and Visual Evidence Matrix.

**Major Stage Checkpoint:** approve the production direction before generating or assembling visuals.

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

Within Stage 8, produce the planned reviewable visual batch. Do not ask after every frame unless the user requested per-asset review.

For a problematic frame or asset:

- identify the exact issue;
- make at most two autonomous correction attempts for that same issue;
- after two unsuccessful attempts, stop regenerating and surface the current best result plus `NEEDS REVISION` or blocked status;
- if the user says `继续`, `下一步`, `go next`, `先这样`, or equivalent, stop all further work on that frame immediately and advance to Stage 9 with the issue recorded.

**Major Stage Checkpoint:** user reviews the visual batch. Stage 9 begins only after approval or a Transition Command, unless Autonomous Mode is active.

## Stage 9 — Interactive Demo Assembly

Implement only the interactions required to review the proposed page: gallery, tabs, carousel, hotspot, storyboard or video, comparison, Q&A, variants, responsive layout, and review mode.

When downloaded-file previews may restrict JavaScript, use native HTML or CSS-safe controls for essential interactions.

Do not treat the existence of a working HTML file as proof that the visual or marketing quality is approved. Assemble only from the currently locked stage outputs and preserve unresolved visual issues visibly in Review Mode.

**Output:** Interactive Review Demo.

**Major Stage Checkpoint:** user reviews the demo before Final QA.

## Stage 10 — Final QA

Run Product, Claim, Channel, Market/Locale, Visual, Mobile, Technical, Review Mode, and Execution Flow QA. Report passed checks and open items separately.

**Output:** Final QA Result and Open Items.

Final QA does not silently reopen locked earlier stages. It may flag issues for a later revision cycle.
