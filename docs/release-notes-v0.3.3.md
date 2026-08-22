# v0.3.3 — Fail-Closed Hard Verification

v0.3.3 converts the v0.3.2 hardening layer from mostly happy-path verification to fail-closed verification under missing, empty, contradictory, stale, damaged, or install-relocated inputs.

Highlights:

- Demo Delivery State 0.2 now mandates non-empty Production Freeze and pre-Demo evidence; caller state cannot disable the hard audit.
- Required assets are the union of locked plan, implementation, slot contract, and still-required blocked/revision state instead of one source overriding the others.
- Production Freeze binds every final Asset ID to its exact selected candidate and output reference and fails on blockers, pending revisions, stale Set QA, or `ready_for_hardening=false`.
- `FRONTEND_FIDELITY_GATE` and `DEMO_RUNTIME_GATE` are canonical executable gates.
- Physical image verification rejects truncated PNG/JPEG/WebP structures; `PROOF_VISUAL` requires claim and authoritative-source binding plus trusted claim review.
- Standalone HTML preflight rejects external SVG and inline-style resources; interaction hard-PASS requires no-network browser runtime evidence at 1440px and 390px.
- Compatibility and Codex packages are deterministic, symlink-safe, and self-validate after extraction.
- Release publication is triggered only from a successful validation workflow for the exact current `main` SHA. Repository code executes only in a read-only build job; only the non-code publish job receives contents write permission.
- Ambiguous Chinese wording such as `先这样` no longer advances stages; `这张先过` accepts the current exact asset within Production rather than acting as an unconditional major-stage transition.
