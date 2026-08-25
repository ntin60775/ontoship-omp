---
node_type: plan
title: Контракт-спек — входные навыки → ручной /ship
service: _platform
status: archived
updated: 2026-08-17
links:
  documents: [../../.omp/commands/ship.md, ../../.omp/skills/dev-flow/SKILL.md, ../../.omp/skills/grilling/SKILL.md]
  depends_on: [../ontology.md]
---

# Контракт: контракт-спек (входные навыки → ship)

## Goal

Разделить работу с агентом на два цикла и связать их контрактом:
фаза познания (HITL, решения руками) и фаза исполнения (`/ship`, автономно).
Единственный мост между ними — ручная команда `/ship` по контракту в KB.

## Done

- `mp-grill-me` пишет контракт `docs/plans/<slug>.md` (`node_type: plan`) и НЕ запускает ship.
- `mp-diagnose`, `mp-prototype`, `mp-handoff` существуют как навыки пакета, НЕ пишут контракт.
- `/ship` принимает путь к контракту; шаги 1–4 сжимаются в верификацию; `Constraints` задают стоп-точки.
- План проходит `draft → active → archived`; после мержа — `archived`.
- Правило `ship-gate.md`: код — только через ship, триггер — только руками.
- Правило `ship-1c.md`: для 1С-проектов `stop-before-commit` по умолчанию.

## Scope

Изменения только в пакете OntoShip (`.omp/` + docs):

- `docs/ontology.md` / `kb-curate` — описать контракт-план и статусную машину.
- `.omp/commands/ship.md` + `.omp/skills/dev-flow/SKILL.md` — приём контракта, верификация, стоп-точки, архивирование плана.
- `.omp/skills/mp-grill-me` — финальный шаг «написать контракт», без эстафеты.
- `.omp/skills/mp-diagnose`, `mp-prototype`, `mp-handoff` — новые навыки.
- `.omp/rules/ship-gate.md`, `.omp/rules/ship-1c.md` — новые правила.

## Constraints

- Контракт пишет только `mp-grill-me` (итог подтверждённого решения).
- Ship никогда не запускается агентом сам — только ручная команда.
- `mp-handoff` — мост между сессиями (`.scratch/`), не источник знаний в KB.
- `mp-prototype` — данные для решения, не принимает решение.

## Context

Дизайн согласован в диалоге (2026-08-17):

- **Два цикла.** Познание: `grill-me ↔ handoff ↔ prototype` → решение → контракт.
  Исполнение: `/ship` по контракту → гейты → стоп-точки → мерж.
- **Граница без автоматизации.** Между фазами нет авто-моста; ship вызывается только
  разработчиком. Ручной запуск = подтверждение контракта (гейт B поглощается запуском).
- **Роли навыков.** `mp-grill-me` — единственный пишет контракт. `mp-diagnose` —
  root cause + рекомендация (контракт — только если решение тут же подтверждено).
  `mp-prototype` и `mp-handoff` — фаза познания, в `docs/` не пишут (кроме побочных
  `decision`/`gotcha`).
- **Жизненный цикл плана.** `draft` (написан) → `active` (ship стартовал) →
  `archived` (после мержа).
- **1С.** `stop-before-commit`: шаги 1–8 автоматом, остановка с незакоммиченным диффом
  в worktree; по команде «продолжай» — коммит + MR + dev + prod + мерж + деплой.
- **Технический нюанс.** omp native provider выигрывает коллизии имён — новые навыки
  кладутся под `mp-*`, чтобы не затеняться глобальными `diagnose`/`prototype`/`handoff`.
- **Собачий корм.** Изменения самого пакета идут через сам `/ship`; этот файл — первый
  контракт.

## Tasks

1. Обновить `docs/ontology.md` и `kb-curate` SKILL.md: контракт-план, статусная машина.
2. Доработать `.omp/commands/ship.md` + `dev-flow` SKILL.md: вход по контракту, верификация, стоп-точки, архивирование.
3. Доработать `mp-grill-me`: финальный шаг «написать контракт» без запуска ship.
4. Создать `mp-diagnose`, `mp-prototype`, `mp-handoff` (`.omp/skills/`).
5. Создать `.omp/rules/ship-gate.md` и `.omp/rules/ship-1c.md`.
6. `gitmark.py lint` + `index` + `map`.
