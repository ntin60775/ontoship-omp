---
node_type: service
title: grilling — the interview primitive
service: _platform
status: active
updated: 2026-08-28
tags: [service, grilling, interview]
links:
  documents: [../../../.omp/skills/grilling/SKILL.md, ../../../.omp/commands/grill.md, ../../../.omp/commands/grilling.md]
  relates_to: [../../services/mp-grill-with-docs/README.md, ../../services/domain-modeling/README.md, ../../services/mp-improve-codebase-architecture/README.md]
---

# grilling — the interview primitive

The interview primitive behind the "grill me" skills: the agent questions the user
relentlessly about a plan, decision, or idea — round by round — until both reach shared
understanding, resolving each branch of the decision tree.

Three entry points drive it:

- **`/grill`** — the slash command (`.omp/commands/grill.md`): the **plain** primitive —
  the same rounds and frontier, `domain-modeling` off, nothing written to the KB;
- **`/grilling`** — the slash command (`.omp/commands/grilling.md`): runs
  `mp-grill-with-docs` — a relentless interview over a plan, decision, or idea with
  `domain-modeling` active, ending in a plan contract file;
- **mp-improve-codebase-architecture** — after scanning a codebase and presenting an HTML
  report, grills through whichever deepening opportunity the user picks.

`grilling` is the engine; `mp-grill-with-docs` (grilling + domain-modeling) and
`mp-improve-codebase-architecture` are the user-facing wrappers. Invoke it when the user
wants to stress-test their thinking or says "grill me".
