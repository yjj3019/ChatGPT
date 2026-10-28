# Repository Review — 2026-10-28

## Scope and Evidence

Reviewed `yjj3019/ChatGPT` main at `8bef29920a7ce5d2eaba2de2d9d30ae2ebd40358` (TaskForge for ChatGPT 3.0.10). Scope: entry instructions, model routing and role examples, canonical/generated document flow, installer, tests, CI and release gate. This is a source/document review, not a live host certification or a comprehensive security audit. The pre-existing parent workspace was not a checkout of this revision; a separate verified source checkout was used for this initial analysis.

## Structure

- `CHATGPT.md` and `AGENTS.md` are alternative runtime entries. Task routing loads only relevant guides; the pack changes observable guidance, not model weights.
- `scripts/sync_runtime.py` generates the entry's Core block, the standalone guide and full transfer reference from canonical documents. Unlike the older parent workspace, current source covers all three generated documents.
- `scripts/validate_framework.py` checks structure, routes, links, required scenarios, invariants and generated consistency. Python tests cover framework rejection cases, installer safety/integrity, distribution examples and release rules. Golden markdown scenarios are rubrics; they are not evidence of executed model trials.
- `scripts/install_pack.py` packages documentation with integrity manifests and conflict handling. New files under `docs/` use the existing packaging path; no new dependency or installer implementation is needed.
- `.github/workflows/validate-framework.yml` runs on push/PR with Windows/Linux and Python 3.11/3.12. It runs tests, generated checks, framework validation and the version gate. Workflow definitions alone do not prove a successful run.

## Findings and Decisions

| Severity | Finding and evidence | Decision |
|---|---|---|
| Major — requested capability gap | The push/PR workflow has no recurring model-document fetch; upstream review explicitly does not create a scheduler (`docs/upstream-review.md`, Trigger and scope). | Register a daily 09:00 Asia/Seoul Codex thread heartbeat. It uses the GitHub connector directly; no model-information file is retained on the PC after initial verification. It is not a repository-installed service. |
| Major — integration risk | `docs/chatgpt-codex-model-routing.md`, Verify the Product Surface, distinguishes API catalogs from host availability. `docs/codex-three-model-setup.md`, Model ID Inheritance Priority, requires host evidence for fixed IDs. | Store dated API facts separately. Do not replace recipient model/effort, model-inheriting defaults, optional role IDs or past host evidence from the API catalog. This is a risk prevented by the design, not a demonstrated runtime defect. |
| Note | Historical `5.5` filenames are explicitly retained for compatibility in current README and generated-document headers. | Keep names and callers intact. Their presence is not evidence of an obsolete required model. |
| Note | Optional preset IDs also appear in TOML examples and exact assertions in `tests/test_three_model_examples.py`. | Preserve them; adding Terra to the API reference does not require a fourth preset role. |
| Note | Catalog freshness is absent from static tests. | Actually open the official source each run; detect category membership changes as well as field changes. Fetch failures preserve existing data/date and produce a Validation Gap. |

## Update Candidate

Candidate version: 3.0.11. Add `docs/openai-api-models.md`, link it from the model routing guide and both language READMEs, and record this review. No runtime scripts, role files, user settings, permissions or generated Core sources change. Official model source: [API models](https://developers.openai.com/api/docs/models), opened 2026-10-28. The snapshot covers the current flagship category; specialized and legacy models remain task-scoped lookups.

Independent read-only exploration and direction review informed the scope. They identified no reason to rewrite host policy. Required upstream HEAD checks returned the existing reviewed commits: Ponytail `09c434ab73ca43761c5d8b0c5d341926c2fba710`; Karpathy-inspired skills `2c606141936f1eeef17fa3043a72095b4765b9c2`. No changed upstream delta required adoption.

## Publication and Recovery

The user explicitly requested direct GitHub storage. Publish one non-forced commit against the expected main head, preserving concurrent work. Subsequent checks read/write remote files rather than creating PC snapshots. Rollback is a new revert commit restoring only this update's files; never rewrite history or reset recipient settings. The scheduled heartbeat depends on the app/thread and connector access; registration does not prove future execution. Inspect CI for the published revision before claiming cross-platform validation.

## Verification Scope

Initial Windows source checks: `python -X utf8 scripts/sync_runtime.py --check` passed; `python -X utf8 scripts/validate_framework.py` passed with 14 routes, 38 required scenarios and 14 invariants. The model snapshot's IDs/version/readback assertion and `git diff --check` passed. Full unit tests and remaining maintenance checks were still running when preparing this review branch. Review the commit's actual CI checks for the final result; no live API calls, host model trials, or future heartbeat runs are certified here. The model detail pages were also opened to cross-check the table and long-context billing condition. Subsequent source-link/billing-note and review-record edits are documentation-only and need remote CI/readback; they do not change runtime behavior.
