---
node_type: ticket
title: Сценарий «с нуля» в runbook и его прогон
service: _platform
status: draft
updated: 2026-09-14
links:
  part_of: [README.md]
  depends_on: [01-init-command.md]
---

# 02: Сценарий «с нуля» в runbook и его прогон

**What to build:** установка «с нуля» описана в runbook и подтверждена прогоном на чистой
папке: от установки плагина до зелёного `deploy-check`.

**Blocked by:** 01 (сценарий опирается на команду инициализации).

- [ ] `docs/ops/deploy-ontoship.md` содержит сценарий: чистая папка → установка плагина →
      инициализация → `/onto-doc` → `deploy-check` `exit 0`
- [ ] Сценарий прогнан на чистой probe-папке: `exit 0`; повторный запуск инициализации —
      no-op
- [ ] Команды в runbook даны так, чтобы их мог выполнить человек: реальные пути, без
      `skill://`
- [ ] `docs/plans/README.md` актуален, `gitmark lint` чистый, индекс пересобран
