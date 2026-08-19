---
name: japan-listing-demo
description: Use when planning, reviewing, or producing Japan-market product listing strategy, enhanced content, visual briefs, or interactive review demos across Japanese ecommerce channels, DTC pages, and retailer PDPs from product evidence, VOC, competitor pages, research, or design assets.
---

# Japan Listing Demo

## Distribution

This is a **standalone distribution**. It includes a validated snapshot of the generic listing workflow plus Japan market, localization, channel, claim-review, and QA rules. Team users install and invoke only `japan-listing-demo`.

The upstream source is recorded in `core/manifest.yaml` for maintainers. It is not a runtime dependency.

## Core principle

Build one evidence-governed Product Truth and Product Strategy, then adapt them to the requested Japan market, locale, channel, category, offer, and page targets. A country label is not a consumer persona or product-category playbook.

## Execution control

**Continuous execution by default.** When the user asks for an end deliverable such as a strategy, module plan, visual plan, or Listing Demo, continue automatically through all non-blocked stages needed to reach that deliverable.

A **Gate is not a pause point**. Source Gate, Fact Gate, Strategy review, Channel Capability checks, Visual Evidence QA, and other gates are internal validation checkpoints. Report their status when useful, but do not stop and wait for a reply after a normal stage.

Do not ask the user to reply “继续”, “go”, “确认”, “可以继续”, or an equivalent approval phrase merely to enter the next stage.

Progress updates are non-blocking. The agent may state what has been completed and what comes next, then continue automatically in the same workflow unless a pause condition applies.

Non-blocking gaps do not stop the project. Record them as `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items and continue every downstream output that remains valid.

Pause only when one of these applies:

1. **Explicit checkpoint:** the user explicitly asks to stop at a stage, review point, or deliverable before continuing.
2. **Hard Blocker:** continuing would make the next output materially invalid or misleading because a critical decision cannot be resolved from available evidence. Examples include conflicting authoritative facts required by the next output, an unresolved channel/offer/page-target choice that changes the page architecture, or missing real product/UI evidence where a substitute would falsely represent the product.

A normal review opportunity is not a Hard Blocker. If the user has not requested a checkpoint, produce a reviewable snapshot and continue automatically.

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
8. Treat competitor pages as evidence of competitor execution, not proof of current account access or consumer preference.
9. Keep laws, platform rules, certifications, pricing, availability, service terms, and volatile capabilities in `PENDING CLAIM` until authoritative evidence supports release.
10. Keep reusable Japan rules category-neutral. Product-category conclusions belong in `core/profiles/categories/_template.md`-based project overlays or current Project Evidence.
11. AI may create environments and concept backgrounds. Product geometry, UI, packaging, ports, controls, accessories, and functional proof require real assets or explicit provisional labels.
12. Every module must pass the Visual Evidence Matrix: `message → visual subject → evidence object → asset`.
13. Preserve Page Boundary Matrix, Review Mode, Consumer Mode, Mobile QA, and asset-path QA.
14. Keep confidential brand, product, price, design, approval, and unreleased information outside this public repository.
15. Apply the Execution control rules above: normal gates do not require user approval, while explicit user checkpoints must be respected.

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
5.5 Verified Channel Template Mapping
6 Channel-specific Listing IA
6.5 Asset Intake & Audit
7 Channel Slot / Module Planning
7.5 Visual Production Brief
8 Visual Production + Visual Evidence QA
9 Interactive Demo Assembly
10 Final QA + Claim Gate + Review Mode
```

Execute this sequence continuously until the requested deliverable is reached, except for an explicit checkpoint or Hard Blocker.

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
- Product, Claim, Channel, Japan/Locale, Visual, Mobile, Technical, and Review Mode QA results.

## Quality gate

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

When revising this Skill, rerun the scenarios under both `core/evals/` and `evals/`.
