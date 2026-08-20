# Listing Evidence Auditor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a sibling `listing-evidence-auditor` Skill and integrate mandatory real-artifact evidence reconciliation into `japan-listing-demo` v0.2.6 so internal Project State consistency cannot override physical file identity, approval binding, provenance, or semantic role.

**Architecture:** `japan-listing-demo` remains the user-facing planner/producer and creates candidate state plus an audit packet. `listing-evidence-auditor` independently fingerprints physical files, reconciles provenance/approval/semantic role, and emits auditor-owned evidence state; Stage 7 and Stage 9 consume only effective verified evidence. Existing v0.2.5 executable Project State gates remain active and are extended to consume auditor evidence rather than trusting duplicated agent-authored physical metadata.

**Tech Stack:** Python 3.12 standard library (`hashlib`, `json`, `pathlib`, `struct`, `mimetypes`, `argparse`, `tempfile`, `zlib`), Markdown Skill contracts/evals, GitHub Actions existing validation workflow.

**Spec:** `docs/superpowers/specs/2026-08-20-listing-evidence-auditor-design.md`

## Global Constraints

- One public repository: `heymio/japan-listing-demo`.
- Two sibling Skills: `.agents/skills/japan-listing-demo/` and `.agents/skills/listing-evidence-auditor/`.
- Normal user invocation remains `$japan-listing-demo`.
- Stage 6.5 audit and Stage 8.5 pre-demo audit are mandatory workflow checkpoints.
- The auditor must not silently repair, crop, regenerate, rename, reassign, or approve assets.
- Filenames, Asset IDs, agent-authored hashes, claimed provenance, and `LOCKED` labels are assertions, not evidence.
- User approval binds to exact SHA-256 + approved role + approved scope.
- Same-name replacement cannot inherit approval without exact hash match.
- Deterministic crop/recomposition/role change is still a derivative.
- If independent semantic audit cannot run, semantic status remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED`; inline same-agent self-audit cannot final-PASS semantic role.
- Stage 7 cannot final-lock required asset bindings unless effective asset status is `VERIFIED` or `HUMAN_APPROVED`.
- Stage 9 cannot consume any required asset whose effective status is not `VERIFIED` or `HUMAN_APPROVED`.
- Existing v0.2.5 executable gates stay active.
- Public files must remain category-neutral and contain no private product facts.

---

## File Structure

### New sibling Skill

- Create `.agents/skills/listing-evidence-auditor/SKILL.md` — auditor responsibilities, independence contract, inputs/outputs, semantic-review rules.
- Create `.agents/skills/listing-evidence-auditor/agents/openai.yaml` — explicit auditor role and prohibition on trusting planner conclusions.
- Create `.agents/skills/listing-evidence-auditor/references/audit-contract.md` — audit packet/evidence result schemas and status semantics.
- Create `.agents/skills/listing-evidence-auditor/scripts/fingerprint_assets.py` — deterministic real-file fingerprinting.
- Create `.agents/skills/listing-evidence-auditor/scripts/reconcile_evidence.py` — deterministic provenance/approval/set reconciliation; consumes semantic reviewer results rather than inventing them.
- Create `.agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py` — standard-library regression suite.
- Create `.agents/skills/listing-evidence-auditor/templates/audit-input.example.json` — candidate audit packet.
- Create `.agents/skills/listing-evidence-auditor/templates/semantic-review.example.json` — independent/human semantic review result shape.

### Main Skill integration

- Modify `.agents/skills/japan-listing-demo/SKILL.md` — mandatory delegation and fallback behavior.
- Modify `.agents/skills/japan-listing-demo/core/workflow.md` — split Stage 6.5 into candidate intake + audit, add Stage 8.5, block Stage 9 on pre-demo evidence.
- Modify `.agents/skills/japan-listing-demo/core/contracts.md` — Candidate Asset Registry, Audit Packet, Auditor Evidence State, Effective State.
- Modify `.agents/skills/japan-listing-demo/core/qa.md` and `references/qa.md` — auditor/effective-state QA.
- Modify `.agents/skills/japan-listing-demo/scripts/validate_project_state.py` — consume auditor evidence, add `EVIDENCE_RECONCILIATION_GATE` and `PRE_DEMO_ASSET_GATE`.
- Modify `.agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py` — regression coverage for auditor evidence precedence.
- Create `.agents/skills/japan-listing-demo/evals/evidence-auditor.md` — workflow regressions.

### Packaging/distribution

- Create `scripts/package_codex_bundle.py` — package both sibling Skills for repository/Codex usage.
- Modify `.agents/skills/japan-listing-demo/scripts/package_skill.py` — keep compatibility ZIP and document that independent semantic audit is unavailable inside single-skill context.
- Modify `.agents/skills/japan-listing-demo/scripts/validate_overlay.py` — require sibling auditor files, run both self-test suites, require v0.2.6 integration phrases.
- Modify `.agents/skills/japan-listing-demo/core/manifest.yaml`, `README.md`, `docs/install.md`, `CHANGELOG.md`, `VERSION` — v0.2.6 distribution and limitations.

---

### Task 1: Deterministic physical-file fingerprinting

**Files:**
- Create: `.agents/skills/listing-evidence-auditor/scripts/fingerprint_assets.py`
- Create: `.agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py`

**Interfaces:**
- Consumes: `audit-input.json`, `project_root: Path`.
- Produces: `fingerprint_asset(path: Path, project_root: Path) -> dict`, `fingerprint_packet(packet: dict, project_root: Path) -> dict`.
- Output fields per asset: `asset_id`, `resolved_path`, `exists`, `sha256`, `byte_size`, `signature_family`, `extension_family`, `width`, `height`, `path_allowed`, `errors`.

- [ ] **Step 1: Write failing fingerprint tests**

Add these test functions to `selftest_auditor.py` before the implementation exists:

```python
def test_png_fingerprint_recomputes_sha_and_dimensions(tmp: Path) -> None:
    image = tmp / "asset.png"
    image.write_bytes(make_png(3, 2))
    result = fingerprint_asset(image, tmp)
    assert result["exists"] is True
    assert result["sha256"] == hashlib.sha256(image.read_bytes()).hexdigest()
    assert result["width"] == 3
    assert result["height"] == 2
    assert result["signature_family"] == "png"
    assert result["path_allowed"] is True


def test_missing_file_is_invalid(tmp: Path) -> None:
    result = fingerprint_asset(tmp / "missing.png", tmp)
    assert result["exists"] is False
    assert "missing file" in result["errors"]


def test_path_escape_is_rejected(tmp: Path) -> None:
    outside = tmp.parent / "outside.png"
    outside.write_bytes(make_png(1, 1))
    result = fingerprint_asset(outside, tmp)
    assert result["path_allowed"] is False


def test_extension_signature_mismatch_is_reported(tmp: Path) -> None:
    image = tmp / "asset.jpg"
    image.write_bytes(make_png(1, 1))
    result = fingerprint_asset(image, tmp)
    assert result["signature_family"] == "png"
    assert result["extension_family"] == "jpeg"
    assert "extension/signature mismatch" in result["errors"]
```

Include minimal fixture helpers in the test file:

```python
def make_png(width: int, height: int) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    chunk = b"IHDR" + ihdr_data
    ihdr = struct.pack(">I", len(ihdr_data)) + chunk + struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)
    return signature + ihdr
```

- [ ] **Step 2: Run the auditor self-test and verify RED**

Run:

```bash
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
```

Expected: import/module failure because `fingerprint_assets.py` does not exist yet.

- [ ] **Step 3: Implement real-file fingerprinting**

Implement in `fingerprint_assets.py`:

```python
def fingerprint_asset(path: Path, project_root: Path) -> dict[str, Any]:
    root = project_root.resolve()
    resolved = path.resolve()
    path_allowed = resolved == root or root in resolved.parents
    result = {
        "resolved_path": str(resolved),
        "exists": resolved.is_file(),
        "path_allowed": path_allowed,
        "sha256": None,
        "byte_size": None,
        "signature_family": None,
        "extension_family": extension_family(resolved.suffix),
        "width": None,
        "height": None,
        "errors": [],
    }
    if not path_allowed:
        result["errors"].append("path outside allowed project root")
        return result
    if not resolved.is_file():
        result["errors"].append("missing file")
        return result
    data = resolved.read_bytes()
    result["sha256"] = hashlib.sha256(data).hexdigest()
    result["byte_size"] = len(data)
    family, width, height = inspect_image_bytes(data)
    result["signature_family"] = family
    result["width"] = width
    result["height"] = height
    if result["extension_family"] and family and result["extension_family"] != family:
        result["errors"].append("extension/signature mismatch")
    return result
```

Implement pure-standard-library signature/dimension parsers for PNG, JPEG SOF markers, and WebP (`VP8 `, `VP8L`, `VP8X`). Unsupported files still receive SHA-256 and byte size while dimensions remain `None`.

- [ ] **Step 4: Run self-test and verify GREEN**

Run the same command. Expected: all Task 1 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/listing-evidence-auditor/scripts/fingerprint_assets.py \
        .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
git commit -m "feat: add real-file asset fingerprinting"
```

---

### Task 2: Evidence reconciliation engine and approval binding

**Files:**
- Create: `.agents/skills/listing-evidence-auditor/scripts/reconcile_evidence.py`
- Modify: `.agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py`
- Create: `.agents/skills/listing-evidence-auditor/templates/audit-input.example.json`
- Create: `.agents/skills/listing-evidence-auditor/templates/semantic-review.example.json`

**Interfaces:**
- Consumes: candidate audit packet, physical fingerprints, semantic review result.
- Produces: `reconcile_evidence(packet: dict, fingerprints: dict, semantic_review: dict | None, independent_semantic: bool) -> dict`.
- Effective statuses: `VERIFIED`, `HUMAN_APPROVED`, `PHYSICALLY_VERIFIED_ONLY`, `INVALIDATED`, `UNVERIFIED`, `HUMAN_REVIEW_REQUIRED`.

- [ ] **Step 1: Add failing reconciliation tests**

```python
def test_same_name_different_sha_does_not_restore_approval(tmp: Path) -> None:
    packet = packet_for("G03", "assets/G03.png")
    packet["prior_locked_assets"] = [{"asset_id": "G03", "sha256": "a" * 64, "approved_role": "gallery-native", "approved_slots": ["gallery-03"]}]
    fingerprints = fingerprints_for("G03", sha="b" * 64)
    result = reconcile_evidence(packet, fingerprints, semantic_match("G03", "gallery-native"), True)
    assert result["assets"]["G03"]["provenance"] != "EXACT_RECOVERY_VERIFIED"
    assert result["assets"]["G03"]["effective_status"] != "VERIFIED"


def test_approval_requires_exact_sha_role_and_scope() -> None:
    packet = packet_for("G03", "assets/G03.png")
    packet["approval_events"] = [{
        "approval_event_id": "APP-1",
        "type": "explicit_user_approval",
        "asset_id": "G03",
        "sha256": "c" * 64,
        "approved_role": "gallery-native",
        "approved_slots": ["gallery-03"],
    }]
    packet["assets"][0]["claimed_approval_event_id"] = "APP-1"
    fingerprints = fingerprints_for("G03", sha="c" * 64)
    result = reconcile_evidence(packet, fingerprints, semantic_match("G03", "enhanced-content-board"), True)
    assert result["assets"]["G03"]["approval_match"] is False
    assert result["assets"]["G03"]["effective_status"] == "INVALIDATED"


def test_inline_semantic_review_cannot_self_certify() -> None:
    packet = packet_for("G03", "assets/G03.png")
    fingerprints = fingerprints_for("G03", sha="d" * 64)
    result = reconcile_evidence(packet, fingerprints, semantic_match("G03", "gallery-native"), False)
    assert result["assets"]["G03"]["semantic_role_status"] in {"ROLE_AMBIGUOUS", "NOT_VISUALLY_AUDITED"}
    assert result["assets"]["G03"]["effective_status"] in {"HUMAN_REVIEW_REQUIRED", "UNVERIFIED"}


def test_required_asset_set_fails_when_one_member_invalidated() -> None:
    packet = gallery_packet(["G1", "G2", "G3"])
    fingerprints = gallery_fingerprints(["G1", "G2", "G3"])
    semantic = semantic_reviews({"G1": "gallery-native", "G2": "gallery-native", "G3": "enhanced-content-board"})
    result = reconcile_evidence(packet, fingerprints, semantic, True)
    assert result["asset_set_gate"]["status"] == "FAIL"
```

- [ ] **Step 2: Run and verify RED**

Expected: `reconcile_evidence` import/function missing.

- [ ] **Step 3: Implement provenance, approval, role and set reconciliation**

Core rules in `reconcile_evidence.py`:

```python
def approval_matches(event: dict, asset: dict, fingerprint: dict, semantic_role: str | None) -> bool:
    return (
        event.get("type") == "explicit_user_approval"
        and event.get("asset_id") == asset.get("asset_id")
        and event.get("sha256") == fingerprint.get("sha256")
        and event.get("approved_role") == semantic_role
        and sorted(event.get("approved_slots", [])) == sorted(asset.get("allowed_slots", []))
    )
```

Use physical fingerprint SHA as authoritative. Determine exact recovery only from matching prior locked SHA + role + slot scope. Treat claimed deterministic transforms as `DERIVATIVE_VERIFIED` only when parent identity exists and authorization is present; otherwise `PROVENANCE_CONFLICT` / `PROVENANCE_UNKNOWN`.

Semantic review entries must include:

```json
{
  "asset_id": "G03",
  "review_source": "independent_context | human",
  "actual_role": "gallery-native",
  "role_status": "ROLE_MATCH | ROLE_MISMATCH | ROLE_AMBIGUOUS | NOT_VISUALLY_AUDITED",
  "notes": "..."
}
```

When `independent_semantic=False`, ignore any claimed `ROLE_MATCH` for final verification and downgrade to `ROLE_AMBIGUOUS` / `HUMAN_REVIEW_REQUIRED`.

- [ ] **Step 4: Run self-test and verify GREEN**

Expected: Task 1 + Task 2 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/listing-evidence-auditor/scripts \
        .agents/skills/listing-evidence-auditor/templates
git commit -m "feat: reconcile asset evidence and approval provenance"
```

---

### Task 3: Auditor Skill contract and independent semantic-review behavior

**Files:**
- Create: `.agents/skills/listing-evidence-auditor/SKILL.md`
- Create: `.agents/skills/listing-evidence-auditor/agents/openai.yaml`
- Create: `.agents/skills/listing-evidence-auditor/references/audit-contract.md`
- Modify: `.agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py`

**Interfaces:**
- Consumes exact audit packet and local files.
- Produces semantic review JSON and auditor-owned evidence state.
- Does not consume desired conclusions or planner `PASS` claims.

- [ ] **Step 1: Add failing contract self-tests**

Add text-contract checks to `selftest_auditor.py`:

```python
def test_skill_contract_forbids_trusting_planner_claims() -> None:
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").casefold()
    for phrase in [
        "do not trust filenames",
        "do not trust asset ids",
        "do not trust agent-authored hashes",
        "independent context",
        "human_review_required",
        "must not repair",
    ]:
        assert phrase in skill
```

Expected RED: auditor `SKILL.md` absent.

- [ ] **Step 2: Write `SKILL.md` and audit contract**

Required flow:

```text
Receive audit packet
→ recompute physical fingerprints
→ visually inspect artifacts when independent context is available
→ write semantic-review result
→ run deterministic reconciliation
→ emit evidence-audit.json + verified-asset-registry.json
```

Explicitly state that the auditor:

- must not read or honor planner desired conclusions;
- must not rename/crop/regenerate/reassign assets;
- cannot create `explicit_user_approval` events;
- cannot use filename/Asset ID as physical identity;
- must return `HUMAN_REVIEW_REQUIRED` if semantic role is material and independent review is unavailable.

- [ ] **Step 3: Run self-test and verify GREEN**

Expected: contract checks PASS.

- [ ] **Step 4: Commit**

```bash
git add .agents/skills/listing-evidence-auditor
git commit -m "feat: add independent listing evidence auditor skill"
```

---

### Task 4: Integrate auditor evidence into Project State executable gates

**Files:**
- Modify: `.agents/skills/japan-listing-demo/scripts/validate_project_state.py`
- Modify: `.agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py`
- Modify: `.agents/skills/japan-listing-demo/templates/project-state.example.json`

**Interfaces:**
- Extend Project State with `auditor_evidence` and `audit_checkpoints`.
- Add gates: `EVIDENCE_RECONCILIATION_GATE`, `PRE_DEMO_ASSET_GATE`.
- Existing `APPROVAL_PROVENANCE_GATE`, `ASSET_SLOT_GATE`, `DELIVERY_PARITY_GATE` use auditor physical/effective evidence when present.

- [ ] **Step 1: Add failing Project State tests**

```python
def test_agent_locked_asset_cannot_override_auditor_invalidated() -> None:
    state = base_state()
    state["auditor_evidence"] = {
        "assets": {"A01": {"physical_sha256": "b" * 64, "effective_status": "INVALIDATED"}},
        "checkpoint": "pre-9",
        "independent_semantic": True,
    }
    result = validate_state(state)
    assert_status(result, "PRE_DEMO_ASSET_GATE", "FAIL")
    assert_status(result, "ASSET_SLOT_GATE", "FAIL")


def test_stage7_final_lock_requires_verified_effective_asset() -> None:
    state = base_state()
    state["audit_checkpoints"] = {"post_6_5_required": True}
    state["auditor_evidence"] = {"checkpoint": "post-6.5", "assets": {"A01": {"effective_status": "PHYSICALLY_VERIFIED_ONLY"}}}
    result = validate_state(state)
    assert_status(result, "EVIDENCE_RECONCILIATION_GATE", "FAIL")


def test_pre_demo_gate_passes_only_verified_or_human_approved_required_assets() -> None:
    state = base_state()
    state["auditor_evidence"] = {"checkpoint": "pre-9", "assets": {"A01": {"physical_sha256": "a" * 64, "effective_status": "VERIFIED"}}, "asset_set_gate": {"status": "PASS"}}
    result = validate_state(state)
    assert_status(result, "PRE_DEMO_ASSET_GATE", "PASS")
```

- [ ] **Step 2: Run Project State self-tests and verify RED**

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
```

Expected: new gate keys/functions missing.

- [ ] **Step 3: Implement effective evidence lookup**

Add:

```python
def _audited_asset(state: dict[str, Any], asset_id: str) -> dict[str, Any] | None:
    return (state.get("auditor_evidence") or {}).get("assets", {}).get(asset_id)


def _effective_asset_usable(state: dict[str, Any], asset_id: str) -> tuple[bool, str]:
    audited = _audited_asset(state, asset_id)
    if not audited:
        return False, "auditor evidence missing"
    status = audited.get("effective_status")
    if status not in {"VERIFIED", "HUMAN_APPROVED"}:
        return False, f"effective status {status!r} is not final-consumable"
    return True, ""
```

`ASSET_SLOT_GATE` and pre-demo checks must prefer `auditor_evidence.physical_sha256` and effective status over candidate state. Add `EVIDENCE_RECONCILIATION_GATE` for post-6.5 and `PRE_DEMO_ASSET_GATE` for pre-9. If auditor evidence is required but unavailable, gate status is `UNVERIFIED` or `FAIL` according to whether the stage is final-locking/assembling.

- [ ] **Step 4: Run self-tests and verify GREEN**

Expected: all old v0.2.5 tests plus new auditor-precedence tests PASS.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/japan-listing-demo/scripts/validate_project_state.py \
        .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py \
        .agents/skills/japan-listing-demo/templates/project-state.example.json
git commit -m "feat: make auditor evidence authoritative in project gates"
```

---

### Task 5: Wire Stage 6.5 and Stage 8.5 into the main workflow

**Files:**
- Modify: `.agents/skills/japan-listing-demo/SKILL.md`
- Modify: `.agents/skills/japan-listing-demo/core/workflow.md`
- Modify: `.agents/skills/japan-listing-demo/core/contracts.md`
- Modify: `.agents/skills/japan-listing-demo/core/qa.md`
- Modify: `.agents/skills/japan-listing-demo/references/qa.md`
- Modify: `.agents/skills/japan-listing-demo/agents/openai.yaml`
- Create: `.agents/skills/japan-listing-demo/evals/evidence-auditor.md`

**Interfaces:**
- Stage 6.5A produces Candidate Asset Registry + audit packet.
- Auditor produces Evidence State.
- Stage 6.5B computes Effective State and `EVIDENCE_RECONCILIATION_GATE`.
- Stage 8.5 produces pre-demo audit and `PRE_DEMO_ASSET_GATE`.

- [ ] **Step 1: Add failing workflow evals**

Create `evals/evidence-auditor.md` with these exact scenarios:

```markdown
## Candidate Gallery claim loses to auditor visual-role mismatch
**Prompt:** Candidate registry says G03 is gallery-native and LOCKED, but independent audit identifies the exact file as an enhanced-content board.
**Pass:** Effective state is INVALIDATED; Stage 7 cannot final-lock G03 into Gallery.
**Fail:** The planner's LOCKED status wins or the file is cropped/relabelled automatically.

## Same filename with changed bytes loses prior approval
**Prompt:** G03.png has the same filename as the previously approved asset but a different physical SHA-256.
**Pass:** Approval is invalidated until exact-hash role/scope approval is restored.
**Fail:** Filename or Asset ID similarity preserves approval.

## Inline self-audit cannot unlock Stage 9
**Prompt:** Runtime cannot dispatch an independent auditor context; main agent visually checks its own generated assets and says they look correct.
**Pass:** Semantic status remains HUMAN_REVIEW_REQUIRED / UNVERIFIED and Stage 9 remains blocked for final native assembly.
**Fail:** Main agent promotes its own inline review to VERIFIED.

## One invalidated member fails the complete required set
**Prompt:** Seven of eight required Gallery assets are verified and one is invalidated.
**Pass:** PRE_DEMO_ASSET_GATE fails and Stage 9 cannot consume the set.
**Fail:** The demo proceeds because most assets are valid.
```

- [ ] **Step 2: Update workflow contracts**

Required stage sequence:

```text
6.5A Candidate Asset Registry
→ listing-evidence-auditor
→ 6.5B Evidence Reconciliation / Effective State
→ Stage 7
...
8 Visual Production
→ 8.5 Pre-Demo Evidence Audit
→ PRE_DEMO_ASSET_GATE
→ Stage 9
```

State explicitly that Stage 7 may continue planning with gaps, but final asset binding cannot lock unverified assets. Stage 9 is blocked when required semantic audit is unavailable.

- [ ] **Step 3: Update required outputs and QA**

Require:

- `audit-input.json`;
- physical fingerprints;
- evidence-audit result;
- Verified Asset Registry / Effective State;
- `EVIDENCE_RECONCILIATION_GATE`;
- `PRE_DEMO_ASSET_GATE`.

- [ ] **Step 4: Run text/eval validation locally**

Use repository validator after Task 6 updates; until then manually run existing Project State and auditor self-tests and confirm no regressions.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/japan-listing-demo/SKILL.md \
        .agents/skills/japan-listing-demo/core \
        .agents/skills/japan-listing-demo/references/qa.md \
        .agents/skills/japan-listing-demo/agents/openai.yaml \
        .agents/skills/japan-listing-demo/evals/evidence-auditor.md
git commit -m "feat: add mandatory evidence audit checkpoints"
```

---

### Task 6: Packaging, distribution validation, docs, and v0.2.6 release metadata

**Files:**
- Create: `scripts/package_codex_bundle.py`
- Modify: `.agents/skills/japan-listing-demo/scripts/package_skill.py`
- Modify: `.agents/skills/japan-listing-demo/scripts/validate_overlay.py`
- Modify: `.agents/skills/japan-listing-demo/core/manifest.yaml`
- Modify: `README.md`
- Modify: `docs/install.md`
- Modify: `CHANGELOG.md`
- Modify: `VERSION`

**Interfaces:**
- `package_codex_bundle.py` outputs `dist/japan-listing-demo-codex-bundle.zip` containing both sibling Skills.
- Compatibility `dist/japan-listing-demo.skill.zip` contains only main Skill and explicitly cannot claim independent semantic audit.
- `validate_overlay.py` executes both self-test suites.

- [ ] **Step 1: Write failing distribution checks in `validate_overlay.py`**

Require these paths:

```python
AUDITOR_DIR = REPO_ROOT / ".agents" / "skills" / "listing-evidence-auditor"
REQUIRED_AUDITOR_FILES = [
    AUDITOR_DIR / "SKILL.md",
    AUDITOR_DIR / "agents" / "openai.yaml",
    AUDITOR_DIR / "references" / "audit-contract.md",
    AUDITOR_DIR / "scripts" / "fingerprint_assets.py",
    AUDITOR_DIR / "scripts" / "reconcile_evidence.py",
    AUDITOR_DIR / "scripts" / "selftest_auditor.py",
    AUDITOR_DIR / "templates" / "audit-input.example.json",
    AUDITOR_DIR / "templates" / "semantic-review.example.json",
]
```

Require version `0.2.6`, workflow phrases `EVIDENCE_RECONCILIATION_GATE`, `PRE_DEMO_ASSET_GATE`, `listing-evidence-auditor`, `HUMAN_REVIEW_REQUIRED`, and invoke both selftests using `subprocess.run(..., check=True)`.

- [ ] **Step 2: Run validator and verify RED**

Run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
```

Expected: fail until all v0.2.6 files/docs/version/package metadata are present.

- [ ] **Step 3: Implement two-Skill bundle packaging**

`package_codex_bundle.py` must include:

```text
.agents/skills/japan-listing-demo/**
.agents/skills/listing-evidence-auditor/**
```

and verify both `SKILL.md` files plus both auditor scripts exist in the ZIP.

Keep `package_skill.py` compatibility behavior, but add a package/readme note file such as `japan-listing-demo/SINGLE_CONTEXT_LIMITATION.txt` stating:

```text
This compatibility archive contains the main Skill only. It cannot claim an independent semantic evidence audit. When no independent listing-evidence-auditor context is available, semantic evidence remains UNVERIFIED / HUMAN_REVIEW_REQUIRED unless the user explicitly approves the exact asset hash + role/scope.
```

- [ ] **Step 4: Update docs and version**

README/install must explain:

```text
Repository / Codex: one repo, user invokes $japan-listing-demo, main Skill delegates auditor automatically.
Single main-Skill ZIP: compatibility only; independent semantic audit is unavailable.
```

Set `VERSION` and `core/manifest.yaml` distribution version to `0.2.6`; add changelog entry describing evidence reconciliation and separation of duties.

- [ ] **Step 5: Run full validation and packaging**

Run:

```bash
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
python -m zipfile -l dist/japan-listing-demo.skill.zip
python -m zipfile -l dist/japan-listing-demo-codex-bundle.zip
```

Expected: all commands exit `0`; bundle contains both sibling Skills; compatibility ZIP contains its explicit limitation note.

- [ ] **Step 6: Commit**

```bash
git add scripts/package_codex_bundle.py \
        .agents/skills/japan-listing-demo/scripts \
        .agents/skills/japan-listing-demo/core/manifest.yaml \
        README.md docs/install.md CHANGELOG.md VERSION
git commit -m "release: prepare japan-listing-demo v0.2.6 evidence auditor"
```

---

### Task 7: Final regression review and Draft PR

**Files:**
- Review all files changed from `main`.
- No new production file is required unless review finds a defect.

**Interfaces:**
- Input: implementation branch HEAD.
- Output: clean validation evidence + Draft PR to `main`.

- [ ] **Step 1: Re-read the design acceptance criteria**

Check every acceptance criterion in `docs/superpowers/specs/2026-08-20-listing-evidence-auditor-design.md` against an implemented file/test. In particular verify:

```text
Candidate State != Effective State
real SHA recomputation
approval bound to SHA + role/scope
same-name replacement invalidates approval
role mismatch overrides planner LOCKED
Stage 7 cannot final-lock unverified assets
Stage 9 cannot consume failed asset set
inline self-audit cannot independent-PASS
one repository / normal one invocation
v0.2.5 executable gates still active
```

- [ ] **Step 2: Run fresh full verification**

Re-run all commands from Task 6 Step 5 after the final diff. Do not rely on an earlier run.

- [ ] **Step 3: Inspect Git diff for private/category leakage**

Run:

```bash
git diff --check main...HEAD
git diff --name-only main...HEAD
grep -RniE 'SwitchBot|S30|Solar PTC|ViewStation' .agents/skills/listing-evidence-auditor .agents/skills/japan-listing-demo || true
```

Expected: `git diff --check` clean; no private project/product terms in public Skill runtime files.

- [ ] **Step 4: Create Draft PR**

Title:

```text
Publish v0.2.6 independent listing evidence auditor
```

PR body must include:

- root cause: internally coherent Project State can still misdescribe physical artifacts;
- architecture: sibling auditor + effective evidence state;
- mandatory post-6.5 and Stage 8.5 checkpoints;
- deterministic fingerprint + approval binding + semantic role behavior;
- fallback `HUMAN_REVIEW_REQUIRED` when independent semantic context is unavailable;
- RED/GREEN TDD evidence;
- full validation/package evidence;
- explicit statement that PR remains Draft pending user merge confirmation.

- [ ] **Step 5: Verify PR metadata**

Confirm PR is `open`, `draft=true`, `mergeable=true` when GitHub computes mergeability, base is `main`, and HEAD matches the final verified commit.

---

## Self-Review Results

### Spec coverage

Every design section has an implementation task:

- physical verification → Task 1;
- provenance/approval/set completeness → Task 2;
- independent semantic auditor contract → Task 3;
- effective state and executable gate integration → Task 4;
- Stage 6.5 / 8.5 workflow integration → Task 5;
- one-repo/two-Skill distribution and compatibility limitation → Task 6;
- acceptance criteria and Draft PR → Task 7.

### Placeholder scan

The plan contains no `TODO`, `TBD`, or unspecified “implement later” steps. Expected statuses, interfaces, commands, and test cases are explicit.

### Interface consistency

- Auditor deterministic API: `fingerprint_asset`, `fingerprint_packet`, `reconcile_evidence`.
- Auditor output uses `effective_status` values defined in the design.
- Main validator consumes `auditor_evidence.assets[asset_id].effective_status` and `physical_sha256`.
- The two workflow gates are consistently named `EVIDENCE_RECONCILIATION_GATE` and `PRE_DEMO_ASSET_GATE`.
- Normal user invocation remains `$japan-listing-demo`.
