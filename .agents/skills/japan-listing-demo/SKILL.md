---
name: japan-listing-demo
description: Use when planning, reviewing, or producing Japan-market product listing strategy, enhanced content, visual briefs, or interactive review demos across Japanese ecommerce channels, DTC pages, and retailer PDPs from product evidence, VOC, competitor pages, research, or design assets.
---

# Japan Listing Demo

## Distribution

This is a **standalone distribution**. It includes a validated snapshot of the generic listing workflow plus Japan market, localization, channel, claim-review, frontend-reference, and QA rules. Team users install and invoke only `japan-listing-demo`.

The upstream source is recorded in `core/manifest.yaml` for maintainers. It is not a runtime dependency.

## Core principle

Build one evidence-governed Product Truth and Product Strategy, then adapt them to the requested Japan market, locale, channel, category, offer, and page targets. A country label is not a consumer persona or product-category playbook.

When the output is a **channel-native demo**, do not design the channel shell from memory. Verify the current consumer-facing frontend first, lock a Primary Reference, and reproduce the evidenced channel structure before inserting project content.

## Execution control

**Checkpointed execution by default.** Complete one numbered workflow stage to a reviewable state, present the stage output and open items, then stop at a **Major Stage Checkpoint** for the user's review before entering the next numbered stage.

A checkpoint applies to major workflow stages, not every trivial subtask. Within the current stage, finish the planned analysis or reviewable batch without asking permission after every search, table, frame, or tool call.

### Transition Command

Treat an explicit user command such as `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, or equivalent wording as a **Transition Command** unless the user explicitly says to keep improving the current artifact.

When a Transition Command is received:

1. stop further retries, regeneration, self-critique, or polishing of the current stage immediately;
2. preserve the best current result;
3. mark unresolved quality or evidence issues as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items as appropriate;
4. lock the current stage snapshot for downstream use;
5. enter the next numbered workflow stage;
6. do not reopen the prior stage unless the user explicitly asks to return or new authoritative evidence invalidates the locked result.

A Transition Command has higher priority than the stage's normal completeness preference. Never fabricate missing evidence merely to make a stage look complete.

### Retry Budget and anti-loop rule

For the same artifact and the same identified problem, the agent may make **at most two autonomous attempts** without new user input or new evidence. After the Retry Budget is exhausted:

- stop regenerating or re-critiquing the same artifact;
- show the current best result or mark the artifact blocked;
- explain the unresolved issue briefly;
- wait at the current Major Stage Checkpoint for user direction.

If the user gives a Transition Command at any time, the Retry Budget is irrelevant: advance immediately. A new instruction that materially changes the goal, evidence, or creative direction may start a new attempt budget.

### Stage Lock

After the user approves a stage or sends a Transition Command, treat that stage as locked. Downstream work may reference its open items, but must not silently re-run or redesign the locked stage. Reopen it only on explicit user request or when new authoritative evidence creates a material conflict.

### Autonomous Mode is opt-in

Full end-to-end autonomous execution is **not the default**. Use **Autonomous Mode** only when the user explicitly asks to skip stage checkpoints for the current request, for example: “这次不用每一步等我，直接做到最终 Demo”. Autonomous Mode applies only to that request and does not change the default behavior of future work.

Autonomous Mode does not waive evidence gates. A channel-native demo still requires a Channel Frontend Reference Pack and `FRONTEND_FIDELITY_GATE`.

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
2. Keep `market`, `locale`, `channel`, `category`, `offer`, and `page_targets` separate.
3. Do not infer needs, preferences, scenes, keywords, visual settings, or message priorities from `JP` alone.
4. Build a Market Evidence Registry from current category-, channel-, audience-, offer-, and project-specific evidence.
5. Use `references/ja-jp-localization.md` only when the requested consumer locale is `ja-JP`.
6. Load exactly one primary Japan channel profile, plus confirmed retailer or campaign constraints.
7. Verify current channel rules, editable slots, account capabilities, content ownership, and mobile behavior before locking modules.
8. Keep **Platform Capability** evidence separate from **Frontend Visual** evidence. Official rules do not substitute for current consumer-facing frontend visual evidence.
9. When a channel-native demo is requested, read `references/channel-native-demo.md`, ask whether the user has a preferred **Reference URL** / ASIN / retailer page / store page / screenshot set, and build a **Channel Frontend Reference Pack**.
10. A user-provided current frontend reference is the candidate **Primary Reference** unless a concrete limitation is explained. If none is provided, research 1–3 current comparable consumer-facing pages and recommend a Primary Reference at the Stage 5.5 checkpoint.
11. Treat competitor pages as evidence of competitor execution, not proof of current account access or consumer preference. A competitor page may be a frontend reference only for the specific shell evidence it visibly supports.
12. Run `FRONTEND_FIDELITY_GATE` immediately before native Demo Assembly. If it fails, deliver only a clearly named **Content Review Demo**; do not fabricate or label an invented shell as a channel-native demo.
13. Keep laws, platform rules, certifications, pricing, availability, service terms, and volatile capabilities in `PENDING CLAIM` until authoritative evidence supports release.
14. Keep reusable Japan rules category-neutral. Product-category conclusions belong in `core/profiles/categories/_template.md`-based project overlays or current Project Evidence.
15. AI may create environments and concept backgrounds. Product geometry, UI, packaging, ports, controls, accessories, and functional proof require real assets or explicit provisional labels.
16. Every module must pass the Visual Evidence Matrix: `message → visual subject → evidence object → asset`.
17. Preserve Page Boundary Matrix, Review Mode, Consumer Mode, Mobile QA, asset-path QA, and channel frontend fidelity QA.
18. Review Mode is an overlay only. It must not redesign or distort the verified Consumer Mode channel layout.
19. Keep confidential brand, product, price, design, approval, and unreleased information outside this public repository.
20. Apply the Execution control rules above: checkpoint after each numbered stage by default; obey Transition Commands immediately; enforce the Retry Budget on repeated artifact problems.

## Execution order

Read the bundled core and only the Japan files needed for the project:

```text
0 Project Definition
1 Source Intake
2 Source Normalization & Coverage Gate
3 Fact Lock
4 Consumer Strategy
4.2 Japan Market & Localization Enrichment
5 Message Architecture
5.5 Channel Template & Frontend Mapping
6 Channel-specific Listing IA
6.5 Asset Intake & Audit
7 Channel Slot / Module Planning
7.5 Visual Production Brief
8 Visual Production + Visual Evidence QA
9 Channel-native Demo Assembly
10 Final QA + Claim Gate + Review Mode
```

Default behavior: execute the current numbered stage, stop at its Major Stage Checkpoint, and wait for review. Enter the next numbered stage only after approval or a Transition Command. Autonomous Mode may skip these pauses only when explicitly requested for the current task.

## Files to read

Always read:

- `core/manifest.yaml`
- `core/workflow.md`
- `core/contracts.md`
- `core/market-research.md`
- `core/visual-evidence.md`
- `core/qa.md`
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
- Fact Ledger, Conflict Ledger, Missing Evidence, Claim Readiness, and Gate Result;
- Consumer Strategy and Market Evidence Registry;
- Page Target / Product Boundary Matrix;
- Message Architecture and Message-to-Slot Matrix;
- Asset Manifest and Asset Gap Analysis;
- Channel Slot / Module Plan;
- Visual Production Brief and Visual Evidence Matrix;
- interactive demo or production-ready module specification;
- Product, Claim, Channel, Japan/Locale, Visual, Mobile, Technical, Frontend Fidelity, and Review Mode QA results.

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
