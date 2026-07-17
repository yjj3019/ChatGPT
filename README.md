# ChatGPT Transfer Pack

ChatGPT-oriented instructions distilled from the FEF/Fable-style transfer work.

## Memory Bootstrap

Start every new ChatGPT project/session by reading `CHATGPT.md` first. Treat `CHATGPT.md` as the persistent working-memory bootstrap, then let it route the task to the smallest needed supporting files.

## Start Here

- `CHATGPT.md` — single runtime entry point. Use this as the main Project Instruction / Project Knowledge entry.
- `AGENTS.md` — Codex runtime entry point. Use this repository as the working root when you want Codex to apply the included guidance automatically.

## Files

- `docs/chatgpt-5.5-project-instructions.md` — core ChatGPT 5.5 project behavior.
- `docs/fable5-pattern-bank-for-chatgpt.md` — distilled observable behavior patterns.
- `docs/chatgpt-coding-rules.md` — coding/debug behavior.
- `docs/chatgpt-operational-integrity-rules.md` — file, tool, freshness, completion, and proportionality rules.
- `docs/chatgpt-proposal-review-rules.md` — proposal consistency review behavior.
- `docs/chatgpt-blog-rules.md` — technical blog behavior.
- `docs/chatgpt-transfer-instructions.md` — full combined guide.
- `docs/chatgpt-5.5-all-in-one-instructions.md` — single-paste fallback version.
- `prompts/chatgpt-task-prompts.md` — task-specific copy/paste prompts.
- `tests/GoldenTest-015.md` through `tests/GoldenTest-023.md` — Operational Integrity regression scenarios.

## Recommended Use

1. Add `CHATGPT.md` and the `docs/` files to ChatGPT Project knowledge/files.
2. Put the content of `CHATGPT.md` into the Project Instructions field if only one instruction field is available.
3. Let `CHATGPT.md` route each task to the smallest needed supporting files.

## Codex Use

```powershell
git clone https://github.com/yjj3019/ChatGPT.git
cd ChatGPT
```

Start Codex from this directory, or set this directory as the workspace root. Codex will read `AGENTS.md`, which points to the supporting `docs/codex-*.md` guidance files.

## Boundary

This repository transfers observable working patterns. It does not claim to copy Fable5 internals or hidden reasoning.

## Validate

GitHub Actions runs the same structure check on pushes and pull requests. Run it locally with:

```powershell
python scripts/validate_framework.py
```

