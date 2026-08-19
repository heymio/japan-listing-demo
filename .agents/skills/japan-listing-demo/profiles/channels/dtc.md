# Japan DTC product-page profile

## Use when

Select this profile for a brand-controlled Japan-market product page, landing page, launch page, or ecommerce product experience.

## Verify before planning

Confirm:

- the actual CMS and component library;
- available analytics, experimentation, personalization, and localization capabilities;
- checkout, pricing, inventory, account, support, and service ownership;
- current performance, accessibility, privacy, and legal requirements;
- desktop, mobile web, and app-web behavior where applicable.

## Frontend reference rule

When the requested deliverable is a DTC **channel-native demo**, read `references/channel-native-demo.md` and establish a **Channel Frontend Reference Pack**.

The best Primary Reference may be the current live brand PDP, approved design system, component library, or an approved redesign reference rather than a competitor page.

At Stage 5.5:

- ask whether the user has a preferred current **Reference URL**, design file, component-library reference, or screenshot set;
- use a supplied approved brand reference as the candidate **Primary Reference**;
- if none is supplied, inspect the current live DTC experience and relevant current page types before inventing a new shell;
- capture material desktop/mobile structure, conversion controls, navigation context, and component behavior;
- keep CMS/component capability evidence separate from Frontend Visual evidence.

Official or internal component documentation does not substitute for visual evidence of the intended consumer-facing page when high frontend fidelity is requested.

## Content roles

A DTC page may use a flexible sequence such as:

- product identity and primary promise;
- reasons to buy;
- mechanism and proof;
- use contexts;
- offer and variation selection;
- comparison;
- compatibility and service information;
- support, FAQ, and CTA.

This is a planning pattern, not a fixed template. Use the current design system and conversion path.

## Planning rule

Define the minimum page sequence required to make the purchase decision. Do not reproduce marketplace modules when the DTC system provides a better native structure.

For a DTC channel-native demo, reproduce the locked Primary Reference/design-system shell before inserting project content. If `FRONTEND_FIDELITY_GATE` fails, deliver a clearly named **Content Review Demo** rather than claiming production-site fidelity.

Separate product truth, brand narrative, commercial offer, and service terms so volatile content can change without rewriting stable product evidence.

## Localization rule

When `locale.id: ja-JP`, apply the localization reference and native-copy review. Do not infer category messaging or visual settings from the market alone.

## Mobile and performance rule

- Design mobile-first reading order.
- Keep primary actions reachable and understandable.
- Avoid text embedded in images when live text is available.
- Verify image weight, interaction cost, layout shift, keyboard access, and reduced-motion behavior.
- Preserve complete meaning when optional animation or video does not load.
- Compare material responsive behavior against the locked frontend reference when native fidelity is requested.

## Output additions

Record:

- CMS and component constraints;
- page sequence and conversion objective;
- product, brand, commercial, and service content ownership;
- **Channel Frontend Reference Pack** and Primary Reference for native demos;
- frontend fidelity status and `FRONTEND_FIDELITY_GATE` when applicable;
- analytics and experiment plan when requested;
- accessibility, performance, and mobile QA;
- open implementation or frontend dependencies.
