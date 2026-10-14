# Codex Memories and Model Updates

Optional setup/maintenance guide; load only for a Memories or model-update task. This pack distributes instructions, not a Codex runtime or an automatic model router. Installing it does not enable Memories, edit host configuration, or migrate memory state.

## Verified Scope

Official sources checked 2026-10-14: [Memories](https://learn.chatgpt.com/docs/customization/memories), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [config locations and precedence](https://learn.chatgpt.com/docs/config-file/config-basic).

- Local Codex Memories and ChatGPT web memory have separate stores/controls. ChatGPT Work does not use the local Codex memory store.
- `features.memories` enables the local feature (off by default). `memories.generate_memories` and `memories.use_memories` control generation inputs and use, respectively; their documented defaults are true.
- `memories.extract_model` and `memories.consolidation_model` are optional overrides for per-chat extraction and global consolidation. Omitting them delegates selection to the installed host's defaults; it does not mean "use the conversation model" or "always use the newest model".
- Generation is asynchronous and subject to idle-time, eligibility, and remaining-quota gates. No immediate memory file is not proof of failure.
- These sources establish settings and behavior, not a measured speed, accuracy, or cost advantage for any model pair. This repository has not run a live comparison.

Keep mandatory rules in `AGENTS.md`/checked-in docs. Memories are recall evidence, not authority to override current instructions. Never commit generated memory, conversations, credentials, or a real user config to this public pack.

## Default Configuration

After checking installed-host support and obtaining authorization for the user's configuration change, merge these keys into the effective user config (normally `~/.codex/config.toml`, or the selected `CODEX_HOME`). Inspect existing tables and precedence first: do not paste duplicate tables or replace unrelated settings. This is a documentation example, not a file the installer applies.

```toml
[features]
memories = true

[memories]
generate_memories = true
use_memories = true
```

There is deliberately no model ID or model roster in this example. Leave both model override keys absent unless a measured need justifies pinning. This preserves host-managed defaults across upgrades, but defaults can change and still require regression checks. For a read-only memory mode, set `generate_memories = false` while keeping `use_memories = true`; this prevents new generation inputs, not deletion of existing state. Setting both false is not a memory reset either.

## Version and Support Gate

Record sanitized evidence locally, outside this public repository. Do not dump a whole config or raw logs. No guessed minimum version, static model allowlist, or API catalog can certify support on a user's Codex host.

| Gate | Evidence required | If unavailable or failed |
|---|---|---|
| Host identity | Actual surface, installed client/host version, authentication/provider, config source/precedence; CLI: `codex --version` and `codex --help`; app/remote host: its own version | `[unverified]`; do not apply new keys/overrides |
| Key support | Release-matched configuration documentation/schema for that installed host, plus successful host config loading without unknown-key warnings | Keep prior working config; a current online schema alone does not establish older-client support |
| Feature availability | Effective feature setting and account/workspace controls; `/memories` or documented equivalent when exposed by that client | Keep Memories disabled or prior working behavior; do not bypass managed controls |
| Override access | Exact ID supported by the same host/provider/authentication for the intended memory role, then an authorized extraction/consolidation smoke trial | Do not apply a new pin; a chat picker or API model listing alone is insufficient |
| Trial outcome | Extraction and consolidation observed separately, existing memory still readable, no critical output-contract regression | Keep/revert decision; missing trial evidence is a Validation Gap, not PASS |

Do not invent a `codex models` command, assume environment-variable expansion in TOML, or infer support from a model-name prefix. Confirm commands against that client's help. If release-matched documentation is unavailable, record the gap and defer the override rather than guessing support.

## Optional Override and Safe Fallback

When justified and authorized, set only the needed `extract_model` and/or `consolidation_model` key under the existing `[memories]` table to an exact ID verified by the support gate. Record which role is pinned, why, host/version/provider, verification date, and the private evidence reference. Recheck after a host/model/provider/authentication change or an availability/deprecation notice. Do not automatically replace a pin with a "latest" alias or numerically newer ID.

The following is an operator procedure, not a claim that Codex automatically retries on another model. The pack does not intercept model failures or silently rewrite configuration.

| Observed condition | Safe action |
|---|---|
| No overrides | Keep host defaults; rerun update checks when host defaults change |
| New override unverified, inaccessible, or wrong type | Reject the candidate; keep the previous working configuration |
| Existing pin explicitly unsupported/retired for its memory role | With config-change authorization, remove only the affected override key (not an empty string), reload/restart as that host documents, then verify the host default for that role |
| Authentication/permission failure, quota/rate limit, timeout, or unknown error | Stop the attempted change and diagnose the actual error; do not rotate through models, change credentials, increase spend, or weaken controls |
| Host default also fails or key/feature support is removed | Restore compatible prior settings if safe; otherwise disable the affected memory behavior using supported controls and continue required work from checked-in docs |
| Memory quality regresses | Revert the candidate settings; if existing memories are suspect, disable their use with supported controls pending review; do not assume config rollback restores memory contents |

Before an authorized trial, preserve the previous config and, if state recovery is needed, use a supported local backup/snapshot procedure for that host. Protect backups as private state. Do not downgrade a client against newer memory state without documented compatibility. Never delete/reset the memory store as a fallback. Config rollback changes future behavior and cannot undo already generated or consolidated memories.

## Update Verification and Acceptance

1. Freeze baseline/candidate pack commits, installed host versions, effective settings, provider/authentication, and benign trial inputs. Separate the conversation-model change from extraction/consolidation changes; vary one role at a time. Revalidate support rather than editing an embedded model list.
2. Run the repository checks in the README. The unit test parses the TOML example and prevents model pins in the default; the required [Golden Test 038](../tests/GoldenTest-038.md) defines behavior cases. These static checks do not execute live models or certify runtime fallback.
3. In authorized isolated host trials, test default selection, each supported override independently, and the failure cases below. Include an unrelated task with memory absent/disabled to confirm the pack's mandatory rules still hold. Do not deliberately exhaust quota or provoke production failures; simulate errors in a controlled trial where possible.

| Case | Acceptance evidence |
|---|---|
| Defaults before/after host upgrade | Config loads; no model pin introduced; extraction/consolidation and later recall observed under documented eligibility gates |
| Supported override for either role | Exact role's operation succeeds; unrelated role/settings preserved |
| Unsupported/retired override | Candidate rejected or affected pin removed with authorization; default independently verified; no retry loop or memory reset |
| Unknown version, missing model-access evidence, or unsupported feature/key | Candidate deferred with `[unverified]`; previous working behavior retained |
| Authentication, quota, transient, or ambiguous error | Cause reported; no automatic model substitution or concealed PASS |
| Quality regression and rollback | Same task/output contract checked; prior settings restored; state changes and recovery limits disclosed |

4. Compare sanitized responses/action evidence using [the Scorecard](../tests/Scorecard.md). For any claimed improvement, use its paired-trial protocol and record measured latency, actual usage/cost when available, recall correctness, and hard failures. Report unmeasured dimensions explicitly.
5. Promote only after required compatibility/trial evidence passes, with no secret exposure or critical regression. Otherwise keep the previous working choice and record the Validation Gap. Refresh source dates and support evidence when behavior changes; do not periodically rewrite model names just because a new release exists.
