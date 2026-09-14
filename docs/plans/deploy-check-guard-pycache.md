---
node_type: plan
title: Страж deploy-check не ловит __pycache__ в пакете
service: _platform
status: draft
updated: 2026-09-14
links:
  documents: [../../.omp/scripts/deploy-check.sh]
  relates_to: [deploy-check-marketplace-paths/README.md]
---

# Контракт: страж deploy-check не даёт ложный FAIL на байткоде

## Goal

Проверка-страж «в payload не осталось мёртвого пути движка» срабатывает только на
настоящих ссылках в текстах пакета и не срабатывает на служебных артефактах: сейчас
`grep -rl` по `$pkg/skills` находит литерал внутри `__pycache__/*.pyc` (скомпилированный
байткод содержит строки исходника), из-за чего здоровая установка получает `exit 1`.

## Done

- Страж ограничен текстовыми файлами payload (`.md`) — байткод и прочие служебные
  артефакты из области поиска уходят.
- Ложный FAIL воспроизведён до фикса и исчезает после: в этом репо при наличии
  `.omp/skills/kb-search/__pycache__/` прогон даёт `exit 0` (до фикса — `exit 1` с
  указанием на `.pyc`).
- Настоящий литерал в `.md` по-прежнему ловится: probe-пакет с инъекцией строки в
  `rules/kb-first.md` даёт `[FAIL]` и `exit 1`.
- Прогоны сохранены: этот репо `exit 0`; плагинный путь у потребителей
  (`sot-omp-marketplace`, `erp-demo`) `exit 0`; сломанный пакет и инъекция `exit 1`.
- `gitmark lint` чистый, индекс пересобран.

## Scope

- `.omp/scripts/deploy-check.sh` — область поиска стража.
- `docs/plans/README.md` — запись в очереди и индексе.

## Constraints

- Коды возврата (0/1/2) и порядок проверок не меняются.
- Страж остаётся жёстким: любая ссылка на `.omp/skills/kb-search/gitmark.py` в правилах,
  командах или навыках пакета — `[FAIL]`.
- Служебные артефакты (`__pycache__`, `.pyc`) не считаются содержимым payload.

## Context

Найдено при верификации тикета 02 плана `deploy-check-marketplace-paths` (2026-09-14),
уже после архивации того плана: `bash .omp/scripts/deploy-check.sh` в ворктри дал `exit 1`
с сообщением

```
[FAIL] мёртвый путь движка в payload (нужен skill://kb-search/gitmark.py):
    /tmp/ontoship-ship-06/.omp/skills/kb-search/__pycache__/gitmark.cpython-313.pyc
```

Причина: `grep -rl '\.omp/skills/kb-search/gitmark\.py' "$pkg/rules" "$pkg/commands" "$pkg/skills"`
читает и бинарные файлы, а байткод Python хранит строковые литералы исходника. Ложный FAIL
воспроизводится в любой установке, где движок уже запускался (плоская копия в `.omp/`,
ворктри, кэш плагина), то есть почти всегда — проверка непригодна.

Правило приёмки (`.omp/rules/acceptance-rounds.md`): замечания после архивации плана идут
новым багфикс-контрактом, а не правкой поверх архивного тикета — отсюда этот файл.
