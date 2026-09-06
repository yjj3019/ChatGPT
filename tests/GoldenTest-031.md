# Golden Test 031: Model Selection Loads Routing Doc Only

## Scenario

The user asks which ChatGPT/Codex model to use, or how to switch among astra / sol / terra / luna / 5.5 / 5.4-mini (for example: "Which model for everyday PR coding?" or "Set Codex to the right model for this RCA"). No code patch, transfer-guide dump, or unrelated task-file work is requested.

## Gold Rubric

- Primary route: Model selection / routing advice.
- Loads `docs/chatgpt-codex-model-routing.md` (+ Core Runtime).
- Does **not** load `docs/chatgpt-transfer-instructions.md`.
- Does **not** load `docs/chatgpt-5.5-all-in-one-instructions.md`.
- Does **not** load `docs/fable5-pattern-bank-for-chatgpt.md`.
- Does **not** autoload coding / engineering / domain / all `codex-*.md` solely because a model was discussed.
- Affirms the **model-invariant floor**: same Integrity, Context Budget, Task Loading Map, and output contract on every model; escalate model when blocked/risk rises rather than expanding context.
- Recommends defaults aligned with the routing doc (e.g. everyday coding → terra; complex → astra).

## Negative Control

Loading transfer, all-in-one, fable5, or every task pack when the user only asked for model advice fails Context Budget. Treating a weaker model as license to skip Operational Integrity, or dumping extra docs onto astra/mini to "compensate," also fails.

## Protocol

Score: model-selection map row, routing-doc-only (+ Core) load, forbidden heavy loads avoided, model-invariant floor stated, default pick accuracy.
