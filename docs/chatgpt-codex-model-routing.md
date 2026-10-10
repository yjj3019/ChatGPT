# ChatGPT / Codex Model Routing

Load only when choosing or switching models, or when the user asks for model advice. This guide does not establish model availability, relative performance, or permission to switch.

## Default

Use the current session model and effort by default. Respect explicit user choices and host requirements. Do not maintain a fixed preferred roster or switch automatically because a task is complex, risky, or has failed a set number of times.

## Diagnose Before Switching

1. Identify the blocker from actual results. Missing source evidence, unavailable tools, permission boundaries, incorrect assumptions, and failing implementation are not proof of a model capability limit.
2. Gather necessary evidence, correct the approach, or request the missing authorization. Pause only dependent work. A model switch cannot grant access or bypass permission.
3. Consider a capability limit only when task-specific evidence remains after those causes are addressed. State the observed limitation and the expected benefit of a change; avoid unsupported rankings.
4. If a change is justified, inspect the host's currently supported effort settings and models. Use only supported settings within the user's authorization and host rules. Prefer the smallest justified change; ask when required authorization is missing. If switching is unavailable, state that limit and continue safe work on the current model.
5. Recheck the same acceptance criteria after any change. Report observed results, not presumed quality, speed, or cost gains.

## Model-Invariant Floor

- Same Core Runtime, Operational Integrity, and output contract on every model: evidence, authorization, truthful completion, and smallest useful changes.
- Same Context Budget: Core + 1–2 mapped guides or one task section + one domain section. Do not expand unrelated instructions to compensate for a blocker or model choice. Gather necessary source code, logs, and task evidence.
- Same Task Loading Map and Intent Classifier. Do not preload full, standalone, historical, or all Codex guides.
- Model or effort changes never substitute for missing evidence, permissions, or required verification.

## Codex Usage

Use only the model/effort controls actually supported by the host. `AGENTS.md` still governs task loading. This routing guide is advisory, not authorization to change settings or a substitute for task-specific guidance.
