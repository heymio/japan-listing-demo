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

The thin router maps:

```text
Stage 0–7      → listing-planning
Stage 7.5–8    → listing-production
Stage 8.5–10   → listing-hardening
```

`listing-hardening` delegates exact-file evidence work to `listing-evidence-auditor`.

### Planning

Planning remains strategically deep. It owns product/offer/claim truth, consumer/VOC/competitor reasoning, Japan localization, channel capability/frontend reference intake, page architecture, Gallery/enhanced-content role planning, module budget and module fit.

Before Production, Planning creates:

- Project Brief;
- Creative Strategy Kernel;
- Production Handoff;
- Complete Demo-Required Production Set.

For fresh projects, Stage 6.5 is Source Asset Intake only. Full project-wide evidence audit is not mandatory there. Use targeted early audit only for an inherited/reused previously approved exact asset.

### Production

Production receives only formal production inputs and one-job Asset Packets. It is artifact-first and does not carry full workflow/auditor state into visual-generation prompts.

Creative status uses:

```text
PLANNED
READY
REVIEW
REVISE
USER_APPROVED
BLOCKED
```

`USER_APPROVED` is creative approval, not physical verification.

Production Freeze records whether the complete creative asset set is approved for Hardening.

### Hardening

Stage 8.5 runs mandatory full final-asset audit. Hardening owns exact file identity, transform/role/scope integrity, slot binding, module origin, frontend fidelity, demo assembly, delivery parity and Final QA.

Delivery State 0.2 separates creative completeness from evidence verification:

```text
PRODUCTION_FREEZE_GATE
PRE_DEMO_ASSET_GATE
```

The existing machine validator remains available through the compatibility path:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/state.json --json
```

Its canonical implementation now lives under `listing-hardening`.

## Major Stage Checkpoints

Default checkpoint output is concise:

```text
Done:
Open:
Next:
```

Use a full Stage Completion Manifest only for `PARTIAL`, `BLOCKED`, or explicit detailed audit review.

`继续 / 下一步 / go / next / 先这样` normally advances the workflow. The same artifact/problem has at most two autonomous retries without new input or evidence.

## Recommended repository / Codex bundle

Build:

```bash
python scripts/package_codex_bundle.py
```

Output:

```text
dist/japan-listing-demo-codex-bundle.zip
```

This package contains all five sibling Skills under `.agents/skills/` while preserving one normal invocation: `$japan-listing-demo`.

## One-install compatibility ZIP

Build:

```bash
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

The compatibility archive contains the main router plus embedded internal Skills:

```text
japan-listing-demo/
├── SKILL.md
├── references/
├── data/
├── scripts/
└── internal-skills/
    ├── listing-planning/
    ├── listing-production/
    ├── listing-hardening/
    └── listing-evidence-auditor/
```

This is still one model context. Context Projection and stage boundaries apply, but loading embedded `listing-evidence-auditor` does not create independent semantic review. `SINGLE_CONTEXT_LIMITATION.txt` documents the limitation. Unresolved semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless resolved through an appropriate human or genuinely independent review.

## Channel-native work

Planning establishes Platform Capability evidence, a Primary Reference, Frontend Visual evidence and Channel Frontend Reference Pack. Official platform/retailer rules do not substitute for current consumer-facing visual evidence.

Hardening verifies the final channel-native implementation. If native fidelity is not sufficiently supported, use `Content Review Demo` rather than fabricating channel chrome.

## Full validation

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

## Recommended user prompt

```text
Use $japan-listing-demo.
按默认 Major Stage Checkpoint 执行。
从产品/Offer/Claim和消费者策略开始；确认页面结构和完整生产资产集后，再进入逐张视觉生产；最终 Demo 前执行 Hardening。
```

## Optional team GPT

See `docs/team-gpt-setup.md`. The GPT is an optional UX shell; GitHub-packaged Skills remain the versioned execution source of truth.

## Optional private overlay

Private overlays may add confidential product evidence, pricing/SKU decisions, unreleased capabilities, private design assets, internal channel access and approval rules. Do not copy confidential material into this public repository.
