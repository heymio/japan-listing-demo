# Bundled core snapshot

## Runtime behavior

`japan-listing-demo` bundles its generic listing core under:

```text
core/
```

Normal users invoke only `$japan-listing-demo`. In the repository/Codex distribution, the main Skill may delegate physical/semantic asset evidence reconciliation to the sibling `listing-evidence-auditor` Skill located in the same repository. This is a distribution-level separation-of-duties patch, not a dependency on another repository or a second manual user invocation.

The bundled core supplies the generic workflow, output contracts, market-research method, localization method, visual-evidence model, QA, category template, and core evals.

The Japan distribution adds tested runtime patches for:

- checkpointed execution, Transition Commands, Stage Lock, and Retry Budget;
- channel-native frontend reference intake, Channel Frontend Reference Pack, and Frontend Fidelity Gate;
- delivery completeness, stable asset/slot contracts, module-fit/parity, differentiator proof, and targeted reopen;
- executable Project State gates that prevent self-certified PASS;
- v0.2.6 independent evidence reconciliation against physical files, exact-hash approval, provenance, semantic role, and required asset-set completeness.

## Upstream provenance

```yaml
repository: heymio/gtm-listing-demo
version: 0.2.0
commit: b882526f5a683235d30f562006cf1984a9f0d9f9
```

The machine-readable record and distribution patches are in `core/manifest.yaml`.

## Distribution modes

### Repository / Codex

One repository contains two sibling Skills. User-facing flow remains one invocation, `$japan-listing-demo`, and the main workflow delegates the auditor automatically at Stage 6.5B and Stage 8.5 when the runtime supports independent context.

### Compatibility single-Skill ZIP

The `japan-listing-demo.skill.zip` remains supported for compatibility. Because it is a single-context package, it cannot claim independent semantic evidence audit. Unresolved semantic evidence stays `UNVERIFIED` / `HUMAN_REVIEW_REQUIRED` unless the user explicitly approves exact physical hash + role/scope.

## Maintenance boundary

The upstream repository remains the maintenance source for generic methods. This repository publishes a tested snapshot plus Japan distribution patches.

When updating the snapshot:

1. review upstream changelog/commit;
2. update only affected bundled core files;
3. preserve or deliberately revise distribution patches and channel profiles;
4. run core, Japan, channel, cross-category, frontend-fidelity, delivery-integrity, executable-gate, evidence-auditor, packaging, and leakage checks;
5. release only after CI passes.

Optional private brand overlays may add confidential rules, but they are not required for public team use.
