# Changelog

## 0.3.1 — Validator integrity hardening

- Replaced Planning contract keyword-presence checks with structured parsing and type/reference validation for Project Brief, Creative Strategy Kernel, and Production Handoff.
- Rejects malformed planning contract indentation, duplicate keys/IDs, invalid field types, missing required fields, dangling Asset-ID references, and control-plane leakage into Production Handoff.
- Hardened image fingerprinting so supported final images must have a valid PNG/JPEG/WebP signature, matching extension, positive dimensions, positive byte size, and no physical errors; fake `.png` text files now fail.
- Changed normal evidence reconciliation to recompute fingerprints from real project files instead of accepting caller-supplied fingerprint JSON as the trusted CLI input.
- Removed the standalone CLI `--independent-semantic` switch; callers cannot promote their own semantic review to independent trust merely by passing a flag.
- Audit packets now fail fast on duplicate `assets.asset_id`, `approval_events.approval_event_id`, `prior_locked_assets.asset_id`, `slots.slot_id`, or `expected_visual_roles.asset_id`, preventing silent dictionary overwrite.
- Strengthened Delivery State schema fail-fast behavior. Malformed container types and duplicate identity fields stop semantic gates instead of causing tracebacks or ambiguous downstream results.
- `implementation.slots[*].module_id` is now one-to-one with implementation slots; duplicate module IDs are rejected before Module Origin / Delivery Parity can collapse them into dictionaries.
- `PRODUCTION_FREEZE_GATE` now compares the exact approved Asset-ID set against the required Asset-ID set instead of only comparing counts.
- Removed the stray root `x` file and updated compatibility packaging for the strict hardening wrapper.
- Architecture remains unchanged: Thin Router → Planning → Production → Hardening → Evidence Auditor. This release does not claim proven Japan-market output quality; Golden Set / team-pilot validation remains separate.

## 0.3.0 — Creative-first hardening architecture

- Replaced the monolithic `japan-listing-demo` runtime with a **thin router** while keeping one normal user invocation: `$japan-listing-demo`.
- Added `listing-planning` for Stage 0–7 so Product Truth, Offer/Page Boundary, Claim Readiness, Consumer Strategy, VOC/competitor reasoning, Japan localization, channel research, Gallery/enhanced-content architecture, module budget, and `MODULE_FIT_GATE` remain strategically deep without carrying delivery-governance noise into Production.
- Added formal **Project Brief**, **Creative Strategy Kernel**, and **Production Handoff** contracts. Stage 7 now defines the **Complete Demo-Required Production Set**; P0/differentiator proof coverage is not treated as visual-set completeness.
- Changed fresh-project Stage 6.5 to lightweight **Source Asset Intake**. Full project-wide evidence audit is no longer mandatory before final assets exist; targeted early audit remains available for inherited/reused previously approved exact assets.
- Added `listing-production` for Stage 7.5–8 with artifact-first behavior, one-job Asset Packets, explicit **Context Projection**, benchmark-vs-reuse separation, Asset Ledger, Production Freeze, Visual Pattern Library, Golden Examples, and compact Creative QA.
- Separated **Creative Approval** (`USER_APPROVED`) from **Evidence Verification**. Creative approval no longer implies physical identity, provenance, or final delivery eligibility.
- Added `listing-hardening` for Stage 8.5–10 and moved canonical delivery validation there while keeping the legacy `validate_project_state.py` path as a compatibility shim.
- Added **Delivery State 0.2** and `PRODUCTION_FREEZE_GATE`, separating “the complete creative set is approved” from `PRE_DEMO_ASSET_GATE`, which verifies the exact final files.
- Kept mandatory **Stage 8.5 full evidence audit** through `listing-evidence-auditor`, plus existing exact-file, approval-provenance, transform, semantic-role, asset-set, slot, module-origin, frontend-fidelity, and delivery-parity safeguards.
- Moved Amazon.co.jp, Rakuten, Yahoo! Shopping, DTC, and retailer channel planning profiles into `listing-planning`, keeping Platform Capability evidence separate from Frontend Visual evidence and keeping Gallery/enhanced-content role planning separate.
- Removed duplicated monolithic workflow/contracts/delivery/executable/frontend/QA runtime files from the main router Skill after stage-local ownership was established.
- Changed normal checkpoint output to concise `Done / Open / Next`; full Stage Completion Manifest is exception-only for `PARTIAL`, `BLOCKED`, or explicit detailed audit review.
- Added a five-Skill repository/Codex bundle containing `japan-listing-demo`, `listing-planning`, `listing-production`, `listing-hardening`, and `listing-evidence-auditor`.
- Kept one-install `japan-listing-demo.skill.zip` by embedding the four internal stage/audit Skills under `japan-listing-demo/internal-skills/`; the package retains explicit single-context semantic-audit limitations.
- Added Team Golden Path evals and an optional thin Custom GPT setup guide. The GPT remains an optional UX shell; GitHub-packaged Skills remain the versioned execution source of truth.

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
