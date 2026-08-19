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

A high-fidelity Amazon PDP demo therefore requires both:

1. current capability/ownership evidence; and
2. a current Amazon.co.jp frontend reference that visually proves the material shell and section order.

## Frontend reference intake

When an Amazon.co.jp channel-native demo is requested, read `references/channel-native-demo.md`.

At Stage 5.5, ask whether the user has a preferred current **Reference URL** or ASIN.

- If supplied, record it as the candidate **Primary Reference**.
- If not supplied, research 1–3 current comparable Amazon.co.jp PDPs and recommend one Primary Reference.
- Use current visual inspection or supplied screenshots/PDFs to establish the frontend shell.
- If Amazon blocks live access, do not infer fidelity from text/DOM or official documentation alone. Use a supplied capture or clearly identified secondary reference for gaps, otherwise mark fidelity `PARTIAL`, `UNKNOWN`, or `BLOCKED`.

## Frontend anatomy to capture

Capture enough evidence to establish, where present on the current reference:

- Amazon/global page chrome relevant to the PDP context;
- breadcrumb/category trail when material;
- product media/gallery region;
- product title, brand/store link, rating/review summary, price/offer information, and bullet region;
- variation/option controls;
- Featured Offer / purchase controls and other offer regions;
- brand-controlled story/enhanced-content entry points;
- product description / A+ placement;
- specifications or product information regions;
- platform-controlled recommendations, reviews, sponsored, or merchandising blocks that affect section order;
- desktop and mobile/app-web reordering.

The demo does not need to reproduce every Amazon-owned data point, but its shell, ordering, hierarchy, and ownership boundaries must come from the locked reference evidence rather than original web design.

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

## Planning rule

Use the exact module families visible in the current account. If a module cannot be verified, record it as `UNKNOWN` rather than mapping content to a guessed structure.

`Message != Module`. Pack several related messages into one supported carousel, hotspot, video, comparison, or expandable structure when the current account provides it.

For channel-native demo work, map each planned region to the locked **Channel Frontend Reference Pack**. A message-to-module plan does not authorize inventing an Amazon frontend shell.

## Frontend Fidelity Gate

Immediately before Stage 9, run `FRONTEND_FIDELITY_GATE`.

A deliverable may be labeled an Amazon.co.jp PDP/channel-native demo only when the Primary Reference, material consumer-facing shell, section order, ownership boundaries, and required desktop/mobile behavior are visually supported.

If the gate fails, use the fallback name **Content Review Demo**. Do not create a custom brand header, custom marketplace navigation, rounded-card page system, invented buy-box, custom tabs, or generic ecommerce chrome and call it Amazon-native.

Review Mode may add non-destructive overlays for internal status, but the underlying Consumer Mode layout must remain the verified Amazon shell.

## Mobile rule

Review every gallery image, headline, variation, comparison, expandable element, purchase-control relationship, and enhanced-content region on mobile. For downloadable review demos, use native HTML or CSS-safe fallbacks for essential interactions when JavaScript execution is uncertain.

## Output additions

Record:

- marketplace site and account type;
- capability status and verification date;
- editable-slot map;
- selected module families;
- content ownership boundary;
- **Channel Frontend Reference Pack**;
- Primary Reference URL / ASIN / supplied capture;
- desktop/mobile frontend evidence and fidelity status;
- `FRONTEND_FIDELITY_GATE` result when a native demo is requested;
- mobile QA result;
- open channel-policy or frontend questions.
