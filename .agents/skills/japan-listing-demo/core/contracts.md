# Output contracts

## Project Definition

```yaml
market:
  country: DE
locale:
  id: de-DE
region_overlays:
  - EU
channel:
  type: amazon
  site: amazon.de
category: project-defined
product:
  name: Product name or placeholder
offers:
  - single
  - kit
page_targets:
  - single-listing
  - kit-listing
output:
  - strategy
  - module-plan
  - interactive-demo
```

## Selected Profiles

| Layer | Profile | Why selected | Verified source | Status |
|---|---|---|---|---|

## Source Registry

| Source ID | Product / Offer | Type | Version/date | Authority | Completeness | Allowed usage | Downstream dependency |
|---|---|---|---|---|---|---|---|

Use authorities such as `product fact`, `commercial decision`, `marketing decision`, `consumer evidence`, `locale reference`, `channel reference`, and `visual reference`.

## Asset Readiness Preflight

| Asset class | Required for | Received | Source | Quality/status | Needed by stage | Blocking? |
|---|---|---:|---|---|---|---:|

Create this in Stage 1 for asset classes the current project is expected to need.

## Fact Ledger

| Domain | Fact | Value | Conditions | Source | Status | Offer/page scope | Claim readiness |
|---|---|---|---|---|---|---|---|

Statuses: `CONFIRMED`, `CONDITIONAL`, `INHERITED-PENDING`, `CONFLICT`, `MISSING`, and `PROHIBITED`.

## Conflict Ledger

| ID | Field | Evidence A | Evidence B | Impact | Resolution owner | Temporary rule |
|---|---|---|---|---|---|---|

## Change Impact Map

| Changed source / decision | Dependent output | Stage/item | Impact | Action | Reason |
|---|---|---|---|---|---|

Impact values: `UNAFFECTED`, `REVIEW`, `INVALIDATED`, `REOPEN`.

## Market Evidence Registry

| Need state / language / behavior | Market | Locale | Channel | Category | Evidence | Evidence type | Confidence | Permitted use |
|---|---|---|---|---|---|---|---|---|

A country label without evidence cannot populate this table.

## Page Target / Product Boundary Matrix

| Capability or message | Offer A | Offer B | Bundle | Evidence owner | Notes |
|---|---:|---:|---:|---|---|

A blank cell means the page must not inherit that capability.

## Consumer Strategy

```yaml
target_user:
jtbd:
pain_points:
purchase_barriers:
benefits:
reasons_to_believe:
differentiator:
message_priority:
  p0:
  p1:
  p2:
assumptions:
confirmed_by_user:
```

## Message-to-Slot Matrix

| Message | Slot 1 | Slot 2 | Slot 3 | Comparison | Objection handling |
|---|---:|---:|---:|---:|---:|

Use priority and role, not only binary presence.

## Approved Asset Registry

| Asset ID | Canonical source | Role | Dimensions/aspect | Page/offer scope | Allowed slots | Approval status | Derivative of | Transform rule |
|---|---|---|---|---|---|---|---|---|

Approved assets are stable downstream inputs. A material crop/recomposition/role change creates a derivative with a new Asset ID and provenance.

## Asset Manifest

| Asset ID | Object | Source | Quality | Evidence supported | Usable slots | Status | Replacement required |
|---|---|---|---|---|---|---|---|

## Asset-to-Slot Contract

| Slot ID | Page/offer | Channel region/module | Message role | Required Asset ID | Required dimensions/aspect | Crop/transform rule | Interaction | Ownership |
|---|---|---|---|---|---|---|---|---|

Run `ASSET_SLOT_GATE` before final visual adaptation and Demo Assembly.

## Channel Slot / Module Plan

| Slot | Channel module family | Message role | Interaction | Evidence | Existing asset | Asset to create | Claim gate | Module-fit rationale |
|---|---|---|---|---|---|---|---|---|

`CONTENT_COVERAGE` and `MODULE_FIT_GATE` are separate results.

## Visual Evidence Matrix

| Module/tab | Main message | Visual subject | Evidence object | Asset | Alignment result |
|---|---|---|---|---|---|

`PASS` requires the visual to directly prove the copy. A packshot, product quantity, lifestyle scene, UI, and mechanism diagram are not interchangeable evidence.

## Differentiator Proof Matrix

| P0 differentiator | Priority visual | Evidence | Strength | Gate result |
|---|---|---|---|---|

Strength values: `DIRECT`, `INDIRECT`, `WEAK`, `NONE`.

## Planned-to-Implemented Parity

| Check | Planned | Implemented | Result |
|---|---|---|---|
| Slot/module |  |  |  |
| Interaction |  |  |  |
| Source Asset ID |  |  |  |
| Dimensions/aspect |  |  |  |
| Message coverage |  |  |  |
| Page/offer ownership |  |  |  |
| Channel region |  |  |  |

Run `DELIVERY_PARITY_GATE` before a demo is called complete.

## Stage Completion Manifest

| Field | Value |
|---|---|
| Stage |  |
| Planned deliverables |  |
| Completed |  |
| Approved / locked |  |
| Needs revision |  |
| Missing |  |
| Blocked |  |
| Open items |  |
| Stage status | `COMPLETE` / `PARTIAL` / `BLOCKED` |

A completed subset does not make a stage complete. A Transition Command may lock a `PARTIAL` stage, but does not relabel it `COMPLETE`.

## Review Mode

| Status | Meaning | Consumer mode |
|---|---|---|
| `LOCKED` | Current evidence supports formal production | Content visible, badge hidden |
| `PENDING CLAIM` | Requires product, commercial, legal, or test confirmation | Claim hidden or neutralized |
| `DEMO ASSET` | Visual direction only | Internal label hidden; replace before release |
| `PROVISIONAL UI` | Temporary interface evidence | Internal label hidden; replace before release |
| `NEEDS REVISION` | Produced but not accepted or parity-safe | Internal label hidden; cannot be treated as final |
