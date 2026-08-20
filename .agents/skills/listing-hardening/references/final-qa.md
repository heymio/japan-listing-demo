# Final QA

## Purpose

Final QA answers whether the verified delivery is safe to present as complete for the requested review scope.

## Required checks

1. Production Freeze is complete for the approved scope.
2. Mandatory Stage 8.5 evidence audit is attached and current for the exact final files.
3. Required assets are final-consumable under auditor evidence.
4. Transform authorization is valid for every derivative.
5. Asset-to-Slot bindings match the locked plan.
6. Module origin and module budget checks pass.
7. `FRONTEND_FIDELITY_GATE` supports any channel-native label used.
8. `DELIVERY_PARITY_GATE` confirms implementation matches the locked plan.
9. Claim/offer/page boundaries remain intact in the implemented demo.
10. Mobile/responsive behavior has been reviewed for the requested delivery scope.
11. **Consumer Mode** contains no internal workflow labels, claim statuses, Asset IDs, or review-only controls.
12. **Review Mode** overlays are non-destructive and do not change the underlying consumer layout.

## Delivery parity

Delivery parity compares the approved plan and final implementation. A functioning demo can still fail delivery parity when it uses the wrong asset, omits a planned module, invents an interaction, changes the module type, or crosses an offer/page boundary.

## Failure handling

- Wrong file or wrong role: invalidate the affected delivery state and route the exact asset/slot back.
- Unauthorized derivative: return to Production for an approved derivative or exact original.
- Frontend evidence insufficient: deliver only a Content Review Demo unless the user explicitly approves a constrained non-native scope.
- Incomplete Production Freeze: return to Production; do not treat evidence verification as a substitute for creative completeness.

Final QA must not self-declare machine/auditor gates as passed when their required execution did not occur.
