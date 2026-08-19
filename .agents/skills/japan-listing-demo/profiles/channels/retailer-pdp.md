# Japan retailer PDP profile

## Use when

Select this profile when a Japanese retailer controls the product-detail template and the brand supplies a defined content package.

## Verify before planning

Confirm with current retailer documentation, the account team, and a live page capture:

- which fields, media, enhanced areas, specifications, comparisons, and support content the brand can provide;
- retailer-controlled title, pricing, inventory, delivery, review, recommendation, and merchandising areas;
- asset dimensions, file formats, character limits, naming conventions, and submission workflow;
- current category template and mobile rendering;
- retailer approval, revision, and content-refresh process.

Do not assume that one retailer's template or ownership model applies to another.

## Frontend reference rule

When a retailer **channel-native demo** is requested, read `references/channel-native-demo.md` and build a **Channel Frontend Reference Pack**.

At Stage 5.5:

- ask whether the user has a preferred current retailer **Reference URL**, product page, approved screenshot set, or template capture;
- use a supplied current page as the candidate **Primary Reference**;
- if none is supplied, inspect 1–3 current comparable product pages from that retailer and recommend a Primary Reference;
- visually capture material retailer shell, brand-content placement, product/offer controls, section order, and mobile behavior;
- keep retailer capability/submission documentation separate from Frontend Visual evidence.

Official retailer rules do not substitute for current consumer-facing visual evidence.

## Content roles

| Area | Primary role |
|---|---|
| Retailer-controlled product identity | Search, merchandising, and catalog consistency |
| Brand-supplied media | Product and offer understanding |
| Brand-supplied enhanced content | Benefits, mechanism, proof, and conditions |
| Structured specifications | Factual verification and comparison |
| Support information | Compatibility, setup, service, and purchase-barrier removal |

## Planning rule

Create a retailer content contract before designing. It must list:

- editable field;
- owner;
- format and limit;
- evidence source;
- update frequency;
- approval path;
- mobile behavior.

Plan only confirmed brand-controlled areas. Record all other areas as retailer-controlled or `UNKNOWN`.

For a retailer channel-native demo, reproduce the verified retailer shell and section order first. Place brand content only into verified brand-controlled regions. If `FRONTEND_FIDELITY_GATE` fails, deliver a clearly named **Content Review Demo** rather than inventing retailer-native chrome.

## Localization rule

Follow the retailer's terminology and formatting requirements when they differ from the general locale reference, while preserving approved product facts and claim conditions.

## Mobile rule

Review retailer image crops, specification tables, accordions, comparisons, external asset links, and observed responsive reordering on mobile. Provide a fallback when the retailer strips unsupported markup or interaction.

## Output additions

Record:

- retailer and current template;
- brand-controlled versus retailer-controlled content map;
- content contract and submission format;
- **Channel Frontend Reference Pack** and Primary Reference;
- frontend fidelity status and `FRONTEND_FIDELITY_GATE` when a native demo is requested;
- approval and refresh workflow;
- mobile QA result;
- unresolved retailer or frontend dependencies.
