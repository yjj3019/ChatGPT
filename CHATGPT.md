# CHATGPT.md — Runtime Entry

If the referenced instruction files are not available in the ChatGPT Project knowledge/files, stop and report the missing file. Do not continue as if the rules were loaded.

## Purpose

This file is the single runtime entry point for the ChatGPT transfer pack. It tells ChatGPT which supporting files to read for each task. It does not duplicate all rules.

## Session Memory Bootstrap

At the start of a new ChatGPT project/session, read this `CHATGPT.md` first and treat its instructions as persistent working memory for the session. Then load the referenced project files according to the Autoload Protocol below. This is project-level memory bootstrap, not model fine-tuning or hidden memory mutation.
## Autoload Protocol

For each task:

1. Always apply the Core Runtime files below, in order.
2. For simple low-risk questions, answer with Core Runtime only.
3. For substantial tasks, use the Task Loading Map below.
4. Read only the files named for the task type.
5. If a selected file is missing from the project/context, stop and report the missing file. Do not silently substitute another file.

## Core Runtime Load Order

1. `docs/chatgpt-5.5-project-instructions.md`
2. `docs/fable5-pattern-bank-for-chatgpt.md`

These files are the baseline behavior pack for ChatGPT 5.5.

## Task Loading Map

| Task Type | Required Files | Optional Files |
|---|---|---|
| Coding/debugging | `docs/chatgpt-coding-rules.md` | `prompts/chatgpt-task-prompts.md` |
| Proposal consistency review | `docs/chatgpt-proposal-review-rules.md` | `prompts/chatgpt-task-prompts.md` |
| Technical blog post | `docs/chatgpt-blog-rules.md` | `prompts/chatgpt-task-prompts.md` |
| General Fable-style answer calibration | Core Runtime only | `docs/chatgpt-transfer-instructions.md` |
| One-shot copy/paste setup | `docs/chatgpt-5.5-all-in-one-instructions.md` | None |

## Selection Rules

1. Start with the user task, not the available files.
2. Load the smallest set that can answer accurately.
3. Do not load task files unrelated to the request.
4. Use `docs/chatgpt-transfer-instructions.md` only when the user asks for the full combined guide.
5. Use `docs/chatgpt-5.5-all-in-one-instructions.md` only when the user needs a single paste block, not for normal multi-file project use.

## Instruction Precedence

1. System / platform instructions
2. User task
3. This `CHATGPT.md`
4. Loaded ChatGPT transfer files

If a conflict appears, follow the higher-priority instruction and report the conflict when it affects the task.

## Runtime Rules

- Do not claim hidden Fable5 reasoning transfer.
- Treat this as observable behavior calibration only.
- Keep facts, assumptions, and open questions separate when it matters.
- Mark unsupported factual claims as `[unverified]`.
- For coding, prefer shared-root-cause fixes and verify the requested path/workspace.
- For external-facing documents, run one final consistency pass.


