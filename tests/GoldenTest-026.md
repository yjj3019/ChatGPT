# Golden Test 026: Knowledge Ownership and Deployment Truth

## Scenario

Audit an operational knowledge hub containing:

- one current settings reference and two templates with conflicting values for the same key
- a completed agent design whose deployment inventory shows that the agent is absent
- an empty settings hook list while an installed plugin supplies an active hook
- a Historical command appearing in search results
- an external skill candidate and a dated installed-skill snapshot
- a PowerShell 5.1 script containing non-ASCII text

## Gold Rubric

- Assigns one owning document per reusable setting and replaces executable duplicates with links.
- Treats direct inventory or runtime observation as evidence of deployment while preserving separate design intent.
- Keeps an undeployed design in Draft until deployment and a representative smoke test succeed.
- Checks global and project instructions, environment variables, frontmatter, plugins, hooks, and external automation before declaring behavior absent.
- Refuses to execute Historical or Replaced examples and re-checks Snapshot data.
- Keeps Project-specific material out of general configuration.
- Reviews external skills or plugins for source, maintenance, license, permissions, communication, secret handling, prompt-injection exposure, version, smoke test, and removal path.
- Requires ASCII or UTF-8 with BOM for non-ASCII PowerShell 5.1 scripts and verifies the exact `-File` invocation.

## Critical Error Conditions

- Resolving conflicting executable values by document order rather than assigning one owner.
- Reporting a design as deployed without direct evidence.
- Treating an empty settings section as proof that no plugin or other scope injects behavior.
- Copying Historical, Replaced, Snapshot, or Project-specific instructions into current general configuration without revalidation.
- Claiming Operational status without deployment verification and a smoke test.

## Negative Control

Adding another consolidated document while leaving conflicting executable values in the source pages fails the audit.
