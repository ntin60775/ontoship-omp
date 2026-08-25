---
description: Code changes go through dev-flow only; the ship trigger is human-only.
alwaysApply: true
---

# Ship gate

- Code changes in this repo happen **only** through the `dev-flow` (`/ship`).
- Entry skills (`mp-grill-with-docs`, `mp-diagnose`, `mp-prototype`, `mp-handoff`,
  `mp-to-tickets`) end in a contract/ticket under `docs/plans/` or a handoff under
  `.scratch/` — they never edit code.
- `/ship` is launched **only by hand** by the operator, never by the agent on its own.
- One ticket per `/ship` run, strictly sequential.
