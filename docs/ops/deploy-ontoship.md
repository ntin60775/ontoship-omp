---
node_type: runbook
title: Deploy OntoShip into a project
service: _platform
status: active
updated: 2026-08-15
tags: [runbook, deploy, install, omp-package, gitmark]
links:
  documents: [../../AGENTS.md, ../../.omp/skills/kb-search/gitmark.py, ../../.omp/scripts/deploy-check.sh]
  relates_to: [../../README.md]
---

# Deploy OntoShip into a project

Install the OntoShip **omp package** (GitMark KB + dev-flow) into a target repository.
Every step lists its **expected result** — if it doesn't hold, stop and fix before
continuing.

## Prerequisites

- `python3` (≥ 3.7) with SQLite **FTS5** (trigram tokenizer for SQLite ≥ 3.34 is
  optional — detected automatically, degrades gracefully).
- omp agent with the native provider (reads `AGENTS.md`, `.omp/skills/`,
  `.omp/commands/`, `.omp/rules/` from the project root).

## Steps

### 1. Copy the package

```bash
cp -r <path-to-ontoship-omp>/.omp <your-repo>/
cp <path-to-ontoship-omp>/AGENTS.md <your-repo>/
```

**Expected:** `<your-repo>/` has `.omp/skills/`, `.omp/commands/`, `.omp/rules/` and
`AGENTS.md`; omp picks up the slash commands (`/kb`, `/kb-map`, `/doc`, `/onto-doc`,
`/grilling`, `/architecture`, `/code-review`, `/to-tickets`, `/handoff`, `/prototype`, `/ship`) and the always-on rules
(`kb-first`, `kb-source-of-truth`, `ship-gate`); the `ship-1c` rule ships opt-in (enable
it only in a 1C project).

### 2. Bootstrap the KB

`AGENTS.md` links to `docs/`, which a fresh project doesn't have yet:

- **New project** — run `/onto-doc`. It surveys the codebase, fans out `kb-curate`
  curator agents per area, and builds the whole KB: `docs/README.md` master index,
  per-service READMEs, reference specs, decisions — then lints and indexes it.
- **Existing KB** — keep your `docs/` as-is; grow it with `/doc` (never create a
  duplicate — the tool searches first).

**Expected:** `docs/README.md` exists; the links in `AGENTS.md` → «Start here» resolve
(`docs/README.md`, `docs/ontology.md`, `docs/reference/*`).

> **Template tweaks are automatic.** `AGENTS.md` links to specific KB files
> (`docs/ontology.md`, `docs/reference/architecture.md`, `docs/reference/commands.md`)
> that a fresh project doesn't have yet. `/onto-doc`'s lint gate (step 5) flags these as
> broken links (I4) and fixes them — either creating the docs (when the ontology is
> adopted) or trimming the links in `AGENTS.md`. No manual tweaking step; the bootstrap
> is done when lint is clean.

### 3. Build the index and smoke-test

```bash
python3 .omp/skills/kb-search/gitmark.py index
python3 .omp/skills/kb-search/gitmark.py search "<your domain>" -k 3
```

**Expected:** `index` prints the file/chunk/link counts and exits 0; `search` returns
≥ 1 hit from your own docs (not «Index not found»).

### 4. Ignore derived and ephemeral artifacts

Add to `.gitignore`:

```gitignore
.gitmark/
*-map.html
.scratch/
```

**Expected:** `git status` stays clean after `index`/`map` — derived artifacts
(`.gitmark/index.db`, `docs-map.html`) are regenerated from md, never committed; and
session-ephemeral artifacts (handoff docs, code-review reports under `.scratch/`) never
enter the KB.

## Verify the whole install

```bash
python3 .omp/skills/kb-search/gitmark.py stat
git status --short
```

**Expected:** `stat` shows a non-empty index; `git status` shows no `.gitmark/` or
`*-map.html` entries.

If the package ships the check script (`.omp/scripts/deploy-check.sh`), run it instead
of the manual checks — same coverage, one command:

```bash
bash .omp/scripts/deploy-check.sh
```

**Expected:** exit code `0` (all good) or `2` (warnings only: trigram missing, KB not
bootstrapped, `.gitmark/` not ignored). Exit `1` means a broken deployment — fix the
reported `[FAIL]` items first.
