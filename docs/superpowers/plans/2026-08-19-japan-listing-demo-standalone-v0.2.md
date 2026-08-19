# Japan Listing Demo Standalone v0.2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `japan-listing-demo` from a runtime overlay into a standalone public Skill that Japan-team users install and invoke once.

**Architecture:** Keep `heymio/gtm-listing-demo` as the upstream maintenance source, but bundle a version-locked, curated core snapshot inside the `japan-listing-demo` Skill package. Runtime instructions, validation, packaging, README, and installation docs must not require a second Skill. Private brand overlays remain optional and external.

**Tech Stack:** Markdown Skill files, Python 3.12 standard-library validators and packager, GitHub Actions.

**Spec:** User-approved standalone distribution design in the current project conversation.

## Global Constraints

- Public team-facing repositories and projects must be independently usable.
- Japan-team users install only `japan-listing-demo`.
- `japan-listing-demo` may record upstream provenance but must have no runtime dependency on another Skill.
- Product-category conclusions, fixed Japan personas, private brand facts, prices, Figma links, and unreleased assets remain excluded.
- Core snapshot provenance is locked to `heymio/gtm-listing-demo` v0.2.0, commit `b882526f5a683235d30f562006cf1984a9f0d9f9`.
- Essential workflow, contracts, evidence, QA, category template, and core evals must be bundled in the Skill ZIP.

---

### Task 1: Add failing standalone-distribution contract

**Files:**
- Modify: `.agents/skills/japan-listing-demo/scripts/validate_overlay.py`
- Modify: `.agents/skills/japan-listing-demo/evals/core.md`

**Interfaces:**
- Produces: validator checks for bundled core manifest/files, no `REQUIRED SUB-SKILL`, and one-install packaging.

- [ ] Add assertions that fail while the Skill remains overlay-only.
- [ ] Push the test-only commit.
- [ ] Confirm GitHub Actions fails for the expected missing standalone files/dependency wording.

### Task 2: Bundle the version-locked core snapshot

**Files:**
- Create: `.agents/skills/japan-listing-demo/core/manifest.yaml`
- Create: `.agents/skills/japan-listing-demo/core/workflow.md`
- Create: `.agents/skills/japan-listing-demo/core/contracts.md`
- Create: `.agents/skills/japan-listing-demo/core/market-research.md`
- Create: `.agents/skills/japan-listing-demo/core/localization.md`
- Create: `.agents/skills/japan-listing-demo/core/visual-evidence.md`
- Create: `.agents/skills/japan-listing-demo/core/qa.md`
- Create: `.agents/skills/japan-listing-demo/core/profiles/categories/_template.md`
- Create: `.agents/skills/japan-listing-demo/core/evals/core.md`
- Create: `.agents/skills/japan-listing-demo/core/evals/cross-category.md`
- Create: `.agents/skills/japan-listing-demo/core/evals/multichannel.md`

**Interfaces:**
- Consumes: public core v0.2.0 files.
- Produces: local runtime core references available without external installation.

- [ ] Copy and curate the approved core snapshot.
- [ ] Record source repository, version, commit, bundled scope, and update policy.
- [ ] Confirm no non-Japan locale or region profile is required at runtime.

### Task 3: Convert the Skill and metadata to standalone operation

**Files:**
- Modify: `.agents/skills/japan-listing-demo/SKILL.md`
- Modify: `.agents/skills/japan-listing-demo/agents/openai.yaml`
- Replace: `.agents/skills/japan-listing-demo/references/public-core.md` with standalone core provenance and maintenance guidance.

**Interfaces:**
- Produces: `$japan-listing-demo` as the only team-facing invocation.

- [ ] Remove `REQUIRED SUB-SKILL` and external load steps.
- [ ] Instruct the agent to read bundled `core/` plus selected Japan references/channel profile.
- [ ] Preserve category/persona/privacy boundaries.

### Task 4: Make packaging and validation prove one-install usability

**Files:**
- Modify: `.agents/skills/japan-listing-demo/scripts/validate_overlay.py`
- Modify: `.agents/skills/japan-listing-demo/scripts/package_skill.py`
- Modify: `.github/workflows/validate-japan-listing-demo.yml`

**Interfaces:**
- Produces: `dist/japan-listing-demo.skill.zip` containing all runtime files.

- [ ] Validate required bundled core files and provenance.
- [ ] Reject runtime external-dependency wording.
- [ ] Build ZIP and inspect archive members in CI.
- [ ] Verify the ZIP contains `SKILL.md`, `core/`, Japan references, channel profiles, evals, and scripts.

### Task 5: Update team-facing documentation and version

**Files:**
- Modify: `README.md`
- Modify: `docs/install.md`
- Modify: `CHANGELOG.md`
- Create or update: `VERSION`

**Interfaces:**
- Produces: one-repository, one-ZIP, one-command team instructions.

- [ ] State that users install only `japan-listing-demo`.
- [ ] Separate public team use from optional private brand overlays.
- [ ] Document upstream maintenance without exposing it as a user requirement.
- [ ] Set version to `0.2.0`.

### Task 6: Verify, review, and release

**Files:**
- All changed files.

**Interfaces:**
- Produces: green PR, merged `main`, and downloadable CI artifact.

- [ ] Run GitHub Actions validator and package job.
- [ ] Confirm all expected archive members and no category/private leakage.
- [ ] Review PR diff and merge only after CI succeeds.
- [ ] Download the generated artifact and provide it to the user.
