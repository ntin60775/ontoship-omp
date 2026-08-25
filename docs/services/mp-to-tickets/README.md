---
node_type: service
title: mp-to-tickets — plan → tracer-bullet tickets
service: _platform
status: active
updated: 2026-08-25
tags: [service, mp-to-tickets, tickets, plan]
links:
  documents: [../../../.omp/skills/mp-to-tickets/SKILL.md]
  relates_to: [../../services/mp-grill-with-docs/README.md, ../../services/dev-flow/README.md]
---

# mp-to-tickets — plan → tracer-bullet tickets

Breaks a plan (`docs/plans/<slug>/`) or the current conversation into **tracer-bullet
vertical slices**: each ticket cuts a narrow but complete path through every layer, is
sized to fit in a single fresh context window (one `/ship` run), and declares the
tickets that **block** it. Wide refactors are sequenced expand–contract.

Driven by the `/to-tickets` command (or "разбей на тикеты"). Writes
`docs/plans/<slug>/NN-<ticket>.md` (blockers first), updates the parent contract's
`Tickets` section, lints + reindexes, and stops. It does NOT launch `/ship`.
