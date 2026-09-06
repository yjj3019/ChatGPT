# ChatGPT / Codex Model Routing

Authoritative roster and defaults (user-provided 2026-09-06). Load this file only when choosing or switching models, or when the user asks for model advice — never every turn.

**Headline:** routing + Context Budget = a stable quality floor across all six models. Do not treat model choice as “pick the strongest”; deliver consistent performance and efficiency on every pick.

## Model Roster

| Model ID | Role |
|---|---|
| `gpt-6-astra` | Most capable — complex, demanding work (current flagship) |
| `gpt-5.6-sol` | Reliable agentic workhorse for everyday tasks |
| `gpt-5.6-terra` | Balanced agentic coding for everyday work |
| `gpt-5.6-luna` | Fast, affordable agentic coding |
| `gpt-5.5` | Proven previous-gen coding / general |
| `gpt-5.4-mini` | Small, fast, cost-efficient simpler coding |

## Model-Invariant Floor

Regardless of which model is selected (`gpt-6-astra` … `gpt-5.4-mini`):

1. **Same Core Runtime + Operational Integrity** — never skip evidence / completion / files / tools / freshness gates on mini or luna (or any model).
2. **Same Context Budget** — Core + ≤1–2 mapped files (or 1 task file + one domain section). Do not dump more docs onto weaker models to “compensate,” and do not dump more onto astra either.
3. **Same Task Loading Map / Intent Classifier** — model choice does not change which files load.
4. **Same output contract** — facts vs assumptions, `[unverified]`, smallest useful change, no fake completion claims.
5. **Weaker models:** stay inside budget harder; escalate model (`mini` → `luna` → `terra` → `sol` → `astra`) when blocked twice or risk rises — do **not** expand context as a substitute.
6. **Stronger models:** still obey budget; extra capacity goes to deeper reasoning within the same loaded set, not extra file loads.

Core Runtime remains model-independent. Model choice does not relax Operational Integrity or Autoload Protocol.

## Default Picks

| Use case | Model |
|---|---|
| ChatGPT Project default for complex work | `gpt-6-astra` |
| Everyday agentic (non-coding multi-step) | `gpt-5.6-sol` |
| Everyday coding / debug / PR | `gpt-5.6-terra` |
| Cheap / fast coding | `gpt-5.6-luna` |
| Fallback legacy | `gpt-5.5` |
| Tiny / trivial tasks | `gpt-5.4-mini` |

## Task → Model Map

Aligned with Task Loading Map intents in `CHATGPT.md` / `AGENTS.md`:

| Task intent | Prefer |
|---|---|
| Complex architecture / security / multi-file RCA / hard research / high-stakes proposal | `gpt-6-astra` |
| Everyday agentic ops, multi-step non-coding, meetings / exec summaries | `gpt-5.6-sol` |
| Everyday coding / debug / PR | `gpt-5.6-terra` |
| Small coding, boilerplate, simple refactors | `gpt-5.6-luna` (or `gpt-5.4-mini` if trivial) |
| Blog / knowledge work | `gpt-5.6-sol` (or `gpt-5.6-terra` if heavily code-sample) |
| Domain packs + engineering | `gpt-6-astra` if high risk; else `gpt-5.6-sol` (analysis) / `gpt-5.6-terra` (coding) |

## Escalation Ladder

When blocked twice on the same obstacle, or when task risk / ambiguity rises:

`gpt-5.4-mini` → `gpt-5.6-luna` → `gpt-5.6-terra` → `gpt-5.6-sol` → `gpt-6-astra`

Escalate one step at a time; do not jump to astra for a trivial miss. De-escalate when remaining work is clearly in a lower band. Escalation replaces context expansion — never both.

## Budget Pairing

- Stronger model + **stricter** Context Budget (still Core + ≤2 mapped files / one domain section).
- Never compensate for wrong model routing by loading all docs, transfer, all-in-one, or every `codex-*.md`.
- Wrong model ≠ license to blow the Context Budget.

## Codex Usage

1. Pick the model in the Codex UI / settings to match this map.
2. `AGENTS.md` still governs which files load for the task.
3. This routing doc is advisory for model choice only — not a substitute for task-type rule files.
