# Execution efficiency v1 — baseline and bounded design

Status: **READ-ONLY DELIVERABLES COMPLETE; ENGINEERING IMPLEMENTATION AND PERFORMANCE ACCEPTANCE NOT STARTED.**
Scientific certified base: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Prepared on isolated engineering/uqcf-execution-efficiency branch.
These deliverables complete the earlier immediate promise: an evidence-based performance baseline, bounded orchestration proposal and end-to-end validation DESIGN. They do not claim the later engineering runner workstream is complete.

| File | Purpose |
| --- | --- |
| BASELINE.md | Nine historical run chains, critical paths, runner totals and honest attribution limits |
| timing_baseline.json | Raw per-attempt job/step timestamps, source provenance and calculations |
| PERFORMANCE_CONTRACT.md | Scientific invariants, measurement/evaluation boundary and separate execution gate |
| DECISION_LEDGER.md | Evidence-based bounded changes; prepared-universe chunking deferred |
| PIPELINE_DESIGN.md | Automate approved mechanical successors; inherited/domain overlap under 7+1 cap |
| RUN_STATE_SCHEMA.json | Structural receipt schema; semantic gates still required |
| VALIDATION_DESIGN.md | Prospective tiny end-to-end success/refusal fixture design, UNEXECUTED |
| INDEPENDENT_EFFICIENCY_REVIEW.md | Independent source/evidence/design review after candidate freeze |

No source code, tests, workflows, scientific execution, controlled benchmark or measured speedup is included. The certified v16.54 source and evidence stay unchanged. Future implementation/evaluation needs a frozen bounded protocol and independent review; all scientific/test execution remains on GitHub.

The actual-merge campaign took 48m42s from creation to final job, consuming 99m27s summed runner-job spans. Its slowest domain took 29m41s; inherited work then took 13m18s. The subsequent aggregation run was created 77m57s after final computation. These are observational measurements. The gap cause and internal computation phase costs are unavailable.

A2 proposes automation and scheduling changes only. No new platform, scientific algorithm, prepared-universe distribution or domain change. Reserve one inherited worker and at most seven domain workers, total eight, retain every shard and exact-evidence gate. Proposed benefits must later be measured; the changed scheduling may also delay a domain.

User handoff sources: UQCF_GEM_execution_and_research_handoff.md (2026-10-03) and its detailed revised copy; scientific AGENTS requirements remain authoritative for later execution. The current user explicitly requested completion of the separately promised deliverables while continuing A11 analytically.
