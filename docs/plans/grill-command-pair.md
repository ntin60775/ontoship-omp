---
node_type: plan
title: Пара grilling-команд — /grill (обычный) + /grilling (с доками)
service: _platform
status: active
updated: 2026-08-28
links:
  depends_on: [../decisions/ticket-driven-ship.md, command-inventory.md, ../ontology.md]
  documents: [../../.omp/commands/grilling.md, ../../.omp/skills/grilling/SKILL.md, ../../.omp/skills/mp-grill-with-docs/SKILL.md]
  relates_to: [../reference/commands.md, ../services/grilling/README.md]
---

# Контракт: пара grilling-команд

## Goal

У обоих grilling-навыков пакета появляется пользовательский глагол. `grilling`
(примитив: раунды + frontier, ничего не пишет) сегодня доступен только через
model-invocation по триггеру — рядом живёт глобальный `grill-me` с другой дисциплиной
(«по одному вопросу») и пересекающимся триггером «grill me», и по фразе «погриль меня»
агент может увлечь не тот навык. Новая команда `/grill` явно биндит проектный
примитив; `/grilling` (→ `mp-grill-with-docs`) остаётся как есть — документированный
вариант с записью в KB.

## Done

- Файл `.omp/commands/grill.md`: frontmatter `description:` с русскими триггерами
  («погрилл», «грилл», «погриль меня») и телом-биндингом «Run the **grilling** skill
  on the topic: `$ARGUMENTS`»; `$ARGUMENTS` пуст → спросить, что гриллить. Навык НЕ
  создаётся новый — `grilling` уже существует и уже ничего не пишет.
- `/grilling` НЕ переименовывается (цена: 44 вхождения в 26 файлах, рукописных;
  генерацией не закрывается).
- `docs/decisions/ticket-driven-ship.md` дополнен поправкой 2026-08-28 («обычный
  грилл — оптический вход, durable-артефакты пишет только grill-with-docs») —
  записана на grilling-сессии, в скоуп исполнения не входит.
- `CONTEXT.md` дополнен парой терминов «Грилл» / «Грилл с доками» — записано на
  сессии; в скоуп входит только перечисление `/grill` в термине **Команда**.
- Реестр синхронизирован по чеклисту регистрации (см. Context): таблица и секция
  `## /grill` в `docs/reference/commands.md`, строки в `AGENTS.md`, `README.md`,
  `docs/README.md`, `docs/ops/deploy-ontoship.md`, `docs/services/grilling/README.md`
  (там уже заявлен обработчик «grill me» — добавить ссылку на `/grill`).
- `gitmark.py lint` чистый, `index` пересобран.

## Scope

- `.omp/commands/grill.md` — новый файл (тонкий биндинг, ~10 строк).
- `AGENTS.md` — `/grill` в строку `commands/`.
- `README.md` — строка в таблицу команд + блок `**/grill <topic>**` с примерами.
- `CONTEXT.md` — `/grill` в перечисление термина **Команда**.
- `docs/README.md` — упоминание в индексе Reference (список глаголов).
- `docs/reference/commands.md` — `links.documents` += `grill.md`; «families»-проза;
  строка сводной таблицы; секция `## /grill`.
- `docs/reference/architecture.md`, `docs/reference/README.md` — синхронизация, если
  там есть перечисления команд.
- `docs/ops/deploy-ontoship.md` — список «omp picks up the slash commands (…)».
- `docs/services/grilling/README.md` — «Two entry points» → три (`/grill`, `/grilling`,
  mp-improve-codebase-architecture).
- `docs/plans/README.md`, `docs/README.md` — индексная строка этого плана.

Вне scope: новый навык (не нужен); переименование `/grilling`; файл-синоним `/грилл`
(реестр не расщепляется, русское — в `description`); правки глобального
`~/.omp/agent/skills/grill-me` (вне репо); изменения `gitmark.py`.

## Constraints

- **depends_on `command-inventory.md`: исполнять ПОСЛЕ него** (решение Q4). Пока
  `gitmark inventory` не зашиплен, таблицы рукописные и Shotgun Surgery повторится;
  после — генерация закроет сводные таблицы, правка сузится до секций и витрин.
  Не начинать `/ship`, пока `command-inventory` не `archived`.
- Тело `grill.md` — только биндинг на навык `grilling`; не дублировать дисциплину
  раундов текстом (иначе второй источник правды о поведении).
- `description` команды — с русскими триггерами; имя файла/команды — латиница.
- Обычный грилл не создаёт durable-артефактов: в доках не обещать ему вывод в KB.
- Стоп-точек (`stop-before-commit` и т.п.) не требуется — правка чисто доковая.

## Context

Дизайн согласован с оператором на /grilling-сессии 2026-08-28 (Q1–Q5):

- **Q1=a:** обычный грилл = ноль записей (оптический вход). Критика stateless-гриля
  из `ticket-driven-ship.md` остаётся в силе; граница ролей зафиксирована поправкой
  2026-08-28 в том же решении.
- **Q2:** биндинг на проектный `grilling` (тот же темп раундов, что у `/grilling`),
  НЕ на глобальный `grill-me` («по одному вопросу», чужой файл, которого может не
  быть на другой машине — пакет копируется через deploy-ontoship).
- **Q3:** имя `/grill` — свободно (0 вхождений во всём репо и в
  `~/.omp/agent/commands/`); проектные команды бьют пользовательские (native
  provider, project-first), коллизии нет; префикс `mp-*` для навыков сохранён.
- **Q4:** после `command-inventory` (см. Constraints).
- **Q5:** имя латиницей, русские триггеры в `description`; `/грилл`-синоним не
  вводится. Эмпирически проверено: omp регистрирует кириллическое имя команды
  (`{"name":"грилл","source":"file"}` в `get_available_commands`), так что отказ —
  дизайн-решение (не расщеплять реестр), не техническое ограничение.
- **Находка сессии:** `docs/services/grilling/README.md` уже объявляет проектный
  `grilling` обработчиком фразы «grill me» — голос у обычного грилла в KB есть,
  не хватало глагола.
- **Цена регистрации** новой команды измерена по `87086cc`: ~11 файлов. Точный
  чеклист мест правки — в `.omp`-сессии: `local://grill-command-pair-checklist.md`
  (перенесён в Scope выше).
- **Собачий корм:** план исполняется онтошиповым механизмом: `/ship` по файлу-плану
  как единым срезом (тикеты не нужны — один срез).
- **Override гейта Q4 (2026-08-28, оператор):** `/ship` запущен до архивации
  `command-inventory` по явному решению оператора: зависимость была оптимизацией,
  не корректностью — rework нулевой (поздняя генерация `inventory` перепишет
  строку `/grill` идентично). В срез включена правка счётчика «11 файлов» → 12 в
  `command-inventory.md`.
