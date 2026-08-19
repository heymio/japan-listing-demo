# Public core dependency

## Source of truth

Public repository:

```text
heymio/gtm-listing-demo
```

Required version:

```text
0.2.0 or later
```

The public core owns:

- Source Gate and Fact Gate
- Consumer Strategy
- market, locale, region, channel, category, offer, and page-target separation
- output contracts
- Page Boundary Matrix
- Message-to-Slot Matrix
- Asset Manifest
- Visual Evidence Matrix
- Review Mode and Consumer Mode
- interactive-demo, mobile, and technical QA
- generic channel, locale, region, and category profiles

This repository owns only the public Japan overlay:

- Japan market-evidence method
- deeper `ja-JP` localization QA
- Japan channel profiles
- Japan claim/compliance verification queue
- Japan-specific evaluation scenarios

## Precedence

```text
current user request
> current approved project evidence
> current brand/private overlay
> japan-listing-demo overlay
> gtm-listing-demo public core
> generic defaults
```

## Loading rule

Load the public core first. Then load this overlay and one selected Japan channel profile. Do not copy and independently modify the public core inside this repository.

## Upgrade rule

When the public core changes:

1. review its changelog;
2. run this overlay validator;
3. rerun all Japan evals;
4. test one project on at least two different channels;
5. update the minimum version only after compatibility is confirmed.
