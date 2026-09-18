---
node_type: index
title: Plans — plan contracts + tickets
service: _platform
status: active
updated: 2026-09-18
---

# Plans

`docs/plans/` holds the **plan contracts**. A plan starts as a **file**
`docs/plans/<slug>.md` (`node_type: plan`), written by `mp-grill-with-docs`. When the
operator runs `/to-tickets`, the file is promoted to the **folder form**
`docs/plans/<slug>/`: the contract becomes the folder's `README.md`, and under it live
the **tickets** (`NN-<ticket>.md`, `node_type: ticket`) — tracer-bullet vertical slices,
each declaring the tickets that block it.

- The plan contract is written by `mp-grill-with-docs` (as a file); the tickets by
  `mp-to-tickets` (the only step that creates the folder).
- `/ship` executes **one ticket at a time**, strictly sequential: `/ship <folder>` takes
  the first ticket (by `NN` order) whose `status` is not `archived`. A **file plan** is
  shipped as a single slice: `/ship docs/plans/<slug>.md`.
- Lifecycle: plan `draft → active → archived` (shipped as a single slice, or all
  tickets done); ticket `draft → active → archived` (shipped).

**Очередь исполнения** (2026-09-14). `/ship` запускается вручную, один прогон за раз;
порядок задан рёбрами `depends_on` в самих планах, здесь — сводка:

1. [deploy-check-marketplace-paths/](deploy-check-marketplace-paths/README.md) — **archived**
   (все 3 тикета влиты: `b571dd6`, `1cae6d2`, `3629862`).
2. [payload-refs-undelivered-docs.md](payload-refs-undelivered-docs.md) — **archived**
   (влит в `main`, `2439575`).
3. [registry-and-version-in-consumer/](registry-and-version-in-consumer/README.md) — **archived**
   (оба тикета влиты: `436d88a`, `5ca10ab`, `cc2ce88`).
4. [deploy-check-guard-pycache.md](deploy-check-guard-pycache.md) — багфикс стража
   (`__pycache__` давал ложный FAIL) — **archived** (влит в `main`, `a6237c7`).
5. [kb-docs-vs-plugin-delivery.md](kb-docs-vs-plugin-delivery.md) — **archived**
   (влит в `main`, `9667e52`).
6. [consumer-bootstrap/](consumer-bootstrap/README.md) — **archived** (оба тикета влиты:
   `d476dd4`, `b65bd2b`).
7. [ontology-twin-invariant-i8.md](ontology-twin-invariant-i8.md) — **archived**
   (инвариант I8, влит в `main`, `556529b`; в поставку 0.3.0 не входит).
8. [gitignore-parser.md](gitignore-parser.md) — **draft**, ждёт `/ship`: движок
   индексирует то, что git игнорирует (парсер `.gitignore` теряет правила с путём).
   Баг воспроизведён на 0.4.1, влияние замерено: на `erp-demo` бэкапный каталог давал
   74 % индекса.
9. [i4-truthful-links.md](i4-truthful-links.md) — **draft**: I4 проверяет тело и
   frontmatter `links.*` против файловой системы; S1 — открытый PR #3, дальше S2–S4.

- [i4-truthful-links.md](i4-truthful-links.md) — I4 говорит правду: тело и frontmatter резолвятся против ФС как у читателя, граф и поиск остаются мягкими (по [решению о двух модах](../decisions/link-resolution.md))
- [gitignore-parser.md](gitignore-parser.md) — движок уважает `.gitignore` так же, как git: список файлов от `git ls-files --exclude-standard`, неподдержанное правило — предупреждением, а не молчанием
- [deploy-check-marketplace-paths/](deploy-check-marketplace-paths/README.md) — пути движка при плагинной установке: самоотносительный корень в deploy-check.sh + `skill://` в payload, проверка-страж (папка, 3 тикета)
- [payload-refs-undelivered-docs.md](payload-refs-undelivered-docs.md) — payload не ссылается на KB-доки, которых плагин не везёт: схема приёмки и модель онтологии — файлами в payload
- [registry-and-version-in-consumer/](registry-and-version-in-consumer/README.md) — движок находит команды/навыки пакета (I7 и `inventory` перестают быть вакуумными), версия — из манифеста (папка, 2 тикета)
- [kb-docs-vs-plugin-delivery.md](kb-docs-vs-plugin-delivery.md) — доки репо против ADR доставки: «no marketplace», висячий `ship-1c`, плоские примеры команд
- [deploy-check-guard-pycache.md](deploy-check-guard-pycache.md) — багфикс: страж не должен ловить `__pycache__` в пакете (ложный FAIL)
- [consumer-bootstrap/](consumer-bootstrap/README.md) — установка «с нуля»: идемпотентный управляемый блок в `AGENTS.md`, gitignore, зелёный deploy-check (папка, 2 тикета)
- [ontology-twin-invariant-i8.md](ontology-twin-invariant-i8.md) — инвариант I8: дрейф модели онтологии между проектом и пакетом ловится линтером (ERR в репо-источнике, WARN у потребителя)
- [contract-driven-ship.md](contract-driven-ship.md) — contract-spec: entry skills → hand `/ship` (superseded by the ticket-driven model)
- [plan-file-first.md](plan-file-first.md) — plan file by default; folder + tickets only after `/to-tickets`
- [command-inventory.md](command-inventory.md) — генерируемый реестр команд/навыков (`gitmark inventory` + I7), исключение эфемеры из индекса
- [grill-command-pair.md](grill-command-pair.md) — пара grilling-команд: `/grill` (обычный, оптический вход) + `/grilling` (с доками); зависит от command-inventory
- [grilling-omp-native.md](grilling-omp-native.md) — omp-нативный язык в примитиве `grilling`: поиск фактов — read-only `scout`
