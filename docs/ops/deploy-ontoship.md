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

## Step 1. Install — plugin channel (standard)

The package is published from `ntin60775/ontoship-omp` as plugin `ontoship` of the
`sot-omp-marketplace` catalog; the catalog pins a tag, and the plugin lands in
`<project>/.omp/plugins/node_modules/ontoship` (a symlink into the versioned cache
`~/.omp/plugins/cache/plugins/…`). The delivery decision is recorded in the catalog repo —
`sot-omp-marketplace/docs/decisions/plugin-delivery.md`; it is not duplicated here.

```bash
omp plugin install ontoship@sot-omp-marketplace    # into this project
omp plugin upgrade ontoship@sot-omp-marketplace    # pick up a newer pinned tag
```

**Expected:** `<project>/.omp/plugins/node_modules/ontoship/` has `commands/`, `rules/`,
`skills/`, `scripts/`; commands resolve with the plugin prefix (`/ontoship:kb`,
`/ontoship:onto-doc`, `/ontoship:ship`, …); rules are always-on.

> The plugin delivers **only** `.omp/`. `AGENTS.md` and `docs/` belong to the project —
> an upgrade never touches them, and it never creates them either.

### Alternative: local copy (package development, legacy)

Before the plugin channel the package was copied by hand. This stays valid when you work on
the package itself, or on an air-gapped machine.

```bash
cp -r <path-to-ontoship-omp>/.omp <your-repo>/
cp <path-to-ontoship-omp>/AGENTS.md <your-repo>/
```

**Expected:** `<your-repo>/` has `.omp/skills/`, `.omp/commands/`, `.omp/rules/`,
`.omp/scripts/` and `AGENTS.md`; omp picks up the slash commands (`/kb`, `/kb-map`, `/doc`,
`/onto-doc`, `/grill`, `/grilling`, `/architecture`, `/code-review`, `/to-tickets`,
`/handoff`, `/prototype`, `/ship`) and the always-on rules (`kb-first`,
`kb-source-of-truth`, `ship-gate`); the `ship-1c` rule ships opt-in (enable
it only in a 1C project).

> **Optional:** the dev-flow review gate prefers a dedicated `reviewer` model role —
> add `modelRoles.reviewer: <provider/model>` to `~/.omp/agent/config.yml` (or
> `<repo>/.omp/config.yml`); without it the gate falls back to `@slow`.

## Step 2. Bootstrap the KB

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

## Step 3. Build the index and smoke-test

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

## Step 4. Ignore derived and ephemeral artifacts

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
both channels and for a `git worktree`. Two of its checks are worth knowing:

- it fails if the **payload still references the dead flat engine path**
  (`.omp/skills/kb-search/gitmark.py`) — that path does not exist in a plugin install;
- it runs `gitmark index` and a JSON smoke-search in the **project** root, so the index
  belongs to the project, not to the package.
