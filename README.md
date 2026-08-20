# japan-listing-demo

`japan-listing-demo` turns product evidence into Japan-market listing strategy, channel-specific content architecture, visual briefs, and channel-native review demos.

## One repository, one normal invocation

Japan-team repository/Codex users use **one repository**:

```text
heymio/japan-listing-demo
```

The repository now contains two sibling Skills:

```text
.agents/skills/
├── japan-listing-demo/
└── listing-evidence-auditor/
```

Normal users still invoke only:

```text
$japan-listing-demo
```

The main Skill delegates asset-evidence reconciliation to `listing-evidence-auditor` automatically at the required checkpoints. Users do not need to run the auditor manually in the normal repository/Codex workflow.

## Why the evidence auditor exists

A machine-readable Project State can be internally consistent and still be wrong about the actual files. Asset IDs, filenames, planner-authored hashes, claimed provenance, and `LOCKED` status are therefore not enough.

`listing-evidence-auditor` checks:

```text
Candidate State
↕
physical file
↕
approval record
↕
semantic visual role
↕
required asset set
```

It recomputes physical SHA-256, path/file identity, supported image dimensions/signature, provenance, exact-hash approval binding, semantic role, slot scope, and set completeness.

## Candidate State → Auditor Evidence → Effective State

The workflow separates:

```text
Agent-authored Candidate State
+
Auditor-authored Evidence State
=
Effective State
```

For downstream asset eligibility:

```text
Auditor Evidence State > Candidate Asset Status
```

A planner-authored `LOCKED` value cannot override an auditor result such as:

```text
INVALIDATED
UNVERIFIED
PHYSICALLY_VERIFIED_ONLY
HUMAN_REVIEW_REQUIRED
```

Only these asset states are final-consumable:

```text
VERIFIED
HUMAN_APPROVED
```

## Mandatory evidence-audit checkpoints

### After Stage 6.5

```text
6.5A Candidate Asset Registry
↓
listing-evidence-auditor
↓
EVIDENCE_RECONCILIATION_GATE
↓
Effective State
↓
Stage 7
```

Stage 7 may continue planning with visible gaps, but final Asset-to-Slot bindings cannot lock non-final-consumable assets.

### Stage 8.5 before Demo Assembly

```text
Stage 8 Visual Production
↓
Stage 8.5 Pre-Demo Evidence Audit
↓
listing-evidence-auditor
↓
PRE_DEMO_ASSET_GATE
↓
Stage 9
```

`PRE_DEMO_ASSET_GATE` passes only when every required asset referenced by the locked Demo plan is `VERIFIED` or `HUMAN_APPROVED` and the required asset set is complete.

One invalidated/unverified required asset blocks final channel-native Demo assembly.

## Independent semantic review

Semantic visual-role auditing should run in an **independent context** / isolated subagent when the runtime supports it.

The auditor receives only the audit packet and evidence needed to inspect the assets. It should not receive the planner's desired PASS conclusion.

If an independent context is unavailable:

- deterministic physical checks can still run;
- same-agent semantic review cannot self-certify `VERIFIED`;
- semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless the user explicitly approves the exact physical SHA-256 + role + scope.

Loading the auditor instructions in the same reasoning context is not considered independent auditing.

## Exact approval binding

Approval is tied to exact content identity:

```text
physical SHA-256
+ visual role
+ approved slot/page/offer scope
```

A same-name replacement with different bytes does not inherit approval.

A deterministic crop/recomposition/resize/background replacement/role change is still a derivative and requires transform provenance/authorization.

## Existing executable gates remain active

v0.2.5 Project State validation is retained:

```text
CHANNEL_MODULE_BUDGET_GATE
APPROVAL_PROVENANCE_GATE
MODULE_ORIGIN_GATE
TRANSFORM_AUTH_GATE
ASSET_SLOT_GATE
DELIVERY_PARITY_GATE
```

v0.2.6 adds:

```text
EVIDENCE_RECONCILIATION_GATE
PRE_DEMO_ASSET_GATE
```

Agent-authored `declared_gate_results` are ignored.

For Amazon.co.jp the packaged current A+ ceilings remain machine-enforced:

```text
Basic A+    max 5 modules
Premium A+  max 7 modules
```

Brand Story is separate. Content-topic count is not module count.

## Channel-native frontend fidelity

Before generating a channel-native Demo, Stage 5.5 still requires a current consumer-facing reference:

1. verify Platform Capability;
2. ask for preferred current Reference URL / ASIN / retailer/store page / screenshot set;
3. otherwise research 1–3 current comparable pages;
4. build a Channel Frontend Reference Pack;
5. run `FRONTEND_FIDELITY_GATE` before Stage 9.

**Official rules do not substitute for frontend visual evidence.**

If frontend fidelity fails, output a clearly named `Content Review Demo` instead of inventing channel chrome.

## Checkpointed execution

The workflow still uses Major Stage Checkpoints and Stage Completion Manifest by default. `继续 / 下一步 / go / next / 先这样` advances the workflow rather than triggering an unbounded retry loop.

## Distribution

### Recommended: repository / Codex bundle

For the full separation-of-duties workflow use the repository or the two-Skill bundle:

```bash
python scripts/package_codex_bundle.py
```

Output:

```text
dist/japan-listing-demo-codex-bundle.zip
```

This contains both sibling Skills.

### Compatibility single-Skill ZIP

The legacy-compatible main Skill archive remains available:

```bash
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

Output:

```text
dist/japan-listing-demo.skill.zip
```

This is a **single-context compatibility package**. It cannot claim an independent semantic evidence audit. When `listing-evidence-auditor` cannot run in an independent context, unresolved semantic evidence remains `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless the user approves the exact asset hash + role/scope.

## Validation

```bash
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
```

## Quick-start prompt

```text
Use $japan-listing-demo.
按默认 Major Stage Checkpoint 执行。
Candidate Asset Registry 不视为真实素材证据；Stage 6.5 后自动调用 listing-evidence-auditor，并给我 EVIDENCE_RECONCILIATION_GATE。
Stage 8 后必须执行 Stage 8.5 Pre-Demo Evidence Audit；PRE_DEMO_ASSET_GATE 通过前不要进入最终 Stage 9 原生渠道 Demo。
如果无法独立运行 semantic auditor，不要自己审核自己并 PASS，保持 HUMAN_REVIEW_REQUIRED / UNVERIFIED，或者让我针对 exact hash + role + scope 审批。
继续使用 Project State external validator、Frontend Fidelity Gate、module budget / origin / transform / slot / parity gates。
```

## Version

`0.2.6`

## License

MIT.
