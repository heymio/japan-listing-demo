# japan-listing-demo installation and use

## Dependency

This overlay requires the public core:

```text
heymio/gtm-listing-demo
version 0.2.0 or later
```

Install or load the public core first.

## Codex App / CLI / IDE

Open both repositories in the working environment, or install both Skills in the supported Skill directory.

Invoke the public core and overlay explicitly:

```text
$gtm-listing-demo
$japan-listing-demo
```

Recommended prompt:

```text
Use gtm-listing-demo together with japan-listing-demo.
Market: JP
Locale: ja-JP
Channel: select and verify the current Japan channel profile
Category: determine from current project evidence
Keep unsupported claims in PENDING CLAIM.
```

If the consumer locale is not Japanese, set the requested locale explicitly. The overlay must not force `ja-JP` solely because the market is Japan.

## Build the Skill ZIP

From the repository root:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

## ChatGPT Personal Skills

Where Personal Skills are available, install both ZIP files:

1. `gtm-listing-demo.skill.zip`
2. `japan-listing-demo.skill.zip`

The Japan package is an overlay and does not contain a second copy of the public core.

Suggested invocation:

```text
Use the gtm-listing-demo public core and japan-listing-demo overlay.
Confirm market, locale, channel, category, offer, and page targets separately.
Build the Market Evidence Registry before drawing Japan-specific consumer conclusions.
```

## GitHub-connected ChatGPT without Personal Skills

Ask the conversation to read:

```text
Public core:
heymio/gtm-listing-demo/.agents/skills/gtm-listing-demo/SKILL.md

Japan overlay:
heymio/japan-listing-demo/.agents/skills/japan-listing-demo/SKILL.md
```

Then request only the references and channel profile needed for the current project.

Reading repository files in one conversation is not the same as installing a Personal Skill.

## Private company work

Use a separate private brand overlay for:

- confidential product evidence;
- price and SKU decisions;
- unreleased capabilities;
- private design links and assets;
- internal channel access;
- approval and review rules.

Precedence should be:

```text
current user request
> current approved project evidence
> private brand overlay
> japan-listing-demo
> gtm-listing-demo public core
```

Do not copy confidential material into this public repository.

## Maintenance

After changing the overlay:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Rerun the scenarios under `evals/` and test at least two different Japan channels before increasing the minimum public-core version.
