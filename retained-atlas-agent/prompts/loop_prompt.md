# Retained-Atlas Loop Prompt

## Current Task

Run the next retained-atlas loop.

Continue from the current law stack:

- A_norm
- D_A
- horizon_width
- horizon_area
- bad_basin_lock
- late_resilience_dynamics

Current central law:

D_A = mean(max(0, A_c - A_norm(t)))

Current calibration:

- A_c ≈ 0.527
- D_c ≈ 0.0388

Current status:

D_A qualifies as a strong toy law inside the retained-atlas toy model.

---

## Required Objective

Pick the smallest useful next test.

Do not overclaim.

Do not attempt to prove GR.

Test whether the current law stack improves one of:

1. prediction
2. robustness
3. compression
4. intervention
5. failure explanation
6. GR-adjacent geometric credibility

---

## Default Next Loop

If no other instruction is provided, run:

# V308 — Deficit Intervention Threshold Test

Question:

Does triggering repair at D_A > D_c outperform simpler A_norm or horizon-area triggers?

Compare:

1. A_norm trigger
2. D_A trigger
3. horizon_area trigger
4. combined trigger

Report:

- bad_rate
- adaptive_rate
- trigger_rate
- rescued
- harmed
- net_rescue
- severity_reduction
- AUC
- balanced_accuracy

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

---

## Guardrails

Use only toy-model language.

Allowed:

- toy-level emergent law
- reachability geometry
- horizon-like behavior
- future-state accessibility
- GR-adjacent diagnostic

Forbidden:

- proved GR
- recovered Einstein equations
- physical spacetime
- black-hole proof
- quantum gravity proof
- universal law

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
