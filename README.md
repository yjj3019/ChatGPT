# ChatGPT and Codex Transfer Pack

Model-independent working guidance for engineering, writing, and evidence-backed completion. This repository changes **instructions and routing**, not model weights or hidden reasoning. It does **not** create automatic cross-session memory.

**한국어:** [README.ko.md](README.ko.md)

## For AI agents (repo URL only)

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
# then: Codex → open this repo as workspace (loads AGENTS.md)
# ChatGPT → paste CHATGPT.md into Project Instructions; attach docs/ as needed
```

- `python3 scripts/install_pack.py --auto` — detect Claude / Codex / Grok / Cursor / AGENTS hosts and copy the pack to each skills root as `chatgpt-transfer/`
- `python3 scripts/install_pack.py --print-chatgpt` — exact paste steps for ChatGPT Project Instructions (web cannot fully automate)
- `python3 scripts/install_pack.py --check` — verify files and run `validate_framework.py`
- `python3 scripts/install_pack.py --help` — destinations, `--dest`, `--with-tests`, `--dry-run`

Preferred Codex path: **open this clone as the workspace** so `AGENTS.md` loads at the root. Skill copies are for hosts that discover packs under `~/.agents/skills` (and similar). Keep existing higher-priority workspace rules when adopting this pack.

## What this is / is not

| Is | Is not |
|---|---|
| Lean ChatGPT + Codex entry points with selective guide loading | Fine-tuning, weight training, or CoT distillation |
| Context Budget + Model-Invariant Floor across models | A guarantee that every model performs equally |
| Sync / validate / measure / golden-test maintenance tooling | Automatic cross-session memory or secret storage |
| Advisory model routing (`gpt-6-astra` … `gpt-5.4-mini`) | A substitute for verifying host model availability |

## Choose one entry point

| Use | Entry |
|---|---|
| ChatGPT Project | Put `CHATGPT.md` in Project Instructions; make relevant `docs/` available as project knowledge. |
| Codex | Start Codex **in this repository** so it loads `AGENTS.md`. |
| One-shot copy/paste | Use `docs/chatgpt-5.5-all-in-one-instructions.md` for Core + coding / proposal / blog when you cannot attach the repo. |
| Skill-style host | After `--auto`, use the installed `chatgpt-transfer/` pack (`SKILL.md` + `AGENTS.md`). |

Read the chosen entry when available at session start. The entry routes each task to the **smallest** relevant guide. Simple tasks use the Core alone. Full and standalone guides are alternatives, not layers to stack on every task.

## Context Budget + Model-Invariant Floor

**Context Budget (normal use):** Core + 1–2 mapped guides, or one task section + one domain section. Do **not** preload the full transfer guide, all-in-one fallback, pattern bank, or every `docs/codex-*.md`.

**Model-Invariant Floor** (see `docs/chatgpt-codex-model-routing.md`): regardless of `gpt-6-astra` … `gpt-5.4-mini`:

1. Same Core + Operational Integrity (evidence, completion, authorization, no secrets).
2. Same Context Budget — do not dump extra docs onto weaker or stronger models to “compensate.”
3. Same Task Loading Map / Intent Classifier.
4. Same output contract (`[unverified]`, smallest complete change, no fake completion).
5. When blocked: **escalate the model** (`mini` → `luna` → `terra` → `sol` → `astra`); do **not** expand unrelated instructions.

Advisory defaults (verify availability): complex → `gpt-6-astra`; everyday agentic → `gpt-5.6-sol`; everyday coding → `gpt-5.6-terra`; cheap/fast coding → `gpt-5.6-luna`; tiny → `gpt-5.4-mini`.

## Focused guides

- `docs/chatgpt-5.5-project-instructions.md` — canonical task/output and effort rules (Core).
- `docs/chatgpt-operational-integrity-rules.md` — authority, evidence, actions, completion.
- `docs/chatgpt-coding-rules.md` — implementation, debugging, review.
- `docs/chatgpt-proposal-review-rules.md` / `docs/chatgpt-blog-rules.md` — document contracts.
- `docs/chatgpt-engineering-task-rules.md` — architecture, RCA, research, SOP, prompt/security review (**matching section only**).
- `docs/chatgpt-domain-packs.md` — RHEL, OpenShift, Kubernetes, Linux, Ansible, Satellite, EA, AI infra, EV (**matching section only**).
- `docs/chatgpt-knowledge-work-rules.md` — meetings, presentations, executive summaries.
- `docs/chatgpt-codex-model-routing.md` — dated advisory model preferences + Model-Invariant Floor.
- `docs/codex-*.md` — Codex ops, Office, subagents, team gates (load only when relevant).
- `prompts/chatgpt-task-prompts.md` — optional task prompts.
- `docs/chatgpt-transfer-instructions.md` — generated full reference; load only when requested.
- `docs/fable5-pattern-bank-for-chatgpt.md` — optional historical calibration (non-autoload).

Historical filenames containing `5.5` are retained for compatibility; they do not require that model.

## Maintain and verify

Python 3.11+ and the standard library only. No package install, API key, or model call is required for repository checks.

```text
python scripts/sync_runtime.py
python scripts/sync_runtime.py --check
python scripts/validate_framework.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/measure_load.py
python scripts/install_pack.py --check
```

Edit canonical source documents, then regenerate the three distribution documents with `sync_runtime.py`. The sync `--check` never writes files. Validation checks generated-document parity, routing targets, local file references, required Golden Test contracts, fence-aware section parsing, Core invariants, and repository character budgets (`CHATGPT.md` ≤ 8000, `AGENTS.md` ≤ 4000). Regression tests use disposable sibling copies, so the repository parent must be writable.

GitHub Actions runs these checks on Windows and Linux with Python 3.11 and 3.12. `measure_load.py` reports normalized UTF-8 bytes; its bytes/4 heuristic is **not** actual token usage and excludes host/tool overhead.

## Evidence and simulation pointers

- [Five-round improvement report](docs/optimization-report-2026-09-06.md) — Core diet, AGENTS lean, routing, budgets.
- [Simulation-10 report](docs/simulation-10-report-2026-09-06.md) — context budget, model floor, sync, fence-aware sections, invariants (post PR #4/#5/#6/#7).
- Controlled behavior rubrics: `tests/Scorecard.md`, `tests/GoldenTest-015.md` … `tests/GoldenTest-037.md`.

Structural checks do not run live ChatGPT/Codex behavior trials. Official principles that informed routing (not proof of speed/accuracy gains): [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [selective skill loading](https://learn.chatgpt.com/docs/build-skills), [instruction clarity](https://developers.openai.com/api/docs/guides/latest-model) (checked 2026-09-06).
