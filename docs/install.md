# japan-listing-demo installation and use

## Team installation: one Skill

Japan-team users install only:

```text
japan-listing-demo
```

No second repository or Skill ZIP is required.

## Default execution behavior: Major Stage Checkpoints

For each numbered workflow stage:

1. complete the stage to a reviewable state;
2. emit a **Stage Completion Manifest**;
3. show output, assumptions, and open items;
4. stop at the Major Stage Checkpoint;
5. wait for the user's review before the next numbered stage.

The Stage Completion Manifest records planned/completed/approved/needs-revision/missing/blocked/open items and `COMPLETE`, `PARTIAL`, or `BLOCKED` status.

A completed subset does not make a stage complete.

## Transition Commands: continue means move on

These normally mean **move to the next numbered stage**:

```text
继续
下一步
go
go next
next
先这样
这张先过
```

Unless the user explicitly says to continue improving the current artifact, the agent must stop current retries, preserve the best version, record unresolved items, lock the real stage status, and move on immediately.

A `PARTIAL` stage remains `PARTIAL` after transition.

## Retry Budget

For the same artifact and same identified issue, the agent may make at most **two autonomous attempts** without new user evidence or a materially new instruction.

## Delivery-integrity workflow

Read `references/delivery-integrity.md`.

### Asset Readiness Preflight

Stage 1 identifies the asset classes later work is expected to need, what is received, what is missing, when it is needed, and whether the gap is blocking.

### Approved Asset Registry + Asset-to-Slot Contract

Approved assets receive stable Asset IDs with canonical source, role, dimensions/aspect, page/offer scope, allowed slots, approval status, derivative provenance, and transform rules.

The slot contract binds a slot/module to the required Asset ID, dimensions/aspect, crop/transform rule, interaction, and ownership.

Run:

```text
ASSET_SLOT_GATE
```

before final adaptation and Demo Assembly. Do not silently replace an approved asset with another role-class asset or unapproved derivative.

### Coverage and module fit

Run separately:

```text
CONTENT_COVERAGE
MODULE_FIT_GATE
```

Full topic coverage does not prove native module fit. Independent static boards must not be mechanically turned into slide/carousel interactions during Demo Assembly; interaction logic and content packing are planned in Stage 7 and Stage 7.5.

### Differentiator proof

Run:

```text
DIFFERENTIATOR_PROOF_GATE
```

for visualizable P0 purchase reasons. Generic lifestyle imagery alone is not enough.

### Delivery parity

Before a demo is called complete, run:

```text
DELIVERY_PARITY_GATE
```

against planned vs implemented slot/module, interaction, source Asset IDs, dimensions/aspect, message coverage, page/offer ownership, and channel region.

A working HTML file is not proof of parity.

### Change control

When newer authoritative facts, approved decisions, asset/UI sources, channel references, or claim decisions invalidate earlier work, create a **Change Impact Map**:

```text
UNAFFECTED
REVIEW
INVALIDATED
REOPEN
```

Preserve unaffected locked work and reopen only impacted stages/items.

## Channel-native demo frontend reference workflow

When the requested deliverable is intended to look like a real Amazon.co.jp, Rakuten, Yahoo! Shopping, retailer, or DTC frontend, the Skill must not generate the shell from memory.

At Stage 5.5:

1. verify Platform Capability;
2. ask whether the user has a preferred current Reference URL / ASIN / page / screenshot set;
3. use a valid user-supplied reference as candidate Primary Reference;
4. otherwise research 1–3 current comparable consumer-facing pages;
5. visually inspect material desktop/mobile shell, section order, interactions, and ownership;
6. output a Channel Frontend Reference Pack.

**Official rules do not substitute for frontend visual evidence.**

Immediately before Stage 9, run:

```text
FRONTEND_FIDELITY_GATE
```

If it fails, output a clearly named `Content Review Demo` rather than inventing a channel-native shell.

## Autonomous Mode is optional

End-to-end continuous execution is opt-in for the current request only. It does not bypass Stage Completion Manifest, asset-slot, module-fit, differentiator-proof, parity, claim, or frontend-fidelity gates.

## Codex App / CLI / IDE

Open or clone this repository, then invoke:

```text
$japan-listing-demo
```

Recommended prompt:

```text
Use the standalone japan-listing-demo Skill.
Market: JP
Locale: ja-JP
Channel: select and verify the current Japan channel profile
按默认 Major Stage Checkpoint 执行；每个 numbered stage 做完后给我 Stage Completion Manifest。
如果我说“继续 / 下一步 / go next”，立即推进，不要继续生成当前 frame；同一 frame / 同一问题最多自动重试两次。
提前做 Asset Readiness Preflight；已通过素材用稳定 Asset ID 绑定 slot，不能把别的模块素材裁切后替换。
CONTENT_COVERAGE 和 MODULE_FIT_GATE 分开检查；不要在 Demo 阶段把静态图机械切成 slide/carousel。
Demo 前跑 ASSET_SLOT_GATE、DIFFERENTIATOR_PROOF_GATE、DELIVERY_PARITY_GATE。
如果要生成 channel-native Demo，Stage 5.5 先问我是否有参考 URL / ASIN / 页面截图；没有的话研究 1–3 个当前参考并让我确认 Primary Reference。
FRONTEND_FIDELITY_GATE 通过前不要把内容 Review 页面叫作原生渠道 PDP Demo。
```

## ChatGPT Personal Skills

Where Personal Skills are available, upload one ZIP:

```text
dist/japan-listing-demo.skill.zip
```

After installation, invoke only `japan-listing-demo`.

## Build the ZIP

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

## GitHub-connected ChatGPT without Personal Skills

Read this repository's `SKILL.md`, bundled core references, `references/delivery-integrity.md`, selected channel profile, and `references/channel-native-demo.md` when a native frontend demo is requested.

## Optional private company overlay

Private overlays may add confidential product evidence, pricing/SKU decisions, unreleased capabilities, private design links/assets, internal channel access, and approval rules.

Recommended precedence:

```text
current user request
> current approved project evidence
> optional private brand overlay
> standalone japan-listing-demo
> older project material
```

Do not copy confidential material into this public repository.

## Maintainer-only core updates

Preserve or deliberately revise the documented checkpoint/transition, channel-frontend, and delivery-integrity patches; rerun core, Japan, channel, cross-category, frontend-fidelity, and delivery-integrity evals; release only after CI succeeds.
