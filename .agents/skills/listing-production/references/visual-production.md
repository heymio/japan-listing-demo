# Visual production

## Artifact-first execution

Produce the requested final asset from the current Asset Packet. One asset should solve one dominant shopper task.

## Product identity

The referenced real product source is authoritative for product identity. Preserve geometry, ports, controls, accessories, packaging, UI, color, material, and proportions when the brief requires exact product evidence.

AI may generate approved environment, lighting, atmosphere, or explanatory layers around the real product source. Do not invent product structure or functional proof.

## Evidence Mode

Every current production job should carry the Planning-assigned `evidence_mode` when using the v0.3.2 handoff.

### SOURCE_FAITHFUL

Use when faithful product/pack/offer identity is intrinsic to the visual role. If the authoritative source required to represent that identity safely is missing, return `BLOCKED` rather than inventing it.

### CREATIVE_MOCK

Use for lifestyle, atmosphere, spatial-use, and concept scenes. The product must remain commercially credible and must not gain contradictory structure, but generated placement/installation details do not become Product Truth or proof.

Missing proof-grade source evidence may produce `READY_WITH_LIMITATION` rather than forcing a creative redesign. The limitation must remain explicit for later Hardening.

### PROOF_VISUAL

Use for factual installation structure, dimensions, interfaces, mechanism, UI, compatibility, or other visual proof. If the required authoritative proof source is missing, return `BLOCKED`; never creatively invent the proof object.

Core rule:

```text
source insufficiency != automatic creative rework
```

## Evidence alignment

The visual subject and proof object must support the primary message in the Asset Packet. Attractive lifestyle imagery is not proof by itself.

## Page Visual System context

The Asset Packet may include only the current asset's `page_visual_direction` plus its nearest same-region neighbors. Use that minimal context to preserve brand art direction while avoiding accidental scene/composition/tone/scale/proof-form repetition.

**Same art direction ≠ same composition.** Do not interpret “continue in this style” as “reuse the previous layout.”

## Missing upstream input

If the Asset Packet is blocked by a missing fact, offer decision, or source asset required by its Evidence Mode, return `BLOCKED` with the missing field. Do not infer or silently rewrite Planning.

## Retry budget

For the same asset and same identified problem, allow at most two autonomous attempts without new input/evidence. After that, stop and request review rather than replacing the requested artifact with a workflow/status graphic.

## Role discipline

Gallery and enhanced-content outputs remain distinct final roles. A shared topic does not authorize cross-role reuse.
