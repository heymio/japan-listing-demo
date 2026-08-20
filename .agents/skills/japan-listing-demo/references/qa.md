# Japan standalone QA

## Distribution QA

- The bundled core manifest, workflow, contracts, evidence, QA, category template, and core evals are present.
- Repository/Codex distribution contains sibling `japan-listing-demo` and `listing-evidence-auditor` Skills.
- Normal user-facing invocation remains `$japan-listing-demo`; the main workflow delegates the auditor at required checkpoints.
- The compatibility single-Skill ZIP explicitly states that it cannot claim an independent semantic audit.
- Upstream provenance is recorded for maintainers but not exposed as a second-repository runtime requirement.
- Optional private overlays remain optional and separate.

## Execution Flow QA

- **Checkpointed execution by default** is active.
- Every numbered workflow stage ends at a Major Stage Checkpoint unless user explicitly opts into Autonomous Mode for the current request.
- Every advanced stage emits a truthful Stage Completion Manifest.
- Transition Commands stop current iteration and advance immediately without turning `PARTIAL` into `COMPLETE` or unverified evidence into final evidence.
- Same artifact/problem has Retry Budget at most two autonomous attempts without new input/evidence.
- New authoritative facts or auditor evidence trigger targeted Change Impact rather than silent ignore or whole-project restart.

## Configuration QA

- `market.country` is `JP`.
- `locale`, `channel`, `category`, `offer`, and `page_targets` are explicit.
- Requested locale is not inferred solely from market.
- One primary Japan channel profile is selected.
- Brand/private overlays are separated from this public repository.

## Market evidence QA

- Every market conclusion has source, date, category, channel, evidence type, confidence, and allowed usage.
- Hypotheses do not enter final consumer copy as facts.
- Search language, scenarios, and visual direction come from current project evidence.
- Competitor execution is not proof of account access or market preference.

## Locale QA

When `locale.id: ja-JP`:

- copy completes terminology, tone, ambiguity, and native-language review;
- numbers, dates, currency, units, symbols, and punctuation match current channel requirements;
- translation artifacts/internal placeholders are removed;
- mobile headlines remain understandable without zooming;
- conditions remain attached to qualified claims.

## Channel QA

- Current editable slots/account capabilities are verified.
- Brand-controlled and platform/retailer-controlled areas are separated.
- Module names/limits belong to selected channel.
- Unsupported capabilities remain `UNKNOWN` / `PENDING`.
- Platform Capability and Frontend Visual evidence are separate.
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE` are separate.
- Native interactive modules have interaction logic/content packing planned before production.

## Frontend Fidelity QA

- A Channel Frontend Reference Pack exists for native demos.
- User is asked for preferred current Reference URL / ASIN / retailer/store page / design reference / screenshot set.
- Valid user-supplied reference is not silently replaced.
- If none, 1–3 current comparable references are researched and a Primary Reference recommended.
- **Official rules do not substitute** for current frontend visual evidence.
- `FRONTEND_FIDELITY_GATE` runs before Stage 9 native naming/assembly.
- Gate failure produces Content Review Demo rather than fabricated native shell.
- Review Mode is overlay-only.

## Candidate / Auditor / Effective State QA

- Stage 6.5A Candidate Asset Registry is explicitly planner-authored assertion state.
- Filenames, Asset IDs, candidate hashes, claimed role, claimed provenance, and candidate `LOCKED` do not by themselves establish physical truth.
- `listing-evidence-auditor` writes a separate Auditor Evidence State and never rewrites Candidate State.
- Effective State gives auditor evidence precedence for downstream asset eligibility.
- Candidate status cannot override auditor `INVALIDATED`, `UNVERIFIED`, `PHYSICALLY_VERIFIED_ONLY`, or `HUMAN_REVIEW_REQUIRED`.

## Physical File QA

- Auditor recomputes SHA-256 from real file bytes.
- Auditor validates allowed project-root path and file existence.
- Byte size, signature family, supported image dimensions, and extension/signature mismatch are recomputed rather than copied from candidate metadata.
- Missing file or path escape is surfaced; no silent substitute is created.
- Same filename/Asset ID with changed bytes does not preserve exact-recovery approval.

## Provenance and Approval QA

- Exact recovery requires current physical SHA-256, approved role, and approved scope to match prior locked evidence.
- Human approval binds to exact physical SHA-256 + approved role + approved slot/page/offer scope.
- Approval does not automatically carry across byte, role, or scope change.
- Deterministic crop/recomposition/role change remains a derivative and requires authorization.
- Auditor may verify but cannot create an explicit user approval event itself.

## Semantic Role QA

- Semantic review prefers an **independent context** or human review.
- Audit packet excludes planner desired audit result and prior PASS conclusions.
- Same-agent inline semantic review cannot become final independent `ROLE_MATCH`.
- If independent semantic audit is unavailable and role is material, status remains `HUMAN_REVIEW_REQUIRED` / `UNVERIFIED` unless human explicitly approves exact hash + role/scope.
- Visual role mismatch invalidates final downstream use even when Candidate State is internally coherent.

## Stage 6.5 Evidence Reconciliation QA

- Main workflow builds `audit-input.json` after candidate intake.
- Auditor produces physical fingerprints, evidence audit, semantic role, provenance/approval result, and asset-set result.
- `EVIDENCE_RECONCILIATION_GATE` is computed from auditor evidence.
- Stage 7 may continue planning with visible gaps but final Asset-to-Slot binding may use only `VERIFIED` / `HUMAN_APPROVED` assets.

## Stage 8.5 Pre-Demo QA

- Stage 8.5 audits exact final files referenced by locked module plan/slot contract.
- Physical SHA is recomputed after edits/transforms.
- Approval carryover, provenance, semantic role, page/offer/slot scope, and required asset-set completeness are rechecked.
- `PRE_DEMO_ASSET_GATE` passes only when all required assets are `VERIFIED` / `HUMAN_APPROVED` and auditor set gate passes.
- One invalidated/unverified required member blocks Stage 9 final channel-native consumption.

## Executable Gate QA

- Project State Manifest exists for work that locks modules/assets or assembles demo.
- External validator is used rather than agent-authored PASS prose.
- `declared_gate_results` is ignored.
- Missing validator/auditor execution leaves relevant gates `UNVERIFIED`.
- `CHANNEL_MODULE_BUDGET_GATE`, `APPROVAL_PROVENANCE_GATE`, `MODULE_ORIGIN_GATE`, `TRANSFORM_AUTH_GATE`, `ASSET_SLOT_GATE`, and `DELIVERY_PARITY_GATE` remain active.
- New `EVIDENCE_RECONCILIATION_GATE` and `PRE_DEMO_ASSET_GATE` are computed from Auditor Evidence State.
- `ASSET_SLOT_GATE` uses auditor effective status and physical hash when available.

## Visual QA

- Every module passes Visual Evidence Matrix.
- Visual subject/evidence object directly support message.
- Product, packaging, UI, controls, interfaces, and functional proof use real approved evidence or explicit provisional labels.
- Visualizable P0 differentiators have Differentiator Proof Matrix entries.
- `DIFFERENTIATOR_PROOF_GATE` requires direct proof or explicit approved alternative.

## Change-control QA

- New authoritative facts, offer/strategy changes, asset/UI evidence, channel-reference changes, claim/legal decisions, or auditor invalidations trigger Change Impact Map.
- Outputs are classified `UNAFFECTED`, `REVIEW`, `INVALIDATED`, or `REOPEN`.
- Unaffected locked work is preserved.
- Invalidated dependent outputs do not remain silently final.

## Technical and Review Mode QA

- Essential native/review interactions work desktop/mobile as required.
- Asset paths resolve.
- Standalone files have no missing local dependencies.
- Review Mode exposes internal status without changing Consumer Mode geometry.
- Consumer Mode hides internal labels/statuses.
- Channel-native naming matches evidence.

## Final Delivery QA

Before calling work complete:

- Stage Completion Manifests are truthful;
- planned deliverables exist or reduced scope is explicitly approved;
- required Auditor Evidence State is present;
- `EVIDENCE_RECONCILIATION_GATE` and `PRE_DEMO_ASSET_GATE` pass when required;
- every final required asset is `VERIFIED` / `HUMAN_APPROVED`;
- `ASSET_SLOT_GATE` passes;
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or approved alternative exists;
- `DELIVERY_PARITY_GATE` passes;
- channel-native work satisfies `FRONTEND_FIDELITY_GATE`;
- passed checks and open items are separate.
