---
node_type: service
title: grilling — the interview primitive
service: _platform
status: active
updated: 2026-08-15
tags: [service, grilling, interview]
links:
  documents: [../../../.omp/skills/grilling/SKILL.md]
  relates_to: [../../services/mp-grill-me/README.md, ../../services/improve-codebase-architecture/README.md]
---

# grilling — the interview primitive

The interview primitive behind the "grill me" skills: the agent questions the user
relentlessly about a plan, decision, or idea — round by round — until both reach shared
understanding, resolving each branch of the decision tree.

Two skills drive it:

- **mp-grill-me** — a stateless brainstorm interview to sharpen a plan or design;
- **improve-codebase-architecture** — after scanning a codebase and presenting an HTML
  report, grills through whichever deepening opportunity the user picks.

`grilling` is the engine; the two skills above are the user-facing wrappers. Invoke it
when the user wants to stress-test their thinking or says "grill me".
