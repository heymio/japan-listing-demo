# Japan standalone QA

## Distribution QA

- The bundled core manifest, workflow, contracts, evidence, QA, category template, and core evals are present.
- The repository and Skill ZIP can run without loading or installing a second Skill.
- Team-facing instructions mention one repository, one ZIP, and one invocation.
- Upstream provenance is recorded for maintainers but not exposed as a runtime requirement.
- Optional private overlays remain optional and separate.

## Execution Flow QA

- **Checkpointed execution by default** is active.
- Every numbered workflow stage ends at a **Major Stage Checkpoint** unless the user explicitly opts into Autonomous Mode for the current request.
- The agent completes a useful batch inside the current stage and does not pause after every minor search, tool call, frame, or image.
- A user Transition Command such as `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, or `这张先过` stops further current-stage iteration and advances immediately unless the user explicitly asks to keep improving the current artifact.
- After a Transition Command, the prior stage is locked. Unresolved items are recorded as `NEEDS REVISION`, `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, `UNKNOWN`, or Open Items instead of being silently regenerated.
- The same artifact/problem has a Retry Budget of at most two autonomous attempts without new user input or new evidence.
- After the Retry Budget is exhausted, the workflow stops the retry loop and waits at the current checkpoint with the best available result or blocked status.
- A Transition Command overrides the Retry Budget; the agent must not require a second `继续` before entering the next stage.
- Final QA may flag earlier locked-stage issues but does not silently reopen them.

## Configuration QA

- `market.country` is `JP`.
- `locale`, `channel`, `category`, `offer`, and `page_targets` are explicit.
- The requested locale is not inferred solely from the market.
- One primary Japan channel profile is selected.
- Brand/private overlays are separated from this public repository.

## Market evidence QA

- Every market conclusion has source, date, category, channel, evidence type, confidence, and allowed usage.
- Hypotheses are labeled and do not enter final consumer copy as facts.
- Conflicting evidence remains visible until resolved.
- Search language, scenarios, and visual direction come from current project evidence.
- Competitor execution is not treated as proof of account access or market preference.

## Locale QA

When `locale.id: ja-JP`:

- copy has completed terminology, tone, ambiguity, and native-language review;
- numbers, dates, currency, units, symbols, and punctuation match current channel requirements;
- translation artifacts and internal placeholders are removed;
- mobile headlines remain understandable without enlarging the page;
- conditions remain attached to the claims they qualify.

## Channel QA

- Current editable slots and account capabilities are verified.
- Brand-controlled and platform- or retailer-controlled areas are separated.
- Module names and limits belong to the selected channel.
- A previous marketplace implementation does not define the current one.
- Unsupported or unknown capabilities remain `UNKNOWN` or `PENDING`.
- Mobile rendering and current content policies are checked.

## Claim and compliance QA

- The verification queue includes only requirements relevant to the current project.
- Volatile laws, platform rules, certification, pricing, availability, and service terms use current authoritative evidence.
- Copy and visuals imply no broader claim than the evidence supports.
- Comparisons, badges, rankings, endorsements, and quantified performance have current approval.
- `PENDING CLAIM`, `PROHIBITED`, and `INTERNAL ONLY` content is excluded from consumer mode.

## Visual QA

- Every module passes the bundled core Visual Evidence Matrix.
- The visual subject and evidence object directly support the message.
- Product, packaging, UI, controls, interfaces, and functional proof use approved real assets or explicit provisional labels.
- Environment, casting, props, and interactions are project-specific and approved.
- Text remains readable and correctly localized on mobile.
- Visual-quality failure does not trigger an unbounded regeneration loop; retry and transition rules are enforced.

## Technical and review-mode QA

- Gallery, tabs, carousels, comparisons, Q&A, and essential review interactions work on desktop and mobile.
- Local review files use native or CSS-safe fallbacks when JavaScript support is uncertain.
- Asset paths are complete.
- Standalone files have no missing local dependencies.
- Review Mode exposes status and open items.
- Consumer Mode hides internal labels and unsupported details while preserving complete meaning.
