---
name: japan-listing-demo
description: Use when running a Japan-market listing project from source intake through strategy, visual production, hardening, and channel-native demo review.
---

# Japan Listing Demo Router

## Purpose

One project, one Chat, one normal invocation: `$japan-listing-demo`.

This is a **standalone** public distribution. The main Skill is a thin Router; stage-specific work lives in sibling Skills so deep strategy, focused production, and final hardening do not compete in one always-on instruction context.

Target operating principle:

> Think deeply. Produce narrowly. Verify rigorously.

Execution principle:

> Plan lightly → Produce directly → Harden rigorously.

Here, `lightly` means light control-plane overhead, not shallow strategy.

## Stage routing

Read `references/routing.md` and route by current stage:

- Stage 0–7 → `listing-planning`
- Stage 7.5–8 → `listing-production`
- Stage 8.5–10 → `listing-hardening`
- `listing-hardening` delegates exact-file evidence work to `listing-evidence-auditor`.

Do not duplicate the detailed rules of those Skills in this Router.

## Major Stage Checkpoint

Use **Major Stage Checkpoint** execution by default. Complete the current stage to a reviewable state, then stop for the user's review before entering the next major stage unless the user gives a Transition Command or explicitly requests autonomous execution.

Normal checkpoint display is concise:

```text
Done:
Open:
Next:
```

Show the full Stage Completion Manifest only when the stage is `PARTIAL`, `BLOCKED`, or the user explicitly requests detailed audit/state review.

## Transition Command

Treat `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalent wording as a **Transition Command** unless the user explicitly says to keep improving the current artifact.

On a Transition Command:

1. stop further retry/regeneration for the current artifact/problem;
2. preserve the best current result and truthful unresolved status;
3. persist the current formal state/handoff object;
4. advance immediately to the next stage;
5. do not silently reopen the prior stage.

A Transition Command never upgrades missing evidence or incomplete work into a false success state.

## Retry Budget

For the same artifact and same identified problem, allow at most **two autonomous attempts** without new user input or new evidence. After the Retry Budget is exhausted, stop and surface the current artifact, revision need, or blocker.

A Transition Command overrides the Retry Budget and advances immediately.

## Context Firewall

The Router enforces a **Context Firewall** between execution planes.

Planning may use deep source, product, VOC, market, localization, competitor, and channel reasoning. It must compress resolved production-relevant conclusions into formal handoff objects.

Production receives only:

- Creative Strategy Kernel;
- Production Handoff;
- current one-job Asset Packet;
- referenced source assets;
- approved visual benchmarks/patterns.

Do not inject workflow-control narration, long research history, prior failed attempts, auditor reports, or delivery-state machinery into visual-production prompts.

Hardening receives Production Freeze, exact final files, locked plan/slot requirements, relevant verification context, and frontend evidence. It does not need the full strategy conversation.

Loading a sibling Skill in the same Chat is not treated as proof of isolated model context; the formal handoff/context projection is the boundary.

## Plane boundaries

### Planning

`listing-planning` answers:

> What should we build, and why?

It owns product/offer/claim truth, consumer and market strategy, Japan localization, channel planning, Gallery/enhanced-content architecture, module fit/budget, Creative Strategy Kernel, and the Complete Demo-Required Production Set.

### Production

`listing-production` answers:

> Produce the approved artifacts.

It is artifact-first. It uses one-job Asset Packets, preserves real product identity, applies visual patterns/benchmarks, runs Creative QA, records creative approval in the Asset Ledger, and creates Production Freeze only when the approved production scope is complete.

### Hardening

`listing-hardening` answers:

> Are the final artifacts exact, safe, channel-correct, and ready to assemble/deliver?

Stage 8.5 performs mandatory full final-asset hardening. Final evidence-auditor and delivery-gate details belong there, not in Planning or Production.

## Exception routing

Read `references/exception-routing.md` when a downstream plane reports a missing upstream decision or invalidated dependency.

A downstream Skill must not improvise across ownership boundaries. Return a structured `BLOCKED` result with the specific `missing_field`, `return_to`, and affected Asset ID when applicable. Reopen only the impacted upstream item.

Detailed Change Impact analysis is exception-only. Legacy Recovery Mode is not part of the normal runtime path.

## State and resume

Conversation history is not the project database. Preserve formal project state through:

- Project Brief;
- Creative Strategy Kernel;
- Production Handoff;
- Asset Ledger / Production Freeze;
- Delivery State.

Use project/workspace files when the runtime supports them; otherwise maintain a compact structured snapshot without dumping it into every user-visible turn.

## Team Golden Path

The default team experience is:

```text
Upload source material
→ review Product / Offer / Claim baseline
→ review Consumer / Market Strategy
→ review channel page plan
→ review Creative Strategy / complete asset set
→ review generated visuals
→ review verified demo
```

Ordinary users should not need to manually invoke internal Skills or understand validator, evidence-auditor, hash, provenance, or state-machine internals.

## Public-safety boundary

Keep reusable public logic category-neutral. Do not place confidential brand/product/price/design/approval/unreleased project facts into this public repository or generic regression examples.
