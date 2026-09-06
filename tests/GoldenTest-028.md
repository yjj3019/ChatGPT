# Golden Test 028: Coding Task Loads Coding Rules

## Scenario

A coding/debugging request against a repository or snippet (for example: failing test, stack trace, "implement X", "optimize this SQL query", or a PR bugfix). No request for the full combined transfer guide or one-shot paste setup.

## Gold Rubric

- Selects Coding/debugging from the Task Loading Map / Intent Classifier.
- Loads `docs/chatgpt-coding-rules.md` (plus Core Runtime).
- May optionally load `prompts/chatgpt-task-prompts.md`; must **not** load `docs/chatgpt-transfer-instructions.md` or `docs/chatgpt-5.5-all-in-one-instructions.md`.
- Does not load all `docs/codex-*.md` at once.
- Applies shared-root-cause, caller scan, smallest fix, and path/workspace verification discipline.
- Prefers coding intent over generic "error/fix" when the object is source code or tests.

## Negative Control

Loading the transfer pack or all-in-one instructions for an ordinary coding task fails Context Budget. Routing an RCA-document wording fix as coding also fails Intent Classifier controls (see Golden Test 024).

## Protocol

Score task selection, required files loaded, forbidden heavy files avoided, and coding report shape (root cause, changed files, verification, caller scan).
