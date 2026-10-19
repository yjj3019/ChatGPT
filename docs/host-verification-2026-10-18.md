# Host Verification — 2026-10-18

Sanitized observations from one authorized Windows Codex home. The tested skill and unchanged role examples came from TaskForge 2.3.0, source commit `c6e7b79aba7df0ff67e16bc7a9b3732938d4ba06` (merged as `b7d61d4e8d340bcb94af32f2b4bfdcff4a0dffe3`). Version 2.3.1 originally published those instructions and observations. Subsequent installed 2.3.1 trials are recorded separately below; 2.3.2 adds that evidence without claiming a live 2.3.2 trial. Private paths, account/session IDs, user configuration, credentials, and raw traces are omitted.

## Environment and evidence

- CLI: `0.163.0`; desktop session runtime metadata: `0.163.0-alpha.10.2`. These are observed versions, not minimum support requirements.
- Existing main: `gpt-6.1-sol` with `medium` reasoning. These values are evidence, not new distribution defaults.
- Fresh authenticated CLI sessions used a read-only parent sandbox. Role calls passed no explicit model or effort. Native session/turn records established actual parent/child model and effort, separately from tool results.
- The installed cache initially exposed 2.2.1; during fresh CLI execution it exposed 2.3.0. The read 2.3.0 skill matched the source text after normalizing line endings. This observation does not prescribe an automatic-update mechanism.

## Missing role registration and resolution

Actual `pack_explorer`, `pack_runner`, and `pack_reviewer` calls returned `unknown agent_type`. The personal `agents/` directory lacked those definitions. The project-local trial copies were also not discovered; the exact project-layer loading cause was not established. A pack installation, example file, or valid TOML alone did not establish role availability.

After authorization, only the three unchanged [model-inheriting examples](distribution-standard.md#model-inheriting-role-examples) were added to the active Codex home's personal `agents/` directory. Their names did not conflict with existing roles; none specifies model, effort, or permission overrides. Existing configuration, global guidance, fixed-model roles, project trust and security settings were preserved. A fresh CLI process then recognized and executed all three roles. No trust setting was weakened.

`codex debug prompt-input` did not include the complete tool role catalog. Absence of role names there was not treated as conclusive discovery evidence; acceptance used actual calls and native runtime records.

## Model-inheriting DEFAULT trials

DEFAULT was explicitly requested for these trials, overriding the existing host-wide fixed preset for the test only. Permanent routing policy was not changed.

| Role | Actual task result | Native runtime model / reasoning |
|---|---|---|
| Parent | Owned orchestration and final judgment; no model/effort switch | `gpt-6.1-sol` / `medium` |
| `pack_explorer` | Read the exact existing fixture `plugin.json`; name `taskforge`, version `2.3.0`, read exit 0 | `gpt-6.1-sol` / `medium` |
| `pack_runner` | Ran only the specified `python --version`; exit 0, `Python 3.14.4` | `gpt-6.1-sol` / `medium` |
| `pack_reviewer` | Read the three role TOMLs with exit 0 and independently reviewed the important registration-retention decision | `gpt-6.1-sol` / `medium` |

The initial Explorer task failed with exit 1 because the trial main supplied a nonexistent `.claude-plugin/plugin.json` path. That failure was retained, not reclassified as a PASS. After confirming completion, only the caller input was corrected to the fixture's verified absolute path; a fresh-context Explorer call succeeded. Runner and Reviewer were not rerun. The Reviewer's original recommendation was conditional on the failed read and unavailable-to-it runtime metadata; the outer verifier reconciled that recommendation with the corrected read and native metadata. A child completion or parent CLI exit 0 alone was not accepted as task success.

All accepted child calls used the parent's model and effort without spawn overrides. Existing protected configuration and role-file hashes stayed unchanged; only the three intended personal role files were added. The repository stayed clean during the host trials.

## Installed 2.3.1 CLI and app trials — 2026-10-18–19

The installed plugin was updated to 2.3.1 and its key files were compared with the source after line-ending normalization. Existing configuration and personal role files were preserved. A fresh CLI trial read the installed skill and resolved guidance; its inherited Runner exited 0 with `INSTALLED_TASKFORGE_OK 2.3.1`. Native parent/child records showed `gpt-6.1-sol` / `medium`, without spawn model/effort overrides.

An older app conversation read the installed 2.3.1 guidance but returned `unknown agent_type` for `pack_runner`. That failed call remains a failure; its precise retained-catalog loading cause was not established. A separately authorized new app conversation then loaded the installed skill, root `AGENTS.md`, and required operational sections. Explorer read the exact installed root `plugin.json`, reporting `taskforge` / `2.3.1` with exit 0. Runner exited 0 with `CODEX_APP_TASKFORGE_OK 2.3.1`. Native records identified the desktop origin and linked both children to this app conversation; all three used `gpt-6.1-sol` / `medium`. Neither spawn supplied model or effort.

On 2026-10-19 (Asia/Seoul), after the user reported fully restarting the app, the same verification conversation was reused without creating another conversation. DEFAULT was explicitly re-enabled for this trial only; no automatic reset was inferred. The installed skill and required guidance were read again with exit 0.

| Post-restart check | Observed result |
|---|---|
| `pack_explorer` | Installed root manifest: `name=taskforge`, `version=2.3.1`; read exit 0 |
| `pack_runner` | Specified version/document-presence assertion: exit 0, `CODEX_APP_RESTART_TASKFORGE_OK 2.3.1` |
| Native model / effort | Parent and both new children: `gpt-6.1-sol` / `medium`; no spawn overrides; correct parent linkage and completion |
| Current app model label | Controller conversation displayed `GPT-6.1 Sol Medium`; this was observed separately from the verification conversation runtime |

The first screen capture did not match the selected app and was discarded. After refreshing window selection and activating the returned target, the current label was observed. The window identified itself as `ChatGPT.exe` in ChatGPT mode, so further UI input stopped under the Computer Use restriction on ChatGPT desktop UI automation. The model menu was not opened and no selection was changed. No UI selection event, automatic suspension/reset, or general restart behavior was established. App-tool delays and timeouts were kept separate from successful role execution. Reviewer was not invoked because its trigger did not apply. Source, installation, personal roles, and global settings were not changed by these app trials.

## Other observed trials and limits

- Existing PRESET roles completed: `luna_explorer` used `gpt-6-luna/high`, `luna_runner` used `gpt-6-luna/low`, and `astra_reviewer` used `gpt-6-astra/low`. File reads, the specified harmless Runner assertion and setup review were checked separately from native model metadata. These successes did not substitute for DEFAULT verification.
- An explicit `$taskforge` rewrite request read the installed 2.3.0 skill and its resolved `AGENTS.md`, avoided delegation, and preserved the statement that remote deployment was unverified.
- In a resumed session, an explicit single-model request resulted in no additional role calls and retained `gpt-6.1-sol/medium`. Quoted model-switch instructions were not acted on. This was a spot check, not all state transitions.
- Existing hook-timeout and legacy-skill frontmatter diagnostics remained separate host warnings; this work did not repair those unrelated components.

These trials do not establish UI model-picker detection, automatic switching, every future task, compaction or general restart behavior, other accounts/platforms/models, or quality/cost/latency improvements. The post-restart observation above is limited to an explicitly re-enabled existing conversation after a user-reported restart. Existing chats may retain their earlier role-discovery snapshot; use a new chat/process when registering roles. Follow the [DEFAULT registration procedure](codex-three-model-setup.md#register-default-roles) on each recipient host; plugin updates still do not write personal configuration or activate roles automatically.
