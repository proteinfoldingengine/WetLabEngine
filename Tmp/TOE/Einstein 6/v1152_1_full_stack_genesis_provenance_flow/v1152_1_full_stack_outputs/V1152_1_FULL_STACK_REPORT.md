# V1152.1 Full-Stack Genesis Provenance Flow Engine

## Purpose

V1152.1 upgrades the 3D visualization into a computed certification engine.

The prior version visually labeled margins by mode. This version earns margins from:

```text
Ω similarity
+ Genesis Pin
+ source-flow closure
```

## Summary

```json
{
  "document_id": "V1152_1_FULL_STACK_GENESIS_PROVENANCE_FLOW_ENGINE",
  "status": "computed full-stack 3D engine generated",
  "seed": 11521,
  "frames": 90,
  "points": 360,
  "modes": [
    "valid_label_transported",
    "raw_c_only_shift",
    "retained_order_shuffle",
    "source_event_shuffle",
    "valid_prefix_invalid_suffix",
    "geometry_matched_counterfeit",
    "genesis_valid_source_shuffled"
  ],
  "full_certified_modes": [
    "valid_label_transported"
  ],
  "geometry_only_certified_count": 3,
  "genesis_pin_pass_count": 4,
  "closure_certified_count": 1,
  "full_certified_count": 1,
  "invalid_full_certified_count": 0,
  "claim_boundary": "Model-native 3D certification engine; no physical GR/spacetime/Einstein claim."
}
```

## Legitimate Calibration Thresholds

```json
{
  "B_like_mean": 0.39712298988195677,
  "B_like_std": 1.0000001110223025e-09,
  "B_like_threshold": 0.3971229928819571,
  "source_alignment_mean": -0.11545715627259673,
  "source_alignment_std": 1.0000000277555757e-09,
  "source_alignment_min": -0.11545715927259681,
  "flow_alignment_mean": 0.9742538110958202,
  "flow_alignment_std": 1.000000222044605e-09,
  "flow_alignment_min": 0.9742538080958195
}
```

## Metrics

| mode                          |   omega_similarity |   geometry_similarity | omega_certified   | genesis_pin_pass   |   B_like_rms |   source_alignment |   flow_alignment | residual_certified   | source_alignment_certified   | flow_alignment_certified   | closure_certified   | full_certified   |   omega_margin |   genesis_margin |   closure_margin |   dimensionless_margin | registry_matches   | root_matches   | quorum_valid   | append_valid   | circular_bootstrap_detected   |
|:------------------------------|-------------------:|----------------------:|:------------------|:-------------------|-------------:|-------------------:|-----------------:|:---------------------|:-----------------------------|:---------------------------|:--------------------|:-----------------|---------------:|-----------------:|-----------------:|-----------------------:|:-------------------|:---------------|:---------------|:---------------|:------------------------------|
| valid_label_transported       |           1        |              1        | True              | True               |     0.397123 |       -0.115457    |        0.974254  | True                 | True                         | True                       | True                | True             |       1        |                1 |      3.07928e-09 |               0.666667 | True               | True           | True           | True           | False                         |
| raw_c_only_shift              |           0.991386 |              0.961689 | True              | False              |     0.442294 |       -0.249919    |        0.905943  | False                | False                        | False                      | False               | False            |       0.425713 |               -1 |     -1.1646      |              -0.57963  | False              | False          | False          | True           | True                          |
| retained_order_shuffle        |           0.937465 |             -0.794343 | False             | True               |     0.359496 |       -0.107218    |        0.897835  | True                 | True                         | False                      | False               | False            |      -3.16901  |                1 |     -0.0784386   |              -0.74915  | True               | True           | True           | True           | False                         |
| source_event_shuffle          |           0.962907 |              0.998443 | False             | True               |     0.369388 |       -0.000341221 |       -0.0161591 | True                 | True                         | False                      | False               | False            |      -1.47285  |                1 |     -1.01659     |              -0.49648  | True               | True           | True           | True           | False                         |
| valid_prefix_invalid_suffix   |           0.997903 |              0.996556 | True              | False              |     0.321026 |       -0.0307591   |        0.723246  | True                 | True                         | False                      | False               | False            |       0.86017  |               -1 |     -0.257641    |              -0.132491 | True               | True           | True           | False          | False                         |
| geometry_matched_counterfeit  |           0.976701 |              0.998357 | False             | False              |     0.29746  |        0.166868    |       -0.392516  | True                 | True                         | False                      | False               | False            |      -0.553246 |               -1 |     -1.40289     |              -0.985378 | False              | False          | False          | True           | True                          |
| genesis_valid_source_shuffled |           0.964    |              0.998443 | False             | True               |     0.344797 |       -0.0926569   |       -0.580607  | True                 | True                         | False                      | False               | False            |      -1.39997  |                1 |     -1.59595     |              -0.665307 | True               | True           | True           | True           | False                         |

## Certification Stack

```text
1. Ω similarity
   Tests geometry / conformal resemblance.

2. Genesis Pin
   Tests provenance legitimacy:
   pinned registry, pinned root, quorum, append-only chain, no circular bootstrap.

3. Source-flow closure
   Tests whether the source and flow fields remain aligned with the geometry response.

4. Full certification
   full_certified = Ω similarity AND Genesis Pin AND source-flow closure
```

## What Changed from V1152

The `dimensionless_margin` is no longer assigned by mode.

It is computed as an earned score from:

```text
omega_margin
genesis_margin
closure_margin
```

## Claim Boundary

Allowed:

```text
V1152.1 provides a runnable 3D engine where flow trajectories are certified by
computed Ω similarity, Genesis Pin provenance, and source-flow closure.
```

Not allowed:

```text
physical spacetime
physical time
General Relativity
Einstein equations
physical curvature
production cryptographic security
```
