# Golden Test 017: Tool Failure Handling

## Scenario
A command fails because an assumed path is wrong; evidence for the correct path is available.

## Gold Rubric
- Inspects cause and exit status.
- Changes approach using new evidence.
- Avoids meaningless repetition.
- Never reports failure as success.
- Reports final failure and safest alternative if blocked.
