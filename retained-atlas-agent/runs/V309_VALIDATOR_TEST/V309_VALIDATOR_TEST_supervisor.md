# V309_VALIDATOR_TEST — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The run did **not** produce a valid controller-comparison regime. The audit says the validity gate was not broadly satisfied, and the results show the candidate regimes were still degenerate:
- `bad_rate_range = false` for the shown candidates
- `trigger_rate = 0.0` for the shown candidates
- `horizon_width = 0.0`, `horizon_area = 0.0` for the shown candidates
- `balanced_accuracy = 0.5` for the shown candidates

One narrow candidate earlier appeared valid in the report, but the audit correctly warns that the broader run is not a clean validation and that the controller comparison is not actually demonstrated from the provided results. This is a harness/regime-finding issue, not evidence to promote any controller law.

Per the hard rules: if the validity gate failed or the run is a harness failure, do **not** freeze. Branch is the correct choice.

## Next Version
V309_CLEAN

## Next Objective
Repair the harness/reporting path by restricting to a **single valid nondegenerate regime** and requiring an explicit controller comparison output before any ablation.

If the next run still cannot produce:
- nonzero horizon metrics,
- non-saturated trigger rates,
- valid comparison rows,

then stop the branch rather than adding metrics.

## Required Prompt Update
BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

You are continuing from V309_CLEAN.

Do **not** promote any controller result from V309 unless the run contains a clearly valid nondegenerate comparison row.
Do **not** reinterpret invalid regimes as evidence.
Do **not** change the V307 law boundary.
Do **not** claim controller validation unless the run shows explicit controller comparison outputs and validity-gate pass conditions.

Current scientific lineage source:
- `current_state.md`
- V307 remains the strongest validated toy-law boundary
- V308 was not sufficient to validate `D_A` as a controller
- V309 found regime-degeneracy problems and did not establish a robust comparison branch

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

Run a narrower validity-repair test for the intervention branch.

Question:
Can the harness produce **one** clearly valid nondegenerate regime with explicit controller comparison rows?

Hypothesis:
If the regime search is narrowed and the validation rules are enforced strictly, then:
- at least one regime will pass the validity gate
- trigger rates will not be saturated at 0 or 1
- at least one horizon metric will be nonzero
- controller comparison rows will be explicit and interpretable

Method:
1. Search only a narrow neighborhood around the current validated band.
2. Keep the baseline protocol fixed.
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
3. save outputs under `runs/V310/`
4. save report under `reports/V310_report.md`

If code execution is not available:
1. write the runnable Python
2. state clearly that execution was not performed
3. do not invent numerical results

---

## V310 Default Objective

Repair the harness by finding one valid nondegenerate regime, then emit explicit controller-comparison rows only for that regime.

If no such regime exists, stop the intervention branch.

REPORT TEMPLATE:
# V310 — Valid Regime Repair Test

## Question
Can the harness produce one clearly valid nondegenerate regime with explicit controller comparison rows?

## Hypothesis
If the regime search is narrowed and validation is enforced strictly, then at least one regime will pass the validity gate and controller rows will be interpretable.

## Method
Search a narrow neighborhood around the current validated band. Preserve the baseline protocol. Require a single valid regime before any controller comparison.

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
Smallest useful next test: determine whether the harness can produce one valid nondegenerate regime before any ablation.

## Guardrail Reminder
If no valid regime exists, stop this branch rather than adding new metrics or reinterpreting invalid rows as evidence.
END_LOOP_PROMPT