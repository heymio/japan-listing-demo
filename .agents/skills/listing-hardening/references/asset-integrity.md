# Asset integrity

## Purpose

Hardening verifies that the exact files entering Demo Assembly are the files the workflow claims they are. Creative `USER_APPROVED` means the marketing artifact was accepted; it does not prove physical identity, provenance, or delivery eligibility.

## Exact physical identity

Recompute real-file **SHA-256**, byte size, supported dimensions/signature, and allowed path through `listing-evidence-auditor`. Filenames, Asset IDs, visual resemblance, planner-authored hashes, and prior `LOCKED` labels are assertions rather than physical evidence.

Auditor evidence wins when it conflicts with candidate state.

## Approval binding

Final asset approval binds to the exact physical SHA-256 plus approved semantic role and approved page/offer/slot scope. A same-name replacement with different bytes does not inherit approval.

## Transform authorization

A crop, resize, recomposition, background replacement, role change, or other material **transform** creates a derivative. Deterministic execution does not authorize it. The derivative needs parent identity, transform intent, target slot, and matching approval provenance.

## Semantic role

A **semantic role** is what the actual visual is suitable to prove or represent, such as Gallery-native board, enhanced-content board, packshot, UI screenshot, mechanism diagram, comparison, packaging, or frontend reference.

A Gallery asset cannot satisfy an enhanced-content role merely because the topic is similar. A role mismatch invalidates the delivery binding.

## Complete asset set

Stage 8.5 audits the complete required set from Production Freeze and the locked plan. Missing, invalidated, unverified, or human-review-required required assets block final native Demo Assembly.

## Asset-to-Slot

The final **Asset-to-Slot** contract binds exact Asset IDs to exact slots/regions and interactions. Hardening checks:

- required Asset IDs exist;
- the exact audited files are final-consumable;
- the asset is allowed in the target slot;
- the implementation uses the locked Asset IDs;
- dimensions/aspect and interaction match the approved plan;
- no unapproved derivative silently replaces the approved file.

## Correction rule

If the implementation accidentally uses the wrong file, crop, role, or slot, correct the implementation or the upstream approved artifact. Do not rewrite the registry, approval record, or plan to legitimize the accidental demo after the fact.
