# Channel evaluations

## Rakuten project must not inherit Amazon modules

**Prompt:** Plan a Rakuten product page after completing an Amazon.co.jp project.

**Pass:** The agent loads the Rakuten profile, verifies current editable areas and store capabilities, and maps messages to those slots. Amazon-specific module names and limits do not carry over.

**Fail:** The agent plans Premium A+, Amazon bullets, or Amazon comparison modules for Rakuten.

## Unknown channel capability

**Prompt:** The merchant cannot confirm whether a channel feature is enabled.

**Pass:** The agent records the capability as `UNKNOWN` or `PENDING`, continues unaffected work, and prevents unsupported modules from entering final production.

**Fail:** The agent infers account access from a competitor page or another marketplace.

## Yahoo! Shopping project

**Prompt:** Create a Japan-market listing plan for Yahoo! Shopping with only a product brief and no current template capture.

**Pass:** The agent requests or captures the current store/template structure before locking page modules, while still allowing Fact Lock and Consumer Strategy to proceed.

**Fail:** The agent treats Yahoo! Shopping as Amazon or assumes a fixed editable page layout.

## Retailer PDP

**Prompt:** A Japanese retailer controls most of the PDP template and only accepts a limited brand-content package.

**Pass:** The agent separates retailer-controlled and brand-controlled regions and plans only the confirmed editable slots.

**Fail:** The agent designs a full DTC page or attributes retailer-generated content to the brand.

## Amazon channel-native demo requires frontend reference intake

**Prompt:** “Amazon.co.jp 的视觉已经确认了。现在生成最终 Listing Demo。” No PDP reference URL or ASIN has been supplied.

**Pass:** Before Stage 9, the agent checks whether the user has a preferred current Amazon.co.jp reference URL or ASIN. If the user has one, it becomes the primary frontend-fidelity reference. If the user has none, the agent researches 1–3 current comparable Amazon.co.jp PDPs, selects a primary reference with reasons, captures the consumer-facing frontend structure, and presents the resulting Channel Frontend Reference Pack at the Stage 5.5 checkpoint before the demo is assembled.

**Fail:** The agent skips reference intake and invents an Amazon-like branded website shell from memory.

## User-provided frontend reference has priority

**Prompt:** “参考这个 Amazon.co.jp 商品页来做 Demo：https://www.amazon.co.jp/dp/EXAMPLE”

**Pass:** The supplied URL is recorded as the Primary Reference. The agent inspects the live consumer-facing page to the extent accessible, separates direct visual evidence from inferred structure, and uses secondary references only to fill explicitly identified gaps. It does not replace the user's reference with a more convenient competitor page without explaining why.

**Fail:** The agent ignores the supplied page and designs from generic Amazon knowledge or another reference.

## Platform rules are not frontend visual evidence

**Prompt:** Official Amazon documentation confirms title, images, variations, bullets, featured offer, and A+ capabilities, but no live PDP frontend has been inspected.

**Pass:** The agent records official guidance as Platform Capability evidence only. Frontend fidelity remains `PARTIAL` or `UNKNOWN` until a current consumer-facing PDP is visually inspected or an approved visual capture is supplied.

**Fail:** The agent treats Seller Central documentation as sufficient proof of the current desktop/mobile frontend layout and generates a high-fidelity PDP demo anyway.

## Frontend Fidelity Gate blocks invented channel shells

**Prompt:** Stage 8 visuals are approved. Stage 9 is about to assemble an Amazon.co.jp PDP demo, but desktop shell, mobile shell, section order, and A+ placement have no visual evidence.

**Pass:** `FRONTEND_FIDELITY_GATE` fails for a channel-native PDP demo. The agent may deliver a clearly named `Content Review Demo` using approved content, but it must not label the result an Amazon PDP Demo or fabricate Amazon navigation, cards, tabs, or layout. It lists the missing evidence needed to unlock the native demo.

**Fail:** The agent creates a custom header, branded navigation, rounded-card layout, or other generic ecommerce shell and calls it an Amazon PDP Demo.

## Channel-native demo shell comes from reference evidence

**Prompt:** A current Amazon.co.jp Primary Reference has been visually captured and the project visuals are approved.

**Pass:** Stage 9 first reproduces the verified channel shell and section order, then places approved project content into the verified brand-controlled slots. Amazon-controlled regions are represented as platform-owned structure/placeholders rather than redesigned marketing modules. Review Mode is an overlay and does not alter the consumer-facing channel layout.

**Fail:** Stage 9 treats the demo as a blank web-design canvas or exposes internal IA/module labels as the consumer-facing page structure.

## Non-Amazon channel-native demos use the same reference contract

**Prompt:** Generate a Rakuten or retailer-PDP native demo after content planning, with no current frontend reference.

**Pass:** The agent applies the same Channel Frontend Reference Pack and Frontend Fidelity Gate using that channel's current consumer-facing reference, without importing Amazon anatomy.

**Fail:** The agent assumes only Amazon needs frontend-reference research or reuses an Amazon shell for another channel.
