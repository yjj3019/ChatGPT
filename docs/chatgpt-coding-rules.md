# ChatGPT Coding Rules

Use for debugging, implementation, and code review.

## Default Flow

1. Identify the symptom.
2. Locate the shared boundary likely causing it.
3. Scan sibling callers/users of that boundary.
4. Apply the smallest root-cause fix.
5. Run or propose the smallest verification.
6. Confirm the result belongs to the requested path/workspace.

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
- If several callers break from one helper, fix the helper.
