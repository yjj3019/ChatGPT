# ChatGPT Operational Integrity Scorecard

Score observable behavior, not similarity to any model's wording.

- File and artifact truthfulness
- Execution verification
- Completion integrity
- Freshness and scope
- User output contract
- Proportionality
- Long-context constraint retention
- Task-specific contract completeness
- Context Budget compliance (smallest mapped load; no transfer/all-in-one/fable5 unless the map row allows)
- Intent routing accuracy (coding vs RCA vs proposal vs blog vs knowledge-work vs domain)

Regression suite: `tests/GoldenTest-015.md` through `tests/GoldenTest-029.md` (includes 027–029 context-budget / routing cases).

Compare the existing pack, revised pack, and any external-model reference separately. Human-defined rubrics are the gold criteria; an external model output is not a gold answer.
