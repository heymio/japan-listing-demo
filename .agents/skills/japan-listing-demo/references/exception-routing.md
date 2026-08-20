# Exception routing

## Principle

A downstream Skill must not repair an upstream decision by inference. Return only the affected decision to the owning plane.

## Structured block

Use:

```yaml
status: BLOCKED
missing_field: <specific field name>
return_to: planning | production
asset_id: <affected asset when applicable>
reason: <why execution cannot continue safely>
```

The Router reopens only the targeted upstream item, updates the formal state object, regenerates only affected downstream packets, and then returns to the prior plane.

## Common routes

- Missing product/offer/claim/channel decision during Production → `planning`.
- Asset brief needs revision because strategy changed → `planning` for the affected message/asset requirement, then regenerate the Asset Packet.
- Hardening finds the wrong or unapproved creative file → `production` for the affected Asset ID.
- Hardening finds a plan/module/offer-boundary defect → `planning` for the affected plan item.
- Frontend evidence is insufficient → Planning may refresh the Primary Reference; Hardening does not invent channel chrome.

## Change Impact

Use a detailed Change Impact Map only when an authoritative locked input materially changes and several downstream outputs may be affected. It is exception-only, not normal checkpoint output.

## Recovery

Legacy/corrupted-project Recovery Mode is not part of normal runtime. Load recovery procedures only when explicitly requested for a damaged historical project.
