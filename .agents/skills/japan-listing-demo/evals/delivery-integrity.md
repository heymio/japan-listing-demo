# Delivery-integrity evaluations

These cases are anonymized from real project failures. They test workflow behavior without carrying product-private facts into the public Skill.

## Stage Completion Manifest blocks false completion

**Prompt:** A visual-production stage planned 8 gallery assets, 7 enhanced-content modules, 1 brand-story asset, and 1 storyboard. Eight gallery assets are complete, but none of the enhanced-content modules, brand-story asset, or storyboard exists yet.

**Pass:** The stage emits a **Stage Completion Manifest** showing planned versus completed counts, open items, blockers, and `STAGE_STATUS = PARTIAL`. It does not say the stage or visual production is complete.

**Fail:** The agent treats the completed gallery batch as completion of the whole visual-production stage.

## Approved asset cannot be silently replaced downstream

**Prompt:** Eight gallery-native assets were reviewed and approved. During Demo Assembly, an enhanced-content landscape asset appears visually convenient for Gallery slot 3.

**Pass:** Demo Assembly reuses the exact approved gallery asset bound to Gallery slot 3. If a different source or derivative is needed, the agent records a new derivative, explains the reason, and requests explicit approval before replacing the locked asset.

**Fail:** The agent crops, resizes, or substitutes the enhanced-content asset and presents it as the approved gallery image.

## Asset-to-Slot Contract rejects cross-slot asset leakage

**Prompt:** A slot contract marks an asset as `allowed_slots = enhanced-content` and another slot requires a `gallery-native` asset with a square target ratio.

**Pass:** `ASSET_SLOT_GATE = FAIL` when the enhanced-content asset is mapped into the gallery slot. The issue is surfaced before demo assembly.

**Fail:** The demo builder crops the asset until it visually fits and proceeds.

## Topic coverage does not prove module fit

**Prompt:** An enhanced-content plan covers all 10 planned message topics, but the implementation proposes to turn ten previously designed static boards into a carousel simply by slicing or grouping them.

**Pass:** The agent reports `CONTENT_COVERAGE = PASS` but `MODULE_FIT_GATE = FAIL` unless the verified native module, message grouping, interaction purpose, and evidence structure justify the carousel. Coverage and module fit are evaluated separately.

**Fail:** The agent declares the plan complete because all topics are present.

## Native interaction is planned before production

**Prompt:** A verified channel supports a carousel. The existing assets were designed as independent static boards with no slide-level narrative, navigation logic, or shared interaction purpose.

**Pass:** The agent redesigns the module plan and visual brief for the carousel before production, or selects a better verified native module. It does not retrofit the static boards into a carousel only during demo assembly.

**Fail:** Stage 9 mechanically converts static boards into slides to imitate a native interaction.

## Planned-to-Implemented Parity Gate catches missing interaction

**Prompt:** The locked module plan contains a carousel, a hotspot module, and a comparison module. The demo renders all three as static images.

**Pass:** `DELIVERY_PARITY_GATE = FAIL`. The parity check compares planned slot/module, interaction, source asset IDs, dimensions, and message coverage against implementation before the demo can be called complete.

**Fail:** The HTML opens successfully, so the agent declares the demo complete.

## P0 differentiator requires visual proof

**Prompt:** Consumer Strategy identifies one P0 purchase reason as the primary product differentiator, but all final visuals only show generic lifestyle context and never directly demonstrate or evidence that differentiator.

**Pass:** `DIFFERENTIATOR_PROOF_GATE = FAIL` or remains open. At least one priority visual must provide direct evidence, or the user must explicitly approve an alternative proof strategy.

**Fail:** The visual batch passes because each individual image is attractive and loosely relevant.

## Asset Readiness Preflight happens before late visual discovery

**Prompt:** The workflow knows that later stages will require real product render, UI evidence, channel-native gallery assets, and enhanced-content assets, but these inputs have not been checked yet.

**Pass:** Stage 1 records an **Asset Readiness Preflight** with required, received, missing, provisional, and blocking asset classes before downstream planning depends on them.

**Fail:** The workflow waits until Stage 8 or Stage 9 to discover that critical real assets were never supplied.

## Authoritative change reopens only impacted work

**Prompt:** After several stages are locked, a newer authoritative product fact invalidates one offer assumption and several dependent messages, but not unrelated market research or unaffected assets.

**Pass:** The agent creates a **Change Impact Map**, marks affected outputs `INVALIDATED` or `REOPEN`, preserves unaffected locked outputs, and reruns only the dependent stages/items.

**Fail:** The agent either ignores the new fact because the stage was locked or restarts the whole project without dependency analysis.
