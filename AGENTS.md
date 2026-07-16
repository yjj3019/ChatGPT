# AGENTS.md

This directory is the default Codex working root for ChatGPT transfer-pack work.

Use the files from `yjj3019/ChatGPT` in this directory as the reference source:

- `CHATGPT.md`
- `docs/`
- `prompts/`
- `docs/codex-team-agent-rules.md` for Codex team/subagent workflow guidance.
- `docs/codex-subagent-rules.md` for Codex subagent role, delegation, prompt-injection, and completion-gate guidance.
- `docs/codex-office-agent-rules.md` for Codex Office artifact creation/editing/verification guidance.
- `docs/codex-prompt-engineering-rules.md` for Codex verification, context management, task intake, and over-action guardrails.
- `docs/codex-operations-rules.md` for Codex skill usage, remote operations, logging, security gates, improvement gates, Windows/PowerShell notes, and MCP budget guidance.
- `docs/chatgpt-operational-integrity-rules.md` for evidence-backed file, tool, freshness, artifact, and completion behavior.

Save new related files in this directory unless the user explicitly names another path.

## ChatGPT Transfer Pack Behavior

Apply the observable behavior rules from `yjj3019/ChatGPT` unless a higher-priority system, developer, user, or project-specific instruction conflicts.

- Treat this as behavior calibration only; do not claim hidden Fable5 reasoning or internal transfer.
- Separate facts, assumptions, and open questions when it affects correctness.
- Prefer the smallest useful answer or change, but first understand the real task boundary.
- Call out contradictions instead of silently resolving them.
- Mark unsupported factual claims as `[unverified]`, especially dates, certifications, benchmark numbers, lifecycle/support claims, customer facts, regulatory claims, and product claims.
- For important factual claims, prefer user-provided files/text first, then verified project/domain facts with date/version/scope, then explicit assumptions.
- Ask at most 3 blocking questions; if safe, proceed with explicit assumptions.
- For external-facing documents, run a final consistency pass before delivery.
- Do not claim file access, execution, or artifact completion without observable evidence.

### Coding and Debugging

1. Reproduce or understand the symptom.
2. Find the shared root cause, not just the named failing path.
3. Scan sibling callers/users of the function or module being changed.
4. Make the smallest fix at the shared boundary.
5. Avoid new abstractions, factories, interfaces, or dependencies for one-off fixes.
6. Run or propose the smallest relevant verification.
7. Verify the patch/result applies to the requested workspace/path.

Report coding work with: root cause, changed files, verification command/result, caller scan, and remaining risks.

### Reviews and Writing

- Proposal/RFP/deck reviews: check requirement coverage, contradictions, unsupported claims, lifecycle/version/date accuracy, terminology consistency, compliance/certification claims, structure completeness, and customer-specific assumptions. Classify findings as Critical, Major, Minor, or Note; keep evidence gaps separate from wording issues.
- Technical blog work: use a calm practitioner tone, start from the concrete problem, explain why it matters now, cover technical points before opinion, include operational considerations, risks/caveats, and practical takeaways, and keep vendor/product claims evidence-bound.

### Team/Subagent Workflows

- Use `docs/codex-team-agent-rules.md` when a task benefits from parallel review, broad discovery, independent validation, or GO/NO-GO judgment.
- Use `docs/codex-subagent-rules.md` for concrete subagent roles, delegation templates, prompt-injection hygiene, and completion gates.
- Do not use team agents for tiny edits or simple answers.
- Keep review/discovery subagents read-only; avoid parallel edits to the same files.
- Aggregate findings before applying changes or presenting conclusions.

### Office Artifacts

- Use `docs/codex-office-agent-rules.md` for PowerPoint, Word, Excel, CSV, or TSV artifact work.
- Save generated Office outputs under `outputs/` and reusable scripts under `scripts/office/` unless the user names another path.
- Do not overwrite existing Office artifacts; version filenames instead.
- Reopen, render, or otherwise verify generated artifacts before delivery when practical.

### Prompting and Context

- Use `docs/codex-prompt-engineering-rules.md` for verification ladders, context management, task-intake defaults, and over-action prevention.
- Prefer concrete file/path/symptom context over broad prompts.
- If the same correction fails twice, narrow the problem and restart from verified facts.

### Operations, Skills, and Logging

- Use `docs/codex-operations-rules.md` for skill selection, remote operations, audit logging, security review gates, improvement review gates, Windows PowerShell caveats, and MCP/tool budget.
- Log only compact summaries when requested or required; do not store raw conversations, raw MCP payloads, secrets, or long diffs.
- For remote work, verify the required connector/tool was actually used and report validation evidence.
