# V1011.1 Full Certification Closure Fix

## Purpose

V1011 showed the right structure but exposed one certification gap:

```text
Genesis Pin certifies provenance.
Ω similarity certifies geometry resemblance.
B-like closure certifies source-flow consistency.
```

The failed V1011 condition happened because `source_shuffled_null` histories used valid pinned provenance. They correctly passed Genesis Pin even though their source fields were shuffled.

That is not a Genesis Pin failure. It proves Genesis Pin is necessary but not sufficient for source-flow closure.

## What I Modified

### Old V1011 certification

```text
full_certified = geometry_only_certified AND genesis_pin_pass
```

### New V1011.1 certification

```text
full_certified =
    geometry_only_certified
    AND genesis_pin_pass
    AND closure_certified
```

where:

```text
closure_certified =
    residual_certified
    AND source_alignment_certified
    AND flow_alignment_certified
```

## Why This Version Uses Alignment

A pure B-like RMS residual was too weak because a shuffled source could still produce a small scalar residual.

The closure gate now checks spatial consistency:

```text
fixed-law residual size
source/geometry alignment
flow/geometry alignment
```

All thresholds are calibrated from legitimate histories only.

## Summary

```json
{
  "document_id": "V1011_1_FULL_CERTIFICATION_CLOSURE_FIX",
  "groups_tested": 40,
  "histories_tested": 280,
  "omega_similarity_threshold": 0.985,
  "legitimate_closure_calibration": {
    "beta0": 0.011192560666947729,
    "beta_source": -0.028337489282260035,
    "beta_divJ": -0.2696461819953865
  },
  "thresholds": {
    "K_SIGMA": 3.0,
    "legitimate_mean_B_like_rms": 0.06933950399678039,
    "legitimate_std_B_like_rms": 0.012781923525336681,
    "B_like_threshold": 0.10768527457279044,
    "legitimate_mean_source_alignment": 0.715659999713241,
    "legitimate_std_source_alignment": 0.04312710388293657,
    "source_alignment_min": 0.5862786880644313,
    "legitimate_mean_flow_alignment": 0.9890006989824516,
    "legitimate_std_flow_alignment": 0.004179190314981443,
    "flow_alignment_min": 0.9764631280375072
  },
  "geometry_only_certified_total": 280,
  "genesis_pin_pass_total": 80,
  "residual_certified_total": 280,
  "source_alignment_certified_total": 48,
  "flow_alignment_certified_total": 280,
  "closure_certified_total": 48,
  "old_full_certified_total": 80,
  "new_full_certified_total": 40,
  "invalid_geometry_only_certified": 240,
  "invalid_old_full_certified": 40,
  "invalid_new_full_certified": 0,
  "legitimate_mean_B_like_rms": 0.06933950399678039,
  "invalid_mean_B_like_rms": 0.07111628102515105,
  "source_shuffled_null_mean_B_like_rms": 0.07250294531285814,
  "source_shuffled_null_mean_source_alignment": 0.017993296959788258,
  "legitimate_mean_source_alignment": 0.715659999713241,
  "source_shuffled_null_old_full_certified": 40,
  "source_shuffled_null_new_full_certified": 0,
  "geometry_matched_invalid_mean_omega_similarity": 0.9999999999995998,
  "pass_condition": {
    "geometry_counterfeits_exist": true,
    "old_certification_has_invalids": true,
    "no_invalid_new_full_certified": true,
    "source_shuffled_null_rejected_by_closure": true,
    "legitimate_histories_preserved": true
  },
  "claim_boundary": "Model-native Bianchi-like closure certification only; no physical GR/Bianchi/tensor claim."
}
```

## By-Kind Results

| kind                         |   n |   mean_omega_similarity |   geometry_only_certified |   genesis_pin_pass |   residual_certified |   source_alignment_certified |   flow_alignment_certified |   closure_certified |   old_full_certified |   new_full_certified |   mean_B_like_rms |   mean_source_alignment |   mean_flow_alignment |   mean_G_source_corr |
|:-----------------------------|----:|------------------------:|--------------------------:|-------------------:|---------------------:|-----------------------------:|---------------------------:|--------------------:|---------------------:|---------------------:|------------------:|------------------------:|----------------------:|---------------------:|
| append_tampered              |  40 |                       1 |                        40 |                  0 |                   40 |                            2 |                         40 |                   2 |                    0 |                    0 |         0.070958  |               0.223984  |              0.989001 |             0.988842 |
| forked_root                  |  40 |                       1 |                        40 |                  0 |                   40 |                            2 |                         40 |                   2 |                    0 |                    0 |         0.0705438 |               0.305936  |              0.989001 |             0.98894  |
| geometry_matched_counterfeit |  40 |                       1 |                        40 |                  0 |                   40 |                            0 |                         40 |                   0 |                    0 |                    0 |         0.0707906 |               0.254539  |              0.989001 |             0.988853 |
| legitimate                   |  40 |                       1 |                        40 |                 40 |                   40 |                           40 |                         40 |                  40 |                   40 |                   40 |         0.0693395 |               0.71566   |              0.989001 |             0.989189 |
| quorum_failed                |  40 |                       1 |                        40 |                  0 |                   40 |                            2 |                         40 |                   2 |                    0 |                    0 |         0.0709492 |               0.237958  |              0.989001 |             0.988838 |
| self_defined                 |  40 |                       1 |                        40 |                  0 |                   40 |                            2 |                         40 |                   2 |                    0 |                    0 |         0.0709532 |               0.207949  |              0.989001 |             0.988849 |
| source_shuffled_null         |  40 |                       1 |                        40 |                 40 |                   40 |                            0 |                         40 |                   0 |                   40 |                    0 |         0.0725029 |               0.0179933 |              0.989001 |             0.988498 |

## Scientific Meaning

The stack is now:

```text
Ω similarity
    geometry resemblance

Genesis Pin
    provenance legitimacy

B-like closure gate
    source-flow consistency
```

The important behavior is:

```text
source_shuffled_null:
    passes Ω similarity
    passes Genesis Pin
    fails source-flow closure
```

That proves the B-like closure diagnostic is not redundant with provenance.

## Claim Boundary

Allowed:

```text
The tested recoverability/accessibility system exhibits a model-native Bianchi-like software closure diagnostic.
```

Not allowed:

```text
physical GR
actual Bianchi identity
Einstein equations
actual ADM constraints
physical spacetime curvature
coordinate-covariant tensor identity
```
