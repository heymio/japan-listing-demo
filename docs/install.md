# japan-listing-demo installation and use

## Team installation: one Skill

Japan-team users install only:

```text
japan-listing-demo
```

No second repository or Skill ZIP is required. The generic workflow is bundled inside the Japan distribution.

## Default execution behavior: Major Stage Checkpoints

The Skill uses **checkpointed execution by default**.

For each numbered workflow stage:

1. complete the stage to a reviewable state;
2. show the output, assumptions, and open items;
3. stop at the Major Stage Checkpoint;
4. wait for the user's review before moving to the next numbered stage.

The agent should not pause after every small search, tool call, table, frame, or image inside a stage.

## Transition Commands: continue means move on

At a checkpoint or while iterating a problematic frame, the following normally mean **move to the next numbered stage**:

```text
继续
下一步
go
go next
next
先这样
这张先过
```

Unless the user explicitly says `继续优化这张` or equivalent, these are Transition Commands.

After a Transition Command, the agent must:

- stop regenerating or re-critiquing the current frame/subtask;
- preserve the best current version;
- record remaining issues as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items;
- lock the current stage snapshot;
- enter the next numbered stage immediately.

It must not require another `继续` before advancing.

## Retry Budget

For the same artifact and the same identified issue, the agent may make at most **two autonomous attempts** without new user evidence or a materially new instruction.

After two unsuccessful attempts, it stops the loop and waits at the current Major Stage Checkpoint with the current best result or blocked status.

A Transition Command overrides this Retry Budget and moves on immediately.

## Channel-native demo frontend reference workflow

When the requested deliverable is intended to look like a real Amazon.co.jp, Rakuten, Yahoo! Shopping, retailer, or DTC frontend, the Skill must not generate the shell from memory.

At Stage 5.5 it performs two separate research tracks:

### Platform Capability

Verify current editable regions, account capabilities, module/component access, limits, content ownership, policies, and mobile constraints from authoritative sources and the actual account/retailer/CMS context when available.

### Frontend Visual Reference

Before native demo assembly, the agent asks whether the user has a preferred current **Reference URL**, ASIN, retailer/store page, approved design-system reference, screenshot set, or PDF capture.

- If supplied, it becomes the candidate **Primary Reference**.
- If none is supplied, the agent researches 1–3 current comparable consumer-facing pages and recommends one Primary Reference.
- It visually inspects/captures the material desktop/mobile shell, section order, interactions, and brand/platform ownership.
- It outputs a **Channel Frontend Reference Pack** and frontend fidelity status.

**Official rules do not substitute for frontend visual evidence.** A platform document can confirm capabilities, but it does not prove the exact current consumer-facing layout.

If a live page is blocked, the agent follows the normal Retry Budget, then asks for screenshots/PDF or uses an explicitly identified secondary reference for gaps. It must not invent the missing channel shell.

## Frontend Fidelity Gate

Immediately before Stage 9, the Skill runs `FRONTEND_FIDELITY_GATE`.

A channel-native demo requires a locked Primary Reference plus material consumer-facing evidence for the shell, section order, ownership boundaries, and required desktop/mobile behavior.

If the gate fails, the Skill may produce:

```text
Content Review Demo
```

It must not call that fallback an Amazon PDP Demo, Rakuten native page, retailer-native PDP, or another channel-native demo.

When the gate passes, Stage 9 reproduces the verified channel shell first and then inserts approved project content into verified brand-controlled regions. Review Mode is an overlay only and must not change the Consumer Mode layout.

## Autonomous Mode is optional

If a user explicitly wants full automatic execution for one task, they can say:

```text
这次不用每一步等我，直接做到最终 Demo；只有真正 blocker 才停。
```

Autonomous Mode applies only to that request. It is not the default, and it does not bypass the Channel Frontend Reference Pack or Frontend Fidelity Gate.

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
Category: determine from current project evidence
Keep unsupported claims in PENDING CLAIM.
按默认 Major Stage Checkpoint 执行；每个 numbered stage 做完后让我 review。
如果我说“继续 / 下一步 / go next”，立即推进到下一 stage，不要继续生成当前 frame。
同一 frame / 同一问题最多自动重试两次。
如果要生成 channel-native Demo，Stage 5.5 先问我是否有参考 URL / ASIN / 页面截图；没有的话你自己研究 1–3 个当前参考并让我确认 Primary Reference。
FRONTEND_FIDELITY_GATE 通过前不要把内容 Review 页面叫作原生渠道 PDP Demo。
```

If consumer copy uses another locale, specify it explicitly. Japan market does not automatically force Japanese copy.

## ChatGPT Personal Skills

Where Personal Skills are available, upload one ZIP:

```text
dist/japan-listing-demo.skill.zip
```

After installation, invoke only `japan-listing-demo`.

## Build the ZIP

From the repository root:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

The package command verifies required core and Japan files before succeeding.

## GitHub-connected ChatGPT without Personal Skills

Ask the conversation to read this repository's Skill:

```text
heymio/japan-listing-demo/.agents/skills/japan-listing-demo/SKILL.md
```

Then request the bundled core references, Japan references, selected channel profile, and `references/channel-native-demo.md` when a native frontend demo is requested. No separate public-core repository read is required for normal use.

## Optional private company overlay

Private overlays may add:

- confidential product evidence;
- price and SKU decisions;
- unreleased capabilities;
- private design links and assets;
- internal channel access;
- approval and review rules.

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

The bundled snapshot records its source in `core/manifest.yaml`.

To update it:

1. review the upstream core changelog;
2. update the bundled files in a feature branch;
3. preserve or deliberately revise Japan distribution patches such as checkpoint/transition and channel-frontend behavior;
4. rerun core, Japan, channel, cross-category, and frontend-fidelity evals;
5. run validator and packager;
6. release only after CI succeeds.
