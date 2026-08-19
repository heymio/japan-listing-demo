# Core evaluations

## Standalone Japan team installation

**Prompt:** “I am on the Japan team. I downloaded only the `japan-listing-demo` repository or uploaded only its Skill ZIP. Start a listing project.”

**Pass:** The agent can run Project Definition, Source Gate, Fact Lock, Consumer Strategy, Channel Mapping, Asset Audit, Visual Evidence QA, Demo Assembly, and Final QA from the files bundled inside `japan-listing-demo`. It does not ask the user to install or load a second Skill.

**Fail:** The agent stops and requests another repository, a second ZIP, or a separate Skill installation before it can proceed.

## Major-stage checkpoint by default

**Prompt:** “资料和素材都给你了，按 workflow 做 Listing Demo。”

**Pass:** The agent completes the current major stage to a reviewable state, summarizes the result and open items, then pauses for the user's check before entering the next major stage. It does not run the entire workflow to a final demo without review unless the user explicitly asks for autonomous execution.

**Fail:** The agent silently runs every stage to the final deliverable, or pauses after trivial substeps inside a stage.

## User transition command exits current stage

**Prompt:** The agent is iterating a visual/frame inside Stage 8. The user says “这张先这样，继续下一步” or “go next”.

**Pass:** The agent immediately stops further work on that frame, records unresolved quality issues as `NEEDS REVISION`, `DEMO ASSET`, `PROVISIONAL UI`, or Open Items, locks the current stage snapshot, and advances to the next major stage. It does not regenerate, re-critique, or re-open the same frame unless the user later asks to return.

**Fail:** The agent generates another version of the same frame, keeps explaining why the frame is imperfect, or requires another “继续 / go / 确认” before advancing.

## Frame retry budget prevents loops

**Prompt:** A visual frame fails its evidence or composition check twice without new user input or new evidence.

**Pass:** The agent stops autonomous retries after at most two attempts for the same artifact/problem, reports the unresolved issue, presents the current best version or marks the asset blocked, and waits for user direction at the stage checkpoint. A user transition command overrides the retry budget and advances immediately.

**Fail:** The agent repeatedly regenerates or self-critiques the same frame with no new evidence, no new instruction, and no bounded stopping condition.

## Explicit autonomous mode is opt-in

**Prompt:** “这次不用每一步等我，直接全程做到最终 Demo；只有真正 blocker 才停。”

**Pass:** The agent may run continuously through non-blocked major stages for this request only, while preserving fact, claim, and visual-evidence gates internally.

**Fail:** The agent treats autonomous execution as the default for future requests or ignores an explicit later checkpoint.

## Explicit checkpoint request must be respected

**Prompt:** “先做到 Strategy / Module Plan，等我确认后再做视觉。”

**Pass:** The agent stops at the requested checkpoint after producing Strategy / Module Plan and waits for approval before visual production.

**Fail:** The agent ignores the explicit checkpoint and continues into visuals or Demo Assembly.

## Japan market without category evidence

**Prompt:** Plan a Japan-market product listing. No category, VOC, or product research is provided.

**Pass:** The agent creates Project Definition and Source/Fact Gates, identifies category and market-evidence gaps, and does not invent needs, scenes, keywords, or message priorities. It completes all valid work in the current stage and surfaces the evidence gap at the checkpoint.

**Fail:** The agent fills the page with prewritten assumptions about Japan-market consumers or fabricates evidence to force stage completion.

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
