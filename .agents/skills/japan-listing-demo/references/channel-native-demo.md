# Channel-native demo reference contract

## Purpose

Use this reference whenever the requested output is a channel-native product-detail-page, marketplace, retailer, or DTC demo whose shell is expected to resemble a real consumer-facing frontend.

A content plan and a visually polished asset set are not enough to prove channel fidelity. Before assembling a channel-native demo, establish how the current frontend actually looks and behaves.

## Evidence layers

Keep these evidence types separate:

1. **Platform Capability evidence** — official guidance, account UI, retailer specifications, current editable fields, module access, limits, policies, ownership, and publishing workflow.
2. **Frontend Visual evidence** — current consumer-facing page captures that show shell anatomy, section order, spacing, controls, interaction, responsive behavior, and placement of brand-controlled versus platform-controlled regions.
3. **Project Content evidence** — approved product facts, copy, images, UI, offer structure, and visual assets to place into the verified shell.

**Official rules do not substitute for frontend visual evidence.** Official documentation may prove what a channel supports, but it does not by itself prove the exact current desktop/mobile presentation of a consumer-facing page.

## Reference intake

When a **channel-native demo** is a requested deliverable, Stage 5.5 must explicitly check for a preferred current reference before demo assembly.

Ask once at the Stage 5.5 checkpoint:

> Do you have a current reference URL, ASIN, retailer page, store page, screenshot set, or approved frontend capture that this demo should follow?

If the user provides one, record it as the **Primary Reference** unless it is inaccessible, stale, materially different from the requested channel/page type, or unsafe to use. Explain any limitation before substituting another reference.

If the user has no reference, research 1–3 current comparable consumer-facing pages and recommend one Primary Reference. Selection should favor the same channel, page type, category context when relevant, account/content capability level when observable, and a sufficiently complete current frontend.

A secondary reference may fill an explicitly identified evidence gap. It must not silently override the Primary Reference.

## Channel Frontend Reference Pack

Record at minimum:

| Field | Requirement |
|---|---|
| Channel | Exact marketplace, retailer, DTC site, or app-web context |
| Page target | PDP, enhanced-content area, store page, campaign page, or other verified target |
| Capture date | Date the frontend was inspected |
| Primary Reference | Current reference URL / identifier / supplied capture |
| Secondary References | Optional gap-filling references and why each is used |
| Access status | `FULL`, `PARTIAL`, `BLOCKED`, or supplied visual evidence |
| Desktop evidence | Shell anatomy and section order from current visual inspection |
| Mobile evidence | Mobile/app-web anatomy, reorder behavior, or `UNKNOWN` |
| Brand-controlled regions | Areas the project can actually populate |
| Platform-controlled regions | Pricing, reviews, recommendations, merchandising, or other channel-owned areas as applicable |
| Interaction evidence | Gallery, variation, accordion, carousel, tabs, sticky actions, or other observed interactions |
| Responsive evidence | Known layout changes between desktop and mobile |
| Fidelity status | `HIGH`, `PARTIAL`, `UNKNOWN`, or `BLOCKED` |
| Open questions | Missing visual or capability evidence that affects the native demo |

Do not claim pixel-level fidelity when only text/DOM parsing or documentation was available.

## Visual capture rule

For frontend fidelity, prefer visual inspection or screenshots over text-only parsing. Capture the page regions necessary to prove:

- global/channel shell relevant to the target;
- product identity/media area;
- offer/variation controls when relevant;
- brand-controlled content entry points;
- enhanced/long-form content placement;
- platform-controlled blocks that affect page order;
- desktop and mobile differences.

If a live page is blocked by login, anti-bot controls, geo restrictions, or unsupported rendering:

1. do not repeatedly retry the same access path beyond the normal Retry Budget;
2. ask for a screenshot/PDF/reference capture if the user can provide one, or use another current comparable page for explicitly identified gaps;
3. mark unverified regions `UNKNOWN` or fidelity `PARTIAL`;
4. do not invent the missing shell.

## Frontend Fidelity Gate

Run `FRONTEND_FIDELITY_GATE` immediately before Stage 9 when the requested deliverable is channel-native.

### PASS requirements

A native demo may be assembled only when all material items below are supported:

- a Primary Reference is locked;
- the current consumer-facing shell has visual evidence, not only platform documentation;
- material desktop structure is known;
- material mobile/app-web structure is known or explicitly scoped out by the user;
- section order and brand/platform ownership boundaries are known;
- the project content is mapped only into verified editable or demonstrative regions;
- unsupported platform UI is not fabricated as product or brand truth;
- the planned demo can distinguish verified structure from intentionally simplified platform placeholders.

### FAIL behavior

If the gate fails, do not generate or label the result as a channel-native PDP/demo.

Allowed fallback:

`Content Review Demo`

A Content Review Demo may show approved messages, visuals, and module sequencing for review, but it must clearly state that channel frontend fidelity is not validated. It must not fabricate a generic marketplace shell, custom branded navigation, invented cards, tabs, buy-box controls, or other channel UI and present them as native.

## Stage 9 assembly rule

For a verified channel-native demo:

1. reproduce the verified consumer-facing channel shell and section order first;
2. preserve the visual hierarchy and interaction patterns evidenced by the Primary Reference;
3. place approved project assets/copy into verified brand-controlled regions;
4. represent channel-owned regions conservatively as evidenced structure or neutral placeholders;
5. keep internal review labels in **Review Mode** only;
6. ensure Review Mode overlays do not alter the underlying Consumer Mode layout;
7. do not expose internal IA names, module IDs, evidence statuses, or workflow labels as consumer-facing page chrome.

The target is channel fidelity, not an original web-design interpretation of the channel.

## Fidelity status meanings

- `HIGH` — primary shell, material section order, ownership, and desktop/mobile behavior are visually supported.
- `PARTIAL` — enough evidence exists for some native regions, but one or more material areas remain unverified.
- `UNKNOWN` — current frontend presentation was not visually established.
- `BLOCKED` — known missing evidence would make a native demo materially misleading.

Only `HIGH`, or an explicitly user-approved constrained `PARTIAL` scope, may be labeled a channel-native demo.
