# TaskForge Sol / Luna / Astra Session Setup

This is the native TaskForge skill's default Codex session policy under the [distribution baseline](distribution-standard.md). ChatGPT and legacy entries retain their current-model default. Role files remain documentation assets until explicitly configured; marketplace installation does not write a user's Codex home. Existing installation conflict handling still applies.

## Session Policy

DEFAULT requests `gpt-6.1-sol` (medium) for the main, `luna_explorer` / `gpt-6-luna` (high), `luna_runner` / `gpt-6-luna` (low), and `astra_reviewer` / `gpt-6-astra` (low). The main owns implementation and final judgment. Luna handles scoped exploration and specified verification; tiny tasks stay with the main. Astra reviews only before an important direction is finalized or after two failed fix/retest attempts for the same error. Child agents do not re-delegate.

| Event | Routing state |
|---|---|
| New conversation applying TaskForge, without an explicit model choice | DEFAULT: Sol main, Luna exploration/verification, conditional Astra review |
| Explicit user model choice, including Sol, or "use this model only" | SUSPENDED for the rest of this conversation; preserve the selected model/effort and stop pinned Luna/Astra routing |
| Further turns, compaction, or resuming the same conversation | Keep its existing state; do not reset suspension |
| Explicit request to re-enable the three-model preset | Return to DEFAULT after support checks |
| New conversation applying TaskForge | Return to DEFAULT; do not carry suspension from another conversation |

State is conversational guidance, not a persisted setting or a runtime state machine. Never write a global disable flag or reset user settings. An explicit model choice in the first request wins over the default immediately. An explicit choice remains an override even when its ID equals the default. Quoted text and the active model slug alone do not prove a manual selection.

Use host-exposed evidence for UI choices. If unavailable, tell the user to say **"use this model only" / "이 대화에서는 선택한 모델만 사용해"**. This instruction package cannot reliably intercept every model-picker action. It does not control app restart, and reopening an existing conversation does not reset its override. These limits must not be reported as tested automatic UI behavior.

DEFAULT requests the models/efforts in the table below; it does not change the running main model by instruction alone. Use only supported controls and registered roles. If Sol is not active and cannot be selected by supported controls, report that gap and continue authorized work on the current model; do not claim that Sol is running. Missing roles or account access similarly disable only dependent delegation. Do not silently install roles, guess alternate models, or expand permissions.

In SUSPENDED, handle work with the selected main model. If the user separately requests subagents, use supported unpinned roles that inherit the chosen model/effort; fixed-model role files must not override the user's choice. Existing permissions and higher-priority instructions always apply.

## Official Contract

Checked 2026-10-15 against [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) and the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

- Personal custom agents are standalone TOML files under `~/.codex/agents/`. Each requires `name`, `description`, and `developer_instructions`; `model` and `model_reasoning_effort` can override model behavior. The `name` field identifies the role, independently of the filename.
- Parent sessions govern permissions, providers, MCP servers, and service-tier preferences. An agent file's `sandbox_mode` or `approval_policy` does not create independent child permissions. These examples therefore omit those keys.
- Explorer/Reviewer no-edit rules are behavioral restrictions, not a separate read-only sandbox. Runner may create only the temporary files/cache/build outputs required by the parent's approved verification command. For hard read-only isolation, start the entire parent session read-only; do not weaken permissions merely to make a test pass.
- Agent instructions guide delegation but cannot guarantee that every task is routed correctly. Check the actual spawn/action evidence. Cost savings and equal code quality require measurement on representative tasks, not just configuration.

## Selected Preset

These exact IDs define TaskForge's default native session preset for environments where they have been verified. They are not a universal roster or an automatic latest-model policy. Recipients must confirm model availability and role registration in their own host before use. If the IDs are unavailable, use model-inheriting roles or let the main agent handle authorized work. Manual session overrides take precedence.

| Role | Model | Initial reasoning | Responsibility |
|---|---|---|---|
| Main Sol | `gpt-6.1-sol` | `medium` | Requirements, design, implementation, debugging, integration, final judgment |
| `luna_explorer` | `gpt-6-luna` | `high` | Read files/symbols/callers; return concise evidence and search coverage |
| `luna_runner` | `gpt-6-luna` | `low` | Execute only specified checks; summarize exits/errors without fixes |
| `astra_reviewer` | `gpt-6-astra` | `low` | Independent review before an important direction is finalized or after two failed fix/retest attempts |

Official subagent guidance suggests explicit model-compatible efforts; these are starting values. Reassess report quality and actual usage before increasing effort or claiming savings. Do not change the memory extraction/consolidation models as part of this preset; see the separate [Memories guide](codex-memories-maintenance.md).

## Model ID Inheritance Priority

When resolving a model and effort for a role, apply the following order. Use the first matching rule; do not fall through.

| Priority | Condition | Model / effort applied | Notes |
|---|---|---|---|
| 1 | User explicitly selected a model for this conversation, or requested "use this model only" | The user-selected model and effort | SUSPENDED. Fixed-ID role files must not override this. |
| 2 | Role TOML omits both `model` and `model_reasoning_effort` | Host inheritance rules (parent session or host default) | Recommended default. See `docs/examples/codex-standard-agents/`. |
| 3 | Role TOML specifies a model ID that is **actually usable** in the current account | The ID and effort from the TOML | Catalog visibility alone is not enough; a successful call is required. |
| 4 | Specified ID is unavailable, or the role is not registered | Inherit the current main model (or host default) | Stop that delegation; main handles the work. Report as Validation Gap. |
| 5 | None of the above | Do not delegate | Main handles the work directly. |

### Rules
- Prefer inheritance. Fixed IDs such as `gpt-6.1-sol` are optional presets verified in specific environments, not distribution defaults.
- If a role file contains a model ID, the recipient must confirm that ID is callable in their own host before use.
- Do not silently substitute another model when the specified ID is unavailable. Hand the work to the main and report the gap.
- Effort follows the same priority. If a specified effort is unsupported, use the host default or the parent session's effort.
- This order is evaluated per conversation. A new conversation restarts evaluation from priority 1.

### Recipient guidance
1. Prefer role files that omit `model` and `model_reasoning_effort` when possible.
2. Use a fixed ID only after confirming a successful call in the target host (for example via `codex debug models` when available).
3. Do not register a role with an unverified ID.

## When Not to Delegate

Keep the work with the main agent when any of the following apply. Do not spawn Luna or Astra in these cases.

- The change touches one file or fewer and is limited to a rename, comment, whitespace, or trivial local edit.
- The expected effort is under roughly one minute of main-agent work and does not require external evidence gathering.
- The task is a pure lookup or single-fact question with no code or document modification.
- The user explicitly said to handle it alone or not to use subagents.
- Role discovery failed or the required model/effort is unavailable (see inheritance priority 4–5).

When in doubt and the task is small, prefer the main. Report the decision only if the user asked about routing.

## Astra Review Triggers

Call Astra only in the following cases. Do not call it for routine progress updates or minor edits.

| Trigger | Examples |
|---|---|
| Before finalizing an important direction | Architecture or public API contract change; security-sensitive modification; change that affects three or more files or crosses a service boundary; irreversible data or configuration migration |
| After two failed fix/retest cycles | The same error or acceptance criterion fails twice in a row after attempted fixes; main has already applied one corrective change and retested |

Astra receives a narrow packet: the proposed direction or the failing evidence, the acceptance criteria, and the relevant file paths. It does not implement fixes. After Astra reports, the main decides whether to proceed, revise, or stop.

## Context Packet Standard

When the main delegates, send a narrow packet. Do not forward the full conversation or unrelated files.

### Main → child (minimum fields)
- Goal of this delegation
- Constraints that must not be violated
- Relevant file paths (and line ranges when known)
- Acceptance criteria for this subtask
- Evidence already confirmed (so the child does not re-search the same items)

### Child → main (standard return)
- Conclusion (one or two sentences)
- Evidence with file:line citations
- Items not confirmed and why
- Suggested next action for the main (no implementation)

### Size limit
Keep the packet under roughly 20% of the current context window or a short summary if it would exceed that. Prefer a condensed packet over a large paste. The child does not re-delegate and does not edit source unless it is the Runner executing a specified non-mutating check.

## Role Discovery Failure Wording

When a required role is not discovered or cannot be used, tell the user plainly and continue with the main. Do not invent a substitute role or model.

Standard phrasing (use the language matching the conversation):
- Korean: "luna_explorer 역할을 찾을 수 없어 메인에서 직접 처리합니다."
- English: "luna_explorer is not available in this session; the main will handle the work."

Record the gap as a Validation Gap in any host trial notes. Do not claim the role ran.

## Retry Policy

Distinguish temporary and permanent failures before falling back to the main.

| Failure type | Examples | Action |
|---|---|---|
| Temporary | Timeout, transient model unavailability, brief discovery delay | Retry once. If it fails again, fall back to the main and report. |
| Permanent | Role not registered, model ID not callable, permission denied | Do not retry. Fall back immediately and report as Validation Gap. |

Do not loop retries. One attempt is the maximum for temporary failures.

## Cost and Latency Notice

When the main decides to delegate and the expected delay or cost is material, tell the user in one line before proceeding.

Example: "Delegating to luna_explorer; this may add a short delay."

Skip the notice for trivial or already-approved delegations. Do not claim measured savings without matched-task evidence.

## Model Availability Checklist

Before registering or relying on a fixed model ID, distinguish these evidence levels. A higher level does not imply a lower one.

| Level | What it proves | What it does not prove |
|---|---|---|
| Catalog / `codex debug models` | The ID appears in the host catalog | Account access or a successful call |
| Role file accepted | Syntax and name registration succeeded | The model can be invoked |
| Successful role-name call | The host spawned the role | Runtime model/effort matched the file |
| Authoritative runtime metadata | The host recorded the actual model and effort | Quality or cost outcome |

Use a fixed ID only after a successful call is confirmed in the target account. If only catalog evidence exists, prefer a model-inheriting role or let the main handle the work.

## Recipient Verification Template

Use this checklist when validating a new host. Record results privately; do not publish raw logs or credentials.

- [ ] Host and CLI version recorded
- [ ] Model IDs confirmed callable (not only catalog-visible)
- [ ] Role discovery succeeded in a fresh process
- [ ] Context packet delivered and returned in the standard format
- [ ] Runtime model/effort metadata observed
- [ ] Protected files unchanged
- [ ] Any gap recorded as Validation Gap

A completed checklist is evidence for that environment only.

## Configure Host Roles Safely

1. Inspect the effective user config, global `AGENTS.md`, existing custom roles, project overrides, and managed requirements. Record actual app and CLI versions separately. Check `codex --version` and `codex --help` where the CLI is installed. Respect `CODEX_HOME` and host-specific config precedence.
2. Verify each selected ID and effort in the actual authenticated host. On a CLI that exposes it, `codex debug models` provides catalog evidence; confirm that subcommand in local help first. `--bundled`, an old cache, public API documentation, and a model's self-report alone do not establish current account access. Distinguish catalog evidence from a successful model call.
3. Keep existing settings if already correct. If a different main model or conflicting role/policy must be replaced, show the exact difference and obtain approval first. Back up only the affected files to a private location outside this public repository. Do not copy a real user config, memory store, credentials, or raw logs into the pack.
4. If approved and supported, merge the main-model setting into the effective user config: `model = "gpt-6.1-sol"`. Preserve a compatible existing effort, or select the preset's `medium` with authorization. Never paste duplicate TOML tables. Multi-agent may already be enabled; the current documented `agents.enabled` default is true. Check existing feature settings and do not add redundant flags. Use the mechanism supported by that installed host, without changing unrelated features.
5. Review and copy only the three chosen example role files to `~/.codex/agents/` (or the active Codex home): [Explorer](examples/codex-three-models/luna-explorer.toml), [Runner](examples/codex-three-models/luna-runner.toml), [Reviewer](examples/codex-three-models/astra-reviewer.toml). Check both filenames and `name` values for conflicts before writing. Do not copy the whole examples directory into active configuration.
6. Append or reconcile the [optional delegation snippet](examples/codex-three-models/AGENTS.snippet.md) with existing global guidance. Preserve original instructions and higher-priority rules. Do not append a duplicate marked block or treat the snippet as permission to ignore project constraints.
7. Start a new chat/process so role discovery can refresh. An existing chat may still expose only its original role list. Do not silently substitute another role or model when a name is unavailable.

## Automatic Policy for Every New Session

After a one-time authorized setup, the policy can load in every new conversation for that Codex home without manually invoking TaskForge. Use the [automatic snippet](examples/codex-three-models/AGENTS.auto.snippet.md) instead of the skill-scoped [original snippet](examples/codex-three-models/AGENTS.snippet.md). Choose one; do not append both.

### Approval steps before applying the automatic snippet
1. Show the exact diff that will be written to the effective global `AGENTS.md` (or its resolved target if it is a symlink).
2. Record the pre-change hash of the target file.
3. Obtain explicit user approval for that specific diff. Do not apply on implied consent.
4. After writing, re-hash the file and confirm only the intended block changed.
5. Keep a private backup of the prior file outside the public repository.

The markers in the snippet identify the block for later removal. Removing only that marked block restores the prior guidance without touching unrelated content. A full-file restore is required only if later user edits would otherwise be lost.

Inspect and privately back up the effective home's config.toml, selected role files and global AGENTS.md. Keep correct settings. If authorized changes are needed, merge the main defaults below into existing root keys rather than replacing the file or creating duplicate tables:

```toml
model = "gpt-6.1-sol"
model_reasoning_effort = "medium"
```

Register the three role examples using the earlier support/conflict checks. Reconcile the automatic snippet into that home's global AGENTS.md. When migrating from the original snippet, replace only its reviewed marked block, preserving unrelated instructions and later user edits. The marker pairs identify the blocks; they are not activation flags.

Check default Codex and each explicitly selected Orca account separately: an Orca account may use a different CODEX_HOME. Do not infer account paths, copy authentication, enumerate/change every account, or copy a real profile into the public pack. If global AGENTS.md is already a symbolic link to the default home, back up and edit its resolved target once, preserving the link. Start a new session and verify role discovery, native model/effort records and actual task outcomes without passing explicit model/effort to role calls.

The automatic snippet changes when the policy is requested, not the suspension rules. Explicit single-model choices still win for that conversation; reloading the skill, resuming, compaction or restarting the app does not reset that choice. Instructions cannot detect unexposed UI selections or change an already-running main model. Higher-priority/project restrictions still apply. Marketplace installation/update never performs this host setup or grants permissions.

An optional [Luna/low Notion recorder](codex-notion-recording.md) handles approved writes separately from the verification-only Runner. It is not part of the three required roles. See the [sanitized host verification](host-verification-2026-10-16.md) for observed successes and remaining gaps.

## Verification and Rollback

Run repository checks from the README. TOML parsing validates examples, and [Golden Test 039](../tests/GoldenTest-039.md) defines behavior acceptance; neither executes real models or proves sandbox enforcement.

In a benign authorized host trial, invoke each **role name** without an explicit spawn model/effort so the role file is tested. Explorer should read a harmless fixture and cite lines; Runner should run one specified non-mutating command and report its exit/output. Call Astra only for the final important setup-direction review or after the specified two failures. Keep unrelated integrations out of the trial where supported. Inspect authoritative runtime model/effort metadata if exposed; report missing metadata as a Validation Gap rather than trusting self-identification. Verify that source/settings stayed unchanged. Do not equate a successful spawn with a successful command.

For update/rollback, preserve the prior compatible main-model choice, role files, and guidance. Revalidate version, account access, effort, role discovery, and the same acceptance criteria after changes. If a selected ID is unsupported, stop that delegation and let the main handle authorized work; do not cycle through guesses or expand permissions. Restore the affected prior files or move newly added roles outside the discovery directory. Remove only the added marked guidance block; use a full backup restore only if it would not overwrite later user changes. No force-push, memory reset, or credential change is part of recovery.

For any efficiency claim, compare matched tasks with identical acceptance criteria using the [Scorecard](../tests/Scorecard.md). Include delegation overhead, actual usage/cost when available, latency, omissions, and regressions. Report unmeasured dimensions explicitly.

## Evidence Required per Recipient

Record each recipient's actual host/version and account-visible models separately; no maintainer version is a minimum support guarantee. Catalog visibility, valid role-file syntax, role-name invocation, successful task execution, and authoritative runtime model/effort metadata are separate evidence gates.

A blocked fixture read or verification command is not a successful role trial. Missing native metadata stays unknown. Preserve original user settings and role files and report live behavior, permissions, and cost/quality outcomes only for the environment actually tested. Static distribution checks do not establish these outcomes on another host.
