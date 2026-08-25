---
node_type: decision
title: Ticket-driven ship — план-папка + тикеты, 1 тикет = 1 /ship
service: _platform
status: active
updated: 2026-08-25
links:
  documents: [../../.omp/commands/ship.md, ../../.omp/skills/dev-flow/SKILL.md, ../../.omp/skills/mp-grill-with-docs/SKILL.md, ../../.omp/skills/mp-to-tickets/SKILL.md, ../../.omp/skills/domain-modeling/SKILL.md]
  depends_on: [../ontology.md]
  supersedes: [../plans/contract-driven-ship.md]
---

# Решение: ticket-driven ship

## Goal

Заменить монолитный ship-контракт (один большой план → один `/ship`) на **план-папку с
тикетами**: `/ship` исполняет **один тикет**, строго последовательно. Эффективный
контекст агента конечен — монолитный контракт заставляет держать всю фичу в одном
контекстном окне; tracer-bullet тикеты, каждый «под одно свежее контекстное окно» и
верифицируемый сам по себе, — правильная единица работы.

## Done

- `mp-grill-with-docs` (grilling + domain-modeling) пишет **контракт плана** файлом
  `docs/plans/<slug>.md` (`node_type: plan`) и НЕ запускает ship.
- `mp-to-tickets` принимает файл-план, **промоутит его в папку**
  (`git mv docs/plans/<slug>.md docs/plans/<slug>/README.md`, ссылки переписаны) и
  разлагает план на **тикеты** `docs/plans/<slug>/NN-<ticket>.md` (`node_type: ticket`)
  с blocking edges. Папку создаёт только этот шаг.
- `/ship <folder>` берёт **первый не закрытый тикет по порядку** (`NN`,
  `status != archived`); `/ship <file-plan>` исполняет план как **единый срез**;
  1 тикет (или 1 файл-план) = 1 `/ship`, строго последовательно.
- `domain-modeling` — отдельный model-invoked навык: глоссарий (`CONTEXT.md`) + ADR
  (`docs/decisions/`) в процессе дизайна.
- `mp-grill-me` удалён из пакета (stateless grill — глобальный навык, вне репо).
- `mp-handoff`, `mp-prototype` оформлены как команды (`/handoff`, `/prototype`).
- Онтология: новый `node_type: ticket`; `gitmark.py` `NODE_TYPES`/`LOAD_BEARING` += `ticket`.

## Scope

Изменения только в пакете OntoShip (`.omp/` + docs):

- `docs/ontology.md` / `kb-curate` — тип `ticket`, форма плана (файл → папка), статусная машина тикетов.
- `.omp/commands/ship.md` + `.omp/skills/dev-flow/SKILL.md` — вход по тикету, проверка
  блокеров, архивирование тикета, последовательность.
- `.omp/skills/mp-grill-with-docs`, `mp-to-tickets`, `domain-modeling` — новые навыки.
- `.omp/commands/grilling.md` (→ `mp-grill-with-docs`), `to-tickets.md`, `handoff.md`,
  `prototype.md` — команды.
- `.omp/rules/ship-gate.md` — обновлён под тикеты.
- `mp-grill-me` удалён; кросс-ссылки перенаправлены.

## Constraints

- Контракт плана пишет только `mp-grill-with-docs` (файлом); тикеты — только `mp-to-tickets`.
- Ship никогда не запускается агентом сам — только ручная команда, один тикет (или один файл-план) за раз.
- `mp-handoff` — мост между сессиями (`.scratch/`), не источник знаний в KB.
- `mp-prototype` — данные для решения, не принимает решение.
- Тикеты живут в KB (`docs/plans/<slug>/`), а не в `.scratch/` — «KB — носитель»;
  эфемерность закрывается архивированием папки целиком.

## Context

Дизайн согласован в диалоге (2026-08-25):

- **Два цикла.** Познание: `grilling + domain-modeling ↔ handoff ↔ prototype` → решение →
  контракт плана. Исполнение: `/ship` по тикету (или файлу-плану) → гейты → стоп-точки → мерж.
- **Граница без автоматизации.** Между фазами нет авто-моста; ship вызывается только
  оператором. Ручной запуск = подтверждение тикета.
- **Роли навыков.** `mp-grill-with-docs` — единственный пишет родительский контракт.
  `mp-to-tickets` — единственный пишет тикеты. `mp-diagnose` — root cause + рекомендация.
  `mp-prototype` и `mp-handoff` — фаза познания, в `docs/` не пишут (кроме побочных
  `decision`/`gotcha`).
- **Жизненный цикл.** План: `draft` → `active` → `archived` (исполнен как единый срез,
  или все тикеты done). Тикет: `draft` → `active` → `archived` (shipped). «Первый не
  закрытый» = первый по `NN` с `status != archived`.
- **Почему grill-with-docs, а не grill-me.** Ценность пакета — KB как носитель знаний.
  Чистый grill-me выдаёт план и выбрасывает доменный язык; grill-with-docs (grilling +
  domain-modeling) кормит `CONTEXT.md` и `docs/decisions/`, замыкая цикл обратно в KB.
- **Технический нюанс.** omp native provider выигрывает коллизии имён — навыки пакета
  под `mp-*`, чтобы не затеняться глобальными `diagnose`/`prototype`/`handoff`/`grill-me`.
- **Собачий корм.** Изменения самого пакета идут через сам `/ship`.

## Поправка (2026-08-25): plan-file-first

План рождается **файлом** `docs/plans/<slug>.md`, а не папкой. Папка
`docs/plans/<slug>/` (контракт → `README.md` + тикеты) создаётся только `mp-to-tickets`
— `git mv` файла в `README.md` + переписывание ссылок (исходящие: глубина +1,
входящие: из других docs). `/ship` по файлу-плану исполняет его как единый срез
(один worktree, один MR, `status: archived` после мержа).

Причина: для мелкой задачи папка + тикеты избыточны — легитимным стал путь
«файл-план → один `/ship`», без тикетов и без ad-hoc. Детали — в
[`docs/plans/plan-file-first.md`](../plans/plan-file-first.md). Решение
tickets-модели (1 тикет = 1 `/ship`, строго последовательно) **не меняется**;
поправка уточняет форму плана и вход `/ship`.
