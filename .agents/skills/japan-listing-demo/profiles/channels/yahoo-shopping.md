# Yahoo! Shopping channel profile

## Use when

Select this profile for a Yahoo! Shopping product page, store-controlled page, or campaign content area.

## Verify before planning

Confirm from the current store account, official guidance, and live page structure:

- editable product information, images, video, specifications, options, store content, and campaign areas;
- current template, feed, integration, and image constraints;
- platform-generated versus merchant-controlled content;
- current publishing, approval, and policy rules;
- mobile rendering and app-web differences where relevant.

Do not assume a fixed page structure from an old capture or another merchant.

## Frontend reference rule

When a Yahoo! Shopping **channel-native demo** is requested, read `references/channel-native-demo.md` and build a **Channel Frontend Reference Pack**.

At Stage 5.5:

- ask whether the user has a preferred current **Reference URL**, store page, product page, or screenshot set;
- use a supplied page as the candidate **Primary Reference**;
- if none is supplied, inspect 1–3 current comparable consumer-facing pages and recommend one Primary Reference;
- visually capture material shell, section order, option behavior, store/platform-owned areas, and mobile/app-web behavior;
- keep Platform Capability evidence separate from Frontend Visual evidence.

Official rules do not substitute for current consumer-facing visual evidence.

## Content roles

| Area | Primary role |
|---|---|
| Product identity | Product and offer recognition |
| Merchant-controlled media | Fast visual persuasion and proof |
| Description / enhanced area | Mechanism, use context, evidence, and conditions |
| Structured attributes | Factual verification and filtering |
| Options / variations | Validated offer selection |
| Store or campaign area | Portfolio, promotion, and routing when confirmed |

## Planning rule

Create the editable-slot map from the current store interface and live page. Mark unavailable or uncertain fields as `UNKNOWN` or `PENDING`.

For a channel-native demo, reproduce the verified Yahoo! Shopping shell before inserting project content. If `FRONTEND_FIDELITY_GATE` fails, deliver a clearly named **Content Review Demo** rather than a fabricated native page.

Separate evergreen product content from volatile price, inventory, coupon, and campaign content.

## Mobile rule

Test image crops, text density, option selection, store navigation, long-form descriptions, and observed desktop/mobile reordering. Avoid relying on desktop-only side-by-side layouts for primary meaning.

## Output additions

Record:

- store and page target;
- editable fields and ownership;
- template and integration constraints;
- **Channel Frontend Reference Pack** and Primary Reference;
- frontend fidelity status and `FRONTEND_FIDELITY_GATE` when a native demo is requested;
- evergreen versus commercial-content split;
- mobile QA result;
- open platform, account, or frontend questions.
