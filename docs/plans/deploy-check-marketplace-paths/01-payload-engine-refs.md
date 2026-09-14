---
node_type: ticket
title: Ссылки на движок в payload — на skill://
service: _platform
status: draft
updated: 2026-09-14
links:
  part_of: [README.md]
---

# 01: Ссылки на движок в payload — на skill://

**What to build:** у потребителя с плагинной установкой правила, команды и навыки пакета
находят gitmark-CLI: любое обращение к движку из payload исполняется, в том числе в
проекте, где плоских копий `.omp/skills/…` нет (потребитель получает только
`commands/ rules/ scripts/ skills/` из кэша плагина).

**Blocked by:** None (can start immediately).

- [ ] В payload (`.omp/rules`, `.omp/commands`, `.omp/skills`) не осталось литерала
      `.omp/skills/kb-search/gitmark.py` — ни в текстах, которые агент исполняет, ни в
      описаниях
- [ ] Каждое обращение к движку идёт как `python3 skill://kb-search/gitmark.py …` —
      URI **аргументом команды**; идиома `G="python3 skill://…"` не используется
      (в присваивании переменной URI не резолвится — проверено запуском)
- [ ] Тексты, которые читает **человек** (README/runbook), реальных путей не теряют:
      `skill://` в них не появляется
- [ ] Прогон в этом репо (плоская установка) и в потребителе с плагином
      (`sot-omp-marketplace`): `/kb`, `/kb-map`, `/doc`, `/onto-doc` и навыки
      `kb-curate`, `mp-grill-with-docs` вызывают движок без Errno 2
- [ ] `gitmark lint` чистый, индекс пересобран
