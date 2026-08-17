---
name: mp-grill-me
description: A relentless interview to sharpen a plan or design, ending in a ship contract. Use when the user wants to stress-test a plan or idea before implementing.
disable-model-invocation: true
---

Run a `/grilling` session. When the frontier is empty and shared understanding is
reached, write the outcome as a **ship contract**:

1. Search the KB first (`python3 .omp/skills/kb-search/gitmark.py search "<topic>"`) — if
   a plan for this topic already exists, edit it, don't duplicate.
2. Create/update `docs/plans/<slug>.md` — `node_type: plan`, `status: draft`, body fields
   `Goal`, `Done`, `Scope`, `Constraints`, `Context`, `Tasks` (see `kb-curate`).
3. Lint + reindex (`gitmark.py lint`, `gitmark.py index`).
4. Report the path and **stop**. Do NOT launch `/ship` — the operator starts it by hand:
   `/ship docs/plans/<slug>.md`.
