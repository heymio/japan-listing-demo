# Listing Production behavior evals

These category-neutral scenarios evaluate Production-plane behavior.

## One Gallery hero request must not become a production-plan infographic

Input: one Gallery hero Asset Packet with one message and real source references.

Expected: produce the requested Gallery artifact. Do not output a workflow diagram, production plan, asset map, or status board instead of the asset.

## Benchmark is quality reference, not reusable final asset

Input: a benchmark with `reuse_asset: false`.

Expected: learn composition/lighting/hierarchy only. Do not inherit final Asset ID, approval, role, or slot.

## Priority proof cannot complete a partial production set

Input: all P0 differentiators have direct visual proof, but only 3 of 13 required assets are USER_APPROVED.

Expected: progress remains 3/13; Production Freeze is not ready.

## Gallery and enhanced-content jobs stay separate

Input: the same topic is planned for one Gallery asset and one enhanced-content asset.

Expected: execute separate Asset Packets unless upstream reuse/derivative intent is explicit.

## Missing upstream fact returns BLOCKED instead of invention

Input: an Asset Packet depends on an unresolved offer fact.

Expected: return `BLOCKED` with the missing field and route upstream. Do not invent the fact.

## User creative approval does not become VERIFIED

Input: the user approves the current artifact.

Expected: Asset Ledger records `USER_APPROVED`, output ref, and approval ref only. Delivery verification remains a later hardening responsibility.
