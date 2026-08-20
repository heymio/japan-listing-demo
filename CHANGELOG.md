# Changelog

## 0.2.6 — Independent listing evidence auditor

- Added sibling **`listing-evidence-auditor` Skill** in the same public repository while keeping normal user invocation as `$japan-listing-demo`.
- Split planner-authored **Candidate Asset Registry** from auditor-owned **Evidence State** and downstream **Effective State**.
- Added real-file fingerprinting that recomputes path containment, existence, SHA-256, byte size, signature family, extension/signature mismatch, and supported PNG/JPEG/WebP dimensions instead of trusting planner-authored metadata.
- Added provenance reconciliation with `ORIGINAL_VERIFIED`, `DERIVATIVE_VERIFIED`, `EXACT_RECOVERY_VERIFIED`, `PROVENANCE_CONFLICT`, and `PROVENANCE_UNKNOWN`.
- Bound human asset approval to exact physical SHA-256 + approved visual role + approved slot/page/offer scope. Same-name replacement does not inherit approval when bytes change.
- Added semantic visual-role audit contract. Same-agent inline review cannot self-certify final `ROLE_MATCH`; when an independent context is unavailable, unresolved role evidence remains `HUMAN_REVIEW_REQUIRED` / `UNVERIFIED` unless the user explicitly approves exact hash + role/scope.
- Added required asset-set completeness audit so one invalidated/unverified required member blocks final set consumption.
- Split Stage 6.5 into Candidate Asset Intake and post-6.5 evidence reconciliation; added `EVIDENCE_RECONCILIATION_GATE` before final asset binding.
- Added **Stage 8.5 Pre-Demo Evidence Audit** and `PRE_DEMO_ASSET_GATE` before Stage 9.
- Updated v0.2.5 Project State validator so auditor evidence overrides Candidate Asset Status for asset eligibility and physical SHA conflicts fail downstream gates.
- Preserved all v0.2.5 executable gates: module budget, approval provenance, module origin, transform authorization, asset-slot, and delivery parity.
- Added evidence-auditor workflow regressions and two self-test suites.
- Added a two-Skill Codex/repository bundle (`dist/japan-listing-demo-codex-bundle.zip`).
- Kept compatibility `japan-listing-demo.skill.zip`, but it now includes an explicit single-context limitation note and cannot claim independent semantic audit.

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
