# V309F — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The audit failed the run on validity and numerical integrity. `chosen_regime` is null, `valid_for_interpretation` is false everywhere shown, and the reported AUC is degenerate rather than a real ranking metric. This is a harness repair issue, not interpretable ablation evidence. We should not freeze, because the audit explicitly says the harness needs correction and the next test should repair it before any component ablation.

## Next Version
V310

## Next Objective
Repair the harness so the next run can produce at least one valid regime before ablation. Specifically:
- implement a real AUC or remove AUC from the decision gate if not meaningful
- require a non-null `chosen_regime`
- require `0.20 <= bad_rate <= 0.40`
- require `trigger_rate > 0.05`
- require `phase_counts.bad > 0`
- keep `validity_gate` as a first-class output
- if no valid regime is found, report that as a harness failure and stop before ablation

Do not run component ablation until the harness passes the gate.

## Required Prompt Update

BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

Repair the harness and rerun the smallest useful validation test.

Continue from the current toy-law stack:

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

Do not interpret component ablation unless the harness first produces a valid regime.

---

## Required Objective

Find at least one nondegenerate regime where the harness is interpretable.

A valid regime must satisfy all of the following:

- `chosen_regime` is not null
- `0.20 <= bad_rate <= 0.40`
- `trigger_rate > 0.05`
- `phase_counts.bad > 0`
- `valid_for_interpretation = true`
- the run uses a real metric implementation for any classification score it reports

If the run cannot satisfy these conditions, stop before any ablation and report a harness failure.

---

## Default Next Loop

Run:

# V310 — Harness Repair Validation Test

Question:

Can the harness produce one valid regime with nonzero bad cases and nonzero trigger activity?

Hypothesis:

If the harness is repaired, then at least one seed/regime combination will satisfy the validity gate and produce interpretable scores.

Method:

1. Use a narrower calibration sweep before any ablation.
2. Sweep only the smallest necessary regime window to try to reach:
   - bad_rate in [0.20, 0.40]
   - trigger_rate > 0.05
   - phase_counts.bad > 0
3. Compute a real AUC or omit AUC if not meaningful.
4. Report the full validity gate for the selected regime.
5. If `chosen_regime` remains null, stop and label the run as a harness failure.

Controls:

- fixed seeds
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- all reported numbers must be traceable to stdout or saved JSON

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

If `chosen_regime` is null, the next objective must repair the harness before ablation.

If the last run was a harness failure, the next run should be a narrower calibration test.

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
3. save outputs under `runs/V###/`
4. save report under `reports/V###_report.md`

If code execution is not available:

1. write the runnable Python
2. state clearly that execution was not performed
3. do not invent numerical results
END_LOOP_PROMPT