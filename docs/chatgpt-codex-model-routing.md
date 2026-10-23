# ChatGPT / Codex Model Routing

Load only when choosing or switching models, or when the user asks for model advice. This guide does not establish model availability, relative performance, or permission to switch.

## Default

Use the current session model and effort by default. Respect explicit user choices and host requirements. Do not maintain a fixed preferred roster or switch automatically because a task is complex, risky, or has failed a set number of times.

Exception: the native TaskForge for ChatGPT skill uses its [session policy](codex-three-model-setup.md#session-policy) as the Codex default. Explicit model choices suspend that preset for the conversation. This exception does not change ChatGPT or legacy entry defaults, grant settings permissions, or prove an actual main-model switch.

## Verify the Product Surface

Before advising a change, record the actual surface (Chat, ChatGPT Work, Codex, or API), client/version, and authentication method (for example, ChatGPT sign-in versus API/provider credentials). Verify the models and effort levels actually exposed to that session, plus available tools and permissions. Product documentation and API catalogs are not a fixed host roster.

Do not transplant API parameters or an API context-window figure such as 1.05M into an app's capabilities. The `model_context_window` configuration describes available context; setting it is not a capacity upgrade. Check the active product/model's documented limits and observed configuration. This guide does not authorize settings changes, new model calls, or global installation.

Official references (checked 2026-10-10): [product model availability](https://learn.chatgpt.com/docs/models), [model selection and product differences](https://learn.chatgpt.com/docs/model-selection), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference). These references inform compatibility checks; they do not establish performance gains in this repository. Static checks cannot replace an authorized trial against the same acceptance criteria in the actual host/model.

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

Conversation-model selection is separate from local memory extraction/consolidation. For Memories defaults, optional overrides, version/support gates, and safe update recovery, load `docs/codex-memories-maintenance.md` only when relevant. Host-managed defaults do not promise an unchanged model or automatic recovery from a retired override; validate the same acceptance criteria after updates.
