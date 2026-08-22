# japan-listing-demo installation and use

## Recommended team setup: one repository

Use **one repository**:

```text
heymio/japan-listing-demo
```

It contains five sibling Skills:

```text
.agents/skills/japan-listing-demo/
.agents/skills/listing-planning/
.agents/skills/listing-production/
.agents/skills/listing-hardening/
.agents/skills/listing-evidence-auditor/
```

Normal team users invoke only:

```text
$japan-listing-demo
```

Internal Skills are routed automatically by stage. Team users do not need to invoke them manually.

## Runtime model

```text
Stage 0–7      → listing-planning
Stage 7.5–8    → listing-production
Stage 8.5–10   → listing-hardening
```

`listing-hardening` delegates exact-file evidence work to `listing-evidence-auditor`.

### Planning

Planning remains strategically deep. It owns product/offer/claim truth, consumer/VOC/competitor reasoning, Japan localization, channel capability/frontend reference intake, page architecture, Gallery/enhanced-content role planning, module budget and module fit.

Before Production, Planning creates Project Brief, Creative Strategy Kernel, Production Handoff, Complete Demo-Required Production Set, Page Visual System, and one Evidence Mode per final asset.

Evidence Mode is `SOURCE_FAITHFUL`, `CREATIVE_MOCK`, or `PROOF_VISUAL`. v0.3.3 requires `PROOF_VISUAL` to carry explicit claim/fact/authoritative-source bindings before it can become final-consumable.

For fresh projects, Stage 6.5 remains Source Asset Intake only. Full project-wide evidence audit is not mandatory there. Use targeted early audit only for an inherited/reused previously approved exact asset.

### Account Capability Profile

A private team/project environment may supply persistent account-level capability evidence. When that profile is recent and non-conflicted, Planning reuses it instead of repeatedly asking the same project-level question. Missing/stale/conflicting records are re-verified.

The public Skill contains only the generic resolver. Do not place real private brand/account capability values in this public repository.

### Production

Production receives only formal production inputs and one-job Asset Packets. It is artifact-first and does not carry full workflow/auditor state into visual-generation prompts.

v0.3.2 production features remain active: Page Visual System context, Evidence Mode, exact candidate Selection Lock, set-level Creative QA, Scope Delta, and Smallest Sufficient Cleanup.

v0.3.3 strengthens Production Freeze:

- required Asset IDs are the union of authoritative plan/implementation/slot-contract/blocker state rather than one source overriding another;
- every final Asset ID binds to an exact selected `candidate_id` and `output_ref`;
- blocked assets, revision-pending assets, stale Set QA, missing exact output bindings, or `ready_for_hardening=false` prevent hardening readiness.

`USER_APPROVED` remains creative approval, not physical verification.

### Hardening

Stage 8.5 runs mandatory full final-asset audit. Hardening owns exact file identity, transform/role/scope integrity, slot binding, module origin, frontend fidelity, Demo static preflight, no-network browser runtime proof, delivery parity and Final QA.

For Delivery State 0.2, pre-Demo verification is mandatory by workflow. Caller-authored `pre_9_required=false` cannot disable it and an empty required asset set cannot pass.

Canonical final gates include:

```text
PRODUCTION_FREEZE_GATE
PRE_DEMO_ASSET_GATE
FRONTEND_FIDELITY_GATE
DEMO_RUNTIME_GATE
```

The compatibility validator remains available at:

```bash
python3 .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/state.json --json
```

The canonical implementation lives under `listing-hardening`.

Static standalone HTML validation is a preflight, not an interaction hard-PASS. External/local images, scripts, stylesheets, SVG resources, inline-style external URLs, mixed `srcset`, and session-only literal `blob:` resources are rejected. When carousel markup is present, actual PASS requires browser runtime evidence bound to the exact Demo SHA.

Browser runtime QA is no-network and checks 1440px and 390px layouts, horizontal overflow, broken images, clipped primary elements, and both carousel directions when present. If browser runtime cannot run, the Demo runtime gate remains `UNVERIFIED/BLOCKED`.

## Major Stage Checkpoints

Default checkpoint output is concise:

```text
Done:
Open:
Next:
```

Use a full Stage Completion Manifest only for `PARTIAL`, `BLOCKED`, or explicit detailed audit review.

Explicit advancement wording such as `继续 / 下一步 / go / next` advances the workflow. `先这样` is ambiguous and does not advance a major stage by itself. `这张先过` accepts and locks the exact current asset within Production; it does not skip incomplete Production or Hardening.

## Recommended repository / Codex bundle

Build:

```bash
python3 scripts/package_codex_bundle.py
```

Output:

```text
dist/japan-listing-demo-codex-bundle.zip
```

The v0.3.3 Codex bundle contains all five sibling Skills plus repository metadata required for `validate_overlay.py`. The builder rejects symlink inputs, writes deterministic ZIP metadata, extracts the result, and runs `validate_overlay.py` before success.

## One-install compatibility ZIP

Build:

```bash
python3 .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

The compatibility archive contains one user-facing Skill plus embedded internal Skills:

```text
japan-listing-demo/
├── SKILL.md
├── references/
├── data/
├── scripts/
│   ├── validate_project_state.py
│   └── validate_install.py
└── internal-skills/
    ├── listing-planning/
    ├── listing-production/
    ├── listing-hardening/
    └── listing-evidence-auditor/
```

This remains one model context. Loading embedded `listing-evidence-auditor` does not create independent semantic review. `SINGLE_CONTEXT_LIMITATION.txt` documents the boundary.

The v0.3.3 one-install package excludes repository-only selftests and instead runs package-local `validate_install.py` after extraction. It is deterministic and rejects symlink inputs.

## Channel-native work

Planning establishes Platform Capability evidence, a Primary Reference, Frontend Visual evidence and Channel Frontend Reference Pack. Official platform/retailer rules do not substitute for current consumer-facing visual evidence.

Hardening executes `FRONTEND_FIDELITY_GATE`. If native fidelity is not sufficiently supported, use a clearly labeled `Content Review Demo` rather than fabricating channel chrome.

## Full validation

```bash
python3 .agents/skills/japan-listing-demo/scripts/selftest_fail_closed_v033.py
python3 .agents/skills/listing-planning/scripts/selftest_planning.py
python3 .agents/skills/listing-production/scripts/selftest_production.py
python3 .agents/skills/listing-hardening/scripts/selftest_hardening.py
python3 .agents/skills/listing-hardening/scripts/selftest_demo_output.py
python3 .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python3 .agents/skills/japan-listing-demo/scripts/selftest_router.py
python3 .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python3 .agents/skills/japan-listing-demo/scripts/selftest_distribution_v033.py
python3 .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python3 .agents/skills/japan-listing-demo/scripts/package_skill.py
python3 scripts/package_codex_bundle.py
python3 -m zipfile -l dist/japan-listing-demo.skill.zip
python3 -m zipfile -l dist/japan-listing-demo-codex-bundle.zip
```

## Recommended user prompt

```text
Use $japan-listing-demo.
按默认 Major Stage Checkpoint 执行。
从产品/Offer/Claim和消费者策略开始；确认页面结构、完整生产资产集和整页视觉方向后，再进入逐张视觉生产；最终 Demo 前执行 Hardening。
```

## Formal version install / upgrade

For team-wide use, prefer an immutable GitHub Release rather than a temporary CI artifact. A formal v0.3.3 release provides:

```text
Tag: v0.3.3
Release assets:
- japan-listing-demo.skill.zip
- japan-listing-demo-codex-bundle.zip
- SHA256SUMS.txt
```

The release workflow is triggered only after `Validate japan-listing-demo skill` succeeds for an exact `main` SHA. Repository code is checked out and executed only in a `contents: read` build job. A separate publish job receives `contents: write`, re-verifies that `main` still equals the validated SHA, validates checksums, and creates the immutable tag/Release for that SHA.

Upgrade by replacing the installed bundle with the assets from the tagged Release, then verify `VERSION` and run the package-local/extracted validation appropriate to the distribution mode.

A merge to `main` alone is not a formal release. CI artifacts are temporary verification outputs and can expire.

## Rollback

For a v0.3.3 rollout, the immediate rollback target is the immutable `v0.3.2` Release. Reinstall its ZIP assets rather than reconstructing a historical package from a moving branch.

Existing project state should not be silently rewritten during rollback. Resume from the last human-approved checkpoint and re-run Hardening if validator semantics differ between versions.

## Optional team GPT

See `docs/team-gpt-setup.md`. The GPT is an optional UX shell; GitHub-packaged Skills remain the versioned execution source of truth.

## Optional private overlay

Private overlays may add confidential product evidence, pricing/SKU decisions, unreleased capabilities, private design assets, internal channel access and approval rules. Do not copy confidential material into this public repository.