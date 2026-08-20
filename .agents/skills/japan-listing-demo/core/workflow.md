# Workflow reference

## Execution control

**Checkpointed execution by default.** Complete one numbered stage to a reviewable state, emit a truthful **Stage Completion Manifest**, then stop at a **Major Stage Checkpoint** before entering the next numbered stage.

Read:

- `references/delivery-integrity.md` for completion, asset, module-fit, differentiator-proof, parity, and change-control rules;
- `references/executable-gates.md` for the **Project State Manifest**, approval provenance, locked plan hashes, and external validator;
- sibling `.agents/skills/listing-evidence-auditor/SKILL.md` for physical-file, provenance, approval, semantic-role, and asset-set reconciliation.

### Stage Completion Manifest

Every numbered stage records planned deliverables, completed items, approved/locked items, `NEEDS REVISION`, missing items, blocked items, open items, and `STAGE_STATUS = COMPLETE | PARTIAL | BLOCKED`.

A completed subset does not make the stage complete. Advancing a `PARTIAL` stage does not rewrite it as `COMPLETE`.

### Transition Command

Treat `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalent wording as a **Transition Command** unless the user explicitly asks to continue improving the current artifact.

On a Transition Command:

- stop current-stage retries/regeneration immediately;
- preserve the best current result;
- record unresolved items as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, `UNVERIFIED`, `HUMAN_REVIEW_REQUIRED`, or Open Items;
- finalize the Stage Completion Manifest with its real status;
- lock the current stage snapshot;
- advance to the next numbered stage;
- do not silently reopen the prior stage.

A Transition Command never promotes unverified asset evidence into final-consumable status.

### Retry Budget

For the same artifact and same identified problem, allow at most **two autonomous attempts** without new user input or new evidence. A Transition Command overrides the Retry Budget and advances immediately.

### Change Impact and targeted reopen

When newer authoritative facts, approved offer/strategy decisions, approved asset/UI sources, channel capability/reference, claim/legal decision, or auditor evidence materially changes, create a **Change Impact Map**.

Classify dependent outputs `UNAFFECTED`, `REVIEW`, `INVALIDATED`, or `REOPEN`. Preserve unaffected locked work and rerun only impacted stages/items.

### Autonomous Mode

Full continuous execution is opt-in only. Autonomous Mode does not bypass evidence, auditor, approval-provenance, executable, claim, asset-slot, module-fit, differentiator-proof, parity, or frontend-fidelity gates.

## Executable-gate rule

The agent maintains source state but does not author executable PASS verdicts.

Maintain one machine-readable **Project State Manifest** and run the external validator:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

Ignore any agent-authored `declared_gate_results`. If validator or required auditor execution cannot run, applicable gates remain `UNVERIFIED`; do not manually self-certify PASS.

## Evidence-auditor rule

Candidate state is not physical truth.

Use `listing-evidence-auditor` whenever real image/UI/asset files must become final-consumable. The auditor recomputes physical SHA-256 and dimensions, reconciles provenance and exact-hash approval, checks semantic visual role, and audits required asset-set completeness.

### Independent context

Prefer an **independent context** / isolated subagent for semantic audit. Send only the audit packet, exact file paths, approval events, prior locked hashes, expected role/slot evidence, and the minimum channel context required to interpret the slot.

Do not send desired conclusions or prior PASS statements.

If independent context is unavailable, deterministic physical checks may still run, but same-agent semantic review cannot final-PASS. Semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless a human explicitly approves exact physical hash + role + scope.

Auditor Evidence State has precedence over Candidate Asset Status when computing **Effective State**.

## Stage 0 — Project Definition

Record market, locale, region overlays, channel/site, category, product/offers, page targets, output type, review audience, and known account/retailer capabilities.

**Output:** Project Definition + selected profiles.

**Major Stage Checkpoint:** definition, assumptions, blockers, Stage Completion Manifest.

## Stage 1 — Source Intake + Asset Readiness Preflight

Collect product documents, specifications, approvals, commercial decisions, research, VOC, competitor pages, prior references, brand guidance, real product renders/photos, UI sources, videos, and any user-supplied channel frontend reference.

Create an **Asset Readiness Preflight** for asset classes expected later. Record received/missing/status/needed-by-stage/blocking impact.

**Output:** Project Input Pack + Asset Readiness Preflight.

**Major Stage Checkpoint:** sources, gaps, risks, Stage Completion Manifest.

## Stage 2 — Source Normalization & Coverage Gate

Record source authority, version/freshness, completeness, allowed usage, offer/page scope, and downstream dependencies. Keep product facts, commercial decisions, marketing decisions, consumer evidence, localization reference, channel capability, frontend visual reference, and visual asset evidence separate.

**Output:** Source Registry + Missing Coverage + `SOURCE_GATE`.

**Major Stage Checkpoint:** safe-to-continue work, blockers, open items, Stage Completion Manifest.

## Stage 3 — Fact Lock

Create Fact Ledger, Conflict Ledger, Missing Evidence, Claim Readiness, Gate Result. Earlier-generation evidence does not automatically prove successor facts.

**Gate:** `CONFLICT`, `MISSING`, `PROHIBITED`, or unqualified `CONDITIONAL` facts do not enter consumer copy.

**Major Stage Checkpoint:** locked facts/conflicts/claim impacts + Stage Completion Manifest.

## Stage 4 — Consumer Strategy

Draft target user, JTBD, pain points, purchase barriers, benefits, reasons to believe, differentiators, and message priority from evidence. Do not derive needs from country name alone.

Identify visualizable P0 purchase reasons and what would count as direct visual proof.

**Output:** Draft Consumer Strategy + Reviewable Strategy Snapshot.

**Major Stage Checkpoint:** strategy + P0 proof requirements.

## Stage 4.2 — Market & Localization Enrichment

Research:

```text
Product / Category × Market × Locale × Channel × Current evidence
```

Research may add need states, terminology, search language, purchase motivation, objections, scenarios, and channel conventions. It may not overwrite product facts.

**Output:** Market Evidence Registry + Localization Brief.

**Major Stage Checkpoint:** validated evidence, hypotheses, localization implications, Stage Completion Manifest.

## Stage 5 — Message Architecture

Define Core Promise, reasons to buy, trust evidence, objections, and message priority. Build shared product messages once, then fork by offer/page target.

**Output:** Message House + Message Priority.

**Major Stage Checkpoint:** hierarchy + P0 proof requirements.

## Stage 5.5 — Channel Template & Frontend Mapping + Channel Capability State

Read `references/channel-native-demo.md` when channel-native demo is requested.

### 5.5A — Platform Capability Research

Verify editable fields/regions, ownership, current module/component families, limits, policies, account access, publishing workflow, and mobile/app-web constraints.

**Official platform rules prove capability, not frontend fidelity.** Official rules do not substitute for current consumer-facing visual evidence.

Populate Project State channel section. Packaged executable ceilings come from `data/channel-policy-limits.json`; project state may lower but not raise them.

### 5.5B — Frontend Reference Intake

Ask whether user has a preferred current Reference URL / ASIN / retailer/store page / screenshot set / approved frontend capture. If none, research 1–3 current comparable consumer-facing references and recommend one Primary Reference.

### 5.5C — Frontend Visual Capture

Capture material desktop/mobile shell anatomy, section order, gallery/media behavior, offer/variation behavior, brand-controlled entry points, enhanced-content placement, platform-controlled blocks, responsive reordering, and interaction patterns.

**Outputs:** Platform Capability Map + Channel Frontend Reference Pack + Message-to-Slot Matrix + preliminary fidelity status.

**Major Stage Checkpoint:** capability state, Primary Reference, frontend evidence, open gaps, Stage Completion Manifest.

## Stage 6 — Channel-specific Listing IA

Build reader sequence inside verified channel structure. Keep brand-controlled and platform/retailer-controlled areas distinct. Preserve offer/page boundaries.

**Output:** Page IA for every page target.

**Major Stage Checkpoint:** narrative order, boundaries, shell assumptions, ownership, Stage Completion Manifest.

## Stage 6.5A — Candidate Asset Intake / Registry

Reconcile received assets against Stage 1 preflight, but do not promote the planner's asset claims to effective truth.

Create **Candidate Asset Registry** with:

- Asset ID;
- exact path;
- claimed role;
- page/offer scope;
- allowed slots;
- claimed parent/transform;
- claimed approval event.

Maintain corresponding candidate asset/approval state in Project State Manifest.

Candidate `LOCKED`, filename, Asset ID, and agent-authored SHA are assertions that still require physical audit.

**Output:** Candidate Asset Registry + Asset Manifest + Asset Gap Analysis + `audit-input.json`.

## Stage 6.5B — Evidence Reconciliation / Effective State

Delegate the audit packet to `listing-evidence-auditor`.

Auditor outputs:

- physical fingerprints from real files;
- evidence audit;
- semantic role result;
- provenance/approval result;
- asset-set result;
- Verified Asset Registry / Auditor Evidence State.

Merge Candidate State and Auditor Evidence State only through the **Effective State** rule:

```text
Auditor Evidence State > Candidate Asset Status
```

Set `audit_checkpoints.post_6_5_required = true` when final bindings depend on real assets. Run Project State validator for `EVIDENCE_RECONCILIATION_GATE`.

- Planning may continue with explicit gaps.
- Final Asset-to-Slot locking may use only `VERIFIED` or `HUMAN_APPROVED` assets.
- `PHYSICALLY_VERIFIED_ONLY`, `INVALIDATED`, `UNVERIFIED`, and `HUMAN_REVIEW_REQUIRED` are not final-consumable.

**Output:** Auditor Evidence State + Effective State + `EVIDENCE_RECONCILIATION_GATE`.

**Major Stage Checkpoint:** candidate vs auditor conflicts, exact hashes, provenance, approval, semantic role, incomplete sets, Stage Completion Manifest.

## Stage 7 — Channel Slot / Module Planning + Asset-to-Slot Contract + Module Budget Validation

For every slot/module define message role, verified native module family, interaction, evidence, Asset IDs, asset-to-create, claim gate, frontend region, ownership, and module-fit rationale.

Run `CONTENT_COVERAGE` and `MODULE_FIT_GATE` separately. Full topic coverage does not prove native module fit.

Independent static boards must not be mechanically sliced/grouped into carousel/slides later. If interactive module selected, design interaction logic/content packing here.

Create **Asset-to-Slot Contract**. Required final Asset IDs must be final-consumable in Effective State.

Write proposed modules into `locked_module_plan`, compute canonical `plan_hash`, run `CHANNEL_MODULE_BUDGET_GATE`, then record user approval whose hash matches exact plan before setting plan `LOCKED`.

Do not add more modules merely to match topic count. Pack messages into verified channel module budget.

**Output:** Channel Slot / Module Plan + Asset-to-Slot Contract + `CONTENT_COVERAGE` + `MODULE_FIT_GATE` + module-budget result + locked plan hash.

**Major Stage Checkpoint:** exact module count, packing, interactions, asset bindings, plan hash, Stage Completion Manifest.

## Stage 7.5 — Visual Production Brief + Transform Authorization

Specify composition, visual subject, evidence object, product/UI placement, text safe area, responsive behavior, Asset ID/source, frontend-shell constraints, interaction-specific visual logic, and prohibited reconstruction.

Material crop/recomposition/background replacement/role change is a derivative. Record `derivative_of`, transform type, target slot, transform approval ID, approved stage, and canonical transform hash.

“Deterministic crop” is not authorization.

**Output:** Visual Production Brief + Visual Evidence Matrix + transform authorization state.

**Major Stage Checkpoint:** production direction, interaction system, transforms, Stage Completion Manifest.

## Stage 8 — Visual Production + Visual Evidence / Differentiator Proof QA

Produce planned visual batch using approved environments/backgrounds plus real product/UI evidence. Reject visuals whose subject/evidence object cannot directly support message.

Run `DIFFERENTIATOR_PROOF_GATE`. At least one priority visual should provide `DIRECT` proof for each visualizable P0 differentiator, or user explicitly approves another proof strategy.

Approved visuals retain stable Asset IDs. Later stages may not silently substitute another role-class asset or unapproved derivative.

For repeated frame problem, obey Retry Budget. Transition Command stops further attempts immediately.

**Output:** Master visuals + channel adaptations + Differentiator Proof Matrix.

**Major Stage Checkpoint:** full visual-batch status + Stage Completion Manifest.

## Stage 8.5 — Pre-Demo Evidence Audit

Before Stage 9, generate a fresh `pre-9` audit packet for the exact final files referenced by the locked module plan and Asset-to-Slot Contract.

Run `listing-evidence-auditor` again against:

- final generated/edited files;
- derivatives;
- recomputed physical SHA-256;
- approval carryover;
- semantic visual role;
- page/offer/slot scope;
- complete required asset set.

Set `audit_checkpoints.pre_9_required = true` and write auditor output into Project State `auditor_evidence` with `checkpoint = pre-9`.

Run the external validator for `PRE_DEMO_ASSET_GATE`.

`PRE_DEMO_ASSET_GATE` passes only when every required asset is `VERIFIED` or `HUMAN_APPROVED` and the auditor asset-set gate passes. One invalidated/unverified required member blocks Stage 9.

If independent semantic context is unavailable and role evidence is material, the result is `HUMAN_REVIEW_REQUIRED` / `UNVERIFIED`, not PASS.

**Output:** fresh Auditor Evidence State + `PRE_DEMO_ASSET_GATE`.

**Major Stage Checkpoint:** exact file/hash/role/scope results, invalidations, human-review requirements, Stage Completion Manifest.

## Stage 9 — Channel-native Demo Assembly + Module Origin / Asset / Parity Validation

Stage 9 is an assembler, not a new planning stage.

Before native shell assembly, require:

- `FRONTEND_FIDELITY_GATE` acceptable;
- `PRE_DEMO_ASSET_GATE = PASS` for final channel-native asset consumption;
- exact locked `plan_hash`;
- final Asset-to-Slot Contract.

Implementation must consume exact locked plan hash. Do not add/delete modules, change native type/interaction, change Asset IDs, or retroactively edit plan to match implementation.

Run external validator. Machine-computed gates include:

- `CHANNEL_MODULE_BUDGET_GATE`;
- `APPROVAL_PROVENANCE_GATE`;
- `MODULE_ORIGIN_GATE`;
- `TRANSFORM_AUTH_GATE`;
- `EVIDENCE_RECONCILIATION_GATE` when required;
- `ASSET_SLOT_GATE`;
- `PRE_DEMO_ASSET_GATE` when required;
- `DELIVERY_PARITY_GATE`.

`MODULE_ORIGIN_GATE` fails on unplanned/omitted modules, type/interaction drift, or wrong plan hash.

`TRANSFORM_AUTH_GATE` fails on derivative without transform approval provenance.

`ASSET_SLOT_GATE` fails when implementation uses different Asset IDs, assets outside allowed slot, non-final auditor status, or candidate SHA conflicts with auditor physical SHA.

A functioning HTML file is not evidence gates passed.

### Native assembly rule

When fidelity and pre-demo asset gates pass:

1. reproduce verified channel shell/order;
2. preserve evidenced hierarchy/interactions;
3. insert final-consumable project content only into verified brand-controlled regions;
4. keep channel-owned regions conservative;
5. keep internal labels out of Consumer Mode;
6. Review Mode overlays must not alter underlying layout.

If frontend fidelity fails, use **Content Review Demo**. If pre-demo asset gate fails, do not present final channel-native Demo as complete.

**Output:** Channel-native Interactive Review Demo or Content Review Demo + external-validator results.

**Major Stage Checkpoint:** demo, machine/auditor gate results, Stage Completion Manifest.

## Stage 10 — Final QA

Run Product, Claim, Channel, Market/Locale, Visual, Mobile, Technical, Review Mode, Execution Flow, Frontend Fidelity, Delivery Integrity, Evidence Auditor, Executable Gate, and naming QA.

Confirm:

- Stage Completion Manifests are truthful;
- planned deliverables exist or reduced scope explicitly approved;
- `CONTENT_COVERAGE` acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or approved alternative exists;
- required auditor results are attached;
- `PRE_DEMO_ASSET_GATE` passed before final channel-native asset consumption;
- external validator output attached for applicable executable gates;
- channel-native naming used only after frontend fidelity passes;
- authoritative changes handled through Change Impact Map.

Executable/auditor gates cannot be replaced with agent-authored prose. `UNVERIFIED` and `HUMAN_REVIEW_REQUIRED` remain visible until legitimately resolved.

**Output:** Final QA Result + auditor/external-validator result + Stage Completion Manifest + Open Items.
