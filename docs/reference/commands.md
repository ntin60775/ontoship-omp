---
node_type: reference
title: OntoShip slash commands
service: _platform
status: active
updated: 2026-08-27
tags: [commands, slash-commands, reference]
links:
  documents: [../../.omp/commands/kb.md, ../../.omp/commands/kb-map.md, ../../.omp/commands/doc.md, ../../.omp/commands/onto-doc.md, ../../.omp/commands/grilling.md, ../../.omp/commands/architecture.md, ../../.omp/commands/code-review.md, ../../.omp/commands/to-tickets.md, ../../.omp/commands/handoff.md, ../../.omp/commands/prototype.md, ../../.omp/commands/ship.md]
  relates_to: [../services/gitmark-cli/README.md, ../services/dev-flow/README.md]
---

# OntoShip slash commands

Reference for the slash commands shipped by the **OntoShip** omp package. Each command is
a thin `.omp/commands/*.md` definition that drives a skill or engine. Four families:

- **KB curation & search** — `/kb`, `/kb-map`, `/doc`, `/onto-doc` — drive the GitMark
  CLI (`.omp/skills/kb-search/gitmark.py`) and the `kb-curate` ontology rules.
- **Design & knowledge** — `/grilling` (grill + build the domain model → parent
  contract), `/architecture` (scan for deepening opportunities → HTML report → grill the
  chosen candidate), `/to-tickets` (break a plan into tracer-bullet tickets), `/handoff`
  (session bridge), `/prototype` (throwaway prototype for a design question).
- **Review** — `/code-review` (two-axis Standards/Spec review of a diff → report in
  `.scratch/`, read-only).
- **Dev-flow** — `/ship` — drives the gated `dev-flow` pipeline, **one ticket at a
  time**, strictly sequential.

The GitMark CLI is `.omp/skills/kb-search/gitmark.py` (relative to the repo root; stable
when the `.omp/` package is copied into another project).

## Summary

| Command | What it does | Args | Drives |
|---|---|---|---|
| `/kb` | Search the project KB (all `.md`) and answer from the top hits | `<query>` (empty → stat + usage) | GitMark CLI `search` / `stat` / `index` |
| `/kb-map` | Build a self-contained HTML map of the KB (tree + link graph) | `[output-path]` (default `docs-map.html`) | GitMark CLI `map` / `index` |
| `/doc` | Compose or update **one** KB document per the ontology | `<topic>` | `kb-curate` skill + GitMark CLI |
| `/onto-doc` | Build (or rebuild) the **whole** KB by fanning out curator agents | `[scope]` (empty → whole repo) | `kb-curate` skill via `Task` fan-out + GitMark CLI |
| `/grilling` | Grill the user about a plan/decision/idea, building the domain model, ending in a plan contract file | `<topic>` (empty → ask what to grill) | `mp-grill-with-docs` skill |
| `/architecture` | Scan for deepening opportunities, show an HTML report, grill the chosen candidate into a plan contract | `[direction]` (empty → infer hot spots from git history) | `mp-improve-codebase-architecture` skill |
| `/code-review` | Review the diff since a fixed point on two axes (Standards + Spec) via parallel sub-agents; report side by side | `<fixed-point>` (empty → ask) | `mp-code-review` skill |
| `/to-tickets` | Break a plan into tracer-bullet tickets with blocking edges | `[plan path]` (empty → most recent plan) | `mp-to-tickets` skill |
| `/handoff` | Compact the conversation into a handoff doc under `.scratch/` | `[what the next session will do]` | `mp-handoff` skill |
| `/prototype` | Build a throwaway prototype to answer a design question | `<question>` (empty → ask) | `mp-prototype` skill |
| `/ship` | Ship **one ticket** from a plan folder (or a whole **file plan** as a single slice) through the gated pipeline, strictly sequential | `[plan path]` / `[ticket path]` / `<ad-hoc>` | `dev-flow` skill |

---

## `/kb` — search the knowledge base

- **Definition:** `.omp/commands/kb.md`
- **What it does:** searches every `.md` in the project (docs/, READMEs, etc.) via GitMark
  (FTS5 bm25 ranking + trigram/fuzzy matching), then summarizes the top hits and answers
  from the 1–2 most relevant files.
- **Args:** `$ARGUMENTS` = the search query. **Empty** → runs `gitmark.py stat` and shows
  the `/kb <query>` syntax instead of searching.
- **Behavior:**
  1. Empty query → `gitmark.py stat` + usage hint.
  2. Otherwise: refresh index if needed (`gitmark.py index`), then
     `gitmark.py search "$ARGUMENTS" -k 8`, summarize hits as `file:line` (no full
     snippets), and open the most relevant files to answer.
- **Drives:** GitMark CLI (`kb-search` skill).

## `/kb-map` — render the KB graph

- **Definition:** `.omp/commands/kb-map.md`
- **What it does:** generates a self-contained HTML map of the knowledge base — a
  collapsible tree, rendered markdown, and a force/radial link graph built from the typed
  links in frontmatter.
- **Args:** `$ARGUMENTS` = output path. **Default `docs-map.html`** when omitted.
- **Behavior:**
  1. Refresh the index: `gitmark.py index`.
  2. Build the map: `gitmark.py map -o "${ARGUMENTS:-docs-map.html}"`.
  3. Report the output path and offer to `open <path>` or `serve` it.
- **Drives:** GitMark CLI `map` (`kb-search` skill).

## `/doc` — compose/update one KB document

- **Definition:** `.omp/commands/doc.md`
- **What it does:** composes or updates a **single** KB document for a topic, following the
  `kb-curate` ontology (node_type, frontmatter, typed links, folder README index).
- **Args:** `$ARGUMENTS` = the topic/document subject.
- **Behavior (per `kb-curate`):**
  1. **Search first** (`gitmark.py search`) — if the topic exists, edit that doc; never
     create a duplicate.
  2. **Pick a `node_type`** (`service` · `reference` · `runbook` · `gotcha` · `decision` ·
     `plan` · `guide` · `report` · `index`) and the right folder.
  3. **Write frontmatter** — `node_type`, `title`, `service`, `status: active`,
     `updated: <today>`.
  4. **Add ≥1 typed link** (to code or a sibling doc) — no orphans.
  5. **Add a line to the folder `README.md`** index.
  6. **Lint + reindex** — `gitmark.py lint` then `gitmark.py index`.
- **Drives:** `kb-curate` skill + GitMark CLI. Wraps `gitmark:doc`.

## `/onto-doc` — build the whole KB

- **Definition:** `.omp/commands/onto-doc.md`
- **What it does:** builds (or rebuilds) the **entire** OntoShip KB for the repo by
  surveying the codebase and fanning out `kb-curate` curator subagents per area, then
  linting, indexing, and mapping. Used to bootstrap or rebuild a project's whole KB.
- **Args:** `$ARGUMENTS` = scope hint. **Empty** → whole repo; or a subset
  (e.g. `services/api services/billing`, or "only reference docs").
- **Behavior:**
  1. **Survey** the repo (dirs, services, entry points, build/deploy, existing docs);
     check coverage with `gitmark.py stat`.
  2. **Decompose** into doc areas — service READMEs (`service`), cross-cutting specs
     (`reference`), ops procedures (`runbook`/`gotcha`), decisions (`decision`).
  3. **Dispatch curators (fan-out)** — one `Task` subagent per area, each following
     `kb-curate` on its slice only (search first, pick node_type + folder, frontmatter,
     ≥1 typed link, README index line). Independent areas run in parallel, scoped to avoid
     collisions.
  4. **Entry point + indexes** — ensure `AGENTS.md` exists, `docs/README.md`
     is the master index, every folder has a README index.
  5. **Verify & derive** — `gitmark.py lint` (fix broken links/orphans/missing
     frontmatter), then `gitmark.py index`, then `gitmark.py map -o docs-map.html`.
  6. **Report** — docs created/updated, coverage before→after, lint result, map path,
     areas needing a human decision.
- **Drives:** `kb-curate` skill via `Task` fan-out + GitMark CLI. Wraps `gitmark:onto-doc`.

## `/grilling` — grill a plan, decision, or idea

- **Definition:** `.omp/commands/grilling.md`
- **What it does:** runs the `mp-grill-with-docs` skill — a relentless round-by-round
  interview over the design tree (the `grilling` primitive) with `domain-modeling`
  active: glossary terms go to `CONTEXT.md`, load-bearing choices to `docs/decisions/`
  as they crystallise. When the frontier is empty and the user confirms shared
  understanding, it writes the **plan contract** — `docs/plans/<slug>.md`
  (`node_type: plan`, `status: draft`) — and stops. The folder with tickets is created
  later, only by `/to-tickets`.
- **Args:** `$ARGUMENTS` = the plan, decision, or idea to stress-test. **Empty** → ask
  what to grill.
- **Behavior:** the skill holds the discipline — map the design tree, ask the whole
  frontier in one round (numbered, each with a recommended answer), recompute the
  frontier after each round. The agent finds facts itself (sub-agents); the decisions
  are the user's. Done when the frontier is empty; do not act until the user confirms.
- **Drives:** `mp-grill-with-docs` skill (grilling + domain-modeling).

## `/architecture` — deepen the architecture

- **Definition:** `.omp/commands/architecture.md`
- **What it does:** runs the `mp-improve-codebase-architecture` skill — surfaces
  architectural friction and proposes **deepening opportunities** (refactors that turn
  shallow modules into deep ones) using a fixed vocabulary (module, interface, depth,
  seam, adapter, leverage, locality) and the deletion test.
- **Args:** `$ARGUMENTS` = an optional direction (a module, subsystem, or pain point).
  **Empty** → the skill infers hot spots by walking `git log` (YAGNI: weight where change
  is landing).
- **Behavior:**
  1. **KB first** — `gitmark search` for `CONTEXT.md` vocabulary and `docs/decisions/`;
     recorded decisions are not re-litigated.
  2. **Scan** via a sub-agent for friction; apply the deletion test to suspects.
  3. **HTML report** — self-contained, written to the OS temp dir (never into the repo),
     one card per candidate with before/after and a recommendation badge, plus a top
     recommendation. Then: "Which of these would you like to explore?"
  4. **Grill the chosen candidate** — the `/grilling` loop (`mp-grill-with-docs`) walks
     the decision tree; terms go to `CONTEXT.md`, choices to `docs/decisions/`; the
     outcome is the **plan contract** `docs/plans/<slug>.md`.
- **Stops there:** no refactoring, no tickets, no `/ship` — the operator runs
  `/to-tickets` and starts `/ship` by hand.
- **Drives:** `mp-improve-codebase-architecture` skill → `mp-grill-with-docs`.

## `/code-review` — two-axis review of a diff

- **Definition:** `.omp/commands/code-review.md`
- **What it does:** runs the `mp-code-review` skill — reviews the diff between `HEAD` and
  a fixed point along two deliberately separate axes, each handled by its own parallel
  sub-agent:
  - **Standards** — conformance to the repo's documented standards (`.omp/rules/`,
    `AGENTS.md`, `CONTEXT.md` vocabulary, `docs/decisions/`) plus a fixed Fowler smell
    baseline (12 smells). A documented repo standard overrides the baseline; smells are
    always judgement calls, never hard violations.
  - **Spec** — faithfulness to the originating plan contract / ticket in `docs/plans/`
    (missing requirements, scope creep, wrong implementation). No spec → the axis skips
    and reports it.
- **Args:** `$ARGUMENTS` = the fixed point (a SHA, branch, tag, `main`, `HEAD~5`).
  **Empty** → ask for it. The skill verifies the ref resolves and the diff is non-empty
  before spawning sub-agents.
- **Behavior:** pin the fixed point → find the spec in the KB → collect standards sources
  → spawn both sub-agents in parallel → aggregate the two reports **side by side, never
  merged or reranked across axes** → write the report to
  `.scratch/code-review-<timestamp>.md`.
- **Boundaries:** read-only — no fixes, no plan contract, no tickets, no `/ship`. The
  report is ephemeral (`.scratch/`), not a KB doc. If the operator decides to fix, the
  findings go to `/grilling` → `/to-tickets` → `/ship`; a durable trap becomes a `gotcha`.
- **Drives:** `mp-code-review` skill.


## `/to-tickets` — break a plan into tickets

- **Definition:** `.omp/commands/to-tickets.md`
- **What it does:** runs the `mp-to-tickets` skill — breaks a plan (or the current
  conversation) into **tracer-bullet vertical slices**, each declaring the tickets that
  block it. Each ticket is sized to fit in a single fresh context window (one `/ship`
  run).
- **Args:** `$ARGUMENTS` = a plan path (`docs/plans/<slug>.md`, `docs/plans/<slug>/`, or
  its `README.md`) or a topic. **Empty** → use the most recent plan (a file or a folder,
  by `updated:`).
- **Behavior:** if the plan is a **file**, first promote it to the folder form
  (`git mv docs/plans/<slug>.md docs/plans/<slug>/README.md`, rewrite the plan's outgoing
  links for the extra depth and the incoming links from other docs). Then drafts the
  slices, gives each its blocking edges, quizzes the user on granularity and edges, and
  writes `docs/plans/<slug>/NN-<ticket>.md` (blockers first) and updates the plan's
  `Tickets` section. Lints + reindexes and stops.
- **Drives:** `mp-to-tickets` skill.

## `/handoff` — session bridge

- **Definition:** `.omp/commands/handoff.md`
- **What it does:** runs the `mp-handoff` skill — compacts the current conversation into
  a handoff document under `.scratch/` so a fresh agent can continue. A bridge between
  sessions, not a KB doc: it references the KB rather than restating it.
- **Args:** `$ARGUMENTS` = what the next session will focus on. **Empty** → summarize
  the whole conversation.
- **Drives:** `mp-handoff` skill.

## `/prototype` — throwaway prototype

- **Definition:** `.omp/commands/prototype.md`
- **What it does:** runs the `mp-prototype` skill — builds a throwaway prototype to
  answer a design question (logic/state → single HTML file; UI → several radically
  different variations on one route). Returns **data and a recommendation**, never
  commits code.
- **Args:** `$ARGUMENTS` = the design question. **Empty** → ask what to prototype.
- **Drives:** `mp-prototype` skill.

## `/ship` — ship one ticket (or one file plan)

- **Definition:** `.omp/commands/ship.md`
- **What it does:** drives **one ticket** from a plan folder (or a whole **file plan**
  as a single slice) through the gated OntoShip dev-flow pipeline. Launched **only by
  hand**, **one ticket (or one file plan) at a time**, strictly sequential.
- **Args:** `$ARGUMENTS` = a **plan folder** (`docs/plans/<slug>/`), a **file plan**
  (`docs/plans/<slug>.md`), a **ticket path** (`docs/plans/<slug>/NN-<ticket>.md`), an
  ad-hoc description, or **empty** (most recent plan — a file or a folder, by
  `updated:`). `docs/plans/<slug>` without an extension resolves to whichever exists.
- **Entry (plan folder):** pick the **first ticket** (by `NN` order) whose `status` is
  not `archived`. Check its `Blocked by` tickets are all archived (if not, report
  blockers and stop). Check `Context` in the parent contract is still accurate; set
  ticket `status: active`.
- **Entry (file plan):** execute the plan as a **single slice** — the full loop on the
  plan's `Goal`/`Done`/acceptance criteria, no tickets. Check `Context` is still
  accurate; set the plan `status: active`.
- **Pipeline (per the `dev-flow` skill, end to end):**
  1. **Research** — understand from facts (logs, traces, code); reproduce before fixing.
  2. **Goal** — take from the ticket's `What to build` + acceptance criteria (or the plan's `Goal`/`Done` for a file plan).
  3. **Isolate** — work in a dedicated `git worktree`.
  4. **Implement** — code to the ticket's acceptance criteria.
  5. **Tests** — write/adjust unit + E2E.
  6. **Independent review** — run an independent model (e.g. Codex CLI, read-only) over
     the diff.
  7. **Dev-tests** — MR + commits into `dev`; run the full suite. Red → fix, don't merge.
  8. **Prod-tests** — E2E/smoke against the real prod contour.
  9. **Ship** — merge `dev → main` and deploy (build-before-stop + healthcheck-poll).
     Mark the ticket (or the file plan) `status: archived` once merged.
- **Stop-points (from the plan contract's `Constraints`):** `stop-before-commit`
  (pause with uncommitted diff after review), `stop-after-mr` (pause after MR),
  `no-deploy` (skip deploy). A stop-point is a hard pause — the agent reports and waits,
  never resumes on its own.
- **Sequential discipline:** one ticket (or one file plan) per `/ship` run. After a
  ticket is archived, the operator launches `/ship` again for the next. Never batch
  multiple tickets.
- **Gates:** tests + independent review are not skippable.
- **Drives:** `dev-flow` skill.
