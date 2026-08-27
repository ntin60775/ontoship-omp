---
node_type: service
title: improve-codebase-architecture — scan, report, grill
service: _platform
status: active
updated: 2026-08-15
tags: [service, architecture, deep-modules]
links:
  documents: [../../../.omp/skills/improve-codebase-architecture/SKILL.md, ../../../.omp/skills/improve-codebase-architecture/HTML-REPORT.md]
  relates_to: [../../services/grilling/README.md]
---

# improve-codebase-architecture — scan, report, grill

Scans a codebase for **deepening opportunities** (deep modules, narrow interfaces),
presents them as a visual HTML report, then drives the `grilling` primitive to walk the
user through whichever opportunity they pick.

Ships two files: `SKILL.md` (the procedure) and `HTML-REPORT.md` (the report template
the skill renders into). Not invoked by the model directly
(`disable-model-invocation: true` in the skill frontmatter).
