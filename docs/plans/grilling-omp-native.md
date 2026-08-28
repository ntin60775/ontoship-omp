---
node_type: plan
title: omp-нативный язык в примитиве grilling — read-only scout для поиска фактов
service: _platform
status: archived
updated: 2026-08-28
links:
  depends_on: [../decisions/omp-only-package.md, ../decisions/ticket-driven-ship.md]
  documents: [../../.omp/skills/grilling/SKILL.md, ../../.omp/commands/grill.md, ../reference/commands.md, ../services/grilling/README.md]
  relates_to: [../services/dev-flow/README.md]
---

# Контракт: именование нативных механизмов omp в гриллинг-контуре

## Goal

Примитив `grilling` формулирует поиск фактов платформо-нейтрально («dispatch a
sub-agent»), тогда как `dev-flow` уже мигрирован на нативный язык omp
(«independent omp sub-agent», `@reviewer`/`@slow`). Гриллинг-контур эту миграцию
не получил. В omp поиск фактов — это **read-only `scout`** (быстрая модель,
только чтение): ровно то, что описывает скилл, но без имени агента инструкция
теряет точность, и агент может породить полновесный `task` вместо лёгкого скаута.

## Done

- В `grilling/SKILL.md` поиск фактов явно диспетчеризуется на read-only **scout**
  sub-agent (omp).
- Три зеркальные формулировки синхронизированы: `commands/grill.md`, секция
  `## /grilling` в `docs/reference/commands.md`, `docs/services/grilling/README.md`.
- Дисциплина раундов и frontier не переписывается — меняется только именование
  механизма поиска фактов.
- `gitmark.py lint` чистый, `index` пересобран.

## Scope

- `.omp/skills/grilling/SKILL.md` — «dispatch a sub-agent» → «dispatch a
  read-only scout sub-agent».
- `.omp/commands/grill.md` — «the agent finds facts itself (sub-agents)» →
  «…(read-only scout sub-agents)».
- `docs/reference/commands.md` — та же формулировка в секции `## /grilling`.
- `docs/services/grilling/README.md` — уточнение в прозе о движке.
- Индексная строка плана в `docs/plans/README.md`.

Вне scope: гибридное использование `ask` в раундах (оператор: «не влазит
нормально — не трогать»); `command-inventory` (отдельный план, `draft`);
переименование `/grilling`; изменения `gitmark.py`.

## Constraints

- Тела скиллов не дублируют дисциплину раундов текстом — правка точечная,
  только именование механизма.
- Пакет omp-only (ADR `omp-only-package.md`): именование нативных механизмов
  (`scout`) корректно и не нарушает платформо-нейтральность `gitmark.py`.
- Стоп-точек нет: срез чисто доковый. Собачий корм: исполняется онтошиповым
  механизмом — `/ship` по файлу-плану единым срезом (тикеты не нужны).

## Context

Найдено аудитом гриллинг-надстройки 2026-08-28 (внутренняя согласованность и
интеграция — чистые; единственная адаптационная находка — разнобой с `dev-flow`
после коммита `e1b00ec`). Вариант А1 согласован оператором; `ask`-гибрид (Б)
отклонён оператором.
