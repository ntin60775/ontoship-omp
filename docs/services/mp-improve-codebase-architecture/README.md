---
node_type: service
title: mp-improve-codebase-architecture — scan, report, grill
service: _platform
status: active
updated: 2026-08-27
tags: [service, architecture, deep-modules]
links:
  documents: [../../../.omp/skills/mp-improve-codebase-architecture/SKILL.md, ../../../.omp/skills/mp-improve-codebase-architecture/HTML-REPORT.md, ../../../.omp/commands/architecture.md]
  relates_to: [../../services/grilling/README.md, ../../reference/commands.md]
---

# mp-improve-codebase-architecture — scan, report, grill

Scans a codebase for **deepening opportunities** (deep modules, narrow interfaces),
presents them as a visual HTML report, then drives the `grilling` primitive to walk the
user through whichever opportunity they pick.

- **Entry point:** the `/architecture` slash command (`.omp/commands/architecture.md`).
  The skill itself is not invoked by the model
  (`disable-model-invocation: true` in the skill frontmatter).
- Ships two files: `SKILL.md` (the procedure) and `HTML-REPORT.md` (the report template
  the skill renders into). The HTML report goes to the OS temp dir, never into the repo.
- Ends by handing the chosen candidate to `/grilling`, which writes the plan contract —
  so the whole chain stays inside OntoShip: scan → report → grill → `docs/plans/<slug>.md`
  → `/to-tickets` → `/ship`.
