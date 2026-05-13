# Build_SDK_Run — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The run is a harness/regime-search failure, not a validated controller result.

The audit says:
- `valid_for_interpretation: false` for all displayed regimes
- `horizon_nonzero: false` everywhere
- `valid_controller_row_count: 0`
- no explicit controller-comparison rows survived the validity gate
- the report contains mild overclaiming about controller validation and “one valid nondegenerate regime,” which is not supported

This means the current V312 branch did not produce interpretable controller evidence. It should not be frozen, because the branch is not stable. It should also not be stopped outright yet, because the failure is diagnostic: the harness is producing candidates, but the gate structure is too strict or the search space is miscentered such that horizon metrics never become nonzero.

## Next Version
V313_REPAIR_HORIZON_REGIME

## Next Objective
Repair the regime-search harness so it can produce at least one valid nondegenerate regime with:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- `horizon_area > 0` or `horizon_width > 0`
- held-out validation metrics reported
- explicit controller comparison rows only after validity passes

If the revised search still yields `horizon_nonzero: false` for all candidates, stop the intervention branch.

## Required Prompt Update
BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

You are continuing from a harness-validity failure after V312.

Do **not** promote any controller result unless the run contains a clearly valid nondegenerate comparison row.
Do **not** reinterpret invalid regimes as evidence.
Do **not** change the V307 law boundary.
Do **not** claim controller validation unless the run shows explicit controller comparison outputs and validity-gate pass conditions.
Do **not** add new metrics to rescue a degenerate search.
Do **not** ablate components until a valid regime exists.

Current scientific lineage source:
- `current_state.md`
- V307 remains the strongest validated toy-law boundary
- V308 and V312 did not validate `D_A` as a controller
- V309 and V310 exposed regime-degeneracy / harness-validity problems
- V311 and V312 failed the validity gate and produced no interpretable controller regime
- no valid controller-comparison branch is established yet

Current central toy law:
- `A_norm(t) = A(t) / A_baseline`
- `D_A = mean(max(0, A_c - A_norm(t)))`

Current calibration:
- `A_c ≈ 0.527`
- `D_c ≈ 0.0388`
- `A_h ≈ 0.10`

Current interpretation boundary:
- `D_A` remains a strong toy-level diagnostic law
- `A_norm` remains the controller unless a future valid run shows otherwise
- horizon-area control is not validated
- invalid regimes must not be used as comparison evidence
- if validity gates fail, output a failure report, not a controller report

---

## Required Next Objective

Repair the harness by producing **one** valid nondegenerate regime before any controller comparison is interpreted.

Question:
Can the regime-search harness produce a single valid regime with nonzero failure and nonzero trigger activity, including nonzero horizon metrics?

Hypothesis:
If the regime-generation space is re-centered or broadened correctly, and validity gates are enforced strictly, then at least one regime will satisfy all of:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- at least one of `horizon_width` or `horizon_area` nonzero
- held-out validation metrics reported
- `balanced_accuracy` reported

Method:
1. Search a broader but still controlled neighborhood than the previous run.
2. Keep the baseline protocol fixed.
3. Require per-regime validity metadata.
4. Require one selected regime with:
   - `bad_rate > 0`
   - `trigger_rate > 0.05`
   - `horizon_area > 0` or `horizon_width > 0`
   - `balanced_accuracy` reported
5. Only if one valid regime exists, emit explicit rows for all controllers:
   - scalar `A_norm` trigger
   - duration-below-`A_c` trigger
   - integrated deficit `D_A` trigger
   - horizon-area trigger
   - combined trigger
6. If no valid regime exists, stop this branch.
7. Do not start ablation unless validity is established first.
8. Do not tune thresholds after seeing results unless the validation protocol is preserved and reported.
9. If every candidate has `horizon_nonzero: false`, treat that as a harness failure and stop the branch after one bounded repair attempt.

Controls:
- same baseline protocol
- held-out validation required before interpreting controller comparisons
- explicit harm accounting
- no component ablation yet
- no claim escalation
- no mixing invalid rows with valid rows in interpretation
- report whether `mean_A_norm` and `min_A_norm` are computed from the normalized time series, not from raw means divided by baseline
- if AUC is missing or hard-coded in degenerate cases, state that plainly
- if no selected regime exists, do not write controller comparison conclusions

---

## Required Loop Structure

Every loop must output:

# V### — Title

Question:
What are we testing?

Hypothesis:
What should happen if the law is real?

Method:
What code/run was executed?

Controls:
What could fool us?

Results:
Numerical results only.

Interpretation:
What the result means inside the toy.

Failure/Caveat:
What did not work?

Decision:
continue / stop / branch / freeze

Next:
smallest useful next test

---

## Guardrails

Use only toy-model language.

Allowed:
- toy-level emergent law
- reachability geometry
- future-state accessibility
- horizon-like behavior
- GR-adjacent diagnostic signal
- pre-geometric toy diagnostic

Forbidden:
- proved GR
- recovered Einstein equations
- physical spacetime
- black-hole proof
- quantum gravity proof
- universal law

Do not overclaim.
Do not narrativize weak evidence.
Do not interpret invalid results as law evidence.
Do not preserve a controller branch without validity gating.

---

## Execution Rule

If code execution is available:
1. write runnable Python
2. run the experiment
3. save outputs under `runs/V313/`
4. save report under `reports/V313_report.md`

If code execution is not available:
1. write the runnable Python
2. state clearly that execution was not performed
3. do not invent numerical results

---

## V313 Default Objective

Find one valid nondegenerate regime, then emit explicit controller-comparison rows only for that regime.

If no such regime exists after the bounded repair attempt, stop the intervention branch.

REPORT TEMPLATE:
# V313 — Repair Horizon Regime

## Question
Can the regime-search harness produce one valid nondegenerate regime with explicit controller comparison rows?

## Hypothesis
If the search space is widened or re-centered and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

## Method
Search a controlled broader neighborhood around the current validated band. Preserve the baseline protocol. Require a single valid regime before any controller comparison.

## Controls
- same baseline protocol
- held-out validation required
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid and valid rows in interpretation

## Results
To be filled by the next run.

## Interpretation
To be filled by the next run.

## Failure / Caveat
To be filled by the next run.

## Decision
continue / stop / branch / freeze

## Next
Smallest useful next test: determine whether the harness can produce one valid nondegenerate regime before any ablation is interpreted.

## Guardrail Reminder
If no valid regime exists, stop this branch rather than adding new metrics or reinterpreting invalid rows as evidence.

REPORT:
# V312 — Repair Horizon Regime

## Supervisor Verdict
branch

## Reason
The run is a harness/regime-search failure, not a validated controller result.

The audit says:
- `valid_for_interpretation: false` for all displayed regimes
- `horizon_nonzero: false` everywhere
- `valid_controller_row_count: 0`
- no explicit controller-comparison rows survived the validity gate
- the report contains mild overclaiming about controller validation and “one valid nondegenerate regime,” which is not supported

This means the current V312 branch did not produce interpretable controller evidence. It should not be frozen, because the branch is not stable. It should also not be stopped outright yet, because the failure is diagnostic: the harness is producing candidates, but the gate structure is too strict or the search space is miscentered such that horizon metrics never become nonzero.

## Next Version
V313_REPAIR_HORIZON_REGIME

## Next Objective
Repair the regime-search harness so it can produce at least one valid nondegenerate regime with:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- `horizon_area > 0` or `horizon_width > 0`
- held-out validation metrics reported
- explicit controller comparison rows only after validity passes

If the revised search still yields `horizon_nonzero: false` for all candidates, stop the intervention branch.

## Required Prompt Update
BEGIN_LOOP_PROMPT
...full markdown prompt...
END_LOOP_PROMPT
