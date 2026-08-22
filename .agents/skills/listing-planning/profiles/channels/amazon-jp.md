# Amazon.co.jp planning profile

## Use when

Select this profile when the target is an Amazon.co.jp product detail page or brand-controlled enhanced-content area.

## Account capability reuse

Account-level capabilities are not project-level questions when a valid persistent profile already exists.

Decision order:

1. if an `account_capability_profile` exists, is sufficiently recent, and has no conflicting evidence, reuse the recorded capability;
2. if the profile is missing, stale, malformed, or contradicted, ask/verify the capability;
3. never infer account access from competitor execution;
4. never hard-code brand-specific account values in this public profile.

A generic profile may record fields such as:

```yaml
account_capability_profile:
  channel: amazon-jp
  account_scope: brand-account
  capabilities:
    premium_a_plus: true
    brand_story: true
  verified_at: 2026-08-01
  source_ref: team-private-context
```

The values above illustrate the public contract only. Real brand/account values belong in private team context or explicit project input.

## Verify before planning

When capability evidence is not reusable, confirm from current official guidance and the actual Seller/Vendor account interface:

- ownership and ASIN/category eligibility;
- editable title, bullets, attributes, media, variations, Brand Story and enhanced-content regions;
- Basic A+ versus Premium A+ access;
- current module families, dimensions, interaction options, mobile behavior and publishing workflow;
- current content and claim policies.

Do not infer account access from competitor execution.

## Platform capability and frontend evidence

**Platform Capability evidence != Frontend Visual evidence.** Official platform rules prove what Amazon may support; they do not prove the exact current consumer-facing shell.

At Stage 5.5:

1. ask for a preferred current Amazon.co.jp Reference URL / ASIN / screenshot set;
2. treat a valid supplied page as the candidate **Primary Reference**;
3. if none is supplied, inspect 1–3 current comparable consumer-facing PDPs and recommend one;
4. visually capture material desktop/mobile shell, media/gallery behavior, variation/offer controls, enhanced-content placement, section order and ownership boundaries;
5. record unknown or blocked frontend regions rather than inventing them.

Planning produces the Channel Frontend Reference Pack; final native-fidelity enforcement belongs to Hardening.

## Content roles

| Area | Planning role |
|---|---|
| Main image / Gallery | Fast product and offer understanding |
| Title / bullets | Product identity and condensed reasons to buy |
| Attributes/specifications | Structured factual verification |
| Variations | Validated offer selection |
| Brand Story | Brand/portfolio context when available |
| Enhanced-content | Mechanism, proof, use cases, comparison and objection handling |

Platform-generated ratings, reviews, recommendations, sponsored blocks and purchase controls are not brand design ownership unless current evidence says otherwise.

## A+ module budget

The packaged current planning ceilings are:

- **Basic A+**: maximum 5 modules;
- **Premium A+**: maximum 7 modules.

Brand Story is separate from the A+ module count. A current account may have a lower usable limit; Planning may lower but never raise the packaged ceiling without updating verified policy.

## Message and module architecture

`Message != Module`.

Pack related messages into the smallest useful set of verified native modules. Do not create one module per topic.

Evaluate separately:

```text
CONTENT_COVERAGE != MODULE_FIT_GATE
```

Full topic coverage can coexist with poor module architecture.

For every selected enhanced-content module record:

- verified module family/account availability;
- shopper/message role;
- messages packed into it;
- why the interaction helps the shopper;
- evidence objects/assets required;
- orientation/density constraints;
- mobile behavior;
- supporting frontend/capability evidence.

If an interactive carousel, hotspot, video, comparison or other module is selected, design its interaction logic and content packing before Production. Do not leave interaction invention to Demo Assembly.

## Gallery and enhanced-content role separation

**Gallery-native** and **enhanced-content** are separate production roles even when they cover the same topic. Planning must create distinct required Asset IDs unless reuse/derivative intent is explicitly designed upstream.

Do not assume that an A+ landscape board can later be cropped into a Gallery board, or that a Gallery board automatically satisfies an A+ slot.

## Planning outputs

Record:

- account/site/capability state and verification date;
- reusable `account_capability_profile` reference when available;
- editable-region and ownership map;
- Primary Reference + Channel Frontend Reference Pack;
- Gallery and enhanced-content page architecture;
- Basic/Premium module budget used;
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE` planning result;
- mobile implications;
- Complete Demo-Required Production Set and blocked items.
