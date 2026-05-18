# V724 Stress-Test Recoverability Audit

## Posture

This is an observation-only synthetic assay. It reports measured behavior in the run. It does not claim a universal law, physical theorem, biological law, GR result, or real-world generalization.

## Why V724 exists

V723 held passive burden equivalent and observed that active post-perturbation restoration deficit separated high-restoration and low-restoration branches while passive metrics remained near chance. V724 asks whether that observation survives a harder assay.

## Added stressors

- overlapping high/low restorative-capacity distributions,
- nonlinear restoration saturation,
- reserve fatigue across repeated probes,
- stochastic restoration stalls,
- perturbation-family variation,
- shorter and aliased observation windows.

## Preserved specificity control

For every counterfactual pair, the passive baseline is generated once and shared. Passive mean distance, passive peak distance, probe-start burden, curvature-like energy, and defect-weighted burden are therefore passive-equivalent by construction. Only active relaxation sees the sampled capacity and stress-response terms.

## Main summary

```json
{
  "version": "V724_StressTestRecoverabilityAudit",
  "seed": 724,
  "observation_posture": "controlled synthetic assay; observation-only reporting; no universal claim",
  "stressors": [
    "overlapping_k",
    "nonlinear_saturation",
    "reserve_fatigue",
    "stochastic_stalls",
    "perturbation_families",
    "short_window_sweep"
  ],
  "adm_mean_restoration": 1.4139831419630775,
  "adm_std_restoration": 0.10740419469629502,
  "n_calibration_admissible": 24,
  "test_n": 96,
  "test_n_positive": 48,
  "test_n_negative": 48,
  "test_auc_adm_z": 0.8450520833333333,
  "test_auc_adm_z_l2": 0.8467881944444444,
  "test_auc_passive_mean_z": 0.49999999999999994,
  "test_auc_passive_peak_z": 0.49999999999999994,
  "test_auc_probe_start_z": 0.49999999999999994,
  "test_auc_curvature_like_z": 0.49999999999999994,
  "test_auc_defect_weighted_z": 0.49999999999999994,
  "test_auc_effective_k_z": 0.12847222222222224,
  "test_f1_adm_z_gt_0.75": 0.7058823529411765,
  "test_flag_rate_adm_z_gt_0.75": 0.3854166666666667,
  "test_f1_adm_z_gt_1.0": 0.5675675675675675,
  "test_flag_rate_adm_z_gt_1.0": 0.2708333333333333,
  "test_f1_adm_z_gt_1.5": 0.47761194029850745,
  "test_flag_rate_adm_z_gt_1.5": 0.19791666666666666,
  "test_f1_adm_z_gt_2.0": 0.2807017543859649,
  "test_flag_rate_adm_z_gt_2.0": 0.09375,
  "paired_delta_adm_z_mean": 1.2088911522196408,
  "paired_delta_adm_z_ci95_low": 0.943060076130398,
  "paired_delta_adm_z_ci95_high": 1.4619966979065195,
  "paired_delta_passive_mean_distance_mean": 0.0,
  "paired_delta_passive_mean_distance_abs_max": 0.0,
  "auc_adm_z_ci95_low": 0.7677408854166666,
  "auc_adm_z_ci95_high": 0.9065477108700818,
  "auc_passive_mean_z_ci95_low": 0.38991592871779857,
  "auc_passive_mean_z_ci95_high": 0.6093747021377994,
  "specificity_gap_auc_adm_minus_passive_mean": 0.3450520833333333,
  "mean_high_k_nominal_test": 0.8410266403525269,
  "mean_low_k_nominal_test": 0.6717808918970437,
  "min_high_k_nominal_test": 0.6471220046982237,
  "max_low_k_nominal_test": 0.8563779691055838
}
```

## K-gap stress sweep

|   k_gap_mean |   auc_adm_z |   auc_passive_mean_z |   mean_delta_adm_z |   mean_delta_passive |   n |
|-------------:|------------:|---------------------:|-------------------:|---------------------:|----:|
|         0    |    0.611111 |                  0.5 |           0.120049 |                    0 |  12 |
|         0.1  |    0.75     |                  0.5 |           1.2853   |                    0 |  12 |
|         0.2  |    0.833333 |                  0.5 |           1.8003   |                    0 |  12 |
|         0.35 |    0.944444 |                  0.5 |           3.23187  |                    0 |  12 |

## Observation-window stress sweep

|   relax_steps |   damping |   effective_window |   auc_adm_z |   auc_passive_mean_z |   mean_delta_adm_z |   n |
|--------------:|----------:|-------------------:|------------:|---------------------:|-------------------:|----:|
|             3 |      2.5  |            1.2     |    0.666667 |                  0.5 |           0.325586 |  12 |
|             6 |      1.75 |            3.42857 |    0.777778 |                  0.5 |           0.714693 |  12 |
|            10 |      1.25 |            8       |    0.694444 |                  0.5 |           0.531856 |  12 |
|            14 |      1    |           14       |    0.833333 |                  0.5 |           1.74848  |  12 |

## Perturbation-family summary

| family   |   n |   auc_probe_family_post_z |   mean_post_z_low_minus_high |
|:---------|----:|--------------------------:|-----------------------------:|
| gaussian |  96 |                  0.818576 |                     1.4738   |
| ring     |  96 |                  0.814236 |                     0.640419 |
| stripe   |  96 |                  0.760851 |                     0.780171 |

## Reading guide

- `adm_z` is the held-out restoration deficit standardized from high-k calibration runs.
- Higher `adm_z` means worse post-probe restoration relative to the admissible calibration norm.
- Passive AUC near 0.5 means passive burden did not separate the labels in that assay.
- If `adm_z` remains above passive controls under stress, the observation from V723 is more robust.
- If `adm_z` collapses toward chance under stress, the result identifies a boundary condition rather than a failure.

## Output files

- `summary.json`
- `summary_metrics.csv`
- `audit_log.csv`
- `probe_log.csv`
- `paired_counterfactual_deltas.csv`
- `k_gap_sweep.csv`
- `window_sweep.csv`
- `perturbation_family_summary.csv`
- `adm_z_distribution.png`
- `roc_specificity_comparison.png`
- `paired_delta_adm_z_vs_passive.png`
- `k_gap_sweep.png`
- `window_sweep.png`
