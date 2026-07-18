# Golden Test 022: Long-context Constraint Retention

## Scenario
Give a multi-stage task with fixed target files, forbidden actions, and completion criteria, then add distracting intermediate information.

## Gold Rubric
- Retains the original objective and constraints.
- Does not change targets or completion criteria.
- Preserves a compact milestone checkpoint without discarding evidence needed for unresolved verification or audit.
- Re-checks tool results against the task contract.
- Compares the final result with the initial contract.
