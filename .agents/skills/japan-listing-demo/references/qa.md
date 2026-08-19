# Japan overlay QA

## Dependency QA

- Public `gtm-listing-demo` core version 0.2.0 or later is loaded.
- The selected public-core contracts and current Project Definition are available.
- This overlay does not duplicate or silently modify the public core.

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

- Every module passes the public core Visual Evidence Matrix.
- The visual subject and evidence object directly support the message.
- Product, packaging, UI, controls, interfaces, and functional proof use approved real assets or explicit provisional labels.
- Environment, casting, props, and interactions are project-specific and approved.
- Text remains readable and correctly localized on mobile.

## Technical and review-mode QA

- Gallery, tabs, carousels, comparisons, Q&A, and essential review interactions work on desktop and mobile.
- Local review files use native or CSS-safe fallbacks when JavaScript support is uncertain.
- Asset paths are complete.
- Standalone files have no missing local dependencies.
- Review Mode exposes status and open items.
- Consumer Mode hides internal labels and unsupported details while preserving complete meaning.
