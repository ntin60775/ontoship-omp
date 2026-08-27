---
node_type: service
title: mp-code-review — two-axis code review
service: _platform
status: active
updated: 2026-08-27
tags: [service, mp-code-review, review, standards, spec]
links:
  documents: [../../../.omp/skills/mp-code-review/SKILL.md, ../../../.omp/commands/code-review.md]
  relates_to: [../../services/mp-grill-with-docs/README.md, ../../services/dev-flow/README.md, ../../reference/commands.md]
---

# mp-code-review — two-axis code review

Reviews the diff between `HEAD` and a fixed point the operator names, along two
deliberately separate axes, each run as its own parallel sub-agent:

- **Standards** — conformance to the repo's documented standards (`.omp/rules/`,
  `AGENTS.md`, `CONTEXT.md` vocabulary, `docs/decisions/`) plus a fixed **Fowler smell
  baseline** (12 smells) that applies even when a repo documents nothing. A documented
  repo standard overrides the baseline; every smell is a labelled judgement call, never a
  hard violation.
- **Spec** — faithfulness to the originating **plan contract / ticket** in `docs/plans/`
  (missing requirements, scope creep, wrong implementation). No spec found → the axis
  skips and says so.

The reports are presented side by side and **never merged or reranked across axes**: a
change can follow every standard while implementing the wrong thing, and merging the axes
lets one mask the other.

**Entry point:** the `/code-review` slash command (`.omp/commands/code-review.md`).

## Boundaries

- **Read-only.** It never fixes code — delivery happens only through `/ship`.
- **Ephemeral output.** The report goes to the chat and `.scratch/code-review-<timestamp>.md`,
  not into `docs/`: a review is a session artifact, like the handoff doc.
- **Not the ship gate.** Step 6 of `dev-flow` (independent model over the author's own
  diff) stays a pipeline gate; this skill is the on-demand review of any piece of code.
- **Downstream.** If the operator decides to fix, findings go to `/grilling` → plan
  contract → `/to-tickets` → `/ship`. A durable trap becomes a `gotcha`; a finding that
  contradicts a recorded decision updates that `decision` doc — it is never worked around
  silently.
