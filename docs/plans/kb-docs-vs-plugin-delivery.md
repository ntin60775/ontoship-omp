---
node_type: plan
title: Доки пакета против ADR доставки плагинами
service: _platform
status: draft
updated: 2026-09-14
links:
  depends_on: [deploy-check-marketplace-paths/README.md, payload-refs-undelivered-docs.md, registry-and-version-in-consumer/README.md]
  documents: [../../README.md, ../../AGENTS.md]
  relates_to: [../reference/architecture.md, ../ops/deploy-ontoship.md]
---

# Контракт: доки источника не противоречат доставке плагинами

## Порядок выполнения

- **После** `deploy-check-marketplace-paths` (тикет 03 правит тот же
  `docs/ops/deploy-ontoship.md`), `payload-refs-undelivered-docs` и
  `registry-and-version-in-consumer` (последний меняет спецификацию движка в
  `docs/services/gitmark-cli/README.md`, которую правит этот план).
- Это **честный проход по докам поверх устоявшегося поведения**: пока планы выше не
  отгружены, тексты пришлось бы переписывать дважды.
- **До** `consumer-bootstrap`: сценарий «с нуля» дописывается в уже выправленный runbook.

## Goal

Документация репозитория-источника описывает фактический канал доставки — плагин
маркетплейса — и не содержит ни утверждений, противоречащих ADR «доставка плагинами»,
ни ссылок на правила, которых в пакете больше нет. Читатель (человек) из README и
architecture понимает, что установка идёт плагином, где лежат команды/правила/навыки у
потребителя и какие команды он может выполнить сам.

## Done

- `docs/reference/architecture.md`: утверждение «No marketplace, no manifest, no
  installation step» заменено описанием фактической доставки (плагин маркетплейса,
  `.omp/plugins/node_modules/<плагин>` у потребителя); упоминания правила `ship-1c`
  убраны.
- `README.md`: раздел установки описывает штатный плагинный канал; ручное копирование
  `.omp/` помечено локальным/legacy-вариантом; примеры команд движка больше не ведут по
  плоскому пути у потребителя (команды агента `/kb`, `/kb-map` либо реальный путь
  плагина).
- `AGENTS.md`: перечень правил приведён к фактическому составу пакета (без `ship-1c`).
- `docs/services/gitmark-cli/README.md`: описание путей движка согласовано с плагинной
  установкой — плоский путь помечен как путь этого репо, идиома
  `G="python3 <путь>"` приведена к рабочему виду (URI в присваивании не резолвится).
- Ссылка на ADR доставки (репо-каталог `sot-omp-marketplace/docs/decisions/plugin-delivery.md`)
  добавлена без копирования текста: ADR живёт в каталоге.
- Политика сосуществования форм зафиксирована: при установке плагина поверх плоских копий
  копии сносятся (иначе навыки и правила дублируются, нативный провайдер перекрывает
  плагинный); в доке сказано, какая форма штатная и что делать с остатками старой.
- `docs/ops/deploy-ontoship.md`: строка про правило `ship-1c` убрана; остальное в этом
  файле — scope тикета 03 плана `deploy-check-marketplace-paths`.
- `gitmark lint` чистый, индекс пересобран.

## Scope

- `README.md`, `AGENTS.md`, `docs/reference/architecture.md`,
  `docs/services/gitmark-cli/README.md`, `docs/ops/deploy-ontoship.md` (одна строка),
  `docs/plans/README.md`.

Вне scope: `.omp/skills/dev-flow/SKILL.md` (ссылка на `ship-1c` в payload) — план
`payload-refs-undelivered-docs`; поведение движка — план
`registry-and-version-in-consumer`; установка «с нуля» — план `consumer-bootstrap`.

## Constraints

- ADR не дублируется: KB этого репо ссылается на ADR каталога, а не пересказывает его.
- Доки этого репо описывают пакет-источник и его собственные команды; потребительские
  пути в них даются либо плагинным путём, либо командой агента.
- Ни одна правка не меняет поведение пакета — только тексты.

## Context

Аудит 2026-09-14 (отчёт `.scratch/audit-plugin-install-2026-09-14.md`, вне KB):

- `docs/reference/architecture.md:22` — «No marketplace, no manifest, no installation
  step»; строки 81 и 140 описывают правило `ship-1c`, удалённое коммитом 83ba4ed.
- `README.md:148-171` — примеры с плоским путём движка и раздел «Copy the package …
  no marketplace needed»; `README.md:159-161` называет копирование основным способом.
- `AGENTS.md:30` — перечень правил включает `ship-1c`.
- `docs/services/gitmark-cli/README.md:25-26,174-184` — плоский путь скрипта и идиома
  `G="python3 .omp/skills/kb-search/gitmark.py"`; у потребителя такой путь мёртв, а URI в
  присваивании не резолвится (проверено запуском).
- ADR «доставка плагинами» (2026-09-11) лежит в репо-каталоге; в этом репо ADR нет —
  поэтому две правды видны читателю сразу.
- Раскладки на машине (2026-09-14): плоских потребителей 6 (`ontoship-omp`,
  `subvost-xray-tun`, `erp-main`, `erp-mini`, `rusbread-master-site`, `ut-10`),
  плагинных 2 (`sot-omp-marketplace`, `erp-demo`) — обе формы в обиходе, доки обязаны
  называть обе и указывать, какая штатная.
