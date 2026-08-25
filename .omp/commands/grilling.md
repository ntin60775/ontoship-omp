---
description: Grill the user relentlessly about a plan, decision, or idea — rounds over the design tree until shared understanding, building the domain model (CONTEXT.md + decisions) as it goes, ending in a parent ship contract. Argument = the topic to grill.
---

Run the **mp-grill-with-docs** skill on the topic: `$ARGUMENTS`.

- `$ARGUMENTS` = the plan, decision, or idea to stress-test. **Empty** → ask what to grill.
- The skill holds the discipline: a `grilling` session (design tree, rounds, frontier —
  the agent finds facts itself, the decisions are the user's) with `domain-modeling`
  active — glossary terms go to `CONTEXT.md`, load-bearing choices to `docs/decisions/`
  as they crystallise.
- When the frontier is empty and the user confirms shared understanding, it writes the
  **parent ship contract** (`docs/plans/<slug>/README.md`, `node_type: plan`,
  `status: draft`) and stops.
- It does NOT author tickets and does NOT launch `/ship` — the operator runs
  `/to-tickets` (or says "разбей на тикеты") and then starts `/ship` by hand, one ticket
  at a time.
