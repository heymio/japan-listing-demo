# Rakuten channel profile

## Use when

Select this profile for a Rakuten product page, store page, campaign page, or merchant-controlled content area.

## Verify before planning

Confirm from the current merchant account, store setup, and official guidance:

- which product-page, store, campaign, image, video, specification, variation, and navigation areas are editable;
- current template, page-builder, HTML, image, and mobile constraints;
- merchant, platform, and external-service ownership boundaries;
- current review, publishing, approval, and policy requirements;
- whether the page target is a product detail page, store landing page, campaign page, or a combination.

Do not reuse module names, limits, or ownership assumptions from another marketplace.

## Frontend reference rule

When the requested deliverable is a Rakuten **channel-native demo**, read `references/channel-native-demo.md` and build a **Channel Frontend Reference Pack**.

At Stage 5.5:

- ask whether the user has a current preferred **Reference URL**, store page, product page, or screenshot set;
- use a supplied page as the candidate **Primary Reference**;
- if none is supplied, inspect 1–3 current comparable consumer-facing Rakuten pages and recommend one Primary Reference;
- visually capture the current shell, store/product navigation, editable content areas, section order, and mobile behavior;
- keep Platform Capability evidence separate from Frontend Visual evidence.

Official rules do not substitute for current consumer-facing visual evidence.

## Content roles

| Area | Primary role |
|---|---|
| Product identity area | Product and offer recognition |
| Merchant-controlled images and content | Message sequence, mechanism, proof, and use context |
| Specifications / option controls | Structured facts and offer selection |
| Store navigation | Portfolio discovery and campaign routing |
| Campaign area | Time-bound commercial communication when approved |

The actual editable areas vary by account, template, and implementation. Record unknown areas as `UNKNOWN`.

## Planning rule

Build the slot map from the current page capture and merchant interface. Do not force the page into an Amazon, DTC, or retailer template.

For a channel-native demo, reproduce the verified Rakuten shell first and place project content only into verified merchant-controlled regions. If `FRONTEND_FIDELITY_GATE` fails, deliver a clearly named **Content Review Demo** instead of inventing a native shell.

Separate persistent product content from time-bound campaign content so price, discount, inventory, and offer changes do not invalidate evergreen product claims.

## Mobile rule

Review long images, text embedded in images, navigation, option selection, campaign modules, and observed responsive reordering on mobile. Keep primary benefits and conditions understandable without horizontal zoom.

## Output additions

Record:

- page target type;
- editable areas and ownership;
- current template or builder constraints;
- **Channel Frontend Reference Pack** and Primary Reference;
- frontend fidelity status and `FRONTEND_FIDELITY_GATE` when a native demo is requested;
- evergreen versus campaign content split;
- mobile QA result;
- unresolved merchant, platform, or frontend questions.
