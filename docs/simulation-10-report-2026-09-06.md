# Simulation-10 Report (2026-09-06)

Structural/routing/load simulations on commit baseline `0411e55` (main), then fixes on branch `fix/sim-10-findings`.

**Method:** mechanical checks only (`Task Loading Map`, `measure_load.py`, fence-aware section parse, `sync_runtime.py --check`, `validate_framework.py`). This is a **simulation rubric** for repository structure — not a host-model quality score. No invented /100 behavioral scores.

Timezone note: work recorded 2026-09-06 evening KST (UTC+9).

## Summary table

| ID | Scenario | Expected load / tier | Result | Issue IDs |
|---|---|---|---|---|
| SIM-01 | Simple factual Q&A | Core only; trivial/mini–sol | PASS | — |
| SIM-02 | Coding/debug | Core + coding-rules; prefer `gpt-5.6-terra` | PASS | — |
| SIM-03 | RCA | Eng **Root Cause Analysis** section (+ Execution Shape); not full-file preference | PASS | — |
| SIM-04 | RHEL RCA | Eng RCA section + domain **RHEL** only | PASS | — |
| SIM-05 | Proposal review | Core + proposal-review-rules | PASS | — |
| SIM-06 | Model selection | Core + model-routing; AGENTS floor pointer | PARTIAL→fixed | P1-AGENTS-MODEL-FLOOR |
| SIM-07 | Weak model + hard architecture | Escalate model; same Context Budget | PARTIAL→fixed | P1-AGENTS-ESCALATE-NOT-EXPAND |
| SIM-08 | Transfer/all-in-one temptation | Non-autoload; not Task Map required | PASS | — |
| SIM-09 | Sync drift (temp copy mutate generated) | `sync_runtime.py --check` fails | PASS | — |
| SIM-10 | `##` inside fences (blog-rules) | Only real H2 sections | FAIL→fixed | P0-FENCE-UNAWARE-SECTION-PARSE |

Pre-fix tally: 7 PASS, 2 PARTIAL, 1 FAIL. Additional gaps found during derivation (not separate sims): missing invariant CI matrix, missing Core rules-only meta guard, Scorecard lacked simulation protocol.

## Per-scenario notes

### SIM-01 Simple factual Q&A — PASS
- Route: `General answer calibration` → Core Runtime only.
- Autoload: simple low-risk needs no supporting file.
- `measure_load`: 4887 bytes Core canonical docs; no coding/domain autoload.

### SIM-02 Coding/debug — PASS
- Route: `docs/chatgpt-coding-rules.md`.
- Routing doc Default/Task map prefers `gpt-5.6-terra` for everyday coding.
- Load: Core + coding-rules (6015 bytes full-file estimate).

### SIM-03 RCA — PASS
- Route: engineering-task-rules; section-aware RCA estimate 6619 vs full-file upper 9143.
- Sections present: Execution Shape, Root Cause Analysis, …

### SIM-04 RHEL RCA — PASS
- Domain row requires matching section only; combined section estimate 9619 vs full-file upper 14315.

### SIM-05 Proposal review — PASS
- Route and measure_load row bind proposal-review-rules.

### SIM-06 Model selection — PARTIAL (pre-fix)
- Route and Model-Invariant Floor doc OK; AGENTS linked routing file but lacked an explicit floor / escalate-not-expand one-liner.

### SIM-07 Weak model hard architecture — PARTIAL (pre-fix)
- Routing doc correctly says escalate model, do not expand unrelated instructions.
- AGENTS Context Budget did not state escalate≠expand before the fix.

### SIM-08 Heavy guides — PASS
- Transfer not a required Task Map row; Autoload forbids full/fallback/pattern bank; validate rejects forced always-load; measure lists heavy optional.

### SIM-09 Sync drift — PASS
- Temp-copy mutation of all-in-one generated artifact → `--check` returns 1 / out of sync (unittest pattern).

### SIM-10 Fence/`##` parse — FAIL (pre-fix)
- Naive `^## ` split on `docs/chatgpt-blog-rules.md` invented fake sections from the Outline fence (`Why this matters now`, `Background`, …).
- Real sections must be Style, Outline, Review Checklist only.

## Phase 2 — Problems

| Priority | ID | Defect |
|---|---|---|
| P0 | P0-FENCE-UNAWARE-SECTION-PARSE | `measure_load.parse_sections` / validate `section()` naive split; shared fence-aware helper missing |
| P1 | P1-AGENTS-MODEL-FLOOR | AGENTS lacked Model-Invariant Floor one-liner |
| P1 | P1-AGENTS-ESCALATE-NOT-EXPAND | AGENTS did not say escalate model, not expand context |
| P1 | P1-NO-INVARIANT-MATRIX | No CI assertion for ~8–16 core invariants (folklore gap) |
| P1 | P1-NO-CORE-RULES-ONLY-GUARD | No fail if maintainer/meta phrases appear inside BEGIN/END Core |
| P1 | P1-SCORECARD-NO-SIM-PROTOCOL | Scorecard lacked simulation protocol referencing 10-sim reports |
| P2 | P2-GOLDEN-MAX-STALE | `EXPECTED_TEST_IDS` stopped at 035 before fence/invariant scenarios |

## Phase 3 — Fixes implemented

1. **`scripts/markdown_sections.py`** — fence-aware H2 helper; used by `measure_load.py` and `validate_framework.py`.
2. **Invariant coverage** — 14 invariants checked in validate; AGENTS may pointer-satisfy.
3. **Rules-only guard** — meta phrases inside BEGIN/END Core fail validate.
4. **AGENTS Context Budget** — escalate model / keep Context Budget / pointer to routing floor (budget ≤4000).
5. **GoldenTest-036** (fence sections) and **GoldenTest-037** (invariants + rules-only); `EXPECTED_GOLDEN_MAX=37`.
6. **Scorecard** — Simulation Protocol section → this report.
7. Context Budget & model-invariant floor preserved; sync still sole generator for Core/all-in-one/transfer.

## Phase 4 — Validation (post-fix)

Commands:

```text
python3 scripts/sync_runtime.py --check
python3 scripts/validate_framework.py
python3 -m unittest tests.test_framework -v
python3 scripts/measure_load.py
```

Post-fix blog section titles (fence-aware): `Outline`, `Review Checklist`, `Style` only.

## Simulation rubric (structural, not host quality)

| Dimension | Pre-fix | Post-fix |
|---|---|---|
| Routing map integrity (sims 1–5,8) | PASS | PASS |
| Model-floor entry coverage (6–7) | PARTIAL | PASS (docs+AGENTS) |
| Sync drift detection (9) | PASS | PASS |
| Fence-aware sections (10) | FAIL | PASS |
| Invariant CI signal | absent | present (14) |
| Rules-only Core guard | absent | present |

Do not read the table as model accuracy percentages.
