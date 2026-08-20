# Production Context Firewall Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the `listing-production` sibling Skill so Stage 7.5–8 turns approved strategy into focused final artifacts using one-job Asset Packets, a context firewall, creative QA, and complete-set accounting instead of narrating workflow management.

**Architecture:** Production receives only the Creative Strategy Kernel, Production Handoff, current Asset Packet, referenced source assets, and visual benchmarks/patterns. A deterministic projection helper validates the packet and renders a production-only generation context that excludes control-plane fields. Production keeps a small creative status vocabulary, persists user creative approval in an Asset Ledger, and creates a Production Freeze only when the complete required set is approved or explicitly reduced. It does not perform physical-file hardening or delivery verification.

**Tech Stack:** Markdown Skill contracts, YAML examples, Python 3.12 standard library (`json`, `pathlib`, `re`, `argparse`) for packet/state validation and self-tests, existing image-generation capability at runtime.

**Spec:** `docs/superpowers/specs/2026-08-20-creative-first-hardening-architecture-design.md`

## Global Constraints

- This plan assumes the Planning Foundation plan has been implemented first and the canonical inputs are `creative-strategy.yaml` and `production-handoff.yaml`.
- One Asset Packet represents exactly one final Asset ID, one channel role, one primary shopper task/message, and one output quantity of 1 by default.
- Gallery and enhanced-content assets remain separate production jobs even when they communicate the same topic, unless explicit reuse/derivative intent was planned upstream.
- Visual benchmarks communicate quality/composition direction; they do not become reusable final assets unless `reuse_asset: true` is explicit on a source asset.
- Production prompts/contexts must not contain workflow control-plane fields or narration.
- Production vocabulary is limited to `PLANNED`, `READY`, `REVIEW`, `REVISE`, `USER_APPROVED`, `BLOCKED`.
- `USER_APPROVED` means creative/marketing approval only; it never means `VERIFIED`, `LOCKED`, or physically audited.
- Stage 8 completion is measured against the complete `asset_set` from Production Handoff.
- Production must return a structured `BLOCKED` result when an upstream fact/decision is missing; it must not infer or rewrite Planning.
- Product geometry/UI/packaging/ports/controls/accessories must not be AI-reconstructed when exact real assets are required.
- Public examples and visual patterns remain category-neutral and contain no private project data.
- `VERSION` remains `0.2.6` in this slice; release integration happens later.

---

## File Structure

### New Production Skill

- Create `.agents/skills/listing-production/SKILL.md` — Stage 7.5–8 boundary, artifact-first behavior, creative statuses, block/return semantics.
- Create `.agents/skills/listing-production/agents/openai.yaml` — production-only prompt.
- Create `.agents/skills/listing-production/references/visual-production.md` — Asset Packet execution and product identity rules.
- Create `.agents/skills/listing-production/references/benchmark-policy.md` — benchmark vs reuse semantics.
- Create `.agents/skills/listing-production/references/production-qa.md` — compact seven-dimension Creative QA.
- Create `.agents/skills/listing-production/references/visual-patterns/hero-positioning.md`.
- Create `.agents/skills/listing-production/references/visual-patterns/compact-proof.md`.
- Create `.agents/skills/listing-production/references/visual-patterns/mechanism-explainer.md`.
- Create `.agents/skills/listing-production/references/visual-patterns/automation-flow.md`.
- Create `.agents/skills/listing-production/references/visual-patterns/comparison.md`.
- Create `.agents/skills/listing-production/references/visual-patterns/installation-decision.md`.
- Create `.agents/skills/listing-production/references/visual-patterns/ui-proof.md`.
- Create `.agents/skills/listing-production/references/golden-examples.md` — anonymized strong/weak principles in text form.
- Create `.agents/skills/listing-production/templates/asset-packet.example.yaml`.
- Create `.agents/skills/listing-production/templates/asset-ledger.example.yaml`.
- Create `.agents/skills/listing-production/templates/production-freeze.example.yaml`.
- Create `.agents/skills/listing-production/scripts/project_asset_packet.py` — validate and project an Asset Packet into production-only context.
- Create `.agents/skills/listing-production/scripts/production_state.py` — creative status transitions and freeze completeness.
- Create `.agents/skills/listing-production/scripts/selftest_production.py` — regression suite.
- Create `.agents/skills/listing-production/evals/production.md` — behavior scenarios.

### Existing files touched in this slice

- Modify `.github/workflows/validate-japan-listing-demo.yml` — run Production self-tests after Planning self-tests.
- Do not switch the public router or release packaging yet.

---

### Task 1: Establish the Production Skill and artifact-first boundary

**Files:**
- Create: `.agents/skills/listing-production/scripts/selftest_production.py`
- Create: `.agents/skills/listing-production/SKILL.md`
- Create: `.agents/skills/listing-production/agents/openai.yaml`

**Interfaces:**
- Skill name: `listing-production`.
- Owns Stage `7.5` and `8` only.
- Consumes `Production Handoff`, `Creative Strategy Kernel`, current `Asset Packet`, source assets, benchmarks/patterns.
- Returns an artifact plus creative status or a structured upstream block.

- [ ] **Step 1: Write the failing boundary tests**

Create `selftest_production.py`:

```python
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_production_skill_is_artifact_first() -> None:
    text = read(SKILL_DIR / "SKILL.md").casefold()
    for phrase in [
        "name: listing-production", "stage 7.5", "stage 8",
        "artifact-first", "one asset packet", "user_approved",
    ]:
        assert phrase in text
    for forbidden in [
        "exact_recovery_verified", "provenance_conflict",
        "pre_demo_asset_gate", "delivery_parity_gate",
    ]:
        assert forbidden not in text


def test_production_has_small_status_vocabulary() -> None:
    text = read(SKILL_DIR / "SKILL.md")
    for status in ["PLANNED", "READY", "REVIEW", "REVISE", "USER_APPROVED", "BLOCKED"]:
        assert status in text
    assert "Creative Approval ≠ Evidence Verification" in text


def main() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
    print(f"PASS: {len(tests)} listing-production boundary tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Run and verify RED**

```bash
python .agents/skills/listing-production/scripts/selftest_production.py
```

Expected: FAIL with missing `listing-production/SKILL.md`.

- [ ] **Step 3: Create minimal Production Skill**

`SKILL.md` must contain the explicit mode switch:

```markdown
---
name: listing-production
description: Use when producing Stage 7.5–8 listing assets from an approved Production Handoff and one-job Asset Packets.
---

# Listing Production

## Core question
Produce the approved artifacts.

## Plane boundary
This Skill owns Stage 7.5–8. It does not reinterpret Planning and does not perform final physical-file hardening.

## Artifact-first mode
Once production starts, the default response is the requested artifact, followed by a concise creative status. Do not substitute a workflow diagram, asset map, production plan, or status board for the requested final asset.

## Creative status
PLANNED / READY / REVIEW / REVISE / USER_APPROVED / BLOCKED

Creative Approval ≠ Evidence Verification.

## One-job rule
Execute one Asset Packet at a time unless the user explicitly enables a batch after approving the visual direction.
```

Use a short `agents/openai.yaml` that says to consume only the formal production inputs and produce the artifact directly.

- [ ] **Step 4: Run and verify GREEN**

Expected:

```text
PASS: 2 listing-production boundary tests
```

- [ ] **Step 5: Commit**

```bash
git add .agents/skills/listing-production/SKILL.md \
        .agents/skills/listing-production/agents/openai.yaml \
        .agents/skills/listing-production/scripts/selftest_production.py
git commit -m "feat: add focused listing production skill"
```

---

### Task 2: Implement the one-job Asset Packet validator and context projection

**Files:**
- Create: `.agents/skills/listing-production/templates/asset-packet.example.yaml`
- Create: `.agents/skills/listing-production/scripts/project_asset_packet.py`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`

**Interfaces:**
- `validate_asset_packet(packet: dict) -> list[str]`
- `project_generation_context(packet: dict) -> dict`
- The projected context includes only creative-production fields and never includes governance fields.

- [ ] **Step 1: Add failing Asset Packet tests**

Append:

```python
import json
import sys
sys.path.insert(0, str(SKILL_DIR / "scripts"))
from project_asset_packet import validate_asset_packet, project_generation_context


def base_packet() -> dict:
    return {
        "asset_id": "AMZ-G1",
        "role": {"channel": "amazon-jp", "region": "gallery", "slot": "G1", "asset_type": "gallery-native"},
        "objective": {"shopper_task": "understand the core purchase reason", "primary_message": "Compact performance"},
        "strategy_context": {"consumer_barrier": "small can feel basic", "core_tension": "compact vs capability", "proof_principle": "show spatial proof"},
        "evidence": {"allowed": ["confirmed size"], "forbidden": ["unsupported superlative"]},
        "product_sources": {"required": ["SRC-P01"]},
        "benchmark": {"references": ["BENCH-01"], "learn_from": ["product prominence"], "reuse_asset": False},
        "composition": {"product_role": "hero", "environment": "residential", "information_density": "low", "one_image_focus": True},
        "output": {"aspect_ratio": "1:1", "final_role": "Amazon Gallery", "quantity": 1},
        "must_preserve": ["product geometry"],
        "must_not_generate": ["workflow diagram", "fictional product structure"],
    }


def test_one_job_packet_passes() -> None:
    assert validate_asset_packet(base_packet()) == []


def test_multiple_asset_ids_fail_one_job_rule() -> None:
    packet = base_packet()
    packet["asset_id"] = ["AMZ-G1", "AMZ-G2"]
    errors = validate_asset_packet(packet)
    assert any("one asset_id" in e for e in errors)


def test_quantity_above_one_requires_batch_outside_asset_packet() -> None:
    packet = base_packet()
    packet["output"]["quantity"] = 3
    errors = validate_asset_packet(packet)
    assert any("quantity must be 1" in e for e in errors)


def test_projection_drops_control_plane_fields() -> None:
    packet = base_packet()
    packet["project_state_manifest"] = {"declared_gate_results": {"X": "PASS"}}
    packet["stage_completion_manifest"] = {"status": "COMPLETE"}
    projected = project_generation_context(packet)
    encoded = json.dumps(projected, ensure_ascii=False).casefold()
    for forbidden in ["project_state_manifest", "declared_gate_results", "stage_completion_manifest", "delivery_parity"]:
        assert forbidden not in encoded
```

- [ ] **Step 2: Run and verify RED**

Expected: import failure because `project_asset_packet.py` does not exist.

- [ ] **Step 3: Implement validation and projection**

Use explicit allow-list projection rather than blacklist-only sanitization:

```python
REQUIRED_TOP_LEVEL = {
    "asset_id", "role", "objective", "strategy_context", "evidence",
    "product_sources", "benchmark", "composition", "output",
    "must_preserve", "must_not_generate",
}


def validate_asset_packet(packet: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(packet.get("asset_id"), str) or not packet.get("asset_id"):
        errors.append("Asset Packet requires exactly one asset_id string")
    if packet.get("output", {}).get("quantity") != 1:
        errors.append("Asset Packet output quantity must be 1; batch control belongs outside the packet")
    if packet.get("composition", {}).get("one_image_focus") is not True:
        errors.append("one_image_focus must be true")
    missing = sorted(REQUIRED_TOP_LEVEL - set(packet))
    errors.extend(f"missing field: {name}" for name in missing)
    return errors


def project_generation_context(packet: dict) -> dict:
    errors = validate_asset_packet(packet)
    if errors:
        raise ValueError("; ".join(errors))
    keys = [
        "asset_id", "role", "objective", "strategy_context", "evidence",
        "product_sources", "benchmark", "composition", "output",
        "must_preserve", "must_not_generate",
    ]
    return {key: packet[key] for key in keys}
```

Add a CLI that accepts JSON input/output for deterministic testing. YAML remains the human-readable template; runtime agents may construct the equivalent dict directly.

- [ ] **Step 4: Create the category-neutral Asset Packet example**

The example must clearly distinguish:

```yaml
benchmark:
  references: [BENCH-01]
  learn_from: [composition, lighting, hierarchy]
  reuse_asset: false
```

from `product_sources.required` or an explicitly reusable prior source asset.

- [ ] **Step 5: Run and verify GREEN**

Expected: all Asset Packet tests PASS.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/listing-production/templates/asset-packet.example.yaml \
        .agents/skills/listing-production/scripts
git commit -m "feat: add one-job production context projection"
```

---

### Task 3: Add Asset Ledger, creative approval persistence, and Production Freeze accounting

**Files:**
- Create: `.agents/skills/listing-production/templates/asset-ledger.example.yaml`
- Create: `.agents/skills/listing-production/templates/production-freeze.example.yaml`
- Create: `.agents/skills/listing-production/scripts/production_state.py`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`

**Interfaces:**
- `set_creative_status(ledger: dict, asset_id: str, status: str, output_ref: str | None = None, approval_ref: str | None = None) -> dict`
- `production_progress(handoff: dict, ledger: dict) -> dict`
- `build_production_freeze(handoff: dict, ledger: dict) -> dict`
- A freeze is ready only when every required asset is `USER_APPROVED` or explicitly excluded by user-approved reduced scope represented upstream.

- [ ] **Step 1: Add failing state tests**

```python
from production_state import set_creative_status, production_progress, build_production_freeze


def test_user_approval_is_creative_only() -> None:
    ledger = {"assets": {"AMZ-G1": {"status": "REVIEW"}}}
    updated = set_creative_status(ledger, "AMZ-G1", "USER_APPROVED", "file:g1", "chat:approval-1")
    row = updated["assets"]["AMZ-G1"]
    assert row["status"] == "USER_APPROVED"
    assert row["current_output_ref"] == "file:g1"
    assert "VERIFIED" not in json.dumps(row)


def test_three_of_thirteen_is_not_complete() -> None:
    handoff = {"asset_set": [{"asset_id": f"A{i}"} for i in range(13)]}
    ledger = {"assets": {f"A{i}": {"status": "USER_APPROVED"} for i in range(3)}}
    progress = production_progress(handoff, ledger)
    assert progress == {"expected": 13, "approved": 3, "remaining": 10, "complete": False}


def test_freeze_refuses_revision_pending_asset() -> None:
    handoff = {"asset_set": [{"asset_id": "A1"}, {"asset_id": "A2"}]}
    ledger = {"assets": {"A1": {"status": "USER_APPROVED", "current_output_ref": "file:a1"}, "A2": {"status": "REVISE"}}}
    freeze = build_production_freeze(handoff, ledger)
    assert freeze["ready_for_hardening"] is False
    assert freeze["revision_pending"] == ["A2"]
```

- [ ] **Step 2: Run and verify RED**

Expected: import failure because `production_state.py` does not exist.

- [ ] **Step 3: Implement creative-state transitions**

```python
ALLOWED_STATUSES = {"PLANNED", "READY", "REVIEW", "REVISE", "USER_APPROVED", "BLOCKED"}


def set_creative_status(ledger, asset_id, status, output_ref=None, approval_ref=None):
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"invalid creative status: {status}")
    result = json.loads(json.dumps(ledger))
    row = result.setdefault("assets", {}).setdefault(asset_id, {})
    row["status"] = status
    if output_ref is not None:
        row["current_output_ref"] = output_ref
    if approval_ref is not None:
        row["approval_ref"] = approval_ref
    return result
```

`production_progress` must compare exact `asset_id` membership from Handoff against ledger `USER_APPROVED` status.

`build_production_freeze` returns:

```json
{
  "expected_assets": 13,
  "user_approved_assets": [],
  "blocked_assets": [],
  "revision_pending": [],
  "approved_output_refs": [],
  "ready_for_hardening": false
}
```

- [ ] **Step 4: Create example Ledger and Freeze templates**

Examples must use only creative statuses; do not include SHA, provenance, or delivery verification fields.

- [ ] **Step 5: Run and verify GREEN**

Expected: all Production state tests PASS.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/listing-production/templates \
        .agents/skills/listing-production/scripts
git commit -m "feat: persist creative approvals and production freeze"
```

---

### Task 4: Add Visual Pattern Library, benchmark policy, golden examples, and Creative QA

**Files:**
- Create: `.agents/skills/listing-production/references/visual-production.md`
- Create: `.agents/skills/listing-production/references/benchmark-policy.md`
- Create: `.agents/skills/listing-production/references/production-qa.md`
- Create: `.agents/skills/listing-production/references/golden-examples.md`
- Create: `.agents/skills/listing-production/references/visual-patterns/hero-positioning.md`
- Create: `.agents/skills/listing-production/references/visual-patterns/compact-proof.md`
- Create: `.agents/skills/listing-production/references/visual-patterns/mechanism-explainer.md`
- Create: `.agents/skills/listing-production/references/visual-patterns/automation-flow.md`
- Create: `.agents/skills/listing-production/references/visual-patterns/comparison.md`
- Create: `.agents/skills/listing-production/references/visual-patterns/installation-decision.md`
- Create: `.agents/skills/listing-production/references/visual-patterns/ui-proof.md`
- Modify: `.agents/skills/listing-production/scripts/selftest_production.py`
- Create: `.agents/skills/listing-production/evals/production.md`

**Interfaces:**
- Production selects a visual pattern by shopper task/evidence need, not by product category name.
- Creative QA evaluates exactly: message clarity, product prominence, visual proof, composition, realism, benchmark/pattern match, channel readiness.

- [ ] **Step 1: Add failing pattern/QA tests**

```python
def test_visual_pattern_library_is_complete() -> None:
    names = [
        "hero-positioning.md", "compact-proof.md", "mechanism-explainer.md",
        "automation-flow.md", "comparison.md", "installation-decision.md", "ui-proof.md",
    ]
    for name in names:
        text = read(SKILL_DIR / "references" / "visual-patterns" / name).casefold()
        for phrase in ["when to use", "shopper question", "good composition", "proof object", "information density", "common failure"]:
            assert phrase in text, (name, phrase)


def test_creative_qa_has_seven_dimensions_and_no_hardening_terms() -> None:
    text = read(SKILL_DIR / "references" / "production-qa.md").casefold()
    for phrase in [
        "message clarity", "product prominence", "visual proof", "composition",
        "realism", "benchmark", "channel readiness",
    ]:
        assert phrase in text
    for forbidden in ["sha-256", "exact recovery", "delivery parity"]:
        assert forbidden not in text


def test_benchmark_policy_separates_reference_from_reuse() -> None:
    text = read(SKILL_DIR / "references" / "benchmark-policy.md").casefold()
    assert "benchmark" in text and "reuse" in text
    assert "does not automatically" in text
```

- [ ] **Step 2: Run and verify RED**

Expected: FAIL because references/patterns do not exist.

- [ ] **Step 3: Write the pattern library and benchmark policy**

Each pattern uses the exact section labels expected by the tests. Keep examples category-neutral. `golden-examples.md` should show strong/weak text-described compositions, for example:

```text
Weak compact proof: a tiny product in a huge room plus a "compact" label.
Strong compact proof: a controlled spatial relationship where furniture clearance itself proves the size claim.
```

Do not include private brand/product names or images.

- [ ] **Step 4: Write Production QA and visual-production rules**

`visual-production.md` must state:

```text
- Product source is authoritative for product identity.
- AI may generate environment, lighting, and approved explanatory layers.
- One final asset must solve one dominant shopper task.
- If the Asset Packet is BLOCKED by a missing upstream fact, return the block; do not invent the fact.
- After two failed autonomous attempts for the same asset/problem, stop and request review.
```

- [ ] **Step 5: Add anonymized eval scenarios**

Include scenarios named exactly:

```text
One Gallery hero request must not become a production-plan infographic
Benchmark is quality reference, not reusable final asset
Priority proof cannot complete a partial production set
Gallery and enhanced-content jobs stay separate
Missing upstream fact returns BLOCKED instead of invention
User creative approval does not become VERIFIED
```

- [ ] **Step 6: Run and verify GREEN**

Expected: all Production tests PASS.

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/listing-production/references \
        .agents/skills/listing-production/evals \
        .agents/skills/listing-production/scripts/selftest_production.py
git commit -m "feat: add creative patterns and production qa"
```

---

### Task 5: Add Production self-tests to CI while preserving the current public runtime

**Files:**
- Modify: `.github/workflows/validate-japan-listing-demo.yml`

**Interfaces:**
- CI order: Planning self-test → Production self-test → existing Auditor/Project State/packaging checks.

- [ ] **Step 1: Verify Production is not yet in CI**

```bash
grep -n "selftest_production.py" .github/workflows/validate-japan-listing-demo.yml
```

Expected: no match.

- [ ] **Step 2: Add Production self-test**

```yaml
      - run: python .agents/skills/listing-production/scripts/selftest_production.py
```

- [ ] **Step 3: Run complete local regression sequence**

```bash
python .agents/skills/listing-planning/scripts/selftest_planning.py
python .agents/skills/listing-production/scripts/selftest_production.py
python .agents/skills/listing-evidence-auditor/scripts/selftest_auditor.py
python .agents/skills/japan-listing-demo/scripts/selftest_project_state_validator.py
python .agents/skills/japan-listing-demo/scripts/validate_overlay.py
python .agents/skills/japan-listing-demo/scripts/package_skill.py
python scripts/package_codex_bundle.py
```

Expected: all exit 0; public v0.2.6 router/package behavior is still unchanged in this intermediate slice.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/validate-japan-listing-demo.yml
git commit -m "test: validate focused production skill"
```

---

## Plan Self-Review Checklist

Before implementation review, verify:

- Spec §§10–16, 24.3, 30.1–30.2, 31.3, 32 are fully represented above.
- The projected generation context uses an allow-list rather than passing full project state through a filter.
- `USER_APPROVED` never maps to delivery verification.
- Complete-set accounting compares exact Handoff Asset IDs to Ledger state.
- Benchmark policy cannot silently convert a reference into a reusable asset.
- Visual patterns are category-neutral and contain no private project data.
- No Hardening vocabulary is required for normal Production operation.
- Existing v0.2.6 regressions still pass.
- Verify this plan contains no placeholder markers:

```bash
python - <<'PY'
from pathlib import Path
p = Path('docs/superpowers/plans/2026-08-20-production-context-firewall.md')
text = p.read_text(encoding='utf-8').upper()
for marker in ['TO' + 'DO', 'T' + 'BD', 'FIX' + 'ME']:
    assert marker not in text, marker
print('PASS: no placeholder markers')
PY
```
