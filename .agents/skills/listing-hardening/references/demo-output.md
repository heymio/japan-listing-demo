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

- raster images use embedded `data:image/...` URIs;
- SVG may be inline, but inline `<image>` / `<use>` references cannot depend on external/local URLs;
- CSS is inline; no external/local stylesheet dependency;
- JavaScript is inline; no external/local script dependency;
- CSS `url(...)`, including inline `style="..."`, must not depend on local/network/session-only resources;
- video/audio/source/iframe/object/embed resources must be physically embedded when used;
- Review Mode, if present, stays inside the same HTML file and must not alter Consumer Mode layout.

Run static preflight on the exact final file:

```bash
python3 .agents/skills/listing-hardening/scripts/validate_demo_html.py <project>-listing-demo.html --json
```

A static FAIL blocks delivery. A static PASS proves standalone structure only; it does not prove browser interaction.

## Carousel verification

Every planned carousel must be functional in the final HTML, not represented as a static visual only.

Static preflight checks the presence and consistency of carousel structure. When carousel markup exists, the static result is **runtime-required**, not interaction hard-PASS. JavaScript keywords or unused strings do not constitute interaction evidence.

Final interaction proof comes from the no-network browser runtime validator:

```bash
python3 .agents/skills/listing-hardening/scripts/validate_demo_runtime.py \
  <project>-listing-demo.html \
  --output demo-runtime-evidence.json
```

If the browser runtime dependency is unavailable, this command returns **BLOCKED** rather than fabricating PASS.

## Exact-Demo binding

Runtime evidence must be bound to the SHA-256 of the exact final `.html` file. `DEMO_RUNTIME_GATE` rejects evidence for a different Demo SHA.

Any material edit to the final HTML after runtime QA invalidates the prior runtime evidence and requires another browser run.

## No-network browser verification

The runtime validator opens the local file and blocks HTTP/HTTPS requests. A hard-PASS requires zero observed network requests.

Runtime verification includes at least:

- **1440px** desktop viewport;
- **390px** mobile viewport.

At both widths verify:

- no horizontal overflow;
- no broken images;
- no clipped primary copy or controls.

When carousel markup exists, also verify:

- clicking next causes an actual visible-slide transition;
- clicking previous returns to the prior visible state.

Project review may also inspect approved content order, image/text pairing, and Review Mode behavior. Machine browser evidence does not replace human creative review.

## Gate semantics

Static preflight and runtime proof answer different questions:

```text
validate_demo_html.py     → is the file structurally standalone and responsive?
DEMO_RUNTIME_GATE         → did this exact file actually render and interact correctly in a no-network browser?
```

If browser/runtime verification cannot be performed, the Demo runtime state remains **UNVERIFIED/BLOCKED**. Do not claim carousel or mobile hard verification passed from source inspection alone.

## Final handoff

The user-facing handoff links the single `.html` file directly. Do not require the recipient to unzip a package, preserve folder structure, or repair relative image paths before review.
