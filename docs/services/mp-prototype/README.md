---
node_type: service
title: mp-prototype — throwaway prototype
service: _platform
status: active
updated: 2026-08-17
tags: [service, mp-prototype, prototype]
links:
  documents: [../../../.omp/skills/mp-prototype/SKILL.md]
  relates_to: [../../services/mp-grill-me/README.md]
---

# mp-prototype — throwaway prototype

Builds a throwaway prototype to answer a design question (logic/state vs UI). It returns
**data and a recommendation** for the decision-maker — it never decides or commits code.
The main branch keeps only the validated decision; `/mp-grill-me` turns the outcome into
a contract, then `/ship`.
