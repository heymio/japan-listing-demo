# japan-listing-demo

`japan-listing-demo` turns product evidence into Japan-market listing strategy, channel-specific content architecture, focused visual production, and verified review demos.

## One repository, one normal invocation

Use **one repository**:

```text
heymio/japan-listing-demo
```

Normal users invoke only:

```text
$japan-listing-demo
```

A normal project can run in one Chat from source intake through strategy, visual production, hardening, and demo review.

## Team Golden Path

The user-facing workflow is deliberately simple:

```text
Upload product/GTM/source materials
↓
Review Product / Offer / Claim baseline
↓
Review Consumer / Market Strategy
↓
Review channel page plan
↓
Review Creative Strategy / complete production asset set
↓
Review generated visuals
↓
Review verified demo
```

Normal checkpoints use `Done / Open / Next`. `继续 / 下一步 / go / next / 先这样` advances the workflow instead of triggering an unbounded retry loop.

## Creative-first architecture

v0.3.0 introduced stage-local execution planes behind a thin router; v0.3.1 keeps that architecture unchanged and hardens the validators around it:

```text
$japan-listing-demo
        ↓
Thin Router
        ↓
listing-planning      Stage 0–7
        ↓
listing-production    Stage 7.5–8
        ↓
listing-hardening     Stage 8.5–10
        ↓
listing-evidence-auditor
```

The repository contains five sibling Skills:

```text
.agents/skills/
├── japan-listing-demo/
├── listing-planning/
├── listing-production/
├── listing-hardening/
└── listing-evidence-auditor/
```

Users do not manually invoke the internal stage Skills during the Golden Path.

### Planning: think deeply

`listing-planning` preserves deep product, offer, claim, consumer, VOC, competitor, Japan localization, channel, Gallery/enhanced-content, module-budget, and module-fit reasoning.

Planning ends with formal state objects instead of forwarding the whole conversation:

- Project Brief;
- Creative Strategy Kernel;
- Production Handoff;
- Complete Demo-Required Production Set.

For a fresh project, Stage 6.5 is lightweight Source Asset Intake. Full project-wide evidence audit is not required before final assets exist. A targeted early audit is used only when inheriting/reusing a previously approved exact asset.

### Production: produce narrowly

`listing-production` receives only the Creative Strategy Kernel, Production Handoff, current one-job Asset Packet, referenced source assets, and approved visual benchmarks/patterns.

It is artifact-first: a request for one final Gallery or enhanced-content asset should produce that artifact rather than a workflow diagram, asset map, or production-plan infographic.

Production uses:

- one-job Asset Packets;
- Visual Pattern Library and Golden Examples;
- compact Creative QA;
- Asset Ledger;
- `USER_APPROVED` creative state;
- Production Freeze for complete-set accounting.

**Creative Approval ≠ Evidence Verification.**

### Hardening: verify rigorously

`listing-hardening` owns final file identity, evidence audit, role/scope integrity, transform authorization, module origin, slot integrity, frontend fidelity, demo assembly, delivery parity, and Final QA.

Stage 8.5 runs the mandatory full final-asset audit through `listing-evidence-auditor` before final channel-native Demo Assembly.

Delivery State 0.2 keeps two separate questions explicit:

```text
PRODUCTION_FREEZE_GATE   → is the exact creatively approved Asset ID set complete?
PRE_DEMO_ASSET_GATE     → are the exact final files evidence-safe?
```

Both matter. One cannot substitute for the other.

## v0.3.1 validator integrity

v0.3.1 is a narrow engineering hardening release, not a workflow redesign. It adds parsed planning-contract validation, rejects invalid image bytes during physical fingerprinting, recomputes real-file fingerprints inside the normal reconciler path, rejects self-asserted semantic independence in the standalone CLI, requires Production Freeze Asset IDs to equal the required set, and makes malformed Delivery State fail before downstream gates execute.

These checks are designed primarily to prevent accidental or internally inconsistent workflow state. They do not by themselves prove Japan-market output quality or create an adversarial security boundary.

## Channel-native planning and demo fidelity

Planning separates Platform Capability evidence from Frontend Visual evidence. Official rules do not substitute for current consumer-facing visual evidence.

For channel-native work, Planning locks a Primary Reference and Channel Frontend Reference Pack. Hardening later verifies that the final demo follows the evidenced shell/order/ownership. When native fidelity cannot be supported, use a clearly labeled `Content Review Demo` rather than inventing channel chrome.

For Amazon.co.jp the current packaged planning ceilings remain:

```text
Basic A+    max 5 modules
Premium A+  max 7 modules
```

Brand Story is separate. `Message != Module`, and `CONTENT_COVERAGE` remains separate from `MODULE_FIT_GATE`.

## Evidence auditor

`listing-evidence-auditor` remains the exact-file evidence boundary. It checks physical file identity, approval binding, provenance, semantic visual role, and required asset-set completeness.

Normal reconciliation takes the audit packet plus the real project root and recomputes fingerprints from the files. A caller-supplied fingerprint JSON is not the normal trusted CLI input.

Loading the auditor inside the same model context does not create independent semantic review. If independent semantic review is unavailable, unresolved role evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless resolved by an appropriate human or genuinely independent review.

## Distribution

### Recommended repository / Codex bundle

Build the five-sibling-Skill bundle:

```bash
python scripts/package_codex_bundle.py
```

Output:

```text
dist/japan-listing-demo-codex-bundle.zip
```

### One-install compatibility ZIP

Build:

```bash
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

This archive keeps one user-facing Skill and embeds the four internal stage/audit Skills under `japan-listing-demo/internal-skills/`. It remains a **single-context** package, so embedded auditor loading does not claim independent semantic review. `SINGLE_CONTEXT_LIMITATION.txt` documents that boundary.

## Validation

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

## Quick start

```text
Use $japan-listing-demo.
按默认 Major Stage Checkpoint 执行。
从产品与市场策略开始，先确认页面结构和完整生产资产集，再逐张产出视觉；最终 Demo 前执行 Hardening。
```

Ordinary team users should not need to understand Skill routing, file hashes, provenance, or validator internals.

## Optional team GPT

A thin team-facing Custom GPT can provide onboarding and project-entry UX, but it is not the execution source of truth. See `docs/team-gpt-setup.md`.

## Version

`0.3.1`

## License

MIT.
