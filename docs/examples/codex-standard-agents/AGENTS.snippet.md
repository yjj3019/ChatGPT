<!-- BEGIN TRANSFER PACK STANDARD DELEGATION -->
## Optional model-inheriting delegation

- Keep the recipient host's current model, reasoning effort, and permissions. This optional policy does not enable agents or install role files.
- When the supported roles are available, prefer `pack_explorer` for scoped file/caller/documentation research and `pack_runner` for specified tests, lint, type checks, builds, and log analysis. Handle tiny tasks directly when delegation costs more.
- The main owns design, edits, complex debugging, integration, and final judgment. Give children only the needed scope, commands, evidence, and acceptance criteria; prefer fresh context. Require concise file:line evidence and gaps, then verify important facts in the originals.
- Run only independent tasks in parallel. Avoid simultaneous edits to the same files. Verify search coverage when omissions matter; children must not delegate again.
- Call `pack_reviewer` only before finalizing an important design/implementation direction or after two unsuccessful fix/retest attempts for the same error. Pause further fixes after the second failure and supply the error, attempts, and assumptions. Reviewer advice is evidence, not authority.
- Explorer/Reviewer do not edit. Runner may produce only the outputs required by specified checks within granted permissions. Child permissions are inherited; no independent read-only sandbox is claimed.
- Do not pass model/effort overrides for this baseline. If a role or capability is unavailable, report the gap and retain the main workflow; do not guess another model, enable features, or expand permissions.
<!-- END TRANSFER PACK STANDARD DELEGATION -->
