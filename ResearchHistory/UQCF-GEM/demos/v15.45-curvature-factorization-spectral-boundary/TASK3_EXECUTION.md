# Task 3 execution record

Plan: `docs/superpowers/plans/2026-09-23-v1545-curvature-factorization-spectral-boundary-implementation.md`.
Base: `bb79da3fd78065cf4fc5543eb2d3c3ae58fa2a01`.
Scope: Task 3 only; prior scientific code and spec/plan bytes are unchanged.

## TDD

In a local isolated partial workspace on CPython 3.13.5, the fourteen new
`test_spectral` tests first failed with fourteen assertion failures and zero
errors because the spectral module was absent. Implementation then passed all
fourteen tests. No local access to the original archives is claimed: this
container could not resolve github.com for git clone. Archive integration is
executed in the GitHub runner against the original checkout.

The actual-carrier integration tests compare every coefficient with the
archived matrices, the frozen coefficient routine, and a direction-derived
square chart. Even-period fixtures are expressly not archived physical carriers.
Exact certificate replay, damaged-basis rejection and absence of numerical rank
thresholds are covered by tests. A negative even-size result is retained.

## Rulings

- Approval is scoped to Task 3. Tasks 4–7 are not silently started.
- L6/L8 outcomes were previously exposed; no blinded-holdout claim is permitted.
- The general theorem has an algebraic L>=3 domain, not a carrier-adoption rule.
- `test_spectral_archives.py` is an additional test adapter needed to bind the
  theorem to archived matrices without loading archives in `spectral.py`.
- `TASK3_SPECTRAL.json.gz` is a task-local certificate, not final `RESULTS.json`.
- A focused Task-3 workflow supplements rather than replaces the unchanged
  full Task-1/Task-2 development workflow. Their statuses must be distinguished.
- Final review is an author self-review; no independent reviewer is claimed.

- Complete certificate JSON is losslessly gzip-compressed for transfer; replay
  compares decompressed canonical JSON byte-for-byte, not rounded summaries.

## Self-review

Checked the four-edge coefficient derivation, Fourier zero condition, double
counting of the checkerboard intersection, rational basis independence,
centered dimension, no numeric-label coordinate assumption, frozen file pins,
no physical-source verdict, and preservation of predecessor files. Independent
review of the complete v15.45 branch remains part of its later closeout.

GitHub run/job/head and actual integration results are recorded in PR #56
metadata, avoiding a new scientific commit merely to record a run number.
