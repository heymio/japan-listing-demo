# Changelog

## 0.2.4 — Delivery integrity and change control

- Added **Stage Completion Manifest** so a completed subset of a stage cannot be mislabeled as full stage completion; statuses are `COMPLETE`, `PARTIAL`, or `BLOCKED`.
- Added **Asset Readiness Preflight** in Stage 1 to surface critical product/UI/channel asset gaps before visual production or demo assembly.
- Added **Approved Asset Registry** with stable Asset IDs, canonical source, dimensions/aspect, page/offer scope, allowed slots, approval status, derivative provenance, and transform rules.
- Added **Asset-to-Slot Contract** and `ASSET_SLOT_GATE` to prevent approved assets from being silently replaced, cross-slot asset leakage, wrong dimensions/crops, and unapproved derivatives.
- Added explicit Amazon rule that Gallery-native and enhanced-content assets are distinct slot classes unless an approved derivative says otherwise.
- Separated `CONTENT_COVERAGE` from `MODULE_FIT_GATE`; complete topic coverage no longer implies the selected native module architecture is valid.
- Prohibited mechanically converting independent static boards into carousel/slides only during Demo Assembly; interactive module logic/content packing must be planned in Stage 7 and Stage 7.5.
- Added `DIFFERENTIATOR_PROOF_GATE` so visualizable P0 purchase reasons require direct visual proof or an explicitly approved alternative proof strategy.
- Added `DELIVERY_PARITY_GATE` to compare planned vs implemented module/slot, interaction, source Asset IDs, dimensions/aspect, message coverage, page/offer ownership, and channel region before a demo can be called complete.
- Added **Change Impact Map** with `UNAFFECTED`, `REVIEW`, `INVALIDATED`, and `REOPEN` so newer authoritative evidence reopens only impacted work.
- Added anonymized real-project regression cases for false completion, silent asset substitution, cross-slot leakage, module-fit mistakes, missing native interaction, weak P0 proof, late asset discovery, and targeted reopen.
- Updated Amazon.co.jp profile, workflow, output contracts, QA, default prompt, README/install docs, validator, package membership, and version metadata.

## 0.2.3 — Channel-native demo fidelity gate

- Fixed a workflow gap where channel capability research could be completed without establishing the current consumer-facing frontend, allowing the agent to invent a generic marketplace/DTC shell during Demo Assembly.
- Added **Channel Frontend Reference Pack** as a required Stage 5.5 output for channel-native demos.
- Added explicit **Reference URL / ASIN / page / screenshot intake**: the agent asks whether the user has a preferred current reference; user-supplied references become the candidate Primary Reference.
- When the user has no reference, the agent researches 1–3 current comparable consumer-facing pages and recommends one Primary Reference at the Stage 5.5 checkpoint.
- Separated **Platform Capability evidence** from **Frontend Visual evidence**. Official platform/retailer/component rules do not by themselves prove the current frontend layout.
- Added visual-capture requirements for desktop/mobile shell anatomy, material section order, interaction, responsive behavior, and brand/platform ownership boundaries.
- Added `FRONTEND_FIDELITY_GATE` immediately before Stage 9.
- Added the fallback name **Content Review Demo** when frontend fidelity is not sufficiently verified; the workflow must not label an invented shell as a channel-native PDP/demo.
- Changed Stage 9 so verified channel shell and section order are reproduced first, then approved project content is inserted only into verified brand-controlled regions.
- Added Review Mode isolation: internal labels/statuses may overlay the demo but must not redesign the underlying Consumer Mode shell.
- Added channel-native rules to Amazon.co.jp, Rakuten, Yahoo! Shopping, DTC, and retailer PDP profiles.
- Added frontend-fidelity QA, regression evals, validator checks, package-member checks, README/install guidance, and version metadata.

## 0.2.2 — Checkpoint and anti-loop fix

- Restored **Major Stage Checkpoints by default** after real-world testing showed that fully autonomous end-to-end execution could produce structurally complete but low-quality final demos without enough human review.
- Added explicit **Transition Command** semantics: `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, `这张先过`, and equivalents advance to the next numbered stage unless the user explicitly asks to keep improving the current artifact.
- Added **Stage Lock** behavior so a stage that was approved or advanced is not silently reopened downstream.
- Added a **Retry Budget** of at most two autonomous attempts for the same artifact/problem without new user input or new evidence.
- Added Stage 8 anti-loop guidance so frame/image generation cannot repeatedly regenerate the same problem after the user asks to move on.
- Kept full end-to-end **Autonomous Mode** as an explicit opt-in for a specific request rather than the default.
- Updated Skill execution control, bundled workflow, default prompt, QA, team docs, validator rules, and regression evals.

## 0.2.1 — Continuous execution fix

- Changed the default execution model from stage-by-stage approval to continuous execution through all non-blocked stages required by the requested deliverable.
- Defined workflow gates as internal validation checkpoints rather than mandatory chat pause points.
- Added explicit Hard Blocker and user-requested checkpoint rules.
- Added non-blocking progress-update behavior and prohibited routine “继续 / go / 确认” prompts between normal stages.
- Replaced the Stage 4 `Human Review Gate` with a `Reviewable Strategy Snapshot` that remains reviewable without forcing a pause.
- Added batch visual-production guidance so the workflow does not stop after every asset unless per-asset review is explicitly requested.
- Added regression evals for continuous execution and explicit checkpoints.
- Added Execution Flow QA and validator checks for the new behavior.
- Updated README, installation guidance, default prompt, and version metadata.

## 0.2.0 — Standalone distribution

- Bundled a version-locked generic workflow snapshot inside the Japan Skill.
- Removed the runtime requirement to install or load a second Skill.
- Added core provenance manifest, workflow, contracts, evidence methods, QA, category template, and core evals.
- Updated `$japan-listing-demo` to be the only team-facing invocation.
- Updated README and installation instructions for one repository and one ZIP.
- Added validator checks for runtime dependency wording, standalone files, version, provenance, one-install documentation, and leakage boundaries.
- Added ZIP-member verification to the packager.
- Preserved Japan market-evidence, `ja-JP` localization, claim/compliance, channel, visual, mobile, and technical QA layers.

## 0.1.0 — Public Japan overlay

- Added Japan market-evidence framework.
- Added `ja-JP` localization and Japan claim/compliance references.
- Added Amazon.co.jp, Rakuten, Yahoo! Shopping, DTC, and retailer PDP channel profiles.
- Added category/persona leakage checks and Japan-specific evals.
