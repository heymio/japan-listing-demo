# Final Demo output contract

## Required delivery shape

The final project Demo is delivered as **one single standalone HTML file**.

Default final delivery:

```text
<project>-listing-demo.html
```

Do not deliver the project Demo as a ZIP and do not require an adjacent `assets` folder. Skill-distribution ZIPs are separate installation artifacts and are not the project Demo deliverable.

## Standalone file requirements

The HTML must run when opened by itself without local or network asset dependencies.

- **Embedded images:** raster images use `data:image/...` URIs; SVG may be inline.
- CSS is inline in the HTML. No external/local stylesheet dependency.
- JavaScript is inline in the HTML. No external/local script dependency.
- CSS `url(...)`, video/audio/source/iframe/object/embed dependencies must not point to adjacent local files or required network resources.
- Review Mode, if present, stays inside the same HTML file and must not alter Consumer Mode layout.

Run the deterministic validator on the exact final file:

```bash
python .agents/skills/listing-hardening/scripts/validate_demo_html.py <project>-listing-demo.html --json
```

A non-PASS result blocks final delivery until corrected.

## Carousel verification

Every planned carousel must be functional in the final HTML, not represented as a static visual only.

Minimum contract:

- one carousel root;
- at least two slides when carousel interaction is planned;
- previous/next button controls;
- inline JavaScript click wiring;
- controls remain usable at desktop and mobile widths.

Static conformance from `validate_demo_html.py` is necessary but not sufficient for final QA. Before delivery, open the exact final HTML in a browser and exercise every carousel in both directions.

## Mobile / responsive verification

The final file must include a `width=device-width` viewport and responsive CSS.

Runtime verification must include at least:

- **1440px** desktop viewport;
- **390px** mobile viewport.

At both widths verify:

- no horizontal overflow;
- no broken images;
- no clipped primary copy or controls;
- carousel previous/next controls operate;
- content order remains the approved order;
- image/text pairing remains correct;
- Review Mode, when enabled, does not reflow or corrupt the consumer layout.

If browser/runtime verification cannot be performed, the Demo QA state is **BLOCKED**. Do not claim carousel or mobile verification passed from static source inspection alone.

## Final handoff

The user-facing handoff links the single `.html` file directly. Do not require the recipient to unzip a package, preserve folder structure, or repair relative image paths before review.
