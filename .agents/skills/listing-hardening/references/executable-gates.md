# Executable gates

## Purpose

Hardening computes delivery verdicts from machine-readable source state. Agent-authored gate results are not authoritative.

Canonical validator:

```text
.agents/skills/listing-hardening/scripts/validate_delivery_state.py
```

The legacy `japan-listing-demo/scripts/validate_project_state.py` path remains a compatibility shim for Project State 0.1.

## Canonical gate set

The Delivery State 0.2 validator computes:

- `SCHEMA_GATE`
- `CHANNEL_MODULE_BUDGET_GATE`
- `APPROVAL_PROVENANCE_GATE`
- `MODULE_ORIGIN_GATE`
- `TRANSFORM_AUTH_GATE`
- `EVIDENCE_RECONCILIATION_GATE`
- `PRODUCTION_FREEZE_GATE`
- `ASSET_SLOT_GATE`
- `PRE_DEMO_ASSET_GATE`
- `FRONTEND_FIDELITY_GATE`
- `DEMO_RUNTIME_GATE`
- `DELIVERY_PARITY_GATE`

## Fail-closed Demo rule

Delivery State `0.2` is the Demo-delivery schema. Pre-Demo hardening is mandatory by workflow and cannot be disabled by caller-authored `pre_9_required=false`. A Demo state with an empty required Asset-ID set cannot pass.

Required Asset IDs are derived as a union across authoritative plan, implementation, Asset-to-Slot Contract and blocker/revision state. A non-empty contract cannot hide a required asset that still exists in the locked plan or implementation.

## CHANNEL_MODULE_BUDGET_GATE

Compare the locked module count with the packaged current channel limit. A project may lower a verified limit but may not raise packaged policy by editing its state.

## MODULE_ORIGIN_GATE

Stage 9 consumes the exact locked module plan and canonical plan hash. Unplanned modules, omitted planned modules, native-type drift, interaction drift, or a different plan hash fail the gate.

## TRANSFORM_AUTH_GATE

A derivative must have valid transform provenance and approval. Deterministic crop/reframe behavior is still a transform.

## EVIDENCE_RECONCILIATION_GATE

For fresh projects, post-6.5 full audit is not required by default and this gate may be `N/A`. If Planning explicitly requests a targeted early audit for an inherited/reused exact asset, the gate becomes authoritative and missing auditor evidence is `UNVERIFIED`.

## PRODUCTION_FREEZE_GATE

Production Freeze is a creative-state boundary, not physical evidence. In v0.3.3 it must nevertheless be internally exact:

- positive `expected_assets` equals the full required Asset-ID set;
- `user_approved_assets` exactly equals that set;
- `blocked_assets` and `revision_pending` are empty;
- `set_qa_status` is `CLEAR` or `USER_ACCEPTED`;
- `ready_for_hardening` is true;
- `approved_outputs` maps every required Asset ID to the exact selected `candidate_id` and exact `output_ref`.

A stale Set QA record or missing exact output binding fails the gate.

## PRE_DEMO_ASSET_GATE

At Stage 8.5 the full final asset set must be audited. Every required asset must be final-consumable under auditor evidence and the auditor asset-set result must pass. Creative approval alone cannot satisfy this gate.

## ASSET_SLOT_GATE

The implementation must use the exact required Asset IDs in the exact locked slots. Required Asset IDs must exist in Delivery State `assets`, and an implemented asset-bearing slot cannot silently omit its Asset-to-Slot Contract.

## FRONTEND_FIDELITY_GATE

A claimed channel-native Demo requires current Frontend Visual evidence and matching user approval of the fidelity payload. The gate checks shell/order support, distinction between brand-controlled and platform-controlled regions, desktop structure, mobile scope, evidenced interactions, verified content regions, and absence of fabricated unsupported UI.

When native fidelity cannot be supported, use explicit `CONTENT_REVIEW` mode. It must be labeled as such and may not claim channel-native fidelity.

## DEMO_RUNTIME_GATE

Runtime evidence is bound to the exact final Demo SHA-256. A hard-PASS requires:

- validator identity `browser-runtime`;
- zero HTTP/HTTPS network requests;
- 1440px desktop and 390px mobile evidence;
- no horizontal overflow;
- zero broken images;
- zero clipped primary elements;
- both next and previous carousel transitions when carousel markup is present.

Static source inspection alone cannot satisfy this gate. If browser runtime is unavailable, the gate remains `UNVERIFIED/BLOCKED`.

## DELIVERY_PARITY_GATE

Compare locked plan to implementation for module IDs, native types, interactions, Asset IDs, and required slot coverage. A working HTML file is not delivery parity.

## Failure semantics

- `PASS`: executable conditions are satisfied.
- `FAIL`: known contradiction or missing mandatory condition.
- `UNVERIFIED`: required external/auditor/browser evidence is unavailable or incomplete.
- `N/A`: the gate genuinely does not apply to this schema/project state; `N/A` is not a caller-controlled escape hatch for mandatory Demo gates.

Do not replace `FAIL` or `UNVERIFIED` with prose assertions of success.
