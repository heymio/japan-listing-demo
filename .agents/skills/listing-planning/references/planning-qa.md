# Planning QA

Planning QA asks whether the project has enough evidence and architecture to hand a complete, coherent production job downstream.

## Required checks

1. Product/offer facts are traceable and conflicts are visible.
2. Claim readiness is separate from capability existence.
3. Consumer Strategy is evidence-based and not inferred from country name alone.
4. VOC/competitor findings are separated from inference.
5. Market and `ja-JP` localization implications are current and scoped.
6. Channel capability and Frontend Visual evidence are distinguished.
7. Message Architecture reflects priority, objections, and reasons to believe.
8. Gallery and enhanced-content roles are planned separately.
9. `CONTENT_COVERAGE` and `MODULE_FIT_GATE` are both evaluated.
10. Module count respects verified channel limits.
11. Interaction/content packing is decided before Production.
12. Stage 7 defines the **Complete Demo-Required Production Set** for Gallery, enhanced-content, and any other required page/demo regions.
13. Every current final Asset ID has exactly one `evidence_mode`: `SOURCE_FAITHFUL`, `CREATIVE_MOCK`, or `PROOF_VISUAL`.
14. The Production Handoff contains a concise Page Visual System covering every current final Asset ID.
15. Adjacent assets do not accidentally repeat the same scene/composition/tone/product-scale/proof-form signature unless intentional repetition is documented.
16. Any post-Stage-7 production-set change is represented by an explicit scope revision/delta rather than silent mutation.

## Stage 6.5 decision table

| Situation | Stage 6.5 behavior |
|---|---|
| Fresh source render/UI/brand asset | inventory only |
| New final Gallery/A+ asset not produced yet | plan its Asset ID; do not audit nonexistent output |
| Previously approved exact asset requested for reuse | targeted early audit |
| User supplied visual only as benchmark | register benchmark role; no reuse approval |

## Page Visual System quality

The Page Visual System is an art-direction matrix, not a project-management manifest and not a new Gate. It should be compact enough to survive the Production context firewall while still preventing adjacent assets from converging on one template.

For each Asset ID record:

- visual role;
- scene family;
- composition family;
- tone;
- product scale;
- proof form;
- optional neighbor contrast note.

**Same art direction ≠ same composition.** Brand consistency may repeat typography, product treatment, and design language while deliberately varying scene, composition, scale, tone, or proof form.

## Evidence-mode quality

- `SOURCE_FAITHFUL`: product/pack/offer identity must remain source-faithful; missing authoritative source may block production when identity cannot be represented safely.
- `CREATIVE_MOCK`: lifestyle/atmosphere/spatial creative work may proceed with reduced evidence entitlement when commercially credible; generated placement/installation details do not become Product Truth.
- `PROOF_VISUAL`: factual installation/dimension/interface/mechanism/UI/compatibility proof requires suitable authoritative source evidence; missing proof source is blocked rather than invented.

Core rule: `source insufficiency != automatic creative rework`.

## Handoff quality

The Project Brief, Creative Strategy Kernel, and Production Handoff should preserve resolved decisions and creative strategy while excluding final-delivery hardening machinery and long-form research history.

A Planning stage is not ready for Production merely because P0 messages have visual concepts. The complete required asset set must be enumerated, including blocked assets and their missing upstream decisions.

If a scope revision removes or replaces an asset, the current `asset_set` is authoritative; the delta explains the change and does not reopen unrelated approved work.
