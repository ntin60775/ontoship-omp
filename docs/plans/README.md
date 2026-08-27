---
node_type: index
title: Plans — plan contracts + tickets
service: _platform
status: active
updated: 2026-08-27
---

# Plans

`docs/plans/` holds the **plan contracts**. A plan starts as a **file**
`docs/plans/<slug>.md` (`node_type: plan`), written by `mp-grill-with-docs`. When the
operator runs `/to-tickets`, the file is promoted to the **folder form**
`docs/plans/<slug>/`: the contract becomes the folder's `README.md`, and under it live
the **tickets** (`NN-<ticket>.md`, `node_type: ticket`) — tracer-bullet vertical slices,
each declaring the tickets that block it.

- The plan contract is written by `mp-grill-with-docs` (as a file); the tickets by
  `mp-to-tickets` (the only step that creates the folder).
- `/ship` executes **one ticket at a time**, strictly sequential: `/ship <folder>` takes
  the first ticket (by `NN` order) whose `status` is not `archived`. A **file plan** is
  shipped as a single slice: `/ship docs/plans/<slug>.md`.
- Lifecycle: plan `draft → active → archived` (shipped as a single slice, or all
  tickets done); ticket `draft → active → archived` (shipped).

- [contract-driven-ship.md](contract-driven-ship.md) — contract-spec: entry skills → hand `/ship` (superseded by the ticket-driven model)
- [plan-file-first.md](plan-file-first.md) — plan file by default; folder + tickets only after `/to-tickets`
- [command-inventory.md](command-inventory.md) — генерируемый реестр команд/навыков (`gitmark inventory` + I7), исключение эфемеры из индекса
