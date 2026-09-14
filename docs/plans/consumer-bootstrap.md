---
node_type: plan
title: Bootstrap потребителя — entry point и установка «с нуля»
service: _platform
status: draft
updated: 2026-09-14
links:
  depends_on: [deploy-check-marketplace-paths/README.md, kb-docs-vs-plugin-delivery.md]
  documents: [../../.omp/commands/onto-doc.md]
  relates_to: [../ops/deploy-ontoship.md, ../../AGENTS.md]
---

# Контракт: свежий потребитель доходит до зелёного deploy-check

## Порядок выполнения

- **После** `deploy-check-marketplace-paths`: приёмка этого плана заканчивается зелёным
  `deploy-check`, а красный в плагинной установке чинит тикет 02 того плана.
- **После** `kb-docs-vs-plugin-delivery`: оба плана правят `docs/ops/deploy-ontoship.md`;
  тот план описывает канал доставки, этот — дописывает в него сценарий «с нуля».
- **Последний в очереди**: от него не зависит ни один план. `payload-refs-undelivered-docs`
  и `registry-and-version-in-consumer` с ним не связаны.

## Goal

Проект, поставивший плагин маркетплейса и ничего больше, доходит до `deploy-check`
`exit 0` без ручной сборки entry point: пакет даёт идемпотентную инициализацию, которая
создаёт `AGENTS.md` проекта, приводит `.gitignore` к требованиям правил и передаёт работу
`/onto-doc`. Плагин доставляет только `.omp/` — проектные файлы он не пишет и не затирает;
инициализация запускается человеком и только по проекту.

## Done

- Зафиксировано решение: отсутствие `AGENTS.md` у потребителя закрывается командой
  инициализации в payload (идемпотентной), а не требованием к проекту.
- Команда инициализации: пишет `AGENTS.md` из шаблона (шаблон — часть payload, не `docs/`
  пакета), добавляет в `.gitignore` строки, которых требуют правила (`.gitmark/`,
  `*-map.html`, `.scratch/`), и зовёт `/onto-doc`; повторный запуск ничего не ломает и
  ничего не затирает.
- Проверка «с нуля»: чистая probe-папка → установка плагина → инициализация → `/onto-doc`
  → `deploy-check` `exit 0`; шаги описаны в runbook.
- KB синхронизирован: `docs/plans/README.md`, `gitmark lint` чистый, индекс пересобран.

## Scope

- Payload: команда инициализации и шаблон entry point внутри `.omp/`.
- `docs/ops/deploy-ontoship.md` — сценарий «с нуля».
- `docs/plans/README.md`.

Вне scope: поведение самого `deploy-check.sh` — план `deploy-check-marketplace-paths`;
доки README/architecture — план `kb-docs-vs-plugin-delivery`.

## Constraints

- Идемпотентность: повторный запуск на уже инициализированном проекте не перезаписывает
  проектные файлы (KB, `AGENTS.md` — только по явному согласию).
- Плагин остаётся доставкой только `.omp/`; проектные данные (`AGENTS.md`, `docs/`) —
  собственность проекта.
- Шаблон едет в payload: у потребителя нет `docs/` пакета.

## Context

Аудит 2026-09-14 (отчёт `.scratch/audit-plugin-install-2026-09-14.md`, вне KB):

- Каталог объявляет источник как `git-subdir` с `path: ".omp"` — в потребителя едут только
  `commands/ rules/ scripts/ skills/`; `AGENTS.md` и `docs/` не поставляются.
- В поставке 0.2.0 нет команд инициализации и апгрейда (архивный план `marketplace-delivery`
  репо-каталога, тикет 03 — `/ontoship:init` + `/ontoship:upgrade` — не доехал).
- `deploy-check.sh` считает отсутствие `AGENTS.md` критическим (`exit 1`) — значит свежий
  потребитель без entry point красный по построению, а создать его нечем.
- Плагинные потребители на машине (`sot-omp-marketplace`, `erp-demo`) вышли из миграции с
  уже написанным `AGENTS.md`; сценарий «с нуля» нигде не описан.
