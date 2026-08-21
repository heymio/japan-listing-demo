# v0.3.2 Production UX & Set-level Creative QA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve first-pass listing production quality and team UX by adding page-level art direction, set-level Creative QA, exact candidate selection locks, per-asset evidence modes, reusable account capability state, explicit scope deltas, and smallest-sufficient cleanup while preserving the v0.3.0 context firewall and v0.3.1 hardening behavior.

**Architecture:** Keep the existing Planning → Production → Hardening split. Planning enriches the compact Production Handoff with `page_visual_system`, `evidence_mode`, and optional account-capability state; Production projects only the current asset plus minimal set context, manages immutable user-selected candidate history, runs asset-level and set-level creative checks, and applies scoped cleanup/scope-delta logic. Hardening and the evidence auditor remain unchanged except for distribution/package parity checks.

**Tech Stack:** Python 3.12 standard library, YAML-like restricted contract parser already in `listing-planning`, Markdown/YAML templates, GitHub Actions CI, ZIP packaging scripts.

**Spec:** `docs/superpowers/specs/2026-08-21-production-ux-set-level-creative-qa-design.md`

## Global Constraints

- Target version: `0.3.2`.
- Do not add a new formal numbered Stage.
- Do not add a new Hardening/validator gate.
- Do not weaken Stage 8.5 evidence verification or v0.3.1 validator integrity.
- Keep the one-job rule: one Asset Packet = one Asset ID, one channel role, one primary shopper task/message, quantity 1.
- Preserve the Production context firewall: no Stage history, Project State, auditor reports, gate/parity state, or full research corpus in generation context.
- Public repository must not hard-code private brand/account capability values.
- Use Python standard library only; do not introduce third-party dependencies.
- Same art direction must not be interpreted as same composition.
- User selection is an explicit state transition; an approved exact candidate cannot be silently replaced.
- `source insufficiency != automatic creative rework`; behavior depends on `evidence_mode`.
- Cleanup uses the Smallest Sufficient Intervention and preserves unrelated approved assets.

---

## File Structure

### Planning ownership

- Modify `.agents/skills/listing-planning/SKILL.md` — describe `page_visual_system`, `evidence_mode`, scope revision, and capability reuse as Stage 7 handoff responsibilities.
- Modify `.agents/skills/listing-planning/templates/production-handoff.example.yaml` — canonical example for new fields.
- Modify `.agents/skills/listing-planning/references/planning-qa.md` — planning-time visual-rhythm and evidence-mode rules.
- Modify `.agents/skills/listing-planning/profiles/channels/amazon-jp.md` — generic account-capability reuse order; no brand-specific values.
- Create `.agents/skills/listing-planning/scripts/account_capability.py` — pure capability freshness/conflict resolver.
- Modify `.agents/skills/listing-planning/scripts/validate_planning_contracts.py` — structural validation of Page Visual System, evidence modes, scope revisions, and asset references.
- Modify `.agents/skills/listing-planning/scripts/selftest_planning.py` — behavioral regressions for planning contracts and capability reuse.

### Production ownership

- Modify `.agents/skills/listing-production/SKILL.md` — clarify same-art-direction vs composition, selection lock, set QA cadence, minimal cleanup, concise continuation behavior.
- Modify `.agents/skills/listing-production/templates/asset-packet.example.yaml` — add `evidence_mode` and `set_context`.
- Modify `.agents/skills/listing-production/templates/asset-ledger.example.yaml` — add candidate history and selected candidate identity.
- Modify `.agents/skills/listing-production/references/production-qa.md` — keep seven asset checks and add six set-level checks.
- Modify `.agents/skills/listing-production/references/visual-production.md` — evidence-mode production behavior.
- Modify `.agents/skills/listing-production/scripts/project_asset_packet.py` — project only minimal current/set context.
- Modify `.agents/skills/listing-production/scripts/production_state.py` — candidate selection/reopen, scope-delta-aware progress/freeze.
- Create `.agents/skills/listing-production/scripts/set_level_qa.py` — pure set-level repetition/rhythm analysis.
- Create `.agents/skills/listing-production/scripts/cleanup_policy.py` — pure Smallest Sufficient Intervention planner.
- Modify `.agents/skills/listing-production/scripts/selftest_production.py` — Light Bars regressions plus compatibility coverage.

### Router/distribution/release ownership

- Modify `.agents/skills/japan-listing-demo/SKILL.md` — concise transition acknowledgement and routing wording only; no new stage.
- Modify `.agents/skills/japan-listing-demo/scripts/selftest_router.py` — continuation/selection acknowledgement regressions.
- Modify `.agents/skills/japan-listing-demo/scripts/validate_overlay.py` — require new scripts and `VERSION=0.3.2` after behavior is green.
- Modify `.agents/skills/japan-listing-demo/core/manifest.yaml` — add v0.3.2 production-UX patch lineage.
- Modify `.agents/skills/japan-listing-demo/scripts/package_skill.py` — package new Planning/Production scripts automatically and extend smoke assertions if needed.
- Modify `scripts/package_codex_bundle.py` only if required-member smoke checks need explicit new files.
- Modify `README.md`, `CHANGELOG.md`, `docs/install.md`, `VERSION` only after functional RED→GREEN is complete.

---

### Task 1: Planning Handoff — Page Visual System, Evidence Mode, Scope Revision

**Files:**
- Modify: `.agents/skills/listing-planning/templates/production-handoff.example.yaml`
- Modify: `.agents/skills/listing-planning/scripts/validate_planning_contracts.py`
- Modify: `.agents/skills/listing-planning/scripts/selftest_planning.py`
- Modify: `.agents/skills/listing-planning/SKILL.md`
- Modify: `.agents/skills/listing-planning/references/planning-qa.md`

**Interfaces:**
- Consumes: current Production Handoff mapping.
- Produces: validated `page_visual_system.asset_directions[]`, per-asset `evidence_mode`, optional `scope_revision` / `scope_delta`, and cross-reference guarantees to the authoritative `asset_set`.

- [ ] **Step 1: Write failing Planning tests**

Add tests that load the real Planning validator and assert these behaviors:

```python
def test_handoff_requires_valid_evidence_mode_and_visual_direction_refs() -> None:
    handoff = valid_production_handoff()
    handoff["production_handoff"]["asset_set"][0]["evidence_mode"] = "NOT_A_MODE"
    handoff["production_handoff"]["page_visual_system"] = {
        "asset_directions": [{
            "asset_id": "MISSING-ASSET",
            "visual_role": "color-mood",
            "scene_family": "dark-living-space",
            "composition_family": "wide-lifestyle",
            "tone": "saturated-dark",
            "product_scale": "medium",
            "proof_form": "lifestyle",
        }]
    }
    result = validate_contract("production_handoff", handoff)
    assert result["valid"] is False
    assert any("evidence_mode" in e for e in result["errors"])
    assert any("MISSING-ASSET" in e for e in result["errors"])


def test_adjacent_accidental_visual_duplicate_is_rejected_without_intent_note() -> None:
    handoff = handoff_with_two_assets_same_visual_signature()
    result = validate_contract("production_handoff", handoff)
    assert result["valid"] is False
    assert any("adjacent visual direction" in e.casefold() for e in result["errors"])


def test_intentional_repetition_with_neighbor_contrast_note_is_allowed() -> None:
    handoff = handoff_with_two_assets_same_visual_signature()
    handoff["production_handoff"]["page_visual_system"]["asset_directions"][1][
        "neighbor_contrast_note"
    ] = "Intentional matched pair; message contrast is the comparison device"
    assert validate_contract("production_handoff", handoff)["valid"] is True
```

Also add a scope-delta cross-reference test:

```python
def test_scope_delta_removed_asset_must_not_remain_in_current_asset_set() -> None:
    handoff = valid_production_handoff()
    handoff["production_handoff"]["scope_revision"] = 2
    handoff["production_handoff"]["scope_delta"] = {
        "added": [], "removed": ["G2"], "changed": [],
        "reason": ["message merged into G1"],
    }
    result = validate_contract("production_handoff", handoff)
    assert result["valid"] is False
```

- [ ] **Step 2: Run Planning selftest and verify RED**

Run:

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
```

Expected: FAIL on the new Page Visual System/evidence-mode/scope-delta tests because v0.3.1 does not validate those structures.

- [ ] **Step 3: Implement minimal structural validation**

Add constants and helpers to `validate_planning_contracts.py`:

```python
EVIDENCE_MODES = {"SOURCE_FAITHFUL", "CREATIVE_MOCK", "PROOF_VISUAL"}
VISUAL_DIRECTION_FIELDS = {
    "visual_role", "scene_family", "composition_family",
    "tone", "product_scale", "proof_form",
}


def _visual_signature(direction: dict[str, object]) -> tuple[object, ...]:
    return tuple(direction.get(key) for key in (
        "scene_family", "composition_family", "tone", "product_scale", "proof_form"
    ))
```

Validation requirements:

- every current `asset_set` entry has one valid `evidence_mode`;
- every `page_visual_system.asset_directions[*].asset_id` exists exactly once in the current `asset_set`;
- every current asset has exactly one visual direction;
- all six minimum visual-direction fields are non-empty strings;
- adjacent entries with identical `_visual_signature(...)` require a non-empty `neighbor_contrast_note` on the latter entry;
- `scope_revision`, when present, is a positive integer and not boolean;
- `scope_delta.added/removed/changed/reason` are lists of non-empty strings;
- IDs in `removed` cannot remain in current `asset_set`; IDs in `added` must exist in current `asset_set`.

- [ ] **Step 4: Update handoff template and Planning guidance**

Use an example that demonstrates deliberate variation, for example:

```yaml
  asset_set:
    - asset_id: G1
      role: gallery-native
      slot: G1
      primary_message: Core positioning
      evidence_mode: SOURCE_FAITHFUL
      status: READY
    - asset_id: G2
      role: gallery-native
      slot: G2
      primary_message: Primary proof
      evidence_mode: PROOF_VISUAL
      status: READY
    - asset_id: A1
      role: enhanced-content
      slot: A1
      primary_message: Lifestyle expansion
      evidence_mode: CREATIVE_MOCK
      status: READY

  page_visual_system:
    asset_directions:
      - asset_id: G1
        visual_role: hero-positioning
        scene_family: clean-product-stage
        composition_family: centered-hero
        tone: bright-neutral
        product_scale: large
        proof_form: source-faithful-product
      - asset_id: G2
        visual_role: mechanism-proof
        scene_family: technical-detail
        composition_family: close-up-explainer
        tone: neutral-technical
        product_scale: close-up
        proof_form: mechanism
      - asset_id: A1
        visual_role: lifestyle-use
        scene_family: realistic-home
        composition_family: wide-lifestyle
        tone: warm-natural
        product_scale: medium
        proof_form: lifestyle
```

Document: “Same art direction ≠ same composition” and “Page Visual System is an art-direction matrix, not a new gate/stage.”

- [ ] **Step 5: Run Planning selftest and verify GREEN**

Run:

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
```

Expected: all Planning tests PASS, including v0.3.1 strict contract regressions.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/listing-planning
 git commit -m "feat: add page visual system and evidence modes"
```

---

### Task 2: Account Capability Profile Reuse

**Files:**
- Create: `.agents/skills/listing-planning/scripts/account_capability.py`
- Modify: `.agents/skills/listing-planning/scripts/selftest_planning.py`
- Modify: `.agents/skills/listing-planning/profiles/channels/amazon-jp.md`
- Modify: `.agents/skills/listing-planning/SKILL.md`

**Interfaces:**
- Produces: `resolve_capability(profile, capability, now, max_age_days, conflicting=False) -> dict`.
- Result shape: `{"status": "REUSE"|"VERIFY", "value": bool|None, "reason": str}`.

- [ ] **Step 1: Write failing capability tests**

```python
from datetime import datetime, timezone
from account_capability import resolve_capability


def test_recent_confirmed_capability_is_reused() -> None:
    profile = {
        "channel": "amazon-jp",
        "capabilities": {"premium_a_plus": True},
        "verified_at": "2026-08-01",
        "source_ref": "team-private-context",
    }
    result = resolve_capability(
        profile, "premium_a_plus",
        now=datetime(2026, 8, 21, tzinfo=timezone.utc),
        max_age_days=90,
    )
    assert result == {"status": "REUSE", "value": True, "reason": "recent confirmed capability"}


def test_stale_or_conflicted_capability_requires_verification() -> None:
    profile = {
        "channel": "amazon-jp",
        "capabilities": {"premium_a_plus": True},
        "verified_at": "2025-01-01",
        "source_ref": "team-private-context",
    }
    stale = resolve_capability(profile, "premium_a_plus", now=datetime(2026, 8, 21, tzinfo=timezone.utc), max_age_days=90)
    conflict = resolve_capability(profile, "premium_a_plus", now=datetime(2026, 8, 21, tzinfo=timezone.utc), max_age_days=9999, conflicting=True)
    assert stale["status"] == "VERIFY"
    assert conflict["status"] == "VERIFY"
```

- [ ] **Step 2: Run Planning selftest and verify RED**

Expected: import/function failure because `account_capability.py` does not exist.

- [ ] **Step 3: Implement resolver**

Implementation behavior:

```python
def resolve_capability(profile, capability, now, max_age_days, conflicting=False):
    if conflicting:
        return {"status": "VERIFY", "value": None, "reason": "conflicting evidence"}
    if not isinstance(profile, dict):
        return {"status": "VERIFY", "value": None, "reason": "capability profile missing"}
    capabilities = profile.get("capabilities")
    if not isinstance(capabilities, dict) or capability not in capabilities:
        return {"status": "VERIFY", "value": None, "reason": "capability not recorded"}
    value = capabilities.get(capability)
    if not isinstance(value, bool):
        return {"status": "VERIFY", "value": None, "reason": "capability value invalid"}
    # parse YYYY-MM-DD; invalid/missing date => VERIFY
    # age > max_age_days => VERIFY
    return {"status": "REUSE", "value": value, "reason": "recent confirmed capability"}
```

Reject boolean/negative `max_age_days`; keep all behavior deterministic.

- [ ] **Step 4: Update Amazon profile decision order**

Document exactly:

1. reuse a sufficiently recent, non-conflicted profile;
2. ask/verify only when missing, stale, invalid, or contradicted;
3. never infer account access from competitors;
4. never hard-code private brand values in the public Skill.

- [ ] **Step 5: Run Planning selftest and verify GREEN**

Expected: all Planning tests PASS.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/listing-planning
 git commit -m "feat: reuse verified account capabilities"
```

---

### Task 3: Asset Packet Minimal Set Context + Evidence Mode

**Files:**
- Modify: `.agents/skills/listing-production/templates/asset-packet.example.yaml`
- Modify: `.agents/skills/listing-production/scripts/project_asset_packet.py`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`
- Modify: `.agents/skills/listing-production/SKILL.md`
- Modify: `.agents/skills/listing-production/references/visual-production.md`

**Interfaces:**
- Consumes: validated Production Handoff + current Asset ID.
- Produces: one Asset Packet containing current asset `evidence_mode`, its own `page_visual_direction`, and nearest-neighbor visual summaries only.

- [ ] **Step 1: Write failing packet-projection tests**

```python
def test_asset_packet_includes_minimal_set_context_and_evidence_mode() -> None:
    packet = project_asset_packet(handoff_fixture(), "A05-02")
    assert packet["evidence_mode"] == "CREATIVE_MOCK"
    assert packet["set_context"]["page_visual_direction"]["scene_family"] == "daylight-study"
    assert packet["set_context"]["nearest_neighbors"] == [{
        "asset_id": "A05-01",
        "scene_family": "dark-living-space",
        "composition_family": "wide-lifestyle",
        "tone": "saturated-dark",
        "product_scale": "medium",
        "proof_form": "lifestyle",
    }]


def test_asset_packet_context_firewall_still_excludes_control_plane() -> None:
    packet = project_asset_packet(handoff_with_extra_control_fields(), "A05-02")
    serialized = json.dumps(packet).casefold()
    for forbidden in ["stage_manifest", "project_state", "auditor", "parity", "gate"]:
        assert forbidden not in serialized
```

- [ ] **Step 2: Run Production selftest and verify RED**

Expected: FAIL because packet projection does not yet include the new fields.

- [ ] **Step 3: Implement minimal projection**

In `project_asset_packet.py`:

- resolve current asset from `asset_set`;
- resolve its visual direction from `page_visual_system.asset_directions`;
- include at most the nearest previous/next assets that exist in the same `page_plan` region/order;
- project only these neighbor keys: `asset_id`, `scene_family`, `composition_family`, `tone`, `product_scale`, `proof_form`;
- do not copy the full Page Visual System or Planning history.

- [ ] **Step 4: Encode evidence-mode production behavior**

Document in `visual-production.md`:

```text
SOURCE_FAITHFUL -> block when exact product identity cannot be safely represented.
CREATIVE_MOCK -> allow credible creative production with reduced evidence entitlement; generated placement details are not Product Truth.
PROOF_VISUAL -> block when required proof source is missing.
```

Add an executable helper or packet preflight branch in `project_asset_packet.py` returning `BLOCKED` only for `SOURCE_FAITHFUL`/`PROOF_VISUAL` when their declared required source list is unavailable; `CREATIVE_MOCK` remains projectable when non-proof source limitations are explicitly recorded.

- [ ] **Step 5: Run Production selftest and verify GREEN**

Expected: all Production tests PASS, including the existing “Gallery hero must not become infographic” regression.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/listing-production
 git commit -m "feat: project minimal set context into asset packets"
```

---

### Task 4: Exact Candidate Selection Lock and Reopen History

**Files:**
- Modify: `.agents/skills/listing-production/templates/asset-ledger.example.yaml`
- Modify: `.agents/skills/listing-production/scripts/production_state.py`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`
- Modify: `.agents/skills/listing-production/SKILL.md`

**Interfaces:**
- Produces:
  - `add_candidate(ledger, asset_id, candidate_id, output_ref) -> dict`
  - `select_candidate(ledger, asset_id, candidate_id, approval_ref=None) -> dict`
  - `reopen_asset(ledger, asset_id, reason) -> dict`
- `set_creative_status(..., output_ref=...)` must reject silent output replacement after selection lock.

- [ ] **Step 1: Write failing selection-lock tests**

```python
def test_user_selected_candidate_cannot_be_silently_replaced() -> None:
    ledger = add_candidate({}, "A05-01", "A05-01-v1", "file:v1")
    ledger = select_candidate(ledger, "A05-01", "A05-01-v1", "chat:42")
    try:
        set_creative_status(ledger, "A05-01", "USER_APPROVED", output_ref="file:v2")
    except ValueError as exc:
        assert "reopen" in str(exc).casefold()
    else:
        raise AssertionError("selected candidate must not be silently replaced")


def test_reopen_preserves_selected_candidate_history() -> None:
    ledger = add_candidate({}, "A05-01", "A05-01-v1", "file:v1")
    ledger = select_candidate(ledger, "A05-01", "A05-01-v1")
    ledger = reopen_asset(ledger, "A05-01", "user requested another version")
    ledger = add_candidate(ledger, "A05-01", "A05-01-v2", "file:v2")
    row = ledger["assets"]["A05-01"]
    assert [c["candidate_id"] for c in row["candidates"]] == ["A05-01-v1", "A05-01-v2"]
    assert row["selected_candidate_id"] == "A05-01-v1"
    assert row["status"] == "REVIEW"
```

Also test duplicate candidate IDs fail.

- [ ] **Step 2: Run Production selftest and verify RED**

Expected: FAIL because candidate-version APIs do not exist.

- [ ] **Step 3: Implement candidate state transitions**

Rules:

- `add_candidate` appends a candidate with status `REVIEW`; duplicate `candidate_id` raises `ValueError`.
- `select_candidate` marks the chosen candidate `USER_SELECTED`, marks any prior selected candidate `SUPERSEDED` only if the asset was explicitly reopened, stores `selected_candidate_id`, `current_output_ref`, optional `approval_ref`, and asset status `USER_APPROVED`.
- `reopen_asset` requires current asset status `USER_APPROVED`, preserves `selected_candidate_id` for history, records `reopen_reason`, and sets asset status `REVIEW` plus `reopened=True`.
- `set_creative_status` may not overwrite `current_output_ref` for a locked `USER_APPROVED` asset unless `reopened=True`.

- [ ] **Step 4: Update ledger example and Skill UX**

Show `candidates[]`, `selected_candidate_id`, exact output ref, and the default transition: user selects → acknowledge candidate → next asset. Explicit reopen phrases are intent examples, not a hard-coded language parser requirement.

- [ ] **Step 5: Run Production selftest and verify GREEN**

Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/listing-production
 git commit -m "feat: lock exact user-selected asset candidates"
```

---

### Task 5: Set-level Creative QA

**Files:**
- Create: `.agents/skills/listing-production/scripts/set_level_qa.py`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`
- Modify: `.agents/skills/listing-production/references/production-qa.md`
- Modify: `.agents/skills/listing-production/SKILL.md`

**Interfaces:**
- Produces: `evaluate_set(asset_rows: list[dict]) -> dict` with shape:

```python
{
    "status": "CLEAR" | "REVIEW" | "REVISE",
    "issues": [
        {"type": "scene_repetition", "asset_ids": ["A05-01", "A05-02"], "message": "..."}
    ],
}
```

- [ ] **Step 1: Write failing behavioral set-QA tests**

```python
def test_identical_adjacent_visual_signatures_are_flagged() -> None:
    rows = [
        asset_direction("A1", scene="dark-living", composition="wide", tone="dark", scale="medium", proof="lifestyle"),
        asset_direction("A2", scene="dark-living", composition="wide", tone="dark", scale="medium", proof="lifestyle"),
    ]
    result = evaluate_set(rows)
    assert result["status"] == "REVISE"
    assert any(i["type"] == "composition_repetition" for i in result["issues"])


def test_same_brand_style_with_different_composition_can_clear() -> None:
    rows = [
        asset_direction("A1", scene="home", composition="wide", tone="brand-warm", scale="medium", proof="lifestyle"),
        asset_direction("A2", scene="home", composition="close-up", tone="brand-warm", scale="close-up", proof="mechanism"),
    ]
    assert evaluate_set(rows)["status"] == "CLEAR"
```

Add tests for repeated message role and poor proof-form diversity across 3+ adjacent assets.

- [ ] **Step 2: Run Production selftest and verify RED**

Expected: import/function failure.

- [ ] **Step 3: Implement deterministic set QA**

Implement six checks from the spec:

- exact adjacent scene repetition;
- exact adjacent composition repetition;
- runs of 3+ same tone/brightness family;
- runs of 3+ same product scale;
- runs of 3+ same proof form;
- adjacent duplicate `message_role` when both are non-empty.

Severity:

- identical full visual signature on adjacent assets => `REVISE`;
- one repeated dimension => `REVIEW`;
- no issues => `CLEAR`.

Do not infer aesthetics from pixels; this helper evaluates the structured Page Visual System / asset metadata. Human/model visual review can add issues, but may not erase deterministic repetition findings without an intentional-repeat note.

- [ ] **Step 4: Document cadence**

Production runs set QA:

- after first 2–3 assets in a region;
- at Gallery completion;
- after each logical enhanced-content cluster;
- before Production Freeze as final contact-sheet/set review.

Do not add a new gate name.

- [ ] **Step 5: Run Production selftest and verify GREEN**

Expected: all tests PASS.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/listing-production
 git commit -m "feat: add set-level creative quality checks"
```

---

### Task 6: Scope Delta + Scope-aware Progress/Freeze

**Files:**
- Modify: `.agents/skills/listing-production/scripts/production_state.py`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`
- Modify: `.agents/skills/listing-production/SKILL.md`

**Interfaces:**
- Produces: `_required_ids(handoff)` based only on current authoritative `asset_set`.
- Produces: `apply_scope_delta(handoff, delta) -> dict` that returns a new handoff with incremented `scope_revision`, updated current `asset_set`, and recorded delta.

- [ ] **Step 1: Write failing scope-delta test**

```python
def test_removed_asset_no_longer_counts_toward_progress_or_freeze() -> None:
    handoff = handoff_with_assets(["G1", "G2", "G3"])
    ledger = approved_ledger(["G1", "G2"])
    updated = apply_scope_delta(handoff, {
        "added": [], "removed": ["G3"], "changed": [],
        "reason": ["message merged into G2"],
    })
    progress = production_progress(updated, ledger)
    freeze = build_production_freeze(updated, ledger)
    assert progress == {"expected": 2, "approved": 2, "remaining": 0, "complete": True}
    assert freeze["ready_for_hardening"] is True
    assert ledger["assets"]["G1"]["status"] == "USER_APPROVED"
```

Add rejection tests for removing unknown IDs and adding duplicate IDs.

- [ ] **Step 2: Run Production selftest and verify RED**

Expected: `apply_scope_delta` missing.

- [ ] **Step 3: Implement scope delta**

Rules:

- deep-copy input;
- validate lists and non-empty reason;
- removed IDs must exist in current asset set;
- added entries must be supplied as complete asset objects, not bare IDs, so role/slot/message/evidence mode remain explicit;
- changed entries replace by same `asset_id` only;
- increment `scope_revision` from absent/1 to next integer;
- store concise `scope_delta` record;
- never mutate ledger or reopen unaffected assets.

- [ ] **Step 4: Run Production selftest and verify GREEN**

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/listing-production
 git commit -m "feat: make production scope revisions explicit"
```

---

### Task 7: Smallest Sufficient Cleanup

**Files:**
- Create: `.agents/skills/listing-production/scripts/cleanup_policy.py`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`
- Modify: `.agents/skills/listing-production/SKILL.md`
- Modify: `.agents/skills/listing-production/references/production-qa.md`

**Interfaces:**
- Produces: `plan_cleanup(problem_class, affected_assets, approved_assets, evidence_modes=None) -> dict`.
- Output: `{"reopen": [...], "preserve": [...], "reason": str}`.

- [ ] **Step 1: Write failing cleanup tests**

```python
def test_set_repetition_reopens_smallest_nonapproved_subset() -> None:
    result = plan_cleanup(
        "SET_REPETITION",
        affected_assets=["A05-01", "A05-02", "A05-03", "A06"],
        approved_assets=["A05-01", "A05-02"],
    )
    assert result["preserve"] == ["A05-01", "A05-02"]
    assert result["reopen"] == ["A05-03"]


def test_creative_mock_evidence_limitation_does_not_force_visual_rework() -> None:
    result = plan_cleanup(
        "EVIDENCE_LIMITATION",
        affected_assets=["A04"],
        approved_assets=["A04"],
        evidence_modes={"A04": "CREATIVE_MOCK"},
    )
    assert result["reopen"] == []
    assert result["preserve"] == ["A04"]
```

Also test `SINGLE_ASSET_DEFECT` reopens only that asset and `PRODUCT_DISTORTION` may reopen an approved asset because the defect is intrinsic.

- [ ] **Step 2: Run Production selftest and verify RED**

Expected: import/function failure.

- [ ] **Step 3: Implement deterministic minimal policy**

Support exactly these problem classes:

```python
PROBLEM_CLASSES = {
    "SINGLE_ASSET_DEFECT", "SET_REPETITION", "WRONG_MESSAGE_ROLE",
    "EVIDENCE_LIMITATION", "CLAIM_ERROR", "PRODUCT_DISTORTION",
}
```

Rules:

- single-asset defects/role/claim/product distortion => reopen only explicitly affected intrinsic-defect assets;
- evidence limitation + `CREATIVE_MOCK` => preserve creative image; annotate reason that evidence entitlement is limited;
- set repetition => preserve approved assets first, reopen the first non-approved affected asset only; if every affected asset is approved, return one asset in `reopen` only when the caller explicitly allows `reopen_approved=True`, otherwise return `reopen=[]` and a reason requiring user choice;
- never return all affected assets for `SET_REPETITION` by default.

- [ ] **Step 4: Run Production selftest and verify GREEN**

Expected: all tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/listing-production
 git commit -m "feat: minimize targeted production cleanup"
```

---

### Task 8: Router UX — Concise Continuation and Selection Acknowledgement

**Files:**
- Modify: `.agents/skills/japan-listing-demo/SKILL.md`
- Modify: `.agents/skills/japan-listing-demo/scripts/selftest_router.py`

**Interfaces:**
- Behavioral contract only; no new runtime state format.

- [ ] **Step 1: Write failing router tests**

Add source-contract tests requiring phrases equivalent to:

```text
transition acknowledgement <= 3 lines when nothing material changed
selected candidate -> acknowledge exact candidate/output -> next asset
explicit reopen required before producing a new candidate for a locked asset
```

Also assert the router does not introduce `Stage 7.25` or a new set-level gate name.

- [ ] **Step 2: Run router selftest and verify RED**

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/selftest_router.py
```

Expected: FAIL because v0.3.1 router does not contain these UX contracts.

- [ ] **Step 3: Update router wording minimally**

Add a compact UX section without expanding router size materially. Keep routing boundaries unchanged.

- [ ] **Step 4: Run router selftest and verify GREEN**

Expected: all router tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/japan-listing-demo
 git commit -m "feat: tighten production continuation UX"
```

---

### Task 9: Distribution Parity and v0.3.2 Release Metadata

**Files:**
- Modify: `.agents/skills/japan-listing-demo/scripts/validate_overlay.py`
- Modify: `.agents/skills/japan-listing-demo/core/manifest.yaml`
- Modify: `.agents/skills/japan-listing-demo/scripts/package_skill.py` only if explicit smoke assertions need new files
- Modify: `scripts/package_codex_bundle.py` only if explicit required-member checks need new files
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `docs/install.md`
- Modify: `VERSION`

**Interfaces:**
- Repository/Codex bundle and one-install compatibility ZIP must contain the same Planning/Production behavior.

- [ ] **Step 1: Add distribution RED assertions before bumping metadata**

In `validate_overlay.py`, require:

```text
listing-planning/scripts/account_capability.py
listing-production/scripts/set_level_qa.py
listing-production/scripts/cleanup_policy.py
```

and require `VERSION == 0.3.2` plus manifest marker `production-ux-set-level-creative-qa-v0.3.2`.

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
```

Expected: FAIL until version/manifest/docs are updated.

- [ ] **Step 2: Update version and manifest**

Set `VERSION` to:

```text
0.3.2
```

Add manifest patch lineage describing only:

- Page Visual System;
- Evidence Mode;
- account capability reuse hook;
- minimal set context;
- set-level Creative QA;
- selection lock/candidate history;
- scope delta;
- minimal cleanup;
- concise production UX.

Do not claim new Hardening gates.

- [ ] **Step 3: Update README / install / changelog**

Document:

- v0.3.2 is a Production UX/creative-quality release;
- account capability profile values remain private inputs, not public defaults;
- same one-command `$japan-listing-demo` invocation;
- package/install paths unchanged;
- rollback target `v0.3.1` remains valid.

- [ ] **Step 4: Verify both package modes**

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
python -m zipfile -l dist/japan-listing-demo.skill.zip
python -m zipfile -l dist/japan-listing-demo-codex-bundle.zip
```

Then unzip each package to separate temporary directories and execute the packaged Planning and Production selftests or smoke imports for:

```text
account_capability.py
set_level_qa.py
cleanup_policy.py
production_state.py
project_asset_packet.py
```

Expected: both package modes contain and can import/run the new behavior.

- [ ] **Step 5: Run full CI-equivalent validation**

Run:

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
python .agents/skills/listing-production/scripts/selftest_production.py
python .agents/skills/listing-hardening/scripts/selftest_hardening.py
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_router.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
```

Expected: all v0.3.1 integrity suites remain green and all new v0.3.2 tests pass.

- [ ] **Step 6: Commit**

```bash
git add VERSION CHANGELOG.md README.md docs/install.md .agents/skills/japan-listing-demo scripts/package_codex_bundle.py
 git commit -m "chore: prepare v0.3.2 production ux release"
```

---

### Task 10: Final PR Review Gate

**Files:**
- No runtime changes unless verification exposes a defect.
- Update Draft PR body only.

**Interfaces:**
- Produces a reviewable Draft PR; never merges automatically.

- [ ] **Step 1: Inspect branch diff against `main`**

Confirm all changes are limited to the v0.3.2 design/implementation scope and no private brand/account values leaked into the public repository.

- [ ] **Step 2: Verify latest-head GitHub Actions**

Require the latest PR-head workflow run to complete `success` after the final code/docs commit.

- [ ] **Step 3: Update Draft PR description**

Include:

- Light Bars pilot findings addressed;
- no new Stage/Gate;
- RED→GREEN run IDs for each new behavior cluster;
- final test counts;
- both ZIP package results;
- explicit maturity boundary: this improves Production UX/creative safeguards but does not replace Golden Set outcome validation.

- [ ] **Step 4: Stop before merge**

Keep PR Draft and wait for explicit user confirmation before marking Ready or merging.

---

## Self-Review

### Spec coverage

- Page Visual System: Task 1.
- Evidence Mode: Tasks 1 and 3.
- Minimal set context / context firewall: Task 3.
- Two-layer Creative QA and cadence: Task 5.
- Exact candidate selection lock/history: Task 4.
- Scope Delta and scope-aware Freeze: Task 6.
- Smallest Sufficient Cleanup: Task 7.
- Account Capability Profile hook: Task 2.
- Concise continuation/selection UX: Task 8.
- Packaging parity: Task 9.
- No new Stage/Gate, Hardening unchanged, public/private capability separation: Global Constraints + Tasks 8–9.
- Final explicit merge gate: Task 10.

### Placeholder scan

No `TBD`, `TODO`, “similar to”, or unspecified implementation steps remain. Every behavior-changing task starts with a concrete failing regression and ends with an explicit verification command.

### Type/interface consistency

- `evidence_mode` uses exactly `SOURCE_FAITHFUL | CREATIVE_MOCK | PROOF_VISUAL` across Planning and Production.
- Set QA uses `CLEAR | REVIEW | REVISE` only and is not a Hardening gate.
- Candidate state uses `USER_SELECTED` at candidate level and `USER_APPROVED` at asset level.
- Scope revision remains inside the current authoritative Production Handoff; progress/freeze continue to derive from `asset_set`.
- Capability resolver returns `REUSE | VERIFY` and never stores brand-specific values in public defaults.
