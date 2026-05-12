# V310 — Valid Regime Repair Test

Question:
Can the harness produce one clearly valid nondegenerate regime with explicit controller comparison rows?

Hypothesis:
If the regime search is narrowed and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

Method:
1. Search a narrow neighborhood around the current validated band.
2. Preserve the baseline protocol.
3. Require a single selected regime with:
   - `bad_rate > 0`
   - `trigger_rate > 0.05`
   - at least one of `horizon_width` or `horizon_area` nonzero
   - `balanced_accuracy` reported
4. If a valid regime is found, print explicit rows for all controllers:
   - scalar `A_norm` trigger
   - duration-below-`A_c` trigger
   - integrated deficit `D_A` trigger
   - horizon-area trigger
   - combined trigger
5. If no valid regime exists, stop this branch.
6. Do not start ablation unless validity is established first.

Controls:
- same baseline protocol
- held-out validation required before interpreting controller comparisons
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid rows with valid rows in interpretation
- report whether `mean_A_norm` and `min_A_norm` are computed from the normalized time series, not from raw means divided by baseline

Results:
To be filled by the run.

Interpretation:
To be filled by the run.

Failure/Caveat:
To be filled by the run.

Decision:
continue / stop / branch / freeze

Next:
Smallest useful next test: determine whether the harness can produce one valid nondegenerate regime before any ablation.
