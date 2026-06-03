# V1025 Native Continuity Closure

## Purpose

V1024.1 showed only a weak B_ADM-like gap. V1025 measures the primitive continuity law directly.

## Native Closure

```text
C_native = Δsource + dt * div(J * source)
J = -∇ψ
```

## Summary

```json
{
  "document_id": "V1025_NATIVE_CONTINUITY_CLOSURE",
  "transitions_tested": 1080,
  "legitimate_mean_C_norm": 0.4107443781715948,
  "control_mean_C_norm": 10.364879969443374,
  "legitimate_mean_C_rms": 149.17651569460398,
  "control_mean_C_rms": 0.685001195675709,
  "legitimate_mean_corr_delta_flux": 0.9011880461484345,
  "control_mean_corr_delta_flux": 0.0042721141683898225,
  "pass_conditions": {
    "native_continuity_lower_than_controls": true,
    "native_continuity_near_zero": false,
    "effect_gap": 9.954135591271779
  },
  "claim_boundary": "Native source-continuity closure only; no physical GR/Bianchi/ADM/tensor claim."
}
```

## By-Kind Results

| family          | kind                    |   n |   mean_C_norm |   mean_C_rms |    mean_corr |
|:----------------|:------------------------|----:|--------------:|-------------:|-------------:|
| calibration     | forged_static_control   | 120 |     18.9318   |     0.16493  |  0.0047774   |
| calibration     | legitimate_native       | 120 |      0.41122  |   126.583    |  0.901243    |
| calibration     | source_shuffled_control | 120 |      1.49026  |     1.1101   |  0.010771    |
| holdout_shifted | forged_static_control   | 120 |     16.7514   |     0.147609 |  0.000305244 |
| holdout_shifted | legitimate_native       | 120 |      0.391014 |   104.573    |  0.906376    |
| holdout_shifted | source_shuffled_control | 120 |      1.47627  |     1.11413  |  0.00583685  |
| ood_multi       | forged_static_control   | 120 |     21.9455   |     0.194549 | -0.00280632  |
| ood_multi       | legitimate_native       | 120 |      0.43     |   216.374    |  0.895945    |
| ood_multi       | source_shuffled_control | 120 |      1.59405  |     1.37869  |  0.00674852  |

## Interpretation

This tests whether the ordered accessibility-flow update has an internal conservation-like closure before lifting it to ADM-like H/M branches.

## Claim Boundary

Model-native source-continuity closure only.

Not physical Bianchi identity, not ADM, not GR, not Einstein equations, not tensor covariance.
