# ChatGPT and Codex Transfer Pack

Model-independent instructions for engineering, writing, and evidence-backed completion. This repository changes working guidance; it does not train model weights or copy hidden reasoning.

## Choose One Entry Point

| Use | Entry |
|---|---|
| ChatGPT Project | Put `CHATGPT.md` in Project Instructions and make the relevant `docs/` files available as project knowledge. |
| Codex | Start Codex in this repository so it can load `AGENTS.md`. |
| Standalone copy/paste | Use `docs/chatgpt-5.5-all-in-one-instructions.md` for Core, coding, proposal review, and blog tasks. |

Read the chosen entry when available at session start. Files do not create automatic cross-session memory. Keep existing higher-priority workspace rules when adopting this pack.

The entry routes each task to the smallest relevant guide. Simple tasks use the Core alone. Full and standalone guides are alternatives, not extra layers to load on every task.

## Focused Guides

- `docs/chatgpt-5.5-project-instructions.md` — canonical task/output and effort rules.
- `docs/chatgpt-operational-integrity-rules.md` — canonical authority, evidence, actions, and completion rules.
- `docs/chatgpt-coding-rules.md` — implementation, debugging, and review.
- `docs/chatgpt-proposal-review-rules.md` and `docs/chatgpt-blog-rules.md` — document-specific contracts.
- `docs/chatgpt-engineering-task-rules.md` — architecture, RCA, research, SOP, prompt review, and security review; load the matching section.
- `docs/chatgpt-domain-packs.md` — RHEL, OpenShift, Kubernetes, Linux, Ansible, Satellite, enterprise architecture, AI infrastructure, and EV domains.
- `docs/chatgpt-knowledge-work-rules.md` — meetings, presentations, and executive summaries.
- `docs/chatgpt-codex-model-routing.md` — dated advisory model preferences; verify availability before switching.
- `docs/codex-*.md` — task-specific Codex operations, context, Office, and subagent guidance.
- `prompts/chatgpt-task-prompts.md` — optional task prompts.
- `docs/chatgpt-transfer-instructions.md` — generated full reference, loaded only when requested.
- `docs/fable5-pattern-bank-for-chatgpt.md` — optional historical calibration.

Historical filenames containing 5.5 are retained for compatibility; they do not require that model.

## Maintain and Verify

Python 3.11+ and the standard library; no package installation, API key, or model call is needed for repository checks.

Edit canonical source documents, then regenerate the three distribution documents:

```text
python scripts/sync_runtime.py
python scripts/sync_runtime.py --check
python scripts/validate_framework.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/measure_load.py
```

The sync check never writes files. Validation checks generated-document parity, routing targets, local file references, required Golden Test contracts, and repository-defined character budgets. Regression tests use disposable sibling copies, so the repository parent must be writable.

GitHub Actions runs these checks on Windows and Linux with Python 3.11 and 3.12. The optional load report uses normalized UTF-8 bytes; its bytes/4 heuristic is not actual token usage and excludes entry/router and host/tool overhead. Structural checks do not run ChatGPT/Codex behavior trials. Use `tests/Scorecard.md` and `tests/GoldenTest-015.md` through `tests/GoldenTest-035.md` for controlled behavior evaluation.

## Improvement Evidence

See the [five-round improvement report](docs/optimization-report-2026-09-06.md) for the baseline, measured instruction reductions, validation results, and limitations.

The routing and effort choices align with official guidance on [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [selective skill loading](https://learn.chatgpt.com/docs/build-skills), and [proportional verification and instruction clarity](https://developers.openai.com/api/docs/guides/latest-model). Checked 2026-09-06; these are principles, not proof of a speed or accuracy gain.