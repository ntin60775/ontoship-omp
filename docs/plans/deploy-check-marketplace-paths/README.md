---
node_type: plan
title: Пути движка в пакете — маркетплейс-установка (deploy-check.sh + payload)
service: _platform
status: archived
updated: 2026-09-14
links:
  documents: [../../../.omp/scripts/deploy-check.sh]
  relates_to: [../../services/gitmark-cli/README.md, ../../ops/deploy-ontoship.md]
---

# Контракт: пути движка в пакете при плагинной установке

## Порядок выполнения

- **Первый в очереди** (`docs/plans/README.md` → «Очередь исполнения»): живой баг — два
  потребителя с плагинной установкой (`sot-omp-marketplace`, `erp-demo`) получают ложный
  `exit 1` — плюс страж против возврата всего класса.
- От этого плана зависят: `payload-refs-undelivered-docs` (общий
  `.omp/skills/kb-curate/SKILL.md`), `registry-and-version-in-consumer` (общий
  `.omp/skills/kb-search/SKILL.md`), `kb-docs-vs-plugin-delivery` (общий
  `docs/ops/deploy-ontoship.md`) и `consumer-bootstrap` (его приёмка «с нуля» заканчивается
  зелёным `deploy-check`).
- Внутри плана порядок жёсткий: **01 → 02 → 03**. Страж из тикета 02 красный, пока payload
  не мигрирован (тикет 01), а runbook тикета 03 описывает поведение уже исправленного
  скрипта.

## Goal

Пакет, доставленный маркетплейсом, работает у потребителя: `deploy-check.sh`
завершается `exit 0` на здоровой установке и `exit 1` на реально сломанной, а все
обращения к gitmark-CLI из payload (правила, команды, навыки) резолвятся, а не ведут
в мёртвый плоский путь `.omp/skills/…`. Скрипт перестаёт быть «зелёным вслепую»:
он сам ловит класс «payload ссылается на несуществующий путь движка».

## Done

- `deploy-check.sh` резолвит корень пакета от собственного расположения, а не хардкодит
  плоский layout. `$0`/`BASH_SOURCE[0]` абсолютизируется **до** `cd` в корень проекта:
  скрипт делает `cd "$(git rev-parse --show-toplevel)"` (стр. 7), и относительный `$0`
  при запуске из подкаталога после этого не резолвится.
- Под корнем пакета резолвятся только `skills/`, `commands/`, `rules/`, `scripts/`.
  `AGENTS.md`, `docs/`, `.gitignore` остаются **проектными** (от корня git-репо, как
  сейчас): плагин доставляет только содержимое `.omp/`, AGENTS.md в payload нет.
- Все ссылки на движок в payload переведены на `python3 skill://kb-search/gitmark.py …`:
  `.omp/rules/kb-first.md`, `.omp/rules/kb-source-of-truth.md`,
  `.omp/commands/{kb,kb-map,doc,onto-doc}.md`,
  `.omp/skills/{kb-search,kb-curate,mp-grill-with-docs}/SKILL.md`.
- URI идёт **аргументом команды**, а не через переменную: идиома
  `G="python3 skill://kb-search/gitmark.py"` не работает — в присваивании харнесс URI
  не резолвит (проверено запуском). `kb-search/SKILL.md` переписывается под прямые вызовы.
- `deploy-check.sh` получает проверку-страж: литерал `.omp/skills/kb-search/gitmark.py`
  в пакетных `rules/`, `commands/`, `skills/` → `[FAIL]` (иначе зелёный deploy-check
  стоит на пакете, чьи правила ведут в никуда).
- Смоук-поиск перестаёт быть вакуумным: сейчас `hits="$(… 2>&1)" || rc=1;
  [[ -n "$hits" ]]` считает текстом ошибки python «хитом» и `[FAIL] поиск вернул пусто`
  не печатается (воспроизведено). stderr отделяется, пустой результат → `[FAIL]`.
- Семантика кодов возврата сохранена: FTS5 обязателен (`exit 1`), trigram опционален
  (`exit 2`), предупреждения по `docs/` и `.gitignore` (`exit 2`). Порядок проверок
  сохранён; добавляется только проверка-страж.
- Проверка `.gitignore` доведена до требований правил: `kb-source-of-truth` требует
  игнорировать `.gitmark/`, `*-map.html` и `.scratch/`, а скрипт предупреждает только про
  первое. Новые предупреждения не меняют код возврата.
- Приёмка (в этом ране):
  - (a) в этом репо `bash .omp/scripts/deploy-check.sh` → `exit 0`;
  - (b) в потребителях с плагинной установкой (`sot-omp-marketplace`, `erp-demo` —
    оба ставят `ontoship@0.2.0`) исправленный скрипт, запущенный по плагинному пути
    с cwd потребителя, → `exit 0`;
  - (c) зафиксировано явно: **установленная** копия позеленеет только после релиза
    v0.2.1 в этом репо + bump `ref` в каталоге + `omp plugin upgrade` у потребителя —
    вне этого рана.
- `docs/ops/deploy-ontoship.md` обновлён: канал установки — плагин маркетплейса,
  путь к скрипту у потребителя — `.omp/plugins/node_modules/ontoship/scripts/deploy-check.sh`.
  Команды движка в runbook остаются с реальным путём: runbook читает человек, а в
  человеческой оболочке `skill://` не резолвится. ADR доставки — ссылкой на
  репо-каталог (`sot-omp-marketplace/docs/decisions/plugin-delivery.md`), без дублирования.
- KB синхронизирован: `docs/plans/README.md` дополнен ссылкой на план; `gitmark lint`
  чистый, `index` пересобран.

## Scope

- `.omp/scripts/deploy-check.sh` — самоотносительный корень, проверка-страж, смоук-поиск.
- Payload-файлы со ссылками на движок: `.omp/rules/{kb-first,kb-source-of-truth}.md`,
  `.omp/commands/{kb,kb-map,doc,onto-doc}.md`,
  `.omp/skills/{kb-search,kb-curate,mp-grill-with-docs}/SKILL.md`.
- `docs/ops/deploy-ontoship.md`, `docs/plans/README.md`.

Вне scope (зафиксировано, но не делается здесь):

- Релиз v0.2.1 и bump `ref` в каталоге — репо-каталог, отдельный прогон; без него фикс
  не доедет до потребителей.
- KB потребителя `sot-omp-marketplace` (`docs/reference/ontoship-package.md`,
  `docs/services/gitmark-cli/README.md`) — там свой дом.
- Найденные аудитом (2026-09-14) дефекты другого класса: payload ссылается на KB-доки,
  которые плагином не поставляются (`docs/ontology.md`, `docs/reference/acceptance-rounds.md`
  — второго нет и в этом репо, при том что на него ссылается always-on правило
  `acceptance-rounds`); `gitmark inventory`/lint I7 у потребителя не видит команд и
  навыков (`COMMANDS_DIR = ".omp/commands"`, `SKILLS_DIR = ".omp/skills"`); стандарты
  code-review читаются из `.omp/rules/` потребителя. Требуют отдельных планов.

## Constraints

- Скрипт остаётся чистым bash, без новых зависимостей.
- Коды возврата (0/1/2) не меняются.
- Внутри bash-скрипта `skill://` не резолвится — там только файловый резолв (проверено).
- `skill://` резолвится только как аргумент в командной строке, исполняемой omp-bash;
  в присваивании переменной и в человеческой оболочке — нет (проверено).

## Решения (грил 2026-09-14)

- **Симптом или класс** → класс: фиксим и скрипт, и все ссылки на движок в payload;
  deploy-check получает проверку-страж, чтобы класс не вернулся.
- **AGENTS.md** → остаётся проектным; «через корень пакета» относится только к
  `skills/commands/rules/scripts`. Код возврата не меняем; известное следствие
  (свежий потребитель без AGENTS.md → `exit 1`) записано как проектное требование,
  а не поломка пакета.
- **Приёмка** → (a)+(b) в этом ране, (c) — оговоркой.
- **Доставка** → релиз/каталог отдельно, в репо-каталоге.
- **Вакуумный смоук-поиск** → чинится здесь (тот же файл и тот же контракт).
- **Доки этого репо** → минимальная правка runbook здесь, ADR не дублировать.

## Context

- Баг найден при аудите KB `sot-omp-marketplace` (2026-09-14): после переезда на
  «доставка плагинами» (ADR `plugin-delivery`, 2026-09-11) плагин ставится в
  `.omp/plugins/node_modules/ontoship/`, а `deploy-check.sh` смотрит плоский layout.
- Подтверждено запуском в потребителе: `[FAIL] отсутствует` ×4 (`.omp/skills/kb-search/gitmark.py`,
  `.omp/commands/kb.md`, `.omp/commands/onto-doc.md`, `.omp/rules/kb-first.md`),
  падение `gitmark index` (Errno 2), итог `exit 1`.
- Раскладка потребителя: `.omp/` содержит только `plugins/`; плагин — симлинк на
  `~/.omp/plugins/cache/plugins/sot-omp-marketplace___ontoship___0.2.0`; каталог
  объявляет `git-subdir` из `git@github.com:ntin60775/ontoship-omp.git`, `path: ".omp"`,
  `ref: v0.2.0`. HEAD этого репо == `v0.2.0`, рабочая копия скрипта байт-в-байт равна
  установленной — поэтому правка исходника не меняет установленную копию.
- Механизм плана проверен: `$(dirname $0)/..` через симлинк даёт корень плагина
  (`…/node_modules/ontoship`), все четыре файла на месте, движок возвращает хиты.
- `skill://kb-search/gitmark.py` проверен в обоих контекстах (этот репо и потребитель);
  литерал в bash-скрипте — Errno 2; в `G="…"` — Errno 2.
- Скрипт живёт внутри пакета (`<пакет>/scripts/deploy-check.sh`), поэтому корень
  резолвится от собственного пути — без хардкода пути маркетплейса.

## Tickets

Порядок — по зависимостям; `/ship` — строго по одному, последовательно.

1. [01-payload-engine-refs.md](01-payload-engine-refs.md) — ссылки на движок в payload
   на `skill://` — **archived** (влит в `main`, `b571dd6`).
2. [02-deploy-check-rework.md](02-deploy-check-rework.md) — самоотносительный корень,
   проверка-страж, смоук-поиск — **archived** (влит в `main`, `1cae6d2`).
3. [03-runbook-and-kb-sync.md](03-runbook-and-kb-sync.md) — runbook развёртывания и
   KB-синк — **archived** (влит в `main`, `3629862`).
