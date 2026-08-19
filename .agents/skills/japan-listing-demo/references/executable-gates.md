# Executable gates and approval provenance

## Purpose

Natural-language QA rules are necessary but insufficient when the same agent can plan, transform, approve, audit, and then write its own PASS statement. Use this reference for machine-checkable state that an **external validator** computes independently from the agent's prose.

The validator is:

```text
scripts/validate_project_state.py
```

The machine-readable state is the **Project State Manifest**. Start from:

```text
templates/project-state.example.json
```

## Non-self-certification rule

The agent may create and update source state, but it does not author executable PASS results.

A field such as:

```json
{"declared_gate_results":{"CHANNEL_MODULE_BUDGET_GATE":"PASS"}}
```

has no authority. The validator intentionally ignores it and computes gate results from the Project State Manifest plus packaged channel-policy data.

If the runtime cannot execute the validator, machine-checkable gates remain:

```text
UNVERIFIED
```

The agent may present the manifest for review, but must not manually convert an executable gate from `UNVERIFIED` to `PASS`.

## Project State Manifest

Maintain one JSON document for the current page-target/offer execution state. The relevant sections are:

```text
schema_version
channel
approval_events
assets
locked_module_plan
asset_slot_contract
implementation
```

Keep the document under version control or otherwise preserve snapshots at Major Stage Checkpoints when the environment permits it.

## Channel policy source

Machine-enforced channel limits live under:

```text
data/channel-policy-limits.json
```

The packaged policy is a conservative executable ceiling. A project may use a lower current-account limit. It must not increase a packaged ceiling by editing only the Project State Manifest.

If a channel limit changes, update the packaged channel policy and Skill version from current authoritative evidence rather than allowing a project agent to override the ceiling ad hoc.

## `CHANNEL_MODULE_BUDGET_GATE`

The external validator compares:

- packaged channel/tier maximum;
- current project declared maximum;
- locked module-plan count.

The effective maximum is the lower supported value.

A module plan that exceeds the effective maximum returns `FAIL` before it can be treated as a valid locked Stage 7 plan.

Content-topic count is not module count. Several messages may be packed into one verified native module.

## Locked module-plan hash

Stage 7 produces one `locked_module_plan` with:

- `status: LOCKED`;
- stable `module_id` values;
- `native_type`;
- `interaction`;
- `asset_ids`;
- `approved_stage`;
- a canonical `plan_hash`;
- a plan approval event whose `approved_hash` matches the canonical plan.

Changing module count, type, interaction, assets, or other hashed module-plan fields changes the plan hash. Stage 9 must consume the exact locked plan hash.

## `MODULE_ORIGIN_GATE`

Every implemented brand-controlled module must originate from the locked module plan.

The validator fails when:

- an implemented module ID was not in the locked plan;
- a planned module disappears from implementation;
- `native_type` changes;
- `interaction` changes;
- the implementation does not reference the locked plan hash.

Stage 9 is an assembler, not a new module-planning stage. It may not add a module, retrofit a carousel, or rewrite the locked interaction and then retroactively edit the plan to match.

## Approval events

User approval provenance is recorded as an `approval_event` with at least:

- stable `approval_id`;
- `actor: user`;
- non-empty `source_ref` that identifies the checkpoint/confirmation in the available runtime;
- `scope`;
- `stage`;
- `approved_hash` for the exact approved state.

The hash binds approval to the state that was actually reviewed. If the state changes, the old approval no longer validates the new state.

A runtime may not provide a cryptographically verifiable chat-event identity. In that case, `source_ref` provides traceability rather than cryptographic proof. The workflow must not invent a user approval that did not occur; if usable provenance cannot be recorded, keep the affected item unapproved or `UNVERIFIED`.

## `APPROVAL_PROVENANCE_GATE`

A `LOCKED` asset requires one of two paths:

1. a user approval event whose scope and approved hash match the current asset-lock payload; or
2. exact recovery of a previously locked asset where SHA-256 matches the recorded prior locked SHA-256.

Filename similarity, visual resemblance, or the agent deciding that a file is probably the old asset does not count as exact recovery.

An asset found after being `MISSING` may be labeled, for example:

```text
RECOVERED_UNAPPROVED
```

until one of the approved locking paths is satisfied.

## Transform authorization

Cropping, recomposition, background replacement, role changes, or other material transformations create a derivative when they can affect framing, evidence, dimensions, or slot suitability.

A locked derivative records:

- `derivative_of`;
- transform type;
- target slot;
- transform `approval_id`;
- `approved_stage`;
- an approval event whose `approved_hash` matches the canonical transform payload.

Deterministic execution is not authorization. A deterministic crop can still change message/evidence or create a new interaction asset.

## `TRANSFORM_AUTH_GATE`

A locked derivative without matching transform authorization returns `FAIL`.

Valid authorization normally occurs in Stage 7.5 or Stage 8 before Demo Assembly.

## `ASSET_SLOT_GATE`

The executable gate uses the Asset-to-Slot Contract and implementation state to check that:

- required Asset IDs exist;
- the asset is actually `LOCKED`;
- the asset explicitly allows the target slot;
- implementation uses the exact required Asset IDs;
- locked interaction matches the slot contract.

Do not repair a failure by silently changing the manifest to match what the demo happened to use. Correct the source asset, approval, transform, or plan at the appropriate reopened stage.

## `DELIVERY_PARITY_GATE`

The executable parity check compares planned and implemented module IDs, native types, interactions, and Asset IDs.

A functioning HTML file is not evidence of parity.

## Validator usage

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json
```

For machine-readable output:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

Exit behavior:

- `0` — all applicable executable gates PASS/N/A;
- `1` — at least one executable gate FAIL;
- `2` — no FAIL exists, but at least one applicable executable gate is `UNVERIFIED`.

## Stage usage

- Stage 5.5: populate channel/tier capability state from verified channel evidence and packaged limits.
- Stage 6.5: register asset hashes and approval/recovery provenance.
- Stage 7: write the proposed module plan, validate module budget, then obtain user approval for the exact plan hash before marking it locked.
- Stage 7.5/8: record approved derivatives and transform hashes.
- Stage 9: consume the locked plan hash; write implementation slots; run the external validator before calling executable gates PASS.
- Stage 10: include validator output in Final QA.

Executable gates supplement, rather than replace, strategy, module-fit, visual-evidence, claim, frontend-fidelity, and human review.