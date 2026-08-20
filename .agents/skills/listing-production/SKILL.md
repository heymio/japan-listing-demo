---
name: listing-production
description: Use when producing Stage 7.5–8 listing assets from an approved Production Handoff and one-job Asset Packets.
---

# Listing Production

## Core question

Produce the approved artifacts.

## Plane boundary

This Skill owns Stage 7.5–8 only. It consumes the formal Production Handoff and Creative Strategy Kernel. It does not reinterpret Planning and does not perform final physical-file hardening.

## Inputs

Production may use only:

- Production Handoff;
- Creative Strategy Kernel;
- one current Asset Packet;
- referenced source assets;
- approved visual benchmarks/patterns.

Do not traverse the full project history to rebuild planning decisions during ordinary production.

## Artifact-first mode

Once production starts, the default response is the requested final artifact followed by a concise creative status. Do not substitute a workflow diagram, asset map, production plan, status board, or project-management infographic for the requested final asset.

## Creative status

`PLANNED` / `READY` / `REVIEW` / `REVISE` / `USER_APPROVED` / `BLOCKED`

**Creative Approval ≠ Evidence Verification.** `USER_APPROVED` means the creative/marketing output was accepted; it does not mean the file is physically verified or delivery-safe.

## One-job rule

Execute one Asset Packet at a time. One Asset Packet means one Asset ID, one channel role, one primary shopper task/message, and one final output quantity of 1.

Gallery and enhanced-content assets remain separate production jobs even when they communicate the same topic, unless Planning explicitly authorized reuse/derivative intent.

Batch production may begin only after the user approves the visual direction and explicitly asks to continue in that style.

## Context firewall

Build the generation/editing context from the current Asset Packet and referenced sources only. Do not inject Project State, auditor, gate, parity, or stage-status narration into production prompts.

## Missing upstream input

If the current asset lacks a required fact or business decision, return a structured `BLOCKED` result and identify the missing field. Do not invent or silently rewrite Planning.

## Completion

Stage 8 completion is measured against the complete required `asset_set` in Production Handoff. Priority proof coverage does not make a partial batch complete.
