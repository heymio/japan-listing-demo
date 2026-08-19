# japan-listing-demo installation and use

## Team installation: one Skill

Japan-team users install only:

```text
japan-listing-demo
```

No second repository or Skill ZIP is required.

## Default execution behavior: Major Stage Checkpoints

For each numbered workflow stage:

1. complete the stage to a reviewable state;
2. emit a **Stage Completion Manifest**;
3. show output, assumptions, and open items;
4. stop at the Major Stage Checkpoint;
5. wait for the user's review before the next numbered stage.

A completed subset does not make a stage complete. A Transition Command can advance a `PARTIAL` stage, but does not relabel it `COMPLETE`.

## Transition Commands and Retry Budget

`继续 / 下一步 / go / go next / next / 先这样 / 这张先过` normally mean move to the next numbered stage unless the user explicitly asks to keep improving the current artifact.

The same artifact/problem has at most two autonomous retries without new evidence or direction.

## Delivery integrity

Read `references/delivery-integrity.md`.

The workflow uses:

- Asset Readiness Preflight;
- stable approved Asset IDs;
- Asset-to-Slot Contract;
- separate `CONTENT_COVERAGE` and `MODULE_FIT_GATE`;
- Differentiator Proof Matrix;
- Change Impact Map;
- planned-to-implemented parity.

Approved assets cannot be silently substituted downstream. A material crop/recomposition/role change creates a derivative with provenance.

## Project State Manifest and external validator

Read `references/executable-gates.md`.

Maintain one machine-readable **Project State Manifest**. Start from:

```text
.agents/skills/japan-listing-demo/templates/project-state.example.json
```

Run the **external validator**:

```bash
python .agents/skills/japan-listing-demo/scripts/validate_project_state.py path/to/project-state.json --json
```

It computes:

```text
CHANNEL_MODULE_BUDGET_GATE
APPROVAL_PROVENANCE_GATE
MODULE_ORIGIN_GATE
TRANSFORM_AUTH_GATE
ASSET_SLOT_GATE
DELIVERY_PARITY_GATE
```

Do not trust agent-authored `declared_gate_results`. The validator ignores that field.

If the validator cannot execute, applicable machine gates remain:

```text
UNVERIFIED
```

The agent must not manually self-certify PASS.

### Approval provenance

A `LOCKED` asset requires either:

- a user approval event bound to the exact current asset hash; or
- exact SHA-256 recovery of the previously locked asset.

Filename similarity or visual resemblance does not count as exact recovery.

A deterministic crop is still a transform. Material derivatives require a transform approval event and `TRANSFORM_AUTH_GATE`.

### Locked module plan

Stage 7 produces the module architecture, canonical `plan_hash`, and user approval event for that exact hash.

Stage 9 must consume that exact plan hash. It cannot add/remove modules, change native type/interaction, or retrofit a carousel and then rewrite the plan retroactively.

## Amazon.co.jp module budget

The packaged executable policy for this Skill version is:

```text
Basic A+   max 5 modules
Premium A+ max 7 modules
```

Brand Story is separate from the Premium A+ module budget.

The project may use a lower current-account limit. It cannot raise the packaged ceiling by editing its own Project State Manifest.

## Channel-native demo frontend reference workflow

When the requested deliverable should look like a real Amazon.co.jp, Rakuten, Yahoo! Shopping, retailer, or DTC frontend, the Skill must not generate the shell from memory.

At Stage 5.5:

1. verify Platform Capability;
2. ask whether the user has a preferred current Reference URL / ASIN / page / screenshot set;
3. use a valid user-supplied reference as candidate Primary Reference;
4. otherwise research 1–3 current consumer-facing references;
5. visually inspect material desktop/mobile shell, section order, interactions, and ownership;
6. output a Channel Frontend Reference Pack.

**Official rules do not substitute for frontend visual evidence.**

Immediately before Stage 9, run `FRONTEND_FIDELITY_GATE`. If it fails, output a clearly named `Content Review Demo` rather than inventing a channel-native shell.

## Autonomous Mode is optional

End-to-end continuous execution is opt-in for the current request only. It does not bypass Stage Completion Manifest, executable, approval-provenance, asset-slot, module-fit, differentiator-proof, parity, claim, or frontend-fidelity gates.

## Recommended prompt

```text
Use the standalone japan-listing-demo Skill.
按默认 Major Stage Checkpoint 执行；每个 numbered stage 做完后给我 Stage Completion Manifest。
如果我说“继续 / 下一步 / go next”，立即推进，不要继续重做当前 frame；同一问题最多自动重试两次。
提前做 Asset Readiness Preflight；已通过素材用稳定 Asset ID 绑定 slot。
CONTENT_COVERAGE 和 MODULE_FIT_GATE 分开检查；不要在 Demo 阶段把静态图机械切成 slide/carousel。
维护 Project State Manifest，并用 external validator 计算 CHANNEL_MODULE_BUDGET_GATE / APPROVAL_PROVENANCE_GATE / MODULE_ORIGIN_GATE / TRANSFORM_AUTH_GATE / ASSET_SLOT_GATE / DELIVERY_PARITY_GATE。
不要相信 declared_gate_results；validator 不能运行时保持 UNVERIFIED。
如果要生成 channel-native Demo，Stage 5.5 先问我是否有参考 URL / ASIN / 页面截图；没有则研究 1–3 个当前参考并让我确认 Primary Reference。
FRONTEND_FIDELITY_GATE 通过前不要把内容 Review 页面叫原生渠道 PDP Demo。
```

## Build the ZIP

```bash
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
```

## Optional private company overlay

Private overlays may add confidential product evidence, pricing/SKU decisions, unreleased capabilities, private design assets, internal channel access, and approval rules.

Recommended precedence:

```text
current user request
> current approved project evidence
> optional private brand overlay
> standalone japan-listing-demo
> older project material
```

Do not copy confidential material into this public repository.
