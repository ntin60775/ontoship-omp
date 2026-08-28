---
node_type: index
title: OntoShip knowledge base
service: _platform
status: active
updated: 2026-08-28
links:
  part_of: [../AGENTS.md]
---

# OntoShip — knowledge base

Master index of the docs. Markdown is the source of truth; the search index
(`.gitmark/index.db`) and the HTML graph are **derived** — regenerate them, never commit
them as truth. See [ontology.md](ontology.md) for how documents are typed and linked.

## Reference

- [architecture.md](reference/architecture.md) — how OntoShip fits together (omp package → skills → commands → KB)
- [commands.md](reference/commands.md) — slash commands: `/kb`, `/kb-map`, `/doc`, `/onto-doc`, `/grilling`, `/architecture`, `/code-review`, `/to-tickets`, `/handoff`, `/prototype`, `/ship`
- [metrics.md](reference/metrics.md) — what OntoShip is measured by (experience-transfer metrics)
- [ontology.md](ontology.md) — the knowledge model (node_type, properties, typed links, linter)

## Decisions

- [ontoship-positioning.md](decisions/ontoship-positioning.md) — what OntoShip is for (team experience-transfer for AI-agent dev)
- [ticket-driven-ship.md](decisions/ticket-driven-ship.md) — plan file by default; folder + tickets only after `/to-tickets`; `/ship` runs one ticket (or one file plan) at a time, strictly sequential

## Plans

- [contract-driven-ship.md](plans/contract-driven-ship.md) — контракт-спек: входные навыки → ручной /ship (superseded by the ticket-driven model)
- [plan-file-first.md](plans/plan-file-first.md) — план-файл по умолчанию; папка + тикеты только после `/to-tickets`
- [command-inventory.md](plans/command-inventory.md) — генерируемый реестр команд/навыков; эфемера вне индекса
- [grill-command-pair.md](plans/grill-command-pair.md) — пара grilling-команд: `/grill` (обычный) + `/grilling` (с доками)

## Services

- [gitmark-cli](services/gitmark-cli/README.md) — KB search/index engine
- [kb-curate](services/kb-curate/README.md) — KB maintenance skill
- [dev-flow](services/dev-flow/README.md) — spec-driven ship pipeline
- [grilling](services/grilling/README.md) — the interview primitive (rounds + frontier)
- [domain-modeling](services/domain-modeling/README.md) — glossary + ADR discipline during design
- [mp-grill-with-docs](services/mp-grill-with-docs/README.md) — grill + domain model → plan contract file
- [mp-to-tickets](services/mp-to-tickets/README.md) — plan → tracer-bullet tickets
- [mp-diagnose](services/mp-diagnose/README.md) — hard-bug diagnosis → root cause for /ship
- [mp-prototype](services/mp-prototype/README.md) — throwaway prototype → data for the decision-maker
- [mp-handoff](services/mp-handoff/README.md) — session bridge (.scratch/), not KB knowledge
- [mp-code-review](services/mp-code-review/README.md) — two-axis code review (Standards + Spec) → report in .scratch/
- [mp-improve-codebase-architecture](services/mp-improve-codebase-architecture/README.md) — architectural scan + HTML report + grill
- [destructive-guard](services/destructive-guard/README.md) — destructive-command guard hook (archived: moved to its own repo, not part of the omp package)

## Ops

- [deploy-ontoship.md](ops/deploy-ontoship.md) — deploy the OntoShip package into a project (checklist with expected results)

## Derive

```bash
# from the repo root
python3 .omp/skills/kb-search/gitmark.py index            # build .gitmark/index.db
python3 .omp/skills/kb-search/gitmark.py search "query"   # FTS5 + trigram search
python3 .omp/skills/kb-search/gitmark.py lint             # check the ontology (I1–I6)
python3 .omp/skills/kb-search/gitmark.py map -o docs-map.html   # HTML overview + graph
```
