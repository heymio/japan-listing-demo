# japan-listing-demo

`japan-listing-demo` is a public Japan-market overlay for the generic [`gtm-listing-demo`](https://github.com/heymio/gtm-listing-demo) workflow.

It adds Japan-specific market-evidence, localization, channel, claim-review, and QA layers without hard-coding one product category, company, or marketplace.

## What this repository is

```text
gtm-listing-demo public core
        +
japan-listing-demo public overlay
        +
optional brand/private overlay
        +
current project evidence
```

Use the public core for Source Gate, Fact Lock, Consumer Strategy, page boundaries, message architecture, visual evidence, interactive demos, and final QA.

Use this repository when the target market is Japan and the project needs:

- Japan market-evidence governance;
- deeper `ja-JP` localization QA;
- Japan channel profiles;
- Japan claim and compliance verification queues;
- Japan-specific regression tests;
- a reusable public Skill package for ChatGPT or Codex.

## What it does not contain

This repository does **not** assume:

- a product category;
- a fixed Japan consumer persona;
- predefined user needs or scenes;
- a universal keyword list;
- one marketplace or page template;
- private company facts, pricing, claims, designs, or approvals.

Actual needs, barriers, search language, visual direction, and message priority must come from:

```text
category
× channel
× audience
× offer
× current project evidence
```

## Dependency

Required public core:

```text
heymio/gtm-listing-demo
version 0.2.0 or later
```

Install or load the public core before using this overlay.

## Built-in Japan channel profiles

- Amazon.co.jp
- Rakuten
- Yahoo! Shopping
- Japan DTC product pages
- Japan retailer PDPs

Each profile requires current account, template, policy, and editable-slot verification. A previous page or competitor implementation is not proof of current capability.

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

Then ask:

```text
Use the gtm-listing-demo public core together with japan-listing-demo.
First confirm Project Definition, Source Gate, Fact Lock, selected Japan channel profile, and Market Evidence Registry.
Do not infer category needs or Japan consumer preferences without current project evidence.
Keep unsupported claims in PENDING CLAIM.
```

## Skill layout

```text
.agents/skills/japan-listing-demo/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── public-core.md
│   ├── japan-market-evidence.md
│   ├── ja-jp-localization.md
│   ├── japan-claim-compliance.md
│   └── qa.md
├── profiles/
│   └── channels/
├── evals/
└── scripts/
```

## Validation

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

The package command creates:

```text
dist/japan-listing-demo.skill.zip
```

GitHub Actions runs the validator, builds the ZIP, and uploads it as an artifact.

## Installation

See [`docs/install.md`](docs/install.md).

For ChatGPT Personal Skills, install both:

1. `gtm-listing-demo`
2. `japan-listing-demo`

For confidential company work, add a separate private overlay rather than publishing private data here.

## Version

Current release target:

```text
0.1.0
```

## License

MIT.
