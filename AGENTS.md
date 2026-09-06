# AGENTS.md — Codex Runtime Entry

Codex working root for the ChatGPT transfer pack (`yjj3019/ChatGPT`). Save new related files here unless the user names another path.

## Purpose

Lean Codex entry: apply Core Runtime invariants, load the smallest mapped task files, keep unique Codex gates in `docs/codex-*.md`. Do not claim hidden Fable5 reasoning transfer.

## Context Budget

- **Simple Q&A:** Core Runtime / invariants only.
- **Substantial tasks:** Core + at most 1–2 mapped task files (or 1 task file + one domain section).
- **Never autoload** unless the Task Loading Map row for that exact task allows it:
  - `docs/chatgpt-transfer-instructions.md`
  - `docs/chatgpt-5.5-all-in-one-instructions.md`
  - `docs/fable5-pattern-bank-for-chatgpt.md`
- **Domain packs:** matching section of `docs/chatgpt-domain-packs.md` only — never all sections.
- **Anti-pattern:** do not load all `docs/codex-*.md` at once.

## Instruction Precedence

1. Platform / system instructions
2. Organization, workspace, and project instructions
3. Runtime invariants in `CHATGPT.md` / Operational Integrity Core
4. Explicit user task constraints and output contract
5. Task-specific defaults (`docs/chatgpt-*.md`, `docs/codex-*.md`)
6. Model general behavior

Report conflicts that affect the task.

## Short Invariants

- Separate facts, assumptions, and open questions when correctness depends on it.
- Mark unsupported factual claims `[unverified]` (dates, certifications, benchmarks, lifecycle/support, customer, regulatory, product).
- Prefer user-provided files/text → verified facts (date/version/scope) → explicit assumptions.
- Ask at most 3 blocking questions; if safe, proceed with explicit assumptions.
- Smallest useful change; call out contradictions; no unverified file/tool/artifact completion claims.
- External-facing docs: one final consistency pass.

## Codex Task Loading Map

| When | Read |
|---|---|
| Session bootstrap | `CHATGPT.md` Core (or `docs/chatgpt-5.5-project-instructions.md` + `docs/chatgpt-operational-integrity-rules.md`) |
| Coding / debugging | `docs/chatgpt-coding-rules.md` |
| Proposal / RFP / deck review | `docs/chatgpt-proposal-review-rules.md` |
| Technical blog | `docs/chatgpt-blog-rules.md` |
| Architecture, RCA, research, SOP, prompt/security review | `docs/chatgpt-engineering-task-rules.md` (matching section only) |
| Meeting notes, presentation, executive summary | `docs/chatgpt-knowledge-work-rules.md` |
| RHEL / OpenShift / K8s / Linux / Ansible / Satellite / EA / AI infra / EV | matching section only of `docs/chatgpt-domain-packs.md` (+ task-type file when both apply) |
| Team / parallel review / GO–NO-GO | `docs/codex-team-agent-rules.md` |
| Subagent roles, delegation, injection hygiene, completion gates | `docs/codex-subagent-rules.md` |
| PowerPoint / Word / Excel / CSV / TSV | `docs/codex-office-agent-rules.md` |
| Verification ladders, context, intake, over-action | `docs/codex-prompt-engineering-rules.md` |
| Skills, remote ops, logging, security/improvement gates, MCP budget | `docs/codex-operations-rules.md` |
| Full combined guide (user asks) | `docs/chatgpt-transfer-instructions.md` |
| One-shot paste setup only | `docs/chatgpt-5.5-all-in-one-instructions.md` |

Optional one-shot calibration only when the map row allows: `docs/fable5-pattern-bank-for-chatgpt.md`.

## Codex-only pointers

- **Team/subagents:** tiny edits stay solo; review/discovery subagents read-only; no parallel edits to the same files; aggregate before changing.
- **Office:** `outputs/` + `scripts/office/` unless named otherwise; version filenames; verify before delivery.
- **Ops:** compact logs when required; no secrets or raw MCP payloads; remote work needs connector evidence.
