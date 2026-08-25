---
description: Break a plan (docs/plans/<slug>/) or the current conversation into tracer-bullet tickets with blocking edges under the plan folder. Argument = plan path or topic; empty = most recent plan.
---

Run the **mp-to-tickets** skill.

- `$ARGUMENTS` = a plan path (`docs/plans/<slug>/` or its `README.md`) or a topic.
  **Empty** → use the most recent `docs/plans/<slug>/` parent contract.
- The skill drafts tracer-bullet vertical slices (each sized to one fresh context
  window / one `/ship` run), gives each its blocking edges, quizzes the user on
  granularity and edges, then writes `docs/plans/<slug>/NN-<ticket>.md` (blockers first)
  and updates the parent contract's `Tickets` section.
- It lints + reindexes and stops. It does NOT launch `/ship` — the operator starts it by
  hand, one ticket at a time.
