---
name: "taskforge"
description: "Apply TaskForge guidance when the user requests this pack for a task or a setup review. Not for unrelated coding or writing."
---
# TaskForge

Use when this pack is requested, including explicit skill invocation. Preserve
the user's task, model, effort, permissions, and existing workspace instructions.

Resolve the plugin root as two directories above this SKILL.md directory. Read
[AGENTS.md](../../AGENTS.md) as the minimal entry, then read only the task-relevant
guides it selects. Resolve its `docs/` paths relative to that plugin root, even
when the user's current workspace is elsewhere. Do not preload CHATGPT.md as a
second entry or load every guide. Installing this plugin does not make its root
the user's workspace or automatically apply its AGENTS.md.

For a requested ChatGPT Project setup, read [README.md](../../README.md) or
[README.en.md](../../README.en.md). File installation does not prove live skill
selection or behavior. Keep verification limits visible.
