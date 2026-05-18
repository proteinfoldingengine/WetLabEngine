# V723 Passive-Equivalent Recoverability Audit

## Purpose

V723 fixes the key specificity gap discovered after V722.

V722 showed that changing restorative capacity `k` creates a real paired counterfactual signal, but it also showed the test was too easy: passive burden metrics separated just as well as `adm_z`.

V723 asks the sharper question:

> Can active perturbation-response measurement reveal hidden restorative capacity when passive burden observables are held equivalent?

## Scientific design

For every pair, V723 generates one shared passive baseline trajectory independent of `k`.

Then, at each probe time, it branches from the exact same pre-probe state into two active relaxation assays:

```text
High-k branch: k = 1.00
Low-k branch:  k = 0.35
```

Both branches share:

```text
same target field
same passive baseline
same pre-probe state
same perturbation mask
same perturbation amplitude
same relaxation noise
same relaxation window
```

Only restorative capacity `k` changes.

This makes the high-k and low-k members passive-equivalent by construction.

## What passive-equivalent means

The following metrics should be identical or near-identical within each pair:

```text
passive_mean_distance
passive_peak_distance
probe_start_mean
mean_curvature_like_energy
mean_defect_weighted_error
```

Those metrics measure burden, not active restoration.

The primary test is whether `adm_z` still separates when those metrics do not.

## Core observable

```text
adm_z = (restoration_measure - admissible_calibration_mean) / admissible_calibration_std
```

where:

```text
restoration_measure = mean post-perturbation distance to target field after relaxation
```

Interpretation:

```text
higher adm_z = worse restoration than admissible baseline
lower adm_z = closer to admissible restoration behavior
```

## Physics / systems interpretation

The synthetic field `Omega(x,t)` represents an effective recoverability state over a retained atlas.

The passive baseline evolves under:

```text
source loading
repair background
defect pressure
diffusion
background relaxation
exogenous noise
```

The active assay then asks:

> Given the same burdened state, how much corrective response capacity remains?

That is the core response-transfer question.

This is not a GR tensor, not a proof of spacetime curvature, and not a universal physical proof. It is a controlled synthetic law-discovery assay for recoverability.

## Pass condition

A successful V723 run should show:

```text
passive_mean_z AUC ≈ 0.50 to 0.65
passive_peak_z AUC ≈ 0.50 to 0.65
probe_start_z AUC ≈ 0.50 to 0.65
adm_z AUC meaningfully higher
paired_delta_adm_z > 0 with CI above zero
paired_delta_passive_mean_distance ≈ 0
k-gap ablation weakens as k_low approaches k_high
null/shuffled-label condition collapses toward chance
```

## Why this is stronger than V722

V722 proved:

```text
changing k changes the system trajectory
```

V723 tests:

```text
active restoration capacity can be detected even when passive burden cannot separate the systems
```

That is the actual restoration-specific law test.

## How to run

```bash
python v723_passive_equivalent_recoverability_audit.py --zip
```

Faster smoke test:

```bash
python v723_passive_equivalent_recoverability_audit.py \
  --n_grid 32 \
  --n_calibration_pairs 8 \
  --n_test_pairs 12 \
  --bootstrap_n 100 \
  --zip
```

Larger run:

```bash
python v723_passive_equivalent_recoverability_audit.py \
  --n_grid 64 \
  --n_calibration_pairs 50 \
  --n_test_pairs 100 \
  --bootstrap_n 1000 \
  --zip
```

## Outputs

The script writes:

```text
v723_passive_equivalent_outputs/
  audit_log.csv
  probe_log.csv
  paired_counterfactual_deltas.csv
  summary.json
  summary.csv
  k_gap_ablation.csv
  damping_window_sweep.csv
  perturbation_family_summary.csv
  adm_z_distribution.png
  paired_delta_adm_z_vs_passive.png
  roc_specificity_comparison.png
  k_gap_ablation.png
  damping_window_sweep.png
  V723_PEER_REVIEW_README.md
  config.json
```

If `--zip` is used, it also creates:

```text
v723_passive_equivalent_outputs.zip
```

## Claim boundary

A positive V723 result supports this specific claim:

> In this controlled synthetic retained-atlas assay, active post-perturbation restoration deficit reveals hidden restorative capacity even when passive burden observables are held equivalent.

That is the specificity gap V722 did not close.
