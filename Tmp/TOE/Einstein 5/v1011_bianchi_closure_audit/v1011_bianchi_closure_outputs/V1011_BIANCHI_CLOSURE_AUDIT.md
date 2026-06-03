# V1011 Accessibility-Flow Bianchi Closure Audit

## Purpose

This audit supports the Bianchi-like branch without claiming physical GR.

It tests whether a model-native closure diagnostic ties together:

```text
Ω curvature proxy
accessibility flow J = -grad(log A)
retained source balance
Genesis Pin provenance predicate
```

## Core Result

```json
{
  "document_id": "V1011_ACCESSIBILITY_FLOW_BIANCHI_CLOSURE_AUDIT",
  "groups_tested": 40,
  "histories_tested": 280,
  "geometry_only_certified_total": 280,
  "full_certified_total": 80,
  "invalid_geometry_only_certified": 240,
  "invalid_full_certified": 40,
  "legitimate_mean_B_like_rms": 0.06716857129806345,
  "invalid_mean_B_like_rms": 0.0679951052306306,
  "legitimate_mean_provenance_weighted_B_rms": 0.06716857129806345,
  "invalid_mean_provenance_weighted_B_rms": 0.4130395896854014,
  "geometry_matched_invalid_mean_omega_similarity": 0.9999999999995998,
  "pass_condition": {
    "geometry_counterfeits_exist": true,
    "no_invalid_full_certified": false,
    "provenance_weighted_residual_separates": true
  },
  "claim_boundary": "Bianchi-like software closure diagnostic only; no physical GR/Bianchi/tensor claim."
}
```

## By-Kind Results

| kind                         |   n |   mean_omega_similarity |   geometry_only_certified |   genesis_pin_pass |   full_certified |   mean_B_like_rms |   mean_provenance_weighted_B_rms |   mean_G_source_corr |
|:-----------------------------|----:|------------------------:|--------------------------:|-------------------:|-----------------:|------------------:|---------------------------------:|---------------------:|
| append_tampered              |  40 |                       1 |                        40 |                  0 |                0 |         0.0678933 |                        0.481959  |             0.989169 |
| forked_root                  |  40 |                       1 |                        40 |                  0 |                0 |         0.06783   |                        0.481948  |             0.989195 |
| geometry_matched_counterfeit |  40 |                       1 |                        40 |                  0 |                0 |         0.0679056 |                        0.48196   |             0.98917  |
| legitimate                   |  40 |                       1 |                        40 |                 40 |               40 |         0.0671686 |                        0.0671686 |             0.989394 |
| quorum_failed                |  40 |                       1 |                        40 |                  0 |                0 |         0.0679204 |                        0.481962  |             0.989166 |
| self_defined                 |  40 |                       1 |                        40 |                  0 |                0 |         0.0679827 |                        0.48197   |             0.98915  |
| source_shuffled_null         |  40 |                       1 |                        40 |                 40 |               40 |         0.0684387 |                        0.0684387 |             0.989004 |

## Interpretation

This audit separates three layers:

1. Geometry-only certification via Ω similarity.
2. Genesis Pin provenance certification.
3. Bianchi-like closure residual tying geometry proxy to source-flow balance.

The important expected pattern is:

```text
geometry-matched counterfeits can pass Ω similarity,
Genesis Pin rejects illegitimate histories,
and provenance-weighted B-like residual separates legitimate from illegitimate histories.
```

## Claim Boundary

Allowed:

```text
The tested recoverability/accessibility system exhibits a Bianchi-like software closure diagnostic.
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
