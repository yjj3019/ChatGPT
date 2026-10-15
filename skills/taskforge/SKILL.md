---
name: "taskforge"
description: "Apply TaskForge guidance when the user requests this pack for a task or a setup review. Not for unrelated coding or writing."
---
# TaskForge

Use when this pack is requested, including explicit skill invocation. Preserve
the user's task, permissions, and existing workspace instructions.

## Session model policy

For a new conversation applying TaskForge, default to the Sol / Luna / Astra
policy in [Session policy](../../docs/codex-three-model-setup.md#session-policy).
Read that short section before choosing delegation; load setup details only
when setup is requested. This Codex-specific policy takes precedence over the
pack's general current-model default. It does not change ChatGPT defaults.

An explicit user model choice or request to disable the preset suspends all
three-model routing for the rest of this conversation, even if the user selects
Sol again. Keep the selected model and effort; do not invoke pinned Luna/Astra
roles while suspended. Resume only on an explicit re-enable request or in a
new conversation applying TaskForge. A resumed conversation or compaction is
not a new conversation. Never persist this suspension to global configuration.

Observe UI model choices only when the host exposes authoritative evidence;
otherwise ask the user to say "use this model only" to make the override explicit.
Do not infer manual selection from the active model alone or quoted text.
Never claim to detect a UI selection, switch the main model, or create roles
without supported controls and evidence. If the default main model or roles are
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
