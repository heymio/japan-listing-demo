# Amazon.co.jp channel profile

## Use when

Select this profile when the current page target is an Amazon.co.jp product detail page or brand-controlled enhanced-content area.

## Verify before planning

Confirm from current official guidance and the actual account interface:

- Seller or Vendor ownership;
- category and ASIN eligibility;
- editable title, bullet, attribute, image, video, brand, enhanced-content, comparison, and variation areas;
- Basic versus Premium enhanced-content access;
- current module names, limits, dimensions, and mobile behavior;
- account-specific publishing and approval workflow;
- current content and claim policies.

Do not infer account access from a competitor page or another marketplace site.

## Platform capability is not frontend fidelity

Amazon official guidance and Seller/Vendor interfaces are **Platform Capability** evidence. They establish what the account/channel may support, but **official rules do not substitute** for current **consumer-facing** frontend visual evidence.

A high-fidelity Amazon PDP demo requires both current capability/ownership evidence and a current Amazon.co.jp frontend reference that visually proves the material shell and section order.

## Frontend reference intake

When an Amazon.co.jp channel-native demo is requested, read `references/channel-native-demo.md`.

At Stage 5.5, ask whether the user has a preferred current **Reference URL** or ASIN.

- If supplied, record it as the candidate **Primary Reference**.
- If not supplied, research 1–3 current comparable Amazon.co.jp PDPs and recommend one Primary Reference.
- Use current visual inspection or supplied screenshots/PDFs to establish the frontend shell.
- If live access is blocked, do not infer fidelity from text/DOM or official documentation alone.

## Frontend anatomy to capture

Capture enough evidence to establish, where present:

- Amazon/global page chrome relevant to PDP context;
- breadcrumb/category trail when material;
- product media/gallery region;
- title, brand/store link, rating/review summary, price/offer information, bullets;
- variation/option controls;
- Featured Offer / purchase controls;
- brand-controlled story/enhanced-content entry points;
- product description / A+ placement;
- specifications/product information regions;
- platform-controlled recommendations, reviews, sponsored, or merchandising blocks affecting section order;
- desktop/mobile reordering.

The demo does not need every Amazon-owned data point, but shell, ordering, hierarchy, and ownership boundaries must come from locked reference evidence rather than original web design.

## Slot roles

| Area | Primary role |
|---|---|
| Main image and gallery | Fast product and offer understanding |
| Title | Product identity, category language, and validated search terms |
| Bullet points | Condensed reasons to buy and key conditions |
| Attributes / specifications | Structured factual verification |
| Brand-controlled story area | Brand and portfolio context when available |
| Enhanced content | Mechanism, use cases, proof, comparison, and objection handling |
| Variations | Validated offer selection |

Ratings, reviews, sponsored placements, recommendations, Featured Offer UI, and other platform-generated blocks are outside brand design ownership unless current evidence says otherwise.

## Executable Amazon A+ module budget

Read `references/executable-gates.md` and `data/channel-policy-limits.json`.

The packaged current executable ceilings are:

- Basic A+: **5 modules**;
- Premium A+: **7 modules**.

These limits are machine policy for the current Skill version. A current account may have a lower usable limit; the project may record that lower value. The project agent must not raise the packaged ceiling by editing its own Project State Manifest.

Brand Story is treated as a separate detail-page section and is not counted as one of the Premium A+ module slots in the packaged policy.

Before Stage 7 can lock an A+ module plan, run:

```text
CHANNEL_MODULE_BUDGET_GATE
```

A plan with more modules than the effective limit fails even when all content topics are covered.

Content topics are not modules. Pack multiple related messages into the limited set of verified native modules.

## Amazon asset-role integrity

Read `references/delivery-integrity.md`.

Gallery assets and enhanced-content assets are distinct slot classes unless an explicitly approved derivative says otherwise.

- Approved Gallery assets keep stable Asset IDs and are reused exactly in Demo Assembly.
- Do not crop an A+/enhanced-content landscape board into a Gallery image and present it as the approved Gallery asset.
- Do not reuse a Gallery asset inside A+ merely because the subject looks relevant when the locked module requires a different role/evidence object.
- Record dimensions/aspect, crop/transform rule, page/offer scope, and allowed slots in the **Asset-to-Slot Contract**.

A material crop/recomposition/role change creates a derivative with a new Asset ID and approval status.

A deterministic crop is still a transform. It does not pass `TRANSFORM_AUTH_GATE` without matching transform authorization provenance.

## Planning rule

Use exact module families visible in the current account. If a module cannot be verified, record it as `UNKNOWN` rather than mapping content to a guessed structure.

`Message != Module`. Pack several related messages into one supported carousel, hotspot, video, comparison, or expandable structure when the current account provides it.

For channel-native work, map each planned region to the locked **Channel Frontend Reference Pack**. A message-to-module plan does not authorize inventing an Amazon frontend shell.

## A+ / enhanced-content module fit

Run `CONTENT_COVERAGE` and `MODULE_FIT_GATE` separately.

A+ message coverage may be complete while the module architecture is wrong. Do not treat “all topics are present” as proof that the selected Amazon module family is optimal or native.

For every selected enhanced-content module record:

- verified module family/account availability;
- message role and messages packed into it;
- why the interaction is useful for the shopper;
- evidence objects/assets required;
- source Asset IDs and orientation/density constraints;
- mobile behavior;
- corresponding frontend-reference evidence when relevant.

Do not take independent static boards and mechanically cut/group them into navigation carousel, image carousel, slide sequence, hotspot, or other interaction during Demo Assembly. If an interactive module is the best choice, redesign content packing and visual brief for that interaction in Stage 7 / 7.5 before production.

`CONTENT_COVERAGE = PASS` can coexist with `MODULE_FIT_GATE = FAIL`.

## Locked module origin

Stage 7 writes Amazon A+ architecture into the Project State Manifest `locked_module_plan` and computes a canonical `plan_hash`.

After user review, record a matching approval event for that exact plan hash. Stage 9 must consume the same hash.

Run:

```text
MODULE_ORIGIN_GATE
```

The gate fails if Demo Assembly adds an unplanned module, removes a planned module, changes native module type, changes interaction, or does not consume the exact locked plan hash.

Stage 9 may not create M08/M09/M10 after a 7-module plan was approved and then retroactively update the plan to legitimize them.

## Approval provenance

A `LOCKED` asset must pass `APPROVAL_PROVENANCE_GATE` through either a matching user approval event or exact SHA-256 recovery of a previously locked asset.

A file that looks similar to a missing prior asset is `RECOVERED_UNAPPROVED` until provenance is valid. Filename similarity is not exact recovery.

## Demo parity

After Stage 9 assembly, the external validator computes `DELIVERY_PARITY_GATE` and related gates.

For Amazon work, explicitly compare:

- planned Gallery slot count/order vs implemented Gallery assets;
- exact Gallery Asset IDs and target dimensions/aspect;
- planned Brand Story/A+ modules vs implemented modules;
- carousel/slide/hotspot/video/comparison interaction vs actual demo interaction;
- planned message coverage vs implemented coverage;
- Single/Kit/variation boundaries where applicable.

A missing A+ module, static rendering of a planned carousel, wrong source asset, wrong crop/dimension, or unplanned module causes failure even if HTML runs.

Agent-authored `declared_gate_results` are ignored. Executable PASS comes only from the **external validator**.

If the validator cannot run, executable gates remain `UNVERIFIED`.

## Frontend Fidelity Gate

Immediately before Stage 9, run `FRONTEND_FIDELITY_GATE`.

A deliverable may be labeled an Amazon.co.jp PDP/channel-native demo only when the Primary Reference, material consumer-facing shell, section order, ownership boundaries, and required desktop/mobile behavior are visually supported.

If the gate fails, use **Content Review Demo**. Do not create custom brand header, marketplace navigation, rounded-card page system, invented buy-box, custom tabs, or generic ecommerce chrome and call it Amazon-native.

Review Mode may add non-destructive overlays, but underlying Consumer Mode must remain the verified Amazon shell.

## Mobile rule

Review every gallery image, headline, variation, comparison, expandable element, purchase-control relationship, and enhanced-content region on mobile. For downloadable review demos, use native HTML or CSS-safe fallbacks for essential interactions when JavaScript execution is uncertain.

## Output additions

Record:

- marketplace site/account type;
- capability status/verification date;
- editable-slot map;
- selected module families;
- content ownership boundary;
- Channel Frontend Reference Pack and Primary Reference;
- Approved Asset Registry and Asset-to-Slot Contract;
- Project State Manifest;
- locked Amazon module plan and `plan_hash`;
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE`;
- external-validator results for `CHANNEL_MODULE_BUDGET_GATE`, `APPROVAL_PROVENANCE_GATE`, `MODULE_ORIGIN_GATE`, `TRANSFORM_AUTH_GATE`, `ASSET_SLOT_GATE`, and `DELIVERY_PARITY_GATE`;
- `FRONTEND_FIDELITY_GATE` result;
- mobile QA result;
- open channel-policy/frontend questions.
