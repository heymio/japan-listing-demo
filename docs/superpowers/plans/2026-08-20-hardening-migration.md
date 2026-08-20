# Hardening Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `listing-hardening` sibling Skill, move final evidence/delivery responsibilities to Stage 8.5–10, preserve v0.2.5/v0.2.6 protections, and change early evidence audit from mandatory project-wide behavior to targeted inherited-asset audit only.

**Architecture:** Hardening consumes the Production Freeze, exact final files, locked module/page plan, relevant Project Brief fields, and frontend evidence. It owns physical-file validation, evidence-auditor orchestration, exact approval/provenance, transforms, slot integrity, module origin, frontend fidelity, demo assembly, delivery parity, and final QA. The existing executable validator is migrated to the Hardening Skill while the old script path remains a compatibility shim for one release. Full `listing-evidence-auditor` audit is mandatory at Stage 8.5; `EVIDENCE_RECONCILIATION_GATE` becomes applicable only when targeted inherited-asset audit was explicitly requested earlier.

**Tech Stack:** Python 3.12 standard library, existing `listing-evidence-auditor` scripts, JSON Delivery State / Project State compatibility, Markdown hardening references/evals, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-08-20-creative-first-hardening-architecture-design.md`

## Global Constraints

- This plan assumes Planning and Production slices are already implemented.
- Preserve all proven safeguards: Amazon/module budget, locked module origin, transform authorization, exact approval provenance, real-file fingerprinting, semantic role audit, complete required asset set, slot integrity, delivery parity, and frontend fidelity.
- Full evidence audit is mandatory at Stage 8.5 on the exact final files from Production Freeze.
- Fresh projects do not require full project-wide post-6.5 audit by default.
- Targeted early audit remains available for inherited/reused previously approved exact assets; when requested, its evidence must still be authoritative.
- `USER_APPROVED` creative status alone is never final-consumable delivery evidence.
- `listing-evidence-auditor` remains a separate sibling Skill and retains its independent/human semantic-review limitation.
- Wrong files, unauthorized derivatives, role mismatch, incomplete sets, or plan drift must invalidate delivery state rather than being normalized by rewriting registries.
- Keep the old `.agents/skills/japan-listing-demo/scripts/validate_project_state.py` CLI/API working as a compatibility shim until the final integration/release slice.
- Public files remain category-neutral; no private project examples.
- `VERSION` remains `0.2.6` in this slice.

---

## File Structure

### New Hardening Skill

- Create `.agents/skills/listing-hardening/SKILL.md` — Stage 8.5–10 responsibilities and inputs.
- Create `.agents/skills/listing-hardening/agents/openai.yaml` — hardening-only prompt.
- Create `.agents/skills/listing-hardening/references/asset-integrity.md` — exact file, approval, transform, role, set, slot rules.
- Create `.agents/skills/listing-hardening/references/executable-gates.md` — machine gate contract migrated from current reference.
- Create `.agents/skills/listing-hardening/references/frontend-fidelity.md` — implementation/fidelity half of channel-native demo rules.
- Create `.agents/skills/listing-hardening/references/final-qa.md` — final delivery QA.
- Create `.agents/skills/listing-hardening/templates/delivery-state.example.json` — Hardening-owned delivery state.
- Create `.agents/skills/listing-hardening/scripts/validate_delivery_state.py` — canonical validator implementation, preserving `canonical_hash()` and `validate_state()` APIs.
- Create `.agents/skills/listing-hardening/scripts/selftest_hardening.py` — selective early-audit and mandatory pre-demo regressions.
- Create `.agents/skills/listing-hardening/evals/hardening.md` — anonymized hardening scenarios.

### Compatibility / existing files

- Modify `.agents/skills/japan-listing-demo/scripts/validate_project_state.py` — compatibility shim that loads/re-exports the Hardening validator.
- Modify `.agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py` — import compatibility must remain green; add no new business logic here after migration.
- Modify `.github/workflows/validate-japan-listing-demo.yml` — run Hardening self-tests.
- Do not yet rewrite the public Router/README/package bundle; final integration owns that.

---

### Task 1: Establish the Hardening Skill boundary

**Files:**
- Create: `.agents/skills/listing-hardening/scripts/selftest_hardening.py`
- Create: `.agents/skills/listing-hardening/SKILL.md`
- Create: `.agents/skills/listing-hardening/agents/openai.yaml`

**Interfaces:**
- Owns Stage `8.5`, `9`, `10`.
- Consumes `Production Freeze`, exact final files, locked plan/slot contract, relevant Project Brief fields, frontend evidence.
- Delegates exact-file evidence work to `listing-evidence-auditor`.
- Produces Delivery State and final demo/QA results.

- [ ] **Step 1: Write failing Hardening boundary tests**

Create `selftest_hardening.py`:

```python
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_hardening_owns_only_final_delivery_plane() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    for phrase in [
        "name: listing-hardening", "stage 8.5", "stage 9", "stage 10",
        "production freeze", "listing-evidence-auditor", "delivery state",
    ]:
        assert phrase in text
    for forbidden in ["consumer strategy", "voc research", "visual generation brief"]:
        assert forbidden not in text


def test_full_audit_is_mandatory_at_stage_8_5_not_fresh_stage_6_5() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "mandatory full audit" in text
    assert "stage 8.5" in text
    assert "targeted early audit" in text
    assert "inherited" in text or "previously approved exact asset" in text


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-hardening boundary tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run and verify RED**

```bash
python .agents/skills/listing-hardening/scripts/selftest_hardening.py
```

Expected: FAIL because `listing-hardening/SKILL.md` does not exist.

- [ ] **Step 3: Create minimal Hardening Skill and prompt**

`SKILL.md` must state:

```markdown
---
name: listing-hardening
description: Use when hardening Stage 8.5–10 final listing assets, assembling the verified channel demo, and running delivery QA.
---

# Listing Hardening

## Core question
Are the final artifacts exact, safe, channel-correct, and ready to assemble/deliver?

## Inputs
Production Freeze, exact final files, locked page/module plan, final Asset-to-Slot contract, relevant Project Brief fields, and frontend evidence.

## Audit timing
Stage 8.5 runs the mandatory full audit through listing-evidence-auditor. Planning may request a targeted early audit only for inherited/reused previously approved exact assets; a fresh project does not run the full project-wide audit before final assets exist.

## Output
Delivery State, verified demo assembly, delivery parity, and Final QA.
```

Use a short hardening-only `agents/openai.yaml`.

- [ ] **Step 4: Run and verify GREEN**

Expected:

```text
PASS: 2 listing-hardening boundary tests
```

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/listing-hardening/SKILL.md \
        .agents/skills/listing-hardening/agents/openai.yaml \
        .agents/skills/listing-hardening/scripts/selftest_hardening.py
git commit -m "feat: add final delivery hardening boundary"
```

---

### Task 2: Move the canonical executable validator into Hardening with compatibility equivalence

**Files:**
- Create: `.agents/skills/listing-hardening/scripts/validate_delivery_state.py`
- Modify: `.agents/skills/japan-listing-demo/scripts/validate_project_state.py`
- Modify: `.agents/skills/listing-hardening/scripts/selftest_hardening.py`

**Interfaces:**
- New canonical API: `canonical_hash(value) -> str`, `validate_state(state, policy=None) -> dict`, `main() -> int`.
- Old API/CLI path re-exports those exact names and behavior.
- Packaged policy path must resolve from the repository/main-skill data file until final integration decides its permanent owner.

- [ ] **Step 1: Add failing equivalence tests before migration**

Append:

```python
import importlib.util
import json
import sys

REPO_ROOT = SKILL_DIR.parents[2]
OLD_VALIDATOR = REPO_ROOT / ".agents" / "skills" / "japan-listing-demo" / "scripts" / "validate_project_state.py"
NEW_VALIDATOR = SKILL_DIR / "scripts" / "validate_delivery_state.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_new_validator_exists_and_matches_legacy_api() -> None:
    old = load_module(OLD_VALIDATOR, "legacy_validator")
    new = load_module(NEW_VALIDATOR, "hardening_validator")
    assert callable(new.canonical_hash)
    assert callable(new.validate_state)
    assert new.canonical_hash({"b": 2, "a": 1}) == old.canonical_hash({"b": 2, "a": 1})
```

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because `validate_delivery_state.py` does not exist.

- [ ] **Step 3: Move current validator implementation to Hardening**

Copy/refactor the current `validate_project_state.py` implementation into `listing-hardening/scripts/validate_delivery_state.py` without changing gate behavior yet.

Change its packaged policy location to an explicit repository-relative path:

```python
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[3]
DEFAULT_POLICY_PATH = REPO_ROOT / ".agents" / "skills" / "japan-listing-demo" / "data" / "channel-policy-limits.json"
```

- [ ] **Step 4: Replace the old script with a compatibility loader**

The old file must dynamically load the new implementation because hyphenated Skill directory names are not importable packages:

```python
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[4]
TARGET = REPO_ROOT / ".agents" / "skills" / "listing-hardening" / "scripts" / "validate_delivery_state.py"
SPEC = importlib.util.spec_from_file_location("listing_hardening_validate_delivery_state", TARGET)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load hardening validator: {TARGET}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

canonical_hash = MODULE.canonical_hash
validate_state = MODULE.validate_state
main = MODULE.main

if __name__ == "__main__":
    raise SystemExit(main())
```

Validate the `parents[]` index against the actual path before committing; the resolved `TARGET` must equal `.agents/skills/listing-hardening/scripts/validate_delivery_state.py`.

- [ ] **Step 5: Run old and new self-tests**

```bash
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/listing-hardening/scripts/selftest_hardening.py
```

Expected: both exit 0 and the existing 12 project-state regressions remain unchanged.

- [ ] **Step 6: Commit the validator ownership migration**

```bash
git add .agents/skills/listing-hardening/scripts \
        .agents/skills/japan-listing-demo/scripts/validate_project_state.py
git commit -m "refactor: move delivery validator to hardening"
```

---

### Task 3: Change evidence-audit timing semantics without weakening final gates

**Files:**
- Modify: `.agents/skills/listing-hardening/scripts/validate_delivery_state.py`
- Modify: `.agents/skills/listing-hardening/scripts/selftest_hardening.py`
- Modify: `.agents/skills/japan-listing-demo/templates/project-state.example.json` only if needed for compatibility examples; final template ownership moves in the release slice.

**Interfaces:**
- `audit_checkpoints.post_6_5_required` means targeted inherited-asset audit was requested; default absent/false => `EVIDENCE_RECONCILIATION_GATE = N/A`.
- `audit_checkpoints.pre_9_required` must be true for a final channel-native delivery state created from Production Freeze.
- `PRE_DEMO_ASSET_GATE` remains strict.

- [ ] **Step 1: Add selective-audit regressions**

Append helpers/tests modeled on the existing v0.2.6 base state:

```python
def test_fresh_project_does_not_require_post_6_5_audit() -> None:
    validator = load_module(NEW_VALIDATOR, "fresh_project_validator")
    state = minimal_valid_state()
    state["audit_checkpoints"] = {"post_6_5_required": False, "pre_9_required": False}
    result = validator.validate_state(state)
    assert result["gates"]["EVIDENCE_RECONCILIATION_GATE"]["status"] == "N/A"


def test_targeted_inherited_asset_audit_is_enforced_when_requested() -> None:
    validator = load_module(NEW_VALIDATOR, "targeted_audit_validator")
    state = minimal_valid_state()
    state["audit_checkpoints"] = {"post_6_5_required": True}
    state.pop("auditor_evidence", None)
    result = validator.validate_state(state)
    assert result["gates"]["EVIDENCE_RECONCILIATION_GATE"]["status"] == "UNVERIFIED"


def test_pre_demo_audit_remains_mandatory_when_required() -> None:
    validator = load_module(NEW_VALIDATOR, "pre_demo_validator")
    state = minimal_valid_state()
    state["audit_checkpoints"] = {"pre_9_required": True}
    state.pop("auditor_evidence", None)
    result = validator.validate_state(state)
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] == "UNVERIFIED"
```

`minimal_valid_state()` may be copied from the existing category-neutral `base_state()` fixture so the test is self-contained.

- [ ] **Step 2: Run and inspect baseline**

The first test should already PASS if current v0.2.6 semantics treat absent/false post-6.5 audit as N/A. The targeted/pre-demo tests must also preserve existing strict behavior. If all three already pass, keep them as characterization tests and continue; do not force an artificial failure.

For the actual TDD RED in this task, add this new behavior test:

```python
def test_creative_user_approval_does_not_satisfy_pre_demo_gate() -> None:
    validator = load_module(NEW_VALIDATOR, "creative_only_validator")
    state = minimal_valid_state()
    state["audit_checkpoints"] = {"pre_9_required": True}
    state["production_freeze"] = {
        "expected_assets": 1,
        "user_approved_assets": ["A01"],
        "approved_output_refs": ["file:a01"],
    }
    state.pop("auditor_evidence", None)
    result = validator.validate_state(state)
    assert result["gates"]["PRE_DEMO_ASSET_GATE"]["status"] == "UNVERIFIED"
```

If current validator ignores `production_freeze` but already returns `UNVERIFIED`, add schema validation in Step 3 so the new Delivery State contract is materially tested.

- [ ] **Step 3: Add Delivery State / Production Freeze schema awareness**

Require `production_freeze` when `pre_9_required` is true and final implementation exists:

```python
def _production_freeze_gate(state: dict[str, Any]) -> dict[str, Any]:
    checkpoints = state.get("audit_checkpoints") or {}
    if checkpoints.get("pre_9_required") is not True:
        return _gate("N/A", "pre-9 hardening not required")
    freeze = state.get("production_freeze")
    if not isinstance(freeze, dict):
        return _gate("FAIL", "production_freeze missing before pre-demo hardening")
    expected = freeze.get("expected_assets")
    approved = freeze.get("user_approved_assets", [])
    if not isinstance(expected, int) or expected < 0:
        return _gate("FAIL", "production_freeze expected_assets must be a non-negative integer")
    if len(approved) != expected:
        return _gate("FAIL", f"production freeze approved {len(approved)} of {expected} expected assets")
    return _gate("PASS", f"production freeze contains {expected} creatively approved assets")
```

Add this gate to `validate_state()` before `PRE_DEMO_ASSET_GATE`. Creative completeness does not replace evidence verification; both gates must pass.

- [ ] **Step 4: Run Hardening and legacy validator tests**

Expected: new Production Freeze regressions pass and all v0.2.5/v0.2.6 tests remain green.

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/listing-hardening/scripts \
        .agents/skills/japan-listing-demo/templates/project-state.example.json
git commit -m "feat: separate creative freeze from evidence verification"
```

---

### Task 4: Migrate hardening-only references and final QA

**Files:**
- Create: `.agents/skills/listing-hardening/references/asset-integrity.md`
- Create: `.agents/skills/listing-hardening/references/executable-gates.md`
- Create: `.agents/skills/listing-hardening/references/frontend-fidelity.md`
- Create: `.agents/skills/listing-hardening/references/final-qa.md`
- Create: `.agents/skills/listing-hardening/templates/delivery-state.example.json`
- Create: `.agents/skills/listing-hardening/evals/hardening.md`
- Modify: `.agents/skills/listing-hardening/scripts/selftest_hardening.py`

**Interfaces:**
- Hardening reference set owns final-only governance terms.
- Planning/Production no longer need these files at runtime after router integration.

- [ ] **Step 1: Add failing reference-ownership tests**

```python
def test_hardening_references_cover_delivery_integrity() -> None:
    expected = {
        "asset-integrity.md": ["sha-256", "transform", "semantic role", "asset-to-slot"],
        "executable-gates.md": ["channel_module_budget_gate", "module_origin_gate", "pre_demo_asset_gate", "delivery_parity_gate"],
        "frontend-fidelity.md": ["primary reference", "frontend_fidelity_gate", "content review demo"],
        "final-qa.md": ["final qa", "consumer mode", "review mode", "delivery parity"],
    }
    for filename, phrases in expected.items():
        text = read(SKILL_DIR / "references" / filename).casefold()
        for phrase in phrases:
            assert phrase in text, (filename, phrase)
```

- [ ] **Step 2: Run and verify RED**

Expected: missing reference files.

- [ ] **Step 3: Migrate/rewrite current hardening rules**

Use the current `references/delivery-integrity.md`, `references/executable-gates.md`, `references/channel-native-demo.md`, QA files, and `listing-evidence-auditor` contract as source material, but keep only Stage 8.5–10 concerns here.

`asset-integrity.md` must include:

```text
Creative USER_APPROVED does not prove physical identity.
Auditor physical evidence overrides candidate file claims.
Wrong implementation must be corrected at the source; do not rewrite the registry to match an accidental demo.
```

`frontend-fidelity.md` must preserve the `Content Review Demo` fallback.

- [ ] **Step 4: Create Delivery State example**

Use category-neutral JSON:

```json
{
  "schema_version": "0.2",
  "production_freeze": {
    "expected_assets": 2,
    "user_approved_assets": ["G1", "A1"],
    "approved_output_refs": ["file:g1", "file:a1"]
  },
  "audit_checkpoints": {"pre_9_required": true},
  "auditor_evidence": {},
  "locked_module_plan": {},
  "asset_slot_contract": [],
  "implementation": {},
  "frontend_fidelity": {},
  "delivery_parity": {}
}
```

The example intentionally contains no fake PASS verdicts.

- [ ] **Step 5: Add anonymized hardening evals**

Include exact scenario names:

```text
Creative approval cannot replace physical verification
Wrong same-name file fails exact identity
Unauthorized crop fails transform authorization
Gallery asset cannot satisfy enhanced-content role by convenience
Incomplete final asset set blocks pre-demo gate
Stage 9 cannot invent an interaction absent from locked plan
Channel-native name requires frontend fidelity
Accidental demo must not rewrite source registry
```

- [ ] **Step 6: Run and verify GREEN**

Expected: all Hardening tests and existing auditor/project-state regressions PASS.

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/listing-hardening/references \
        .agents/skills/listing-hardening/templates \
        .agents/skills/listing-hardening/evals \
        .agents/skills/listing-hardening/scripts/selftest_hardening.py
git commit -m "feat: isolate final delivery hardening rules"
```

---

### Task 5: Add Hardening self-tests to CI and verify compatibility path

**Files:**
- Modify: `.github/workflows/validate-japan-listing-demo.yml`

**Interfaces:**
- CI runs Planning → Production → Hardening → Auditor → legacy Project State compatibility → packaging.

- [ ] **Step 1: Verify Hardening self-test is absent from CI**

```bash
grep -n "selftest_hardening.py" .github/workflows/validate-japan-listing-demo.yml
```

Expected: no match.

- [ ] **Step 2: Add Hardening self-test**

```yaml
      - run: python .agents/skills/listing-hardening/scripts/selftest_hardening.py
```

- [ ] **Step 3: Run all current self-tests and compatibility commands**

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
python .agents/skills/listing-production/scripts/selftest_production.py
python .agents/skills/listing-hardening/scripts/selftest_hardening.py
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
```

Expected: all exit 0. The legacy validator CLI must still work through the compatibility shim.

- [ ] **Step 4: Commit CI coverage**

```bash
git add .github/workflows/validate-japan-listing-demo.yml
git commit -m "test: validate listing hardening skill"
```

---

## Plan Self-Review Checklist

Before implementation review, verify:

- Spec §§17–18, 19.2, 22, 24.4–24.5, 30.3, 31.4, 32, 33.3–33.6 are covered.
- Mandatory full audit remains at Stage 8.5.
- Fresh Stage 6.5 no longer implies full project-wide evidence audit.
- Targeted inherited-asset audit remains strict when explicitly requested.
- Production Freeze completeness and Evidence Verification remain separate gates.
- All v0.2.5/v0.2.6 structural/evidence regressions remain active.
- The old validator path remains compatible until final integration.
- Hardening references contain no strategy/creative-generation responsibilities.
- Public files contain no private project data.
- Verify this plan contains no placeholder markers:

```bash
python - <<'PY'
from pathlib import Path
p = Path('docs/superpowers/plans/2026-08-20-hardening-migration.md')
text = p.read_text(encoding='utf-8').upper()
for marker in ['TO' + 'DO', 'T' + 'BD', 'FIX' + 'ME']:
    assert marker not in text, marker
print('PASS: no placeholder markers')
PY
```
