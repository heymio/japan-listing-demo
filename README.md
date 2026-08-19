# japan-listing-demo

`japan-listing-demo` is a **standalone public Skill** for turning product evidence into Japan-market listing strategy, channel-specific content architecture, visual briefs, and interactive review demos.

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

## Included capabilities

- Project Definition, Source Gate, and Fact Lock
- Consumer Strategy and Market Evidence Registry
- Page Boundary Matrix and Message Architecture
- Channel-specific slot and module planning
- Asset Manifest and Visual Evidence Matrix
- Visual-production briefs and interactive review demos
- Claim, Japan-market, locale, channel, mobile, technical, and Review Mode QA
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
Confirm Project Definition, Source Gate, Fact Lock, selected Japan channel profile, and Market Evidence Registry first.
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

The bundled core snapshot is sourced from `heymio/gtm-listing-demo` v0.2.0, commit `b882526f5a683235d30f562006cf1984a9f0d9f9`. This provenance is for maintainers only and creates no runtime dependency.

See [`docs/install.md`](docs/install.md).

## Version

`0.2.0`

## License

MIT.
