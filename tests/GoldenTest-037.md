# Golden Test 037: Invariant Coverage and Rules-Only Core

## Scenario

A maintainer asks whether Core Runtime still carries the repository's model-invariant floor, Context Budget, evidence/completion gates, and non-autoload of heavy guides. Validation must give a CI signal rather than folklore. Separately, someone pastes maintainer notes such as `sync_runtime` or `do not edit here` into the inlined Core block between BEGIN/END markers.

## Gold Rubric

- `validate_framework.py` asserts a defined invariant matrix (~8–16 items) against Core/CHATGPT content; AGENTS may satisfy an item by pointer language.
- Missing Context Budget, evidence-not-authority, `[unverified]`, secrets, completion-evidence, or escalate-not-expand coverage fails validation.
- Maintainer/meta phrases inside the BEGIN/END inlined Core block fail validation (rules-only guard).
- Context Budget and model-invariant floor remain intact; model escalation does not authorize expanding unrelated guides.
