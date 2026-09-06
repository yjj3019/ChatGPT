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
- Section-scoped loading (engineering-task and domain-packs: matching `##` section only)
- Model-invariant floor (same Integrity/Budget/Map on all six models; escalate model, not context)

Regression suite: `tests/GoldenTest-015.md` through `tests/GoldenTest-031.md` (includes 027–030 context-budget / routing / section-scope; 031 model-routing).

Compare the existing pack, revised pack, and any external-model reference separately. Human-defined rubrics are the gold criteria; an external model output is not a gold answer.

## Training rounds (instruction-pack closed loop)

Five measure→change→validate rounds on `perf/context-budget-routing` (Core diet, AGENTS lean, routing precision + Golden 030, section-aware load measurement, budget recalibration). See `/workspace/ChatGPT-training-log.md` when present in the agent workspace, and the README training summary in-repo.
