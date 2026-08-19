# Cross-category evaluations

## Category conclusions must not leak across projects

**Prompt:** First complete a Japan project for one product category. Then start a second Japan project in a different category with no shared VOC.

**Pass:** The second project starts with a clean category evidence state. Only generic Japan overlay rules, selected channel rules, and current project evidence carry forward.

**Fail:** The second project inherits the first category's scenarios, objections, keywords, message priorities, proof objects, or visual environment.

## Category overlay is optional

**Prompt:** A new category has no reusable overlay yet.

**Pass:** The agent proceeds from project documents, VOC, research, and competitor evidence while recording assumptions and gaps. It does not create a category profile from one project without review.

**Fail:** The agent stops the full workflow or promotes one project's findings into reusable category truth.

## Visual localization is evidence-led

**Prompt:** Create a Japan-market visual brief without project-specific use context.

**Pass:** The agent requests or researches the actual user, use environment, channel, category, and offer. It treats any proposed environment or casting as provisional.

**Fail:** The agent inserts a fixed national lifestyle scene as an established market rule.
