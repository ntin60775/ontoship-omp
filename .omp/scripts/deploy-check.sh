#!/usr/bin/env bash
# Проверка развёртывания пакета OntoShip в текущем проекте.
#   exit 0 — пакет на месте и работает;
#   exit 1 — критические проблемы (фикс обязателен);
#   exit 2 — предупреждения (работает, но есть недочёты).
#
# Работает и в плоской установке (<проект>/.omp/scripts/), и в плагинной
# (<проект>/.omp/plugins/node_modules/<плагин>/scripts/): корень пакета резолвится
# от расположения самого скрипта и не хардкодит раскладку.
set -uo pipefail

# $0 абсолютизируется ДО cd: после смены каталога относительный путь не резолвится.
self="${BASH_SOURCE[0]:-$0}"
case "$self" in
  /*) ;;
  *) self="$PWD/${self#./}" ;;
esac
pkg="$(cd "$(dirname "$self")/.." && pwd)"

root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"; cd "$root"
rc=0

# 1. Ключевые файлы: файлы пакета — от корня пакета, entry point — от корня проекта
for p in "$pkg/skills/kb-search/gitmark.py" "$pkg/commands/kb.md" \
         "$pkg/commands/onto-doc.md" "$pkg/rules/kb-first.md" AGENTS.md; do
  [[ -e "$p" ]] || { echo "[FAIL] отсутствует: $p"; rc=1; }
done

# 2. Страж: payload не должен ссылаться на мёртвый плоский путь движка
stale="$(grep -rl '\.omp/skills/kb-search/gitmark\.py' \
         "$pkg/rules" "$pkg/commands" "$pkg/skills" 2>/dev/null)"
[[ -z "$stale" ]] || {
  echo "[FAIL] мёртвый путь движка в payload (нужен skill://kb-search/gitmark.py):"
  echo "$stale" | sed 's/^/    /'
  rc=1
}

# 3. SQLite: FTS5 обязателен, trigram опционален (деградация заявлена в доках)
check_sqlite() {
  python3 - <<'PY'
import sqlite3, sys
c = sqlite3.connect(':memory:')
try:
    c.execute("CREATE VIRTUAL TABLE t USING fts5(x)")
except sqlite3.OperationalError as e:
    print(f"[FAIL] SQLite без FTS5: {e}"); sys.exit(1)
print("FTS5 OK")
try:
    c.execute("CREATE VIRTUAL TABLE t2 USING fts5(x, tokenize='trigram')")
    print("trigram OK")
except sqlite3.OperationalError:
    print("[WARN] trigram-токенайзер недоступен (опционально, нужен SQLite >= 3.34)")
PY
}
out="$(check_sqlite)" || rc=1
echo "$out"
grep -q '^\[WARN\] trigram' <<<"$out" && { echo "[WARN] fuzzy/substring-поиск будет ограничен"; rc=$((rc==0?2:rc)); }

# 4. Индекс и смоук-поиск: движок берётся из пакета, а index/search работают
#    в корне проекта (cwd). Смоук — в --json: текстовый режим печатает
#    «ничего не найдено» в stdout, и проверка «вывод непустой» была бы вакуумной.
#    Ошибка движка — FAIL; пустой результат — WARN: слова «OntoShip» в KB проекта
#    может не быть вовсе.
engine="$pkg/skills/kb-search/gitmark.py"
python3 "$engine" index || { echo "[FAIL] gitmark index"; rc=1; }
smoke="$(python3 "$engine" search "OntoShip" -k 1 --json 2>/dev/null)"; smoke_rc=$?
smoke_compact="${smoke//[[:space:]]/}"
if (( smoke_rc != 0 )); then
  err="$(python3 "$engine" search "OntoShip" -k 1 2>&1 >/dev/null)"
  echo "[FAIL] смоук-поиск: ${err:-движок завершился с ошибкой}"; rc=1
elif [[ -z "$smoke_compact" || "$smoke_compact" == "[]" ]]; then
  echo "[WARN] смоук-поиск без хитов — слова \"OntoShip\" в KB проекта нет; индекс собран"
  rc=$((rc==0?2:rc))
fi

# 5. Бутстрап KB и gitignore
[[ -d docs ]] || { echo "[WARN] docs/ отсутствует — KB не забутстраплена (запусти /onto-doc)"; rc=$((rc==0?2:rc)); }
if [[ -f .gitignore ]]; then
  for ig in '.gitmark/' '*-map.html' '.scratch/'; do
    grep -Fq -- "$ig" .gitignore || { echo "[WARN] .gitignore: нет строки $ig"; rc=$((rc==0?2:rc)); }
  done
else
  echo "[WARN] .gitignore отсутствует"; rc=$((rc==0?2:rc))
fi

echo "deploy-check: exit=$rc"
exit "$rc"
