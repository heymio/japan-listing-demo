# Visual benchmark policy

## Benchmark purpose

A benchmark communicates the quality bar and specific visual principles to learn from, such as composition, lighting, product prominence, hierarchy, realism, spacing, and information density.

A benchmark **does not automatically** become a reusable final asset.

## Benchmark versus reuse

Use explicit structure:

```yaml
benchmark:
  references: [BENCH-01]
  learn_from: [composition, lighting, hierarchy]
  reuse_asset: false
```

If a prior asset is intentionally reused, Planning must identify it as a source/reusable asset and any required inherited-asset checks must already be resolved upstream.

Do not convert a benchmark into a final Asset ID, approved role, slot assignment, or reuse permission merely because the user says it looks good.

## Production behavior

Use benchmark references to calibrate creative quality. Reuse only when reuse is explicit.
