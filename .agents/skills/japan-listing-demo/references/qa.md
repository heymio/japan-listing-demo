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
- Every advanced stage emits a **Stage Completion Manifest** with planned/completed/approved/needs-revision/missing/blocked/open items and `COMPLETE`, `PARTIAL`, or `BLOCKED` status.
- The agent completes a useful batch inside the current stage and does not pause after every minor search, tool call, frame, or image.
- A user Transition Command such as `继续`, `下一步`, `go`, `go next`, `next`, `先这样`, or `这张先过` stops further current-stage iteration and advances immediately unless the user explicitly asks to keep improving the current artifact.
- A Transition Command locks the real stage status; `PARTIAL` is not rewritten as `COMPLETE`.
- The same artifact/problem has a Retry Budget of at most two autonomous attempts without new user input or new evidence.
- A Transition Command overrides the Retry Budget; the agent must not require a second `继续` before entering the next stage.
- New authoritative evidence triggers a Change Impact Map rather than silent ignore or whole-project restart.

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
- Platform Capability evidence and Frontend Visual evidence are recorded separately.
- `CONTENT_COVERAGE` and `MODULE_FIT_GATE` are separate results.
- Native interactive modules have interaction logic and content packing planned before visual production.

## Frontend Fidelity QA

Run this section whenever the deliverable is intended to look like a real consumer-facing channel page.

- A **Channel Frontend Reference Pack** exists.
- The user was asked whether they had a preferred current **Reference URL**, ASIN, retailer/store page, design-system reference, or screenshot set before native demo assembly.
- A user-supplied valid reference is the candidate **Primary Reference** and is not silently replaced.
- If the user supplied no reference, 1–3 current comparable consumer-facing references were researched and a Primary Reference was selected with reasons.
- **Official rules do not substitute** for visual evidence of the current consumer-facing frontend.
- The reference pack records capture date, access status, desktop evidence, mobile/app-web evidence, section order, brand/platform ownership, material interactions, responsive behavior, fidelity status, and open questions.
- Text/DOM parsing alone is not labeled `HIGH` frontend fidelity.
- Live-page access failures follow the Retry Budget; the workflow does not repeatedly retry an inaccessible page or invent the missing shell.
- `FRONTEND_FIDELITY_GATE` runs immediately before Stage 9 for a channel-native demo.
- A gate failure produces a clearly named **Content Review Demo**, not a falsely labeled **channel-native demo**.
- A native demo reproduces the verified channel shell first and inserts approved project content only into verified brand-controlled regions.
- Review Mode is an overlay and does not change the verified underlying Consumer Mode layout.

## Asset Readiness and Slot Integrity QA

- Stage 1 contains an **Asset Readiness Preflight** for asset classes expected later.
- An **Approved Asset Registry** exists with stable Asset IDs and derivative provenance.
- Approved assets are not silently swapped, recropped, recomposed, or reassigned to another role downstream.
- An **Asset-to-Slot Contract** binds Asset IDs to page/offer, channel region/module, dimensions/aspect, crop/transform rule, interaction, and ownership.
- `ASSET_SLOT_GATE` fails on cross-slot leakage, wrong page/offer, wrong dimensions/crop, or unapproved derivatives.
- Gallery-native and enhanced-content assets remain distinct role classes unless an explicitly approved derivative says otherwise.

## Module Fit and Delivery Parity QA

- Full content/topic coverage does not automatically pass module fit.
- `MODULE_FIT_GATE` checks verified module availability, message grouping, interaction purpose, evidence, asset orientation/density, mobile behavior, frontend evidence, and channel constraints.
- Independent static boards are not mechanically converted into carousel/slides only during Demo Assembly.
- `DELIVERY_PARITY_GATE` compares planned versus implemented slot/module, interaction, Asset IDs, dimensions/aspect, message coverage, page/offer ownership, and channel region.
- Missing modules, wrong source assets, wrong dimensions, or static substitutes for planned interactions fail parity even when the HTML opens successfully.

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
- Every visualizable P0 differentiator has a Differentiator Proof Matrix entry.
- `DIFFERENTIATOR_PROOF_GATE` requires direct proof or an explicitly approved alternative proof strategy; generic lifestyle imagery alone is not enough.

## Change-control QA

- New authoritative facts, approved offer/strategy changes, asset/UI changes, channel-reference changes, or claim/legal decisions trigger a **Change Impact Map**.
- Outputs are classified `UNAFFECTED`, `REVIEW`, `INVALIDATED`, or `REOPEN`.
- Unaffected locked outputs are preserved.
- Invalidated dependent outputs do not remain silently in final work.
- The workflow does not restart the entire project unless dependency impact actually requires it.

## Technical and review-mode QA

- Gallery, tabs, carousels, comparisons, Q&A, and essential review interactions work on desktop and mobile when those interactions belong to the verified target shell.
- Local review files use native or CSS-safe fallbacks when JavaScript support is uncertain.
- Asset paths are complete.
- Standalone files have no missing local dependencies.
- Review Mode exposes status and open items without changing Consumer Mode geometry.
- Consumer Mode hides internal labels and unsupported details while preserving complete meaning.
- Deliverable naming matches evidence: a native PDP/demo name is used only after `FRONTEND_FIDELITY_GATE` passes or the user explicitly approves a constrained `PARTIAL` scope.

## Final Delivery QA

Before calling the work complete:

- Stage Completion Manifests are truthful;
- required planned deliverables exist or reduced scope is explicitly approved;
- `ASSET_SLOT_GATE` passes;
- `CONTENT_COVERAGE` is acceptable;
- `MODULE_FIT_GATE` passes;
- `DIFFERENTIATOR_PROOF_GATE` passes or has an approved alternative;
- `DELIVERY_PARITY_GATE` passes;
- channel-native work satisfies `FRONTEND_FIDELITY_GATE`;
- passed checks and open items are reported separately.
