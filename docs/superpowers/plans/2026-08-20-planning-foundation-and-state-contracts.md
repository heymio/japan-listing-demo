# Planning Foundation and State Contracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `listing-planning` sibling Skill and formal planning-state contracts so Stage 0–7 remains strategically deep while producing a compact, complete Production Handoff instead of carrying the full planning history into later stages.

**Architecture:** This slice adds the Planning plane without switching the public router yet. Existing `japan-listing-demo` v0.2.6 remains the active user-facing runtime during this slice, while the new sibling Skill is independently testable. Planning owns product/offer/claim truth, consumer/VOC/market reasoning, channel planning, Gallery/A+ architecture, module fit/budget, the Creative Strategy Kernel, and the Complete Demo-Required Production Set. Stage 6.5 becomes lightweight source-asset intake by default; only inherited exact assets request targeted early evidence audit.

**Tech Stack:** Markdown Skill contracts, YAML example state files, Python 3.12 standard library validation/self-tests, existing GitHub Actions workflow.

**Spec:** `docs/superpowers/specs/2026-08-20-creative-first-hardening-architecture-design.md`

## Global Constraints

- One public repository: `heymio/japan-listing-demo`.
- Normal public invocation remains `$japan-listing-demo`; do not switch the router in this slice.
- Preserve deep strategy: Product Truth, Offer/Page Boundary, claim readiness, Consumer Strategy, VOC/competitor analysis, Japan localization, channel research, Message Architecture, Gallery/A+ IA, module budget, `CONTENT_COVERAGE`, and `MODULE_FIT_GATE`.
- Stage 6.5 is lightweight Source Asset Intake for fresh projects; project-wide evidence reconciliation is not mandatory here.
- Targeted early `listing-evidence-auditor` use is allowed only for an inherited/reused previously approved exact asset.
- Stage 7 must produce the Complete Demo-Required Production Set; P0 visual proof coverage is not asset-set completeness.
- Planning output must include Project Brief, Creative Strategy Kernel, and Production Handoff.
- Production Handoff must exclude auditor reports, Project State internals, gate definitions, full research corpora, recovery history, rejected-attempt history, and verbose stage-manifest history.
- Public files remain category-neutral and contain no private product/project facts.
- `VERSION` remains `0.2.6` in this slice; release/version changes happen only in the final integration plan.
- Existing v0.2.6 validator/auditor behavior must continue passing throughout this slice.

---

## File Structure

### New Planning Skill

- Create `.agents/skills/listing-planning/SKILL.md` — Stage 0–7 responsibilities, planning workflow, handoff boundary, targeted early-audit rule.
- Create `.agents/skills/listing-planning/agents/openai.yaml` — planning-focused default prompt with no production/hardening machinery.
- Create `.agents/skills/listing-planning/references/source-authority.md` — source precedence, Fact/Conflict/Claim handling.
- Create `.agents/skills/listing-planning/references/market-research.md` — current market/VOC/competitor research method migrated from the existing core.
- Create `.agents/skills/listing-planning/references/localization.md` — planning-time locale rules and Japan evidence boundary.
- Create `.agents/skills/listing-planning/references/channel-planning.md` — channel capability/frontend reference intake and page ownership planning.
- Create `.agents/skills/listing-planning/references/module-fit.md` — Gallery/A+ role separation, module budget, coverage vs module fit.
- Create `.agents/skills/listing-planning/references/planning-qa.md` — planning-plane QA only.
- Create `.agents/skills/listing-planning/templates/project-brief.example.yaml` — stable planning conclusions.
- Create `.agents/skills/listing-planning/templates/creative-strategy.example.yaml` — Creative Strategy Kernel.
- Create `.agents/skills/listing-planning/templates/production-handoff.example.yaml` — complete downstream production contract.
- Create `.agents/skills/listing-planning/scripts/validate_planning_contracts.py` — deterministic structural validator for the three planning artifacts.
- Create `.agents/skills/listing-planning/scripts/selftest_planning.py` — standard-library regressions.
- Create `.agents/skills/listing-planning/evals/planning.md` — human-readable behavior regressions.

### Existing files touched in this slice

- Modify `.github/workflows/validate-japan-listing-demo.yml` — run `selftest_planning.py` before existing v0.2.6 checks.
- Do **not** rewrite `japan-listing-demo/SKILL.md`, `agents/openai.yaml`, package scripts, or release docs yet.

---

### Task 1: Establish the Planning Skill boundary with a RED-first self-test

**Files:**
- Create: `.agents/skills/listing-planning/scripts/selftest_planning.py`
- Create: `.agents/skills/listing-planning/SKILL.md`
- Create: `.agents/skills/listing-planning/agents/openai.yaml`

**Interfaces:**
- Produces Skill name `listing-planning`.
- Owns Stage `0`, `1`, `2`, `3`, `4`, `4.2`, `5`, `5.5`, `6`, `6.5`, `7`.
- Produces the formal outputs `Project Brief`, `Creative Strategy Kernel`, and `Production Handoff` before handing off to Production.

- [ ] **Step 1: Write the failing Skill-boundary tests**

Create `selftest_planning.py` with the following initial tests before `SKILL.md` exists:

```python
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_exists_and_owns_only_planning_plane() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "name: listing-planning" in text
    for phrase in [
        "stage 0", "stage 7", "creative strategy kernel",
        "production handoff", "complete demo-required production set",
    ]:
        assert phrase in text
    for forbidden in [
        "pre_demo_asset_gate", "delivery_parity_gate",
        "provenance_conflict", "exact_recovery_verified",
    ]:
        assert forbidden not in text


def test_stage_6_5_is_lightweight_by_default() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "source asset intake" in text
    assert "targeted early audit" in text
    assert "inherited" in text or "previously approved exact asset" in text
    assert "full project-wide audit is not mandatory" in text


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-planning boundary tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
```

Expected: FAIL with `FileNotFoundError` for `.agents/skills/listing-planning/SKILL.md`.

- [ ] **Step 3: Add the minimal Planning Skill and agent prompt**

Create `SKILL.md` with frontmatter and these explicit responsibility sections:

```markdown
---
name: listing-planning
description: Use when planning Stage 0–7 of a Japan-market listing project: product/offer truth, consumer and market strategy, channel/page architecture, and the complete production handoff.
---

# Listing Planning

## Core question
What should we build, and why?

## Plane boundary
This Skill owns Stage 0–7 only. It does not produce final visual assets, assemble demos, or perform final physical-file hardening.

## Stage 6.5
Use lightweight Source Asset Intake for fresh projects. A full project-wide audit is not mandatory here. Use a targeted early audit only when inheriting or reusing a previously approved exact asset.

## Required handoff
Before leaving Stage 7, produce:
- Project Brief
- Creative Strategy Kernel
- Production Handoff
- Complete Demo-Required Production Set
```

Create `agents/openai.yaml` with a short planning-only default prompt:

```yaml
interface:
  display_name: "Listing Planning"
  short_description: "Deep product, consumer, Japan-market, and channel planning for listing production"
  default_prompt: "Plan Stage 0–7 deeply. Preserve product/offer/claim truth, consumer/VOC/market reasoning, Japan localization, channel capability/frontend evidence, Gallery/A+ architecture, module budget and module fit. End Stage 7 with a Complete Demo-Required Production Set, Creative Strategy Kernel, and Production Handoff. Do not perform final visual production or delivery hardening."
policy:
  allow_implicit_invocation: true
```

- [ ] **Step 4: Run the boundary test and verify GREEN**

Run the same command.

Expected:

```text
PASS: 2 listing-planning boundary tests
```

- [ ] **Step 5: Commit the boundary**

```bash
git add .agents/skills/listing-planning/SKILL.md \
        .agents/skills/listing-planning/agents/openai.yaml \
        .agents/skills/listing-planning/scripts/selftest_planning.py
git commit -m "feat: add listing planning boundary"
```

---

### Task 2: Migrate deep strategy references into the Planning plane

**Files:**
- Create: `.agents/skills/listing-planning/references/source-authority.md`
- Create: `.agents/skills/listing-planning/references/market-research.md`
- Create: `.agents/skills/listing-planning/references/localization.md`
- Create: `.agents/skills/listing-planning/references/channel-planning.md`
- Create: `.agents/skills/listing-planning/references/module-fit.md`
- Create: `.agents/skills/listing-planning/references/planning-qa.md`
- Modify: `.agents/skills/listing-planning/scripts/selftest_planning.py`

**Interfaces:**
- Planning reads these references lazily according to stage.
- `channel-planning.md` consumes current platform/channel evidence and produces a Channel Frontend Reference Pack plus ownership/module capability state.
- `module-fit.md` consumes the message/page plan and produces Gallery/A+ role architecture, `CONTENT_COVERAGE`, `MODULE_FIT_GATE`, and a bounded module plan.

- [ ] **Step 1: Add failing reference-coverage tests**

Append:

```python
def test_deep_strategy_references_exist() -> None:
    required = {
        "source-authority.md": ["product fact", "conflict", "claim"],
        "market-research.md": ["voc", "competitor", "evidence", "inference"],
        "localization.md": ["locale", "ja-jp", "evidence"],
        "channel-planning.md": ["primary reference", "platform capability", "frontend visual"],
        "module-fit.md": ["content_coverage", "module_fit_gate", "message != module"],
        "planning-qa.md": ["complete demo-required production set", "gallery", "enhanced-content"],
    }
    for filename, phrases in required.items():
        text = read(SKILL_DIR / "references" / filename).casefold()
        for phrase in phrases:
            assert phrase in text, (filename, phrase)


def test_planning_references_do_not_own_final_hardening() -> None:
    joined = "\n".join(
        read(path) for path in sorted((SKILL_DIR / "references").glob("*.md"))
    ).casefold()
    for forbidden in ["provenance_conflict", "exact_recovery_verified", "delivery_parity_gate"]:
        assert forbidden not in joined
```

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because the planning reference files do not exist.

- [ ] **Step 3: Create the stage-local planning references**

Migrate the strategy-bearing content from the current `japan-listing-demo/core/market-research.md`, `core/localization.md`, `references/japan-market-evidence.md`, `references/ja-jp-localization.md`, `references/channel-native-demo.md`, and channel profiles, but rewrite ownership so only planning-time concerns remain.

`module-fit.md` must explicitly contain:

```text
CONTENT_COVERAGE != MODULE_FIT_GATE
Message != Module
Gallery-native role != enhanced-content role
Priority differentiator proof != complete production asset set
```

`channel-planning.md` must keep:

```text
Platform Capability evidence != Frontend Visual evidence
Official rules do not substitute for current frontend visual evidence.
```

Do not copy final demo parity, SHA/provenance, or pre-demo audit machinery into these files.

- [ ] **Step 4: Run and verify GREEN**

Expected: all four Planning self-tests PASS.

- [ ] **Step 5: Commit the planning references**

```bash
git add .agents/skills/listing-planning/references \
        .agents/skills/listing-planning/scripts/selftest_planning.py
git commit -m "feat: isolate deep planning references"
```

---

### Task 3: Add formal Project Brief, Creative Strategy Kernel, and Production Handoff contracts

**Files:**
- Create: `.agents/skills/listing-planning/templates/project-brief.example.yaml`
- Create: `.agents/skills/listing-planning/templates/creative-strategy.example.yaml`
- Create: `.agents/skills/listing-planning/templates/production-handoff.example.yaml`
- Create: `.agents/skills/listing-planning/scripts/validate_planning_contracts.py`
- Modify: `.agents/skills/listing-planning/scripts/selftest_planning.py`

**Interfaces:**
- `validate_project_brief(text: str) -> list[str]`
- `validate_creative_strategy(text: str) -> list[str]`
- `validate_production_handoff(text: str) -> list[str]`
- Empty error list means the example contract is structurally valid.

- [ ] **Step 1: Add failing template-validation tests**

Append imports and tests:

```python
from validate_planning_contracts import (
    validate_project_brief,
    validate_creative_strategy,
    validate_production_handoff,
)


def test_planning_templates_validate() -> None:
    templates = SKILL_DIR / "templates"
    cases = [
        ("project-brief.example.yaml", validate_project_brief),
        ("creative-strategy.example.yaml", validate_creative_strategy),
        ("production-handoff.example.yaml", validate_production_handoff),
    ]
    for filename, validator in cases:
        errors = validator(read(templates / filename))
        assert errors == [], (filename, errors)


def test_production_handoff_rejects_control_plane_fields() -> None:
    text = """production_handoff:\n  project:\n  asset_set: []\n  project_state_manifest: {}\n"""
    errors = validate_production_handoff(text)
    assert any("project_state_manifest" in error for error in errors)
```

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because `validate_planning_contracts.py` is missing.

- [ ] **Step 3: Implement the minimal structural validator**

Use only the Python standard library. The validator does not need a full YAML parser; it checks required canonical keys and forbidden control-plane keys in the human-readable example files.

```python
REQUIRED_PROJECT_BRIEF = {
    "project:", "offers:", "product_truth:", "claim_boundaries:",
    "consumer_evidence_sources:", "channel_reference:", "open_business_decisions:",
}

REQUIRED_CREATIVE = {
    "creative_strategy:", "target_user:", "core_tension:", "core_promise:",
    "primary_purchase_reasons:", "shopper_barriers:", "reasons_to_believe:",
    "message_priority:", "japan_implications:", "proof_principles:",
    "visual_direction:", "visual_anti_patterns:",
}

REQUIRED_HANDOFF = {
    "production_handoff:", "project:", "page_plan:", "asset_set:", "source_assets:",
    "product_invariants:", "creative_strategy_ref:", "global_visual_direction:",
    "visual_benchmark_refs:", "prohibited:", "blocked_assets:",
}

FORBIDDEN_HANDOFF = {
    "project_state_manifest", "auditor_evidence", "declared_gate_results",
    "change_impact_map", "delivery_parity_gate", "pre_demo_asset_gate",
}


def _missing(text: str, required: set[str]) -> list[str]:
    folded = text.casefold()
    return [f"missing key: {key}" for key in sorted(required) if key.casefold() not in folded]


def validate_project_brief(text: str) -> list[str]:
    return _missing(text, REQUIRED_PROJECT_BRIEF)


def validate_creative_strategy(text: str) -> list[str]:
    return _missing(text, REQUIRED_CREATIVE)


def validate_production_handoff(text: str) -> list[str]:
    errors = _missing(text, REQUIRED_HANDOFF)
    folded = text.casefold()
    errors.extend(f"forbidden handoff field: {key}" for key in sorted(FORBIDDEN_HANDOFF) if key in folded)
    return errors
```

Add a CLI that validates the three example files and exits 0/1.

- [ ] **Step 4: Create concrete example templates**

Use category-neutral sample values. `production-handoff.example.yaml` must demonstrate a complete set with separate Gallery and enhanced-content roles, for example:

```yaml
production_handoff:
  project:
    market: JP
    channel: amazon-jp
    locale: ja-JP
    product: Example Product
  page_plan:
    gallery: [AMZ-M0, AMZ-G1, AMZ-G2]
    enhanced_content: [AMZ-A1, AMZ-A2]
    other_required_regions: []
  asset_set:
    - asset_id: AMZ-M0
      role: main-image
    - asset_id: AMZ-G1
      role: gallery-native
    - asset_id: AMZ-A1
      role: enhanced-content
  source_assets: [SRC-P01]
  product_invariants: [preserve-product-geometry]
  creative_strategy_ref: creative-strategy.yaml
  global_visual_direction: [product-first, commercial-ecommerce]
  visual_benchmark_refs: [BENCH-01]
  prohibited: [unsupported-claims, invented-product-geometry]
  blocked_assets: []
```

- [ ] **Step 5: Run and verify GREEN**

Run:

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
python .agents/skills/listing-planning/scripts/validate_planning_contracts.py
```

Expected: both exit 0.

- [ ] **Step 6: Commit the planning state contracts**

```bash
git add .agents/skills/listing-planning/templates \
        .agents/skills/listing-planning/scripts
git commit -m "feat: add planning state and handoff contracts"
```

---

### Task 4: Enforce complete production-set accounting and targeted early-audit semantics

**Files:**
- Modify: `.agents/skills/listing-planning/SKILL.md`
- Modify: `.agents/skills/listing-planning/references/planning-qa.md`
- Modify: `.agents/skills/listing-planning/references/module-fit.md`
- Modify: `.agents/skills/listing-planning/scripts/selftest_planning.py`
- Create: `.agents/skills/listing-planning/evals/planning.md`

**Interfaces:**
- Stage 7 output has explicit `asset_set` and `blocked_assets`.
- `P0 proof covered` cannot imply `production complete`.
- Gallery and enhanced-content assets remain separate required role classes unless explicit reuse is planned.
- `targeted early audit` is triggered only by inherited exact-asset reuse.

- [ ] **Step 1: Add failing behavioral regressions**

Append:

```python
def test_priority_proof_is_not_complete_asset_set() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "priority proof coverage" in text
    assert "does not" in text and "complete" in text


def test_gallery_and_enhanced_content_are_separate_production_roles() -> None:
    text = read(SKILL_DIR / "references" / "module-fit.md").casefold()
    assert "gallery-native" in text
    assert "enhanced-content" in text
    assert "separate" in text


def test_fresh_project_does_not_require_full_stage_6_5_audit() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    assert "full project-wide audit is not mandatory" in text
    assert "targeted early audit" in text
```

- [ ] **Step 2: Run and verify RED**

Expected: at least `priority proof coverage` behavior is absent from the minimal Skill text.

- [ ] **Step 3: Implement the planning completion rules**

Add explicit Stage 7 completion language:

```text
Stage 7 is complete only when every Demo-required final role has an Asset ID or an explicit BLOCKED entry in Production Handoff. P0/Differentiator visual coverage is a strategy/proof check, not a substitute for complete production-set accounting.
```

Add the targeted-audit decision table to `planning-qa.md`:

| Situation | Stage 6.5 behavior |
|---|---|
| Fresh source render/UI/brand asset | inventory only |
| New final Gallery/A+ asset not produced yet | plan its Asset ID; do not audit nonexistent output |
| Previously approved exact asset requested for reuse | targeted early audit |
| User supplied visual only as benchmark | register benchmark role; no reuse approval |

Add anonymized eval scenarios covering all four rows.

- [ ] **Step 4: Run and verify GREEN**

Expected: all Planning tests PASS.

- [ ] **Step 5: Commit the completion semantics**

```bash
git add .agents/skills/listing-planning
git commit -m "feat: require complete production handoff"
```

---

### Task 5: Add Planning self-test to CI without changing public routing

**Files:**
- Modify: `.github/workflows/validate-japan-listing-demo.yml`

**Interfaces:**
- CI runs Planning self-tests before current v0.2.6 validator/package steps.
- Existing auditor and project-state tests remain unchanged.

- [ ] **Step 1: Verify the new Skill is currently not covered by CI**

Run or inspect:

```bash
grep -n "selftest_planning.py" .github/workflows/validate-japan-listing-demo.yml
```

Expected: no match.

- [ ] **Step 2: Add the Planning self-test step**

Insert after Python setup:

```yaml
      - run: python .agents/skills/listing-planning/scripts/selftest_planning.py
```

Do not yet add Planning to packaging requirements; that is owned by the final integration plan.

- [ ] **Step 3: Run the full local validation sequence**

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
python .agents/skills/listing-planning/scripts/validate_planning_contracts.py
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
```

Expected: all commands exit 0; v0.2.6 packaging still works exactly as before because the public router has not been switched yet.

- [ ] **Step 4: Commit CI coverage**

```bash
git add .github/workflows/validate-japan-listing-demo.yml
git commit -m "test: validate listing planning skill"
```

---

## Plan Self-Review Checklist

Before declaring this slice ready for implementation review, verify:

- Every Planning responsibility in Spec §§7–9, 19, 21, 24.2, 25, 30.1, 31.2 is mapped to a task above.
- No Production or Hardening runtime behavior has been moved into `listing-planning`.
- The Planning templates contain no private product facts.
- Stage 6.5 default is lightweight and targeted audit is explicit.
- Complete production-set accounting is explicit and mechanically represented in Production Handoff.
- Existing v0.2.6 CI/package behavior remains green after adding the sibling Planning Skill.
- Search this plan for placeholder markers and remove any occurrence before execution:

```bash
python - <<'PY'
from pathlib import Path
p = Path('docs/superpowers/plans/2026-08-20-planning-foundation-and-state-contracts.md')
text = p.read_text(encoding='utf-8').upper()
for marker in ['TO' + 'DO', 'T' + 'BD', 'FIX' + 'ME']:
    assert marker not in text, marker
print('PASS: no placeholder markers')
PY
```
