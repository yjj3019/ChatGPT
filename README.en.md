# TaskForge for ChatGPT

**Task guidance for ChatGPT and Codex**

An **instruction pack** for engineering, writing, and evidence-backed completion. Install it as a GitHub marketplace plugin in the Codex app, or use Project Instructions in ChatGPT. It does not train or copy model weights or hidden reasoning, or create automatic cross-session memory.

New conversations applying the native Codex TaskForge for ChatGPT skill preserve the current model/effort and use registered model-inheriting roles for exploration, verification, and conditional review. Fixed Sol/Luna/Astra models require an explicitly selected PRESET. An explicit user model choice suspends automatic delegation for that conversation and preserves the chosen model/effort. A new conversation applying TaskForge for ChatGPT returns to DEFAULT unless a separately approved host-wide PRESET policy applies; resuming a conversation or restarting the app alone does not reset it. Installation does not modify user settings, roles, or memories. See the [distribution standard](docs/distribution-standard.md).

**Language:** [한국어](README.md) | English

## Recent improvements (3.0.2)

| Improvement | Current behavior |
|---|---|
| Name and ID migration | Use TaskForge for ChatGPT and the shared plugin, skill, and Python installation ID `taskforge-for-chatgpt`. Existing 2.x installations require the migration below |
| Long-task harness | Criterion-level evidence/verdicts, observed-state resume, and separate sample/final artifact validation |
| Skill display name | Add UI metadata that preserves `TaskForge for ChatGPT` capitalization in the skill row |
| Model defaults | Preserve the current model/effort and prefer registered model-inheriting roles. Fixed models require explicit PRESET selection |
| Operational loading | Read only the required operational sections linked by the skill; do not preload the full setup guide |
| Installer options | `--auto` and `--dest` are mutually exclusive. Select only one of `--check`, `--list-targets`, or `--print-chatgpt`; reject conflicts before any action |
| Regression checks | Detect missing or duplicate operational sections, missing core rules, and missing skill-loading links |
| Release version | Require a higher version for payload changes, compared with the PR or push base commit |
| Host role registration | Add DEFAULT personal-role registration, conflict preservation, fresh-process checks, and observed model-inheritance evidence |

This summary describes the source version. Update an installed copy separately and check its version. The [live verification record](docs/host-verification-2026-10-18.md) separates 2.3.0 role-registration trials from installed 2.3.1 CLI/app trials. After the user reported restarting the app on 2026-10-19, the existing verification conversation reread the guidance, Explorer and Runner exited 0, and native records reconfirmed actual parent/child model and effort inheritance. The app's current model label was also observed; menu contents, selection-change detection, and automatic state resets were not tested. Version 2.3.2 documents this evidence; the live target was 2.3.1. The observations do not establish success outside the recorded environment or cover every behavior.

See the [harness pattern adoption record](docs/ai-harness-adoption.md) for the comparison and excluded patterns. Small tasks do not require stage tables or new state files; model, delegation, memory, and installation policies remain unchanged. Structural checks of scenarios 041–043 do not establish live model behavior or visual QA success.

## Choose an installation method

| Environment or purpose | Method |
|---|---|
| **Codex app — default installation** | Install `taskforge-for-chatgpt` through the marketplace steps below |
| ChatGPT Project | Put `CHATGPT.md` in Project Instructions and provide relevant `docs/` files |
| Other skill-style hosts or existing installation method | Copy `taskforge-for-chatgpt/` with the Python installer below |
| Repository development or workspace rules | Open the repository and verify that root `AGENTS.md` is active |
| One-shot copy/paste | Use `docs/chatgpt-5.5-all-in-one-instructions.md` |

Choose one entry point. Using both the marketplace plugin and a Python copy can cause duplicate discovery of this pack.

## Codex app marketplace install, remove, and update

Codex CLI is required. Check `codex plugin --help` and `codex plugin marketplace --help` for support before running these commands. The marketplace is `yjj3019`; the plugin is `taskforge-for-chatgpt`. In `taskforge-for-chatgpt@yjj3019`, the part before `@` is the plugin and the part after it is the marketplace identifier. This GitHub marketplace is separate from review and listing in the universal public plugin directory.

### Install

Register the repository marketplace and install the plugin from a terminal. No manual clone or Python installer is needed.

```text
codex plugin marketplace add yjj3019/ChatGPT --ref main
codex plugin add taskforge-for-chatgpt@yjj3019
```

Restart the Codex app and use a new chat. Example: “Apply TaskForge for ChatGPT to review this code.” The plugin reads its installed `AGENTS.md` and relevant guides; it does not change the user's working folder to the pack repository.

### Check installation

```text
codex plugin list --marketplace yjj3019 --json
```

Check the installed entry/version and installation status in the app's Plugins view. File installation and actual model selection/compliance are separate checks.

### Update

Use **remove → refresh marketplace → reinstall** to avoid the cache replacement error observed on the tested Windows CLI. Check each command succeeds before running the next.

```text
codex plugin remove taskforge-for-chatgpt@yjj3019
codex plugin marketplace upgrade yjj3019
codex plugin add taskforge-for-chatgpt@yjj3019
```

The pack is temporarily uninstalled during this update. If network refresh fails, restore connectivity and rerun refresh/install. Then check installation, restart the app, and open a new chat.

### Remove the plugin

```text
codex plugin remove taskforge-for-chatgpt@yjj3019
```

This removes the plugin's installation settings/cache, not previous Python copies or Git clones.

### Unregister the marketplace — optional

After removing the plugin, run this only if you no longer want to use this marketplace.

```text
codex plugin marketplace remove yjj3019
```

### Validation scope

Codex CLI `0.162.0-alpha.17.2` on Windows was tested with separate temporary configuration/cache. Actual GitHub URL registration, installation, update by reinstalling, and removal were verified, alongside local fixture version/document updates. Refreshing while installed failed with access denied during cache replacement; the reinstall sequence above succeeded. Actual app presentation and model behavior require separate validation.

Those remote checks used the previous identity. For 3.0.0, a separate Codex home and local marketplace verified the 2.3.4 → new-ID 3.0.0 → 2.3.4 transition while preserving configuration and user files. On 2026-10-23, this Windows host verified new-ID 3.0.0 installation and, after an app restart, automatic catalog discovery and guidance loading in a fresh verification conversation, plus actual parent/Explorer/Runner model and effort inheritance. A user-supplied plugin detail screenshot also confirmed the name, version 3.0.0, and enabled state. These are host-specific observations, not 3.0.1 installation or UI verification.

[Official packaging guide](https://developers.openai.com/plugins/build/plugins?install-scope=workspace), [official management commands](https://learn.chatgpt.com/docs/developer-commands#codex-plugin) (checked 2026-10-15).

## Migrate from the previous plugin

### When an existing conversation does not discover the new skill

An existing conversation can retain its previous skill catalog after an ID migration. Check installation/enabled state separately from automatic discovery in a fresh conversation. On this host a fresh conversation recognized 3.0.0, while the existing verification conversation did not receive the new ID. `skills/list` with `forceReload` rescans disk metadata; it does not guarantee replacement of an existing conversation’s context. Continuing in a fresh conversation was verified. Preserve the existing conversation; do not delete it or reset configuration as a remedy.

### Version 3 migration

The old `taskforge@yjj3019` installation does not automatically become the new ID. First use `codex plugin list --available --json` to confirm that the target marketplace publishes `taskforge-for-chatgpt` version 3.0.0. Keep the old installation until that version is available.

Privately back up the installed-plugin list, existing plugin settings, and user modifications. Removal deletes that plugin's settings and cache, including edits made inside the cache. Preserve model, permission, role, and memory settings; do not reset the entire Codex home.

Check each command before continuing. Keep the existing marketplace registration. The pack is unavailable between removal and installation.

```text
codex plugin marketplace upgrade yjj3019
codex plugin list --marketplace yjj3019 --available --json
codex plugin remove taskforge@yjj3019
codex plugin add taskforge-for-chatgpt@yjj3019
codex plugin list --marketplace yjj3019 --json
```

Confirm only the new ID is installed and enabled, restart the app, and test it in a new chat. Do not enable both IDs or a Python copy together. Review backed-up user changes before applying them selectively to the new installation.

If installation fails, resolve the connection or permission error and retry the new ID. To roll back to 2.3.4, first confirm this marketplace registration belongs to this repository alone, then pin its previous commit. Omit the first removal if the new ID was never installed. Returning to the latest release later requires registering the marketplace with `--ref main` again.

```text
codex plugin remove taskforge-for-chatgpt@yjj3019
codex plugin marketplace remove yjj3019
codex plugin marketplace add yjj3019/ChatGPT --ref bd3d3843694caef0ff3682baf88a48f1d4ddd410
codex plugin add taskforge@yjj3019
```

The Python installer stops before writing, even with `--force`, when a sibling `chatgpt-transfer/` or `taskforge/` has the old integrity manifest or matching skill ID. An unrelated directory with that name is not treated as an old installation. Back up the whole old pack and manually retire it outside every active skills root, then install and run `--check`. To recover, retire the new pack and return the saved old pack to its original location. Do not combine old and new manifests or overwrite a new home with old configuration. No automatic move or deletion is performed.

### Older marketplace migration

Run this only if `chatgpt-transfer@yjj3019-chatgpt` is installed. Renaming does not automatically update existing installs: remove the old plugin and marketplace registration, then install the new identity. Check each command succeeds before proceeding. The repository URL is unchanged.

```text
codex plugin remove chatgpt-transfer@yjj3019-chatgpt
codex plugin marketplace remove yjj3019-chatgpt
codex plugin marketplace add yjj3019/ChatGPT --ref main
codex plugin add taskforge-for-chatgpt@yjj3019
```

The plugin is temporarily uninstalled during migration. Recover any failure before continuing the remaining steps, then restart the app and use TaskForge for ChatGPT in a new chat. Python copies also require the version 3 migration above.

## Use in a ChatGPT Project

1. Put the repository's `CHATGPT.md` in Project Instructions.
2. Provide only the relevant `docs/` files as project knowledge.
3. Verify actual access to the selected guide.

The full transfer guide and all-in-one are alternative entries; do not stack them during normal use. For paste instructions, run `python3 scripts/install_pack.py --print-chatgpt` from a local clone.

## Existing Python installation — other skill-style hosts

Use this to copy files for Claude / Grok / Cursor / AGENTS-compatible hosts. Codex CLI is also detected, but the marketplace above is the Codex app's default installation method.

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
```

- `--dest` — choose the destination skills root; mutually exclusive with `--auto`
- `--with-tests` — also include evaluation/test files
- `--dry-run` — inspect destinations and conflicts without writing
- `--check` — check a Python install's file integrity; also run structural validation when test files exist
- `--force` — replace the entire existing pack, including user-added files; back up first

Identical installations are skipped and user files preserved. Changed, incomplete, or legacy installations are refused by default. Do not install concurrently to the same destination. This installer's `--check` does not verify marketplace installation status or publisher authenticity.

When moving from Python installation to the marketplace, inspect and back up the old destination, then retire that pack outside every active skills root. This applies to old `chatgpt-transfer/` and current `taskforge-for-chatgpt/` copies. Marketplace commands do not remove Python installations automatically.

For a source ZIP, run `python scripts/validate_framework.py`. Source-mode `install_pack.py --check` requires a Git checkout. ZIP sources can still be installed using Python.

## Check the actual host after setup

A file's presence does not prove its instructions were loaded. A ChatGPT Project alone does not grant access to a computer folder; upload relevant files or provide an authorized connection. See [Projects documentation](https://learn.chatgpt.com/docs/projects) (checked 2026-10-10).

1. Record the surface (Chat, ChatGPT Work, Codex, API), client/version, and authentication method. For local work, also verify the primary folder or `cwd`.
2. For Codex, verify the active `AGENTS.md` source, global/parent instructions, and `AGENTS.override.md`. See the [operations guide](docs/codex-operations-rules.md#host-setup-smoke-check) for the default combined 32 KiB limit and `project_doc_max_bytes` setting.
3. In the current session, verify access to one selected guide and that its relevant section was read. Do not report successful loading without evidence.

These are checks for the user to perform in that host. Static repository checks do not replace actual host/model smoke tests. Before model selection, verify the exposed models, effort settings, tools, and permissions in the [model guide](docs/chatgpt-codex-model-routing.md#verify-the-product-surface).

## Automatic New-Session Delegation and Notion Recording

### Default roles and conversation state

DEFAULT uses `pack_explorer`, `pack_runner`, and `pack_reviewer`, inheriting model/effort under host rules. Roles must already be registered; small tasks stay with the main. If a role is unavailable, report the affected delegation gap and continue authorized work with the main. Installation alone does not activate roles or features.

| State | When it applies | Model and delegation behavior |
|---|---|---|
| `DEFAULT` | A new conversation applying TaskForge for ChatGPT | Preserve the current main model/effort and delegate only useful work to registered model-inheriting roles |
| `PRESET` | Explicit selection or re-enabling of fixed models after support/access checks | Use the optional fixed-model examples below. Instructions alone do not switch the running main model |
| `SUSPENDED` | An explicit model choice or a request to use only one model | Stop all automatic delegation for that conversation. Inherited subagents require a separate user request |

Resuming, compacting, or restarting the app with the same conversation does not reset its state. New conversations start in DEFAULT unless a separately approved host-wide PRESET policy applies. Re-enabling inherited delegation and re-enabling a fixed PRESET are distinct requests. See the [session policy](docs/codex-three-model-setup.md#session-policy).

If a role fails with `unknown agent_type`, follow the [DEFAULT registration procedure](docs/codex-three-model-setup.md#register-default-roles) to check the active Codex home, personal role directory, and conflicts. Skill installation and role registration are separate. In a fresh process, verify role-name calls, actual task success, and parent/child model and effort separately; neither missing names in `debug prompt-input` nor a CLI exit code alone determines acceptance.

### Operational rules for ordinary delegation

Read only the operational sections linked by the skill; do not preload the full setup guide.

- Limit the packet to the goal, constraints, relevant paths, acceptance criteria, and confirmed evidence. Do not forward the full conversation or unrelated logs. Children do not re-delegate.
- Retry a temporary failure at most once, only after confirming the prior call never started or has ended. For a timeout or lost response, inspect the existing task status first; do not duplicate a running or unknown call.
- Do not retry unregistered roles, unavailable model access, or permission denials. Continue permitted work with the main, report the `Validation Gap`, and do not expand permissions.
- Give advance notice when expected cost/latency is material. Do not claim unmeasured cost savings or quality gains.

### Optional fixed models and automatic setup

The table below and host-wide automatic setup are explicitly selected PRESET examples. After a one-time authorized setup, new conversations can request the fixed configuration without manually invoking TaskForge for ChatGPT. Follow the [automatic setup procedure](docs/codex-three-model-setup.md#automatic-policy-for-every-new-session): check the actual homes/roles and differences from existing settings, then merge only approved changes. Plugin installation/update alone does not modify personal settings.

| Role | Settings | Scope |
|---|---|---|
| Sol main | `gpt-6.1-sol` / medium | Design, implementation, integration and final judgment |
| Luna Explorer / Runner | `gpt-6-luna` / high / low | Exploration / specified verification |
| Astra Reviewer | `gpt-6-astra` / low | Before important directions are finalized or after two failed fix/retest attempts |
| Optional Notion Recorder | `gpt-6-luna` / low | Approved-page recording and readback |

### Optional Notion recording

The [Notion guide](docs/codex-notion-recording.md) separates confirmed content from recording. Its distributable example takes an approved `page_url` and six record fields, with no private project destination. Do not automatically replace an existing project-specific role.

The [2026-10-16 verification record](docs/host-verification-2026-10-16.md) separates actual model/command trials, one private-role Notion write, Windows execution errors and Hook limitations. For Windows and Orca checks, see [host troubleshooting](docs/host-troubleshooting.md). UI model-picker detection, success on other hosts and cost savings are not guaranteed. An explicit single-model choice suspends all automatic delegation for that conversation; inherited subagents require a separate user request.

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

Bump the version in root `plugin.json` when changing distributed plugin content. Record the version, exact commit, CI run link, and validation gaps together. CI compares PRs with the base-branch commit and pushes to existing branches with the previous commit, requiring a version increase for payload changes. Locally, replace `BASE_COMMIT` below with the actual base commit. The check is read-only and includes staged, unstaged, and untracked files. Changes limited to `.github/` and `.gitignore` are excluded.

```text
python scripts/check_release.py --base BASE_COMMIT
```

A new branch's first push compares with the fetched default-branch tip. For a newly created default branch itself, only a parentless root commit is an initial distribution; existing history without an explicit comparison base fails the check. This checks version traceability; it neither publishes a release nor substitutes for live host validation.

Use the [session-based three-model guide](docs/codex-three-model-setup.md) for the native Codex default. Actual execution requires model access and host role registration. Instructions cannot switch the running main model or reliably detect every UI model choice. If the host does not expose your selection, say **"use this model only"**; to restore inherited delegation, request **"re-enable TaskForge for ChatGPT model-inheriting delegation"**. To opt into fixed models for this conversation, explicitly request **"re-enable the TaskForge for ChatGPT three-model preset"**, subject to support/access checks. Settings changes require separate authorization and verification. ChatGPT and legacy Python entry points retain the current-model default.

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

Edit canonical source documents, then regenerate the three distribution documents with `sync_runtime.py`. The sync `--check` never writes files. Validation checks generated-document parity, routing targets, local file references, required Golden Test contracts, fence-aware section parsing, Core invariants, and repository character budgets (`CHATGPT.md` ≤ 8000, `AGENTS.md` ≤ 4000).

| Check | What it verifies |
|---|---|
| Synchronization | Generated documents match canonical sources |
| Structure | Required native operational sections, core rules, and skill-loading links exist; operational sections are not duplicated |
| Regression tests | Installation preservation/rollback, conflicting options, missing rules/links, and release-version edge cases |
| Release version | Payload changes and a higher version against the base commit; new-branch pushes versus root commits |
| Live host trials | Actual instruction selection, section reads, role calls, model/effort, and command outcomes; run separately from repository checks |

Structural checks do not prove model understanding or compliance. Regression tests use disposable sibling copies and temporary folders, so both the repository parent and temporary location must be writable. Record why unsupported checks, such as link/junction creation, were skipped; never count them as passes.

Parallel review stays read-only. Give reviewers the scope and acceptance criteria, the exact revision or diff and relevant files, and each verification command with its working directory, exit status, and success or failure evidence. State why any check was not run. Report missing, stale, or insufficient validation as `Validation Gap`; an observed failed check is FAIL. The parent owns fixes and focused retests, then reconciles findings against fresh evidence without recursive review. See `docs/codex-subagent-rules.md` and `docs/codex-team-agent-rules.md`.

The GitHub Actions workflow is configured to run regression, synchronization, structure, and release-version checks on Windows/Linux × Python 3.11/3.12. Verify the outcome in the run for the exact revision. `measure_load.py` reports normalized UTF-8 bytes; its bytes/4 heuristic is **not** actual token usage and excludes host/tool overhead.

## Evidence and simulation pointers

- [Five-round improvement report](docs/optimization-report-2026-09-06.md) — Core diet, AGENTS lean, routing, budgets.
- [Simulation-10 report](docs/simulation-10-report-2026-09-06.md) — context budget, model floor, sync, fence-aware sections, invariants (post PR #4/#5/#6/#7).
- Controlled behavior rubrics: `tests/Scorecard.md`, `tests/GoldenTest-015.md` … `tests/GoldenTest-040.md`.

Structural checks do not run live ChatGPT/Codex behavior trials. Official principles that informed routing (not proof of speed/accuracy gains): [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [selective skill loading](https://learn.chatgpt.com/docs/build-skills), [instruction clarity](https://developers.openai.com/api/docs/guides/latest-model) (checked 2026-09-06).

## License

[MIT License](LICENSE).
