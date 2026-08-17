---
node_type: service
title: mp-diagnose — hard-bug diagnosis loop
service: _platform
status: active
updated: 2026-08-17
tags: [service, mp-diagnose, diagnosis]
links:
  documents: [../../../.omp/skills/mp-diagnose/SKILL.md]
  relates_to: [../../services/mp-grill-me/README.md]
---

# mp-diagnose — hard-bug diagnosis loop

A discipline for hard bugs and performance regressions: build a tight red/green feedback
loop, reproduce, minimise, hypothesise, instrument — then **report the root cause, don't
fix the code here**. The fix goes through `dev-flow` (`/ship`), so `mp-diagnose` hands the
root cause, minimal repro, and recommended fix to `mp-grill-me` → contract → `/ship`.
