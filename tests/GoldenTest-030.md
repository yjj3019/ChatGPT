# Golden Test 030: Domain Section-Only Load (No Full Pack)

## Scenario

A Kubernetes-focused architecture review (for example: "Review this OpenShift-adjacent Kubernetes control-plane HA design" or "K8s storage class design review"). The user names a single platform domain and wants an architecture review deliverable — not a code patch, not a full transfer-guide dump.

## Gold Rubric

- Primary route: Architecture review (+ domain Kubernetes or OpenShift as named).
- Loads `docs/chatgpt-engineering-task-rules.md` **Architecture Review section only**.
- Loads **only** the matching domain section of `docs/chatgpt-domain-packs.md` (Kubernetes and/or OpenShift as named — not RHEL, Ansible, Satellite, EA, AI infra, EV, etc.).
- Applies Core Runtime; does **not** load transfer / all-in-one / fable5.
- Does **not** treat the entire domain-packs or engineering-task file as required content for every section.
- Distinguishes upstream Kubernetes vs OpenShift-specific behavior when both appear in the request.

## Negative Control

Loading every `##` section of `docs/chatgpt-domain-packs.md`, every engineering-task section, all `docs/codex-*.md`, or the transfer/all-in-one packs fails Context Budget and Intent Classifier domain/section-scope rules — even if the written architecture advice looks plausible.

## Protocol

Score: primary task type, engineering section-only + domain section-only load, forbidden heavy/full-pack loads avoided, architecture-review contract completeness.
