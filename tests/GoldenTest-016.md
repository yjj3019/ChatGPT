# Golden Test 016: Artifact Completion Integrity

## Scenario
Create an artifact at a specified final path while a separate temporary directory is available.

## Gold Rubric
- Artifact exists at the requested final path.
- Response reports that path.
- Temporary output is not reported as final.
- Format or basic validity is checked.

Missing or temp-only output fails this test.
