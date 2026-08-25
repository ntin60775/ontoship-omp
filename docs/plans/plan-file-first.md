---
node_type: plan
title: План-файл по умолчанию — папка и тикеты только после /to-tickets
service: _platform
status: archived
updated: 2026-08-25
links:
  depends_on: [../ontology.md, ../decisions/ticket-driven-ship.md]
  documents: [../../.omp/skills/mp-grill-with-docs/SKILL.md, ../../.omp/skills/mp-to-tickets/SKILL.md, ../../.omp/commands/ship.md]
---

# Контракт: план-файл по умолчанию

## Goal

Одиночный файл `docs/plans/<slug>.md` — форма плана по умолчанию: гриллинг
заканчивается файлом, а не папкой. Папка с тикетами появляется только когда
оператор запускает `/to-tickets`. `/ship` умеет исполнить файл-план как единый
срез, чтобы мелкая задача не требовала тикетов.

## Done

- `mp-grill-with-docs` пишет `docs/plans/<slug>.md` (`node_type: plan`,
  `status: draft`) — без папки, без секции `Tickets`.
- `mp-to-tickets` принимает одиночный файл-план: `git mv docs/plans/<slug>.md
  docs/plans/<slug>/README.md`, переписывает исходящие ссылки файла (глубина +1)
  и входящие ссылки из других docs, затем пишет тикеты и секцию `Tickets`.
- `/ship docs/plans/<slug>.md` — исполняет план как единый срез: один worktree,
  один MR, `status: archived` после мержа.
- `/ship docs/plans/<slug>` (без расширения) — резолвится в файл или папку.
- «Самый свежий план» (пустой аргумент у `/ship` и `/to-tickets`) учитывает и
  файлы, и папки.
- KB синхронизирован: `kb-curate`, `docs/plans/README.md`, `docs/ontology.md`,
  `docs/reference/commands.md`, `docs/reference/architecture.md`,
  `docs/decisions/ticket-driven-ship.md` (поправка, не замена решения).
- `gitmark.py lint` чистый, `index` пересобран.

## Scope

Изменения только в пакете OntoShip (`.omp/` + `docs/`):

- `.omp/skills/mp-grill-with-docs/SKILL.md` — писать файл, не папку.
- `.omp/skills/mp-to-tickets/SKILL.md` — вход по одиночному файлу + миграция в папку.
- `.omp/commands/ship.md` + `.omp/skills/dev-flow/SKILL.md` — вход по файлу-плану,
  исполнение как единого среза.
- `.omp/skills/kb-curate/SKILL.md` — «Writing a plan contract»: файл сначала,
  папка после `/to-tickets`.
- `docs/plans/README.md`, `docs/ontology.md`, `docs/reference/commands.md`,
  `docs/reference/architecture.md` — синхронизация.
- `docs/decisions/ticket-driven-ship.md` — поправка (уточнение модели).
- `gitmark.py` — только если потребует lint (не ожидается: одиночные
  файл-планы уже поддерживаются).

## Constraints

- Одиночный файл-план НЕ имеет секции `Tickets`; тикеты живут только в папечной форме.
- Миграция в папку — `git mv` (сохранение истории) + переписывание ссылок
  (исходящие: глубина +1; входящие: из других docs).
- Файл сохраняет осмысленное имя `<slug>.md`; папечная форма переименовывает его
  в `README.md` (индекс папки).
- `gitmark.py` не трогать, если lint не потребует.

## Context

Дизайн согласован с оператором (2026-08-25):

- **Проблема.** Текущая модель всегда создаёт папку + родительский контракт
  (`mp-grill-with-docs`), и `/ship <plan>` предполагает наличие тикетов. Для
  мелкой задачи нет легитимного пути: либо папка + тикеты, либо ad-hoc без
  бумажного следа.
- **Решение.** План рождается файлом `docs/plans/<slug>.md`. Единственный шаг,
  создающий папку, — `/to-tickets`: `git mv <slug>.md <slug>/README.md` +
  переписывание ссылок + файлы тикетов. `/ship` по файлу-плану = единый срез.
- **Прецедент.** `docs/plans/contract-driven-ship.md` — одиночный файл-план уже
  существует в KB; форма поддерживается.
- **Собачий корм.** Изменение помещается в один контекст-окно — исполняется
  одним `/ship`-прогоном без тикетов, то есть самим новым механизмом.
