---
node_type: service
title: mp-grill-with-docs — grill + domain model → parent contract
service: _platform
status: active
updated: 2026-08-25
tags: [service, mp-grill-with-docs, grilling, plan]
links:
  documents: [../../../.omp/skills/mp-grill-with-docs/SKILL.md]
  relates_to: [../../services/grilling/README.md, ../../services/domain-modeling/README.md, ../../services/mp-to-tickets/README.md]
---

# mp-grill-with-docs — grill + domain model → parent contract

A relentless interview to sharpen a plan or design, with `domain-modeling` active: as
terms and decisions crystallise, glossary terms go to `CONTEXT.md` and load-bearing
choices to `docs/decisions/`. When the frontier is empty and the user confirms shared
understanding, it writes the **parent ship contract** — `docs/plans/<slug>/README.md`
(`node_type: plan`, `status: draft`) — and stops.

Driven by the `/grilling` command. It does NOT author tickets (`mp-to-tickets` does) and
does NOT launch `/ship` — the operator runs `/to-tickets` and then starts `/ship` by
hand, one ticket at a time.
