# Codex Operations Rules

Public-safe Codex operations guidance. Private source links, model-specific settings, statusline scripts, local tool paths, hostnames, and project-specific environment values are intentionally omitted.

## Source Scope

This file consolidates generally useful operational patterns:

- persistent guidance hygiene
- skill use
- remote operation safety
- audit logging
- design/review/execute pipeline gates
- security and improvement review gates
- Windows and PowerShell notes
- MCP and tool budget management

## Persistent Guidance Hygiene

- Keep `AGENTS.md` short and durable.
- Put reusable workflows in focused files under `docs/`.
- Do not store secrets, raw logs, API keys, `.env` values, SSH private-key material, or raw MCP responses in persistent guidance.
- Prefer markdown/plain text summaries over dumping binary Office/PDF/HTML source into context.
- If source material is noisy, flatten it to concise markdown before using it as long-lived context.

## Skill Use

- Use an existing Codex skill when the task matches it.
- Read the selected `SKILL.md` before acting.
- Treat skills as workflow routers: load only the relevant references, scripts, and templates.
- For custom/reusable workflows, document trigger, inputs, dependencies, output path, and verification.
- Do not install or create a new skill for a one-off task.

## Remote Operations

- Use the configured connector/tool for remote work when the user or project requires it.
- Verify the actual tool path used; do not accept a direct local shell fallback as success when remote connector use was required.
- Keep remote host exposure minimal: only approved hosts, least-privilege users, and task-specific keys.
- Do not mix untrusted external content review with privileged remote execution in the same workflow unless necessary.
- For remote changes, report target host/alias, command class, changed files, and validation result. Do not echo secrets.

## Audit Logging

Log only when the user asks, when the work needs an audit trail, or when a project rule requires it.

Use a compact record:

```json
{
  "title": "short title",
  "type": "design | implementation | debugging | review | office | ops",
  "summary": "what changed",
  "files": ["paths or source pages"],
  "result": "GO | CONDITIONAL_GO | NO_GO | completed",
  "next": "next action or none"
}
```

Do not log raw conversation, raw MCP payloads, long diffs, secrets, or full generated artifacts.

## Pipeline Patterns

- Separate design/review from execution for large or high-risk work.
- Use adversarial review before accepting architecture, security, or deployment decisions.
- Use structured artifacts for handoff: `gate_result`, `aggregated_report`, and `supervisor_verdict` style names are acceptable when a file-based workflow helps.
- Do not write pipeline artifacts for tiny tasks.

## Security Review Gate

- `P0`: secret exposure, auth bypass, command injection, SQL injection, destructive remote execution, or critical data loss risk.
- `P1`: missing rate limits, weak validation, unsafe CORS/security headers, weak integrity checks, or high-impact reliability risk.
- `GO`: P0 is 0 and verification passed.
- `CONDITIONAL_GO`: P0 is 0, P1 remains with a clear mitigation plan.
- `NO_GO`: any P0 or failed required verification.

## Improvement Review Gate

- Apply YAGNI first: reject improvements that add abstraction, dependencies, or migration risk without a clear current benefit.
- Classify useful improvements by priority:
  - `P0`: immediate correctness/security fix
  - `P1`: short-term maintainability or reliability improvement
  - `P2`: medium-term cleanup
- For high-impact improvements, list affected files and test scope before implementation.

## Windows and PowerShell Notes

- Save generated PowerShell scripts as UTF-8.
- Validate JSON after editing config-like files.
- When parsing CLI JSON from PowerShell, join multiline output before `ConvertFrom-Json`.
- Prefer non-blocking/cache-based status or telemetry helpers; do not let cosmetic telemetry slow task execution.

## MCP and Tool Budget

- Enable or use only connectors needed for the current task.
- Prefer local files/project context before broad external connector searches.
- Treat tool schemas and connector payloads as context cost; avoid loading unrelated connectors or pages.
