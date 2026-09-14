---
node_type: runbook
title: Deploy OntoShip into a project
service: _platform
status: active
updated: 2026-09-14
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
  `.omp/commands/`, `.omp/rules/` from the project root, and plugin-provided skills,
  commands and rules).

## Step 1. Install

**Plugin channel (standard).** The package is published from `ntin60775/ontoship-omp` as
plugin `ontoship` of the `sot-omp-marketplace` catalog; the catalog pins a tag, and the
plugin lands in `<project>/.omp/plugins/node_modules/ontoship` (a symlink into the versioned
cache `~/.omp/plugins/cache/plugins/…`). The delivery decision is recorded in the catalog
repo — `sot-omp-marketplace/docs/decisions/plugin-delivery.md`; it is not duplicated here.

```bash
omp plugin install ontoship@sot-omp-marketplace    # into this project
omp plugin upgrade ontoship@sot-omp-marketplace    # pick up a newer pinned tag
```

**Expected:** `<project>/.omp/plugins/node_modules/ontoship/` has `commands/`, `rules/`,
`skills/`, `scripts/`; commands resolve with the plugin prefix (`/ontoship:init`,
`/ontoship:kb`, `/ontoship:ship`, …); rules are always-on.

**Local-copy channel (development, air-gapped).** Before the plugin channel the package was
copied by hand; this stays valid when you work on the package itself or have no network.

```bash
cp -r <path-to-ontoship-omp>/.omp <your-repo>/
cp <path-to-ontoship-omp>/AGENTS.md <your-repo>/
```

**Expected:** `<your-repo>/` has `.omp/{skills,commands,rules,scripts}` and `AGENTS.md`;
commands resolve by their short names (`/init`, `/kb`, `/kb-map`, `/doc`, `/onto-doc`,
`/grill`, `/grilling`, `/architecture`, `/code-review`, `/to-tickets`, `/handoff`,
`/prototype`, `/ship`); the always-on rules are `kb-first`, `kb-source-of-truth`,
`ship-gate`, `acceptance-rounds`.

> **Optional:** the dev-flow review gate prefers a dedicated `reviewer` model role —
> add `modelRoles.reviewer: <provider/model>` to `~/.omp/agent/config.yml` (or
> `<repo>/.omp/config.yml`); without it the gate falls back to `@slow`.

> In either channel the plugin/copy delivers **only** `.omp/`. `AGENTS.md` and `docs/` belong
> to the project: an upgrade never touches them, and it never creates them either — that is
> the next step. Installing the plugin over an existing flat copy means removing the copy
> first (the native provider has priority 100 and would shadow the plugin's 90).

## Step 2. Initialize the entry point

A fresh project has no `AGENTS.md`, and `deploy-check` treats its absence as a critical
failure — so the entry point comes first.

```
/ontoship:init          # with a local copy: /init
```

It creates or updates the **managed block** in `AGENTS.md` (between `<!-- BEGIN ontoship -->`
and `<!-- END ontoship -->`), adds the three `.gitignore` lines the rules require, and points
at the next step. It is idempotent: a second run changes nothing.

**Expected:** `AGENTS.md` exists and contains both markers; `.gitignore` has `.gitmark/`,
`*-map.html`, `.scratch/`. Edits *inside* the block are not preserved (project edits belong
outside the markers) — if the block had to be updated, the command says so.

## Step 3. Bootstrap the KB

`AGENTS.md` links to `docs/`, which a fresh project doesn't have yet:

- **New project** — run `/ontoship:onto-doc`: it surveys the codebase, fans out `kb-curate`
  curator agents per area, and builds the whole KB: `docs/README.md` master index,
  per-service READMEs, reference specs, decisions — then lints and indexes it.
- **Existing KB** — keep your `docs/` as-is; grow it with `/ontoship:doc` (never create a
  duplicate — the tool searches first).

**Expected:** `docs/README.md` exists; the links in `AGENTS.md` → «Start here» resolve
(`docs/README.md`, `docs/ontology.md`, `docs/reference/*`).

> **Template tweaks are automatic.** The block links to `docs/README.md`, which `/onto-doc`
> creates; if a project adopts the ontology too, `/onto-doc`'s lint gate (step 5 of the
> command) flags broken links (I4) and fixes them — either creating the docs or trimming the
> links. The bootstrap is done when lint is clean.

## Step 4. Build the index and smoke-test

These commands are for a **human shell**, so they use the real path to the engine — a
`skill://` URI resolves only inside the agent's shell, not in your terminal:

```bash
# plugin install:
ENGINE=.omp/plugins/node_modules/ontoship/skills/kb-search/gitmark.py
# local copy:
# ENGINE=.omp/skills/kb-search/gitmark.py

python3 "$ENGINE" index
python3 "$ENGINE" search "<your domain>" -k 3
```

**Expected:** `index` prints the file/chunk/link counts and exits 0; `search` returns
≥ 1 hit from your own docs (not «Индекс не найден»).

## Step 5. Ignore derived and ephemeral artifacts

Add to `.gitignore` (step 2 already did it if you ran `/init`):

```gitignore
.gitmark/
*-map.html
.scratch/
```

**Expected:** `git status` stays clean after `index`/`map` — derived artifacts
(`.gitmark/index.db`, `docs-map.html`) are regenerated from md, never committed; and
session-ephemeral artifacts (handoff docs, code-review reports under `.scratch/`) never
enter the KB.

## Step 6. Verify the whole install

The package ships the check script; in a plugin install it lives inside the plugin, in a
local copy inside `.omp/scripts/`:

```bash
bash .omp/plugins/node_modules/ontoship/scripts/deploy-check.sh   # plugin install
# bash .omp/scripts/deploy-check.sh                               # local copy
```

**Expected:** exit code `0` (all good) or `2` (warnings only: trigram missing, KB not
bootstrapped, a `.gitignore` line missing, or no smoke hits for the word «OntoShip» —
a project KB may simply not contain it). Exit `1` means a broken deployment — fix the
reported `[FAIL]` items first.

The script resolves the package root from its own location, so the same file works for
both channels and for a `git worktree`. Three of its checks are worth knowing:

- it fails if the **payload still references the dead flat engine path**
  (`.omp/skills/kb-search/gitmark.py`) — that path does not exist in a plugin install;
- it runs `gitmark index` and a JSON smoke-search in the **project** root, so the index
  belongs to the project, not to the package;
- it reports a missing `AGENTS.md` as a critical failure — that is what step 2 fixes.

## From scratch — one pass

A fresh project, in order, with the expected result of each step:

| # | Command | Expected |
|---|---|---|
| 1 | `omp plugin install ontoship@sot-omp-marketplace` | plugin in `.omp/plugins/node_modules/ontoship`; commands resolve with the prefix |
| 2 | `/ontoship:init` | `AGENTS.md` with both markers; `.gitignore` has the three lines |
| 3 | `/ontoship:onto-doc` | `docs/README.md` + per-area docs; `gitmark lint` clean |
| 4 | `bash .omp/plugins/node_modules/ontoship/scripts/deploy-check.sh` | `exit 0` |

Re-running step 2 is a no-op; re-running step 4 after any doc change keeps the index fresh.
