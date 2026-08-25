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

Breaks a plan (`docs/plans/<slug>.md` or `docs/plans/<slug>/`) or the current
conversation into **tracer-bullet vertical slices**: each ticket cuts a narrow but
complete path through every layer, is sized to fit in a single fresh context window
(one `/ship` run), and declares the tickets that **block** it. Wide refactors are
sequenced expand–contract.

Driven by the `/to-tickets` command (or "разбей на тикеты"). If the plan is a **file**,
it is first promoted to the folder form (`git mv docs/plans/<slug>.md
docs/plans/<slug>/README.md`, links rewritten for the extra depth) — the folder is
created **only here**. Then it writes `docs/plans/<slug>/NN-<ticket>.md` (blockers
first), updates the plan's `Tickets` section, lints + reindexes, and stops. It does NOT
launch `/ship`.
