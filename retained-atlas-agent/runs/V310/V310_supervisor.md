# V310 — Supervisor Decision

## Supervisor Verdict
freeze

## Reason
The audit says the previous decision was not justified: `chosen_regime` stayed null, `valid_for_interpretation` failed, and the harness still did not produce a valid interpretive regime. This is a harness failure, not a branch worth continuing into ablation. Per the rules, we should not freeze only on a validity-gate pass; but here the gate failed and the branch is not yet repairable by interpretation. The right control action is to freeze this branch until the harness is redesigned.

## Next Version
V310E

## Next Objective
Repair the harness with a narrower calibration test that actually varies seeds, uses a correct AUC implementation, and searches for any regime with:
- `chosen_regime != null`
- `valid_for_interpretation = true`
- `trigger_rate > 0.05`
- `phase_counts.bad > 0`

If none exists, report a harness failure and stop before any ablation.

## Required Prompt Update

BEGIN_LOOP_PROMPT
# Retained-Atlas Loop Prompt

## Current Task

Repair the harness with the smallest possible calibration sweep.

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

# V310E — Seed-sensitive harness repair test

Question:

Can the harness produce one valid regime when seeds are actually varied and the scoring metric is computed correctly?

Hypothesis:

If the harness is repaired, then at least one seed/regime combination will satisfy the validity gate and produce interpretable scores.

Method:

1. Use a narrower calibration sweep than before.
2. Vary the actual loop seed in `simulate_regime(sev, bf, nz, seed=seed)`.
3. Use a correct AUC implementation or omit AUC entirely if it is not meaningful.
4. Search only the smallest necessary regime window needed to test validity.
5. Report the full validity gate for the selected regime.
6. If `chosen_regime` remains null, stop and label the run as a harness failure.

Controls:

- fixed seeds, but actually passed into the simulation
- shared simulation code across candidate regimes
- no threshold tuning after validation
- no component ablation unless the validity gate passes
- all reported numbers must be traceable to stdout or saved JSON
- do not reuse a single seed while claiming a seed sweep

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