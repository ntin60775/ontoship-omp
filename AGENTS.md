# OntoShip — entry point

OntoShip is an **omp package** — a project-local `.omp/` (skills + commands + rules)
shipping **GitMark** — an md+git knowledge base (FTS5 search, HTML graph, ontology
linter) plus the spec-driven dev-flow built on top of it.

> **destructive-guard** (the PreToolUse safety hook) now lives in its own repo:
> [github.com/vakovalskii/destructive-guard](https://github.com/vakovalskii/destructive-guard).
> omp has its own built-in safety (extensions + rules), so the package ships without it.

## Where things live

```
.omp/
  skills/
    kb-search/         the gitmark CLI engine (gitmark.py) + SKILL.md
    kb-curate/         rules for maintaining the KB as a typed ontology
    dev-flow/          the gated ship pipeline
    grilling/          the interview primitive (rounds + frontier)
    domain-modeling/   glossary + ADR discipline (model-invoked)
    mp-grill-with-docs/ grill + domain model → plan contract (docs/plans/<slug>.md)
    mp-to-tickets/     plan file → folder + tracer-bullet tickets
    mp-diagnose/       hard-bug diagnosis loop → root cause for /ship
    mp-prototype/      throwaway prototype → data for the decision-maker
    mp-handoff/        session bridge (.scratch/), not KB knowledge
    improve-codebase-architecture/  architectural scan + deepening report
  commands/            slash commands: /kb /kb-map /doc /onto-doc /grilling /to-tickets /handoff /prototype /ship
  rules/               project rules (kb-source-of-truth, kb-first, ship-gate, ship-1c)
AGENTS.md              this entry point (read by omp)
docs/                  the knowledge base itself (this is the KB)
```

## Start here

- **Knowledge base** → [docs/README.md](docs/README.md) — master index
- **The model** → [docs/ontology.md](docs/ontology.md) — how docs are typed & linked
- **How it fits together** → [docs/reference/architecture.md](docs/reference/architecture.md)
- **Commands** → [docs/reference/commands.md](docs/reference/commands.md)

## Principle

Markdown + git is the source of truth. Everything derived — the search index
(`.gitmark/index.db`), the HTML graph — is regenerated, never committed as truth.
Every folder's `README.md` is its index; never let a doc become an orphan.

## Maintain

```bash
python3 .omp/skills/kb-search/gitmark.py index    # rebuild the index after editing docs
python3 .omp/skills/kb-search/gitmark.py lint     # check the ontology (broken links, orphans, frontmatter)
python3 .omp/skills/kb-search/gitmark.py map -o docs-map.html   # regenerate the graph
```
