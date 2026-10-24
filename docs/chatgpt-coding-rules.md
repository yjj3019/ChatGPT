# ChatGPT Coding Rules

Use for debugging, implementation, and review.

## Default Flow

1. Find the shared cause; scan sibling callers.
2. State assumptions; clarify material scope/contract/safety/authority ambiguity; decide reversible details.
3. Reproduce bugs when feasible; make the smallest root-cause fix.
4. Run minimal relevant checks; report unrun checks and gaps.
5. Check target path/workspace and diff: map hunks to the request/needed fixes; reject weakened tests, secrets, and generated noise.

## Required Report

```text
Root cause: ...
Change: ...
Verification: command, result, gaps
Caller scan: ...
Risks: ...
```

## Rules

- No one-off abstractions, speculative settings, or trivial-fix dependencies.
- For cleanup, check callers; remove newly unused imports/variables/functions; report unrelated existing dead code without deleting it.
- Test changed behavior; verify bugs fail-before/pass-after when feasible. Never weaken defect-sensitive assertions.
- Do not call failed commands or edits in temporary/redirected copies successful.
- Keep input/security checks; fix shared helpers when callers break.
