# ChatGPT Transfer Pack

ChatGPT-oriented instructions distilled from the FEF/Fable-style transfer work.

## Memory Bootstrap

Start every new ChatGPT project/session by reading `CHATGPT.md` first. Treat `CHATGPT.md` as the persistent working-memory bootstrap, then let it route the task to the smallest needed supporting files.

## Context Budget

Keep token load small and routing precise:

- **Simple Q&A:** Core Runtime / invariants only.
- **Substantial tasks:** Core + at most 1–2 mapped task files (or 1 task file + one domain section).
- **Never autoload** unless the Task Loading Map row for that exact task allows it:
  - `docs/chatgpt-transfer-instructions.md`
  - `docs/chatgpt-5.5-all-in-one-instructions.md`
  - `docs/fable5-pattern-bank-for-chatgpt.md`
- **Domain packs:** load the matching section only.
- **Anti-pattern:** do not load all `docs/codex-*.md` at once.

See `CHATGPT.md` (Context Budget, Task Loading Map, Intent Classifier) and the lean Codex entry `AGENTS.md`.

## Start Here

- `CHATGPT.md` — single runtime entry point. Use this as the main Project Instruction / Project Knowledge entry.
- `AGENTS.md` — Codex runtime entry point. Use this repository as the working root when you want Codex to apply the included guidance automatically.

## Recommended Project Setup

1. Add `CHATGPT.md` and the needed `docs/` / `prompts/` files to ChatGPT Project knowledge (prefer the mapped task files you actually use; you do not need the heavy transfer/all-in-one/fable5 files for normal multi-file use).
2. Paste `CHATGPT.md` into Project Instructions when only one instruction field is available.
3. Let Autoload Protocol + Task Loading Map + Intent Classifier select the smallest file set per task.
4. After editing canonical Core sources (`docs/chatgpt-5.5-project-instructions.md`, `docs/chatgpt-operational-integrity-rules.md`), run `python3 scripts/sync_runtime.py` — never hand-edit the generated Core block in `CHATGPT.md`.

## Files

- `docs/chatgpt-5.5-project-instructions.md` — core ChatGPT 5.5 project behavior (canonical).
- `docs/chatgpt-operational-integrity-rules.md` — file, tool, freshness, completion, and proportionality rules (canonical).
- `docs/fable5-pattern-bank-for-chatgpt.md` — optional historical calibration only (map-gated).
- `docs/chatgpt-coding-rules.md` — coding/debug behavior.
- `docs/chatgpt-proposal-review-rules.md` — proposal consistency review behavior.
- `docs/chatgpt-blog-rules.md` — technical blog behavior.
- `docs/chatgpt-engineering-task-rules.md` — architecture, RCA, research, operations manual, prompt review, and security review contracts.
- `docs/chatgpt-domain-packs.md` — RHEL, OpenShift, Kubernetes, Linux, Ansible, Satellite, Enterprise Architecture, AI infrastructure, and Tesla/EV domain rules; load only the matching section alongside a task-type file.
- `docs/chatgpt-knowledge-work-rules.md` — meeting notes, presentation, and executive summary structures.
- `docs/chatgpt-transfer-instructions.md` — full combined guide (user asks / map-gated).
- `docs/chatgpt-5.5-all-in-one-instructions.md` — single-paste fallback (one-shot only).
- `docs/codex-*.md` — Codex team, subagent, office, prompt-engineering, and operations gates (load by task, not all at once).
- `prompts/chatgpt-task-prompts.md` — task-specific copy/paste prompts.
- `tests/GoldenTest-015.md` through `tests/GoldenTest-030.md` — Operational Integrity, task-routing, proportional-governance, knowledge-governance, context-budget, and section-scope regression scenarios.

## Codex Use

```powershell
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
```

Start Codex from this directory, or set this directory as the workspace root. Codex will read `AGENTS.md`, which points to the supporting `docs/codex-*.md` guidance files under Context Budget.

## Boundary

This repository transfers observable working patterns. It does not claim to copy Fable5 internals or hidden reasoning.

## Validate and Measure

GitHub Actions runs the structure check on pushes and pull requests. Locally:

```bash
python3 scripts/sync_runtime.py
python3 scripts/validate_framework.py
python3 scripts/measure_load.py
```

- `sync_runtime.py` — regenerates the inlined Core Runtime in `CHATGPT.md` from the two canonical docs.
- `validate_framework.py` — structure, sync, Task Loading Map, path existence, Context Budget sections, entry size caps (`CHATGPT.md` ≤ 13800 bytes, `AGENTS.md` ≤ 4000 bytes), Autoload never-require heavy files, Golden Tests 015–030.
- `measure_load.py` — per task type, prints required file bytes and rough token estimate (bytes/4), plus section-aware estimates for engineering-task and domain-packs.

## Training Rounds (instruction-pack closed loop)

Five measure → change → validate rounds on branch `perf/context-budget-routing` (not ML training):

1. **Core token diet** — slim canonical Core sources; `sync_runtime.py` regenerates inlined Core.
2. **AGENTS lean** — cut duplicated pointers; keep Budget + map + hard gates.
3. **Routing precision** — clearer Intent Classifier / Selection Rules; Golden Test 030 (domain section-only).
4. **Load path efficiency** — section-scope banners on domain + engineering packs; section-aware `measure_load.py`.
5. **Final polish** — recalibrated entry size caps; Scorecard + README updated.

After edits to Core sources, always run `python3 scripts/sync_runtime.py` then validate + measure.
