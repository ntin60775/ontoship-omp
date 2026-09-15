---
node_type: gotcha
title: Мусор в индексе KB — правило .gitignore с путём движок не видит
service: gitmark-cli
status: archived
updated: 2026-09-15
links:
  documents: [../../.omp/skills/kb-search/gitmark.py]
  depends_on: [../services/gitmark-cli/README.md]
  relates_to: [../plans/gitignore-parser.md]
---

# Мусор в индексе KB: правило `.gitignore` с путём

**Симптом.** `gitmark index` показывает заметно больше файлов, чем в репозитории
документации; `search` выдаёт на верхних позициях копии правил или черновики вместо
живых документов. На `erp-demo` это выглядело так: 154 файла / 835 чанков в индексе,
из них 103 файла / 619 чанков (74 %) — содержимое каталога `.omp/.backup-cutover-…/`,
который git игнорирует.

**Причина.** `parse_gitignore()` в движке — рукописное подмножество `.gitignore`, и
правила с путём оно обрабатывает неверно:

- правило с `/` и **без** хвостового слэша (`.omp/.backup-*`, `drafts/secret.md`,
  `.omp/RULES.md`, `.omp/mcp.json`) **молча отбрасывается** — оно не попадает ни в
  список каталогов, ни в список файлов;
- шаблон каталога с путём (`.omp/plugins/`) сохраняется целиком, а сверка идёт по
  отдельным сегментам пути — одиночный сегмент `plugins` никогда не равен
  `.omp/plugins`, поэтому такие каталоги не исключаются никогда;
- файловые шаблоны сверяются только с базовым именем файла, а не с путём.

Работают только односегментные правила: `build/`, `vendor/`, `.gitmark/`. Их эффект
маскирует баг: на простом репозитории кажется, что `.gitignore` учитывается.

**Обход.** Удалить или вынести за пределы репозитория каталоги, которые git игнорирует,
а движок — нет (бэкапы `.omp/.backup-*`, черновики). Затем `gitmark index`.
Обходной путь не выводится из `.gitignore` и потому не защищает от повторения.

**Проверка, что вас это касается.**

```bash
python3 .omp/plugins/node_modules/ontoship/skills/kb-search/gitmark.py index
python3 - <<'PY'
import sqlite3
c = sqlite3.connect('.gitmark/index.db')
rows = list(c.execute("select path from files where path like '.omp/.backup-%' or path like 'drafts/%'"))
print(f"файлов из игнорируемых каталогов: {len(rows)}")
PY
```

**Устранено в 0.4.2.** Причина ушла вместе с правкой:
[планом gitignore-parser](../plans/gitignore-parser.md) (отгружен): движок берёт список
файлов у `git ls-files --exclude-standard`, а неподдержанные правила фолбэка печатает
предупреждением. Запись оставлена как история: симптомов этого класса больше нет.

**Связанное.** Политика `.gitignore` у потребителей каталога
(`sot-omp-marketplace`, `docs/reference/consumer-repo-layout.md`) опирается на правила
с путём — до релиза правки они для индекса инертны.
