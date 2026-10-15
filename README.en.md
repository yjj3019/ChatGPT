# ChatGPT and Codex Transfer Pack

A **model-independent instruction distribution** for multiple recipients and hosts, supporting engineering, writing, and evidence-backed completion. This repository provides **instructions and routing**, not model weights or hidden reasoning. It does **not** create automatic cross-session memory.

The baseline **preserves the recipient's model, reasoning effort, permissions, and existing settings**. No particular machine or model combination is required. The [distribution standard](docs/distribution-standard.md) defines model-inheriting role examples, opt-in activation, and environment-specific verification/rollback. Installation alone does not activate user settings, roles, or memory features.

**Language:** [한국어](README.md) | English

## Codex app marketplace install, remove, and update

Check that `codex plugin --help` and `codex plugin marketplace --help` support the commands below. This repository exposes one `chatgpt-transfer` plugin through the `yjj3019-chatgpt` marketplace. This does not mean it has been reviewed or listed in the universal public plugin directory.

Register the repository marketplace and install the plugin:

```text
codex plugin marketplace add yjj3019/ChatGPT --ref main
codex plugin add chatgpt-transfer@yjj3019-chatgpt
```

Restart the Codex app, check installation in Plugins, and start a new chat. For example: “Apply the chatgpt-transfer pack to review this code.” Installation and observed skill selection/compliance are separate checks. The pack does not change model, permission, or memory settings.

Update by reinstalling: remove this plugin, refresh the marketplace's Git snapshot, then install it again. Check each command succeeds before running the next:

```text
codex plugin remove chatgpt-transfer@yjj3019-chatgpt
codex plugin marketplace upgrade yjj3019-chatgpt
codex plugin add chatgpt-transfer@yjj3019-chatgpt
codex plugin list --marketplace yjj3019-chatgpt --json
```

Restart the app and verify in a new chat after updating. On the tested Windows CLI, refreshing while installed failed with access denied when replacing the existing cache; the reinstall sequence above succeeded. The pack is temporarily uninstalled during this update. If network refresh fails, restore connectivity and rerun refresh/install. Publishers also bump the version in root `plugin.json` when plugin content changes.

To uninstall, remove the plugin. Run the second command only if you also want to unregister its marketplace:

```text
codex plugin remove chatgpt-transfer@yjj3019-chatgpt
codex plugin marketplace remove yjj3019-chatgpt
```

Removal targets this plugin's configuration/cache. Skills copied by the existing Python installer and Git clones are managed separately. Choose one installation method to avoid duplicate discovery. Confirm actual app presentation and compatibility in the installed version. [Official packaging guide](https://developers.openai.com/plugins/build/plugins?install-scope=workspace), [official management commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin) (checked 2026-10-15).

Validation scope: Codex CLI `0.162.0-alpha.17.2` on Windows, with separate temporary configuration/cache. Local fixture version/document updates and actual GitHub URL registration, installation, update by reinstalling, and removal were verified. Actual app presentation and model compliance require separate validation.

## For AI agents (repo URL only)

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
# then: Codex → open this repo as workspace (verify AGENTS.md is active)
# ChatGPT → paste CHATGPT.md into Project Instructions; attach docs/ as needed
```

- `python3 scripts/install_pack.py --auto` — detect Claude / Codex / Grok / Cursor / AGENTS hosts and copy the pack to each skills root as `chatgpt-transfer/`
- `python3 scripts/install_pack.py --print-chatgpt` — exact paste steps for ChatGPT Project Instructions (web cannot fully automate)
- `python3 scripts/install_pack.py --check` — verify files and run `validate_framework.py`
- `python3 scripts/install_pack.py --help` — destinations, `--dest`, `--with-tests`, `--dry-run`

Existing identical installs are skipped and user files are preserved. Changed, incomplete, or legacy installs are refused. Back up local files before using `--force`: it replaces the entire pack, including user-added files. `--dry-run` checks conflicts without writing; `--check` verifies the local content manifest (not publisher authenticity). Do not run concurrently against the same destination.

For a source ZIP, run `python scripts/validate_framework.py`; source-mode `install_pack.py --check` requires a Git checkout. ZIP sources can still be installed.

Preferred Codex path: **open this clone as the workspace** and verify that the root `AGENTS.md` is active. Skill copies are for hosts that discover packs under `~/.agents/skills` (and similar). Keep existing higher-priority workspace rules when adopting this pack.

## What this is / is not

| Is | Is not |
|---|---|
| Lean ChatGPT + Codex entry points with selective guide loading | Fine-tuning, weight training, or CoT distillation |
| Context Budget + Model-Invariant Floor across models | A guarantee that every model performs equally |
| Sync / validate / measure / golden-test maintenance tooling | Automatic cross-session memory or secret storage |
| Evidence-based model/effort routing | A substitute for verifying host model availability |

## Choose one entry point

| Use | Entry |
|---|---|
| ChatGPT Project | Put `CHATGPT.md` in Project Instructions; make relevant `docs/` available as project knowledge. |
| Codex | Start Codex **in this repository** and verify that `AGENTS.md` is active. |
| One-shot copy/paste | Use `docs/chatgpt-5.5-all-in-one-instructions.md` for Core + coding / proposal / blog when you cannot attach the repo. |
| Skill-style host | After `--auto`, use the installed `chatgpt-transfer/` pack (`SKILL.md` + `AGENTS.md`). |

Read the chosen entry when available at session start. The entry routes each task to the **smallest** relevant guide. Simple tasks use the Core alone. Full and standalone guides are alternatives, not layers to stack on every task.

## Check the actual host after setup

A file's presence does not prove its instructions were loaded. A ChatGPT Project alone does not grant access to a computer folder; upload relevant files or provide an authorized connection. See [Projects documentation](https://learn.chatgpt.com/docs/projects) (checked 2026-10-10).

1. Record the surface (Chat, ChatGPT Work, Codex, API), client/version, and authentication method. For local work, also verify the primary folder or `cwd`.
2. For Codex, verify the active `AGENTS.md` source, global/parent instructions, and `AGENTS.override.md`. See the [operations guide](docs/codex-operations-rules.md#host-setup-smoke-check) for the default combined 32 KiB limit and `project_doc_max_bytes` setting.
3. In the current session, verify access to one selected guide and that its relevant section was read. Do not report successful loading without evidence.

These are checks for the user to perform in that host. Static repository checks do not replace actual host/model smoke tests. Before model selection, verify the exposed models, effort settings, tools, and permissions in the [model guide](docs/chatgpt-codex-model-routing.md#verify-the-product-surface).

## Context Budget + Model-Invariant Floor

**Context Budget (normal use):** Core + 1–2 mapped guides, or one task section + one domain section. Do **not** preload the full transfer guide, all-in-one fallback, pattern bank, or every `docs/codex-*.md`.

**Model-Invariant Floor** (see `docs/chatgpt-codex-model-routing.md`): on every model:

1. Same Core + Operational Integrity (evidence, completion, authorization, no secrets).
2. Same Context Budget — do not dump extra docs onto weaker or stronger models to “compensate.”
3. Same Task Loading Map / Intent Classifier.
4. Same output contract (`[unverified]`, smallest complete change, no fake completion).
5. Diagnose blockers first: missing evidence or permission is not a model capability limit. Do **not** expand unrelated instructions.

Keep the current session model and effort by default. Change only when task evidence justifies it, the host supports it, and authorization permits it. Follow `docs/chatgpt-codex-model-routing.md`; no fixed roster or automatic escalation ladder applies.

## Focused guides

- `docs/chatgpt-5.5-project-instructions.md` — canonical task/output and effort rules (Core).
- `docs/chatgpt-operational-integrity-rules.md` — authority, evidence, actions, completion.
- `docs/chatgpt-coding-rules.md` — implementation, debugging, review.
- `docs/chatgpt-proposal-review-rules.md` / `docs/chatgpt-blog-rules.md` — document contracts.
- `docs/chatgpt-engineering-task-rules.md` — architecture, RCA, research, SOP, prompt/security review (**matching section only**).
- `docs/chatgpt-domain-packs.md` — RHEL, OpenShift, Kubernetes, Linux, Ansible, Satellite, EA, AI infra, EV (**matching section only**).
- `docs/chatgpt-knowledge-work-rules.md` — meetings, presentations, executive summaries.
- `docs/chatgpt-codex-model-routing.md` — current-model default, evidence-based changes, and Model-Invariant Floor.
- `docs/codex-*.md` — Codex ops, Office, subagents, team gates (load only when relevant).
- `prompts/chatgpt-task-prompts.md` — optional task prompts.
- `docs/chatgpt-transfer-instructions.md` — generated full reference; load only when requested.
- `docs/fable5-pattern-bank-for-chatgpt.md` — optional historical calibration (non-autoload).

Historical filenames containing `5.5` are retained for compatibility; they do not require that model.

## Maintain and verify

For an explicitly requested Sol main / Luna explorer-runner / conditional Astra reviewer setup, use the [optional three-model guide](docs/codex-three-model-setup.md) and its role TOML/delegation examples. It covers inherited permissions, support/conflict checks, fresh-session verification, and rollback. Pack installation does not activate the preset; normal routing stays model-independent.

For Codex Memories setup or model updates, optionally read the [Memories maintenance guide](docs/codex-memories-maintenance.md). Its default example omits model IDs; apply only justified overrides after checking the installed version, supported keys, and access for each memory role. It covers unsupported-pin removal and default revalidation, error-specific stop conditions, and the difference between config and memory-state rollback. Installing the pack does not change user settings or memories. Report static checks separately from live host trials.

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

Parallel review stays read-only. Give reviewers the scope and acceptance criteria, the exact revision or diff and relevant files, and each verification command with its working directory, exit status, and success or failure evidence. State why any check was not run. Report missing, stale, or insufficient validation as `Validation Gap`; an observed failed check is FAIL. The parent owns fixes and focused retests, then reconciles findings against fresh evidence without recursive review. See `docs/codex-subagent-rules.md` and `docs/codex-team-agent-rules.md`.

GitHub Actions runs these checks on Windows and Linux with Python 3.11 and 3.12. `measure_load.py` reports normalized UTF-8 bytes; its bytes/4 heuristic is **not** actual token usage and excludes host/tool overhead.

## Evidence and simulation pointers

- [Five-round improvement report](docs/optimization-report-2026-09-06.md) — Core diet, AGENTS lean, routing, budgets.
- [Simulation-10 report](docs/simulation-10-report-2026-09-06.md) — context budget, model floor, sync, fence-aware sections, invariants (post PR #4/#5/#6/#7).
- Controlled behavior rubrics: `tests/Scorecard.md`, `tests/GoldenTest-015.md` … `tests/GoldenTest-040.md`.

Structural checks do not run live ChatGPT/Codex behavior trials. Official principles that informed routing (not proof of speed/accuracy gains): [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [selective skill loading](https://learn.chatgpt.com/docs/build-skills), [instruction clarity](https://developers.openai.com/api/docs/guides/latest-model) (checked 2026-09-06).
