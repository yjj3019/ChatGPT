# Codex Team Agent Rules

Public-safe Codex guidance for team/subagent workflows. Tool-specific settings, model names, local paths, and environment-specific mandates are intentionally omitted.

## Purpose

Use team/subagents only when they reduce real work: broad codebase scans, independent reviews, document comparison, risk checks, or parallel research. For small edits, do the work directly.

## Codex Roles

- `architect`: read-only design review for architecture, interfaces, tradeoffs, and contradictions.
- `executor`: implementation worker for scoped edits or command execution.
- `reviewer`: read-only code or document reviewer focused on bugs, security, missing evidence, and test gaps.
- `aggregator`: merges subagent findings into one concise report.
- `supervisor`: final GO / CONDITIONAL_GO / NO_GO judgment for high-risk changes.
- `logger`: records durable session notes only when the user asks or the work needs an audit trail.

## Delegation Rules

1. State the exact task, input paths, output shape, and acceptance criteria.
2. Keep each subagent scoped to one responsibility.
3. Prefer read-only agents for review and discovery.
4. Use structured outputs for handoff: `status`, `findings`, `evidence`, `risks`, `next_action`.
5. Do not let subagents edit the same files in parallel.
6. Aggregate results before acting on them.
7. Stop and ask the user after the same blocker repeats 3 times.

## Output Contract

When a subagent-style workflow is used, summarize:

```json
{
  "status": "SUCCESS | FAILED | CONDITIONAL",
  "agents_used": ["role-name"],
  "findings": [
    {
      "severity": "Critical | Major | Minor | Note",
      "evidence": "file, line, command, or source",
      "summary": "short finding",
      "next_action": "specific next step"
    }
  ],
  "verification": "command/result or reason not run",
  "remaining_risks": ["risk"]
}
```

## GO / NO-GO Gate

- `GO`: no critical issues, verification passed, remaining risks are acceptable.
- `CONDITIONAL_GO`: no critical issues, but warnings or follow-up tasks remain.
- `NO_GO`: critical issue, failed verification, missing required evidence, or conflicting agent findings.

## Local Storage

Save team-agent related notes, templates, or generated reports in this repository unless the user names another path.
