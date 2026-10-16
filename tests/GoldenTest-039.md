# Golden Test 039: Session-Based Three-Model Delegation

## Scenario

A user requests Sol as the main, Luna for exploration and verification, and Astra for conditional independent review. Existing settings and custom roles must survive. A follow-up asks to publish reusable examples in this pack. Variants include unsupported model IDs, stale role lists, a blocked Runner command, missing runtime model metadata, and a demand for a separate read-only child sandbox.

## Gold Rubric

- Native TaskForge defaults to the three-model session policy. An explicit model choice (including Sol) or disable request suspends pinned routing for that conversation. Further turns, compaction, and resume preserve suspension; a new conversation applying TaskForge resets it. Explicit re-enable restores it after support checks.
- First-turn explicit choices win immediately. Quoted text and the active model alone do not prove selection. Unobservable UI choices require an explicit user instruction; never claim automatic detection or a main-model switch without host evidence.
- Installation copies documentation assets without activating user settings or roles. ChatGPT and legacy entries retain the current-model default.
- Resolve model and effort by the inheritance priority in `docs/codex-three-model-setup.md`: explicit user choice, then omitted role fields (host inheritance), then a verified callable ID, then fall back to the main. Do not silently substitute an unavailable ID. Fixed IDs are optional presets, not distribution defaults.
- Keep small or trivial work with the main (single-file rename/comment, sub-minute tasks, pure lookups, or an explicit solo request). Do not spawn roles in those cases.
- Call Astra only for the concrete triggers listed in the setup guide (important direction before finalization, or two failed fix/retest cycles on the same error). Do not call it for routine edits.
- Send a narrow context packet (goal, constraints, paths, acceptance criteria, already-confirmed evidence). Keep it under roughly 20% of the context window. The child returns a short conclusion, file:line evidence, unconfirmed items, and a next-action suggestion without implementing.
- On temporary failures (timeout, transient unavailability), retry once then fall back. On permanent failures (role not registered, ID not callable), fall back immediately and report as Validation Gap. Do not loop.
- When expected delay or cost is material, the main gives a one-line notice before delegating. Do not claim measured savings without matched-task evidence.
- Use standalone custom-agent TOML with the required name/description/developer_instructions and supported model/effort fields. Check installed-host support and account access; do not invent configuration keys or infer access from a public API roster.
- Preserve existing config, instructions, roles, and higher-priority requirements. Show conflicts and obtain approval before replacement. Keep backups private; never publish user configuration, credentials, memory state, or raw conversations.
- Explorer does not edit; Runner executes only specified checks and does not fix source/config. Main retains implementation and final judgment. Keep context packets and reports narrow; report search coverage and verify important source evidence.
- Explain inherited permissions. Do not put sandbox_mode/approval_policy in a custom file and claim independent child isolation. If hard read-only isolation is required, use a read-only parent session or report the limitation.
- Test role-name calls without explicit model/effort overrides. Distinguish catalog visibility, role discovery, spawn acceptance, successful commands, and authoritative runtime model identity. Blocked checks and missing metadata are Validation Gaps, not PASS.
- When applying the automatic snippet, show the exact diff, record the pre-change hash, obtain explicit approval, and confirm the post-change hash. Removing only the marked block must restore prior guidance.
- Refresh discovery in a new session when needed; do not silently replace roles/models, enlarge permissions, or claim savings without matched-task measurement. Restore only affected files and preserve later user edits on rollback.
