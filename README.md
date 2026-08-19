# japan-listing-demo

`japan-listing-demo` is a **standalone public Skill** for turning product evidence into Japan-market listing strategy, channel-specific content architecture, visual briefs, and channel-native interactive review demos.

## One repository, one ZIP, one Skill

Japan-team users install and invoke only:

```text
japan-listing-demo
```

No second generic-core Skill is required.

Invoke:

```text
$japan-listing-demo
```

## Checkpointed execution by default

The Skill uses **Major Stage Checkpoints** by default. Each numbered stage ends with a truthful **Stage Completion Manifest**:

```text
planned
completed
approved / locked
needs revision
missing
blocked
open items
STAGE_STATUS = COMPLETE / PARTIAL / BLOCKED
```

A completed subset does not make a stage complete.

When the user says `继续 / 下一步 / go / next / 先这样`, the Skill stops current retries, locks the real stage status, and advances. The same artifact/problem has at most two autonomous retries without new evidence or direction.

## Delivery integrity

The Skill prevents common downstream drift through:

- **Asset Readiness Preflight**;
- stable approved Asset IDs;
- **Asset-to-Slot Contract**;
- separate `CONTENT_COVERAGE` and `MODULE_FIT_GATE`;
- interaction planning before production;
- `DIFFERENTIATOR_PROOF_GATE`;
- Change Impact Map for targeted `REOPEN`;
- planned-to-implemented parity checks.

Approved assets must not be silently replaced by assets from another slot class. A material crop, recomposition, background change, or role change creates a derivative with provenance.

## Executable gates: no self-certified PASS

Critical structural gates use a machine-readable **Project State Manifest** and an **external validator**.

Start from:

```text
.agents/skills/japan-listing-demo/templates/project-state.example.json
```

Validate with:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

The external validator computes:

```text
CHANNEL_MODULE_BUDGET_GATE
APPROVAL_PROVENANCE_GATE
MODULE_ORIGIN_GATE
TRANSFORM_AUTH_GATE
ASSET_SLOT_GATE
DELIVERY_PARITY_GATE
```

Agent-authored fields such as `declared_gate_results` are ignored.

If validator execution is unavailable, applicable executable gates remain:

```text
UNVERIFIED
```

The agent must not manually self-certify PASS.

### Locked module plans

Stage 7 creates one locked module plan with stable module IDs, native module type, interaction, Asset IDs, approval stage, and canonical `plan_hash`.

Stage 9 must consume the exact plan hash. It cannot add a module, change static to carousel, remove a planned module, or retrofit interaction and then rewrite the plan retroactively.

### Approval provenance

A `LOCKED` asset requires either:

- a matching user approval event bound to the current asset hash; or
- exact SHA-256 recovery of a previously locked asset.

Filename similarity or visual resemblance is not exact recovery. A found file may remain `RECOVERED_UNAPPROVED` until valid provenance exists.

A deterministic crop is still a transform. Material derivatives require transform authorization and `TRANSFORM_AUTH_GATE`.

## Amazon.co.jp executable module limit

The packaged channel-policy file contains the current machine-enforced A+ ceilings used by this Skill version:

```text
Basic A+   5 modules
Premium A+ 7 modules
```

Brand Story is handled separately from the Premium A+ module budget.

Before an Amazon A+ module plan is locked, `CHANNEL_MODULE_BUDGET_GATE` compares the packaged ceiling, the current project/account limit, and the planned module count.

Content-topic count is not module count. Multiple messages must be packed into the verified native module budget rather than creating one module per topic.

## Channel-native demos require frontend references

A Platform Capability Map is not enough to generate a native-looking page.

At Stage 5.5, the Skill must:

1. verify current platform/account capability;
2. ask whether the user has a preferred current **Reference URL**, ASIN, retailer/store page, design-system reference, screenshot set, or PDF;
3. use a valid user reference as candidate Primary Reference;
4. otherwise research 1–3 current consumer-facing references;
5. visually inspect material desktop/mobile shell, section order, interactions, and ownership;
6. produce a **Channel Frontend Reference Pack**.

**Official rules do not substitute for frontend visual evidence.**

Immediately before Stage 9, run `FRONTEND_FIDELITY_GATE`. If it fails, the fallback must be named:

```text
Content Review Demo
```

The Skill must not invent marketplace chrome and call it a channel-native PDP/demo.

## Quick-start prompt

```text
Use the standalone japan-listing-demo Skill.
按默认 Major Stage Checkpoint 执行；每个 numbered stage 给我 Stage Completion Manifest。
如果我说“继续 / 下一步 / go next”，立即推进，不要继续重做当前 frame；同一问题最多自动重试两次。
提前做 Asset Readiness Preflight；已通过素材用稳定 Asset ID 绑定 slot。
CONTENT_COVERAGE 与 MODULE_FIT_GATE 分开检查，不要在 Demo 阶段把静态图机械切成 slide/carousel。
维护 Project State Manifest，并使用 external validator 计算 CHANNEL_MODULE_BUDGET_GATE / APPROVAL_PROVENANCE_GATE / MODULE_ORIGIN_GATE / TRANSFORM_AUTH_GATE / ASSET_SLOT_GATE / DELIVERY_PARITY_GATE。
不要相信或生成 declared_gate_results；validator 不能运行时保持 UNVERIFIED。
如果要生成 channel-native Demo，Stage 5.5 先问我是否有参考 URL / ASIN / 页面截图；没有则研究 1–3 个当前参考并让我确认 Primary Reference。
FRONTEND_FIDELITY_GATE 通过前不要把内容 Review 页面叫原生渠道 PDP Demo。
```

## Validation and packaging

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

The package output is:

```text
dist/japan-listing-demo.skill.zip
```

## Optional private use

Private brand overlays may add confidential product facts, pricing, claims, design links/assets, account capabilities, and approvals. Public Japan-team use remains one Skill.

## Version

`0.2.5`

## License

MIT.
