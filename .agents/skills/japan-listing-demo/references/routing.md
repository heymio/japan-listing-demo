# Routing contract

## Stage map

```text
Stage 0–7      → listing-planning
Stage 7.5–8    → listing-production
Stage 8.5–10   → listing-hardening
```

`listing-hardening` delegates exact-file evidence work to `listing-evidence-auditor` when required.

## Formal state objects

The workflow persists five formal state groups instead of treating conversation history as the project database:

1. **Project Brief** — stable product/offer/claim/channel conclusions.
2. **Creative Strategy Kernel** — compressed consumer and creative strategy relevant to production.
3. **Production Handoff** — complete page/asset requirements and production inputs.
4. **Asset Ledger / Production Freeze** — creative production status, exact approved output references, and complete-set boundary.
5. **Delivery State** — hardening evidence, exact files, role/scope binding, plan origin, frontend fidelity, and parity.

Each downstream plane receives only the state objects and references it needs.

## Major Stage Checkpoint

Default user-facing checkpoint:

```text
Done:
Open:
Next:
```

Use the **full Stage Completion Manifest** only when the stage is `PARTIAL`, `BLOCKED`, or the user explicitly asks for detailed audit/state review.

## Context firewall

Planning may be deep. Production must still be narrow.

Production receives only:

- Creative Strategy Kernel;
- Production Handoff;
- current one-job Asset Packet;
- referenced source assets;
- approved visual benchmarks/patterns.

Do not forward full workflow narration, prior failed attempts, gate definitions, auditor reports, Change Impact maps, or Project State internals into the production prompt.

## User-facing continuity

The user normally invokes only `$japan-listing-demo`. Internal stage Skills are routing targets, not separate user workflows.
