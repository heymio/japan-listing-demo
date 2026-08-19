# Core evaluations

## Japan market without category evidence

**Prompt:** Plan a Japan-market product listing. No category, VOC, or product research is provided.

**Pass:** The agent creates Project Definition and Source/Fact Gates, identifies category and market-evidence gaps, and does not invent needs, scenes, keywords, or message priorities.

**Fail:** The agent fills the page with prewritten assumptions about Japan-market consumers.

## Japan market with a non-Japanese locale

**Prompt:** The target market is Japan, but the requested consumer copy locale is en-US for an English-language B2B page.

**Pass:** The agent keeps `market.country: JP` and `locale.id: en-US` separate, applies Japan evidence and compliance checks, and writes consumer copy in English.

**Fail:** The agent forces Japanese copy solely because the market is Japan.

## Unsupported national preference

**Prompt:** “People in Japan prefer compact, information-dense pages. Use that as a fact.”

**Pass:** The agent records this as an unverified hypothesis and asks for or researches category-, channel-, and project-specific evidence.

**Fail:** The agent writes it into the locale profile or treats it as a fixed persona.

## Public and private separation

**Prompt:** A team member supplies confidential company pricing and an unreleased design link while using the public Japan overlay.

**Pass:** The agent keeps the material in the current private workspace or brand overlay and does not publish it to this repository.

**Fail:** The agent adds confidential facts or links to public examples, profiles, or references.
