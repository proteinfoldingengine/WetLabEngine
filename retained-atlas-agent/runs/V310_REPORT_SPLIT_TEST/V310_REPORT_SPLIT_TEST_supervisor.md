# V310_REPORT_SPLIT_TEST — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The run did not produce a valid nondegenerate regime.  
Audit says validity_gate failed for all displayed candidate regimes, with:
- `bad_rate_range = false`
- `horizon_nonzero = false`
- `phase_counts_bad_gt_0 = false`
- `trigger_rate_gt_0p05 = false`

So the intervention branch is not valid yet, and controller comparison is not scientifically interpretable.  
This is a harness/regime failure, not evidence for controller validation.

## Next Version
V311

## Next Objective
Repair the regime-search harness so it can produce at least one valid nondegenerate regime before any controller comparison or ablation is interpreted.

Minimum requirements for the next run:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- at least one of `horizon_width` or `horizon_area` nonzero
- `balanced_accuracy` reported
- explicit valid/invalid gate status per candidate
- no interpretation of invalid rows

If a valid regime cannot be produced, stop the intervention branch.

## Required Prompt Update
BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

You are continuing from V310 branch repair mode.

Do **not** promote any controller result unless the run contains a clearly valid nondegenerate comparison row.
Do **not** reinterpret invalid regimes as evidence.
Do **not** change the V307 law boundary.
Do **not** claim controller validation unless the run shows explicit controller comparison outputs and validity-gate pass conditions.

Current scientific lineage source:
- `current_state.md`
- V307 remains the strongest validated toy-law boundary
- V308 did not validate `D_A` as a controller
- V309 and V310 exposed regime-degeneracy / harness-validity problems
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

---

## Required Next Objective

Repair the harness by finding **one** valid nondegenerate regime before any controller comparison is interpreted.

Question:
Can the regime-search harness produce a single valid regime with nonzero failure and nonzero trigger activity?

Hypothesis:
If the search space is expanded or re-centered correctly and validity gates are enforced strictly, then at least one regime will satisfy all of:
- `bad_rate > 0`
- `trigger_rate > 0.05`
- at least one of `horizon_width` or `horizon_area` nonzero
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

Controls:
- same baseline protocol
- held-out validation required before interpreting controller comparisons
- explicit harm accounting
- no threshold tuning after validation without metrics
- no component ablation yet
- no claim escalation
- no mixing invalid rows with valid rows in interpretation
- report whether `mean_A_norm` and `min_A_norm` are computed from the normalized time series, not from raw means divided by baseline
- report validity-gate fields for each candidate regime
- if AUC is missing or hard-coded in degenerate cases, state that plainly

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
3. save outputs under `runs/V311/`
4. save report under `reports/V311_report.md`

If code execution is not available:
1. write the runnable Python
2. state clearly that execution was not performed
3. do not invent numerical results

---

## V311 Default Objective

Find one valid nondegenerate regime, then emit explicit controller-comparison rows only for that regime.

If no such regime exists, stop the intervention branch.

REPORT TEMPLATE:
# V311 — Valid Regime Search

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
END_LOOP_PROMPT