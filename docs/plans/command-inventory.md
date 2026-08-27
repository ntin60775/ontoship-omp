---
node_type: plan
title: Реестр команд — генерируемый, единый источник, с I7 и исключением эфемеры
service: _platform
status: draft
updated: 2026-08-27
links:
  depends_on: [../ontology.md]
  documents: [../../.omp/skills/kb-search/gitmark.py, ../reference/commands.md, ../../README.md]
  relates_to: [../reference/architecture.md, ../services/gitmark-cli/README.md]
---

# Контракт: генерируемый реестр команд

## Goal

Список команд и навыков перестаёт быть рукописной копией в 7 местах. Единственный
полный реестр — `docs/reference/commands.md`, его сводные таблицы **генерируются** из
frontmatter `.omp/commands/*.md` и `.omp/skills/*/SKILL.md` новой субкомандой
`gitmark.py inventory`. Рассинхрон ловится машиной (`inventory --check` + инвариант
I7), а не охотой по файлам. Побочно: `gitmark` перестаёт индексировать эфемеру
(`.scratch/`, `.artifacts/` и всё, что в `.gitignore`) — эфемерные отчёты не должны
находиться поиском как «знание KB».

## Done

- `gitmark.py inventory` перегенерирует обе сводные таблицы (команды + навыки) внутри
  маркеров `<!-- BEGIN/END inventory:commands -->` и `<!-- BEGIN/END inventory:skills -->`
  в `docs/reference/commands.md`; повторный запуск не меняет файл (идемпотентность).
- `gitmark.py inventory --check` — exit≠0 при любом рассинхроне: файл команды без
  строки в таблице / без секции `## /cmd`; строка или секция без файла; отсутствующие
  `args:`/`drives:` во frontmatter. На чистом репо — exit 0.
- Во всех 11 `.omp/commands/*.md` frontmatter дополнен полями `args:` и `drives:`.
- `lint` включает **I7** (то же, что `--check`, в отчёте линта); на текущем репо — чисто.
- `index`/`search`/`lint`/`map` исключают пути из `.gitignore` (подмножество: точные
  имена папок со `/`, записи `*.ext`); отчёт в `.scratch/` не находится поиском.
- `README.md`: дубли-таблицы навыков/команд убраны, осталась ссылка на
  `docs/reference/commands.md` как единственный реестр; числовых счётчиков («N skills»)
  нет и не будет.
- `tests/test_gitmark.py` (pytest, tmp-фикстуры): 5–7 тестов на новое поведение —
  идемпотентность `inventory`, поимка рассинхрона `--check`, парсер `.gitignore`,
  I7 на отсутствующую секцию. Проходят; существующее поведение не покрывается.
- KB синхронизирован: `docs/ontology.md` документирует I7; `docs/services/gitmark-cli/README.md`,
  `.omp/skills/kb-search/SKILL.md`, `docs/reference/architecture.md` упоминают `inventory`;
  индексы `docs/plans/README.md` и `docs/README.md` дополнены.
- `gitmark.py lint` чистый, `index` пересобран.

## Scope

- `.omp/skills/kb-search/gitmark.py` — субкоманда `inventory` (+`--check`), парсер
  `.gitignore`, I7 в `lint`, исключение игнорируемых путей в `index`/`search`/`lint`/`map`.
- `.omp/commands/*.md` (11 файлов) — только frontmatter (`args:`, `drives:`), тела не трогать.
- `docs/reference/commands.md` — маркеры + генерируемые таблицы; рукописные секции
  `## /cmd` остаются рукописными (генерится только таблица).
- `README.md` — убрать дубли-таблицы, оставить ссылку.
- `docs/ontology.md`, `docs/services/gitmark-cli/README.md`, `.omp/skills/kb-search/SKILL.md`,
  `docs/reference/architecture.md`, `docs/plans/README.md`, `docs/README.md` — синхронизация.
- `tests/test_gitmark.py` — новый файл.

Вне scope: дерево в `architecture.md` (иллюстрация, не реестр — не генерируется);
«витрины» в `AGENTS.md` и `CONTEXT.md` (остаются, I7 их не проверяет); покрытие
существующего поведения `gitmark.py` тестами; покрытие тестами навыка `mp-code-review`.

## Constraints

- `gitmark.py` остаётся чистым stdlib (парсер `.gitignore` — рукописный подмножество,
  без библиотек и без вызова `git check-ignore`).
- Генерация пишет **только** между маркерами; вне маркеров файл не трогать.
- I7 проверяет соответствие строго в одну пару: `commands.md` ↔ `.omp/commands/*.md`
  (таблица + секция `## /cmd` ↔ файл). Витрины не проверяются никогда.
- `inventory --check` — единственный источник истины для CI/гейта; дублировать проверку
  в других субкомандах, кроме появления той же ошибки в отчёте `lint`, запрещено.
- Исключение по `.gitignore` применяется ко всем режимам, читающим `.md` репо;
  `.gitmark/` и `*-map.html` и так не индексировались — поведение не регрессировать.
- Таблица навыков генерится из существующих `name`/`description` — новых полей у
  навыков не требовать.
- Числовые счётчики состава в доках запрещены (протухают; выводятся из `stat`).

## Context

Дизайн согласован с оператором на/grilling-сессии 2026-08-27 (Q1–Q7):

- **Проблема.** Перечисление команд/навыков живёт руками в 7 местах; за один день
  найдены три протухших (README «nine skills and five commands» при 11/9, «Four
  families» при трёх, список в `CONTEXT.md`). Добавление двух команд тронуло 16 файлов.
  Это же Shotgun Surgery из отчёта `/code-review` (`.scratch/code-review-20260827T154730Z.md`,
  находка №3).
- **Q1:** генерятся обе таблицы (команды и навыки) в `commands.md`; README — ссылка,
  без чисел. **Q2:** `inventory` (пишет) + `inventory --check` (докладывает, exit≠0).
  **Q3:** генерится только таблица; секции `## /cmd` рукописные, но их наличие обязательно.
  **Q4:** `args:`/`drives:` обязательны у команд; навыки — из `name`/`description`.
  **Q5:** эфемера исключается чтением `.gitignore` (один источник правил).
  **Q6:** минимальные pytest-тесты ровно на новое поведение. **Q7=B:** полный реестр —
  только `commands.md`; витрины в `AGENTS.md`/`CONTEXT.md` остаются, I7 их не трогает.
- **Смежная находка:** `gitmark index` сканирует все `.md` репо — отчёт ревью из
  `.scratch/` попал в поиск как знание KB (закрыто пунктом Q5/Done).
- **Предпосылка:** незакоммиченный дифф этой же сессии (синк grilling, `/architecture`,
  `/code-review`, переименование в `mp-improve-codebase-architecture`) — план исполняется
  поверх него; 11 файлов `.omp/commands/*.md` включают две новые команды.
- **Собачий корм:** план исполняется онтошиповым механизмом: `/to-tickets` (по желанию)
  и `/ship` — один-два среза, укладывается в одно контекст-окно.
