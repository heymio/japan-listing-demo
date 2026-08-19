---
name: japan-listing-demo
description: Use when planning, reviewing, or producing Japan-market product listing strategy, enhanced content, visual briefs, or interactive review demos across Japanese ecommerce channels, DTC pages, and retailer PDPs from product evidence, VOC, competitor pages, research, or design assets.
---

# Japan Listing Demo

## Distribution

This is a **standalone distribution**. It includes a validated snapshot of the generic listing workflow plus Japan market, localization, channel, claim-review, frontend-reference, delivery-integrity, and QA rules. Team users install and invoke only `japan-listing-demo`.

The upstream source is recorded in `core/manifest.yaml` for maintainers. It is not a runtime dependency.

## Core principle

Build one evidence-governed Product Truth and Product Strategy, then adapt them to the requested Japan market, locale, channel, category, offer, and page targets. A country label is not a consumer persona or product-category playbook.

When the output is a **channel-native demo**, do not design the channel shell from memory. Verify the current consumer-facing frontend first, lock a Primary Reference, and reproduce the evidenced channel structure before inserting project content.

Do not treat a polished partial artifact as a complete stage. Do not silently replace approved assets downstream. Content coverage, native module fit, visual proof strength, and implemented parity are separate checks.

## Execution control

**Checkpointed execution by default.** Complete one numbered workflow stage to a reviewable state, present the stage output and open items, then stop at a **Major Stage Checkpoint** for the user's review before entering the next numbered stage.

Every numbered stage ends with a **Stage Completion Manifest**. It records planned deliverables, completed items, approved/locked items, `NEEDS REVISION`, missing items, blockers, open items, and `STAGE_STATUS = COMPLETE | PARTIAL | BLOCKED`.

A checkpoint applies to major workflow stages, not every trivial subtask. Within the current stage, finish the planned analysis or reviewable batch without asking permission after every search, table, frame, or tool call.

### Transition Command

Treat an explicit user command such as `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, or equivalent wording as a **Transition Command** unless the user explicitly says to keep improving the current artifact.

When a Transition Command is received:

1. stop further retries, regeneration, self-critique, or polishing of the current stage immediately;
2. preserve the best current result;
3. mark unresolved quality or evidence issues as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items as appropriate;
4. finalize the Stage Completion Manifest with its real status;
5. lock the current stage snapshot for downstream use;
6. enter the next numbered workflow stage;
7. do not reopen the prior stage unless the user explicitly asks to return or new authoritative evidence invalidates the locked result.

A Transition Command may lock a `PARTIAL` stage, but it never relabels it `COMPLETE`.

### Retry Budget and anti-loop rule

For the same artifact and the same identified problem, the agent may make **at most two autonomous attempts** without new user input or new evidence. After the Retry Budget is exhausted:

- stop regenerating or re-critiquing the same artifact;
- show the current best result or mark the artifact blocked;
- explain the unresolved issue briefly;
- wait at the current Major Stage Checkpoint for user direction.

If the user gives a Transition Command at any time, the Retry Budget is irrelevant: advance immediately. A new instruction that materially changes the goal, evidence, or creative direction may start a new attempt budget.

### Stage Lock and Change Impact

After the user approves a stage or sends a Transition Command, treat that stage as locked for normal downstream use.

If a newer authoritative fact, approved strategy/offer decision, approved asset/UI source, channel capability/reference, or claim/legal decision materially changes, create a **Change Impact Map**. Classify dependent outputs as `UNAFFECTED`, `REVIEW`, `INVALIDATED`, or `REOPEN`, preserve unaffected work, and rerun only impacted stages/items.

Do not ignore new evidence because a stage was locked, and do not restart the whole project when dependency analysis shows unaffected work remains valid.

### Autonomous Mode is opt-in

Full end-to-end autonomous execution is **not the default**. Use **Autonomous Mode** only when the user explicitly asks to skip stage checkpoints for the current request, for example: “这次不用每一步等我，直接做到最终 Demo”. Autonomous Mode applies only to that request and does not change the default behavior of future work.

Autonomous Mode does not waive evidence gates or delivery-integrity gates. A channel-native demo still requires a Channel Frontend Reference Pack and `FRONTEND_FIDELITY_GATE`.

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
3. Keep `market`, `locale`, `channel`, `category`, `offer`, and `page_targets` separate.
4. Do not infer needs, preferences, scenes, keywords, visual settings, or message priorities from `JP` alone.
5. Build a Market Evidence Registry from current category-, channel-, audience-, offer-, and project-specific evidence.
6. Use `references/ja-jp-localization.md` only when the requested consumer locale is `ja-JP`.
7. Load exactly one primary Japan channel profile, plus confirmed retailer or campaign constraints.
8. Verify current channel rules, editable slots, account capabilities, content ownership, and mobile behavior before locking modules.
9. Keep **Platform Capability** evidence separate from **Frontend Visual** evidence. Official rules do not substitute for current consumer-facing frontend visual evidence.
10. When a channel-native demo is requested, read `references/channel-native-demo.md`, ask whether the user has a preferred **Reference URL** / ASIN / retailer page / store page / screenshot set, and build a **Channel Frontend Reference Pack**.
11. A user-provided current frontend reference is the candidate **Primary Reference** unless a concrete limitation is explained. If none is provided, research 1–3 current comparable consumer-facing pages and recommend a Primary Reference at the Stage 5.5 checkpoint.
12. Treat competitor pages as evidence of competitor execution, not proof of current account access or consumer preference. A competitor page may be a frontend reference only for the specific shell evidence it visibly supports.
13. Run `FRONTEND_FIDELITY_GATE` immediately before native Demo Assembly. If it fails, deliver only a clearly named **Content Review Demo**; do not fabricate or label an invented shell as a channel-native demo.
14. Create an **Asset Readiness Preflight** in Stage 1 for asset classes the current project is expected to need. Do not wait until visual/demo stages to discover critical evidence is missing.
15. Build an **Approved Asset Registry** with stable Asset IDs. Approved assets are stable downstream inputs; material transformations or role changes create a derivative with provenance and a new Asset ID.
16. Build an **Asset-to-Slot Contract** and run `ASSET_SLOT_GATE`. Do not substitute assets across gallery/enhanced-content/offer/page roles merely because they fit visually.
17. Evaluate `CONTENT_COVERAGE` and `MODULE_FIT_GATE` separately. Full topic coverage does not prove that a carousel, hotspot, video, comparison, or other native module is the right structure.
18. Do not mechanically convert independent static boards into carousel/slides during Demo Assembly. Native interaction logic and content packing must be planned in Stage 7 and Stage 7.5.
19. Run `DIFFERENTIATOR_PROOF_GATE` for visualizable P0 purchase reasons. Attractive generic lifestyle imagery does not substitute for direct proof.
20. Before a demo is called complete, run `DELIVERY_PARITY_GATE` against the locked plan for module/slot, interaction, Asset IDs, dimensions/aspect, coverage, page/offer ownership, and channel region.
21. Keep laws, platform rules, certifications, pricing, availability, service terms, and volatile capabilities in `PENDING CLAIM` until authoritative evidence supports release.
22. Keep reusable Japan rules category-neutral. Product-category conclusions belong in `core/profiles/categories/_template.md`-based project overlays or current Project Evidence.
23. AI may create environments and concept backgrounds. Product geometry, UI, packaging, ports, controls, accessories, and functional proof require real assets or explicit provisional labels.
24. Every module must pass the Visual Evidence Matrix: `message → visual subject → evidence object → asset`.
25. Preserve Page Boundary Matrix, Review Mode, Consumer Mode, Mobile QA, asset-path QA, channel frontend fidelity QA, and delivery-integrity QA.
26. Review Mode is an overlay only. It must not redesign or distort the verified Consumer Mode channel layout.
27. Keep confidential brand, product, price, design, approval, and unreleased information outside this public repository.
28. Apply the Execution control rules above: checkpoint after each numbered stage by default; obey Transition Commands immediately; enforce the Retry Budget on repeated artifact problems; do not turn `PARTIAL` into `COMPLETE`.

## Execution order

Read the bundled core and only the Japan files needed for the project:

```text
0 Project Definition
1 Source Intake + Asset Readiness Preflight
2 Source Normalization & Coverage Gate
3 Fact Lock
4 Consumer Strategy
4.2 Japan Market & Localization Enrichment
5 Message Architecture
5.5 Channel Template & Frontend Mapping
6 Channel-specific Listing IA
6.5 Asset Intake & Approved Asset Registry
7 Channel Slot / Module Planning + Asset-to-Slot Contract
7.5 Visual Production Brief
8 Visual Production + Visual Evidence / Differentiator Proof QA
9 Channel-native Demo Assembly + Asset/Parity Gates
10 Final QA + Claim Gate + Review Mode
```

Default behavior: execute the current numbered stage, emit its Stage Completion Manifest, stop at its Major Stage Checkpoint, and wait for review. Enter the next numbered stage only after approval or a Transition Command. Autonomous Mode may skip these pauses only when explicitly requested for the current task.

## Files to read

Always read:

- `core/manifest.yaml`
- `core/workflow.md`
- `core/contracts.md`
- `core/market-research.md`
- `core/visual-evidence.md`
- `core/qa.md`
- `references/delivery-integrity.md`
- `references/japan-market-evidence.md`
- `references/japan-claim-compliance.md`
- `references/qa.md`

Read conditionally:

- `references/channel-native-demo.md` whenever a channel-native frontend demo is requested;
- `core/localization.md` and `references/ja-jp-localization.md` when locale work is required;
- one file under `profiles/channels/` for the selected primary channel;
- `core/profiles/categories/_template.md` when creating a project-specific category overlay.

## Required outputs

Before declaring the workflow complete, produce:

- Project Definition and selected profiles;
- Source Registry and coverage status;
- Asset Readiness Preflight;
- Fact Ledger, Conflict Ledger, Missing Evidence, Claim Readiness, and Gate Result;
- Consumer Strategy and Market Evidence Registry;
- Page Target / Product Boundary Matrix;
- Message Architecture and Message-to-Slot Matrix;
- Approved Asset Registry, Asset Manifest, and Asset Gap Analysis;
- Asset-to-Slot Contract and `ASSET_SLOT_GATE` result;
- Channel Slot / Module Plan;
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE` results;
- Visual Production Brief, Visual Evidence Matrix, Differentiator Proof Matrix, and `DIFFERENTIATOR_PROOF_GATE` result;
- interactive demo or production-ready module specification;
- `DELIVERY_PARITY_GATE` result;
- Stage Completion Manifest for every completed/advanced numbered stage;
- Change Impact Map whenever authoritative evidence invalidated locked work;
- Product, Claim, Channel, Japan/Locale, Visual, Mobile, Technical, Frontend Fidelity, Delivery Integrity, and Review Mode QA results.

When a channel-native demo is requested, also produce:

- Platform Capability Map;
- **Channel Frontend Reference Pack** with Primary Reference, desktop/mobile evidence, ownership, and fidelity status;
- `FRONTEND_FIDELITY_GATE` result;
- either a verified channel-native demo or a clearly labeled **Content Review Demo** fallback.

## Quality gate

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

When revising this Skill, rerun the scenarios under both `core/evals/` and `evals/`.
