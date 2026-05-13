# V312 — Regenerate Regimes

Question:
Can the regime-search harness produce one valid nondegenerate regime with explicit controller comparison rows?

Hypothesis:
If the search space is widened or re-centered and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

Method:
Run a compact but broadened deterministic search over regime parameters using fixed seeds. Preserve the baseline protocol. For each candidate regime, compute per-seed outcomes and regime-level summaries. Apply a strict validity gate requiring:
- bad_rate > 0
- trigger_rate > 0.05
- horizon_area > 0 or horizon_width > 0
- balanced_accuracy reported
Only if at least one regime is valid, emit explicit controller-comparison rows for:
- scalar A_norm trigger
- duration-below-A_c trigger
- integrated deficit D_A trigger
- horizon-area trigger
- combined trigger
If no valid regime exists, stop this branch and report failure only.

Controls:
- same baseline protocol
- held-out validation required
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid and valid rows in interpretation
- report whether mean_A_norm and min_A_norm are computed from the normalized time series
- if AUC is missing or degenerate, state that plainly
- if no selected regime exists, do not write controller comparison conclusions

Results:
To be produced by the run.

Interpretation:
To be produced by the run.

Failure/Caveat:
To be produced by the run.

Decision:
continue / stop / branch / freeze

Next:
Smallest useful next test: determine whether the harness can produce one valid nondegenerate regime before any ablation is interpreted.

Guardrail Reminder:
If no valid regime exists, stop this branch rather than adding new metrics or reinterpreting invalid rows as evidence.