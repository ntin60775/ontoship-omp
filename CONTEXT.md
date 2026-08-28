# OntoShip

A project-local **omp package** that turns a repo's markdown into a searchable, typed
knowledge base (KB) and ships a gated dev-flow on top of it. Markdown + git is the source
of truth; everything derived is regenerated.

## Language

**KB (knowledge base)**:
The repo's markdown (`docs/`, README files, any `*.md`) treated as the project's
knowledge — searchable via GitMark, typed via the ontology.
_Avoid_: wiki, memory bank, documentation site

**GitMark**:
The engine: a zero-dependency Python-stdlib CLI (`gitmark.py`) that indexes, searches,
lints, and renders the KB.
_Avoid_: the search plugin, the tool

**Пакет (package)**:
The `.omp/` directory (skills + commands + rules) plus the `AGENTS.md` entry point,
copied into a project to enable OntoShip. omp's native provider discovers it from the
project root.
_Avoid_: плагин, marketplace, plugin

**Скилл (skill)**:
A `.omp/skills/<name>/SKILL.md` capability the agent invokes: `kb-search`, `kb-curate`,
`dev-flow`.
_Avoid_: плагин, под-команда

**Команда (command)**:
A `.omp/commands/<name>.md` slash-command (`/kb`, `/kb-map`, `/doc`, `/onto-doc`,
`/grill`, `/grilling`, `/architecture`, `/code-review`, `/to-tickets`, `/handoff`,
`/prototype`, `/ship`) — the user-facing verbs that drive skills and the CLI.
_Avoid_: слэш-команда Claude Code, plugin command

**Точка входа (entry point)**:
The root `AGENTS.md` — the file the omp agent reads first to orient in the repo.
_Avoid_: CLAUDE.md

**Онтология (ontology)**:
The knowledge model over the KB — `node_type`, frontmatter properties, typed links,
invariants I1–I6 (see `docs/ontology.md`).
_Avoid_: модель данных, схема

**Куратор (curator)**:
An agent that creates/updates KB documents following `kb-curate`; `/onto-doc` fans out
one curator per doc area.
_Avoid_: документатор, писатель

**Dev-flow**:
The gated ship pipeline, **one ticket at a time**, strictly sequential: worktree →
implement → tests → review → dev-tests → prod-tests → ship (MR → `dev` → `main`).
_Avoid_: CI/CD, релизный процесс

**Код-ревью (code review)**:
An on-demand, read-only review of a diff along two separate axes — **Standards** (the
repo's documented standards plus a fixed smell baseline) and **Spec** (the originating
plan or ticket) — reported side by side, never merged. Distinct from **review** below:
the gate inside a `/ship` run, which checks the author's own diff before rollout.
_Avoid_: аудит, ревью кода как часть шипа

**Ревью-гейт (review gate)**:
Step 6 of Dev-flow: an independent omp sub-agent (read-only, on the `@reviewer` model
role, fallback `@slow`) reads the diff of the change being shipped.
A gate in the pipeline, not a standalone report.
_Avoid_: код-ревью

**Derived-артефакты (derived artifacts)**:
Regenerated outputs — `.gitmark/index.db` (search index) and `*-map.html` (graph).
Never edited or committed by hand.
_Avoid_: кэш, база знаний

**План (plan)**:
A file `docs/plans/<slug>.md` (`node_type: plan`) — the ship contract. Written by
`mp-grill-with-docs`. `mp-to-tickets` promotes it to the folder `docs/plans/<slug>/`
(contract → `README.md` + tickets) — the only step that creates the folder.
_Avoid_: задача, тикет, спринт

**Тикет (ticket)**:
A tracer-bullet vertical slice of a plan (`docs/plans/<slug>/NN-<ticket>.md`,
`node_type: ticket`), sized to one fresh context window; one `/ship` run each, strictly
sequential. Written by `mp-to-tickets`.
_Avoid_: задача, story, подзадача

**Доменная модель (domain model)**:
The project's ubiquitous language — the `CONTEXT.md` glossary plus load-bearing choices
in `docs/decisions/`. Kept current during design by the `domain-modeling` skill.
_Avoid_: модель данных, схема БД

**Грилл (grill)**:
The plain interview over a design tree — rounds and a frontier, no durable output.
The lightweight entry: think out loud, decide nothing is worth recording yet. When the
conclusions do deserve the KB, the operator re-runs the documented variant on the same
thread.
_Avoid_: допрос, собеседование

**Грилл с доками (grill with docs)**:
The same interview with the domain model active: terms crystallise into the glossary,
load-bearing choices into decisions, and the confirmed outcome becomes a **План**. The
only grilling that leaves durable artifacts.
_Avoid_: grilling-полный, grill-me
