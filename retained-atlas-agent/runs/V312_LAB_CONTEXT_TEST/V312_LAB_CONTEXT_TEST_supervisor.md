# V312_LAB_CONTEXT_TEST — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The run is not a validated controller result, but it is a stable failure branch.

The audit says:
- `execution_validator.py` ran
- `overall_status: pass`
- `interpretation_allowed: true`
- but `valid_for_interpretation: false` for the displayed candidate regimes
- `selected_regime_present: false`
- `valid_controller_row_count: 0`
- `horizon_nonzero: false` everywhere shown

So the branch did not produce interpretable controller evidence, and there is no need to keep pushing the same intervention setup immediately. This is exactly the kind of stable failure that should be frozen rather than retested without a harness change.

This does not change the V307 boundary:
- `D_A` remains a strong toy-level diagnostic law
- `A_norm` remains the controller
- `D_A` is not validated as an intervention controller here

## Next Version
V313_FREEZE

## Next Objective
Freeze the failed intervention branch and preserve the current toy-law boundary.

Smallest useful next test:
- do not rerun intervention comparison yet
- instead, write a new harness only after changing the regime generator so at least one candidate can satisfy:
  - `bad_rate > 0`
  - `trigger_rate > 0.05`
  - `horizon_area > 0` or `horizon_width > 0`
  - `valid_for_interpretation: true`
  - explicit controller rows surviving the gate

If the next branch is opened later, it should start with a narrower calibration repair, not ablation.

## Required Prompt Update
BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

You are continuing from a frozen harness-failure branch after V312.

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
- this branch is now frozen until the harness changes

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
- if every candidate has `horizon_nonzero: false`, stop that search branch after one bounded repair attempt

---

## Required Next Objective

Do not run intervention comparisons on the frozen branch.

Instead, prepare the next loop only if the harness is modified to search a new regime space that can plausibly produce one valid nondegenerate regime.

Question:
Can a modified regime-search harness produce a single valid regime with nonzero failure, nonzero trigger activity, and nonzero horizon metrics?

Hypothesis:
If the regime-generation space is re-centered or broadened correctly, and validity gates are enforced strictly, then at least one regime will satisfy all of:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- at least one of `horizon_width` or `horizon_area` nonzero
- held-out validation metrics reported
- `balanced_accuracy` reported
- `valid_for_interpretation: true`

Method:
1. Do not interpret the frozen V312 outputs as controller evidence.
2. If a new harness is written, search a broader but still controlled neighborhood than the previous run.
3. Keep the baseline protocol fixed.
4. Require per-regime validity metadata.
5. Require one selected regime with:
   - `bad_rate > 0`
   - `trigger_rate > 0.05`
   - `horizon_area > 0` or `horizon_width > 0`
   - `balanced_accuracy` reported
   - `valid_for_interpretation: true`
6. Only if one valid regime exists, emit explicit rows for all controllers:
   - scalar `A_norm` trigger
   - duration-below-`A_c` trigger
   - integrated deficit `D_A` trigger
   - horizon-area trigger
   - combined trigger
7. If no valid regime exists, stop that branch.
8. Do not start ablation unless validity is established first.
9. Do not tune thresholds after seeing results unless the validation protocol is preserved and reported.
10. If every candidate has `horizon_nonzero: false`, treat that as a harness failure and stop the branch after one bounded repair attempt.

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

The frozen branch is not for controller validation.

If a new branch is opened later, its first objective must be to produce one valid nondegenerate regime before any ablation or controller claim.

If no such regime exists after one bounded repair attempt, stop that branch.

REPORT TEMPLATE:
# V313 — Frozen Harness-Failure Branch

## Question
Is the current intervention branch interpretable?

## Hypothesis
A valid controller comparison requires at least one selected regime with nonzero horizon metrics and a passing validity gate.

## Method
Preserve the current toy-law boundary and do not reinterpret invalid rows as evidence.

## Controls
- same baseline protocol
- held-out validation required
- explicit harm accounting
- no component ablation yet
- no claim escalation
- no mixing invalid and valid rows in interpretation

## Results
To be filled by the next run or left empty if no run is performed.

## Interpretation
The branch is frozen because the displayed regimes failed the validity gate and no selected regime survived for interpretation.

## Failure / Caveat
No valid controller-comparison regime was established.

## Decision
freeze

## Next
Smallest useful next test: only after harness repair, search for one valid nondegenerate regime before any controller comparison is interpreted.

## Guardrail Reminder
If no valid regime exists, do not add new metrics or reframe invalid rows as evidence.

END_LOOP_PROMPT

## Supervisor Safety Override
Original verdict was `freeze`, but the text described a harness/regime failure or failed validity gate. Per constitution hardening, this was overridden to `branch`.
