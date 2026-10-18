# Distribution Baseline

This repository is a distributable instruction pack for multiple recipients and hosts. This baseline is the pack's maintenance contract, not an OpenAI certification or a promise that every host supports every feature. TaskForge defines native Codex role responsibilities and optional presets; a maintainer's client version, paths, credentials, memory, and successful local checks are not compatibility guarantees.

## Default Contract

| Area | Distribution baseline | Recipient-specific opt-in |
|---|---|---|
| Main model and reasoning | All entries preserve the current host selection; DEFAULT defines responsibilities, not model IDs | A justified, supported, authorized override |
| Subagents | Native DEFAULT uses registered model-inheriting roles; fixed Luna/Astra IDs require explicit PRESET opt-in; SUSPENDED allows unpinned roles only when separately requested; inherit permissions | Reviewed custom role files or a named model preset |
| Permission and tools | Preserve host policy, managed requirements, provider, integrations, and existing roles | Separately authorized changes; no privilege expansion to make tests pass |
| Memory | The pack does not enable memory or ship generated memory state | Supported host memory setup after privacy/support review |
| Installation | Copy the pack, verify its manifest, preserve conflicts and user files | Explicit conflict resolution after backup; never silent overwrite |
| Evidence | Static checks, live host behavior, and measured gains are separate | Private, sanitized trial records for a specific environment |

The standard does not add an active `.codex/config.toml`, change global `AGENTS.md`, enable multi-agent tools, or install personal agent definitions. The existing installer distributes examples under `docs/`; it does not activate them. Existing installation conflict rules still apply. Use one minimal entry and only relevant guides.

## Model-Inheriting Role Examples

For a Codex host that supports standalone custom agents, start with [Explorer](examples/codex-standard-agents/pack-explorer.toml), [Runner](examples/codex-standard-agents/pack-runner.toml), and [Reviewer](examples/codex-standard-agents/pack-reviewer.toml). These files contain only `name`, `description`, and `developer_instructions`. Omitting model and reasoning fields lets the host resolve them from its supported spawn settings, subagent defaults, and parent session; it does not force a particular model.

The names `pack_explorer`, `pack_runner`, and `pack_reviewer` avoid replacing built-in role names. Check for recipient conflicts anyway. After support and authorization checks, copy only selected files into that recipient's custom-agent directory and reconcile the [optional delegation snippet](examples/codex-standard-agents/AGENTS.snippet.md) with their existing instructions. Do not auto-apply it on pack installation. On a host without custom agents, retain the main-agent workflow and report only the affected delegation as unavailable. Follow the [DEFAULT registration procedure](codex-three-model-setup.md#register-default-roles) for active-home selection, conflict preservation, fresh-process calls, and native model/effort verification. The [2026-10-18 trial](host-verification-2026-10-18.md) records a successful personal registration; project-local discovery and other hosts still require their own checks.

Explorer and Reviewer must not edit. Runner executes only the main's specified verification, allowing its necessary temporary/cache/build outputs within granted permissions. These are behavioral restrictions: custom files do not create separate child sandboxes. For hard read-only isolation, restrict the whole parent session using supported controls. Do not add unsupported permission fields or silently replace the recipient's policy.

The [session policy](codex-three-model-setup.md#session-policy) defaults to model-inheriting role responsibilities. Sol/Luna/Astra fixed IDs are an explicit PRESET opt-in. Explicit model choices suspend automatic delegation for the conversation; new conversations applying TaskForge restore DEFAULT, not the previous conversation-only fixed-model opt-in, unless a separately approved host-wide PRESET policy applies. Resuming the same conversation preserves its state. Role registration remains a separately authorized host setup step, and instructions cannot force model switching or detect unexposed UI selections. Its observed versions and trials describe one environment. The [Memories example](codex-memories-maintenance.md) is also opt-in; no memory feature is activated by distributing its TOML documentation.

For a reviewed one-time setup that requests routing in every new conversation, use the [automatic global snippet](codex-three-model-setup.md#automatic-policy-for-every-new-session) instead of the skill-scoped snippet. The optional [Notion recorder](codex-notion-recording.md) requires an explicitly approved destination and six confirmed record fields. Neither example runs on plugin installation; fixed-model recording also respects conversation-scoped model overrides. [Observed host trials](host-verification-2026-10-16.md) are separate from static coverage of the distributable examples.

## Support and Change Validation

Official schema references checked 2026-10-15: [custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic). Verify current installed-host support before activating examples; do not infer a minimum client version from one maintainer's successful test.

| Recipient scenario | Acceptance criterion |
|---|---|
| New installation with no model override | No model/effort/permissions written by the pack; native session policy and required operational sections load without preloading configuration details; no automatic role registration |
| Customized model, disabled feature, or existing roles | Original recipient config and role bytes preserved; conflicts reported before replacement |
| Custom agents unavailable or name discovery stale | No invented API or role substitution; main performs permitted work, dependent trial marked unavailable |
| Restricted/offline host or denied verification command | No bypass, automatic install, or concealed PASS; required evidence remains a Validation Gap |
| Host/model/provider upgrade | Revalidate supported keys, role discovery, actual command outcomes, and observable model/effort; no guessed replacement model |
| Named preset selected | Check that recipient's exact model/effort access and authorization separately from the baseline |

Repository checks require Python 3.11+ and its standard library. The workflow defines Windows/Linux × Python 3.11/3.12 checks; a release report must link the actual run for that revision. This is not a macOS, ChatGPT, Codex-app, remote-host, or live model certification. Required [Golden Test 040](../tests/GoldenTest-040.md) covers the baseline contract; structural validation does not execute its scenarios.

For a distribution release, record the plugin version, exact revision, CI run link, each checked environment, command/exit/evidence, skipped or unavailable checks, and rollback instructions. Run `python scripts/check_release.py --base BASE_COMMIT` against the real pre-change commit. CI applies this read-only version gate to PRs and pushes; payload changes require a strictly higher numeric version. A new branch compares against the fetched default-branch tip, including its current version, rather than only the last commit or merge-base. An all-zero base is accepted only for a parentless root commit; existing history without an explicit base fails closed. Workflow-only and .gitignore-only changes are excluded. This does not require live trials to publish an honestly labeled instruction-only package. Test benign explicit/implicit delegation and negative cases on available recipient hosts using the [Scorecard](../tests/Scorecard.md). Missing live coverage remains unknown; it does not block publishing an honestly labeled instruction-only package, but it blocks claims of tested live behavior or performance in that environment.

Do not ship user settings, generated memory, private traces, machine-specific installation paths, or secrets. Keep optional integration dependencies separate. Restore only changed recipient files after an authorized opt-in trial, preserving later user edits; pack updates must not reset memory or credentials. Model or platform updates should change compatibility evidence and optional overrides when necessary, without overriding explicit session choices.
