# V722 Paired Counterfactual Response-Geometry Audit

## Purpose

This package fixes the main rigor issue identified in V721: high-k and low-k runs were scientifically meaningful, but not fully paired. V722 turns the experiment into a causal counterfactual audit.

The core design rule is:

```text
Same world.
Same target field.
Same initial condition.
Same passive noise stream.
Same probe masks.
Same perturbation amplitude.
Same relaxation noise.
Only restorative capacity k changes.
```

This is intended to test whether active post-perturbation restoration deficit reveals recoverability better than passive burden alone.

## Scientific posture

This is a first-principles synthetic law-discovery harness. It does not assume the final form of the law is proven. It treats the prior stack as an iterative sequence of observations:

- **V395** observed a control skeleton: reserve/reachability product, dynamic floor, hierarchy, and ablations.
- **V541** expressed observed recoverability behavior in field-geometric form.
- **V713** froze the measurable restoration-deficit observable.
- **V721** introduced active perturbation-response testing and damping/window controls.
- **V722** adds paired counterfactual rigor.

## Core observable

```text
adm_z = (restoration_measure - admissible_calibration_mean) / admissible_calibration_std
```

where:

```text
restoration_measure = mean post-perturbation distance to target field
```

Positive `adm_z` means worse restoration than the admissible baseline.

Calibration is performed using high-k admissible calibration runs only. Held-out test runs are scored against that frozen calibration.

## Physics / systems interpretation

The synthetic field `Omega(x,t)` represents an effective recoverability state over a retained atlas.

The target field `Omega_target` is constructed from internal reserve factors:

```text
M = adaptive margin
R = retained future capacity / memory
L = lineage continuity
C = M * R * L
C_floor = local survivability floor
Omega_target = clipped function of C - C_floor
```

The field evolves under:

```text
dOmega/dt = Source - Repair - Defect + diffusion - background restoration
```

Active probes are inserted at fixed times. After each probe, the system receives a finite relaxation window. The audit asks whether lower restorative capacity `k` leaves a measurable residual restoration deficit even when passive burden is controlled.

The `curvature_like` diagnostic is an operational second-variation measure. It is not a GR curvature tensor.

## What V722 fixes

### 1. Paired counterfactuals

For every pair, the high-k and low-k runs share the exact same generated world and disturbance streams.

### 2. Held-out calibration

Admissible calibration runs define the `adm_z` baseline. Separate held-out test pairs are evaluated.

### 3. Perturbation-family invariance

The audit cycles through five probe families:

- Gaussian bump
- ring perturbation
- stripe perturbation
- multi-site perturbation
- sinusoidal field perturbation

### 4. Null / k-gap ablation

The code sweeps `k_low` toward `k_high`. When `k_low = k_high`, labels are explicitly randomized as a shuffled-label null. A valid signal should degrade toward chance as the gap closes.

### 5. Damping / observation-window sweep

The code sweeps damping and reports an effective observation window:

```text
effective_window ≈ relax_steps / damping
```

This tests whether recoverability observability has a finite-window boundary.

### 6. Bootstrap uncertainty

The main summary includes bootstrap confidence intervals for:

- AUC of `adm_z`
- AUC of passive mean burden
- paired delta `adm_z`

## Expected peer-review result pattern

A strong result has this pattern:

```text
1. Held-out adm_z separates low-k from high-k better than passive burden.
2. Paired delta adm_z is positive with confidence interval above zero.
3. The signal degrades as k_gap approaches zero.
4. The shuffled-label null approaches chance.
5. The signal persists across perturbation families.
6. Damping exposes an observation-window boundary rather than arbitrary failure.
```

A weak result has this pattern:

```text
1. Passive burden metrics match or beat adm_z.
2. Paired delta adm_z overlaps zero.
3. k_gap ablation does not degrade toward null.
4. Perturbation-family results are inconsistent.
5. Damping effects are erratic rather than window-like.
```

## How to run in Colab

Upload `v722_paired_counterfactual_response_geometry_audit.py`, then run:

```bash
python v722_paired_counterfactual_response_geometry_audit.py
```

Optional larger run:

```bash
python v722_paired_counterfactual_response_geometry_audit.py --n_test_pairs 80 --bootstrap_n 1000 --zip
```

Fast smoke test:

```bash
python v722_paired_counterfactual_response_geometry_audit.py --n_grid 32 --n_steps 120 --n_calibration_pairs 8 --n_test_pairs 8 --bootstrap_n 50 --zip
```

## Outputs

```text
v722_paired_counterfactual_outputs/
  audit_log.csv
  probe_log.csv
  matched_passive_control_log.csv
  paired_counterfactual_deltas.csv
  summary.json
  summary.csv
  k_gap_ablation.csv
  damping_window_sweep.csv
  perturbation_family_summary.csv
  adm_z_distribution.png
  paired_delta_adm_z.png
  k_gap_ablation.png
  damping_window_sweep.png
  V722_PEER_REVIEW_README.md
  config.json
```

## Claim boundary

The result, if positive, supports this narrower claim:

> In this controlled synthetic retained-atlas system, active post-perturbation restoration deficit is a stronger recoverability observable than passive burden alone, and the signal survives paired counterfactual controls.

It does not by itself prove a universal physical law. It strengthens the candidate operational law by removing major confounds.
