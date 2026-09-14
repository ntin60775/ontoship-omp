---
node_type: plan
title: Payload ссылается на непоставляемые артефакты — модель KB, схема приёмки, стандарты
service: _platform
status: draft
updated: 2026-09-14
links:
  depends_on: [deploy-check-marketplace-paths/README.md]
  documents: [../../.omp/rules/acceptance-rounds.md, ../../.omp/skills/kb-curate/SKILL.md, ../../.omp/skills/mp-code-review/SKILL.md]
  relates_to: [../ontology.md, ../services/kb-curate/README.md]
---

# Контракт: payload не ссылается на то, чего у потребителя нет

## Порядок выполнения

- **После** `deploy-check-marketplace-paths`: общий файл `.omp/skills/kb-curate/SKILL.md`
  (тикет 01 того плана меняет в нём путь к движку, этот план — ссылку на модель
  онтологии) и общий `docs/plans/README.md`.
- **Не связан** с `registry-and-version-in-consumer`: общих файлов нет, порядок этих двух
  планов обратим. Но `kb-docs-vs-plugin-delivery` обязан идти после обоих.
- **До** `kb-docs-vs-plugin-delivery`: доки репо описывают итоговое состояние payload.

## Goal

Ни одно правило, команда или навык пакета не требует артефакта, которого у потребителя
нет. Плагин доставляет только `.omp/` (`commands/ rules/ scripts/ skills/`) — значит всё,
на что ссылается payload, обязано лежать внутри payload: либо в самом тексте правила, либо
файлом рядом с навыком и адресуемо через `skill://<skill>/<файл>` (резолвится и в кэше
плагина, проверено). Ссылки на `docs/**` проекта-источника из payload уходят.

## Done

- Правило `acceptance-rounds` больше не ссылается на отсутствующий
  `docs/reference/acceptance-rounds.md`: полная схема раундов лежит файлом внутри
  payload (`.omp/skills/dev-flow/…`) и адресуется как `skill://dev-flow/<файл>`; в самом
  правиле остаются краткие инварианты. Инлайн всей схемы в правило отклонён: правило
  always-on, его текст читается в каждой сессии.
- `kb-curate` перестаёт требовать `docs/ontology.md` как «Full model»: модель онтологии
  (словари `node_type`/`status`, обязательные поля frontmatter, папочная раскладка, типы
  связей, инварианты I1–I7) поставляется файлом рядом с навыком и читается через
  `skill://kb-curate/<файл>`; ссылка на KB-док остаётся только как «если он есть в проекте».
- `mp-code-review` берёт правила пакета из уже загруженного контекста (правила с
  `alwaysApply` присутствуют в сессии), а не из `.omp/rules/*.md` проекта; формулировка
  «the package's own rules ship with the repo» убрана.
- Висячие ссылки на удалённое правило `ship-1c` в payload убраны (навык `dev-flow`).
- Проверка: в probe-проекте с установленным плагином (без `docs/` и без `.omp/rules/`)
  каждое правило/команда/навык, требующее внешнего артефакта, получает его; ручная сверка
  «упомянутый путь существует» даёт ноль промахов; `gitmark lint` чистый в этом репо.
- KB синхронизирован: `docs/plans/README.md`, `gitmark lint`, `gitmark index`.

## Scope

- `.omp/rules/acceptance-rounds.md`, `.omp/skills/kb-curate/SKILL.md`,
  `.omp/skills/mp-code-review/SKILL.md`, `.omp/skills/dev-flow/SKILL.md`,
  новый файл схемы внутри `.omp/skills/dev-flow/`.
- `docs/plans/README.md`.

Вне scope: движок (реестр команд и версия) — план `registry-and-version-in-consumer`;
доки этого репо и README — план `kb-docs-vs-plugin-delivery`; bootstrap нового проекта —
план `consumer-bootstrap`.

## Constraints

- Источник истины не дублируется: схема приёмки и модель онтологии живут в одном месте,
  ссылки — по `skill://`.
- `skill://<skill>/<файл>` резолвится и из нативной установки, и из кэша плагина
  (проверено на `skill://kb-search/gitmark.py`); литерал `skill://` внутри bash-скрипта
  не резолвится — на скрипты это правило не распространяется.
- Правила остаются always-on только с коротким текстом: тяжёлые описания — файлом.

## Context

Аудит 2026-09-14 (отчёт `.scratch/audit-plugin-install-2026-09-14.md`, вне KB):

- `.omp/rules/acceptance-rounds.md:8` ссылается на `docs/reference/acceptance-rounds.md`;
  файла нет **и в этом репо** (в `docs/reference/` только README, architecture, commands,
  metrics) — правило always-on указывает в пустоту и у потребителя, и здесь.
- `.omp/skills/kb-curate/SKILL.md:8` («Full model: `docs/ontology.md`») — у потребителя
  этого файла нет: плагин везёт только `.omp/`; `/onto-doc` создаёт `docs/` проекта, но не
  reference-доки пакета.
- `.omp/skills/mp-code-review/SKILL.md:66` перечисляет стандарты как `.omp/rules/*.md` и
  «the package's own rules ship with the repo» — в плагинной установке `.omp/rules/`
  проекта пуст, ось Standards молча остаётся без источника.
- `.omp/skills/dev-flow/SKILL.md:68` ссылается на правило `ship-1c`, удалённое из пакета
  коммитом 83ba4ed («refactor(rules): убрать ship-1c, добавить acceptance-rounds»).
