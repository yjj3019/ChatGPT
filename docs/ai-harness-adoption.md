# AI-Harness Pattern Adoption

Reviewed reference: [AI-Harness at ac4c59a](https://github.com/yjj3019/AI-Harness/tree/ac4c59adcced5484c9e9c7952b5794c880838a97). Target: TaskForge for ChatGPT 3.0.2, based on 3.0.1 (`3935e40`). The reference repository remains unchanged.

## Scope and existing coverage

Read the reference README pair, CLAUDE.md, six docs, five agent prompts, and JavaScript workflow skeleton. Compare instructions and actual control flow with TaskForge rather than treating a claimed workflow as an implemented runtime. TaskForge already has minimal entry points, scoped loading, acceptance criteria, proportional delegation, evidence rules, bounded retry guidance, and project lessons with evidence/removal conditions. These remain the baseline.

## Adopted changes

| Reference idea | TaskForge adaptation | Existing home |
|---|---|---|
| [Per-stage checklists](https://github.com/yjj3019/AI-Harness/blob/ac4c59adcced5484c9e9c7952b5794c880838a97/docs/PHASES.md) and [evidence-based verification](https://github.com/yjj3019/AI-Harness/blob/ac4c59adcced5484c9e9c7952b5794c880838a97/.claude/agents/verify.md) | Map required criteria to evidence, checked scope, verdict, and next action; distinguish observed failure from missing validation | [Execution Shape](chatgpt-engineering-task-rules.md#execution-shape) |
| [Handoff state](https://github.com/yjj3019/AI-Harness/blob/ac4c59adcced5484c9e9c7952b5794c880838a97/docs/HANDOFF.md) | Read saved state, verify current target/worktree/artifacts/pending operations, then reconcile the existing checkpoint | [Resume checks](chatgpt-engineering-task-rules.md#resume-checks) |
| [Blocking vs optional review](https://github.com/yjj3019/AI-Harness/blob/ac4c59adcced5484c9e9c7952b5794c880838a97/.claude/agents/review.md) | Acceptance/correctness/security/accessibility/regression failures block; optional NITs do not restart work | [Milestone evidence](chatgpt-engineering-task-rules.md#milestone-evidence) |
| [Sample-first document work](https://github.com/yjj3019/AI-Harness/blob/ac4c59adcced5484c9e9c7952b5794c880838a97/docs/ppt-harness-workflow.md) | Validate a representative risky layout and required editable objects before repetition; verify the final artifact separately | [Office workflow](codex-office-agent-rules.md#workflow) |

Detailed rules stay in the existing engineering section and Office guide. ChatGPT intent routing and the Codex task map add only the long-task trigger. Inlined Core and the standalone fallback remain unchanged. No extra mandatory state file, fixed sample count, execution engine, or host setup is introduced.

## Deliberately excluded

- The [JavaScript workflow](https://github.com/yjj3019/AI-Harness/blob/ac4c59adcced5484c9e9c7952b5794c880838a97/.claude/workflows/phase-harness.js) is documented as a skeleton. Its runPhase body only logs the argument; retry counters, step execution, and evidence gates are not implemented. Exit 0 from this scaffold cannot prove a completed phase. Do not ship it as a working TaskForge executor.
- Forced five-agent routing, a verifier for every task, or an automatic three-retry cycle would conflict with existing proportional delegation and retry limits. Keep main-agent verification and supported inherited roles.
- Mandatory new sessions/commits at each phase and a fixed 70% context reset threshold are not needed for evidence handoff. No behavior or product claim about that threshold is adopted.
- Reading or writing a compound log for every task is unnecessary overhead. Retain scoped, evidence-backed project lessons; no automatic cross-session memory or global-policy promotion.
- No vendor-specific Office installation commands, role files, credentials, recipient configuration, or named model defaults are copied.

## Validation and limits

[Golden Test 041](../tests/GoldenTest-041.md) covers false stage completion and scope; [042](../tests/GoldenTest-042.md) covers stale resumes and ambiguous operations; [043](../tests/GoldenTest-043.md) covers sample/final coverage and editability. They are behavioral scenarios and rubrics. Repository validation checks their structure and distribution, not LLM behavior.

Run synchronization, framework validation, relevant unit tests, load measurement, and the release-version check against the real 3.0.1 base. These checks establish packaging, links, budgets, and maintenance behavior. They do not establish runtime policy compliance, better model quality, faster execution, or a successful live Office rendering trial. Follow the [Scorecard](../tests/Scorecard.md) before making such claims.

The installed 3.0.1 host is outside this source change. No global settings, active roles, model/effort, permissions, hooks, memories, or live services are changed.
