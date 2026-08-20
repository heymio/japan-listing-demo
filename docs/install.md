# japan-listing-demo installation and use

## Recommended team setup: one repository

Use one public repository:

```text
heymio/japan-listing-demo
```

It contains two sibling Skills:

```text
.agents/skills/japan-listing-demo/
.agents/skills/listing-evidence-auditor/
```

Normal team users invoke only:

```text
$japan-listing-demo
```

The main workflow delegates to `listing-evidence-auditor` automatically. No second repository is required.

## Why two Skills live in one repository

`japan-listing-demo` plans and produces listing work. `listing-evidence-auditor` independently checks whether the exact physical files really match the planner's asset claims.

The separation prevents a planner-authored Candidate State from becoming its own evidence source.

## Default execution behavior

The workflow uses Major Stage Checkpoints. Each numbered stage emits a Stage Completion Manifest and waits for review unless the current request explicitly opts into Autonomous Mode.

`继续 / 下一步 / go / next / 先这样` normally advance the workflow; they do not authorize more retries or upgrade unresolved evidence.

## Evidence-audit checkpoints

### Post-6.5

```text
6.5A Candidate Asset Registry
→ listing-evidence-auditor
→ EVIDENCE_RECONCILIATION_GATE
→ Effective State
→ Stage 7
```

The Candidate Asset Registry is assertion state. Asset IDs, filenames, claimed role, claimed provenance, agent-authored hashes, and `LOCKED` status are not final physical evidence.

`listing-evidence-auditor` recomputes:

- actual SHA-256;
- allowed project-root path and file existence;
- file signature / supported dimensions;
- provenance;
- exact-hash approval binding;
- semantic visual role;
- required asset-set completeness.

Stage 7 may plan around explicit gaps, but final Asset-to-Slot bindings may use only:

```text
VERIFIED
HUMAN_APPROVED
```

### Stage 8.5 before Stage 9

```text
Stage 8 final visual files
→ Stage 8.5 Pre-Demo Evidence Audit
→ listing-evidence-auditor
→ PRE_DEMO_ASSET_GATE
→ Stage 9
```

Every final required file referenced by the locked Demo plan is re-audited after edits/transforms. `PRE_DEMO_ASSET_GATE` must PASS before final channel-native asset consumption.

One required `INVALIDATED`, `UNVERIFIED`, `PHYSICALLY_VERIFIED_ONLY`, or `HUMAN_REVIEW_REQUIRED` asset blocks final Stage 9 assembly.

## Independent context requirement

Semantic visual-role auditing should run in an **independent context** / isolated subagent whenever supported.

Only send the auditor the audit packet and evidence required to inspect the files. Do not send the planner's desired PASS result.

If the runtime cannot provide an independent context:

- deterministic physical fingerprinting can still run;
- same-agent semantic review cannot self-certify `VERIFIED`;
- unresolved semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED`;
- the user may resolve the ambiguity only by explicitly approving the exact physical SHA-256 + role + scope.

Loading the auditor Skill in the same reasoning context is not independent auditing.

## Approval provenance

Asset approval is tied to:

```text
exact physical SHA-256
+ approved visual role
+ approved slot/page/offer scope
```

A same-name replacement with different bytes does not inherit approval.

A deterministic crop/recomposition/resize/background replacement/role change remains a derivative and needs transform authorization.

## Project State external validator

Maintain one machine-readable Project State Manifest and run:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

It computes the existing v0.2.5 gates plus v0.2.6 evidence gates:

```text
CHANNEL_MODULE_BUDGET_GATE
APPROVAL_PROVENANCE_GATE
MODULE_ORIGIN_GATE
TRANSFORM_AUTH_GATE
EVIDENCE_RECONCILIATION_GATE
ASSET_SLOT_GATE
PRE_DEMO_ASSET_GATE
DELIVERY_PARITY_GATE
```

Agent-authored `declared_gate_results` are ignored. If validator/auditor execution is unavailable, applicable status remains `UNVERIFIED`, not manual PASS.

## Amazon.co.jp module budget

Current packaged executable ceiling:

```text
Basic A+    max 5 modules
Premium A+  max 7 modules
```

Brand Story is separate. Topic count is not module count.

## Frontend reference workflow

For channel-native demos, Stage 5.5 still requires a current consumer-facing frontend reference and Channel Frontend Reference Pack.

**Official rules do not substitute for frontend visual evidence.**

Run `FRONTEND_FIDELITY_GATE` before native Demo Assembly. If it fails, use `Content Review Demo` rather than fabricating channel chrome.

## Recommended repository / Codex distribution

Package both sibling Skills:

```bash
python scripts/package_codex_bundle.py
```

Output:

```text
dist/japan-listing-demo-codex-bundle.zip
```

This is the recommended package when the execution environment can isolate the auditor context.

## Compatibility single-Skill ZIP

Build:

```bash
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

This compatibility archive contains the main Skill only. It includes an explicit `SINGLE_CONTEXT_LIMITATION.txt` and **cannot claim an independent semantic evidence audit**.

In this mode semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless the user explicitly approves exact hash + role/scope.

## Full validation

```bash
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
python -m zipfile -l dist/japan-listing-demo.skill.zip
python -m zipfile -l dist/japan-listing-demo-codex-bundle.zip
```

## Recommended prompt

```text
Use $japan-listing-demo.
按默认 Major Stage Checkpoint 执行。
Stage 6.5 后自动调用 listing-evidence-auditor，Candidate Asset Registry 不能自己变成有效证据；输出 EVIDENCE_RECONCILIATION_GATE。
Stage 8 后必须执行 Stage 8.5 Pre-Demo Evidence Audit；PRE_DEMO_ASSET_GATE 通过前不要进入最终 Stage 9 原生渠道 Demo。
如果无法独立运行 semantic auditor，不要自己审核自己并 PASS；保持 HUMAN_REVIEW_REQUIRED / UNVERIFIED，或者让我针对 exact physical hash + role + scope 审批。
继续使用 Project State external validator、Frontend Fidelity Gate、module budget / origin / transform / slot / parity gates。
```

## Optional private overlay

Private overlays may add confidential product evidence, pricing/SKU decisions, unreleased capabilities, private design assets, internal channel access, and approval rules. Do not copy confidential material into this public repository.
