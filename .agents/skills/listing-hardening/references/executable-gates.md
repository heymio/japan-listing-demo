# Executable gates

## Purpose

Hardening computes delivery verdicts from machine-readable source state. Agent-authored gate results are not authoritative.

Canonical validator:

```text
.agents/skills/listing-hardening/scripts/validate_delivery_state.py
```

The legacy `japan-listing-demo/scripts/validate_project_state.py` path is a compatibility shim during migration.

## Gate ownership

The delivery validator may compute:

- `SCHEMA_GATE`
- `CHANNEL_MODULE_BUDGET_GATE`
- `APPROVAL_PROVENANCE_GATE`
- `MODULE_ORIGIN_GATE`
- `TRANSFORM_AUTH_GATE`
- `EVIDENCE_RECONCILIATION_GATE`
- `PRODUCTION_FREEZE_GATE`
- `ASSET_SLOT_GATE`
- `PRE_DEMO_ASSET_GATE`
- `DELIVERY_PARITY_GATE`

## CHANNEL_MODULE_BUDGET_GATE

Compare the locked module count with the packaged current channel limit. A project may lower a verified limit but may not raise packaged policy by editing its state.

## MODULE_ORIGIN_GATE

Stage 9 consumes the exact locked module plan and canonical plan hash. Unplanned modules, omitted planned modules, native-type drift, interaction drift, or a different plan hash fail the gate.

## TRANSFORM_AUTH_GATE

A derivative must have valid transform provenance and approval. Deterministic crop/reframe behavior is still a transform.

## EVIDENCE_RECONCILIATION_GATE

For fresh projects, post-6.5 full audit is not required by default and this gate is `N/A`. If Planning explicitly requests a targeted early audit for an inherited/reused exact asset, the gate becomes authoritative and missing auditor evidence is `UNVERIFIED`.

## PRODUCTION_FREEZE_GATE

Delivery State `0.2` separates creative completeness from evidence verification. Before pre-demo hardening, Production Freeze must contain the full expected creative set with matching approved output references. This gate does not prove physical identity.

## PRE_DEMO_ASSET_GATE

At Stage 8.5 the full final asset set must be audited. Every required asset must be final-consumable under auditor evidence and the auditor asset-set result must pass. Creative approval alone cannot satisfy this gate.

## ASSET_SLOT_GATE

The implementation must use the exact required Asset IDs in the exact locked slots, with allowed role/scope and acceptable auditor state.

## DELIVERY_PARITY_GATE

Compare locked plan to implementation for module IDs, native types, interactions, Asset IDs, and required slot coverage. A working HTML file is not delivery parity.

## Failure semantics

- `PASS`: machine conditions are satisfied.
- `FAIL`: known contradiction or missing required condition.
- `UNVERIFIED`: required external/auditor execution is unavailable or incomplete.
- `N/A`: gate is not applicable to this project state.

Do not replace `FAIL` or `UNVERIFIED` with prose assertions of success.
