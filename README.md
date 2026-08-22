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

Normal checkpoints use `Done / Open / Next`. Explicit advancement wording such as `继续 / 下一步 / go / next` advances the workflow instead of triggering an unbounded retry loop. `先这样` is treated as ambiguous and does not advance a major stage unless the surrounding instruction clearly requests advancement. `这张先过` accepts and locks the exact current asset within Production; it is not an unconditional major-stage transition.

## Creative-first architecture

v0.3.x separates the workflow into stage-local execution planes behind a thin router:

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
- Complete Demo-Required Production Set;
- Page Visual System;
- one Evidence Mode per final asset.

The **Page Visual System** is a lightweight art-direction matrix inside the existing Stage 7 handoff. It specifies each asset's scene family, composition family, tone, product scale, and proof form so a coherent page does not collapse into one repeated template. **Same art direction ≠ same composition.**

Evidence Mode is one of:

```text
SOURCE_FAITHFUL
CREATIVE_MOCK
PROOF_VISUAL
```

This separates creative lifestyle/mock imagery from visuals that must carry factual proof. In v0.3.3, `PROOF_VISUAL` additionally requires explicit claim/fact/authoritative-source bindings before it can become final-consumable.

For a fresh project, Stage 6.5 is lightweight Source Asset Intake. Full project-wide evidence audit is not required before final assets exist. A targeted early audit is used only when inheriting/reusing a previously approved exact asset.

### Account capability reuse

Persistent channel/account facts such as enhanced-content access may be supplied through a private Account Capability Profile. If a recorded capability is recent and non-conflicted, Planning reuses it instead of asking the same project-level question again. Missing, stale, malformed, or contradicted capability evidence is re-verified.

The public repository contains only the generic mechanism; private brand/account values are not embedded here.

### Production: produce narrowly

`listing-production` receives only the Creative Strategy Kernel, Production Handoff, current one-job Asset Packet, referenced source assets, and approved visual benchmarks/patterns.

It is artifact-first: a request for one final Gallery or enhanced-content asset should produce that artifact rather than a workflow diagram, asset map, or production-plan infographic.

v0.3.2 production safeguards remain active in v0.3.3:

- every one-job Asset Packet requires the current Evidence Mode plus Page Visual System direction and nearest same-region neighbor summaries;
- product-identity sources are separated from proof-grade sources: a Creative Mock may tolerate missing proof evidence, but never missing evidence required to keep the product identity faithful;
- set-level Creative QA checks scene, composition, tone/brightness, product scale, proof form, and adjacent message-role repetition;
- the final current asset set must have a recorded whole-set/contact-sheet visual review before Production Freeze is ready;
- exact candidate Selection Lock protects the selected output, candidate history, and creative status until explicit reopen;
- Production may apply removal-only Scope Delta while keeping `asset_set`, `page_plan`, and `page_visual_system` aligned; additions or role/message/evidence changes return to Planning for a revised handoff;
- Smallest Sufficient Cleanup avoids broad regeneration when one targeted change can restore the page.

v0.3.3 strengthens Production Freeze itself. Required assets are derived from all authoritative planning/implementation sources rather than allowing one non-empty source to override another. Every final Asset ID must bind to an exact selected `candidate_id` and exact `output_ref`; blocked assets, pending revisions, stale Set-level QA, or `ready_for_hardening=false` keep Freeze not ready.

**Creative Approval ≠ Evidence Verification.**

### Hardening: verify rigorously

`listing-hardening` owns final file identity, evidence audit, role/scope integrity, transform authorization, module origin, slot integrity, frontend fidelity, demo assembly, runtime verification, delivery parity, and Final QA.

Stage 8.5 runs the mandatory full final-asset audit through `listing-evidence-auditor` before final Demo Assembly. For Delivery State 0.2 this pre-Demo audit is a workflow requirement; caller-authored `pre_9_required=false` cannot disable it and an empty required asset set cannot pass.

The final user-facing Demo delivery contract is one **standalone `.html` file**: images/resources are physically embedded as `data:` URIs, CSS/JS are inline, and no adjacent `assets/` directory or Demo ZIP is required. Static preflight rejects local/external image dependencies, mixed/external `srcset`, session-only literal `blob:` resources, external CSS/JS, external SVG resources, inline-style external URLs, and missing responsive CSS.

Static validation is necessary but is **not** interaction hard verification. When carousel markup is present, static preflight can validate structure, but `carousel_contract` remains runtime-required. Final hard-PASS requires no-network browser evidence bound to the exact Demo SHA. Runtime QA opens the Demo at 1440px desktop and 390px mobile, checks horizontal overflow, broken images, clipped controls/copy, and verifies carousel next/previous behavior in both directions. If browser runtime cannot be performed, the runtime gate remains `UNVERIFIED/BLOCKED` rather than self-declared PASS.

Delivery State 0.2 now makes these final questions explicit:

```text
PRODUCTION_FREEZE_GATE     → is the exact creatively approved set complete and internally ready?
PRE_DEMO_ASSET_GATE       → are the exact final files evidence-safe?
FRONTEND_FIDELITY_GATE    → is the claimed channel shell/order/interaction supported by evidence and approval?
DEMO_RUNTIME_GATE          → did the exact final HTML pass no-network browser QA at required viewports/interactions?
```

All are independently computed. A declared result cannot substitute for executable evidence.

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

`listing-evidence-auditor` is the exact-file trust boundary. It checks physical file identity, approval binding, provenance, semantic visual role, required asset-set completeness, and—for `PROOF_VISUAL`—claim/source binding.

v0.3.3 rejects structurally truncated supported images rather than accepting a valid-looking header alone. PNG requires complete IHDR/IDAT/IEND structure with CRC/decompression checks; JPEG/WebP receive additional completeness validation. Hard verification also performs a real Pillow decode/load; if the decoder is unavailable, exact-file image verification cannot be promoted to PASS.

A `PROOF_VISUAL` carries exact claim IDs, facts, and authoritative source IDs. Even when file/role/approval checks pass, it cannot become final-consumable without trusted human or genuinely independent semantic claim review covering those exact claims.

Loading the auditor inside the same model context does not create independent semantic review. If independent semantic review is unavailable, unresolved evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless resolved by an appropriate human or genuinely independent review.

## Distribution

### Recommended repository / Codex bundle

Build the five-sibling-Skill bundle:

```bash
python3 scripts/package_codex_bundle.py
```

Output:

```text
dist/japan-listing-demo-codex-bundle.zip
```

The v0.3.3 Codex bundle includes the repository metadata needed by `validate_overlay.py`, rejects symlink inputs, is built deterministically, and is extracted and validated before the packager reports success.

### One-install compatibility ZIP

Build:

```bash
python3 .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

This archive keeps one user-facing Skill and embeds the four internal stage/audit Skills under `japan-listing-demo/internal-skills/`. It remains a **single-context** package, so embedded auditor loading does not claim independent semantic review. `SINGLE_CONTEXT_LIMITATION.txt` documents that boundary.

The v0.3.3 compatibility package is deterministic and symlink-safe. It excludes repository-only selftests and instead contains a package-local `scripts/validate_install.py`; packaging extracts the ZIP and runs that validator against the installed layout before reporting success.

## Validation

Hard-verification CI installs Pillow plus Playwright/Chromium. Copyable repository checks are:

```bash
python3 .agents/skills/japan-listing-demo/scripts/selftest_fail_closed_v033.py
python3 .agents/skills/listing-planning/scripts/selftest_planning.py
python3 .agents/skills/listing-production/scripts/selftest_production.py
python3 .agents/skills/listing-hardening/scripts/selftest_hardening.py
python3 .agents/skills/listing-hardening/scripts/selftest_demo_output.py
python3 .agents/skills/listing-hardening/scripts/selftest_demo_runtime_v033.py
python3 .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python3 .agents/skills/listing-evidence-auditor/scripts/selftest_image_decode_v033.py
python3 .agents/skills/japan-listing-demo/scripts/selftest_router.py
python3 .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python3 .agents/skills/japan-listing-demo/scripts/selftest_distribution_v033.py
python3 .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python3 .agents/skills/japan-listing-demo/scripts/package_skill.py
python3 scripts/package_codex_bundle.py
```

## Quick start

```text
Use $japan-listing-demo.
按默认 Major Stage Checkpoint 执行。
从产品与市场策略开始，先确认页面结构、完整生产资产集和整页视觉方向，再逐张产出视觉；最终 Demo 前执行 Hardening。
```

Ordinary team users should not need to understand Skill routing, file hashes, provenance, or validator internals.

## Optional team GPT

A thin team-facing Custom GPT can provide onboarding and project-entry UX, but it is not the execution source of truth. See `docs/team-gpt-setup.md`.

## Release model

A merge to `main` updates the source-of-truth branch, but it is not the same thing as an immutable public release.

For v0.3.3, `release-validated.yml` is triggered by a `main` push and treats that exact `github.sha` as the only release candidate. Its **read-only build job** checks out that SHA with `persist-credentials: false`, verifies it is still current `main`, installs Pillow and Playwright/Chromium, executes the complete hard-verification suite on that exact source tree, builds both packages twice to prove reproducibility, and emits checksums plus SHA-bound release metadata. Repository code never runs with `contents: write`.

Only after that job succeeds does a separate **publish job** receive `contents: write`. It does not check out or execute repository code; it downloads the validated artifact, re-verifies metadata, checksums, tag state, and that `main` still equals the validated SHA, then creates `v0.3.3` against that exact commit. This keeps release validation and publication bound to the same SHA without relying on a second workflow event chain.

CI artifacts remain temporary verification outputs, not permanent release assets. For a v0.3.3 rollout, the immediate rollback target is the immutable `v0.3.2` Release.

## Version

`0.3.3`

## License

MIT.
