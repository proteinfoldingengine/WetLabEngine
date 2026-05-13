# V312 — Lab Context Repair Test

Question:
Can the harness, when run in a broader but still controlled neighborhood, produce one valid nondegenerate regime with explicit controller-comparison rows?

Hypothesis:
If the search space is re-centered and validity gates are enforced strictly, at least one regime will satisfy: bad_rate > 0, trigger_rate > 0.05, and horizon_area > 0 or horizon_width > 0, with held-out validation metrics reported.

Method:
1. Search a bounded grid of regimes around the current band using fixed seeds.
2. Preserve the baseline protocol.
3. Compute per-regime metrics and validity metadata.
4. Select at most one regime only if the validity gate passes.
5. If one valid regime exists, emit controller rows for scalar A_norm, duration-below-A_c, D_A, horizon-area, and combined triggers.
6. If no valid regime exists, stop the branch and do not ablate components.

Controls:
- same baseline protocol
- held-out validation required before interpretation
- explicit harm accounting
- no threshold tuning after validation
- no component ablation before validity
- no claim escalation
- no mixing invalid and valid rows in interpretation
- report mean_A_norm and min_A_norm as normalized-series quantities
- if AUC is degenerate or missing, state that plainly in results

Results:
To be filled by execution.

Interpretation:
To be filled by execution.

Failure/Caveat:
To be filled by execution.

Decision:
continue / stop / branch / freeze

Next:
Smallest useful next test: determine whether the harness can produce one valid nondegenerate regime before any controller comparison is interpreted.
