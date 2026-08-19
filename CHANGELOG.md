# Changelog

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
