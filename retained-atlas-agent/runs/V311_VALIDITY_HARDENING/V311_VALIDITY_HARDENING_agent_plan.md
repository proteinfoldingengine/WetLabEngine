# V311 — Validity-Gated Regime Search

Question:
Can the regime-search harness produce one valid nondegenerate regime with explicit controller comparison rows?

Hypothesis:
If the search space is widened or re-centered and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

Method:
Search a controlled broader neighborhood around the current validated band. Preserve the baseline protocol. Require a single valid regime before any controller comparison.

Controls:
- same baseline protocol
- held-out validation required
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid and valid rows in interpretation
- report whether mean_A_norm and min_A_norm are computed from the normalized time series, not from raw means divided by baseline
- if AUC is missing or degenerate, state that plainly

Results:
To be filled by the next run.

Interpretation:
To be filled by the next run.

Failure / Caveat:
To be filled by the next run.

Decision:
continue / stop / branch / freeze

Next:
Smallest useful next test: determine whether the harness can produce one valid nondegenerate regime before any ablation is interpreted.

Guardrail Reminder:
If no valid regime exists, stop this branch rather than adding new metrics or reinterpreting invalid rows as evidence.