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

## Project State Manifest

Executable gates use one machine-readable JSON state document. Start from `templates/project-state.example.json`.

Minimum sections:

```json
{
  "schema_version": "0.1",
  "channel": {},
  "approval_events": [],
  "assets": [],
  "locked_module_plan": {},
  "asset_slot_contract": [],
  "implementation": {}
}
```

The **Project State Manifest** is source state, not a place to write gate verdicts. Any `declared_gate_results` field is ignored by `scripts/validate_project_state.py`.

### Approval event contract

```json
{
  "approval_id": "AP-001",
  "actor": "user",
  "source_ref": "checkpoint:identifier",
  "scope": "module_plan",
  "stage": "7",
  "approved_hash": "sha256-of-canonical-approved-state"
}
```

Approval is bound to the exact approved state through `approved_hash`. If the hashed state changes, the old approval does not validate the new state.

### Locked module-plan contract

Each planned module records:

- stable `module_id`;
- verified `native_type`;
- `interaction`;
- exact `asset_ids`;
- `approved_stage`.

The enclosing plan records `status: LOCKED`, `approval_id`, and the canonical `plan_hash`.

Stage 9 implementation records the exact consumed `plan_hash` and implemented slots. It must not add modules or change interaction/type/assets and then retroactively rewrite the plan.

### Asset-lock and recovery contract

A `LOCKED` asset requires:

- valid lowercase SHA-256;
- either a matching user approval event for `asset_lock:<Asset ID>`;
- or exact recovery where current SHA-256 equals the recorded previous locked SHA-256.

Filename similarity and visual resemblance are not exact recovery.

### Transform authorization contract

A locked derivative records `derivative_of` and a transform object containing transform type, target slot, approval ID, and approved stage. The matching approval event is scoped to `transform:<Asset ID>` and hashes the canonical transform state.

Deterministic execution does not itself authorize a crop/recomposition/role change.

## Executable gate output

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

Computed gates include:

- `CHANNEL_MODULE_BUDGET_GATE`;
- `APPROVAL_PROVENANCE_GATE`;
- `MODULE_ORIGIN_GATE`;
- `TRANSFORM_AUTH_GATE`;
- `ASSET_SLOT_GATE`;
- `DELIVERY_PARITY_GATE`.

If validator execution is unavailable, these gates are `UNVERIFIED`; they must not be manually self-declared PASS.

## Review Mode

| Status | Meaning | Consumer mode |
|---|---|---|
| `LOCKED` | Current evidence supports formal production | Content visible, badge hidden |
| `PENDING CLAIM` | Requires product, commercial, legal, or test confirmation | Claim hidden or neutralized |
| `DEMO ASSET` | Visual direction only | Internal label hidden; replace before release |
| `PROVISIONAL UI` | Temporary interface evidence | Internal label hidden; replace before release |
| `NEEDS REVISION` | Produced but not accepted or parity-safe | Internal label hidden; cannot be treated as final |
| `UNVERIFIED` | Executable validation could not run or lacks packaged policy | Must not be treated as machine-validated PASS |
