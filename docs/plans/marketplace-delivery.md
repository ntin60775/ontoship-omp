---
node_type: plan
title: Поставка OntoShip через omp-маркетплейс (каталог-репо + git-subdir)
service: _platform
status: deprecated
updated: 2026-08-30
links:
  depends_on: [../decisions/omp-only-package.md, ../ops/deploy-ontoship.md]
  documents: [../../.omp/skills/kb-search/SKILL.md, ../../.omp/commands, ../../.omp/rules]
---

# Контракт: поставка обновлений через omp-маркетплейс

> **Перенесён 2026-08-30:** разработка продолжается в
> [`ntin60775/sot-omp-marketplace`](https://github.com/ntin60775/sot-omp-marketplace)
> (`docs/plans/marketplace-delivery.md`): репо-каталог стал домом плагина
> (`plugins/ontoship/`, `source: "./plugins/ontoship"`), этот репо — первый
> клиент маркетплейса. Ниже — историческая черновик-версия контракта.

## Goal

OntoShip становится первым плагином личного маркетплейса omp-формата: обновления
движка (skills + commands + rules + gitmark.py) доставляются штатным механизмом
`/marketplace` — один `omp plugin upgrade` обновляет все проекты, копирование
`.omp/` в каждый проект руками уходит. OntoShip остаётся проектным навыком:
`AGENTS.md` и `docs/` (KB) — данные проекта, плагином не поставляются и
обновлениями не затираются.

## Done

- Новый репо-каталог `ntin60775/sot-omp-marketplace` (поле `name` каталога —
  `sot-omp-marketplace`, id плагина `ontoship@sot-omp-marketplace`): только
  `.omp-plugin/marketplace.json` + README-витрина. Запись каталога:
  `name: "ontoship"`, `source: { source: "git-subdir", url: "...ontoship-omp.git",
  path: ".omp", ref: "v0.2.0", sha: ... }`, `version: "0.2.0"`.
- Плагин живёт в этом же репо: корень плагина — каталог `.omp/` (раскладка
  `skills/<name>/SKILL.md`, `commands/*.md`, `rules/*.md` совпадает с
  конвенцией плагина без дублирования; dogfood-репо продолжает грузить их
  нативным провайдером с приоритетом 100, короткие `/kb`-имена сохраняются).
- `.omp/package.json` (`name: "ontoship"`, `version`, `description`) — метаданные
  плагина и источник для `gitmark version`; НО для маркетплейса авторитетна
  `version` из записи каталога (фолбэк на манифесты внутри git-subdir не
  срабатывает — проверено, даёт 0.0.0), поэтому релизный bump обязателен там.
- Все ссылки на CLI в `.omp/**` и `docs/**` переведены с
  `python3 .omp/skills/kb-search/gitmark.py` на
  `python3 skill://kb-search/gitmark.py` (резолв `skill://` в bash проверен
  экспериментально; работает и из нативной установки, и из кэша плагина).
- Новая команда `.omp/commands/init.md` (`/ontoship:init` в проектах-потребителях):
  пишет `AGENTS.md` из шаблона (встроен в текст команды), добавляет в
  `.gitignore` строки `.gitmark/`, `*-map.html`, `.scratch/`, `.omp/plugins/`,
  зовёт `/ontoship:onto-doc` для бутстрапа KB. Идемпотентна: существующие
  файлы не затирает.
- Новая команда `.omp/commands/upgrade.md` (`/ontoship:upgrade`) — пакетный
  апгрейд по списку проектов: читает реестр `~/ontoship-projects.txt` (по строке
  на проект, вне git), для каждого: `omp plugin upgrade` (project-scope) +
  пересборка `.gitmark/index.db`; user-scope апгрейдится один раз на машину и
  в цикле не нуждается. Без реестра — команда работает для текущего проекта.
- `docs/ops/deploy-ontoship.md` переписан под маркетплейс-поток; добавлен
  `docs/ops/release-ontoship.md` (тег в ontoship-omp → bump `version`+`ref`+`sha`
  в записи каталога одним коммитом → у потребителей
  `omp plugin marketplace update sot-omp-marketplace && omp plugin upgrade
  ontoship@sot-omp-marketplace`;
  переустановка — `install --force`); ADR
  `docs/decisions/marketplace-delivery.md` (поставка = omp-маркетплейс;
  уточняет `omp-only-package`: тот запрет был про Claude Code marketplace,
  omp-нативный канал ему не противоречит).
- `gitmark.py index`/`lint` чистые; README (репо и каталога) описывают установку
  двумя скоупами.

## Scope

- ontoship-omp: `.omp/**` (пути CLI, package.json, init.md, upgrade.md), `gitmark.py`
  (version из package.json; проверить авто-резолв корня по cwd, а не по
  расположению скрипта), `docs/ops/*`, `docs/decisions/marketplace-delivery.md`,
  `docs/plans/README.md`, `README.md`, `AGENTS.md`.
- новый репо-каталог: `marketplace.json` + README (создаётся вручную/скриптом,
  вне этого репо).
- Не входит: миграция существующих проектов-потребителей (runbook-инструкция
  `rm -rf .omp/skills .omp/commands .omp/rules` + install + init — в доке, не
  автоматизацией); CI-релизы; шифрование/подпись артефактов.

## Constraints

- `stop-before-commit` (правило ship-gate).
- Префикс `ontoship:` в проектах-потребителях принят сознательно; короткие
  имена остаются только в dogfood-репо за счёт приоритета native-провайдера.
- Версии в каталоге — строгий semver, обязателен bump на каждый релиз
  (иначе `upgrade` не сработает: сравнение только по `version`).
- `.omp/plugins/` в проектах-потребителях — машинная эфемера (абсолютные
  symlink-пути в кэш), в git не коммитится.

## Context

Проверено экспериментом на локальном probe-маркетплейсе (omp v18.0.6):
1. rules из маркетплейс-плагина доставляются и `alwaysApply` срабатывает —
   вопреки перечню провайдеров в доке `rulebook-matching-pipeline` (в нём нет
   `claude-plugins` для rules);
2. команды плагина префиксуются `<plugin>:<command>`;
3. `bash skill://<skill>/<file>` автоматически резолвится в реальный путь —
   в том числе для файлов из кэша плагина (`~/.omp/plugins/cache/...`);
4. user-scope установка видна во всех проектах; project-scope тенит user-scope
   той же пары `name@marketplace`;
5. `installed_plugins.json` хранит абсолютные `installPath` — коммитить его в
   проект нельзя, только gitignore.
6. `gitmark index` перестраивает `.gitmark/index.db` полностью (DELETE + INSERT,
   `CREATE ... IF NOT EXISTS`), версионности схемы нет → после апгрейда плагина
   достаточно `gitmark index`, миграций не требуется; `.gitmark/` в gitignore —
   индекс не переживает `git clean`, что и учитывает upgrade-цикл.
7. полный цикл `upgrade` на живом probe: bump версии в каталоге (0.1.0→0.2.0) →
   `omp plugin marketplace update` → `omp plugin upgrade --scope project` →
   `installPath` переехал в кэш `...___0.2.0`, контент обновился; идемпотентен;
8. `git-subdir` с `path: ".omp"` (скрытая директория!) ставится из реального
   ontoship-omp по SSH: в кэше commands/ (12), rules/ (4), scripts/, skills/;
   правила плагина реально грузятся в проекте-потребителе (KB first, KB source
   of truth, Ship gate, ship-1c видны в rulebook), и команда плагина из
   git-subdir реально исполняется (`/sub:hello` → маркер OK); `ref` как тег не
   проверен на живом удалённом репо — при первом релизе верифицировать тег
   или пиновать `sha`;
9. в проекте-потребителе старый путь `python3 .omp/skills/kb-search/gitmark.py`
   дохнет (Errno 2), а `python3 skill://kb-search/gitmark.py` резолвится из
   кэша плагина — перевод путей из Done-пункта обязателен, а не косметика.
