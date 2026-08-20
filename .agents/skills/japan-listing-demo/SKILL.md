---
name: japan-listing-demo
description: Use when planning, reviewing, or producing Japan-market product listing strategy, enhanced content, visual briefs, or interactive review demos across Japanese ecommerce channels, DTC pages, and retailer PDPs from product evidence, VOC, competitor pages, research, or design assets.
---

# Japan Listing Demo

## Distribution

This is a **standalone distribution** for the main workflow and a one-repository Codex distribution with a sibling `listing-evidence-auditor` Skill. The normal user-facing invocation remains only `$japan-listing-demo`.

The bundled core provenance is recorded in `core/manifest.yaml`. It is not a runtime dependency on another repository.

## Core principle

Build one evidence-governed Product Truth and Product Strategy, then adapt them to the requested Japan market, locale, channel, category, offer, and page targets. A country label is not a consumer persona or product-category playbook.

When the output is a **channel-native demo**, do not design the channel shell from memory. Verify the current consumer-facing frontend first, lock a Primary Reference, and reproduce the evidenced channel structure before inserting project content.

Do not treat a polished partial artifact as a complete stage. Do not silently replace approved assets downstream. Content coverage, native module fit, visual proof strength, and implemented parity are separate checks.

Critical structural gates must not be self-certified by the same agent that authored the state. Read `references/executable-gates.md`, maintain a machine-readable **Project State Manifest**, and use the bundled external validator to compute executable gate results.

Physical asset truth is also independent from planner state. Candidate Asset Registry is an assertion layer; `listing-evidence-auditor` reconciles it against real files, approval records, provenance, semantic role, and complete required asset sets. **Effective State** uses auditor evidence for downstream asset eligibility.

## Execution control

**Checkpointed execution by default.** Complete one numbered workflow stage to a reviewable state, present the stage output and open items, then stop at a **Major Stage Checkpoint** for the user's review before entering the next numbered stage.

Every numbered stage ends with a **Stage Completion Manifest**. It records planned deliverables, completed items, approved/locked items, `NEEDS REVISION`, missing items, blockers, open items, and `STAGE_STATUS = COMPLETE | PARTIAL | BLOCKED`.

A checkpoint applies to major workflow stages, not every trivial subtask. Within the current stage, finish the planned analysis or reviewable batch without asking permission after every search, table, frame, or tool call.

### Transition Command

Treat `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalent wording as a **Transition Command** unless the user explicitly says to keep improving the current artifact.

When a Transition Command is received:

1. stop further retries, regeneration, self-critique, or polishing immediately;
2. preserve the best current result;
3. mark unresolved quality/evidence issues as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, `UNVERIFIED`, `HUMAN_REVIEW_REQUIRED`, or Open Items as appropriate;
4. finalize the Stage Completion Manifest with its real status;
5. lock the current stage snapshot for downstream use;
6. enter the next numbered stage;
7. do not reopen the prior stage unless the user explicitly asks or new authoritative evidence invalidates it.

A Transition Command may lock a `PARTIAL` stage, but it never relabels it `COMPLETE` and never promotes unverified evidence to final-consumable.

### Retry Budget and anti-loop rule

For the same artifact and the same identified problem, allow at most **two autonomous attempts** without new user input or new evidence. After the Retry Budget is exhausted, stop regenerating/re-critiquing, show the current best result or blocked status, and wait at the Major Stage Checkpoint.

A Transition Command overrides the Retry Budget and advances immediately.

### Stage Lock and Change Impact

After approval or Transition Command, treat the stage as locked for normal downstream use. If newer authoritative product/commercial facts, strategy/offer decisions, asset/UI evidence, channel capability/reference, or claim/legal decisions materially change, create a **Change Impact Map** with `UNAFFECTED`, `REVIEW`, `INVALIDATED`, or `REOPEN`, preserve unaffected work, and rerun only impacted items.

### Autonomous Mode is opt-in

Full end-to-end autonomous execution is not the default. Autonomous Mode applies only when the user explicitly asks to skip checkpoints for the current request. It does not waive evidence, audit, delivery-integrity, approval-provenance, executable, claim, asset-slot, module-fit, parity, or frontend-fidelity gates.

## Evidence auditor delegation

Use the sibling `listing-evidence-auditor` at two mandatory points whenever final deliverables depend on real visual/UI/assets:

1. **post-6.5 evidence reconciliation** before final asset bindings are locked;
2. **Stage 8.5 Pre-Demo Evidence Audit** before Stage 9 Demo Assembly.

### Independent context rule

When the runtime supports an **independent context** / isolated subagent, dispatch the auditor with only the audit packet, exact asset paths, approval evidence, prior locked hashes, expected role/slot evidence, and required channel context. Do not send the planner's desired audit conclusion or prior PASS statements.

When no independent context is available, deterministic physical fingerprinting may still run, but same-agent semantic review cannot final-PASS. Semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless the user explicitly approves the exact physical hash + role + scope.

The main workflow may not overwrite auditor results. Auditor Evidence State has precedence over Candidate Asset Status for downstream eligibility.

## Configuration

Keep these fields separate:

```yaml
market:
  country: JP
locale:
  id: ja-JP
channel:
  type: project-defined
category: project-defined
offer: project-defined
page_targets: project-defined
output: project-defined
```

`market.country: JP` activates Japan-market evidence and verification. `locale.id: ja-JP` activates Japanese copy rules. An explicit project locale always wins.

## Mandatory rules

1. Start with Project Definition, Source Gate, and Fact Gate using the bundled files under `core/`.
2. Always read `references/delivery-integrity.md` and use Stage Completion Manifest, Asset Readiness Preflight, approved-asset/slot binding, module-fit, differentiator-proof, parity, and change-control rules.
3. Always read `references/executable-gates.md` for work that locks modules/assets or assembles a demo. Maintain one Project State Manifest and run `scripts/validate_project_state.py` for executable gates.
4. Keep `market`, `locale`, `channel`, `category`, `offer`, and `page_targets` separate.
5. Do not infer needs, preferences, scenes, keywords, visual settings, or message priorities from `JP` alone.
6. Build a Market Evidence Registry from current category-, channel-, audience-, offer-, and project-specific evidence.
7. Use `references/ja-jp-localization.md` only when consumer locale is `ja-JP`.
8. Load exactly one primary Japan channel profile plus confirmed retailer/campaign constraints.
9. Verify current channel rules, editable slots, account capabilities, content ownership, and mobile behavior before locking modules.
10. Keep Platform Capability evidence separate from Frontend Visual evidence. Official rules do not substitute for current consumer-facing frontend visual evidence.
11. When a channel-native demo is requested, read `references/channel-native-demo.md`, ask whether the user has a preferred Reference URL / ASIN / retailer/store page / screenshot set, and build a Channel Frontend Reference Pack.
12. A valid user-provided frontend reference is the candidate Primary Reference unless a concrete limitation is explained. If none is provided, research 1–3 current comparable pages and recommend one at the Stage 5.5 checkpoint.
13. Treat competitor pages as evidence of competitor execution, not proof of current account access or consumer preference.
14. Run `FRONTEND_FIDELITY_GATE` immediately before native Demo Assembly. On fail, deliver only a clearly named Content Review Demo.
15. Create an Asset Readiness Preflight in Stage 1 for asset classes expected later.
16. Stage 6.5 creates a **Candidate Asset Registry**; filenames, Asset IDs, agent-authored hashes, claimed role, provenance, and `LOCKED` are assertions, not final evidence.
17. Generate an audit packet and delegate to `listing-evidence-auditor`; recomputed physical SHA-256 and auditor effective status become authoritative for downstream asset eligibility.
18. User approval for evidence reconciliation binds to exact physical SHA-256 + approved role + approved slot/page/offer scope. Same-name replacement cannot inherit approval without exact hash match.
19. `EVIDENCE_RECONCILIATION_GATE` runs after Stage 6.5. Stage 7 may continue planning with explicit gaps, but it may not final-lock required Asset-to-Slot bindings using assets whose Effective State is not `VERIFIED` or `HUMAN_APPROVED`.
20. Build an Approved Asset Registry with stable Asset IDs. Material transformations/role changes create a derivative with provenance and new Asset ID.
21. Candidate `LOCKED` assets must still pass v0.2.5 `APPROVAL_PROVENANCE_GATE`; auditor evidence can invalidate them even when candidate state is internally consistent.
22. Build an Asset-to-Slot Contract and run `ASSET_SLOT_GATE`. When auditor evidence exists, auditor effective status + physical SHA-256 override candidate asset eligibility.
23. Material crop/recomposition/role-change derivatives require transform provenance and `TRANSFORM_AUTH_GATE`; deterministic execution is not authorization.
24. Evaluate `CONTENT_COVERAGE` and `MODULE_FIT_GATE` separately.
25. Do not mechanically convert independent static boards into carousel/slides during Demo Assembly. Native interaction logic/content packing must be planned in Stage 7/7.5.
26. Lock Stage 7 module architecture into `locked_module_plan` with canonical `plan_hash`; Stage 9 must consume the exact hash.
27. Run `CHANNEL_MODULE_BUDGET_GATE` from packaged channel policy before locking module plan. Project state may lower but not raise packaged ceilings.
28. Run `MODULE_ORIGIN_GATE` during Stage 9. Every implemented module must originate in the exact locked plan; unplanned modules or type/interaction drift fail.
29. Run `DIFFERENTIATOR_PROOF_GATE` for visualizable P0 purchase reasons.
30. Stage 8.5 reruns `listing-evidence-auditor` on final produced/edited files, derivatives, exact physical hashes, approval carryover, visual role, slot scope, and complete required asset set.
31. `PRE_DEMO_ASSET_GATE` must PASS before Stage 9. Every required asset in the locked Demo plan must be `VERIFIED` or `HUMAN_APPROVED`; one invalidated/unverified member blocks final channel-native assembly.
32. Before a demo is called complete, run `DELIVERY_PARITY_GATE` against the locked plan for module/slot, interaction, Asset IDs, dimensions/aspect, coverage, page/offer ownership, and channel region.
33. Ignore agent-authored PASS fields such as `declared_gate_results`. Executable PASS is produced only by the external validator and required auditor evidence.
34. If Project State validator or required audit cannot execute, applicable gates remain `UNVERIFIED`; the agent must not manually convert them to PASS.
35. Keep volatile laws, platform rules, certifications, pricing, availability, service terms, and claims in `PENDING CLAIM` until authoritative evidence supports release.
36. Keep reusable Japan rules category-neutral. Product-category conclusions belong in project/category evidence, not country defaults.
37. AI may create environments/concept backgrounds. Product geometry, UI, packaging, ports, controls, accessories, and functional proof require real assets or explicit provisional labels.
38. Every module must pass the Visual Evidence Matrix: `message → visual subject → evidence object → asset`.
39. Preserve Page Boundary Matrix, Review Mode, Consumer Mode, Mobile QA, asset-path QA, frontend fidelity QA, delivery-integrity QA, evidence-auditor results, and executable-gate results.
40. Review Mode is overlay-only and must not redesign/distort verified Consumer Mode channel layout.
41. Keep confidential brand/product/price/design/approval/unreleased information outside this public repository.

## Execution order

```text
0 Project Definition
1 Source Intake + Asset Readiness Preflight
2 Source Normalization & Coverage Gate
3 Fact Lock
4 Consumer Strategy
4.2 Japan Market & Localization Enrichment
5 Message Architecture
5.5 Channel Template & Frontend Mapping + Channel Capability State
6 Channel-specific Listing IA
6.5A Candidate Asset Intake / Registry
6.5B listing-evidence-auditor → EVIDENCE_RECONCILIATION_GATE → Effective State
7 Channel Slot / Module Planning + Asset-to-Slot Contract + Module Budget Validation
7.5 Visual Production Brief + Transform Authorization
8 Visual Production + Visual Evidence / Differentiator Proof QA
8.5 listing-evidence-auditor Pre-Demo Evidence Audit → PRE_DEMO_ASSET_GATE
9 Channel-native Demo Assembly + Module Origin / Asset / Parity Validation
10 Final QA + Claim Gate + Review Mode
```

Default behavior: execute the current numbered stage, emit its Stage Completion Manifest, stop at its Major Stage Checkpoint, and wait for review. Enter the next stage only after approval/Transition Command unless explicitly in Autonomous Mode.

## Files to read

Always read:

- `core/manifest.yaml`
- `core/workflow.md`
- `core/contracts.md`
- `core/market-research.md`
- `core/visual-evidence.md`
- `core/qa.md`
- `references/delivery-integrity.md`
- `references/executable-gates.md`
- `references/japan-market-evidence.md`
- `references/japan-claim-compliance.md`
- `references/qa.md`

Read conditionally:

- `references/channel-native-demo.md` whenever channel-native frontend demo is requested;
- `core/localization.md` and `references/ja-jp-localization.md` when locale work is required;
- one file under `profiles/channels/` for selected primary channel;
- `core/profiles/categories/_template.md` for project-specific category overlays;
- sibling `.agents/skills/listing-evidence-auditor/SKILL.md` and `references/audit-contract.md` at Stage 6.5B and Stage 8.5.

## Required outputs

Before declaring workflow complete, produce:

- Project Definition and selected profiles;
- Source Registry and coverage status;
- Asset Readiness Preflight;
- Fact Ledger, Conflict Ledger, Missing Evidence, Claim Readiness, Gate Result;
- Consumer Strategy and Market Evidence Registry;
- Page Target / Product Boundary Matrix;
- Message Architecture and Message-to-Slot Matrix;
- Candidate Asset Registry + audit packet;
- Auditor Evidence State / Verified Asset Registry / Effective State;
- `EVIDENCE_RECONCILIATION_GATE` result;
- Asset-to-Slot Contract;
- Channel Slot / Module Plan;
- `CONTENT_COVERAGE` + `MODULE_FIT_GATE`;
- Visual Production Brief, Visual Evidence Matrix, Differentiator Proof Matrix, `DIFFERENTIATOR_PROOF_GATE`;
- Stage 8.5 audit result + `PRE_DEMO_ASSET_GATE`;
- Project State Manifest;
- external-validator results for `CHANNEL_MODULE_BUDGET_GATE`, `APPROVAL_PROVENANCE_GATE`, `MODULE_ORIGIN_GATE`, `TRANSFORM_AUTH_GATE`, `EVIDENCE_RECONCILIATION_GATE`, `ASSET_SLOT_GATE`, `PRE_DEMO_ASSET_GATE`, `DELIVERY_PARITY_GATE`;
- interactive demo or production-ready module specification;
- Stage Completion Manifest for every completed/advanced numbered stage;
- Change Impact Map whenever authoritative evidence invalidated locked work;
- Product, Claim, Channel, Japan/Locale, Visual, Mobile, Technical, Frontend Fidelity, Delivery Integrity, Evidence Auditor, Executable Gate, and Review Mode QA results.

For channel-native demo also produce Platform Capability Map, Channel Frontend Reference Pack, `FRONTEND_FIDELITY_GATE`, and either verified channel-native demo or Content Review Demo fallback.

## Quality gate

Repository/Codex distribution:

```bash
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
```

Project state:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

The compatibility single-Skill ZIP cannot claim an independent semantic evidence audit. In single-context use, unresolved semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless the user explicitly approves exact hash + role/scope.
