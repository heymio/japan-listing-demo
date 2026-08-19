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

## Autonomous Mode is optional

If a user explicitly wants full automatic execution for one task, they can say:

```text
这次不用每一步等我，直接做到最终 Demo；只有真正 blocker 才停。
```

Autonomous Mode applies only to that request. It is not the default.

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

Then request the bundled core references, Japan references, and one selected channel profile needed by the current project. No separate public-core repository read is required for normal use.

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
3. preserve or deliberately revise Japan distribution patches such as checkpoint/transition behavior;
4. rerun core, Japan, channel, and cross-category evals;
5. run validator and packager;
6. release only after CI succeeds.
