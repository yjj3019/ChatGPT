# AI-Harness Pattern Adoption

Initial reviewed reference: [AI-Harness at ac4c59a](https://github.com/yjj3019/AI-Harness/tree/ac4c59adcced5484c9e9c7952b5794c880838a97). Initial target: TaskForge for ChatGPT 3.0.2, based on 3.0.1 (`3935e40`). The reference repository remains unchanged. See the later re-review below for the implemented runner.

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

## Deliberately excluded in the initial review

- The [JavaScript workflow](https://github.com/yjj3019/AI-Harness/blob/ac4c59adcced5484c9e9c7952b5794c880838a97/.claude/workflows/phase-harness.js) is documented as a skeleton. Its runPhase body only logs the argument; retry counters, step execution, and evidence gates are not implemented. Exit 0 from this scaffold cannot prove a completed phase. Do not ship it as a working TaskForge executor.
- Forced five-agent routing, a verifier for every task, or an automatic three-retry cycle would conflict with existing proportional delegation and retry limits. Keep main-agent verification and supported inherited roles.
- Mandatory new sessions/commits at each phase and a fixed 70% context reset threshold are not needed for evidence handoff. No behavior or product claim about that threshold is adopted.
- Reading or writing a compound log for every task is unnecessary overhead. Retain scoped, evidence-backed project lessons; no automatic cross-session memory or global-policy promotion.
- No vendor-specific Office installation commands, role files, credentials, recipient configuration, or named model defaults are copied.

## Initial validation and limits

[Golden Test 041](../tests/GoldenTest-041.md) covers false stage completion and scope; [042](../tests/GoldenTest-042.md) covers stale resumes and ambiguous operations; [043](../tests/GoldenTest-043.md) covers sample/final coverage and editability. They are behavioral scenarios and rubrics. Repository validation checks their structure and distribution, not LLM behavior.

Run synchronization, framework validation, relevant unit tests, load measurement, and the release-version check against the real 3.0.1 base. These checks establish packaging, links, budgets, and maintenance behavior. They do not establish runtime policy compliance, better model quality, faster execution, or a successful live Office rendering trial. Follow the [Scorecard](../tests/Scorecard.md) before making such claims.

The installed 3.0.1 host is outside this source change. No global settings, active roles, model/effort, permissions, hooks, memories, or live services are changed.

## Re-review of the evidence-gated runner

On 2026-10-24, reviewed [45664d3](https://github.com/yjj3019/AI-Harness/tree/45664d315faa13aab71f3b01bf270d50a42f4906) against the last analysis at `77b0dc8` and the original adoption above. Reviewed against TaskForge 3.0.4; these source improvements are released in 3.0.5. The new delta contains 13 commits and changes 31 files; the JavaScript skeleton has been replaced by an implemented evidence-gated runner. The initial skeleton assessment is historical and does not describe this revision.

Scope: current README pair, PHASES, new decisions/external-pattern/supplement/usage documents, gate implementation and Node tests, CI, settings, lifecycle command, test-agent protocol, evidence/read/destructive-command hooks and compound guidance. No upstream installation, live Claude phase run or recipient configuration change was performed. The upstream [CI run](https://github.com/yjj3019/AI-Harness/actions/runs/40081975809) passed for this exact commit; that is upstream Linux test evidence, not native Windows or live agent certification.

| Adopted principle | TaskForge home and evaluation |
|---|---|
| A person can reproduce a substantial stage's check from its prerequisites, inputs, steps and expected result | Existing engineering Execution Shape; no new mandatory file or manual rerun for every task |
| Bind evidence to actual commands, real exit/completion, selected test coverage and relevant content state; invalidate affected evidence after changes | Execution Shape and [Golden 047](../tests/GoldenTest-047.md), including an empty required set and changes during execution |
| Separate evidence consistency from independent provenance, read access, host capability and active enforcement | Execution Shape and [Golden 048](../tests/GoldenTest-048.md); preserve valid single-agent workflows |
| Evidence-backed conclusion titles for analytical slides, with user/template exceptions | Existing Office guide and [Golden 043](../tests/GoldenTest-043.md); this idea predates the latest delta |

Implementation caveats found in the reference:

- `cmdRun` computes its tree hash after command execution. A post-run hash alone cannot establish which content a test observed if relevant files changed during execution. Existing tests cover edits after a run, not this timing case. A controlled local CLI probe asserted the original fixture input, changed it during the command, and observed a recorded test PASS with a non-null tree fingerprint. This probe covers the run-command record only, not a complete phase, doctor, hooks or live Claude execution.
- `verify-attestation` skips its expected-command comparison when no command pin is available. The CI attestation loop also permits an empty set. These modes do not establish that a required command and required phase records were checked.
- The tree fingerprint omits Git-ignored inputs and follows its own handling of symlinks/read failures; its scope is not all external test dependencies. Read tracking checks path/hash records rather than proving correct interpretation or an independently trusted producer.
- The destructive/evidence hooks are documented as pattern-based guardrails and fail open without `jq`. The runner's doctor explicitly rejects native Windows; Git Bash with Windows Node does not change Node's platform. These are constraints of this upstream implementation, not TaskForge host requirements.

Sources: [gate](https://github.com/yjj3019/AI-Harness/blob/45664d315faa13aab71f3b01bf270d50a42f4906/.claude/workflows/phase-gate.js), [gate tests](https://github.com/yjj3019/AI-Harness/blob/45664d315faa13aab71f3b01bf270d50a42f4906/tests/phase-gate.test.js), [CI](https://github.com/yjj3019/AI-Harness/blob/45664d315faa13aab71f3b01bf270d50a42f4906/.github/workflows/ci.yml), [evidence hook](https://github.com/yjj3019/AI-Harness/blob/45664d315faa13aab71f3b01bf270d50a42f4906/.claude/hooks/evidence-guard.sh).

Do not copy the engine, hooks, fixed agent/retry/session counts, global compound-log reads, automatic rule promotion or model/permission settings. No runtime dependency is added. Canonical Core, Codex entry and standalone budget remain unchanged. Installed copies require a separate 3.0.5 update. Maintenance checks cover synchronization, required cases, links, budgets and packaging; the new Golden rubrics are not live model trials, and no performance or model-quality gain is claimed.

## Platform and test-hardening re-review

On 2026-10-25, reviewed [6bc8e25](https://github.com/yjj3019/AI-Harness/tree/6bc8e252d9295fcb2b7c3420706ff5e4349307f8) against `45664d315faa13aab71f3b01bf270d50a42f4906`: three commits, 18 changed files. Target: TaskForge 3.0.6 source release; installed-host validation is recorded separately. Inspected the complete delta, including the gate, three hooks, required-command pin, attributes, new branch/edge/E2E suites, updated hook tests and documentation. No upstream executable, installer or hook was run for this review.

Adopted into the existing engineering Execution Shape and Golden 047/048:

- Probe prerequisites in the actual execution shell; test relevant path dialects, canonical containment and the actual evidence operation. A launcher's PATH or OS label cannot establish hook capability.
- Pair bad-case rejection with legitimate-case acceptance, including relevant boundaries. Exercise affected component wiring when isolated units miss it. Coverage is not defect detection; a targeted disposable mutation can check a consequential regression assertion when warranted. Scripted E2E simulations establish the exercised contract, not live model execution. No mandatory mutation campaign or extra workflow is introduced.

The previous review's Windows and missing-pin findings are historical at this revision: `doctor` now probes a selected bash environment instead of rejecting Windows outright, read tracking converts Windows paths, the evidence guard accepts both separators, and `["bash", "tests/run-all.sh"]` is committed as the command pin. This is source evidence, not our certification of native Windows, macOS or live Claude behavior. Upstream reports Windows runs, high coverage and three killed mutations; the mutation driver is outside the repository, so those counts are reported claims rather than independently reproduced results.

Remaining caveats from direct code inspection:

- The test tree fingerprint is still computed after execution; the during-run input-drift caveat remains. Git-ignored/external inputs are still outside that fingerprint.
- The CI attestation loop can still accept no records; the committed pin constrains existing records, not their required presence. Removing the pin still leaves the verifier's optional-command mode.
- Pattern-based destructive checks remain bypassable and may overmatch components of compound commands; added long-option coverage does not create a security boundary. Missing hook prerequisites still weaken enforcement. Shell selection in doctor is a capability probe, not proof of the host's actual lifecycle invocation.
- Current CI is Linux-only. Added real-hook simulations improve wiring coverage but do not invoke live `claude` agents, certify all platform branches or prove interpretation/independent provenance.

Sources: [gate](https://github.com/yjj3019/AI-Harness/blob/6bc8e252d9295fcb2b7c3420706ff5e4349307f8/.claude/workflows/phase-gate.js), [read tracker](https://github.com/yjj3019/AI-Harness/blob/6bc8e252d9295fcb2b7c3420706ff5e4349307f8/.claude/hooks/read-tracker.sh), [E2E suite](https://github.com/yjj3019/AI-Harness/blob/6bc8e252d9295fcb2b7c3420706ff5e4349307f8/tests/e2e.test.js), [edge suite](https://github.com/yjj3019/AI-Harness/blob/6bc8e252d9295fcb2b7c3420706ff5e4349307f8/tests/gate-edge.test.js), [branch suite](https://github.com/yjj3019/AI-Harness/blob/6bc8e252d9295fcb2b7c3420706ff5e4349307f8/tests/gate-branches.test.js), [reported measurements](https://github.com/yjj3019/AI-Harness/blob/6bc8e252d9295fcb2b7c3420706ff5e4349307f8/docs/SUPPLEMENTS.md).

Ponytail `09c434ab73ca43761c5d8b0c5d341926c2fba710` and Karpathy `2c606141936f1eeef17fa3043a72095b4765b9c2` remote HEADs were checked on the same date and remain unchanged. No runtime engine, hook, dependency, global setting or model policy is adopted. Core, Codex entry and standalone remain unchanged; the full transfer document is regenerated.

Local validation: synchronization and structure passed (14 routes, 34 required scenarios, 14 invariants); plugin-distribution tests passed (3); the required-Golden-assets focused regression passed (1). Release checking against `a877eebb85e11b1427e4912ec9467707cdbc0b38` accepted version 3.0.6 and eight changed payload files; load measurement and whitespace checking passed. The broader framework unittest attempts returned partial output without a retained final result, so their outcome is a Validation Gap, not a pass. No full-suite, live model, native upstream-hook or installed-host acceptance is claimed. This paragraph records pre-release local checks. Publication, exact-commit CI and installed-host acceptance require their own observed results; none is established by these local checks.
