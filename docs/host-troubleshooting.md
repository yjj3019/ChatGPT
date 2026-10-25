# Windows and Orca environment checks

This document summarizes observations from Windows and Orca accounts using TaskForge for ChatGPT. It records one environment; the findings do not apply equally to every recipient. Recheck the current state on the relevant host.

## CreateProcessWithLogonW 1326

- Symptom: logon fails when running a command.
- Observation: some retries have succeeded. Account permissions or security policy are suspected as the root cause, but this is unconfirmed.
- Action: check the process permissions and, if it fails, retry in a standard user session. The pack does not expand permissions.

## Hook timeouts

- A 10-second timeout has been reported with the default settings.
- A separate diagnostic completed 20/20 runs with a 30-second budget; the longest observed run took 14.549 seconds.
- PermissionRequest and Interrupt were not exercised in that test.
- Action: record the host's Hook budget separately from the actual execution time. The pack does not change host Hook settings.

## Orca accounts and CODEX_HOME

- An Orca account may use a different home from standard Codex.
- If the global AGENTS.md is a symbolic link, edit the target file only once and preserve the link.
- Check role discovery and model availability separately for each account.

## Role discovery

- In some cases, the role list refreshes only in a new process.
- Existing conversations may retain the previous role list.
- After invoking a role by name, check its runtime metadata (model and reasoning effort). Do not record success based on self-report alone.

## Verification procedure

1. Record `codex --version` and the version of the client actually in use.
2. Check the role list in a new process.
3. Perform a harmless fixture read (Explorer) and run a specified command (Runner), recording the exit codes.
4. Compare protected-file hashes before and after.
5. Mark failed items as Validation Gaps and limit success claims to that environment.

These items are documented separately from the [2026-10-16 verification record](host-verification-2026-10-16.md).
