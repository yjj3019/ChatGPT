# ChatGPT Coding Rules

Use for debugging, implementation, and code review.

## Default Flow

1. Identify the symptom.
2. Locate the shared boundary likely causing it.
3. Scan sibling callers/users of that boundary.
4. Apply the smallest root-cause fix.
5. Run or propose the smallest verification.
6. Confirm the result belongs to the requested path/workspace.
7. Inspect the final diff for unrelated changes, weakened tests, secrets, and generated-file noise.

## Required Report

```text
Root cause
- ...

Change
- ...

Verification
- Command: ...
- Result: ...

Caller scan
- ...

Risks
- ...
```

## Rules

- Do not add an abstraction for one implementation.
- Do not add dependencies for small parsing/formatting/control-flow fixes.
- Do not modify tests unless the task asks for test changes.
- If verification cannot be run, say exactly what remains unverified.
- Do not report a failed command or an edit in a temporary/redirected copy as successful.
- If several callers break from one helper, fix the helper.
