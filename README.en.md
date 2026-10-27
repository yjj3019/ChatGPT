# TaskForge for ChatGPT

**Task-scoped guidance** for code review, operations analysis and document work in ChatGPT and Codex.
Load only the relevant guides and report results with evidence.

[한국어](README.md) | English · [Distribution principles](docs/distribution-standard.md) · [License](LICENSE)

## Quick start — Codex app

Check command support with `codex plugin --help` and `codex plugin marketplace --help`, then run:

```text
codex plugin marketplace add yjj3019/ChatGPT --ref main
codex plugin add taskforge-for-chatgpt@yjj3019
```

Restart the app and make a request such as:

> Apply TaskForge for ChatGPT to review this code.

```text
codex plugin list --marketplace yjj3019 --json
```

Check the installed version and the enabled state in the app's Plugins page. This is a GitHub-backed marketplace, separate from review or listing in the public plugin directory.

## Update and remove

Back up the existing plugin settings and any user changes inside its cache. **Confirm marketplace refresh succeeds before** removing and reinstalling the plugin, then check the installed version.

```text
codex plugin marketplace upgrade yjj3019
```

Run the following commands in order only after refresh succeeds:

```text
codex plugin remove taskforge-for-chatgpt@yjj3019
codex plugin add taskforge-for-chatgpt@yjj3019
codex plugin list --marketplace yjj3019 --json
```

Keep the existing installation if refresh fails. Some Windows CLI versions fail when replacing an installed cache; do not remove the working plugin first without a recoverable backup. If reinstall fails, restore the retained previous version and check installation and enabled state.

To remove only the plugin, use `codex plugin remove taskforge-for-chatgpt@yjj3019`. Unregister the marketplace with `codex plugin marketplace remove yjj3019` only when it is no longer needed. Manage Python copies and Git clones separately.

## Other environments

### ChatGPT Project

1. Put [CHATGPT.md](CHATGPT.md) in Project Instructions.
2. Provide only the required `docs/` files as project knowledge.
3. Check actual access to the selected guide.

The full reference and [one-shot instructions](docs/chatgpt-5.5-all-in-one-instructions.md) are alternative entry points. For ordinary work, use one entry and one or two relevant guides.

<details>
<summary>Python installation — other skill-style hosts</summary>

Requires Python 3.11+ and the standard library. Use this copy-based setup for Claude, Grok, Cursor and AGENTS-compatible hosts.

```bash
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
python3 scripts/install_pack.py --auto
```

| Option | Purpose |
|---|---|
| `--dest <path>` | Set the target skill root. Mutually exclusive with `--auto` |
| `--with-tests` | Include tests and evaluation materials |
| `--dry-run` | Check targets and conflicts without writing |
| `--check` | Verify a Python installation's integrity |
| `--force` | Replace the entire pack, including added user files. Back up first |

Install sequentially when using the same target. Identical installations are skipped; changed installations are preserved by default. `--check` does not verify marketplace state or publisher authenticity.

Enabling both a marketplace installation and a Python copy can produce duplicate discovery. When switching, back up the old pack and retain it outside every active skills root.

</details>

<details>
<summary>Previous plugins and older identities</summary>

### Version 3 migration

An existing `taskforge@yjj3019` does not automatically move to the new ID. Back up the installation list, settings and user changes, then check that the new ID is available.

```text
codex plugin marketplace upgrade yjj3019
codex plugin list --marketplace yjj3019 --available --json
codex plugin remove taskforge@yjj3019
codex plugin add taskforge-for-chatgpt@yjj3019
```

Remove the old ID only after confirming the new ID can be installed. Restore the retained old version if installation fails. Preserve model, permission, role and memory settings.

For the older `chatgpt-transfer@yjj3019-chatgpt`, confirm the new marketplace registration and installation before retiring the old plugin and registration. Do not leave both IDs active.

For Python's `chatgpt-transfer/` or `taskforge/` copies, back up the entire pack and move it outside every active skills root before installing the new one. The installer stops on a detected old ID even with `--force`. Do not combine old and new manifests.

Commands for restoring a specific 2.x version remain in the [migration and recovery record from 3.0.6](https://github.com/yjj3019/ChatGPT/blob/654e954870bd522d7be4aa5d8159b05eeda65add/README.en.md#version-3-migration). Check the record's stated version and environment before using them.

</details>

## Models, roles and application checks

- **DEFAULT:** Preserve the current model and reasoning effort. Use registered `pack_explorer`, `pack_runner` and `pack_reviewer` roles only when useful; keep small tasks with the main agent.
- **PRESET:** Use fixed Sol/Luna/Astra settings only after an explicit opt-in and support/access checks.
- **SUSPENDED:** An explicit model choice stops automatic delegation for that conversation. Inherited subagents require a separate request.

Resuming, compaction and app restart do not reset the state. New conversations start in DEFAULT unless a separately approved host-wide PRESET policy applies. Installation does not activate roles, personal settings or memory, or switch the main model. See the [session policy](docs/codex-three-model-setup.md#session-policy) and [role registration](docs/codex-three-model-setup.md#register-default-roles).

Mark missing roles or required evidence as a `Validation Gap`. If a new skill is absent from an existing conversation, check installation/enabled state and discovery in a new conversation separately. `forceReload` rescans disk metadata; it does not guarantee replacement of the entire existing context. Preserve the existing conversation.

<details>
<summary>Check the actual host after setup</summary>

File presence does not prove instructions were loaded. A ChatGPT Project does not grant access to local folders. Upload files or provide them through an allowed connection.

1. Record the surface (Chat, ChatGPT Work, Codex, API), client/version, authentication method, and primary folder or `cwd`.
2. Check the active `AGENTS.md` source and global/parent instructions, including `AGENTS.override.md`. See the [host check guide](docs/codex-operations-rules.md#host-setup-smoke-check) for the default combined 32 KiB limit and `project_doc_max_bytes`.
3. Check access and actual reads of the selected guide, plus the required role's execution result. Verify model and reasoning effort through host-exposed runtime evidence.

Static repository checks do not replace live smoke tests. [Surface/model checks](docs/chatgpt-codex-model-routing.md#verify-the-product-surface) · [Official Projects guide](https://learn.chatgpt.com/docs/projects) (related guidance checked: 2026-10-10).

</details>

## Find a guide

| Task | Guide |
|---|---|
| Core rules, evidence and completion | [Core](docs/chatgpt-5.5-project-instructions.md) · [Operational Integrity](docs/chatgpt-operational-integrity-rules.md) |
| Implementation, debugging and code review | [Coding](docs/chatgpt-coding-rules.md) |
| Architecture, RCA, research, SOP and security | [Engineering](docs/chatgpt-engineering-task-rules.md) — matching section only |
| Infrastructure and technical domains | [Domain packs](docs/chatgpt-domain-packs.md) — matching section only |
| Meetings, presentations, executive summaries and PDF translation | [Knowledge work](docs/chatgpt-knowledge-work-rules.md) |
| Proposals, blogs and Office | [Proposals](docs/chatgpt-proposal-review-rules.md) · [Blogs](docs/chatgpt-blog-rules.md) · [Office](docs/codex-office-agent-rules.md) |
| Models, operations and delegation | [Model selection](docs/chatgpt-codex-model-routing.md) · [Operations](docs/codex-operations-rules.md) · [Subagents](docs/codex-subagent-rules.md) · [Team gates](docs/codex-team-agent-rules.md) |
| Optional integrations | [Memories](docs/codex-memories-maintenance.md) · [Notion](docs/codex-notion-recording.md) |
| Prompts and full reference | [Task prompts](prompts/chatgpt-task-prompts.md) · [Prompt guidance](docs/codex-prompt-engineering-rules.md) · [Full reference](docs/chatgpt-transfer-instructions.md) |

The `5.5` in historical filenames is for compatibility; it does not require that model. Do not preload the full reference or every guide.

Design evidence and history: [AI-Harness comparison](docs/ai-harness-adoption.md) · [Ponytail comparison](docs/ponytail-adoption.md) · [Evaluation criteria](tests/Scorecard.md) · [Host trial history](docs/host-verification-2026-10-18.md) · [Windows/Orca troubleshooting](docs/host-troubleshooting.md).

<details>
<summary>Repository development and checks</summary>

Requires Python 3.11+ and the standard library only. Repository checks need no package installation, API key or model call. Edit canonical sources, then synchronize generated documents.

```text
python scripts/sync_runtime.py
python scripts/sync_runtime.py --check
python scripts/validate_framework.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/measure_load.py
python scripts/install_pack.py --check
python scripts/check_release.py --base BASE_COMMIT
```

Replace `BASE_COMMIT` with the actual pre-change commit. Bump `plugin.json` for distributed changes and record the exact revision, CI outcome and validation scope with a release. Check source ZIPs with structural validation; the installer's source `--check` requires a Git checkout.

CI covers Windows/Linux × Python 3.11/3.12. The load estimator's bytes/4 figure is not actual token usage. During source updates, follow the [upstream review procedure](docs/upstream-review.md) for Ponytail/Karpathy changes. This creates no background monitor. Follow the [repository language policy](docs/language-policy.md) for shared sources and localized guides.

</details>

## License

[MIT License](LICENSE).
