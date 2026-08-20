# listing-evidence-auditor + japan-listing-demo v0.2.6 Design

Date: 2026-08-20

## 1. Problem

The current workflow can validate internal consistency while still being wrong about the real files. A Project State Manifest may contain coherent Asset IDs, hashes, roles, slot mappings, and approval statuses that all agree with each other, while the underlying image or UI file is not the asset that was actually approved or is not semantically suitable for the claimed role.

This creates a second form of self-certification:

```text
planner/producer writes project state
→ executable validator checks project state consistency
→ project state is internally coherent
→ PASS

but real file / provenance / visual role is wrong
```

The missing layer is independent evidence reconciliation against the physical artifacts and the human approval record.

## 2. Goal

Add a sibling Skill named `listing-evidence-auditor` and integrate it into `japan-listing-demo` v0.2.6 at two mandatory audit points:

1. after Stage 6.5 Asset Intake, before Stage 7 Module Planning can lock asset assignments;
2. after Stage 8 Visual Production, before Stage 9 Demo Assembly can consume produced/derived assets.

The user-facing entry point remains `$japan-listing-demo`. The main workflow delegates evidence reconciliation to the auditor. Team users continue to clone/use one repository; they do not need to manually invoke the auditor during a normal workflow.

## 3. Non-goals

- The auditor does not decide consumer strategy, message architecture, Amazon module planning, copy, or visual creative direction.
- The auditor does not replace the existing Project State executable validator.
- The auditor does not silently repair, crop, regenerate, rename, or reassign assets.
- The auditor does not turn uncertain visual-role judgments into automatic PASS.
- The auditor does not assume that a filename, Asset ID, agent-authored hash, or `LOCKED` label is trustworthy evidence.

## 4. Architecture

The repository will contain two sibling Skills:

```text
.agents/skills/
├── japan-listing-demo/
└── listing-evidence-auditor/
```

Responsibilities:

```text
$japan-listing-demo
What should we build?
- strategy
- channel research
- IA/module planning
- asset requirements
- visual production
- demo assembly

$listing-evidence-auditor
Are these exact artifacts really what the workflow says they are?
- physical file identity
- provenance
- approval binding
- semantic visual role
- asset-set completeness
```

The main Skill may create candidate state. Only auditor output plus deterministic recomputation can create effective verified evidence state.

## 5. Separation of duties

### 5.1 Preferred execution mode: independent context

When the runtime supports a separate subagent / isolated agent context, `japan-listing-demo` must dispatch `listing-evidence-auditor` with only the audit packet required for evidence reconciliation:

- candidate asset registry;
- exact local asset paths;
- page/offer/slot contract;
- approval events bound to hashes when available;
- previous locked hashes when recovery is claimed;
- relevant visual briefs / expected evidence roles;
- channel frontend evidence only when needed for slot-role classification.

Do not send the planner's desired audit conclusion, self-critique, or prior PASS statements.

### 5.2 Fallback mode: no independent context available

If the runtime cannot execute the auditor in an independent context:

- deterministic physical verification may still run;
- the main agent may prepare the audit packet;
- semantic visual-role/provenance judgments that require independent review remain `UNVERIFIED` unless the user explicitly approves the exact file hash and role;
- the main agent cannot promote an inline self-audit to `VERIFIED` merely by switching instruction sets or loading the auditor file in the same reasoning context.

This limitation must be explicit in the workflow. The correct fallback is `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED`, not self-certified PASS.

## 6. Audit packet

The main workflow creates `audit-input.json` from candidate project state. It contains no gate result.

Minimum shape:

```json
{
  "audit_version": "1",
  "project_id": "project-defined",
  "checkpoint": "post-6.5 | pre-9",
  "assets": [
    {
      "asset_id": "G03",
      "path": "assets/gallery/g03.png",
      "claimed_role": "gallery-native",
      "page_offer_scope": ["offer-a"],
      "allowed_slots": ["gallery-03"],
      "claimed_parent_asset_id": null,
      "claimed_transform": null,
      "claimed_approval_event_id": "APP-017"
    }
  ],
  "slots": [],
  "approval_events": [],
  "prior_locked_assets": [],
  "expected_visual_roles": []
}
```

Fields labeled `claimed_*` are assertions to verify, not trusted facts.

## 7. Deterministic physical verification

`listing-evidence-auditor/scripts/fingerprint_assets.py` recomputes from the real file system:

- existence;
- canonical resolved path under the allowed project root;
- SHA-256;
- byte size;
- file signature / MIME family;
- image width and height for supported PNG/JPEG/WebP files;
- file extension/signature mismatch.

It must not accept agent-authored physical metadata as proof.

Output: `physical-fingerprints.json`.

The existing project-state validator may consume this output, but should also be able to recompute critical file identity directly when local paths are available.

## 8. Provenance verification

For each asset, the auditor classifies provenance:

- `ORIGINAL_VERIFIED` — exact source file is established;
- `DERIVATIVE_VERIFIED` — parent asset exists and transform lineage is documented/authorized;
- `EXACT_RECOVERY_VERIFIED` — current SHA-256 exactly matches a previously locked/approved SHA-256;
- `PROVENANCE_CONFLICT` — claimed origin conflicts with physical or historical evidence;
- `PROVENANCE_UNKNOWN` — insufficient evidence.

A same-name file is never an exact recovery unless its SHA-256 matches the prior locked SHA-256.

A crop, recomposition, resize that changes framing, text/background replacement, or role reassignment remains a derivative even when deterministic and repeatable.

## 9. Approval binding

Human approval is bound to exact content identity, not only Asset ID or filename.

Approval event contract:

```json
{
  "approval_event_id": "APP-017",
  "type": "explicit_user_approval",
  "asset_id": "G03",
  "sha256": "...",
  "approved_role": "gallery-native",
  "approved_slots": ["gallery-03"]
}
```

Rules:

- if SHA changes, prior approval does not automatically carry over;
- if role or slot changes, prior approval does not automatically carry over;
- exact recovery may restore approval only when SHA, approved role, and approved scope match the prior record;
- the auditor cannot create a user approval event itself.

## 10. Semantic visual-role verification

The auditor visually inspects each image/UI artifact and compares the actual content to the expected role and evidence requirement.

Example role classes:

- gallery-native;
- enhanced-content board;
- product packshot;
- lifestyle scene;
- UI screenshot;
- mechanism diagram;
- comparison visual;
- packaging;
- frontend-reference capture.

The semantic check asks:

1. What kind of artifact is this actually?
2. Does it visually support the expected slot role?
3. Does it contain signs that it was repurposed from another role (for example, enhanced-content copy/layout inside a gallery image)?
4. Does the visual subject/evidence object match the locked brief?

Result values:

- `ROLE_MATCH`;
- `ROLE_MISMATCH`;
- `ROLE_AMBIGUOUS`;
- `NOT_VISUALLY_AUDITED`.

An inline same-agent semantic check cannot by itself produce final `ROLE_MATCH` in fallback mode. It remains `ROLE_AMBIGUOUS` or `NOT_VISUALLY_AUDITED` until independent-context or human review occurs.

## 11. Asset-set completeness

The auditor verifies the whole required asset set, not only individual files.

Example:

```text
expected gallery: G1 G2 G3 G4 G5 G6 G7 G8
verified:         G1 G2
invalidated:            G3 G4 G5 G6 G7 G8

ASSET_SET_GATE = FAIL
```

Checks include:

- expected slot count/order;
- one-to-one required asset binding when applicable;
- duplicate physical file reused under different Asset IDs when not allowed;
- missing required assets;
- unexpected additional assets entering a locked set.

## 12. Auditor output

The auditor writes a separate namespace, never overwriting candidate project state:

```text
audit/
├── audit-input.json
├── physical-fingerprints.json
├── evidence-audit.json
└── verified-asset-registry.json
```

`evidence-audit.json` contains per-asset results for:

- physical identity;
- provenance;
- approval match;
- semantic role;
- slot compatibility;
- set completeness.

Effective asset statuses:

- `VERIFIED` — physical, provenance, approval/scope, and semantic-role checks all satisfy the checkpoint requirements;
- `HUMAN_APPROVED` — deterministic physical identity is verified and the user explicitly approves the exact hash + role/scope for an otherwise unresolved semantic/provenance point;
- `PHYSICALLY_VERIFIED_ONLY` — physical identity is known but semantic/provenance assurance is incomplete; not final-consumable;
- `INVALIDATED` — evidence conflict exists;
- `UNVERIFIED` — insufficient evidence;
- `HUMAN_REVIEW_REQUIRED` — independent semantic audit is unavailable and human confirmation is required.

## 13. Effective state rule

`japan-listing-demo` keeps two layers:

```text
Agent-authored Candidate State
+
Auditor-authored Evidence State
=
Effective State
```

The main workflow may not overwrite auditor results.

When candidate and auditor states conflict, auditor evidence wins for downstream asset eligibility.

Example:

```yaml
asset_id: G03
agent_claim:
  role: gallery-native
  status: LOCKED

auditor_result:
  physical_sha256: actual-sha
  provenance: PROVENANCE_CONFLICT
  semantic_role: enhanced-content-board
  approval_match: false

effective_status: INVALIDATED
```

## 14. Workflow integration

### Stage 6.5 — Asset Intake

New flow:

```text
Stage 6.5A Candidate Asset Registry
        ↓
listing-evidence-auditor
        ↓
EVIDENCE_RECONCILIATION_GATE
        ↓
Verified Asset Registry
        ↓
Stage 7
```

Stage 7 may plan around missing/unverified assets, but cannot lock a final Asset-to-Slot Contract using an asset whose effective status is not `VERIFIED` or `HUMAN_APPROVED`.

### Stage 8.5 — Pre-Demo Evidence Audit

Add a new explicit stage:

```text
Stage 8 Visual Production
        ↓
Stage 8.5 Pre-Demo Evidence Audit
        ↓
listing-evidence-auditor
        ↓
PRE_DEMO_ASSET_GATE
        ↓
Stage 9 Demo Assembly
```

Stage 8.5 re-audits:

- final generated/edited files;
- derivatives;
- exact hashes;
- approval carryover;
- role/slot compatibility;
- the complete asset set expected by the locked module plan.

Stage 9 may consume only `VERIFIED` or `HUMAN_APPROVED` assets for final channel-native regions.

## 15. Gate behavior

### `EVIDENCE_RECONCILIATION_GATE`

PASS only when assets needed to lock the next stage are sufficiently verified.

May be `PARTIAL` when planning can continue with explicit gaps, but final slot binding remains unlocked.

### `PRE_DEMO_ASSET_GATE`

PASS only when every asset required by the locked Demo plan is `VERIFIED` or `HUMAN_APPROVED`, the expected set is complete, and no invalidated asset is referenced.

If the independent auditor cannot run and required semantic checks are unresolved, result is `UNVERIFIED`, not PASS.

## 16. Interaction with v0.2.5 executable gates

v0.2.5 remains responsible for machine-checking project-state structure and locked-plan consistency:

- module budget;
- plan hash;
- module origin;
- transform authorization;
- approval provenance fields;
- asset-slot mapping;
- delivery parity.

v0.2.6 adds real-artifact evidence:

```text
v0.2.5
Manifest ↔ Manifest consistency

v0.2.6
Manifest ↔ Physical file ↔ Approval record ↔ Visual role
```

The v0.2.5 validator must consume auditor-computed physical fingerprints instead of trusting duplicated agent-authored hashes when both exist.

## 17. Distribution

Primary distribution target: repository/Codex workflow.

- One public repository: `heymio/japan-listing-demo`.
- Two sibling Skills in the repository.
- User normally invokes only `$japan-listing-demo`.
- `japan-listing-demo` delegates to `listing-evidence-auditor` at mandatory audit checkpoints.

The existing standalone `japan-listing-demo.skill.zip` remains supported for compatibility, but a single-context archive cannot claim independent semantic audit. In that environment, semantic evidence must remain `UNVERIFIED` unless explicit human review supplies the approval.

The repository may additionally package a Codex/project bundle containing both sibling Skills; this does not change the user-facing invocation.

## 18. Error handling

- Missing file → `INVALIDATED` for required exact artifact, not silent replacement.
- Unsupported image format → physical hash still verified; dimensions/semantic checks `UNVERIFIED` as applicable.
- File outside allowed project root → reject path.
- Hash mismatch against approval → approval invalidated.
- Auditor cannot inspect image → `HUMAN_REVIEW_REQUIRED` when semantic role matters.
- Candidate registry and slot contract disagree → surface conflict; do not auto-edit either side.
- Main workflow attempts to proceed despite failed pre-demo gate → Stage 9 blocked.

## 19. Testing strategy

### Auditor deterministic tests

Use temporary fixtures to verify:

- SHA-256 recomputation;
- PNG/JPEG/WebP dimensions;
- extension/signature mismatch;
- missing file;
- path escape outside allowed root;
- exact-recovery hash match/mismatch;
- approval invalidation when SHA changes;
- duplicate physical file detection.

### Workflow regression tests

- Candidate says Gallery, physical/semantic audit says enhanced-content → cannot become Verified Gallery.
- Same filename but different SHA → exact recovery fails.
- Deterministic crop without authorized derivative → fails.
- Inline same-agent audit → cannot final-PASS semantic role.
- Human approval of exact SHA + role can resolve required ambiguity.
- Stage 7 final slot lock blocked when required asset is not verified.
- Stage 9 blocked when any locked module references invalidated/unverified asset.
- A complete 8-asset set with one invalidated member fails PRE_DEMO_ASSET_GATE.

### Packaging tests

- repository contains both sibling Skills;
- main Skill explicitly declares mandatory auditor checkpoints;
- bundle packaging includes both Skills and auditor scripts;
- single-skill archive documentation clearly states semantic-audit limitation.

## 20. Acceptance criteria

The implementation is acceptable when all of the following hold:

1. The main workflow no longer treats Candidate Asset Registry as effective truth.
2. A real-file fingerprint is recomputed by code from the asset path.
3. Approval is bound to exact SHA + role/scope.
4. Same-name replacement cannot preserve approval without exact hash match.
5. A role mismatch detected by the auditor invalidates downstream use even when Asset ID and manifest fields are internally consistent.
6. Stage 7 cannot final-lock unverified asset bindings.
7. Stage 9 cannot consume an asset set that failed the pre-demo audit.
8. Inline same-agent semantic auditing cannot silently become independent PASS.
9. User-facing flow remains one repository and normally one invocation: `$japan-listing-demo`.
10. Existing v0.2.5 executable project-state gates remain active and consume auditor evidence where applicable.
