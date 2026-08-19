# japan-listing-demo installation and use

## Team installation: one Skill

Japan-team users install only:

```text
japan-listing-demo
```

No second repository or Skill ZIP is required. The generic workflow is bundled inside the Japan distribution.

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
3. rerun core, Japan, channel, and cross-category evals;
4. run validator and packager;
5. release only after CI succeeds.
