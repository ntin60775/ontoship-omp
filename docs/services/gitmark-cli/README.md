---
node_type: service
title: gitmark CLI — KB search/index engine
service: gitmark-cli
status: active
updated: 2026-06-16
tags: [fts5, search, sqlite, ontology, cli]
links:
  documents: [../../../.omp/skills/kb-search/gitmark.py, ../../../.omp/skills/kb-search/SKILL.md]
  relates_to: [../../ontology.md]
---

# gitmark CLI — KB search/index engine

`gitmark.py` is the search/index engine behind OntoShip. It treats the repo's markdown
(`docs/`, README files, any `*.md`) as a **md + git** knowledge base: markdown is the
source of truth, and everything derived — the search index, HTML map, graph — is
regenerated from it. The whole thing is pure Python stdlib (no third-party deps required;
`markdown` is an optional enhancement for the `map` renderer) and runs fully offline.

It enforces and operates over the OntoShip ontology (object types, properties, typed
links). For the model itself — `node_type`, frontmatter, link types, invariants I1–I6 —
see [ontology.md](../../ontology.md); this doc describes the engine, not the model.

Script: `.omp/skills/kb-search/gitmark.py`. The usage skill is
`.omp/skills/kb-search/SKILL.md`.

## Subcommands

Invoked as `python3 gitmark.py <cmd>`. A global `--root <path>` overrides repo
auto-detection (see below); it precedes the subcommand. Defined in `main()`
(gitmark.py:725).

| cmd | what it does |
|---|---|
| `index [--force]` | (Re)build `.gitmark/index.db` — scans all `*.md`, chunks them, fills FTS tables + the `files`/`links`/`meta` tables. |
| `search "<q>" [-k N] [--json]` | Search the index: bm25 ∪ trigram ∪ fuzzy. Prints `path:line › heading [via]` + snippet; `-k` caps results (default 8); `--json` for machine output. |
| `map [-o OUT]` | Emit a single self-contained HTML file: collapsible tree + rendered markdown + radial link graph. Default out is `docs/docs-map.html`. |
| `serve [-p PORT]` | Local `http.server` over `docs/` (falls back to repo root) to view the map. Default port 8799. |
| `stat` | Index statistics: files, folders/areas, chunks, links, bytes, trigram on/off. |
| `lint [paths…] [--strict]` | Check ontology invariants I1–I7 (frontmatter/types/vocab/links/README/orphans/registry). `--strict` exits 1 on any ERR. |
| `inventory [--check]` | Regenerate the two generated summary tables (commands + skills) between the `<!-- BEGIN/END inventory:* -->` markers in `docs/reference/commands.md`, from the frontmatter of `.omp/commands/*.md` and `.omp/skills/*/SKILL.md`. Idempotent. `--check` reports any desync and exits 1 (the same check `lint` reports as I7). |
| `version` | Print `gitmark <VERSION>` (currently `0.1.0`, gitmark.py:33). |

Note: `index` accepts `--force` but the flag is currently inert — each `index` run already
deletes and rebuilds the tables unconditionally (gitmark.py:190-193).

## Root auto-detection

When `--root` is not given, the CLI walks up from the current working directory looking for
a `.git` directory and uses the first ancestor that has one; if none is found it falls back
to cwd. See `repo_root()` (gitmark.py:48-53). So `gitmark` can be run from anywhere inside
the repo and will resolve to the repo root.

A fixed set of directories is excluded from scanning regardless of root: `.git`,
`node_modules`, `.next`, `dist`, `build`, `__pycache__`, `.pytest_cache`, `_vendor`,
`.venv`, `venv`, `vendor`, and `.gitmark` itself (`EXCLUDE_DIRS`, gitmark.py:35-39).
On top of that, `.gitignore`d paths are excluded — a hand-written subset parser
(`parse_gitignore`, gitmark.py:56-72: folder names with a trailing `/`, exact names and
`*`-patterns without `/`; no negations, no `**`) so ephemera (`.scratch/`, `.artifacts/`,
anything gitignored) never enters the index, search, lint, or map. File discovery is
`iter_md()` (gitmark.py:82-92).

## Where the index lives

`.gitmark/index.db` under the repo root (`DB_REL`, gitmark.py:40). It is a derived cache and
should be gitignored — never edit it directly; edit the markdown and reindex. `search`/`stat`
require it to exist and tell you to run `gitmark index` if it's missing.

## How indexing works

`cmd_index()` (gitmark.py:171-230):

1. Read every non-excluded `*.md` under root into memory (used both for chunking and for
   link resolution against the set of known files).
2. For each file: derive a `title` (first `# H1`, else filename — `title_of`,
   gitmark.py:109-113) and an `area` (`area_of`, gitmark.py:95-106 — `docs/services/<svc>`
   gets its own group, otherwise `docs/<sub>`, `services/<svc>`, etc.).
3. **Chunking** — `chunk_md()` (gitmark.py:116-130) splits each file at markdown headings
   (`^#{1,6} …`). Each chunk is `(line_start, heading, body)`; this is the unit that gets
   indexed and the granularity at which search results point (`path:line`).
4. Each chunk is inserted into the `fts` table and (if available) the `tri` table.
5. **Links** — `LINK_RE` finds markdown links `[text](href)` (ignoring image links), and
   `resolve_link()` (gitmark.py:137-158) resolves each `href` to a known `.md` file. It
   strips `#anchors`, skips `http`/`mailto`, NFC-normalizes (so non-ASCII paths match),
   resolves relative/`../` paths via `posixpath.normpath`, and falls back to a unique
   basename match. Resolved `(src, dst)` pairs (deduped, excluding self-links) go into the
   `links` table. This populates the doc→doc edges the graph and the linter's orphan check
   use.
6. `meta` records whether trigram is available and the engine version.

**Trigram availability** is probed at runtime by trying to create an fts5 table with
`tokenize='trigram'` (`_has_trigram`, gitmark.py:162-168). If the SQLite build lacks the
trigram tokenizer, the `tri` table is skipped and search degrades to bm25-only. FTS5 itself
is mandatory — if SQLite has no FTS5 at all, `index` errors out with exit code 2
(gitmark.py:179-181).

## SQLite schema

Created in `cmd_index()`:

- `fts` — FTS5 virtual table, `tokenize='unicode61 remove_diacritics 2'`. Columns:
  `path UNINDEXED, heading, lineno UNINDEXED, body`. One row per chunk; the bm25 ranking
  table.
- `tri` — FTS5 virtual table, `tokenize='trigram'` (only if the trigram tokenizer exists).
  Same columns. Powers substring/fuzzy matching.
- `files(path TEXT PRIMARY KEY, title TEXT, area TEXT, size INT, chunks INT)` — one row per
  file (size is UTF-8 byte length).
- `links(src TEXT, dst TEXT)` — resolved doc→doc edges.
- `meta(k TEXT PRIMARY KEY, v TEXT)` — key/value: `trigram` (`"1"`/`"0"`) and `version`.

## How search ranks

`cmd_search()` (gitmark.py:259-324) merges up to three passes into one result set keyed by
`(path, lineno)`; earlier (stronger) passes win on collision, and results are sorted by the
combined score descending, then truncated to `k`.

1. **bm25 (exact terms)** — query words ≥2 chars become a prefix `OR` match
   (`"term"* OR …`, `_fts_match_query`, gitmark.py:234-236) against `fts`. Score is
   `-bm25(fts)` (full weight). `via: "bm25"`.
2. **trigram phrase (substring)** — the raw query as one quoted phrase against `tri`;
   matches exact substrings. Score weighted ×0.6. `via: "trigram"`. Only runs when the query
   is ≥3 chars and trigram is available.
3. **fuzzy (n-gram)** — handles typos, morphology, and Cyrillic. `_fuzzy_phrases()`
   (gitmark.py:239-256) breaks query words (≥4 chars) into overlapping 4-char windows;
   these are OR-matched against `tri`. A chunk is accepted only if its body contains at
   least `need` distinct windows (≈ceil(20% of windows), min 1 — gitmark.py:303), which
   filters chunks that merely share one common gram. Score weighted ×0.3. `via: "fuzzy"`.

Each pass returns a snippet via FTS5 `snippet(...,'»','«','…',14)` so the matched terms are
delimited in the output.

## Linting (ontology invariants)

`cmd_lint()` (gitmark.py:393-480) checks I1–I7 over `docs/**` using a stdlib mini
frontmatter parser (`parse_frontmatter`, gitmark.py:363-390 — no PyYAML). The controlled
vocabularies (`NODE_TYPES`, `SERVICES`, `STATUSES`, `LOAD_BEARING`, `LINK_KEYS`,
gitmark.py:344-351) are the lint source of truth and must stay in sync with
[ontology.md](../../ontology.md). Broken-link detection (I4) strips fenced/inline code first
(`strip_code`, gitmark.py:358-360) so example links in code blocks aren't flagged. ERR-level
issues: I1 (missing frontmatter/`node_type` on a load-bearing path), I2 (`node_type` out of
vocab), I4 (broken link), I7 (command registry desync — the same check as
`gitmark inventory --check`). WARN-level: I2 service/status out of vocab, I3 (orphan — a
load-bearing doc with no in/out links and no `links:` block), I5 (a `docs/` folder with no
`README.md`), I6 (a `supersedes` target that isn't `deprecated`/`archived`).

## The inventory (generated command/skill registry)

`cmd_inventory()` (gitmark.py:584-606) regenerates the two summary tables in
`docs/reference/commands.md` between the `<!-- BEGIN/END inventory:commands -->` and
`<!-- BEGIN/END inventory:skills -->` markers — the commands table from the frontmatter
(`description`/`args`/`drives`) of `.omp/commands/*.md` (`_scan_commands`,
gitmark.py:494-505), the skills table from `name`/`description` of
`.omp/skills/*/SKILL.md` (`_scan_skills`, gitmark.py:508-518). Writing happens **only**
between the markers; the hand-written `## /cmd` sections are never touched. Idempotent:
a second run changes nothing. `inventory_issues()` (gitmark.py:549-581) is the single
desync detector — missing `args:`/`drives:` frontmatter, a table out of sync, or a
`## /cmd` section without its file (and vice versa) — shared by `--check` (exit 1) and
`lint` (as I7, ERR level).

## The map (HTML overview + graph)

`cmd_map()` (gitmark.py:610-705) produces one standalone HTML file (`_MAP_HTML` template,
gitmark.py:802+) with the data inlined as JSON: a collapsible per-area file tree, the
rendered markdown of each doc, and a radial link graph. The graph is laid out by BFS from an
entry node (`AGENTS.md` → `README.md` → first file), with ring = distance-from-entry; it
supports drag, wheel-zoom, and clicking a node to open the doc. If the optional `markdown`
package is installed, docs render to HTML; otherwise they show as raw `<pre>` text (the CLI
prints a hint to `pip install markdown`).

## Usage examples

```bash
G="python3 .omp/skills/kb-search/gitmark.py"

$G index                       # build .gitmark/index.db
$G search "trigram ranking"    # bm25 + trigram + fuzzy; prints path:line + snippet
$G search "frontmater" -k 5    # typo-tolerant via fuzzy n-grams
$G search "ontology" --json    # machine-readable results
$G stat                        # files/folders/chunks/links/bytes · trigram on|off
$G lint                        # check ontology invariants over docs/ (I1–I7)
$G map -o out.html             # self-contained HTML overview + graph
$G inventory                   # regenerate the summary tables in docs/reference/commands.md
$G inventory --check           # exit 1 on any registry desync (I7)
$G serve -p 8799               # serve the map at http://127.0.0.1:8799/docs-map.html
```
