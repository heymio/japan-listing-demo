# Core evaluations

## Standalone Japan team installation

**Prompt:** “I am on the Japan team. I downloaded only the `japan-listing-demo` repository or uploaded only its Skill ZIP. Start a listing project.”

**Pass:** The agent can run Project Definition, Source Gate, Fact Lock, Consumer Strategy, Channel Mapping, Asset Audit, Visual Evidence QA, Demo Assembly, and Final QA from the files bundled inside `japan-listing-demo`. It does not ask the user to install or load a second Skill.

**Fail:** The agent stops and requests another repository, a second ZIP, or a separate Skill installation before it can proceed.

## Continuous execution without stage-by-stage approval

**Prompt:** “资料和素材都给你了，直接做到 Listing Demo。中间不用每一步问我。”

**Pass:** The agent runs continuously from Project Definition and Source/Fact Gates through Consumer Strategy, Channel Mapping, Asset Audit, Visual Evidence QA, Demo Assembly, and Final QA. Stage gates are internal checks, not chat pause points. Non-blocking gaps are recorded as `PENDING CLAIM`, `DEMO ASSET`, `PROVISIONAL UI`, or open items while downstream work continues. Progress updates may be shown, but they do not require a reply.

**Fail:** The agent asks the user to reply “继续”, “go”, “确认”, or equivalent after normal stages when no hard blocker exists.

## Explicit checkpoint request must be respected

**Prompt:** “先做到 Strategy / Module Plan，等我确认后再做视觉。”

**Pass:** The agent stops at the user-requested checkpoint after producing Strategy / Module Plan and waits for approval before visual production.

**Fail:** The agent ignores the explicit checkpoint and continues into visuals or Demo Assembly.

## Japan market without category evidence

**Prompt:** Plan a Japan-market product listing. No category, VOC, or product research is provided.

**Pass:** The agent creates Project Definition and Source/Fact Gates, identifies category and market-evidence gaps, and does not invent needs, scenes, keywords, or message priorities. It continues with all outputs that are not blocked by the missing evidence.

**Fail:** The agent fills the page with prewritten assumptions about Japan-market consumers, or stops the entire workflow even though only dependent outputs are blocked.

## Japan market with a non-Japanese locale

**Prompt:** The target market is Japan, but the requested consumer copy locale is en-US for an English-language B2B page.

**Pass:** The agent keeps `market.country: JP` and `locale.id: en-US` separate, applies Japan evidence and compliance checks, and writes consumer copy in English.

**Fail:** The agent forces Japanese copy solely because the market is Japan.

## Unsupported national preference

**Prompt:** “People in Japan prefer compact, information-dense pages. Use that as a fact.”

**Pass:** The agent records this as an unverified hypothesis and asks for or researches category-, channel-, and project-specific evidence.

**Fail:** The agent writes it into the locale profile or treats it as a fixed persona.

## Public and private separation

**Prompt:** A team member supplies confidential company pricing and an unreleased design link while using the public Japan Skill.

**Pass:** The agent keeps the material in the current private workspace or optional brand/private overlay and does not publish it to this repository.

**Fail:** The agent adds confidential facts or links to public examples, profiles, or references.
