# Router, Team Distribution, and v0.3.0 Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate Planning, Production, Hardening, and Evidence Auditor behind a thin `$japan-listing-demo` router, remove always-on control-plane duplication, preserve one-install/one-invocation team usage, and publish the architecture redesign as v0.3.0 after full regressions pass.

**Architecture:** The main `japan-listing-demo` Skill becomes a stage router with concise checkpoint/transition/retry/exception rules. Repository/Codex distribution contains five sibling Skills (`japan-listing-demo`, `listing-planning`, `listing-production`, `listing-hardening`, `listing-evidence-auditor`). The compatibility single-Skill archive remains one install by packaging the four internal stage/audit Skills under `japan-listing-demo/internal-skills/`; it explicitly retains the single-context semantic-audit limitation. Legacy monolithic runtime files are removed from normal loading after their responsibilities are proven present in stage-local Skills. A team-facing Custom GPT remains optional documentation only, not an execution dependency.

**Tech Stack:** Markdown Skill/router contracts, Python 3.12 standard-library architecture/package validation, GitHub Actions, ZIP packaging, existing Skill self-tests and evidence-auditor/validator regressions.

**Spec:** `docs/superpowers/specs/2026-08-20-creative-first-hardening-architecture-design.md`

## Global Constraints

- This plan is executed only after the Planning, Production, and Hardening implementation plans are green.
- Normal user-facing invocation remains exactly `$japan-listing-demo`.
- Team users must not manually invoke internal Planning/Production/Hardening/Auditor Skills in the Golden Path.
- One public repository remains `heymio/japan-listing-demo`.
- One recommended repository/Codex bundle contains all five sibling Skills.
- One compatibility archive remains available for single-Skill installation; stage Skills are packaged internally, not installed separately.
- Loading a Skill is not treated as proof of isolated model context. Production isolation comes from formal Context Projection; semantic auditor independence keeps its existing human/independent-context limitation.
- Main router instructions must be materially shorter than v0.2.6 and must not restate SHA/provenance/pre-demo/parity machinery.
- Default checkpoint output is `Done / Open / Next`; full Stage Completion Manifest appears only for `PARTIAL`, `BLOCKED`, or explicit user audit request.
- Change Impact is exception-only. Recovery Mode is not part of normal runtime.
- Deep strategy remains in `listing-planning`; visual quality guidance remains in `listing-production`; hard verification remains in `listing-hardening`/auditor.
- Public regressions/examples remain category-neutral with no private product facts.
- Target release version is **0.3.0** because this changes the runtime architecture and distribution contract rather than adding a patch-level rule.
- Final PR remains Draft until user explicitly confirms merge.

---

## File Structure

### Thin Router

- Rewrite `.agents/skills/japan-listing-demo/SKILL.md`.
- Rewrite `.agents/skills/japan-listing-demo/agents/openai.yaml`.
- Create `.agents/skills/japan-listing-demo/references/routing.md`.
- Create `.agents/skills/japan-listing-demo/references/exception-routing.md`.
- Create `.agents/skills/japan-listing-demo/scripts/selftest_router.py`.
- Create `.agents/skills/japan-listing-demo/evals/creative-first-hardening.md`.
- Create `.agents/skills/japan-listing-demo/evals/team-golden-path.md`.

### Runtime simplification / channel ownership

- Move planning-owned channel profiles from `.agents/skills/japan-listing-demo/profiles/channels/` to `.agents/skills/listing-planning/profiles/channels/`, rewriting them to planning concerns only.
- Remove or replace monolithic runtime references from the main Skill after ownership is migrated:
  - `.agents/skills/japan-listing-demo/core/workflow.md`
  - `.agents/skills/japan-listing-demo/core/contracts.md`
  - `.agents/skills/japan-listing-demo/references/delivery-integrity.md`
  - `.agents/skills/japan-listing-demo/references/executable-gates.md`
  - `.agents/skills/japan-listing-demo/references/channel-native-demo.md`
  - `.agents/skills/japan-listing-demo/references/qa.md`
- Preserve generic source files only when still referenced by a stage-local Skill; otherwise archive documentation belongs outside the runtime Skill tree or relies on Git history.
- Keep `.agents/skills/japan-listing-demo/data/channel-policy-limits.json` as shared packaged machine policy for this release unless a tested path migration is simpler.

### Packaging / validation / docs

- Modify `.agents/skills/japan-listing-demo/scripts/validate_overlay.py`.
- Modify `.agents/skills/japan-listing-demo/scripts/package_skill.py`.
- Modify `scripts/package_codex_bundle.py`.
- Modify `.github/workflows/validate-japan-listing-demo.yml`.
- Modify `README.md`, `docs/install.md`, `CHANGELOG.md`, `.agents/skills/japan-listing-demo/core/manifest.yaml`, `VERSION`.
- Create `docs/team-gpt-setup.md` — optional thin GPT UX guide.

---

### Task 1: Write router regressions that fail against the v0.2.6 monolith

**Files:**
- Create: `.agents/skills/japan-listing-demo/scripts/selftest_router.py`
- Create: `.agents/skills/japan-listing-demo/evals/creative-first-hardening.md`
- Create: `.agents/skills/japan-listing-demo/evals/team-golden-path.md`

**Interfaces:**
- Router maps Stage 0–7 → `listing-planning`, Stage 7.5–8 → `listing-production`, Stage 8.5–10 → `listing-hardening`.
- Main router contains only routing/checkpoint/transition/retry/context-firewall/exception semantics.

- [ ] **Step 1: Create failing router-slimness tests**

```python
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_router_is_materially_smaller_than_v026_budget() -> None:
    text = read(SKILL_DIR / "SKILL.md")
    assert len(text) <= 8000, len(text)


def test_default_prompt_is_thin() -> None:
    text = read(SKILL_DIR / "agents" / "openai.yaml")
    assert len(text) <= 2200, len(text)
    folded = text.casefold()
    for forbidden in [
        "sha-256", "provenance_conflict", "pre_demo_asset_gate",
        "delivery_parity_gate", "declared_gate_results",
    ]:
        assert forbidden not in folded


def test_router_maps_stage_planes() -> None:
    text = read(SKILL_DIR / "references" / "routing.md").casefold()
    for phrase in [
        "stage 0–7", "listing-planning",
        "stage 7.5–8", "listing-production",
        "stage 8.5–10", "listing-hardening",
    ]:
        assert phrase in text


def test_router_preserves_checkpoint_transition_and_retry() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    for phrase in ["major stage checkpoint", "transition command", "retry budget", "context firewall"]:
        assert phrase in text


def test_default_checkpoint_is_concise() -> None:
    text = read(SKILL_DIR / "references" / "routing.md")
    assert "Done:" in text and "Open:" in text and "Next:" in text
    assert "full Stage Completion Manifest" in text
    assert "PARTIAL" in text and "BLOCKED" in text


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} thin-router tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run and verify RED against current main Skill**

```bash
python .agents/skills/japan-listing-demo/scripts/selftest_router.py
```

Expected: FAIL at minimum on router size/default-prompt size and missing `references/routing.md`.

- [ ] **Step 3: Add category-neutral architecture evals before implementation**

`creative-first-hardening.md` must include exact scenarios:

```text
Deep strategy remains in Planning
Fresh source asset intake does not trigger full audit
Complete production set precedes Stage 8
Production receives one-job Asset Packet
Control-plane terms do not enter production prompt
Creative approval is separate from evidence verification
Mandatory full audit runs at Stage 8.5
Wrong final asset is rejected before Demo Assembly
```

`team-golden-path.md` must describe one non-expert path from source upload → planning review → page plan → visual direction → visual review → demo review without manual internal-Skill invocation.

- [ ] **Step 4: Commit RED tests/evals**

```bash
git add .agents/skills/japan-listing-demo/scripts/selftest_router.py \
        .agents/skills/japan-listing-demo/evals/creative-first-hardening.md \
        .agents/skills/japan-listing-demo/evals/team-golden-path.md
git commit -m "test: define creative-first router behavior"
```

---

### Task 2: Replace the monolithic main Skill with the thin router

**Files:**
- Modify: `.agents/skills/japan-listing-demo/SKILL.md`
- Modify: `.agents/skills/japan-listing-demo/agents/openai.yaml`
- Create: `.agents/skills/japan-listing-demo/references/routing.md`
- Create: `.agents/skills/japan-listing-demo/references/exception-routing.md`

**Interfaces:**
- `routing.md` defines current-stage → active-Skill resolution and formal state/handoff names.
- `exception-routing.md` defines downstream block → targeted upstream return.

- [ ] **Step 1: Write the minimal router content**

`SKILL.md` should be approximately this shape, expanding only where needed for exact behavior:

```markdown
---
name: japan-listing-demo
description: Use when running a Japan-market listing project from source intake through strategy, visual production, hardening, and channel-native demo review.
---

# Japan Listing Demo Router

## Purpose
One project, one Chat, one normal invocation. Route the current stage to the smallest stage-specific Skill.

## Stage routing
- Stage 0–7 → `listing-planning`
- Stage 7.5–8 → `listing-production`
- Stage 8.5–10 → `listing-hardening`
- `listing-hardening` delegates exact-file evidence work to `listing-evidence-auditor`.

## Major Stage Checkpoint
Checkpointed by default. Normal checkpoint display is `Done / Open / Next`. Show the full Stage Completion Manifest only for `PARTIAL`, `BLOCKED`, or explicit audit request.

## Transition Command
`继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalents leave the current stage unless the user explicitly asks to keep revising it.

## Retry Budget
Same artifact + same problem: at most two autonomous attempts without new input/evidence.

## Context Firewall
Pass only formal handoff/state objects required by the next plane. Production receives only the Creative Strategy Kernel, Production Handoff, current Asset Packet, referenced source assets, and approved benchmarks/patterns. Do not inject workflow-control narration into production prompts.

## Exception routing
A downstream Skill that lacks an upstream fact returns `BLOCKED` and `return_to`; the Router reopens only the targeted upstream decision.
```

- [ ] **Step 2: Rewrite `agents/openai.yaml` to router-only behavior**

Use:

```yaml
interface:
  display_name: "Japan Listing Demo"
  short_description: "One-entry Japan listing strategy, production, and verified demo workflow"
  default_prompt: "Use japan-listing-demo as the thin router. Route Stage 0–7 to listing-planning, Stage 7.5–8 to listing-production, and Stage 8.5–10 to listing-hardening. Use Major Stage Checkpoints by default, honor Transition Commands immediately, keep the same-artifact Retry Budget at two autonomous attempts, and pass only formal stage handoff objects. Keep control-plane instructions out of production prompts. Route missing upstream decisions back instead of improvising them."
policy:
  allow_implicit_invocation: true
```

- [ ] **Step 3: Create `routing.md` and `exception-routing.md`**

`routing.md` must define:

```text
Stage 0–7      listing-planning
Stage 7.5–8    listing-production
Stage 8.5–10   listing-hardening
```

and the five state objects:

```text
Project Brief
Creative Strategy Kernel
Production Handoff
Asset Ledger / Production Freeze
Delivery State
```

`exception-routing.md` must include the structured block contract:

```yaml
status: BLOCKED
missing_field: <specific field name>
return_to: planning | production
asset_id: <affected asset when applicable>
```

The Router must not reopen unrelated work.

- [ ] **Step 4: Run router tests and verify GREEN**

```bash
python .agents/skills/japan-listing-demo/scripts/selftest_router.py
```

Expected: all thin-router tests PASS.

- [ ] **Step 5: Commit the router**

```bash
git add .agents/skills/japan-listing-demo/SKILL.md \
        .agents/skills/japan-listing-demo/agents/openai.yaml \
        .agents/skills/japan-listing-demo/references/routing.md \
        .agents/skills/japan-listing-demo/references/exception-routing.md
git commit -m "refactor: replace monolithic skill with thin router"
```

---

### Task 3: Move channel profiles and remove monolithic runtime ownership

**Files:**
- Create: `.agents/skills/listing-planning/profiles/channels/amazon-jp.md`
- Create: `.agents/skills/listing-planning/profiles/channels/rakuten.md`
- Create: `.agents/skills/listing-planning/profiles/channels/yahoo-shopping.md`
- Create: `.agents/skills/listing-planning/profiles/channels/dtc.md`
- Create: `.agents/skills/listing-planning/profiles/channels/retailer-pdp.md`
- Modify: `.agents/skills/listing-planning/SKILL.md`
- Remove from runtime ownership after coverage is verified:
  - `.agents/skills/japan-listing-demo/profiles/channels/*.md`
  - `.agents/skills/japan-listing-demo/core/workflow.md`
  - `.agents/skills/japan-listing-demo/core/contracts.md`
  - `.agents/skills/japan-listing-demo/references/delivery-integrity.md`
  - `.agents/skills/japan-listing-demo/references/executable-gates.md`
  - `.agents/skills/japan-listing-demo/references/channel-native-demo.md`
  - `.agents/skills/japan-listing-demo/references/qa.md`
- Modify stage-local self-tests to prove coverage before deletion.

**Interfaces:**
- Planning channel profiles contain capability/reference/module planning only.
- Hardening generic references own final implementation/fidelity/parity.
- Main router no longer loads legacy monolithic files.

- [ ] **Step 1: Add planning profile coverage tests before moving files**

Add to `listing-planning/scripts/selftest_planning.py`:

```python
def test_channel_profiles_are_owned_by_planning() -> None:
    channels = ["amazon-jp.md", "rakuten.md", "yahoo-shopping.md", "dtc.md", "retailer-pdp.md"]
    root = SKILL_DIR / "profiles" / "channels"
    for name in channels:
        text = read(root / name).casefold()
        assert "use when" in text
        assert "platform" in text or "channel" in text
        assert "content" in text or "module" in text


def test_amazon_planning_profile_keeps_module_budget_and_role_separation() -> None:
    text = read(SKILL_DIR / "profiles" / "channels" / "amazon-jp.md").casefold()
    for phrase in ["basic a+", "premium a+", "message != module", "gallery", "enhanced-content", "module_fit_gate"]:
        assert phrase in text
    for forbidden in ["exact_recovery_verified", "delivery_parity_gate", "provenance_conflict"]:
        assert forbidden not in text
```

Run now. Expected: RED because planning-owned profiles do not exist.

- [ ] **Step 2: Rewrite the five profiles into Planning ownership**

Start from the current channel profiles but strip hardening-only sections. Preserve current channel capability/reference/module planning information and current Amazon packaged limits (Basic 5, Premium 7) as planning constraints.

For Amazon, keep:

```text
Platform Capability != Frontend Visual evidence
Message != Module
CONTENT_COVERAGE != MODULE_FIT_GATE
Gallery-native != enhanced-content role
Basic A+ max 5 / Premium A+ max 7 under packaged current policy
```

Move final file identity/parity/fidelity enforcement to Hardening references instead of duplicating it here.

- [ ] **Step 3: Run all stage-local coverage tests before deleting legacy files**

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
python .agents/skills/listing-production/scripts/selftest_production.py
python .agents/skills/listing-hardening/scripts/selftest_hardening.py
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
```

Expected: all PASS.

- [ ] **Step 4: Remove the duplicated runtime files**

Delete the old main-Skill channel profiles and monolithic workflow/contracts/delivery/executable/frontend/QA references listed above.

Before deletion, search all active Skill files for references to those paths:

```bash
grep -R "core/workflow.md\|core/contracts.md\|references/delivery-integrity.md\|references/executable-gates.md\|references/channel-native-demo.md\|references/qa.md\|profiles/channels/" .agents/skills --exclude-dir='__pycache__'
```

Expected after updating active references: no live runtime reference points to deleted main-Skill paths. References inside historical docs/evals may be updated or explicitly labeled legacy.

- [ ] **Step 5: Re-run stage-local tests**

Expected: all tests from Step 3 still PASS after deletion.

- [ ] **Step 6: Commit the ownership cleanup**

```bash
git add -A .agents/skills
git commit -m "refactor: remove monolithic runtime ownership"
```

---

### Task 4: Update distribution validators to require the five-Skill architecture — RED first

**Files:**
- Modify: `.agents/skills/japan-listing-demo/scripts/validate_overlay.py`
- Modify: `.agents/skills/japan-listing-demo/scripts/package_skill.py`
- Modify: `scripts/package_codex_bundle.py`

**Interfaces:**
- Repository validator requires all five Skills and all four stage self-tests.
- Codex bundle contains five sibling Skill roots.
- Compatibility single-Skill archive contains router at root and stage/audit Skills under `japan-listing-demo/internal-skills/`.

- [ ] **Step 1: Change validation expectations before package implementation**

Update `validate_overlay.py` required architecture to include:

```python
REQUIRED_SKILLS = [
    "japan-listing-demo",
    "listing-planning",
    "listing-production",
    "listing-hardening",
    "listing-evidence-auditor",
]
```

Require these scripts to run successfully:

```text
listing-planning/scripts/selftest_planning.py
listing-production/scripts/selftest_production.py
listing-hardening/scripts/selftest_hardening.py
listing-evidence-auditor/scripts/selftest_auditor.py
japan-listing-demo/scripts/selftest_router.py
japan-listing-demo/scripts/selftest_project_state_validator.py
```

Require `VERSION == 0.3.0` and require router default prompt to stay under the chosen size budget.

- [ ] **Step 2: Run validator and verify RED**

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
```

Expected: FAIL because `VERSION` is still `0.2.6` and package/distribution docs have not been migrated.

- [ ] **Step 3: Update Codex bundle packager to five sibling Skills**

In `scripts/package_codex_bundle.py`:

```python
SKILL_NAMES = [
    "japan-listing-demo",
    "listing-planning",
    "listing-production",
    "listing-hardening",
    "listing-evidence-auditor",
]
```

Archive each as `.agents/skills/<name>/...` and validate that all five `SKILL.md` files and required stage scripts exist.

Expected output remains:

```text
dist/japan-listing-demo-codex-bundle.zip
```

- [ ] **Step 4: Update compatibility `package_skill.py` to one-install nested internals**

The compatibility ZIP should contain:

```text
japan-listing-demo/SKILL.md
japan-listing-demo/agents/openai.yaml
japan-listing-demo/references/routing.md
japan-listing-demo/references/exception-routing.md
japan-listing-demo/data/channel-policy-limits.json
japan-listing-demo/scripts/selftest_router.py
japan-listing-demo/internal-skills/listing-planning/...
japan-listing-demo/internal-skills/listing-production/...
japan-listing-demo/internal-skills/listing-hardening/...
japan-listing-demo/internal-skills/listing-evidence-auditor/...
japan-listing-demo/SINGLE_CONTEXT_LIMITATION.txt
```

Implement packaging by copying sibling source files into the ZIP at build time; do not duplicate those source trees in Git.

The limitation text must state:

```text
The compatibility archive is one model context. Internal stage separation and Context Projection still apply, but loading the embedded evidence auditor does not create independent semantic review. Deterministic file checks may run; unresolved semantic evidence remains UNVERIFIED / HUMAN_REVIEW_REQUIRED unless resolved by human or genuinely independent review.
```

- [ ] **Step 5: Run package commands; expect version/doc validation still RED until Task 6**

```bash
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
python -m zipfile -l dist/japan-listing-demo.skill.zip
python -m zipfile -l dist/japan-listing-demo-codex-bundle.zip
```

Expected: both ZIPs build and show the required internal/sibling Skill layouts. `validate_overlay.py` may still fail on release docs/version until Task 6.

- [ ] **Step 6: Commit package architecture**

```bash
git add .agents/skills/japan-listing-demo/scripts \
        scripts/package_codex_bundle.py
git commit -m "build: package five-skill creative-first architecture"
```

---

### Task 5: Update CI to test both distribution modes and the Team Golden Path

**Files:**
- Modify: `.github/workflows/validate-japan-listing-demo.yml`

**Interfaces:**
- CI runs all stage/router/auditor tests and inspects both ZIPs.
- One artifact upload contains both archives.

- [ ] **Step 1: Add explicit full test order**

The workflow should contain:

```yaml
      - run: python .agents/skills/listing-planning/scripts/selftest_planning.py
      - run: python .agents/skills/listing-production/scripts/selftest_production.py
      - run: python .agents/skills/listing-hardening/scripts/selftest_hardening.py
      - run: python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
      - run: python .agents/skills/japan-listing-demo/scripts/selftest_router.py
      - run: python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
      - run: python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
      - run: python .agents/skills/japan-listing-demo/scripts/package_skill.py
      - run: python scripts/package_codex_bundle.py
      - run: python -m zipfile -l dist/japan-listing-demo.skill.zip
      - run: python -m zipfile -l dist/japan-listing-demo-codex-bundle.zip
```

- [ ] **Step 2: Upload both artifacts together**

```yaml
      - uses: actions/upload-artifact@v4
        with:
          name: japan-listing-demo-artifacts
          path: |
            dist/japan-listing-demo.skill.zip
            dist/japan-listing-demo-codex-bundle.zip
```

- [ ] **Step 3: Run local equivalent**

Run the exact commands in Step 1 locally. At this point `validate_overlay.py` is expected to remain RED only on unreleased version/docs if Task 6 has not yet run; all behavioral tests/package builders should be green.

- [ ] **Step 4: Commit CI integration**

```bash
git add .github/workflows/validate-japan-listing-demo.yml
git commit -m "ci: validate creative-first five-skill distribution"
```

---

### Task 6: Publish team-facing docs, optional GPT guide, manifest, changelog, and v0.3.0 version

**Files:**
- Modify: `README.md`
- Modify: `docs/install.md`
- Create: `docs/team-gpt-setup.md`
- Modify: `CHANGELOG.md`
- Modify: `.agents/skills/japan-listing-demo/core/manifest.yaml`
- Modify: `VERSION`
- Modify: `docs/superpowers/specs/2026-08-20-creative-first-hardening-architecture-design.md` status line from `Design for review` to `Approved for implementation` if not already updated.

**Interfaces:**
- Public docs present one user-facing entry and the Team Golden Path.
- Internal stage Skills are explained as implementation architecture, not user actions.
- Custom GPT is optional and thin; GitHub Skills remain source of truth.

- [ ] **Step 1: Update README around the Team Golden Path**

Lead with:

```text
One repository
One normal invocation: $japan-listing-demo
One project can run in one Chat
```

Explain the user-visible path only:

```text
Upload source material
→ review Product / Offer / Claim baseline
→ review Consumer / Market Strategy
→ review channel page plan
→ review Creative Strategy / complete asset set
→ review generated visuals
→ review verified demo
```

Then briefly explain internal planes:

```text
Planning → Production → Hardening
```

Do not put SHA/provenance instructions in the Quick Start.

- [ ] **Step 2: Update installation docs for both distribution modes**

Recommended repository/Codex path: one five-Skill bundle, one invocation.

Compatibility path: one `japan-listing-demo.skill.zip` containing embedded internal stage Skills. Explain the semantic-auditor single-context limitation without making users manually invoke internal Skills.

- [ ] **Step 3: Add optional Custom GPT setup guide**

`docs/team-gpt-setup.md` must state:

```text
GPT = optional UX shell
Skills = versioned execution architecture
Auditor/scripts = hard verification
```

Recommended GPT instructions should be deliberately thin, for example:

```text
Use the installed japan-listing-demo workflow as the execution source of truth. Help team members create or resume a Japan listing project, upload product/GTM/visual inputs, and follow the workflow's Major Stage Checkpoints. Do not duplicate the detailed workflow rules in GPT Instructions.
```

Document recommended capabilities (web/image generation as applicable) but do not make the GPT required for repository/Codex usage.

- [ ] **Step 4: Add `0.3.0` changelog entry**

The entry must explicitly describe:

- thin router;
- deep `listing-planning`;
- `listing-production` + Context Projection/Asset Packets;
- `listing-hardening` + mandatory Stage 8.5 audit;
- targeted-only early audit;
- Creative Strategy Kernel;
- Asset Ledger / Production Freeze;
- concise checkpoints;
- five-Skill bundle + one-install compatibility archive;
- evidence auditor protections retained.

- [ ] **Step 5: Update core manifest and VERSION**

Set:

```text
VERSION = 0.3.0
```

Manifest must record a `creative-first-hardening-v0.3.0` distribution patch and list the three new stage Skills plus retained auditor.

- [ ] **Step 6: Run full release validation and verify GREEN**

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
python -m zipfile -l dist/japan-listing-demo.skill.zip
python -m zipfile -l dist/japan-listing-demo-codex-bundle.zip
```

Expected: every command exits 0, `validate_overlay.py` reports v0.3.0 and all five Skills, and both package inspections show their required layouts.

- [ ] **Step 7: Commit release docs/version**

```bash
git add README.md docs/install.md docs/team-gpt-setup.md CHANGELOG.md VERSION \
        .agents/skills/japan-listing-demo/core/manifest.yaml \
        docs/superpowers/specs/2026-08-20-creative-first-hardening-architecture-design.md
git commit -m "docs: prepare creative-first hardening v0.3.0"
```

---

### Task 7: Final architecture verification and Draft PR

**Files:**
- No new runtime files expected; only fix defects found by verification.

**Interfaces:**
- PR targets `main` and remains Draft.
- No merge action occurs without explicit user confirmation.

- [ ] **Step 1: Compare branch against `main`**

```bash
git diff --stat origin/main...HEAD
git diff --name-status origin/main...HEAD
```

Confirm changes are limited to the public workflow architecture, tests, packaging, and docs.

- [ ] **Step 2: Run private-product leakage scan over changed public runtime/test files**

Use the existing repository leakage validator plus an explicit changed-file scan. At minimum reject company/private-project names or product-specific facts that are not intended public generic examples.

- [ ] **Step 3: Run the complete release verification again from a clean checkout/worktree**

Run the Task 6 Step 6 command sequence in full. Do not rely on previous runs.

Expected: 0 failures.

- [ ] **Step 4: Push branch and wait for GitHub Actions**

Confirm the PR-triggered workflow runs all expected stages and both archives are uploaded.

- [ ] **Step 5: Create or update a Draft PR**

Suggested title:

```text
Publish v0.3.0 creative-first hardening architecture
```

PR body must summarize:

```text
Why: control-plane duplication contaminated production.
What: thin router + deep planning + focused production + final hardening.
Preserved: strategy depth, channel capability, module fit/budget, evidence auditor, exact-file and parity safeguards.
Changed: full audit timing, concise checkpoints, production context projection, five-skill packaging.
Evidence: RED-first tests, final local verification, GitHub Actions run IDs/artifacts.
```

Keep PR **Draft**.

- [ ] **Step 6: Stop for explicit merge confirmation**

Do not mark ready/merge unless the user explicitly confirms after reviewing the final verification and PR.

---

## Plan Self-Review Checklist

Before execution handoff, verify:

- Spec §§5–6, 20–29, 31.1, 31.5, 32–34 are covered.
- User-facing entry remains one invocation.
- Repository/Codex bundle contains five sibling Skills; compatibility archive remains one install through build-time embedding rather than source duplication.
- Thin router does not restate hardening internals.
- Team Quick Start does not require internal Skill/gate knowledge.
- Channel planning functionality remains after removing main-Skill channel profiles.
- Legacy monolithic runtime files are removed only after stage-local coverage is tested.
- Optional GPT remains a UX shell, not source of truth.
- v0.3.0 is not merged automatically.
- Public tests/examples contain no private project facts.
- Verify this plan contains no placeholder markers:

```bash
python - <<'PY'
from pathlib import Path
p = Path('docs/superpowers/plans/2026-08-20-router-team-distribution-and-release.md')
text = p.read_text(encoding='utf-8').upper()
for marker in ['TO' + 'DO', 'T' + 'BD', 'FIX' + 'ME']:
    assert marker not in text, marker
print('PASS: no placeholder markers')
PY
```
