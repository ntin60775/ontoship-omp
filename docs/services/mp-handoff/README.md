---
node_type: service
title: mp-handoff — session bridge
service: _platform
status: active
updated: 2026-08-17
tags: [service, mp-handoff, handoff]
links:
  documents: [../../../.omp/skills/mp-handoff/SKILL.md]
  relates_to: [../../services/mp-grill-me/README.md]
---

# mp-handoff — session bridge

Compacts the current conversation into a handoff document under `.scratch/` so a fresh
agent can continue. A bridge between sessions, not a source of knowledge: it references
the KB (`docs/plans/`, `docs/decisions/`) rather than restating it, and never authors the
ship contract.
