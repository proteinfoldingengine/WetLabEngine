# V1151 — Independent Rebuild Execution

## Status

independent rebuild executed

## Claim Boundary

```text
Model-native independent rebuild only; no physical continuum theorem, no physical gauge symmetry, no continuum GR, no ADM algebra, no Einstein equations, no tensor covariance, and no physical spacetime curvature claim.
```

## Scaffold Return Code

```text
0
```

## Scaffold Summary

```json
{
  "valid_recall": 1.0,
  "invalid_rate": 0.0,
  "invalid_certified": 0,
  "native_rate": 1.0,
  "label_transported_shift_rate": 1.0,
  "raw_shifted_rate": 0.0,
  "time_shuffle_certified": 0,
  "matched_cost_certified": 0,
  "source_event_shuffled_certified": 0,
  "pass_fail": {
    "valid_recall_min": 0.95,
    "invalid_rate_max": 0.0,
    "time_shuffle_certified_max": 0,
    "matched_cost_certified_max": 0,
    "source_event_shuffled_certified_max": 0,
    "raw_shifted_cert_rate_max": 0.05,
    "certification_instability_max": 0
  },
  "passed": true
}
```

## Interpretation

This run executed the blind rebuild scaffold from the written V1150 specification.

It did **not** import the prior V1143/V1144/V1146/V1148 scored CSV outputs.

## Output Files Copied

```json
[
  "all_results.csv",
  "scale_sweep_by_N.csv",
  "by_kind.csv",
  "summary.json"
]
```

## Next

V1152 — Independent Rebuild Closure if passed; Rebuild Failure Audit if failed
