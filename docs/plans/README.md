---
node_type: index
title: Plans — parent contracts + tickets
service: _platform
status: active
updated: 2026-08-25
---

# Plans

`docs/plans/` holds the **parent ship contracts** — one folder per plan
(`docs/plans/<slug>/`): the parent contract is the folder's `README.md`
(`node_type: plan`), and under it live the **tickets** (`NN-<ticket>.md`,
`node_type: ticket`) — tracer-bullet vertical slices, each declaring the tickets that
block it.

- The parent contract is written by `mp-grill-with-docs`; the tickets by `mp-to-tickets`.
- `/ship` executes **one ticket at a time**, strictly sequential: `/ship <plan>` takes
  the first ticket (by `NN` order) whose `status` is not `archived`.
- Lifecycle: parent `draft → active → archived` (all tickets done); ticket
  `draft → active → archived` (shipped).

- [contract-driven-ship.md](contract-driven-ship.md) — contract-spec: entry skills → hand `/ship` (superseded by the ticket-driven model)
