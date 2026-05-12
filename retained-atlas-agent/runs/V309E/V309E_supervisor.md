# V309E — Supervisor Decision

## Supervisor Verdict
branch

## Reason
The audit says `fail`, `chosen_regime` is `null`, and the validity gate did not pass. Under the hard rules, this cannot freeze. The current toy harness still produces only degenerate all-safe regimes in the tested window, so the next run must repair the harness with a narrower calibration test before any ablation.

## Next Version
V310E

## Next Objective
Repair the harness with a narrower calibration sweep that is designed to produce at least one nondegenerate regime with:
- `chosen_regime != null`
- `bad_rate > 0`
- `trigger_rate > 0`
- `phase_counts.bad > 0`
- `valid_for_interpretation = true`

If that cannot be achieved, stop and report harness failure. Do not ablate components yet.

## Required Prompt Update

BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

Repair the harness with a narrower calibration sweep.

Do not do component ablation yet.

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

The last run was a harness failure.
The audit reported `fail`.
`chosen_regime` was `null`.
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
- any reported classification score must use a real metric implementation

If the run cannot satisfy these conditions, stop before any ablation and report a harness failure.

---

## Default Next Loop

Run:

# V310E — Narrow calibration repair test

Question:

Can the harness produce one valid regime when the regime window is narrowed and the scoring metric is computed correctly?

Hypothesis:

If the harness is repaired, then at least one narrow seed/regime combination will satisfy the validity gate and produce interpretable scores.

Method:

1. Use a narrower calibration sweep than before.
2. Vary the actual loop seed in `simulate_regime(sev, bf, nz, seed=seed)`.
3. Use a correct AUC implementation or omit AUC entirely if it is not meaningful.
4. Search only the smallest necessary regime window needed to test validity.
5. Report the full validity gate for the selected regime.
6. If `chosen_regime` remains null, stop and label the run as a harness failure.

Controls:

- actual seed passed into the simulation
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- all reported numbers must be traceable to stdout or saved JSON
- do not reuse a single seed while claiming a seed sweep
- do not widen the sweep until the narrow calibration fails cleanly
- if the last run was a harness failure, keep the next test narrower than the previous sweep

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

REPORT:
# V310E — Narrow calibration repair test

## Question
Can the harness produce one valid regime when the regime window is narrowed and the scoring metric is computed correctly?

## Hypothesis
If the harness is repaired, then at least one narrow seed/regime combination will satisfy the validity gate and produce interpretable scores.

## Method
Run a narrow seed/regime sweep with:
- actual varying seeds passed into `simulate_regime(sev, bf, nz, seed=seed)`
- a smaller parameter window than the previous sweep
- only regimes near the smallest plausible failure boundary
- a correct AUC implementation if labels are nondegenerate
- omission of AUC if labels are degenerate and AUC would be meaningless

Suggested narrow sweep shape:
- severity_grid: 1–3 values around the previous failure boundary
- base_failure_grid: 1–3 values around the previous boundary
- noise_grid: 1–2 values
- seeds: a compact set such as 0–7
- n_steps: the minimum needed for validity checking

The run must report:
- chosen_regime
- bad_rate
- adaptive_rate
- AUC
- balanced_accuracy
- accuracy
- trigger_rate
- rescued
- harmed
- horizon_area
- horizon_width
- pinch
- mean_A_norm
- min_A_norm
- score_mean
- score_var
- late_K
- late_mobility
- late_residual
- phase_counts
- validity_gate

## Controls
- actual varying seeds
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- compact seed-wise summary
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
Smallest useful next test: run a narrower calibration sweep around the previous boundary and verify whether any regime produces nonzero bad cases and nonzero trigger activity.

## Guardrail Reminder
If the new sweep still yields `chosen_regime = null`, stop and report a harness failure. Do not ablate components.

END_LOOP_PROMPT