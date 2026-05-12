# V308_INTERVENTION_CLEAN — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The intervention comparison was run, but the audit shows the branch is not a controller-validation success:

- `D_A` did not outperform `A_norm`
- `D_A` validity gate failed
- horizon controller was non-informative (`horizon_area = 0.0`, `horizon_width = 0.0`)
- the report mixed valid and invalid rows for interpretation
- no harm occurred, so the comparison does not justify promoting a new controller

This is enough evidence to preserve the current toy-law boundary and freeze the controller branch rather than branch further. `A_norm` remains the controller; `D_A` remains diagnostic.

## Next Version
V309

## Next Objective
Run a narrower calibration/diagnostic test to repair the degenerate horizon/controller regime before any ablation:
- verify whether there exists a regime where horizon metrics are nonzero
- avoid saturated trigger rates
- require held-out seeds
- keep `D_A` as diagnostic only unless it clearly improves control

## Required Prompt Update

BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

You are continuing from V308, but the V308 intervention branch is now frozen as a controller branch.

Do **not** promote `D_A` as the intervention controller on the current evidence.
Do **not** claim horizon control was validated in the last run.
Do **not** interpret invalid rows from the last audit as law evidence.

Current scientific lineage source:
- `current_state.md`
- V307 remains the strongest validated toy-law boundary
- V308 established that the intervention comparison was degenerate for some controllers and did not validate `D_A` as controller

Current central toy law:
- `A_norm(t) = A(t) / A_baseline`
- `D_A = mean(max(0, A_c - A_norm(t)))`

Current calibration:
- `A_c ≈ 0.527`
- `D_c ≈ 0.0388`
- `A_h ≈ 0.10`

Current interpretation boundary:
- `D_A` is a strong toy-level diagnostic law
- `A_norm` remains the controller unless a future valid run shows otherwise
- horizon-area control is currently non-informative in the last regime because horizon metrics were zero

---

## Required Next Objective

Run V309 as a narrower diagnostic/calibration test to repair the degenerate regime before any ablation.

Question:
Can we find a non-saturated regime where at least one horizon metric becomes nonzero and controller comparisons are meaningful?

Hypothesis:
If the regime is adjusted into a less degenerate range, then:
- trigger rates will not saturate at 0 or 1 for all controllers
- horizon metrics may become nonzero for at least some seeds
- `A_norm` and `D_A` may separate more cleanly as controller vs diagnostic

Method:
1. Search a narrower regime around the current validated band rather than changing the law.
2. Keep the same seed family structure, but do not reuse the degenerate comparison unchanged.
3. Report whether horizon width/area remain identically zero.
4. Report whether controller trigger rates are saturated.
5. If a valid non-saturated regime is found, compare only valid rows.
6. If not, stop this branch and preserve the current toy-law boundary.

Controls:
- same baseline protocol
- held-out validation required if any controller comparison is made
- explicit harm accounting
- no threshold tuning after validation without validation metrics
- no component ablation yet
- no claim escalation
- no mixing of invalid and valid rows in interpretation

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

---

## Execution Rule

If code execution is available:
1. write runnable Python
2. run the experiment
3. save outputs under `runs/V309/`
4. save report under `reports/V309_report.md`

If code execution is not available:
1. write the runnable Python
2. state clearly that execution was not performed
3. do not invent numerical results

---

## V309 Default Objective

Test a narrower regime to determine whether the harness can produce:
- nonzero horizon metrics
- non-saturated trigger rates
- valid controller comparison rows

If that fails again, stop this branch rather than adding new metrics.

REPORT TEMPLATE:
# V309 — Narrow Regime Validity Test

## Question
Can we find a non-saturated regime where at least one horizon metric becomes nonzero and controller comparisons are meaningful?

## Hypothesis
If the regime is adjusted into a less degenerate range, then trigger rates will not saturate and horizon metrics may become nonzero for at least some seeds.

## Method
Test a narrower regime near the current validated band. Preserve the baseline protocol. Use held-out validation if a controller comparison becomes meaningful.

## Controls
- same baseline protocol
- held-out validation if applicable
- explicit harm accounting
- no threshold tuning after validation without validation metrics
- no component ablation yet
- no claim escalation

## Results
To be filled by the next run.

## Interpretation
To be filled by the next run.

## Failure / Caveat
To be filled by the next run.

## Decision
continue / stop / branch / freeze

## Next
Smallest useful next test: determine whether the harness can produce a nondegenerate regime before any ablation.

## Guardrail Reminder
If horizon metrics remain zero and trigger rates remain saturated, stop this branch and preserve the current toy-law boundary. Do not reinterpret the failed intervention branch as controller validation.
END_LOOP_PROMPT

## Supervisor Safety Override
Original verdict was `freeze`, but the text described a harness/regime failure or failed validity gate. Per constitution hardening, this was overridden to `branch`.
