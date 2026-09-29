---
node_type: plan
title: "`report` в таблице модели — согласовать с прозой навыка"
service: _platform
status: archived
updated: 2026-09-29
links:
  documents: [../../.omp/skills/kb-curate/SKILL.md, ../../.omp/commands/doc.md, ../../.omp/skills/kb-curate/ontology.md, ../../docs/ontology.md]
  relates_to: [../../docs/services/gitmark-cli/README.md]
---

# Контракт: `report` — узнаваемый тип KB-документа

## Goal

Тип `report` объявлен в прозе навыка `kb-curate` и команды `/doc` как допустимый
`node_type` для KB-документа, но в машиночитаемой таблице модели отсутствовал.
Потребитель на 0.4.8 получал неустранимую пару ошибок: `ERR I2` (неизвестный тип),
если не объявлял `report` у себя, либо `WARN I8` (дрейф модели), если объявлял.

Нужно: строка `report` есть в обеих копиях таблицы `node_type`, её семантика — тип
KB-документа (исследовательский отчёт, обзор, handoff), проза навыка и команды
согласована с этой семантикой.

## Done

- В таблице `node_type` в `docs/ontology.md` и `.omp/skills/kb-curate/ontology.md`
  присутствует строка `report`, описывающая KB-документ (не `.scratch/` и не
  «эфемерный»).
- Проза `kb-curate/SKILL.md` (строки 23–24, 97) и `commands/doc.md` (строка 14)
  сохраняют `report` в списке типов KB-документа; семантика таблицы и прозы не
  противоречат друг другу.
- `NODE_TYPES` в `gitmark.py` содержит `report`.
- `gitmark lint` на этом репо — чистый (I2, I8).
- `gitmark index` пересобран.

## Scope

- `docs/ontology.md` — строка `report` в таблице `node_type`.
- `.omp/skills/kb-curate/ontology.md` — строка `report` в таблице `node_type`
  (пакетная копия для I8).
- `.omp/skills/kb-search/gitmark.py` — `NODE_TYPES` фолбэк-словарь.
- `.omp/skills/kb-curate/SKILL.md` — списки типов в шагах «Pick a `node_type`».
- `.omp/commands/doc.md` — список типов в шаге 2 команды `/doc`.
- `docs/plans/README.md` — индексная строка этого плана.

Вне scope: bump версии в каталоге маркетплейса, релиз — репо-каталог,
отдельный прогон.

## Constraints

- **Одна строка — одна семантика.** `report` не может быть одновременно KB-типом
  и эфемерным артефактом `.scratch/`.
- `ontology.md` правится в обеих копиях **одним коммитом** — иначе I8 упадёт
  уже в этом репо (плоская раскладка: обе копии видны).
- `doc.md` и `SKILL.md` не получают новых `args`/`drives`, реестр команд
  (`inventory`) не требует перегенерации.
- `stop-before-commit` — после тестов и ревью ран останавливается, коммит
  подтверждает оператор.

## Context

- Issue #6 (2026-09-28): полный баг-репорт с воспроизведением на 0.4.8.
- Потребитель (приватный репо) перетипировал документы в `reference`, чтобы
  обойти ERR I2; после синхронизации `ontology.md` с пакетной копией lint стал
  чистым, но причина (отсутствующий тип) не устранена на стороне пакета.
