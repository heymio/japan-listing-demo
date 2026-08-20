# Team Golden Path

A normal Japan marketing teammate should be able to use one public entry point without understanding internal Skill architecture, SHA, provenance, or validator details.

## Scenario

The user starts with `$japan-listing-demo`, supplies current product/GTM/source materials, and selects a target channel such as Amazon.co.jp.

Expected user-visible path:

```text
Upload product/GTM/source materials
↓
Review Product / Offer / Claim baseline
↓
Review Consumer / Market Strategy
↓
Review channel page plan
↓
Review Creative Strategy / complete production asset set
↓
Review generated visuals
↓
Review verified demo
```

Expected internal behavior:

- Stage 0–7 routes to `listing-planning`.
- Stage 7.5–8 routes to `listing-production`.
- Stage 8.5–10 routes to `listing-hardening`.
- `listing-hardening` delegates exact-file evidence checks to `listing-evidence-auditor`.
- The user does not manually invoke internal Skills.
- Normal checkpoints show `Done / Open / Next` rather than governance tables.
- Transition Commands advance immediately instead of trapping the user in regeneration loops.
- Production generates requested artifacts rather than visualizing the workflow itself.
- Final demo review occurs only after hardening requirements for the requested scope are satisfied or a clearly labeled fallback scope is used.
