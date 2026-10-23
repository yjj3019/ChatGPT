---
name: "taskforge-for-chatgpt"
description: "Apply TaskForge for ChatGPT guidance when the user requests this pack for a task or a setup review. Not for unrelated coding or writing."
---
# TaskForge for ChatGPT

Use when this pack is requested, including explicit skill invocation. Preserve
the user's task, permissions, and existing workspace instructions.

## Session model policy

For a new conversation applying TaskForge for ChatGPT, preserve the current main model and
effort. DEFAULT uses registered model-inheriting roles; fixed Sol/Luna/Astra IDs
are an explicit opt-in PRESET, not distribution defaults. Before choosing or
running delegation, read only these operational sections:

- [Session policy](../../docs/codex-three-model-setup.md#session-policy)
- [Model priority](../../docs/codex-three-model-setup.md#model-id-inheritance-priority)
- [Small-task exclusions](../../docs/codex-three-model-setup.md#when-not-to-delegate)
- [Review triggers](../../docs/codex-three-model-setup.md#astra-review-triggers)
- [Context packet](../../docs/codex-three-model-setup.md#context-packet-standard)
- [Role failure](../../docs/codex-three-model-setup.md#role-discovery-failure-wording)
- [Retry policy](../../docs/codex-three-model-setup.md#retry-policy)
- [Cost/latency notice](../../docs/codex-three-model-setup.md#cost-and-latency-notice)

Do not preload the whole guide. Load configuration details only for setup work;
the operational sections above apply to ordinary delegation too.

An explicit user model choice or request to disable the preset suspends all
automatic delegation for the rest of this conversation, even if the user selects
Sol again. Keep the selected model and effort; do not invoke pinned Luna/Astra
roles while suspended. Use inherited subagents only if separately requested.
An explicit re-enable request restores the requested routing: DEFAULT for
inherited delegation, PRESET only for an explicit fixed-model request. A new
conversation applying TaskForge for ChatGPT starts in DEFAULT
unless a separately approved host-wide PRESET policy applies. A resumed
conversation or compaction is not a new conversation. This host-wide exception
is a separate opt-in; installation alone is not. Never persist this suspension
to global configuration.

Observe UI model choices only when the host exposes authoritative evidence;
otherwise ask the user to say "use this model only" to make the override explicit.
Do not infer manual selection from the active model alone or quoted text.
Never claim to detect a UI selection, switch the main model, or create roles
without supported controls and evidence. If selected roles or models are
unavailable, report the gap and continue authorized work on the current model.

## Guide loading

Resolve the plugin root as two directories above this SKILL.md directory. Read
[AGENTS.md](../../AGENTS.md) as the minimal entry, then read only the task-relevant
guides it selects. Resolve its `docs/` paths relative to that plugin root, even
when the user's current workspace is elsewhere. Do not preload CHATGPT.md as a
second entry or load every guide. Installing this plugin does not make its root
the user's workspace or automatically apply its AGENTS.md.

For a requested ChatGPT Project setup, read [README.md](../../README.md) or
[README.en.md](../../README.en.md). File installation does not prove live skill
selection or behavior. Keep verification limits visible.
