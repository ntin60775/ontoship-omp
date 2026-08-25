---
node_type: index
title: Services
service: _platform
status: active
updated: 2026-08-25
links:
  part_of: [../README.md]
---

# Services

Component overviews — one folder per service/skill, each with a `README.md` index.

| Service | What it is |
|---|---|
| [gitmark-cli](gitmark-cli/README.md) | The KB search/index engine (`gitmark.py`) — FTS5 bm25 + trigram/fuzzy, HTML graph, ontology linter |
| [kb-curate](kb-curate/README.md) | The skill that keeps the markdown KB a typed ontology (CREATE/UPDATE/DEPRECATE/LINK/REINDEX) |
| [dev-flow](dev-flow/README.md) | The gated spec-driven ship pipeline (research → … → MR → dev → main) |
| [grilling](grilling/README.md) | The interview primitive (rounds + frontier) |
| [domain-modeling](domain-modeling/README.md) | Glossary + ADR discipline — keeps `CONTEXT.md` and `docs/decisions/` current during design |
| [mp-grill-with-docs](mp-grill-with-docs/README.md) | Grill + build the domain model → writes the plan contract file (`docs/plans/<slug>.md`) |
| [mp-to-tickets](mp-to-tickets/README.md) | Break a plan into tracer-bullet tickets with blocking edges |
| [mp-diagnose](mp-diagnose/README.md) | Hard-bug diagnosis loop → root cause for `/ship` |
| [mp-prototype](mp-prototype/README.md) | Throwaway prototype → data for the decision-maker |
| [mp-handoff](mp-handoff/README.md) | Session bridge (`.scratch/`), not KB knowledge |
| [improve-codebase-architecture](improve-codebase-architecture/README.md) | Architectural scan + deepening report |
| [destructive-guard](destructive-guard/README.md) | PreToolUse hook — archived: moved to its own repo, not part of the omp package |
