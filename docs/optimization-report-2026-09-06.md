# Fifth-round ChatGPT and Codex instruction improvement report

> This report preserves the evidence behind historical changes. The figures, model recommendations, and verification results below apply only to the recorded date and commits. For current distribution requirements, follow the [distribution standard](distribution-standard.md); for current checks, follow the [README](../README.md).

- Work date: 2026-09-06
- Target: yjj3019/ChatGPT
- Baseline commit: `122793160b7fc0b5ec609b0ec7eb537aa0997134`
- Method: 5 rounds of instruction changes → static and regression checks → result review
- Scope: improvements to instructions, routing, and verification, rather than model-weight training or fine-tuning

## Results by round

| Round | Problems identified | Changes and verification |
|---|---|---|
| 1 | Diagnostics stopped on missing required sources or invalid generation markers; no read-only synchronization check | Explicit failure reporting, `--check`, preservation of unchanged files, and consistent line endings. 6 regression tests passed. |
| 2 | Repetition, excessive procedure, and unclear precedence for user instructions in ChatGPT's default entry text | A shorter Core, selective loading, missing-material handling that blocks only the affected work, and an 8,000-character maintenance budget. 7 regression tests passed. |
| 3 | Broad document loading in Codex conflicted with the prohibition on modifying tests | Concise task-specific routing, executable verification commands, permission for necessary regression tests, and a 4,000-character budget. 8 regression tests passed. |
| 4 | Old rules remained in the copy-ready and integrated instructions after the default instructions changed | Three distribution documents generated from the same canonical sources, stopping before writes on source errors, and document-difference checks. 12 regression tests passed. |
| 5 | Checking task names alone missed misrouted paths, empty evaluation criteria, and missing tests | Checks of actual paths and evaluation contracts, invalid-input regression tests, Windows/Linux CI, scoring criteria, and rules for reporting measured results. 30 regression tests and structural and synchronization checks passed. |

## Instruction size measurements

The Git baseline files and final files were read as UTF-8, excluding the BOM and normalizing line endings to LF. Python `len(text)` and UTF-8 byte lengths were then compared. These are not measurements of model tokens or latency.

| Entry file | Characters before | Characters after | Reduction |
|---|---:|---:|---:|
| ChatGPT: CHATGPT.md | 12,150 | 7,914 | 34.9% |
| Codex: AGENTS.md | 5,099 | 3,846 | 24.6% |
| Copy-ready guide | 5,840 | 7,964 | 36.4% increase |

In UTF-8 bytes, the ChatGPT entry file changed from 12,162 → 7,928 bytes, and the Codex entry file from 5,099 → 3,848 bytes.

The copy-ready instructions were expanded to include all current Core, permission, and verification rules. The integrated guide is also generated from the sources, so its overall length increased, but it explicitly states that it is not loaded automatically on the default execution path. This is not a claim that every file became smaller. Character budgets are repository maintenance criteria, not product input limits.

## Integrating remote changes added during the work

After the five improvement commits were complete, remote main was found to have advanced to `13e1e12`. The context budgets and measurement tools from PR #4 and the model-selection guidance from PR #5 were preserved during integration. This was compatibility work after the five rounds above.

- Remote Golden Tests 027–031 were retained, and the new tests from this work were numbered 032–035.
- The final verification scope covered 14 task paths, 21 required behavioral scenarios, and 37 automated regression tests.
- The measurement tool was fixed to avoid counting standalone Core twice, treating missing files or sections as zero bytes, and using inconsistent byte criteria across platforms. The documentation clarified that bytes/4 is an uncalibrated estimate, not actual token usage.
- Model defaults were preserved as dated recommendations. The claim that identical instructions guarantee identical quality across models was removed, and checks of availability and permission to make changes, along with necessary evidence collection, were allowed.
- Before integration, remote main contained 14,406 characters in CHATGPT.md and 4,083 in AGENTS.md. The table's reduction percentages use the starting baseline; effects from concurrent work must not be attributed solely to this work.
- All 37 regression tests in the integrated version passed locally on Python 3.14. Structural and synchronization rechecks also passed after the documentation cleanup.

## Verification and limitations

- Existing structural check: passed on the baseline repository, but fault injection caused a missing source to stop diagnostics with an exception, while invalid routing passed.
- Final local checks for round five: 30 regression tests passed on Python 3.14; structural checks passed for 13 paths and 16 required scenarios; synchronization of the three generated documents and Python syntax checks passed.
- Final independent review: one reviewer compared the code against the rules in scenarios 020 and 023 and final-numbered scenarios 032, 033, 034, and 035. No Critical/P1 regressions were found; exception handling for invalid URLs and report wording were corrected. This was a static review, not a model behavior score.
- GitHub CI: all four Windows/Linux × Python 3.11/3.12 jobs passed in [run 34023599162](https://github.com/yjj3019/ChatGPT/actions/runs/34023599162) for integration commit `eececaad5999761870663871f8e7afdeb797021d`. Subsequent documentation changes are tracked through each commit's GitHub checks.
- Tests did not run in the restricted Windows environment because of temporary-folder access errors. Verification used a temporary repository copy in a separately authorized execution; the environment error was not counted as degraded instruction performance.
- The 21 Golden Tests after integration are behavioral evaluation scenarios. Structural checks do not prove successful actual model responses to those scenarios.
- No controlled experiment was performed through repeated runs on actual ChatGPT/Codex hosts with the same model and settings. Improvements in accuracy, tokens, cost, and response latency remain unmeasured.
- This work did not include training or benchmarks that incur API costs, or changes to user-global settings.

## Subsequent evaluation method

Use the procedure in `tests/Scorecard.md`: identical inputs, separate sessions, and at least 3 paired runs. Compare quality and major failures first, and record measured tool calls, questions, tokens, and time alongside them. Use `tests/GoldenTest-032.md` through `tests/GoldenTest-035.md` for regression evaluation, covering instructions in external documents, missing materials, safe code changes, output formats, and publication evidence.

## Official guidance consulted

Checked on 2026-09-06: [AGENTS.md scope and loading](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [selective skill loading](https://learn.chatgpt.com/docs/build-skills), and [clear instructions and verification proportional to task size](https://developers.openai.com/api/docs/guides/latest-model). These documents provided design rationale, not performance benchmark results for this repository.
