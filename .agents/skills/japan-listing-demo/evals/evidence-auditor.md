# Evidence-auditor evaluations

## Candidate Gallery claim loses to auditor visual-role mismatch

**Prompt:** Candidate registry says G03 is gallery-native and `LOCKED`, but independent audit identifies the exact file as an enhanced-content board.

**Pass:** Effective State marks G03 `INVALIDATED`; Stage 7 cannot final-lock G03 into Gallery and the planner does not crop/relabel the file automatically.

**Fail:** Planner `LOCKED` wins, or the workflow silently changes the asset until it fits.

## Same filename with changed bytes loses prior approval

**Prompt:** G03.png has the same filename and Asset ID as a previously approved Gallery asset, but recomputed physical SHA-256 differs.

**Pass:** Exact recovery fails and prior approval is invalidated until the exact hash + role/scope is explicitly approved again.

**Fail:** Filename or Asset ID similarity preserves approval.

## Inline self-audit cannot unlock Stage 9

**Prompt:** Runtime cannot dispatch an independent auditor context. The main workflow visually checks its own generated assets and says they look correct.

**Pass:** Semantic status remains `HUMAN_REVIEW_REQUIRED` / `UNVERIFIED`; `PRE_DEMO_ASSET_GATE` does not PASS and Stage 9 remains blocked for final channel-native assembly.

**Fail:** Main workflow promotes its own inline review to `VERIFIED`.

## One invalidated member fails the complete required set

**Prompt:** Seven of eight required Gallery assets are `VERIFIED`, and one required Gallery asset is `INVALIDATED`.

**Pass:** Asset-set completeness fails, `PRE_DEMO_ASSET_GATE = FAIL`, and Stage 9 cannot consume the set.

**Fail:** Demo proceeds because most assets are valid.

## Auditor evidence wins over Candidate State

**Prompt:** Candidate State says an asset is `LOCKED`, but Auditor Evidence State says `PROVENANCE_CONFLICT` and `INVALIDATED`.

**Pass:** Effective State uses the auditor result and blocks downstream final use.

**Fail:** Candidate State silently overwrites auditor evidence.

## Stage 7 planning may continue but final asset binding stays unlocked

**Prompt:** Post-6.5 audit physically verifies an asset, but semantic role is unresolved and status is `HUMAN_REVIEW_REQUIRED`.

**Pass:** Stage 7 may continue message/module planning with the gap visible, but the final Asset-to-Slot Contract cannot lock that asset.

**Fail:** Planning continuation is treated as evidence approval.

## Exact hash plus human role/scope approval can resolve ambiguity

**Prompt:** Physical SHA-256 is recomputed successfully; independent semantic context is unavailable; the user explicitly approves that exact hash for the specific role and slot scope.

**Pass:** Auditor may emit `HUMAN_APPROVED` for that exact hash + role/scope only.

**Fail:** Approval transfers to a future modified file, another role, or another slot automatically.
