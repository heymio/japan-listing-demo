# japan-listing-demo

`japan-listing-demo` is a **standalone public Skill** for turning product evidence into Japan-market listing strategy, channel-specific content architecture, visual briefs, and channel-native interactive review demos.

## One repository, one ZIP, one Skill

Japan-team users need only this repository or its packaged ZIP:

```text
japan-listing-demo
```

They do not install a separate generic core. The validated core workflow is bundled under `.agents/skills/japan-listing-demo/core/`.

Invoke:

```text
$japan-listing-demo
```

## Checkpointed execution by default

The Skill uses **Major Stage Checkpoints** by default.

It completes one numbered workflow stage, emits a **Stage Completion Manifest**, presents the reviewable result and open items, and waits for the user's check before entering the next numbered stage.

The Stage Completion Manifest distinguishes:

```text
planned
completed
approved / locked
needs revision
missing
blocked
open items
STAGE_STATUS = COMPLETE / PARTIAL / BLOCKED
```

A completed subset does not make the whole stage complete.

### Moving to the next stage

When the user says `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, or equivalent wording, that is a **Transition Command** unless the user explicitly asks to keep improving the current artifact.

A Transition Command means:

- stop retrying or regenerating the current frame/subtask;
- keep the best current version;
- record unresolved items;
- lock the real Stage Completion Manifest status;
- move to the next numbered stage immediately.

A `PARTIAL` stage stays `PARTIAL`; advancing does not turn it into `COMPLETE`.

### Anti-loop Retry Budget

For the same artifact and same identified problem, the agent gets at most **two autonomous attempts** without new user input or new evidence.

## Delivery integrity: don't leak, substitute, or fake completion

The Skill reads `references/delivery-integrity.md` and enforces the following controls.

### Asset Readiness Preflight

Stage 1 records which asset classes later work will require, which are already received, which are missing, and when they become blocking. Critical product/UI/channel evidence should not be discovered missing only at visual or Demo Assembly stage.

### Approved Asset Registry

Once an asset is approved, it receives a stable **Asset ID** with canonical source, dimensions/aspect, page/offer scope, allowed slots, approval status, derivative provenance, and transform rule.

Approved assets are stable downstream inputs. A material crop, recomposition, text/background change, or role change creates a derivative with a new Asset ID and approval status.

### Asset-to-Slot Contract

Every final slot/module binds to a required Asset ID, page/offer, dimensions/aspect, crop/transform rule, interaction, and ownership.

Run:

```text
ASSET_SLOT_GATE
```

before final adaptation and Demo Assembly.

The workflow must not silently substitute a Gallery asset with an enhanced-content asset, or vice versa, merely because the crop appears to fit.

### Coverage and native module fit are separate

Run both:

```text
CONTENT_COVERAGE
MODULE_FIT_GATE
```

A plan can cover all required topics and still have the wrong native module architecture.

The workflow must not take independent static boards and mechanically convert them into carousel/slides during Demo Assembly. Carousel, hotspot, video, comparison, accordion, or other interaction logic is planned in Stage 7 and Stage 7.5 before production.

### P0 differentiator visual proof

Run:

```text
DIFFERENTIATOR_PROOF_GATE
```

Visualizable P0 purchase reasons should have direct visual proof, or an explicitly approved alternative proof strategy. Generic attractive lifestyle imagery is not enough by itself.

### Planned-to-Implemented parity

Before a demo is called complete, run:

```text
DELIVERY_PARITY_GATE
```

It compares the locked plan against actual implementation for slot/module, interaction, source Asset IDs, dimensions/aspect, message coverage, page/offer ownership, and channel region.

A working HTML file does not prove parity.

### Change control

If newer authoritative evidence invalidates an earlier locked assumption, build a **Change Impact Map** and classify downstream work:

```text
UNAFFECTED
REVIEW
INVALIDATED
REOPEN
```

Preserve unaffected work and reopen only impacted stages/items.

## Channel-native demos require frontend references

A channel capability map is not enough to make a native-looking demo. Before generating an Amazon.co.jp, Rakuten, Yahoo! Shopping, retailer, or DTC **channel-native demo**, the workflow must establish the current **consumer-facing frontend**.

At Stage 5.5 the agent must:

1. verify **Platform Capability**;
2. ask whether the user has a preferred current **Reference URL**, ASIN, retailer/store page, approved design-system reference, or screenshot set;
3. if supplied, use it as the candidate **Primary Reference**;
4. if none is supplied, research 1–3 current comparable consumer-facing pages and recommend one Primary Reference;
5. visually inspect/capture material desktop/mobile shell, section order, interactions, and ownership;
6. produce a **Channel Frontend Reference Pack**.

**Official rules do not substitute for frontend visual evidence.**

Immediately before Stage 9, the Skill runs:

```text
FRONTEND_FIDELITY_GATE
```

If it fails, the allowed fallback is:

```text
Content Review Demo
```

The Skill must not invent generic marketplace chrome or custom branded navigation and label it a channel-native PDP/demo.

## Included capabilities

- Project Definition, Source Gate, and Fact Lock
- Asset Readiness Preflight
- Consumer Strategy and Market Evidence Registry
- Page Boundary Matrix and Message Architecture
- Platform Capability Map
- Channel Frontend Reference Pack and Frontend Fidelity Gate
- Approved Asset Registry and Asset-to-Slot Contract
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE`
- Visual Evidence Matrix and `DIFFERENTIATOR_PROOF_GATE`
- `DELIVERY_PARITY_GATE`
- Stage Completion Manifest and Change Impact Map
- channel-specific slot/module planning and interactive review demos
- Claim, Japan-market, locale, channel, frontend-fidelity, mobile, technical, delivery-integrity, Execution Flow, and Review Mode QA
- `ja-JP` localization guidance
- Japan channel profiles for Amazon.co.jp, Rakuten, Yahoo! Shopping, DTC, and retailer PDPs

## Evidence boundary

This repository does not assume a product category, fixed Japan consumer persona, predefined needs/scenes/keywords, one marketplace template, or private company facts.

Actual strategy comes from:

```text
category
× channel
× audience
× offer
× current project evidence
```

Actual channel-native shell comes from:

```text
current channel capability evidence
+
current consumer-facing frontend visual evidence
+
locked Primary Reference
```

## Quick start

```yaml
market:
  country: JP
locale:
  id: ja-JP
channel:
  type: amazon-jp
category: project-defined
offer: project-defined
page_targets:
  - single
output:
  - strategy
  - module-plan
  - interactive-demo
```

Prompt:

```text
Use the standalone japan-listing-demo Skill.
按默认 checkpoint workflow 执行：每个 numbered stage 做完后给我 Stage Completion Manifest 和 review，再进入下一步。
如果我说“继续 / 下一步 / go next”，立即锁定当前真实状态并推进，不要继续重做当前 frame。
同一个 frame / 同一个问题最多自动重试两次。
提前做 Asset Readiness Preflight；已通过的素材必须用稳定 Asset ID 绑定到正确 slot，不能把别的模块素材裁一裁就替换。
CONTENT_COVERAGE 和 MODULE_FIT_GATE 分开检查；不要在 Demo 阶段把静态图机械切成 slide/carousel。
Demo 前跑 ASSET_SLOT_GATE、DIFFERENTIATOR_PROOF_GATE、DELIVERY_PARITY_GATE。
如果最终要生成 channel-native Demo，在 Stage 5.5 先问我是否有参考链接 / ASIN / 页面截图；没有的话自己研究 1–3 个当前参考并让我确认 Primary Reference。
FRONTEND_FIDELITY_GATE 通过前不要生成或命名为原生渠道 PDP Demo。
```

## Skill layout

```text
.agents/skills/japan-listing-demo/
├── SKILL.md
├── core/
├── references/
│   ├── channel-native-demo.md
│   └── delivery-integrity.md
├── profiles/channels/
├── evals/
└── scripts/
```

## Validation and packaging

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

## Optional private use

A company may add a separate private brand overlay for confidential product facts, pricing, claims, Figma links, approvals, or unreleased assets. That overlay is optional; public Japan-team use remains one Skill.

## Maintenance

The bundled core snapshot is sourced from `heymio/gtm-listing-demo` v0.2.0, commit `b882526f5a683235d30f562006cf1984a9f0d9f9`, with distribution-level execution-control, channel-frontend, and delivery-integrity patches documented in the Japan Skill. This provenance is for maintainers only and creates no runtime dependency.

See [`docs/install.md`](docs/install.md).

## Version

`0.2.4`

## License

MIT.
