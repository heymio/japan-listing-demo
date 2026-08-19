# Bundled core snapshot

## Runtime behavior

`japan-listing-demo` is self-contained. Users do not install, open, or invoke another Skill to run the workflow.

The bundled core lives under:

```text
core/
```

It supplies the generic workflow, output contracts, market-research method, localization method, visual-evidence model, QA, category template, and core evals.

## Upstream provenance

```yaml
repository: heymio/gtm-listing-demo
version: 0.2.0
commit: b882526f5a683235d30f562006cf1984a9f0d9f9
```

The machine-readable record is `core/manifest.yaml`.

## Maintenance boundary

The upstream repository remains the maintenance source for generic methods. This repository publishes a tested snapshot so Japan-team users receive one repository, one ZIP, and one Skill invocation.

When updating the snapshot:

1. review the upstream changelog and commit;
2. update only the bundled core files affected;
3. preserve Japan-specific references and channel profiles;
4. run all core, Japan, channel, cross-category, packaging, and leakage checks;
5. release a new Japan Skill version only after CI passes.

Optional private brand overlays may add confidential rules, but they are not required for public team use.
