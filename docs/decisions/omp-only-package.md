---
node_type: decision
title: OntoShip is an omp-only package — Claude Code specifics removed
service: _platform
status: active
updated: 2026-08-14
tags: [decision, adr, omp, packaging, platform]
links:
  relates_to: [../reference/architecture.md, ../reference/commands.md, ../../README.md, ontoship-positioning.md]
---

# Decision: OntoShip is an omp-only package

> ADR capturing the platform decision: the fork `ontoship-omp` is **fully adapted to the
> omp agent** and excludes all other platforms (Claude Code and its marketplace format).
> See also [architecture](../reference/architecture.md) and
> [commands](../reference/commands.md); it supersedes the former Claude Code packaging
> (`.claude-plugin/`, root `CLAUDE.md`), not the product positioning in
> [positioning](ontoship-positioning.md).

## Context

OntoShip started as a **Claude Code marketplace** (`.claude-plugin/marketplace.json`,
`CLAUDE.md` entry point, `commands/*.md` in Claude Code format, `${CLAUDE_PLUGIN_ROOT}`
path expansion). The fork `ontoship-omp` was created to adapt it to the **omp** agent, but
the codebase was still 100 % Claude Code-specific — nothing in the repo consumed the omp
native mechanisms (`AGENTS.md`, `.omp/skills/`, `.omp/commands/`, `.omp/rules/`).

omp reads `AGENTS.md` (not root `CLAUDE.md`), resolves skills from `.omp/skills/` and
commands from `.omp/commands/` (native provider, project-local), and does **not** support
`${CLAUDE_PLUGIN_ROOT}`. Keeping Claude Code artifacts would mean either maintaining two
formats or shipping dead weight.

## Decision

**OntoShip is an omp-only package**: a project-local `.omp/` directory (skills + commands
+ rules) plus a root `AGENTS.md` entry point. All Claude Code specifics are removed —
`.claude-plugin/`, `CLAUDE.md`, `commands/`, `${CLAUDE_PLUGIN_ROOT}`, and the "marketplace"
wording in docs. The GitMark CLI (`gitmark.py`) is platform-neutral and unchanged except
for its graph entry node (`AGENTS.md` instead of `CLAUDE.md`).

**destructive-guard** (a Claude Code `PreToolUse` hook) is **not** ported: it already lives
in its own repository, and omp has built-in safety (extensions + rules). The KB page is
marked `archived` and points to the external repo.

## Consequences

- Installing OntoShip in a project = copy `.omp/` + `AGENTS.md` (no marketplace step);
  omp's native provider picks everything up automatically.
- Commands keep their short names (`/kb`, `/ship`, …) — no plugin prefix.
- The fork diverges from upstream `vakovalskii/ontoship` (Claude Code marketplace);
  upstream CC changes will not merge cleanly. This is accepted: the repo is omp-native by
  design.
