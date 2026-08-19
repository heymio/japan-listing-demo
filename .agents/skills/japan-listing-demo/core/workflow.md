# Workflow reference

## Execution control

**Checkpointed execution by default.** Complete one numbered stage to a reviewable state, emit a truthful **Stage Completion Manifest**, then stop at a **Major Stage Checkpoint** before entering the next numbered stage.

Read:

- `references/delivery-integrity.md` for completion, asset, module-fit, differentiator-proof, parity, and change-control rules;
- `references/executable-gates.md` for the **Project State Manifest**, approval provenance, locked plan hashes, and external validator.

### Stage Completion Manifest

Every numbered stage records planned deliverables, completed items, approved/locked items, `NEEDS REVISION`, missing items, blocked items, open items, and `STAGE_STATUS = COMPLETE | PARTIAL | BLOCKED`.

A completed subset does not make the stage complete. Advancing a `PARTIAL` stage does not rewrite it as `COMPLETE`.

### Transition Command

Treat `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalent wording as a **Transition Command** unless the user explicitly asks to continue improving the current artifact.

On a Transition Command:

- stop current-stage retries/regeneration immediately;
- preserve the best current result;
- record unresolved items as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, `UNVERIFIED`, or Open Items;
- finalize the Stage Completion Manifest with its real status;
- lock the current stage snapshot;
- advance to the next numbered stage;
- do not silently reopen the prior stage.

### Retry Budget

For the same artifact and same identified problem, allow at most **two autonomous attempts** without new user input or new evidence. A Transition Command overrides the Retry Budget and advances immediately.

### Change Impact and targeted reopen

When a newer authoritative fact, approved offer/strategy decision, approved asset/UI source, channel capability/reference, or claim/legal decision materially changes, create a **Change Impact Map**.

Classify dependent outputs `UNAFFECTED`, `REVIEW`, `INVALIDATED`, or `REOPEN`. Preserve unaffected locked work and rerun only impacted stages/items.

### Autonomous Mode

Full continuous execution is opt-in only. Autonomous Mode does not bypass evidence, approval-provenance, executable, claim, asset-slot, module-fit, differentiator-proof, parity, or frontend-fidelity gates.

## Executable-gate rule

The agent maintains source state but does not author executable PASS verdicts.

Maintain one machine-readable **Project State Manifest** and run the **external validator**:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

Ignore any agent-authored `declared_gate_results` field. If the validator cannot run, applicable executable gates remain `UNVERIFIED`; do not manually self-certify PASS.

## Stage 0 — Project Definition

Record market, locale, region overlays, channel/site, category, product/offers, page targets, output type, review audience, and known account/retailer capabilities.

**Output:** Project Definition and selected profiles.

**Major Stage Checkpoint:** present definition, assumptions, blockers, and Stage Completion Manifest.

## Stage 1 — Source Intake + Asset Readiness Preflight

Collect product documents, specifications, approvals, commercial decisions, research, VOC, competitor pages, prior references, brand guidance, real product renders/photos, UI sources, videos, and any user-supplied channel frontend reference.

Create an **Asset Readiness Preflight** for asset classes the project is expected to need later. Record received/missing/status/needed-by-stage/blocking impact.

**Output:** Project Input Pack + Asset Readiness Preflight.

**Major Stage Checkpoint:** summarize sources, gaps, risks, and Stage Completion Manifest.

## Stage 2 — Source Normalization & Coverage Gate

Record source authority, version/freshness, completeness, allowed usage, offer/page scope, and downstream dependencies. Keep product fact, commercial decision, marketing decision, consumer evidence, localization reference, channel capability, frontend visual reference, and visual asset evidence separate.

**Output:** Source Registry, Missing Coverage, `SOURCE_GATE`.

**Major Stage Checkpoint:** show safe-to-continue work, blocked work, open items, and Stage Completion Manifest.

## Stage 3 — Fact Lock

Create Fact Ledger, Conflict Ledger, Missing Evidence, Claim Readiness, and Gate Result. Earlier-generation evidence does not automatically prove successor facts.

**Gate:** `CONFLICT`, `MISSING`, `PROHIBITED`, or unqualified `CONDITIONAL` facts do not enter consumer copy.

**Major Stage Checkpoint:** present locked facts/conflicts/claim impacts and Stage Completion Manifest.

## Stage 4 — Consumer Strategy

Draft target user, JTBD, pain points, purchase barriers, benefits, reasons to believe, differentiators, and message priority from evidence. Do not derive needs from the country name alone.

Identify visualizable P0 purchase reasons and what would count as direct visual proof.

**Output:** Draft Consumer Strategy + Reviewable Strategy Snapshot.

**Major Stage Checkpoint:** user reviews strategy and P0 proof requirements.

## Stage 4.2 — Market & Localization Enrichment

Research:

```text
Product / Category × Market × Locale × Channel × Current evidence
```

Research may add need states, terminology, search language, purchase motivation, objections, scenarios, and channel conventions. It may not overwrite product facts.

**Output:** Market Evidence Registry + Localization Brief.

**Major Stage Checkpoint:** present validated evidence, hypotheses, localization implications, and Stage Completion Manifest.

## Stage 5 — Message Architecture

Define Core Promise, reasons to buy, trust evidence, objections, and message priority. Build shared product messages once, then fork by offer/page target.

**Output:** Message House + Message Priority.

**Major Stage Checkpoint:** user reviews hierarchy and P0 proof requirements.

## Stage 5.5 — Channel Template & Frontend Mapping + Channel Capability State

Read `references/channel-native-demo.md` when a channel-native demo is requested.

### 5.5A — Platform Capability Research

Verify editable fields/regions, ownership, current module/component families, limits, policies, account access, publishing workflow, and mobile/app-web constraints.

**Official platform rules prove capability, not frontend fidelity.** Official rules do not substitute for current consumer-facing visual evidence.

Populate the Project State Manifest channel section. For packaged executable ceilings, use `data/channel-policy-limits.json`; a project may use a lower supported account limit but may not raise the packaged ceiling by self-declaration.

### 5.5B — Frontend Reference Intake

Ask whether the user has a preferred current Reference URL / ASIN / retailer page / store page / screenshot set / approved frontend capture. If none is supplied, research 1–3 current comparable consumer-facing references and recommend one Primary Reference.

### 5.5C — Frontend Visual Capture

Capture material desktop/mobile shell anatomy, section order, gallery/media behavior, offer/variation behavior, brand-controlled entry points, enhanced-content placement, platform-controlled blocks, responsive reordering, and interaction patterns.

**Outputs:** Platform Capability Map + Channel Frontend Reference Pack + Message-to-Slot Matrix + preliminary fidelity status.

**Major Stage Checkpoint:** present capability state, Primary Reference, frontend evidence, open gaps, and Stage Completion Manifest.

## Stage 6 — Channel-specific Listing IA

Build reader sequence inside the verified channel structure. Keep brand-controlled and platform/retailer-controlled areas distinct. Preserve offer/page boundaries.

**Output:** Page IA for every page target.

**Major Stage Checkpoint:** review narrative order, boundaries, channel shell assumptions, ownership, and Stage Completion Manifest.

## Stage 6.5 — Asset Intake + Approved Asset Registry + Approval Provenance

Reconcile received assets against the Stage 1 preflight. Build the Approved Asset Registry with stable Asset IDs, canonical source, SHA-256, role, dimensions/aspect, page/offer scope, allowed slots, approval status, derivative provenance, and transform rule.

Maintain matching asset state and approval events in the Project State Manifest.

A `LOCKED` asset requires either:

- matching user approval provenance bound to the current asset hash; or
- exact recovery where current SHA-256 equals the prior locked SHA-256.

Filename similarity or visual resemblance is not exact recovery. A found asset may remain `RECOVERED_UNAPPROVED` until valid provenance exists.

**Output:** Approved Asset Registry + Asset Manifest + Asset Gap Analysis + Project State asset/approval state.

**Major Stage Checkpoint:** review reusable/approved/missing assets, provenance, and Stage Completion Manifest.

## Stage 7 — Channel Slot / Module Planning + Asset-to-Slot Contract + Module Budget Validation

For every slot/module define message role, verified native module family, interaction, evidence, Asset IDs, asset-to-create, claim gate, frontend region, ownership, and module-fit rationale.

Run `CONTENT_COVERAGE` and `MODULE_FIT_GATE` separately. Full topic coverage does not prove native module fit.

Independent static boards must not be mechanically sliced/grouped into carousel/slides later. If an interactive module is selected, design its interaction logic and content packing here.

Create the **Asset-to-Slot Contract**.

Write the proposed modules into `locked_module_plan`, compute the canonical `plan_hash`, and run the external validator for `CHANNEL_MODULE_BUDGET_GATE` before the plan is eligible for user lock.

After user review, record a plan approval event whose `approved_hash` matches the exact plan hash. Only then set `locked_module_plan.status = LOCKED`.

Do not add more modules to satisfy message-topic count. Pack messages into the verified channel module budget.

**Output:** Channel Slot / Module Plan + Asset-to-Slot Contract + `CONTENT_COVERAGE` + `MODULE_FIT_GATE` + executable module-budget result + locked plan hash.

**Major Stage Checkpoint:** user reviews exact module count, packing, interactions, asset bindings, plan hash, and Stage Completion Manifest.

## Stage 7.5 — Visual Production Brief + Transform Authorization

Specify composition, visual subject, evidence object, product/UI placement, text safe area, responsive behavior, Asset ID/source, frontend-shell constraints, interaction-specific visual logic, and prohibited reconstruction.

If a crop/recomposition/background replacement/role change creates a material derivative, record `derivative_of`, transform type, target slot, transform approval ID, approved stage, and canonical transform hash in the Project State Manifest.

“Deterministic crop” is not authorization. A derivative intended for a new interaction or slot requires transform approval before Demo Assembly.

**Output:** Visual Production Brief + Visual Evidence Matrix + transform authorization state.

**Major Stage Checkpoint:** approve production direction, interaction system, transforms, and Stage Completion Manifest.

## Stage 8 — Visual Production + Visual Evidence / Differentiator Proof QA

Produce the planned visual batch using approved environments/backgrounds plus real product/UI evidence. Reject visuals whose subject/evidence object cannot directly support the message.

Run `DIFFERENTIATOR_PROOF_GATE` for visualizable P0 differentiators. At least one priority visual should provide `DIRECT` proof or the user explicitly approves another proof strategy.

Approved visuals retain stable Asset IDs. Later stages may not silently substitute another role-class asset or unapproved derivative.

For a repeated frame problem, obey the Retry Budget. A Transition Command stops further attempts immediately.

**Output:** Master visuals + channel adaptations + Differentiator Proof Matrix.

**Major Stage Checkpoint:** review the full planned visual-batch status and Stage Completion Manifest.

## Stage 9 — Channel-native Demo Assembly + Module Origin / Asset / Parity Validation

Stage 9 is an assembler, not a new planning stage.

Before native shell assembly, run `FRONTEND_FIDELITY_GATE`.

The implementation must consume the exact locked `plan_hash`. Write implemented slots into the Project State Manifest. Do not add a module, delete a module, change `native_type`, change interaction, or change Asset IDs and then retroactively edit the plan to match.

Run the external validator. Applicable machine-computed gates include:

- `CHANNEL_MODULE_BUDGET_GATE`;
- `APPROVAL_PROVENANCE_GATE`;
- `MODULE_ORIGIN_GATE`;
- `TRANSFORM_AUTH_GATE`;
- `ASSET_SLOT_GATE`;
- `DELIVERY_PARITY_GATE`.

`MODULE_ORIGIN_GATE` fails when implementation contains a module not present in the locked plan, omits a planned module, changes type/interaction, or does not consume the locked plan hash.

`TRANSFORM_AUTH_GATE` fails when a locked derivative lacks matching transform approval provenance.

`ASSET_SLOT_GATE` fails when implementation uses different Asset IDs from the locked contract or uses an asset outside its allowed slot.

A functioning HTML file is not evidence that these gates passed.

If validator execution is unavailable, applicable executable gates remain `UNVERIFIED`; do not manually self-certify PASS.

### Native assembly rule

When frontend fidelity passes:

1. reproduce the verified consumer-facing channel shell and section order;
2. preserve evidenced hierarchy and interaction patterns;
3. insert approved project content only into verified brand-controlled regions;
4. keep platform-controlled regions conservative;
5. keep internal labels out of Consumer Mode;
6. Review Mode overlays must not alter underlying layout.

If frontend fidelity fails, use the fallback name **Content Review Demo**.

**Output:** Channel-native Interactive Review Demo or Content Review Demo + external-validator result.

**Major Stage Checkpoint:** user reviews the demo, machine gate result, and Stage Completion Manifest before Final QA.

## Stage 10 — Final QA

Run Product, Claim, Channel, Market/Locale, Visual, Mobile, Technical, Review Mode, Execution Flow, Frontend Fidelity, Delivery Integrity, Executable Gate, and naming QA.

Confirm:

- Stage Completion Manifests are truthful;
- planned deliverables exist or reduced scope is explicitly approved;
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or has an approved alternative;
- external validator output is attached for applicable executable gates;
- channel-native naming is used only after `FRONTEND_FIDELITY_GATE` passes;
- any newer authoritative evidence was handled through a Change Impact Map.

Executable gates cannot be replaced with agent-authored prose. `UNVERIFIED` remains visible until the validator can run or the governing machine policy is updated.

**Output:** Final QA Result + external-validator result + Stage Completion Manifest + Open Items.
