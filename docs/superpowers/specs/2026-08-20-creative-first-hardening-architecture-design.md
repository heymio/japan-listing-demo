# Creative-First Hardening Architecture Design

**Date:** 2026-08-20  
**Status:** Design for review  
**Repository:** `heymio/japan-listing-demo`

## 1. Purpose

Refactor `japan-listing-demo` so a team member can run one project in one Chat through strategy, visual production, and channel-native demo delivery without the workflow's control-plane rules overwhelming the production context.

The redesign preserves deep strategy and the hard-won delivery safeguards from v0.2.2–v0.2.6, but changes when and where those safeguards load.

The target operating principle is:

> **Think deeply. Produce narrowly. Verify rigorously.**

The execution principle is:

> **Plan lightly → Produce directly → Harden rigorously.**

Here, **lightly** means light control-plane overhead, not shallow strategy.

---

## 2. Problem Statement

### 2.1 Current failure mode

The current v0.2.6 workflow places too many responsibilities in the same always-on context:

- product and offer truth;
- market/VOC/competitor analysis;
- channel capability and frontend research;
- message architecture;
- Gallery/A+ planning;
- stage completion manifests;
- asset registries;
- approval provenance;
- transform authorization;
- evidence audit;
- executable gates;
- delivery parity;
- demo assembly.

These mechanisms are individually useful, but they are duplicated across `SKILL.md`, `core/workflow.md`, `references/delivery-integrity.md`, `references/executable-gates.md`, QA files, and the sibling evidence-auditor Skill.

The result is **control-plane duplication**: the agent repeatedly sees and narrates workflow management concepts even when the active task is creative production.

### 2.2 Observed regressions

Two classes of regressions demonstrate the architectural issue:

1. **Production-scope collapse** — the agent can confuse “priority differentiators have visual proof” with “the complete demo-required visual asset set has been produced.”
2. **Production-context contamination** — after long planning/status discussions, an image-generation turn can produce workflow plans, asset maps, or production infographics instead of the requested final listing asset.

Earlier, lighter executions showed the opposite pattern: creative output could be strong, but downstream demo assembly silently substituted assets, mixed channel roles, invented interactions, or treated internally coherent registries as proof that exact approved files were used.

The architecture therefore needs both:

- **strong strategy and focused production**, and
- **strict downstream hardening**.

It should not keep both fully active at every stage.

---

## 3. Goals

1. Keep one project, one Chat, and one normal user-facing invocation: `$japan-listing-demo`.
2. Preserve deep strategy, Japan localization, VOC/competitor reasoning, offer/claim boundaries, channel research, and content architecture.
3. Prevent governance language and project-management state from polluting visual-production prompts.
4. Require the complete production asset set to be defined before Stage 8 starts.
5. Preserve user creative approval separately from evidence verification.
6. Keep the existing evidence auditor and machine validation for final delivery integrity.
7. Make the workflow reusable by ordinary Japan marketing team members without requiring prompt-engineering, Skill-architecture, SHA, provenance, or validator knowledge.
8. Support clean project handoff/resume without requiring a new agent or team member to reread the whole conversation.
9. Prefer examples, patterns, and compressed creative strategy over ever-growing natural-language rules.
10. Keep public workflow logic category-neutral and free of confidential project data.

---

## 4. Non-Goals

This redesign does **not**:

- remove product strategy, VOC, market analysis, or consumer reasoning;
- weaken claim safety or channel capability verification;
- remove `listing-evidence-auditor`;
- allow final demo assembly from unverified or silently substituted assets;
- standardize legacy-project recovery procedures into the normal workflow;
- require users to split one project across multiple Chat conversations;
- make a Custom GPT the source of truth for execution logic;
- make plugins/apps a hard dependency;
- guarantee that loading a Skill creates an isolated model context.

---

## 5. Core Architecture

The workflow becomes three execution planes behind a thin router.

```text
Optional team-facing GPT
        ↓
$japan-listing-demo
THIN ROUTER
        ↓
┌──────────────────────────────┐
│ PLANNING                     │
│ Stage 0–7                    │
│ listing-planning             │
└──────────────┬───────────────┘
               ↓
      Production Handoff
               ↓
┌──────────────────────────────┐
│ PRODUCTION                   │
│ Stage 7.5–8                  │
│ listing-production           │
└──────────────┬───────────────┘
               ↓
       Production Freeze
               ↓
┌──────────────────────────────┐
│ HARDENING                    │
│ Stage 8.5–10                 │
│ listing-hardening            │
└──────────────┬───────────────┘
               ↓
      listing-evidence-auditor
```

### 5.1 Separation principle

Each component answers one core question:

| Component | Core question |
|---|---|
| Thin Router | What should execute now? |
| Planning | What should we build, and why? |
| Production | Produce the approved artifacts. |
| Hardening | Are final artifacts correct, safe, consistent, and ready to assemble/deliver? |
| Evidence Auditor | Are these exact physical files really the assets the workflow claims they are? |
| Optional GPT | How does a team member enter/resume the system easily? |

---

## 6. Thin Router

`japan-listing-demo` becomes a small orchestration Skill instead of the monolithic execution Skill.

### 6.1 Responsibilities

The router owns only:

1. current stage;
2. active stage Skill;
3. major-stage checkpoints;
4. transition-command semantics;
5. retry-budget semantics;
6. stage-to-stage handoff;
7. exception routing when a downstream Skill reports a missing upstream decision;
8. context-firewall enforcement.

### 6.2 Always-on rules

The router should keep only a compact permanent rule set:

```text
- One project / one Chat / one user-facing entry.
- Route execution by current stage.
- Use major-stage checkpoints by default.
- A transition command leaves the current stage immediately.
- Same artifact + same problem has at most two autonomous retries without new input/evidence.
- One stage must not silently redo another stage's responsibility.
- Pass only the minimum formal handoff object to the next execution plane.
- Missing upstream decisions must route back; downstream Skills must not improvise them.
- Control-plane language must not enter production prompts.
```

### 6.3 What leaves the router

The router should not contain full product-strategy, visual-production, auditor, provenance, module-fit, or final-QA rules.

The current large mandatory-rule block should be replaced by stage routing plus references to stage-specific Skills.

---

## 7. Planning Plane — `listing-planning`

Planning covers Stage 0–7.

### 7.1 Responsibilities

Planning retains or strengthens:

- Project Definition;
- source authority and freshness;
- Product Truth;
- Offer/Page Boundary;
- claim readiness;
- Consumer Strategy;
- JTBD, pains, barriers, reasons to believe;
- VOC and competitor analysis;
- Japan market and localization reasoning;
- search/category language where relevant;
- channel capability and frontend reference intake;
- Message Architecture;
- Gallery IA;
- A+ / enhanced-content IA;
- module availability, module budget, `CONTENT_COVERAGE`, and `MODULE_FIT_GATE`;
- full page/offer narrative;
- complete final production-asset requirements.

### 7.2 Planning quality remains deep

The redesign must not reduce strategic analysis to a short brief. Planning may use rich research and evidence internally.

The change is at the **handoff boundary**: downstream production receives compressed creative decisions rather than the full research history.

### 7.3 Stage 6.5 behavior

Stage 6.5 becomes lightweight **Source Asset Intake** by default.

It inventories source assets needed by later production, such as:

- real product renders/photos;
- UI sources;
- packaging;
- mechanism diagrams;
- approved brand assets;
- visual references;
- frontend captures.

A full project-wide evidence audit is **not mandatory** here for a fresh project.

#### Targeted early audit

Early `listing-evidence-auditor` use is triggered only when Planning intends to inherit/reuse a previously approved exact asset, for example:

> “Reuse the previously approved Gallery G3.”

The audit is targeted to the inherited asset(s), not the whole future production set.

### 7.4 Stage 7 completion requirement

Stage 7 cannot finish with only a message/module plan. It must determine the **Complete Demo-Required Production Set**.

Examples of required roles may include:

- marketplace main image;
- Gallery-native boards;
- A+-native boards/panes;
- carousel frames if a verified native interaction was intentionally planned;
- UI screenshots;
- comparison visuals;
- installation decision visuals;
- supporting demo assets.

Priority proof coverage does not define asset-set completeness.

---

## 8. Creative Strategy Kernel

Planning produces a formal **Creative Strategy Kernel** before Production starts.

### 8.1 Purpose

The Kernel preserves the high-value strategic reasoning that materially affects creative output while excluding workflow-management noise.

It is the bridge between deep strategy and narrow production.

### 8.2 Minimum fields

```yaml
creative_strategy:
  target_user:
  core_tension:
  core_promise:
  primary_purchase_reasons:
  shopper_barriers:
  reasons_to_believe:
  message_priority:
  japan_implications:
  proof_principles:
  visual_direction:
  visual_anti_patterns:
```

### 8.3 Context projection

This design uses **Context Projection**, not generic context reduction.

The full strategy may be deep and detailed. For each production task, the workflow projects only the relevant strategic subset into the current Asset Packet.

This preserves relevance while reducing context contamination.

---

## 9. Production Handoff

Planning creates one **Production Handoff** at Stage 7/7.5 boundary.

### 9.1 Purpose

It is the formal contract defining what Production must deliver.

### 9.2 Minimum fields

```yaml
production_handoff:
  project:
    market:
    channel:
    locale:
    product:
  page_plan:
    gallery: []
    enhanced_content: []
    other_required_regions: []
  asset_set: []
  source_assets: []
  product_invariants: []
  creative_strategy_ref:
  global_visual_direction: []
  visual_benchmark_refs: []
  prohibited: []
  blocked_assets: []
```

### 9.3 Explicit exclusions

Production Handoff must not contain:

- Stage Completion Manifest history;
- Project State Manifest internals;
- SHA-256 values unless an inherited exact asset is itself a production source;
- auditor reports;
- gate definitions;
- Change Impact Maps;
- full VOC corpus;
- full competitor-research corpus;
- rejected attempt history;
- recovery history;
- long-form module reasoning that has already been resolved.

---

## 10. Production Plane — `listing-production`

Production covers Stage 7.5–8 and answers one question:

> **Produce the approved artifacts.**

### 10.1 Inputs

Production may read only:

- Production Handoff;
- Creative Strategy Kernel;
- current Asset Packet;
- actual source images/files referenced by that packet;
- approved visual benchmarks/patterns.

It should not independently traverse the full conversation history to reinterpret planning decisions.

### 10.2 Production vocabulary

Normal creative-production status is intentionally small:

```text
PLANNED
READY
REVIEW
REVISE
USER_APPROVED
BLOCKED
```

Do not use hardening vocabulary such as `VERIFIED`, `EXACT_RECOVERY_VERIFIED`, `PROVENANCE_CONFLICT`, or physical fingerprint state during ordinary creative work.

### 10.3 Artifact-first behavior

Once Stage 8 starts, the default output should be the artifact itself, not more workflow narration.

Normal flow:

```text
AMZ-G1
→ produce artifact
→ REVIEW
→ user approves/revises
→ AMZ-G2
```

The workflow should not repeatedly output production-plan diagrams, status dashboards, asset maps, or stage summaries unless the user requests them or an exception requires explanation.

### 10.4 Complete-set accountability

Production completion is counted against the required set in Production Handoff.

If Handoff requires 13 final visual assets and 3 are produced, the stage is 3/13 complete. Priority proof coverage cannot promote the stage to complete.

---

## 11. Asset Packet

Each production task receives exactly one Asset Packet.

### 11.1 One Job principle

An Asset Packet has:

- one Asset ID;
- one channel role;
- one primary shopper task/message;
- one final output role;
- one explicit set of source assets/benchmarks.

Gallery and A+ assets with the same topic remain separate jobs unless reuse/derivative behavior was explicitly planned.

### 11.2 Suggested schema

```yaml
asset_id:
role:
  channel:
  region:
  slot:
  asset_type:
objective:
  shopper_task:
  primary_message:
strategy_context:
  consumer_barrier:
  core_tension:
  proof_principle:
evidence:
  allowed: []
  forbidden: []
product_sources:
  required: []
benchmark:
  references: []
  learn_from: []
  reuse_asset: false
composition:
  product_role:
  environment:
  information_density:
  one_image_focus: true
output:
  aspect_ratio:
  final_role:
  quantity: 1
must_preserve: []
must_not_generate: []
```

### 11.3 Benchmark vs reusable asset

The schema must structurally distinguish:

```yaml
benchmark:
  visual_reference: BENCH-01
  reuse_asset: false
```

from:

```yaml
source_asset:
  asset_id: PRIOR-G03
  reuse_asset: true
```

A benchmark communicates creative quality and composition principles. It does not automatically inherit Asset ID, role, approval, slot, or reuse rights.

---

## 12. Production Context Firewall

The production plane requires an explicit context firewall.

### 12.1 Projection pipeline

```text
Full project context
        ↓
Project Brief / Creative Strategy Kernel
        ↓
Production Handoff
        ↓
Current Asset Packet
        ↓
Image-generation / editing prompt
```

### 12.2 Forbidden production-prompt content

Image-generation prompts should not include workflow-management concepts such as:

```text
Stage 8
Asset Registry
Production Plan
Gate
Project State
Checkpoint
Auditor
Change Impact Map
Delivery Parity
```

unless one of those terms is literally consumer-facing creative content, which should be exceptional.

### 12.3 Product identity

When the real product must remain exact, the Asset Packet must explicitly identify the real source asset(s) and prohibit AI reconstruction of geometry, ports, controls, packaging, accessories, UI, or other product evidence.

---

## 13. Visual Patterns, Golden Examples, and Creative QA

Rules alone are insufficient for consistent team output. Production should be guided by reusable examples and patterns.

### 13.1 Visual Pattern Library

The public distribution should include category-neutral patterns such as:

```text
hero-positioning
compact-proof
mechanism-explainer
automation-flow
comparison
installation-decision
ui-proof
```

Each pattern should define:

- when to use it;
- shopper question;
- good composition;
- proof object;
- information-density guidance;
- common failure modes.

### 13.2 Golden Examples

Use anonymized/category-neutral examples showing strong vs weak execution principles.

Examples should teach concepts such as:

- prove compactness through spatial relationship, not only a numeric label;
- explain mechanisms through action → evidence → benefit instead of excessive sci-fi effects;
- keep one dominant shopper decision per Gallery board;
- maintain product prominence and realistic commercial lighting.

Private project visuals must not be copied into the public repository.

### 13.3 Creative QA

Production QA answers:

> Is this a good marketing artifact?

It should evaluate a compact set such as:

1. message clarity;
2. product prominence;
3. visual proof;
4. composition;
5. realism;
6. benchmark/pattern match;
7. channel readiness.

Creative QA is not evidence audit.

---

## 14. User Creative Approval

Creative approval is separate from delivery verification.

When the user approves an asset in Stage 8, record:

```yaml
asset_id:
creative_status: USER_APPROVED
approval_ref:
current_output_ref:
```

This means the creative/marketing output is accepted.

It does **not** mean the file is physically verified, provenance-safe, or locked for final demo consumption.

Formally:

> **Creative Approval ≠ Evidence Verification**

---

## 15. Asset Ledger

Production maintains one simple **Asset Ledger** as its primary state table.

Suggested fields:

| Asset | Role | Status | User decision | Current output ref |
|---|---|---|---|---|

The Ledger should not expose hardening statuses during normal production.

### 15.1 Default review mode

For the first few assets establishing a project's visual language, default to one-asset-at-a-time review.

Batch Production Mode may activate after the user explicitly approves the visual direction and asks to continue in that style.

---

## 16. Production Freeze

Stage 8 ends with a formal **Production Freeze**.

It contains:

```yaml
production_freeze:
  expected_assets:
  user_approved_assets:
  blocked_assets:
  revision_pending:
  approved_output_refs: []
```

The freeze is a creative state boundary. It does not yet assert evidence verification.

Only after the complete required set is creatively approved or explicitly reduced by the user may the workflow enter Hardening.

---

## 17. Hardening Plane — `listing-hardening`

Hardening covers Stage 8.5–10.

It answers:

> **Are the final artifacts safe, exact, channel-correct, and ready to assemble/deliver?**

### 17.1 Inputs

Hardening reads only what it needs:

- Project Brief fields relevant to verification;
- Production Handoff;
- Production Freeze;
- exact final files;
- locked page/module plan;
- frontend reference/capability evidence;
- prior exact-asset approval evidence when relevant.

It does not need rejected creative-attempt history or the full strategy conversation.

### 17.2 Hardening responsibilities

Hardening owns:

- physical fingerprints;
- exact file identity;
- approval binding;
- transform authorization;
- semantic visual-role verification;
- complete required asset-set audit;
- Asset-to-Slot integrity;
- module-plan hash/origin;
- frontend fidelity;
- demo assembly;
- delivery parity;
- final technical/channel QA.

### 17.3 Full evidence audit timing

The mandatory project-wide `listing-evidence-auditor` audit moves to Stage 8.5.

The audit operates on the actual final files produced and approved in Stage 8.

This is the main point where physical SHA, provenance, `VERIFIED`, `HUMAN_APPROVED`, `INVALIDATED`, and related hardening vocabulary become active.

---

## 18. Evidence Auditor

The existing `listing-evidence-auditor` remains a sibling Skill with a narrow trust-boundary responsibility.

It should not be merged into Planning or Production.

### 18.1 Normal invocation

```text
Stage 8.5 → mandatory full audit
```

### 18.2 Early invocation

Planning may call a targeted exact-asset audit only for inherited/reused previously approved assets.

### 18.3 Independence limitation

Loading a Skill in the same Chat does not itself create independent semantic review.

When independent context is unavailable, deterministic file checks may run, but semantic-role evidence remains subject to the existing human/independent-review contract.

---

## 19. Runtime State Model

Conversation history is not the project database.

Use five formal state objects:

1. **Project Brief**
2. **Creative Strategy Kernel**
3. **Production Handoff**
4. **Asset Ledger / Production Freeze**
5. **Delivery State**

### 19.1 Project Brief

Stores stable project execution conclusions such as:

```yaml
project:
offers:
product_truth:
claim_boundaries:
consumer_evidence_sources:
channel_reference:
open_business_decisions:
```

### 19.2 Delivery State

Hardening creates Delivery State with fields such as:

```yaml
physical_sha256:
semantic_role:
approval_binding:
transform_provenance:
slot_binding:
module_plan_hash:
frontend_fidelity:
delivery_parity:
```

This keeps creative-state and delivery-state concerns separate.

---

## 20. State Persistence Strategy

The workflow must work across ChatGPT Web, Custom GPT, Codex, and team handoff scenarios.

### 20.1 Preferred: project workspace files

When supported, persist:

```text
.listing-project/
├── project-brief.yaml
├── creative-strategy.yaml
├── production-handoff.yaml
├── asset-ledger.yaml
└── delivery-state.json
```

### 20.2 Chat fallback: compact state snapshot

When reliable project-file persistence is unavailable, maintain a compact structured state snapshot internally.

Do not display the full snapshot every turn.

User-facing status should remain concise, for example:

```text
G2 approved. Next: G3.
```

The full state is surfaced only when requested or when an exception needs detailed review.

### 20.3 Cross-conversation/team handoff

A new agent or teammate should resume from the formal state objects rather than rereading the entire conversation.

---

## 21. Major Stage Checkpoints

Human review remains a first-class requirement.

### 21.1 Default checkpoint summary

Replace the current verbose Stage Completion Manifest display with:

```text
Done:
Open:
Next:
```

### 21.2 Expanded manifest

Use the full Stage Completion Manifest only when:

- the stage is `PARTIAL`;
- the stage is `BLOCKED`;
- the user requests detailed audit/state review.

This preserves truthful state without turning normal conversations into PMO logs.

---

## 22. Exception-Only Protocols

Some v0.2.6 mechanisms remain important but should load only when triggered.

### 22.1 Change Impact Map

Load only when an authoritative locked input changes materially, such as:

- product/commercial fact;
- offer/page boundary;
- user-approved strategy;
- approved asset/UI source;
- channel capability/reference;
- claim/legal decision.

### 22.2 Recovery Mode

Legacy/corrupted-project recovery procedures must not be part of the normal runtime path.

If retained, they belong in maintainer/exception documentation and load only when explicitly requested.

---

## 23. File/Skill Decomposition

Recommended target structure:

```text
.agents/skills/
├── japan-listing-demo/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
│       ├── routing.md
│       └── exception-routing.md
│
├── listing-planning/
│   ├── SKILL.md
│   ├── references/
│   │   ├── source-authority.md
│   │   ├── market-research.md
│   │   ├── localization.md
│   │   ├── channel-planning.md
│   │   ├── module-fit.md
│   │   └── planning-qa.md
│   └── templates/
│       ├── project-brief.example.yaml
│       ├── creative-strategy.example.yaml
│       └── production-handoff.example.yaml
│
├── listing-production/
│   ├── SKILL.md
│   ├── references/
│   │   ├── visual-production.md
│   │   ├── benchmark-policy.md
│   │   ├── visual-patterns/
│   │   └── production-qa.md
│   └── templates/
│       ├── asset-packet.example.yaml
│       └── asset-ledger.example.yaml
│
├── listing-hardening/
│   ├── SKILL.md
│   ├── references/
│   │   ├── asset-integrity.md
│   │   ├── executable-gates.md
│   │   ├── frontend-fidelity.md
│   │   └── final-qa.md
│   ├── templates/
│   │   └── delivery-state.example.json
│   └── scripts/
│       └── validate_project_state.py
│
└── listing-evidence-auditor/
    └── ... existing auditor ...
```

Exact file moves are implementation details; the architectural requirement is that runtime loading follows these responsibility boundaries.

---

## 24. Current v0.2.6 Content Treatment

### 24.1 Keep always-on, but compress

- workflow stage map;
- Major Stage Checkpoints;
- Transition Command;
- retry budget;
- stage-responsibility boundary;
- context firewall;
- exception routing.

### 24.2 Move to Planning

- source authority;
- Product Truth and Offer Boundary;
- Consumer Strategy;
- Japan market/localization;
- channel capability and frontend-reference planning;
- Message Architecture;
- Gallery/A+ role planning;
- `CONTENT_COVERAGE`;
- `MODULE_FIT_GATE`;
- module budget;
- complete production-asset requirement.

### 24.3 Move to Production

- final visual brief;
- Creative Strategy Kernel projection;
- Visual Benchmark policy;
- visual patterns/golden examples;
- artifact-first production;
- creative QA;
- user creative approval;
- complete-batch accounting.

### 24.4 Move to Hardening

- full Candidate/Verified asset identity machinery;
- SHA/fingerprints;
- approval provenance;
- transform authorization;
- Effective State;
- `ASSET_SLOT_GATE`;
- module plan hash/origin;
- frontend fidelity implementation checks;
- `PRE_DEMO_ASSET_GATE`;
- demo assembly;
- `DELIVERY_PARITY_GATE`;
- final QA.

### 24.5 Exception-only

- Change Impact Map;
- recovery/migration procedures;
- verbose full Stage Completion Manifest.

---

## 25. Team Golden Path

The public workflow should behave as a production system, not as a framework that team members must configure manually.

Default team journey:

```text
Upload product/GTM/source materials
↓
Review Product / Offer / Claim baseline
↓
Review Consumer / Market Strategy
↓
Review Amazon/channel page plan
↓
Review Creative Strategy / complete asset set
↓
Review generated visuals
↓
Review final demo
```

Internal routing, stage-Skill selection, context projection, auditor timing, and validator execution should remain largely invisible.

### 25.1 Team knowledge requirement

A normal Japan marketing teammate should not need to understand:

- prompt engineering;
- Skill architecture;
- evidence-auditor internals;
- physical SHA;
- module plan hashes;
- provenance vocabulary;
- state-machine implementation.

They should make business/creative review decisions, not operate the workflow machinery.

---

## 26. Optional Custom GPT

A Custom GPT may be added as a team-facing UX shell, but it must remain optional.

### 26.1 GPT responsibilities

A possible “Japan Listing Studio” GPT may provide:

- simple onboarding;
- product/channel choice;
- file-upload guidance;
- access to required capabilities such as web/image generation;
- create/resume project entry;
- invocation of `$japan-listing-demo`.

### 26.2 GPT non-responsibilities

Do not duplicate business logic or the full workflow into GPT Instructions.

GitHub-packaged Skills remain the versioned execution source of truth.

Formally:

> **GPT = UX shell**  
> **Skills = execution architecture**  
> **Auditor/scripts = hard verification**

---

## 27. Skills and Context Isolation

Skills are used for responsibility separation and lazy instruction loading, but the design must not assume that Skill invocation creates a fresh/isolated model context.

Therefore the architecture requires explicit context minimization by contract:

- formal handoff objects;
- stage-local references;
- one-job Asset Packets;
- prohibition on reloading full history during Production unless an exception is routed upstream.

Independent semantic evidence audit still follows the auditor's existing isolation/human-review limitations.

---

## 28. Plugins / Apps

Plugins/apps are not core to this redesign.

They may later improve data/asset access, for example:

- GitHub project state;
- design-tool assets;
- approved-asset storage;
- team project handoff.

They do not directly solve production-context contamination and therefore should not block the simplification architecture.

---

## 29. Distribution Requirements

The public distribution should preserve the team's existing simplicity goals:

- one public repository;
- one recommended bundle/install path;
- one normal user invocation: `$japan-listing-demo`;
- internal sibling Skills hidden from ordinary team usage;
- no separate generic-core install requirement;
- no requirement that the user manually invoke Planning/Production/Hardening/Auditor Skills.

The bundle may contain multiple sibling Skills while still presenting one user-facing entry point.

---

## 30. Failure and Routing Semantics

### 30.1 Production discovers missing upstream fact

Production must not infer or silently rewrite strategy.

Return a structured block, for example:

```yaml
status: BLOCKED
missing_field: offer_b_hardware_configuration
return_to: planning
asset_id: AMZ-G6
```

Router performs a targeted Planning reopen, updates the formal state, regenerates only the affected Asset Packet, then returns to Production.

### 30.2 Production artifact repeatedly misses the brief

Retry budget remains maximum two autonomous attempts for the same artifact/problem without new evidence/input.

After that, stop and ask for review rather than generating workflow/status artifacts as substitutes.

### 30.3 Hardening finds wrong or substituted file

Hardening invalidates the affected delivery state and routes only the impacted asset/slot back to Production or Planning according to the cause.

Do not rewrite registries to match the accidental implementation.

---

## 31. Testing Strategy

Implementation should be driven by anonymized regressions that distinguish planning quality, production focus, and hardening integrity.

### 31.1 Router/context tests

- Router loads only the stage-specific Skill for the current stage.
- Transition Command advances without reopening/retrying the current artifact.
- Production prompt does not include gate/auditor/project-state terminology unless explicitly part of consumer content.
- A downstream `BLOCKED` response routes to the correct upstream stage.

### 31.2 Planning tests

- Deep consumer/VOC strategy remains available.
- Stage 7 outputs a complete production asset set, not only P0 visuals.
- Gallery and enhanced-content roles remain separate even for the same topic.
- Full topic coverage does not exceed verified module budget or bypass module-fit reasoning.

### 31.3 Production tests

- One Asset Packet produces one requested final role.
- A visual benchmark is not automatically treated as a reusable final asset.
- A request for one Gallery hero does not produce a workflow/production-plan infographic.
- Product-identity constraints prevent invented product reconstruction.
- Production cannot mark a partial batch complete based only on priority-proof coverage.
- User creative approval is stored as creative approval, not delivery verification.

### 31.4 Hardening tests

Retain v0.2.5/v0.2.6 regressions for:

- module budget;
- exact locked plan origin;
- transform authorization;
- exact-asset approval provenance;
- real-file fingerprinting;
- semantic role mismatch;
- complete required asset set;
- slot integrity;
- delivery parity;
- frontend fidelity.

### 31.5 Team golden-path eval

Add one end-to-end category-neutral eval where a non-expert user:

1. supplies product/GTM materials;
2. reviews planning checkpoints;
3. receives a complete production set;
4. reviews several visual artifacts;
5. reaches hardening and demo without manually invoking internal Skills or understanding governance internals.

---

## 32. Success Criteria

The redesign succeeds when:

1. A normal project can run in one Chat from source intake through demo.
2. Planning remains strategically rich and evidence-based.
3. Production no longer emits workflow-management visuals in place of requested listing assets under the standard path.
4. Stage 8 completion is objectively tied to the complete Production Handoff asset set.
5. A user-provided quality benchmark affects production quality without being silently treated as an approved reusable asset.
6. Gallery/A+ role separation remains intact.
7. User creative approval is immediately persisted and survives stage transitions.
8. Hardening still catches wrong files, unauthorized derivatives, role mismatch, incomplete asset sets, module drift, and demo parity errors.
9. The user normally sees concise checkpoints rather than repeated governance tables.
10. Team members use one public entry point and do not need internal Skill/gate knowledge.
11. A project can be resumed or handed off from structured state rather than full chat-history rereading.
12. Public runtime instructions are materially shorter and less duplicated than v0.2.6.

---

## 33. Migration Principles

Implementation should be a deliberate simplification, not a rule-preserving copy into more files.

1. Start from behavior/regression requirements, not file-by-file migration.
2. Delete duplicated always-on instructions after stage-local ownership is established.
3. Preserve evidence auditor and validator behavior unless a targeted design change explicitly replaces it.
4. Move full-audit timing from mandatory post-6.5 to mandatory Stage 8.5, with targeted early audit for inherited exact assets.
5. Convert normal Stage Completion output to concise `Done / Open / Next` checkpoints.
6. Keep Recovery Mode outside the normal runtime path.
7. Preserve one repository / one user invocation distribution.
8. Do not add a Custom GPT as an implementation dependency; treat it as a later optional team UX layer.

---

## 34. Design Summary

The current workflow became less controllable because strategy, production, governance, and evidence hardening all remained active in one long-running context.

The solution is not to remove strategy or weaken QA. It is to separate execution responsibilities and project only the information relevant to the active job.

The redesigned system therefore uses:

```text
Deep Planning
→ Project Brief
→ Creative Strategy Kernel
→ Production Handoff
→ One-job Asset Packet
→ Artifact-first Production
→ User Creative Approval
→ Production Freeze
→ Evidence Hardening
→ Demo Assembly
```

The workflow remains strategically deep, creatively focused, delivery-safe, and team-reusable while dramatically reducing control-plane contamination during production.
