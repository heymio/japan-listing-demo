# Changelog

## 0.2.5 — Executable gates and approval provenance

- Added a machine-readable **Project State Manifest** for channel capability, approval events, assets, locked module plan, asset-slot bindings, and implementation state.
- Added `scripts/validate_project_state.py` as an **external validator**. Agent-authored `declared_gate_results` are ignored.
- Added packaged channel-policy limits and machine-enforced `CHANNEL_MODULE_BUDGET_GATE`; current Amazon.co.jp policy in this Skill version uses Basic A+ max 5 modules and Premium A+ max 7 modules, with Brand Story handled separately.
- Added canonical locked-module-plan hashes and `MODULE_ORIGIN_GATE` so Stage 9 cannot add/remove modules or change native type/interaction after Stage 7 approval.
- Added `APPROVAL_PROVENANCE_GATE`: a locked asset requires matching user approval bound to the current hash or exact prior-lock SHA-256 recovery.
- Added `TRANSFORM_AUTH_GATE` for material crops/recomposition/role-change derivatives. Deterministic execution is not treated as authorization.
- Made `ASSET_SLOT_GATE` and `DELIVERY_PARITY_GATE` machine-computed from Project State source data.
- Added explicit `UNVERIFIED` behavior when the executable validator or packaged machine policy is unavailable; the agent may not manually self-certify PASS.
- Added Project State template, validator self-tests, executable-gate regression cases, packaging checks, and docs.

## 0.2.4 — Delivery integrity and change control

- Added **Stage Completion Manifest** so a completed subset of a stage cannot be mislabeled as full stage completion; statuses are `COMPLETE`, `PARTIAL`, or `BLOCKED`.
- Added **Asset Readiness Preflight**, **Approved Asset Registry**, **Asset-to-Slot Contract**, `ASSET_SLOT_GATE`, `DIFFERENTIATOR_PROOF_GATE`, and `DELIVERY_PARITY_GATE`.
- Separated `CONTENT_COVERAGE` from `MODULE_FIT_GATE` and prohibited mechanically converting independent static boards into carousel/slides only during Demo Assembly.
- Added **Change Impact Map** with `UNAFFECTED`, `REVIEW`, `INVALIDATED`, and `REOPEN` for targeted rework.
- Added anonymized real-project regression cases and strengthened Amazon asset-role integrity.

## 0.2.3 — Channel-native demo fidelity gate

- Added **Channel Frontend Reference Pack**, Reference URL / ASIN intake, visual frontend capture, and `FRONTEND_FIDELITY_GATE`.
- Separated Platform Capability evidence from Frontend Visual evidence.
- Added **Content Review Demo** fallback when native frontend fidelity cannot be validated.
- Required Stage 9 to reproduce a verified channel shell before inserting approved project content.

## 0.2.2 — Checkpoint and anti-loop fix

- Restored **Major Stage Checkpoints by default**.
- Added Transition Command semantics, Stage Lock, and a two-attempt Retry Budget for repeated artifact problems.
- Kept full end-to-end Autonomous Mode as explicit opt-in only.

## 0.2.1 — Continuous execution fix

- Introduced continuous execution as the default at the time, internalized routine gates, and reduced stage-by-stage approval pauses.
- This behavior was later superseded by v0.2.2 after real-world testing.

## 0.2.0 — Standalone distribution

- Bundled the validated generic core snapshot inside the Japan Skill.
- Removed the runtime requirement to install or load a second Skill.
- Added standalone validation, packaging, Japan market/locale/channel references, and leakage checks.

## 0.1.0 — Public Japan overlay

- Added Japan market-evidence, `ja-JP` localization, claim/compliance references, and Japan channel profiles.
