# Luna/low Notion recording role

The dedicated Notion recording role uses `gpt-6-luna` / `low`. The main agent confirms the facts and conclusions; the recording role saves the supplied content and reads it back. This is the pack's role selection, not a performance guarantee for every Notion task. The official model guide describes Luna as suitable for repetitive tasks with a clear scope. [OpenAI Docs](https://developers.openai.com/api/docs/models/gpt-6-luna) (checked on 2026-10-16).

## One-time setup

1. Follow the [host setup procedure](codex-three-model-setup.md#configure-host-roles-safely) to verify the actual Codex home and each account's model and tool access.
2. Check for conflicts with existing roles, review [notion-recorder.toml](examples/codex-three-models/notion-recorder.toml), and copy it into that home's `agents/` directory. Before replacing an existing file, review the differences, obtain approval, and make a private backup.
3. Preserve any project-specific page already fixed in an existing role. This distribution example is generic: it receives the destination `page_url` with each request, so its input contract differs from an existing role with a fixed destination. Do not automatically replace personal settings with this example.
4. Verify the connected Notion tools' access scope and start a new session. Installing the pack or registering a role does not grant write access or approval to save content.

If standard Codex and Orca use different Codex homes, check each separately. If they share global instructions through a symbolic link, edit the target only once and preserve the link. Installing or updating the pack does not run this procedure automatically.

## Delegate recording

The main agent confirms **one destination and six record fields**.

| Input | Meaning |
|---|---|
| `page_url` | An existing Notion page approved by the user |
| `title` | Task title |
| `type` | One of the Korean input-contract values: `기능구현` (feature implementation), `디버깅` (debugging), `리팩토링` (refactoring), `설계` (design), or `이슈` (issue) |
| `summary` | Confirmed changes |
| `files` | Changed files and key points that may be disclosed |
| `result` | Completion, in-progress, or blocked status supported by verification evidence |
| `next` | Next task |

Invoke the role with `agent_type="notion-recorder"` and omit the model and reasoning_effort arguments. A URL alone does not establish approval to save content. The main agent must confirm approval to record that content on that page; do not pass the original conversation, the entire diff, or authentication files. The main agent checks the returned link and verification result. Do not expand `luna_runner` beyond its verification-only scope.

For automatic routing, review and add the following line to the existing global instructions. Do not add it twice, and retain the [manual per-session selection](codex-three-model-setup.md#session-policy) rule.

> For approved Notion recording, the main agent passes page_url and the six confirmed fields to notion-recorder. Do not override the role configuration with model arguments. Do not save without a destination; check the returned link and read-back result. If the user explicitly selects a single model for the conversation, also suspend delegation to the fixed Luna recording role.

## Verification and rollback

First run a dry run to check that all six fields are preserved, the actual Luna/low model is recorded, and no external tools or file writes are invoked. Then save one required history entry on a user-approved page and read it back. Distinguish duplicate titles and content, Notion display formatting versus actual values, and verification gaps such as truncated reads or unknown blocks. If a write response is ambiguous, do not save again without reading it back.

Duplicate checks are instruction-level checks and do not guarantee atomicity. Concurrent calls, read delays, or lost responses can leave the outcome unclear. Do not automatically delete or modify existing duplicates; report the confirmed state and limitations to the main agent.

To roll back, remove only the added routing line and role, or compare the backup with current changes before restoring. Do not overwrite later user changes. Deleting saved history or restoring an entire page requires separate approval.

The [2026-10-16 host verification record](host-verification-2026-10-16.md) confirmed one actual save through a personal role with a fixed OVE destination. Static checks of the generic page_url example above and live verification of the personal role provide different evidence. Other projects, Orca-specific Notion connections, cost, and speed require separate verification.
