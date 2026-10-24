# Ponytail comparison and adoption

## Scope and source

Reviewed on 2026-10-24: Ponytail 5.3.2 at commit
[`09c434ab73ca43761c5d8b0c5d341926c2fba710`](https://github.com/DietrichGebert/ponytail/tree/09c434ab73ca43761c5d8b0c5d341926c2fba710),
against TaskForge for ChatGPT 3.0.3 (`6c2e3a2`). This is a reference-adoption
review, not a full security certification of Ponytail or a live host trial.

The review covered the main instructions, review/audit/debt skills, Codex
manifest and lifecycle entry points, state handling, CI definition, benchmark
methodology/report/runner and related scoring tests. All host adapters and the
complete metrics UI were not audited. Upstream hooks and benchmarks were not
executed; no installation or trust settings were changed.

## Findings and decisions

| Priority | Gap or adoption risk | Decision |
|---|---|---|
| P2 | TaskForge said to reuse helpers and avoid dependencies, but did not establish whether existing project code should beat a new platform implementation | Prefer suitable project code, then standard library/platform features, then installed dependencies. Reuse does not justify keeping unsafe or incompatible code |
| P2 | Caller scanning was required, but a review could still report a generic scale concern without a reachable failure or inspect only changed lines | Require review of flows and expected load; each finding needs a reachable case, impact and minimal fix. Golden 046 includes an unchanged reservation helper and a concrete two-request race |
| P1 if copied without adaptation | Always-on activation, persistent mode state and host-specific hooks change execution scope and lifecycle behavior | Exclude these components. TaskForge remains task-scoped guidance; this change adds no runtime dependency, mode configuration or hook |
| Evidence limit | Efficiency and correctness figures use different task subsets and one host/model environment | Do not transfer upstream percentages to TaskForge or treat structural tests as behavioral measurements |

The core already covered minimal root-cause fixes, caller scans, cleanup
ownership, defect-sensitive tests, security checks and evidence gaps. Repeating
those principles or importing a persona/mode system adds little value.

Sources: [core instructions](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail/SKILL.md),
[review](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-review/SKILL.md),
[audit](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-audit/SKILL.md).

## Runtime components excluded

The Codex manifest declares lifecycle hooks. The activation hook writes mode
state, emits instructions and optionally starts a repository-map subprocess
with a three-second timeout. Runtime source explicitly documents shared mode
state for sessions in the same repository and a shared fallback flag. These
are operational tradeoffs, not equivalent to loading a task-specific guide.
Importing them would require separate host compatibility, concurrency,
timeout and permission validation.

The shortcut/debt convention is useful when a real limitation is accepted,
but this adoption does not mandate new markers or debt ledgers for small
tasks. Existing milestone evidence and workaround-removal guidance remain.

Sources: [manifest](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/.codex-plugin/plugin.json),
[activation](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-activate.js),
[mode state](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/hooks/ponytail-runtime.js),
[debt guide](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail-debt/SKILL.md).

## Benchmark assessment

The 2026-10-07 report compares three arms on 39 tasks, five repetitions per
arm/task, using headless Claude Code with Opus 5.5. Fresh workspaces, controlled
global configuration, plugin injection checks and separate source/test LOC
measurements are useful practices. TaskForge's existing
[Scorecard](../tests/Scorecard.md) already requires fixed conditions, isolated
sessions, paired trials, quality gates, raw counts and scoped efficiency claims.

Important limits:

- Hidden execution checks cover 18 surgical tasks, not all 39. The report's
  96.7% Ponytail 5 pass rate belongs to that subset; the baseline is 95.6%.
- The other 21 tasks measure code size, with feature completeness assessed
  separately by an LLM judge. Smaller code alone does not establish correctness.
- Fixed adversarial inputs are a security baseline, not proof of security.
- Bash is disabled, so this setup does not measure normal execute/debug loops.
- The reviewed checkout lacks raw `benchmarks/agentic/runs/` results. Reported
  aggregate percentages were not independently recomputed. The published
  reproduction/rescoring path does not substitute for those missing artifacts.
- One host/model and five repetitions per cell do not establish Codex gains.

Sources: [method and limits](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/agentic/README.md),
[runner](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/agentic/run.py),
[reported results](https://github.com/DietrichGebert/ponytail/blob/09c434ab73ca43761c5d8b0c5d341926c2fba710/benchmarks/results/2026-10-07-agentic.md).

## Acceptance and limits

The canonical coding guide retains its report fields and existing guards;
generated standalone/transfer guides must stay synchronized and within the
existing budgets. Golden 046 and its missing-asset regression check make the
new evaluation case required. The English/Korean README identifies release 3.0.4 and distinguishes source
changes from separately updated installed copies.

Maintenance tests validate distribution structure and regression checks, not
whether a live model follows the new rules. No speed, cost, quality, UI loading
or model-inheritance gain is claimed. Publication and installed-plugin update
are separate work; a payload release must pass the existing version gate.
