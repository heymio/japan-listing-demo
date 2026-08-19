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

It completes one numbered workflow stage, presents the reviewable result and open items, and waits for the user's check before entering the next numbered stage. It does **not** run the entire workflow to a final Demo unless the user explicitly opts into Autonomous Mode.

Within the current stage, the agent should finish a useful batch rather than pausing after every minor search, tool call, frame, or image.

### Moving to the next stage

When the user says `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, or equivalent wording, that is a **Transition Command** unless the user explicitly asks to keep improving the current artifact.

A Transition Command means:

- stop retrying or regenerating the current frame/subtask;
- keep the best current version;
- mark unresolved items as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items;
- lock the current stage snapshot;
- move to the next numbered stage immediately.

The agent must not require a second “继续” after the user has already asked to move on.

### Anti-loop Retry Budget

For the same artifact and the same identified problem, the agent gets at most **two autonomous attempts** without new user input or new evidence. After that it must stop regenerating, show the current best result or blocked status, and wait at the stage checkpoint.

If the user says `下一步` or equivalent, the Retry Budget is bypassed and the workflow advances immediately.

### Autonomous Mode

End-to-end continuous execution is opt-in only for the current request. Example:

```text
这次不用每一步等我，直接做到最终 Demo；只有真正 blocker 才停。
```

Autonomous Mode does not bypass evidence gates.

## Channel-native demos require frontend references

A channel capability map is not enough to make a native-looking demo. Before generating an Amazon.co.jp, Rakuten, Yahoo! Shopping, retailer, or DTC **channel-native demo**, the workflow must establish the current **consumer-facing frontend**.

At Stage 5.5 the agent must:

1. verify **Platform Capability** — current editable areas, account access, module/component support, limits, policies, and ownership;
2. ask whether the user has a preferred current **Reference URL**, ASIN, retailer/store page, approved design-system reference, or screenshot set;
3. if supplied, use it as the candidate **Primary Reference**;
4. if none is supplied, research 1–3 current comparable consumer-facing pages and recommend one Primary Reference;
5. visually inspect/capture the material desktop/mobile shell, section order, interactions, and brand/platform ownership;
6. produce a **Channel Frontend Reference Pack**.

**Official rules do not substitute for frontend visual evidence.** Documentation may prove what a platform supports, but it does not prove the exact current consumer-facing layout.

Immediately before Stage 9, the Skill runs `FRONTEND_FIDELITY_GATE`.

If the gate passes, Stage 9 reproduces the verified channel shell first and then inserts approved project content into verified brand-controlled regions.

If the gate fails, the allowed fallback is:

```text
Content Review Demo
```

The Skill must not invent generic marketplace chrome, custom branded navigation, cards, tabs, purchase controls, or other UI and label it a channel-native PDP/demo.

## Included capabilities

- Project Definition, Source Gate, and Fact Lock
- Consumer Strategy and Market Evidence Registry
- Page Boundary Matrix and Message Architecture
- Platform Capability Map
- Channel Frontend Reference Pack and Frontend Fidelity Gate
- Channel-specific slot and module planning
- Asset Manifest and Visual Evidence Matrix
- Visual-production briefs and interactive review demos
- Claim, Japan-market, locale, channel, frontend-fidelity, mobile, technical, Execution Flow, and Review Mode QA
- `ja-JP` localization guidance
- Japan channel profiles for:
  - Amazon.co.jp
  - Rakuten
  - Yahoo! Shopping
  - Japan DTC product pages
  - Japan retailer PDPs

## Evidence boundary

This repository does not assume:

- a product category;
- a fixed Japan consumer persona;
- predefined needs, scenes, or keywords;
- one marketplace or page template;
- private company facts, pricing, claims, designs, or approvals.

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
按默认 checkpoint workflow 执行：每个 numbered stage 做完后给我 review，再进入下一步。
如果我说“继续 / 下一步 / go next”，立即锁定当前 stage 并推进，不要继续重做当前 frame。
同一个 frame / 同一个问题最多自动重试两次。
如果最终要生成 channel-native Demo，在 Stage 5.5 先问我是否有参考链接 / ASIN / 页面截图。
没有的话，你自己调研 1–3 个当前参考，给出 Primary Reference 和 Channel Frontend Reference Pack 后让我确认。
FRONTEND_FIDELITY_GATE 通过前不要生成或命名为原生渠道 PDP Demo。
Do not infer category needs or Japan consumer preferences without current project evidence.
Keep unsupported claims in PENDING CLAIM.
```

## Skill layout

```text
.agents/skills/japan-listing-demo/
├── SKILL.md
├── core/
│   ├── manifest.yaml
│   ├── workflow.md
│   ├── contracts.md
│   ├── market-research.md
│   ├── localization.md
│   ├── visual-evidence.md
│   ├── qa.md
│   ├── profiles/categories/_template.md
│   └── evals/
├── references/
│   └── channel-native-demo.md
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

The packager verifies that the ZIP contains the bundled core and all Japan runtime files.

## Optional private use

A company may add a separate private brand overlay for confidential product facts, pricing, claims, Figma links, approvals, or unreleased assets. That overlay is optional; public Japan-team use remains one Skill.

## Maintenance

The bundled core snapshot is sourced from `heymio/gtm-listing-demo` v0.2.0, commit `b882526f5a683235d30f562006cf1984a9f0d9f9`, with distribution-level execution-control and channel-frontend patches documented in the Japan Skill. This provenance is for maintainers only and creates no runtime dependency.

See [`docs/install.md`](docs/install.md).

## Version

`0.2.3`

## License

MIT.
