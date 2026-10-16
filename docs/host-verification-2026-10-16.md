# Host Verification — 2026-10-16

Sanitized observations from one authorized Windows environment using Codex CLI 0.163.0. These are evidence for that environment, not a minimum supported version or a guarantee for other recipients. Private account paths, page IDs, authentication data, raw conversations and logs are deliberately omitted.

## Automatic delegation

The existing main-model and role settings were already correct. A reviewed global AGENTS block supplied the missing default routing without requiring a manual TaskForge skill call. The Orca account shared that file through an existing symbolic link, which was preserved.

| Trial | Observed outcome |
|---|---|
| Default Codex, fresh process | Sol/medium main, Luna Explorer/high, Luna Runner/low and Astra/low completed; harmless fixture output and Runner exit 0 verified |
| Orca account, fresh Codex process | First trial routed correctly but commands failed with Windows CreateProcessWithLogonW 1326; a fresh retry completed all roles and fixture checks |
| Installed Orca-managed terminal | New Codex process without a model override; automatic block observed, all roles completed, fixture output and Runner exit 0 verified |

Role invocations passed no explicit model/effort. Native runtime records, rather than model self-identification, established the model and reasoning values. CLI trials compared protected-file hashes before/after. The Orca terminal trial checked the post-setup guidance hash and configuration/role modification times; it did not have a separate pre-launch native hash snapshot. The terminal trial was not a structured-chat UI test.

The initial background Orca open request timed out waiting for a window; the runtime subsequently became ready. No unrelated process was stopped. Windows 1326's underlying cause was not repaired. UI model-picker detection, automatic switching of an already-running main model, behavior on every future task and cross-platform operation remain unproven. Astra remains conditional.

## Notion recorder

An existing project-specific recorder was pinned to Luna/low, and the role was registered in the Orca account. Both fresh-process dry-runs confirmed actual Luna/low, preservation of six fields, no child tool calls and unchanged protected-file hashes.

One meaningful configuration milestone was then recorded through that project-specific role on its existing authorized OVE page. The main independently fetched the page and found the title once and all six visible field values. Notion rendered a filename as a link; comparison used its visible text rather than claiming byte-identical Markdown. The fetch exposed no explicit unknown-block/completeness metadata, so an exhaustive page-wide duplicate guarantee is not claimed.

The distributable [recorder example](examples/codex-three-models/notion-recorder.toml) requires an explicit approved page_url instead of a private hardcoded destination. That portable input contract has static coverage, not a live write trial. No other project destination, Orca-owned Notion connector, broad reliability, cost or speed benchmark was tested.

## Hook investigation remains separate

Successful model delegation did not establish Hook health. Earlier actual Orca sessions still reported automatic 10-second Hook timeouts despite standalone command checks passing. A separate isolated diagnostic build observed 20/20 completions at a 30-second budget, no failures/timeouts, maximum 14.549 seconds. PermissionRequest and Interrupt execution were not exercised.

This was a mitigation experiment, not a repair of the underlying Windows process lifecycle delay. It did not replace the installed Orca app or change security products. The reusable source proposal belongs to [Orca PR #29523](https://github.com/stablyai/orca/pull/29523); consult that PR for its current status. It is not bundled into TaskForge and does not change third-party plugin Hook budgets.

## Recipient acceptance

Revalidate the actual host/account, supported keys, model access, role discovery, native model metadata, harmless command outcomes and settings preservation. A discovered role or completion message alone is insufficient. Run the pack's structural checks separately; those tests never call models, mutate a Codex home or write to Notion.
