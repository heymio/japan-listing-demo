# Production Creative QA

Creative QA answers two separate questions:

1. **Asset-level:** Is this a good marketing artifact for the intended channel role?
2. **Set-level:** Does this asset still work when placed next to the other assets in the page narrative?

## Asset-level Creative QA

Evaluate exactly these seven dimensions:

1. **Message clarity** — the intended shopper takeaway is immediately understandable.
2. **Product prominence** — the product/evidence object has the right visual weight for the role.
3. **Visual proof** — the image directly supports the primary message rather than merely decorating it.
4. **Composition** — hierarchy, spacing, safe areas, and reading order are controlled.
5. **Realism** — environment, scale, lighting, and product integration feel commercially credible.
6. **Benchmark / pattern match** — the artifact meets the approved quality/reference principles without copying an unrelated asset role.
7. **Channel readiness** — aspect ratio, density, text hierarchy, and role fit are appropriate for the planned channel slot.

## Set-level Creative QA

Asset-level PASS is not enough. Review the ordered set for these six dimensions:

1. **Scene repetition** — adjacent or repeated sections do not collapse into the same environment by habit.
2. **Composition repetition** — neighboring assets do not repeat the same framing/layout template without a deliberate comparison reason.
3. **Tone / brightness rhythm** — dark, bright, neutral, saturated, and natural treatments create intentional pacing rather than an accidental run of one tone.
4. **Product-scale repetition** — hero, medium, close-up, contextual, and detail scales vary when the shopper task changes.
5. **Proof-form diversity** — lifestyle, source-faithful product, mechanism, UI, comparison, installation, and scenario-flow forms are used according to role rather than one form being repeated everywhere.
6. **Message-role redundancy** — adjacent assets do not repeat the same shopper task under different copy.

**Same art direction ≠ same composition.** Repeating typography, product treatment, or brand design language is acceptable; repeating the full scene/composition/tone/scale/proof signature is not.

The deterministic helper `scripts/set_level_qa.py` evaluates structured Page Visual System metadata. It does not claim pixel-level aesthetic judgment. Human/model visual review may add issues but should not silently erase deterministic repetition findings unless Planning documented intentional repetition.

## Set-level cadence

Run lightweight set review without adding a new formal gate:

- after the first 2–3 assets in a page region;
- at Gallery completion;
- after each logical enhanced-content cluster;
- before Production Freeze as the final contact-sheet / whole-set review.

When a set issue is found, use the Smallest Sufficient Intervention rather than automatically regenerating the whole cluster.

## Final whole-set record

For a v0.3.2 handoff with `page_visual_system`, Production Freeze requires evidence that the **current final set** was actually reviewed together. Store this in the Asset Ledger as `set_qa`:

```yaml
set_qa:
  status: CLEAR
  reviewed_asset_ids:
    - G1
    - G2
    - A1
  reviewed_output_refs:
    G1: file:g1
    G2: file:g2
    A1: file:a1
  visual_review_ref: contact-sheet:final-v1
```

Requirements:

- `reviewed_asset_ids` exactly matches the current authoritative required set;
- `reviewed_output_refs` contains exactly one entry for every current required Asset ID and each value equals that asset's exact current `current_output_ref`;
- if any selected/final output changes after the whole-set review, the previous `set_qa` becomes `STALE` and the current set must be reviewed again;
- `visual_review_ref` identifies the final contact sheet/set that was visually reviewed;
- `CLEAR` means the final set review found no material creative issue;
- `USER_ACCEPTED` is allowed only when the user explicitly accepts the current set despite a non-blocking creative concern;
- missing, stale, `REVIEW`, or `REVISE` set state keeps Production Freeze not ready.

This is Production creative readiness, not a new numbered Stage or Hardening gate.

## Result

For one asset, use `REVIEW`, `REVISE`, or `USER_APPROVED` in the creative Asset Ledger.

For set-level structured QA, use `CLEAR`, `REVIEW`, or `REVISE`. A final explicit whole-set acceptance may use `USER_ACCEPTED` as described above. These are creative-quality statuses only; they are **not** Hardening gates.

Creative QA does not perform physical-file verification or final delivery hardening.
