---
description: Run the OntoShip dev-flow from a plan contract (docs/plans/<slug>.md) or an ad-hoc description — research → spec → worktree → implement → tests → review → dev-tests → prod-tests → ship. Launched only by hand.
---

Drive the change described in `$ARGUMENTS` through the **OntoShip dev-flow**.

## Entry

`$ARGUMENTS` is one of:

1. **A contract path** (`docs/plans/<slug>.md`) — the plan is the spec: collapse
   research/tasks/goal/spec into **verification**, honour its `Constraints`.
2. **An ad-hoc description** — run the full loop.
3. **Empty** — treat the most recent `docs/plans/*.md` as the contract.

**Verification (contract entry):** read the plan; check `Context` is still accurate (code
hasn't drifted since it was written) and update it if not, re-confirming with the operator;
set `status: active`; take `Goal`/`Done`/`Scope` from the file — do not re-derive them. The
operator's hand launch *is* the confirmation.

## The loop

1. **Research** — understand from facts (logs, traces, code); reproduce before fixing.
2. **Tasks** — decompose into tracked tasks.
3. **Goal** — crystallize one clear goal + "done" criterion.
4. **Spec** — write it as markdown in the KB via `kb-curate` (node_type, frontmatter,
   typed links `documents:[src/…]`). Search the KB first (`kb-search`) — don't duplicate.
5. **Isolate** — work in a dedicated `git worktree`.
6. **Implement** — code to the spec.
7. **Tests** — write/adjust unit + E2E.
8. **Independent review** — run an independent model (e.g. Codex CLI, read-only) over the diff.
9. **Dev-tests** — MR + commits into `dev`; run the full suite. Red → fix, don't merge.
10. **Prod-tests** — E2E/smoke against the real prod contour.
11. **Ship** — merge `dev → main` and deploy (build-before-stop + healthcheck-poll).
    Mark the plan contract `status: archived` once merged.

## Stop-points (from the contract's `Constraints`)

- `stop-before-commit` — after review, stop with the uncommitted diff in the worktree;
  commit and everything after wait for the operator's "continue". Default for 1C projects.
- `stop-after-mr` — after opening the MR, stop for the operator's review.
- `no-deploy` — skip the deploy step.

A stop-point is a hard pause: report and wait, never resume on your own.

Keep the gates (tests + independent review). Don't skip the spec — it's the carrier of
knowledge, not a throwaway ticket.
