# V723 Passive-Equivalent Recoverability Audit

## Why V723 exists

V722 confirmed a real counterfactual `k` signal, but the full run was too easy: `adm_z` separated perfectly, and passive burden metrics also separated perfectly. That meant V722 proved that changing restorative capacity changes the whole trajectory, but it did not isolate the restoration-specific law from passive burden.

V723 is the specificity repair.

The scientific goal is now sharper:

> Can active post-perturbation restoration deficit separate recoverability when passive burden is held equivalent?

## Core design

For each pair, V723 creates one shared passive baseline trajectory independent of high/low `k`.

At each probe time, the code branches from the same pre-probe state into two active relaxation assays:

```text
High-k branch: k = 1.0
Low-k branch:  k = 0.35
```

Both branches receive:

```text
same pre-probe state
same perturbation mask
same perturbation amplitude
same relaxation noise
same relaxation window
same target field
```

Only restorative capacity `k` differs.

This means passive burden metrics are the same within each pair by construction:

```text
passive_mean_distance
passive_peak_distance
probe_start_mean
curvature_like_energy
defect_weighted_error
```

The test is whether post-relaxation restoration distance still differs.

## Core observable

```text
adm_z = (restoration_measure - admissible_calibration_mean) / admissible_calibration_std
```

where:

```text
restoration_measure = mean post-perturbation distance to target field
```

Positive `adm_z` means worse restoration than the admissible high-k calibration baseline.

## Physics / systems interpretation

The synthetic field `Omega(x,t)` is an effective recoverability state over a retained atlas. It is not claimed to be spacetime curvature or a GR tensor.

The passive atlas evolves under source, repair, defect, diffusion, background relaxation, and exogenous noise. This creates a burdened state.

The active probe then asks a different question:

> Given the same burdened state, how much corrective response capacity remains?

That is why V723 separates passive burden from active response-transfer capacity.

## Pass condition

A successful V723 result should show:

```text
passive AUC ≈ 0.50 to 0.65
probe_start AUC ≈ 0.50 to 0.65
adm_z AUC meaningfully higher
paired_delta_adm_z > 0 with CI above zero
k-gap ablation collapses toward null as k_low approaches k_high
passive paired deltas approximately zero
```

## Main summary from this run

```json
{
  "version": "V723_PassiveEquivalentRecoverabilityAudit",
  "seed": 723,
  "high_k": 1.0,
  "low_k": 0.35,
  "k_gap": 0.65,
  "damping": 1.0,
  "n_calibration_pairs": 24,
  "n_test_pairs": 36,
  "adm_mean_restoration": 0.4824521317224996,
  "adm_std_restoration": 0.007257813758007652,
  "n_calibration_admissible": 24,
  "passive_mean_distance_mean": 2.2122958460628857,
  "passive_mean_distance_std": 0.0007959950964364551,
  "passive_peak_distance_mean": 2.612437208924829,
  "passive_peak_distance_std": 0.001336617249777442,
  "probe_start_mean_mean": 2.410278511481335,
  "probe_start_mean_std": 0.0347868846680712,
  "mean_curvature_like_energy_mean": 0.2647791791552976,
  "mean_curvature_like_energy_std": 0.0007317963531678777,
  "mean_defect_weighted_error_mean": 0.4146923278683228,
  "mean_defect_weighted_error_std": 2.4701984151069574e-05,
  "full_n": 72,
  "full_n_positive": 36,
  "full_n_negative": 36,
  "full_auc_adm_z": 1.0,
  "full_auc_adm_z_l2": 1.0,
  "full_auc_passive_mean_z": 0.49999999999999994,
  "full_auc_passive_peak_z": 0.49999999999999994,
  "full_auc_probe_start_z": 0.49999999999999994,
  "full_auc_curvature_like_z": 0.49999999999999994,
  "full_auc_defect_weighted_z": 0.49999999999999994,
  "full_f1_adm_z_gt_0.75": 0.9,
  "full_flag_rate_adm_z_gt_0.75": 0.6111111111111112,
  "full_f1_adm_z_gt_1.0": 0.935064935064935,
  "full_flag_rate_adm_z_gt_1.0": 0.5694444444444444,
  "full_f1_adm_z_gt_1.5": 0.972972972972973,
  "full_flag_rate_adm_z_gt_1.5": 0.5277777777777778,
  "full_f1_adm_z_gt_2.0": 0.9863013698630136,
  "full_flag_rate_adm_z_gt_2.0": 0.5138888888888888,
  "delta_passive_mean_distance_mean_abs": 0.0,
  "delta_passive_mean_distance_max_abs": 0.0,
  "delta_passive_peak_distance_mean_abs": 0.0,
  "delta_passive_peak_distance_max_abs": 0.0,
  "delta_probe_start_mean_mean_abs": 0.0,
  "delta_probe_start_mean_max_abs": 0.0,
  "delta_mean_curvature_like_energy_mean_abs": 0.0,
  "delta_mean_curvature_like_energy_max_abs": 0.0,
  "delta_mean_defect_weighted_error_mean_abs": 0.0,
  "delta_mean_defect_weighted_error_max_abs": 0.0,
  "paired_delta_adm_z_mean": 124.53404421597469,
  "paired_delta_adm_z_ci95_low": 123.98704018836135,
  "paired_delta_adm_z_ci95_high": 125.12444274632631,
  "paired_delta_passive_mean_distance_mean": 0.0,
  "paired_delta_passive_mean_distance_ci95_low": 0.0,
  "paired_delta_passive_mean_distance_ci95_high": 0.0,
  "auc_adm_z_ci95_low": 0.9999999999999999,
  "auc_adm_z_ci95_high": 1.0,
  "auc_passive_mean_z_ci95_low": 0.3775957236224742,
  "auc_passive_mean_z_ci95_high": 0.6231771060970278,
  "specificity_gap_auc_adm_minus_passive_mean": 0.5
}
```

## K-gap ablation

|   k_low |   k_gap | shuffled_label_null   |   auc_adm_z |   auc_passive_mean_z |   auc_probe_start_z |   mean_delta_adm_z_low_minus_high |   mean_abs_delta_passive_mean |
|--------:|--------:|:----------------------|------------:|---------------------:|--------------------:|----------------------------------:|------------------------------:|
|    0.2  |    0.8  | False                 |    1        |             0.5      |            0.5      |                          148.904  |                             0 |
|    0.35 |    0.65 | False                 |    1        |             0.5      |            0.5      |                          106.391  |                             0 |
|    0.5  |    0.5  | False                 |    1        |             0.5      |            0.5      |                           71.5337 |                             0 |
|    0.7  |    0.3  | False                 |    1        |             0.5      |            0.5      |                           36.0384 |                             0 |
|    0.85 |    0.15 | False                 |    1        |             0.5      |            0.5      |                           16.0833 |                             0 |
|    1    |    0    | True                  |    0.285714 |             0.514286 |            0.285714 |                            0      |                             0 |

## Damping / observation-window sweep

|   damping |   effective_window_relax_steps_over_damping |   auc_adm_z |   auc_passive_mean_z |   auc_probe_start_z |   mean_delta_adm_z_low_minus_high |   mean_abs_delta_passive_mean |
|----------:|--------------------------------------------:|------------:|---------------------:|--------------------:|----------------------------------:|------------------------------:|
|      0.5  |                                          36 |           1 |                  0.5 |                 0.5 |                          120.319  |                             0 |
|      0.75 |                                          24 |           1 |                  0.5 |                 0.5 |                          147.912  |                             0 |
|      1    |                                          18 |           1 |                  0.5 |                 0.5 |                          152.24   |                             0 |
|      1.5  |                                          12 |           1 |                  0.5 |                 0.5 |                          140.033  |                             0 |
|      2    |                                           9 |           1 |                  0.5 |                 0.5 |                          124.951  |                             0 |
|      3    |                                           6 |           1 |                  0.5 |                 0.5 |                           96.6207 |                             0 |

## Perturbation-family summary

| perturbation_family   |   n |   mean_delta_post_dist |   median_delta_post_dist |   mean_delta_gain |   max_abs_delta_start |   mean_shock_magnitude |
|:----------------------|----:|-----------------------:|-------------------------:|------------------:|----------------------:|-----------------------:|
| gaussian              |  36 |               0.847733 |                 0.834027 |         -0.847733 |                     0 |               0.119207 |
| multi_site            |  36 |               0.932584 |                 0.933668 |         -0.932584 |                     0 |               0.168538 |
| ring                  |  36 |               0.892618 |                 0.907688 |         -0.892618 |                     0 |               0.164814 |
| sinusoidal            |  36 |               0.933434 |                 0.930762 |         -0.933434 |                     0 |               0.764086 |
| stripe                |  36 |               0.912856 |                 0.909313 |         -0.912856 |                     0 |               0.214264 |

## Outputs

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

## Claim boundary

V723, if positive, supports this narrower and stronger claim:

> In this controlled synthetic retained-atlas assay, active perturbation-response measurement reveals hidden restorative capacity even when passive burden observables are held equivalent.

That is the specificity test V722 did not close.
