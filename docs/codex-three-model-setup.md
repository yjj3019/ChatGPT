# Optional Sol / Luna / Astra Setup

This is a recipient-selected override of the [distribution baseline](distribution-standard.md). Use only when the user explicitly requests this three-model preset. The pack's normal routing remains model-independent and keeps the current session model. These examples are documentation assets, not active project configuration; the pack installer copies them under `docs/` without applying them to a user's Codex home. Existing installations still follow the README's manifest/conflict handling; new examples do not bypass those checks.

## Official Contract

Checked 2026-10-15 against [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

- Personal custom agents are standalone TOML files under `~/.codex/agents/`. Each requires `name`, `description`, and `developer_instructions`; `model` and `model_reasoning_effort` can override model behavior. The `name` field identifies the role, independently of the filename.
- Parent sessions govern permissions, providers, MCP servers, and service-tier preferences. An agent file's `sandbox_mode` or `approval_policy` does not create independent child permissions. These examples therefore omit those keys.
- Explorer/Reviewer no-edit rules are behavioral restrictions, not a separate read-only sandbox. Runner may create only the temporary files/cache/build outputs required by the parent's approved verification command. For hard read-only isolation, start the entire parent session read-only; do not weaken permissions merely to make a test pass.
- Agent instructions guide delegation but cannot guarantee that every task is routed correctly. Check the actual spawn/action evidence. Cost savings and equal code quality require measurement on representative tasks, not just configuration.

## Selected Preset

These exact IDs are the user's selected optional preset, not a universal roster or an automatic latest-model policy.

| Role | Model | Initial reasoning | Responsibility |
|---|---|---|---|
| Main Sol | `gpt-6.1-sol` | `medium` | Requirements, design, implementation, debugging, integration, final judgment |
| `luna_explorer` | `gpt-6-luna` | `high` | Read files/symbols/callers; return concise evidence and search coverage |
| `luna_runner` | `gpt-6-luna` | `low` | Execute only specified checks; summarize exits/errors without fixes |
| `astra_reviewer` | `gpt-6-astra` | `low` | Independent review before an important direction is finalized or after two failed fix/retest attempts |

Official subagent guidance suggests explicit model-compatible efforts; these are starting values. Reassess report quality and actual usage before increasing effort or claiming savings. Do not change the memory extraction/consolidation models as part of this preset; see the separate [Memories guide](codex-memories-maintenance.md).

## Apply Safely

1. Inspect the effective user config, global `AGENTS.md`, existing custom roles, project overrides, and managed requirements. Record actual app and CLI versions separately. Check `codex --version` and `codex --help` where the CLI is installed. Respect `CODEX_HOME` and host-specific config precedence.
2. Verify each selected ID and effort in the actual authenticated host. On a CLI that exposes it, `codex debug models` provides catalog evidence; confirm that subcommand in local help first. `--bundled`, an old cache, public API documentation, and a model's self-report alone do not establish current account access. Distinguish catalog evidence from a successful model call.
3. Keep existing settings if already correct. If a different main model or conflicting role/policy must be replaced, show the exact difference and obtain approval first. Back up only the affected files to a private location outside this public repository. Do not copy a real user config, memory store, credentials, or raw logs into the pack.
4. If approved and supported, merge the main-model setting into the effective user config: `model = "gpt-6.1-sol"`. Preserve a compatible existing effort, or select the preset's `medium` with authorization. Never paste duplicate TOML tables. Multi-agent may already be enabled; the current documented `agents.enabled` default is true. Check existing feature settings and do not add redundant flags. Use the mechanism supported by that installed host, without changing unrelated features.
5. Review and copy only the three chosen example role files to `~/.codex/agents/` (or the active Codex home): [Explorer](examples/codex-three-models/luna-explorer.toml), [Runner](examples/codex-three-models/luna-runner.toml), [Reviewer](examples/codex-three-models/astra-reviewer.toml). Check both filenames and `name` values for conflicts before writing. Do not copy the whole examples directory into active configuration.
6. Append or reconcile the [optional delegation snippet](examples/codex-three-models/AGENTS.snippet.md) with existing global guidance. Preserve original instructions and higher-priority rules. Do not append a duplicate marked block or treat the snippet as permission to ignore project constraints.
7. Start a new chat/process so role discovery can refresh. An existing chat may still expose only its original role list. Do not silently substitute another role or model when a name is unavailable.

## Verification and Rollback

Run repository checks from the README. TOML parsing validates examples, and [Golden Test 039](../tests/GoldenTest-039.md) defines behavior acceptance; neither executes real models or proves sandbox enforcement.

In a benign authorized host trial, invoke each **role name** without an explicit spawn model/effort so the role file is tested. Explorer should read a harmless fixture and cite lines; Runner should run one specified non-mutating command and report its exit/output. Call Astra only for the final important setup-direction review or after the specified two failures. Keep unrelated integrations out of the trial where supported. Inspect authoritative runtime model/effort metadata if exposed; report missing metadata as a Validation Gap rather than trusting self-identification. Verify that source/settings stayed unchanged. Do not equate a successful spawn with a successful command.

For update/rollback, preserve the prior compatible main-model choice, role files, and guidance. Revalidate version, account access, effort, role discovery, and the same acceptance criteria after changes. If a selected ID is unsupported, stop that delegation and let the main handle authorized work; do not cycle through guesses or expand permissions. Restore the affected prior files or move newly added roles outside the discovery directory. Remove only the added marked guidance block; use a full backup restore only if it would not overwrite later user changes. No force-push, memory reset, or credential change is part of recovery.

For any efficiency claim, compare matched tasks with identical acceptance criteria using the [Scorecard](../tests/Scorecard.md). Include delegation overhead, actual usage/cost when available, latency, omissions, and regressions. Report unmeasured dimensions explicitly.

## Evidence Required per Recipient

Record each recipient's actual host/version and account-visible models separately; no maintainer version is a minimum support guarantee. Catalog visibility, valid role-file syntax, role-name invocation, successful task execution, and authoritative runtime model/effort metadata are separate evidence gates.

A blocked fixture read or verification command is not a successful role trial. Missing native metadata stays unknown. Preserve original user settings and role files and report live behavior, permissions, and cost/quality outcomes only for the environment actually tested. Static distribution checks do not establish these outcomes on another host.
