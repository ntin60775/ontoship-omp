---
node_type: service
title: mp-grill-me — interview → ship contract
service: _platform
status: active
updated: 2026-08-15
tags: [service, mp-grill-me, interview]
links:
  documents: [../../../.omp/skills/mp-grill-me/SKILL.md]
  relates_to: [../../services/grilling/README.md]
---

# mp-grill-me — interview → ship contract

A stateless interview skill that drives the `grilling` primitive to sharpen a plan or
design: the agent interrogates the user round by round, narrowing the decision tree
until the plan is crisp. When the frontier is empty, it writes the outcome as a
**ship contract** — `docs/plans/<slug>.md` (`node_type: plan`, `status: draft`) — then
stops; it never launches `/ship` (the operator starts it by hand).

Stateless — no session state carried between invocations; every run is a fresh
interview. Not invoked by the model directly (`disable-model-invocation: true` in the
skill frontmatter).
