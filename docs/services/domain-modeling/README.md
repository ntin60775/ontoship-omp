---
node_type: service
title: domain-modeling — glossary + ADR discipline
service: _platform
status: active
updated: 2026-08-25
tags: [service, domain-modeling, glossary, adr]
links:
  documents: [../../../.omp/skills/domain-modeling/SKILL.md]
  relates_to: [../../services/grilling/README.md, ../../services/mp-grill-with-docs/README.md]
---

# domain-modeling — glossary + ADR discipline

The *active* discipline of keeping the project's domain model current **during** design:
challenge terms against the `CONTEXT.md` glossary, sharpen fuzzy language, stress-test
relationships with concrete scenarios, cross-reference with code, and write glossary
terms and load-bearing decisions down the moment they crystallise.

Model-invoked (no user verb): the agent reaches for it while discussing terminology or
recording a decision. `mp-grill-with-docs` runs it alongside `grilling`.

- **Glossary** — `CONTEXT.md` (repo root): terms with definitions and `_Avoid_` lists,
  devoid of implementation details.
- **Decisions** — `docs/decisions/` (`node_type: decision`), offered sparingly: only
  when a choice is hard to reverse, surprising without context, and the result of a real
  trade-off.
