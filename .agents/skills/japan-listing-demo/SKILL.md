---
name: japan-listing-demo
description: Use when adapting product listing strategy, enhanced content, visual briefs, or interactive review demos for the Japan market across Japanese ecommerce channels, DTC pages, and retailer PDPs while preserving evidence, category, locale, channel, and claim boundaries.
---

# Japan Listing Demo

**REQUIRED SUB-SKILL:** Use `gtm-listing-demo` public core version 0.2.0 or later.

## Core principle

Apply Japan-specific market research, localization, channel, claim-review, and QA layers without turning a country label into a consumer persona or a product-category playbook.

## Configuration

Start from the public core Project Definition and set the layers independently:

```yaml
market:
  country: JP
locale:
  id: ja-JP
channel:
  type: project-defined
category: project-defined
page_targets: project-defined
```

`market.country: JP` activates this overlay. `locale.id: ja-JP` is common but not mandatory; an explicit project locale always wins.

## Mandatory rules

1. Load the public core before this overlay.
2. Keep `market`, `locale`, `channel`, `category`, `offer`, and `page_targets` separate.
3. Do not infer needs, preferences, scenes, keywords, visual settings, or message priorities from `JP` alone.
4. Build a Market Evidence Registry from current category-, channel-, and project-specific evidence.
5. Use `references/ja-jp-localization.md` only when the requested consumer locale is `ja-JP`.
6. Load exactly one primary channel profile, plus any confirmed retailer or campaign constraints.
7. Verify current channel rules, editable slots, account capabilities, and content ownership before locking modules.
8. Treat competitor pages as evidence of competitor execution, not proof of current account access.
9. Keep claims, legal checks, certifications, pricing, availability, service terms, and platform capabilities in `PENDING CLAIM` until authoritative evidence supports formal release.
10. Keep reusable Japan rules category-neutral. Product-category conclusions belong in the public core's Category Overlay or current Project Evidence.
11. Preserve the public core's Page Boundary Matrix, Visual Evidence Matrix, Review Mode, Consumer Mode, Mobile QA, and asset-path QA.
12. Keep confidential brand, product, price, design, and approval information outside this public repository.

## Execution order

```text
1 Load gtm-listing-demo public core
2 Confirm Project Definition
3 Load Japan market evidence framework
4 Load requested locale rules
5 Load selected Japan channel profile
6 Execute Source Gate and Fact Gate
7 Build Consumer Strategy from project evidence
8 Map messages to verified channel slots
9 Produce and review visual evidence
10 Run Japan, locale, channel, claim, mobile, and technical QA
```

## References

Read only the references needed by the current project:

- `references/public-core.md`
- `references/japan-market-evidence.md`
- `references/ja-jp-localization.md` when `locale.id: ja-JP`
- `references/japan-claim-compliance.md`
- `references/qa.md`
- one file under `profiles/channels/`

## Required outputs

In addition to the public core outputs, produce:

- selected Japan channel profile and capability status;
- Market Evidence Registry with confidence and allowed usage;
- locale decision and native-review status;
- Japan claim/compliance verification queue;
- Japan-specific QA result with open items separated from passed checks.

## Quality gate

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
```

When revising this overlay, rerun the scenarios under `evals/`.
