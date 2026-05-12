# V308_fresh — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The latest run repaired calibration enough to produce one valid regime, but the audit says the stated V308 objective was not actually executed. The run was a narrow calibration sweep, not the required controller/intervention comparison. The audit also flags that `horizon_area` and `horizon_width` were always `0.0`, and that the trigger logic did not compare scalar, deficit, horizon-area, and combined controllers. That means the result is valid as a narrow calibration confirmation, but not valid as V308 intervention evidence.

So: continue the research line, but branch into a true intervention comparison rather than freezing or accepting the current run as completion of V308.

## Next Version
V308_INTERVENTION_CLEAN

## Next Objective
Run the actual V308 controller comparison on the valid regime from the repaired calibration sweep:
- scalar `A_norm` trigger
- `D_A` trigger
- horizon-area trigger
- combined trigger

Use the same seed set and the same baseline protocol. Report:
- baseline bad rate
- treated bad rate
- adaptive rate
- trigger rate
- rescued
- harmed
- net rescue
- severity reduction
- phase counts
- variant-level performance

Do not reinterpret the calibration sweep as an intervention result.

## Required Prompt Update
BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

Run the true V308 intervention comparison on the current valid narrow regime.

Do not return to calibration unless the intervention harness itself fails.

Continue from the current toy-law stack only as a toy diagnostic:

- A_norm
- D_A
- horizon_width
- horizon_area
- bad_basin_lock
- late_resilience_dynamics

Current central toy law:

D_A = mean(max(0, A_c - A_norm(t)))

Current calibration:

- A_c ≈ 0.527
- D_c ≈ 0.0388
- A_h ≈ 0.10

Current status:

The latest narrow calibration sweep produced one valid regime:
- bf = 0.35
- nz = 0.08
- sev = 0.65

That result repaired the null-regime calibration failure, but it did **not** complete the requested V308 intervention comparison.
The audit says the previous run was calibration-only and that controller comparison was not actually performed.

Do not interpret calibration as intervention evidence.
Do not ablate components yet.
Do not overwrite the V307 law boundary.
Do not claim horizon geometry was tested if `horizon_area` and `horizon_width` remain zero across the selected regime.

---

## Required Objective

Evaluate controller behavior on the valid regime using the same seed set and baseline protocol.

Controllers to compare:
1. scalar `A_norm` trigger
2. integrated deficit `D_A` trigger
3. horizon-area trigger
4. combined trigger

The run must report, for each controller:
- baseline bad rate
- treated bad rate
- adaptive rate
- trigger rate
- rescued
- harmed
- net rescue
- severity reduction
- phase counts
- variant-level performance

The run is valid only if it actually simulates controller behavior rather than hardwiring a single trigger rule.

If the intervention harness cannot compare controllers, stop and report a harness failure.

---

## Default Next Loop

Run:

# V308 — Deficit Intervention Threshold Test

Question:

Does triggering full staged repair at `D_A > D_c` outperform scalar `A_norm`, horizon area, and combined triggers on the valid regime?

Hypothesis:

If the deficit law is the better controller, then `D_A` trigger should match or slightly outperform scalar `A_norm` trigger on rescue, with similar or lower harm, across the same seed set.

Method:

1. Use the valid regime:
   - `bf = 0.35`
   - `nz = 0.08`
   - `sev = 0.65`
2. Use the same seed set as the validated regime.
3. Evaluate all four controllers on identical runs.
4. Keep the baseline protocol fixed.
5. Compute harm accounting explicitly.
6. Report baseline and treated outcomes for each controller.
7. If horizon metrics remain zero, say so plainly and treat horizon controller results as diagnostic only.

Controls:

- same seeds across all controller conditions
- same baseline protocol
- explicit harm accounting
- no threshold tuning after validation
- no component ablation
- no claim escalation
- all numbers traceable to stdout or saved JSON
- do not hardwire `trigger = trigger_da` and call it a comparison
- do not report controller results unless they are actually simulated

---

## Required Output Format

Every loop must output:

# V### — Title

## Question

## Hypothesis

## Method

## Controls

## Results

Numbers only where possible.

## Interpretation

## Failure / Caveat

## Decision

continue / stop / branch / freeze

## Next

Smallest useful next test.

If the intervention harness fails, report that directly and stop that branch.
If the intervention harness succeeds, the next step may branch to ablation only after controller comparison is complete.

---

## Guardrails

Use only toy-model language.

Allowed:

- toy-level emergent law
- reachability geometry
- horizon-like behavior
- future-state accessibility
- GR-adjacent diagnostic
- pre-geometric toy diagnostic

Forbidden:

- proved GR
- recovered Einstein equations
- physical spacetime
- black-hole proof
- quantum gravity proof
- universal law

Do not overclaim. Do not narrativize weak evidence. Do not interpret invalid results as law evidence.

---

## Execution Rule

If code execution is available:

1. write runnable Python
2. run the experiment
3. save outputs under `runs/V308/`
4. save report under `reports/V308_report.md`

If code execution is not available:

1. write the runnable Python
2. state clearly that execution was not performed
3. do not invent numerical results

REPORT:
# V308 — Deficit Intervention Threshold Test

## Question
Does triggering full staged repair at `D_A > D_c` outperform scalar `A_norm`, horizon area, and combined triggers on the valid regime?

## Hypothesis
If the deficit law is the better controller, then `D_A` trigger should match or slightly outperform scalar `A_norm` trigger on rescue, with similar or lower harm, across the same seed set.

## Method
Evaluate four controllers on the validated regime:
- scalar `A_norm` trigger
- `D_A` trigger
- horizon-area trigger
- combined trigger

Use the same seed set and the same baseline protocol for all controllers. Report baseline bad rate, treated bad rate, adaptive rate, trigger rate, rescued, harmed, net rescue, severity reduction, and phase counts.

## Controls
- same seeds across all controller conditions
- same baseline protocol
- explicit harm accounting
- no threshold tuning after validation
- no component ablation
- no claim escalation
- all numbers grounded in stdout or saved JSON

## Results
To be filled by the next run.

## Interpretation
To be filled by the next run.

## Failure / Caveat
To be filled by the next run.

## Decision
branch

## Next
Smallest useful next test: run the actual controller comparison on the valid regime and verify whether `D_A` trigger outperforms or at least matches the scalar trigger without increasing harm.

## Guardrail Reminder
If the intervention harness still hardwires one trigger rule or does not simulate controller side-by-side, stop and report a harness failure. Do not ablate components.

END_LOOP_PROMPT