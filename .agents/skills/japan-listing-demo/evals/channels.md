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
