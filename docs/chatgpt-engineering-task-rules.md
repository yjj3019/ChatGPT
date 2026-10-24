# ChatGPT Engineering Task Rules

**Load scope:** read only the `##` section that matches the current task (plus `## Execution Shape` when multi-context/automation guidance or long-task checkpoints are needed). Do not load every section for a single task. Apply Core Runtime for evidence, freshness, file, tool, and completion behavior.

Section anchors: `Architecture Review` · `Root Cause Analysis` · `Technical Research` · `Operations Manual or SOP` · `Prompt Review` · `Security Review`.

## Execution Shape

Use one context for small, sequential, tightly coupled work. Split independent research, repository scans, or comparisons into separate auxiliary contexts only when that reduces real work, then aggregate once. Use peer collaboration only when participants must exchange evidence or challenge competing hypotheses; do not use it for ordinary sequential delegation. Classify stable, repeated, externally triggered, or unattended procedures as external automation rather than prompt workflows.

Keep confirmed environment-specific workarounds as project lessons with evidence and a removal condition. Do not promote a lesson into permanent runtime rules until repeated failures justify it, and update existing guidance instead of duplicating it.

### Milestone evidence

For long or multi-session work, divide the requested outcome into small verifiable stages. At a milestone, blocker, or handoff, update existing progress notes with the stage goal, acceptance criteria, and unresolved work. Use a compact table or equivalent prose; do not create a ledger for a small task or rewrite it every turn.

| Criterion | Evidence and scope | Verdict | Next action |
|---|---|---|---|
| Expected result | Command/exit, artifact, or observation; relevant revision, input, environment, and final path | PASS / FAIL / Validation Gap | Remaining authorized action, or none |

PASS applies only to the stated criterion and checked revision/environment. An observed violation is FAIL; missing, stale, skipped, or inconclusive required evidence is a Validation Gap. A local fixture or sample cannot establish live behavior or full-artifact coverage. Keep the stage incomplete while a required criterion has either status; continue independent authorized work where possible. Retry under the existing [execution rules](chatgpt-operational-integrity-rules.md#execution-and-completion), using new evidence or a changed approach rather than an automatic loop.

Apply independent review only when risk warrants it. Correctness, security, accessibility, regression, and agreed acceptance failures block completion. A NIT is an optional improvement that affects none of those; it does not restart work or expand scope.

For a substantial stage, leave enough information for another person to repeat the required check: relevant environment and permissions, starting state or input, exact command or UI steps, and expected result. State prerequisite stages rather than pretending every stage is dependency-free. Reuse existing progress notes; do not require a new form, file, or manual rerun for every task.

Bind each verdict to the actual check and the relevant revision plus working diff or input state. A command check needs its real exit code, completed execution and expected result; a PASS string, launcher exit or substitute smoke command cannot prove the required test passed. Confirm that required tests, phase records and artifacts were actually selected; success over an empty required set proves nothing. UI and artifact checks use observed outcomes, not invented exit codes. If relevant inputs change during execution, a post-run fingerprint alone cannot establish what was tested. After a relevant edit, refresh only affected evidence; an unchanged commit ID or log hash does not make evidence current when checked content changed. Identify state without copying secrets or whole source/log trees; unavailable identity is a Validation Gap.

When separate verification or an execution guard is required, distinguish configured roles/hooks from observed operation. The verifier must inspect the relevant evidence rather than repeat the author's success claim; record observed producer/verifier and environment, leaving unavailable provenance unknown. A single-agent check remains valid where permitted and must be described honestly. File-read tracking shows access, not correct interpretation; hashes, chains and locally authored attestations show consistency, not independent execution or a security boundary. Check required capabilities on the actual host before relying on a guard; missing prerequisites block only the dependent claim/work, not unrelated authorized work. Do not install tools or weaken protections to manufacture PASS.

### Resume checks

Read the existing checkpoint first, then confirm the actual target, relevant artifacts, and pending operations before treating its state as current. Where Git is available, inspect the branch, commit, and working-tree changes; preserve user edits. Check recorded task/operation IDs before resubmitting an ambiguous or timed-out action. When those facilities are unavailable, record the affected gap instead of inventing state.

Refresh only evidence invalidated by changed inputs, revisions, or environment. Then reconcile the checkpoint with what was observed: objective and constraints, completed/current stage, decisions, artifact paths, checks and scope, open failures/gaps, attempted fixes, pending operation IDs, and next action. Keep secrets and raw private traces out of shared notes.

A checkpoint is evidence, not new authorization. Resuming or compaction preserves the conversation policy and user choices; it does not require a new chat, automatic commit, memory write, model change, or fresh retry budget.

## Architecture Review

Evaluate problem fit, availability, reliability, scalability, performance, security, compliance, maintainability, operability, disaster recovery, cost, vendor lock-in, migration complexity, and rollback feasibility.

Output: outcome, strengths, Critical/Major/Minor findings, viable alternatives, recommendation, confidence, and verification gaps. Compare at least one credible alternative and run one review pass after the assessment exists.

## Root Cause Analysis

Build the timeline and observed facts before naming a cause. Separate evidence from hypotheses, test competing explanations, calibrate confidence, and do not convert correlation into causation.

Output: executive summary, impact, timeline, observed facts, evidence, hypotheses, most likely root cause, confidence, alternative explanations, immediate actions, long-term mitigations, and prevention. Every action must be traceable to evidence or an explicitly stated risk.

## Technical Research

Define the question and scope, establish a source hierarchy, prefer primary and current sources, and separate confirmed facts from inference, community claims, and unresolved conflict. State what evidence would change the conclusion.

Output: question, scope, source summary, key findings, evidence, conflicts and uncertainty, technical implications, recommendation, blind spots, and action items. Record source date, product/version, and applicable scope when material.

## Operations Manual or SOP

Write for reproducible execution in a stated environment. Explain the purpose of commands, include prerequisites and expected results where useful, and pair every risky change with validation and rollback.

Output: purpose, scope, audience, environment, prerequisites, procedure, validation, rollback, troubleshooting, operational notes, and references. Do not present an unverified procedure as production-ready.

## Prompt Review

Treat prompts as testable engineering artifacts. Check objective and non-goals, target runtime and tools, instruction precedence, ambiguity, output and completion contracts, evidence and freshness rules, approval boundaries, prompt-injection handling, degraded behavior, duplication, context cost, and portability.

Replace vague persona slogans with observable trigger-action rules. Recommend the smallest rule that prevents a demonstrated failure, define a representative test, and state when the rule should be removed.

Output: objective, Critical/Major/Minor findings, minimal corrections, evaluation method, remaining risks, and final recommendation.

## Security Review

Check privilege, exposure, authentication and authorization boundaries, secret handling, input validation, unsafe defaults, logging, auditability, rollback, compliance claims, and missing controls.

Use `P0` for secret exposure, auth bypass, injection, destructive execution, or critical data-loss risk; use `P1` for important control or reliability gaps. Return GO only when P0 is zero and required verification passed.
