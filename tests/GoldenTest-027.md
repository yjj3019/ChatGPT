# Golden Test 027: Simple Q&A Uses Core Only

## Scenario

Ask a simple factual or definitional question that needs no coding, RCA, proposal, blog, or domain pack (for example: "What does RTO mean in disaster recovery?" or a short glossary/clarification request with no attached incident or codebase).

## Gold Rubric

- Loads Core Runtime / invariants only.
- Does **not** load `docs/chatgpt-transfer-instructions.md`.
- Does **not** load `docs/chatgpt-5.5-all-in-one-instructions.md`.
- Does **not** load `docs/fable5-pattern-bank-for-chatgpt.md`.
- Does **not** load task packs such as coding, engineering-task, proposal, blog, knowledge-work, or domain packs.
- Answers concisely; separates facts vs assumptions when needed; marks unsupported claims `[unverified]`.

## Negative Control

Autoloading the transfer pack, all-in-one paste block, or fable5 pattern bank for a simple Q&A fails Context Budget even if the answer text is correct.

## Protocol

Compare routing and loaded files against the Task Loading Map and Context Budget. Score: Core-only compliance, forbidden heavy files avoided, answer usefulness.
