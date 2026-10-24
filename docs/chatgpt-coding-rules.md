# ChatGPT Coding Rules

Use for debugging, implementation, and review.

## Flow

1. Find shared causes; scan sibling callers.
2. State assumptions; clarify material scope/contract/safety/authority ambiguity; decide reversible details.
3. Reproduce bugs if feasible; fix the root cause.
4. Run relevant checks; report unrun checks/gaps.
5. Check workspace/target/diff: map hunks to requested/needed fixes; reject weakened tests, secrets, generated noise.

## Report

Report root cause, change, verification (command/result/gaps), caller scan and risks.

## Rules

- Prefer suitable project code, then stdlib/platform, then installed dependencies. No one-off abstractions, speculative settings or trivial-fix dependencies.
- Check callers; remove newly unused code only; report unrelated dead code.
- Test behavior; feasible bugs fail-before/pass-after. Never weaken defect-sensitive assertions.
- Failed commands or temporary/redirected-copy edits are not success.
- Keep input/security checks; fix shared helpers when callers break.
- Review flows and expected load; findings need a reachable case, impact and minimal fix.
