# Claim and compliance planning

## Purpose

This reference creates a planning-time verification queue for consumer claims and regulated/commercial statements. It is not legal advice and does not assume one rule applies to every product.

Applicable requirements depend on the current category, product design, service model, data flow, sales method, channel, audience, market, locale, and release scope.

## Verification queue

For each project, determine whether current authoritative sources are required for:

- product safety, certification, testing, installation, and labeling;
- wireless, electrical, battery, or connected-device requirements;
- advertising representations, comparisons, rankings, endorsements, and superiority claims;
- pricing, discounts, tax, subscriptions, renewal, cancellation, and trial terms;
- warranties, returns, delivery, availability, and seller identity;
- privacy, account data, analytics, recordings, biometrics, cloud processing, and cross-border transfer;
- children, health, accessibility, or other protected-use contexts;
- environmental, recycling, packaging, and disposal information;
- marketplace-specific restricted claims and content policies.

Keep only the rows relevant to the current project.

## Evidence hierarchy

Prefer, in order:

1. current official government, regulator, standards, or platform source;
2. current approved certification, test, legal, or compliance record;
3. current signed commercial or service terms;
4. current company policy approved for the target project;
5. secondary explanation for orientation only.

Do not rely on an earlier project, another category, a competitor page, or an old marketplace implementation as proof.

## Claim record

For each consumer-visible claim or visual implication, record:

- exact claim/meaning;
- evidence source and version;
- test/environment/compatibility/account/subscription/use conditions;
- market and locale scope;
- channel/slot scope;
- owner/approver;
- status such as `CONFIRMED`, `PENDING CLAIM`, `PROHIBITED`, or `INTERNAL ONLY`;
- refresh trigger such as a date, product change, policy change, or new evidence.

A product capability can be confirmed while the corresponding marketing claim is still pending.

## Visual claims

**A visual can create a claim** even when the text does not. Review icons, diagrams, before/after scenes, badges, comparisons, UI, environmental staging, and implied functional outcomes together with copy.

Do not use a footnote to repair a headline or visual whose main meaning exceeds the evidence.

## Planning boundary

Planning decides whether a claim is allowed, conditional, pending, prohibited, or internal-only and carries the relevant condition into Message Architecture and the Production Handoff.

Production must not invent or broaden the claim. Final file/slot verification and delivery gating belong to Hardening.

## Release readiness

Formal consumer use requires authoritative evidence, current channel-policy compatibility, required product/commercial approval, locale review, conditions preserved across copy and visuals, and a documented refresh trigger.

Anything else remains review-only.