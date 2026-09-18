---
node_type: index
title: Decisions
service: _platform
status: active
updated: 2026-09-18
links:
  part_of: [../README.md]
---

# Decisions

Architectural / product decisions (ADRs) — recorded so conclusions are enforced, not
re-argued.

| Decision | What it settles |
|---|---|
| [ontoship-positioning.md](ontoship-positioning.md) | What OntoShip is for: team experience-transfer for AI-agent dev (not OSS-for-stars, not search engine) |
| [omp-only-package.md](omp-only-package.md) | OntoShip is an omp-only package — Claude Code specifics (`.claude-plugin/`, `CLAUDE.md`, marketplace) removed; `.omp/` + `AGENTS.md` native |
| [ticket-driven-ship.md](ticket-driven-ship.md) | Plan = folder with tickets; `/ship` runs one ticket at a time, strictly sequential (supersedes the contract-driven model) |
| [agent-ship-authorization.md](agent-ship-authorization.md) | Агентский `/ship` разрешён только в явно авторизованном goal-ране; правило `ship-gate` для потребителей не меняется |
| [link-resolution.md](link-resolution.md) | Резолв ссылок: две моды — граф по замыслу (мягко), линт по адресуемости (строго); I4 проверяет тело и frontmatter против ФС |
