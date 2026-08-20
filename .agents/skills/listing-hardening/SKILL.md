---
name: listing-hardening
description: Use when hardening Stage 8.5–10 final listing assets, assembling the verified channel demo, and running delivery QA.
---

# Listing Hardening

## Core question

Are the final artifacts exact, safe, channel-correct, and ready to assemble/deliver?

## Plane boundary

This Skill owns Stage 8.5, Stage 9, and Stage 10 only. It does not own upstream strategy, market-research, or creative-brief design.

## Inputs

Consume only what final verification and assembly need:

- Production Freeze;
- exact final files;
- locked page/module plan;
- final Asset-to-Slot contract;
- relevant Project Brief fields;
- frontend capability/reference evidence;
- prior exact-asset approval evidence when relevant.

## Audit timing

Stage 8.5 runs the **mandatory full audit** through `listing-evidence-auditor` on the exact final files from Production Freeze.

Planning may request a **targeted early audit** only for an inherited or previously approved exact asset intended for reuse. A fresh project does not run the full project-wide audit before final production assets exist.

## Hardening responsibilities

Own:

- physical file identity and fingerprints;
- exact approval binding;
- transform authorization;
- semantic visual role verification;
- complete required asset-set verification;
- Asset-to-Slot integrity;
- locked module origin/plan hash;
- frontend fidelity;
- Demo Assembly;
- delivery parity;
- final technical/channel QA.

`USER_APPROVED` creative state never replaces final evidence verification.

## Evidence auditor

Delegate exact-file evidence work to sibling `listing-evidence-auditor`. When independent semantic review is unavailable, retain the auditor's existing human/independent-context limitation rather than self-certifying semantic truth.

## Output

Produce Delivery State, verified/fallback demo assembly result, delivery-parity result, and Final QA.
