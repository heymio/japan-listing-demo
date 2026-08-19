# Delivery integrity contract

## Purpose

Use this reference to prevent structurally complete but operationally wrong listing deliverables: partial stages presented as complete, approved assets replaced downstream, assets mapped into the wrong slot, topic coverage mistaken for module fit, planned interactions lost in the demo, P0 differentiators disappearing visually, and large rework after late evidence changes.

These rules are category-neutral and apply across Japan channels, DTC, and retailer PDP work.

## Stage Completion Manifest

Every numbered workflow stage must end with a **Stage Completion Manifest** before the Major Stage Checkpoint.

Record:

| Field | Requirement |
|---|---|
| Stage | Number and name |
| Planned deliverables | Items/counts agreed or implied by the locked stage plan |
| Completed | Items actually produced |
| Approved / locked | User-approved items or locked snapshots |
| Needs revision | Produced but not accepted items |
| Missing | Planned items not produced |
| Blocked | Items prevented by missing evidence/capability |
| Open items | Non-blocking unresolved work |
| Stage status | `COMPLETE`, `PARTIAL`, or `BLOCKED` |

A completed subset does not make the stage complete. If gallery work is finished but planned enhanced content or other deliverables are missing, the stage is `PARTIAL`.

A Transition Command may lock a `PARTIAL` stage for downstream work. It does not rewrite `PARTIAL` as `COMPLETE`; unresolved items stay visible and dependent final deliverables remain gated.

## Asset Readiness Preflight

During Stage 1, create an **Asset Readiness Preflight** for asset classes that later stages are expected to need. Do not wait until visual production or demo assembly to discover critical evidence is missing.

Record:

| Asset class | Required for | Received | Source | Quality/status | Needed by stage | Blocking? |
|---|---|---:|---|---|---|---:|

Only include asset classes relevant to the current project. Typical classes may include product render/photography, UI, packaging, diagrams, gallery-native assets, enhanced-content assets, video/storyboard sources, channel frontend captures, brand assets, and approved copy.

Missing assets do not automatically stop all work, but their downstream impact must be explicit.

## Approved Asset Registry

Once an asset is approved or locked, treat it as a stable downstream input.

Record:

| Asset ID | Canonical source | Role | Dimensions/aspect | Page/offer scope | Allowed slots | Approval status | Derivative of | Transform rule |
|---|---|---|---|---|---|---|---|---|

Rules:

1. An **approved asset** must be referenced by stable `Asset ID` downstream.
2. Demo Assembly must reuse the exact approved asset assigned to a slot unless the user explicitly approves a replacement or derivative.
3. Cropping, resizing, recomposition, text replacement, background replacement, or changing an asset from one channel role to another creates a derivative when the transformation can affect meaning, evidence, framing, dimensions, or slot suitability.
4. A derivative gets a new Asset ID, records `Derivative of`, and cannot silently replace the approved original.
5. Visual convenience is not permission to substitute an enhanced-content asset for a gallery-native asset, or vice versa.

## Asset-to-Slot Contract

After channel slots/modules are known, create an **Asset-to-Slot Contract**.

| Slot ID | Page/offer | Channel region/module | Message role | Required Asset ID | Required dimensions/aspect | Crop/transform rule | Interaction | Ownership |
|---|---|---|---|---|---|---|---|---|

Run `ASSET_SLOT_GATE` before final visual adaptation and again before Demo Assembly.

`ASSET_SLOT_GATE = FAIL` when, for example:

- the source Asset ID does not match the locked slot assignment;
- the asset belongs to another page/offer/slot class;
- dimensions/aspect or crop rules are violated;
- a derivative was introduced without provenance/approval;
- a platform-controlled region is populated as if it were a brand-controlled asset.

Do not fix a failed slot by silently cropping until it fits.

## Content Coverage and Module Fit are separate

Run these independently:

### `CONTENT_COVERAGE`

Checks whether every required P0/P1 message, objection, proof point, and planned content topic has a valid home in the channel plan.

### `MODULE_FIT_GATE`

Checks whether the chosen verified native module/component is actually appropriate for the message and evidence.

Evaluate module fit using:

- verified current module availability;
- message grouping and reading sequence;
- whether interaction adds decision value;
- asset orientation and density;
- evidence objects required;
- mobile behavior;
- frontend-reference evidence;
- channel ownership and module constraints.

`CONTENT_COVERAGE = PASS` does not imply `MODULE_FIT_GATE = PASS`.

Independent static boards must not be mechanically grouped, sliced, or converted into a carousel/slide interaction during Demo Assembly. If a carousel, hotspot, video, comparison, accordion, or other native interaction is selected, its interaction logic and content packing must be designed in Stage 7 and Stage 7.5 before production.

## Planned-to-Implemented Parity

Before a demo is called complete, run `DELIVERY_PARITY_GATE`.

Compare the locked plan against implementation:

| Check | Planned | Implemented | Result |
|---|---|---|---|
| Slot/module |  |  |  |
| Interaction |  |  |  |
| Source Asset ID |  |  |  |
| Dimensions/aspect |  |  |  |
| Message coverage |  |  |  |
| Page/offer ownership |  |  |  |
| Channel region |  |  |  |

`DELIVERY_PARITY_GATE = FAIL` if a planned carousel/hotspot becomes static, a planned module disappears, a wrong asset is used, the wrong dimensions/crop are applied, or a planned message loses its mapped implementation.

A functioning HTML file is not evidence of parity.

## P0 differentiator visual proof

Consumer Strategy identifies P0 purchase reasons and differentiators. Visual QA must evaluate whether those reasons are actually proven, not merely mentioned.

For each P0 differentiator, classify strongest visual evidence as:

- `DIRECT` — the visual directly demonstrates or proves the differentiator;
- `INDIRECT` — supportive but not decisive;
- `WEAK` — loosely related lifestyle/context only;
- `NONE` — no visual evidence.

Run `DIFFERENTIATOR_PROOF_GATE` before Stage 8 is complete.

At least one priority visual should provide `DIRECT` proof for each visualizable P0 differentiator, or the user must explicitly approve another proof strategy. Attractive generic lifestyle imagery does not automatically pass this gate.

## Change Impact Map and targeted reopen

A locked stage is stable, not immutable against new authoritative evidence.

Trigger a **Change Impact Map** when one of these materially changes:

- authoritative product/commercial fact;
- user-approved strategy or offer decision;
- page/offer boundary;
- approved asset or UI evidence;
- channel capability or frontend reference;
- claim/legal decision.

Record affected outputs with one of:

- `UNAFFECTED` — preserve locked output;
- `REVIEW` — verify but do not automatically redo;
- `INVALIDATED` — cannot be used downstream as-is;
- `REOPEN` — rerun this stage/item.

Trace dependencies from the changed source to messages, slots/modules, assets, visuals, and demo regions. Reopen only impacted work. Do not ignore new evidence because a stage was locked, and do not restart the entire project when unaffected work remains valid.

## Final completion rule

A final listing/demo may be called complete only when:

- required Stage Completion Manifests are not falsely marked complete;
- required planned deliverables exist or have an explicitly user-approved reduced scope;
- `ASSET_SLOT_GATE` passes;
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes for selected native modules;
- `DIFFERENTIATOR_PROOF_GATE` passes or has an explicit approved alternative;
- `DELIVERY_PARITY_GATE` passes;
- channel-native work also satisfies `FRONTEND_FIDELITY_GATE`;
- open items are separated from passed checks.

Do not convert missing work into a success label merely because the current artifact looks polished.