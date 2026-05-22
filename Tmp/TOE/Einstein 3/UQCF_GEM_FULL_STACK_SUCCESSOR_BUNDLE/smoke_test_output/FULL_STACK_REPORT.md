# UQCF-GEM / Recoverability Accessibility Full-Stack Run Report

## Document ID

V832_FULL_STACK_SUCCESSOR_RUNNER_OUTPUT

## Claim Boundary

This run tests ADM-like same-slice constraint analogs in an ordered accessibility-flow simulation.

It does **not** establish Einstein equations, physical GR, physical spacetime curvature, or a continuum theorem.

## Compact Law

```text
H          ~ access_curv + A_n + K_n + K2_n
M_parallel ~ Jmag + dJ_parallel + divJ
M_perp     ~ Jmag + dJ_perp + divJ
```

## Summary

```json
{
  "mean_true_transfer_r2": 0.8618196463500848,
  "true_compat_rms": 0.891944193478451,
  "bad_rotated_compat_rms": 2.8349615229219474,
  "shuffled_compat_rms": 3.106020006864777
}
```

## Verdict

```json
{
  "compact_law_supported": true,
  "bad_frame_falsification_passed": true,
  "shuffled_falsification_passed": true,
  "claim_boundary": "ADM-like same-slice constraint analog only; no GR/Einstein/physical-spacetime claim."
}
```

## Transfer Summary

| model             | target         |   mean_r2 |    min_r2 |   mean_corr |   mean_rms |
|:------------------|:---------------|----------:|----------:|------------:|-----------:|
| bad_rotated_frame | H              |  0.897751 |  0.890044 |  0.947605   |   0.542968 |
| bad_rotated_frame | M_bad_parallel | -0.879847 | -1.21889  |  0.0272518  |   3.33221  |
| bad_rotated_frame | M_bad_perp     | -0.908204 | -1.45179  | -0.0181482  |   3.56278  |
| shuffled_features | H              | -0.607902 | -0.64949  |  0.00660482 |   2.15436  |
| shuffled_features | M_parallel     | -0.903984 | -1.32818  | -0.0133463  |   3.477    |
| shuffled_features | M_perp         | -0.873844 | -1.19291  |  0.00253088 |   3.49041  |
| true_law          | H              |  0.897751 |  0.890044 |  0.947605   |   0.542968 |
| true_law          | M_parallel     |  0.841253 |  0.808944 |  0.920662   |   1.02199  |
| true_law          | M_perp         |  0.846455 |  0.808213 |  0.922941   |   1.01171  |

## Compatibility Summary

| model             |   mean_compat_rms |   max_compat_rms |
|:------------------|------------------:|-----------------:|
| bad_rotated_frame |          2.83496  |          3.0118  |
| shuffled_features |          3.10602  |          3.28816 |
| true_law          |          0.891944 |          1.00417 |

## Resolution Scaling Summary

| model             |   nx_min |   nx_max |   rms_at_lowest_nx |   rms_at_highest_nx |   improvement_low_to_high |   p_no_offset |
|:------------------|---------:|---------:|-------------------:|--------------------:|--------------------------:|--------------:|
| true_law          |       12 |       32 |            1.1394  |            0.936665 |                  0.202732 |      0.214352 |
| bad_rotated_frame |       12 |       32 |            3.32389 |            2.85416  |                  0.469729 |      0.172786 |
| shuffled_features |       12 |       32 |            3.70244 |            3.06363  |                  0.638806 |      0.203323 |

## Successor-AI Instructions

1. Treat this as an empirical bounded-lattice full stack.
2. Do not claim GR or Einstein recovery.
3. Do not add heuristic smoothing terms.
4. If continuing, prioritize:
   - variational formalization
   - boundary/operator analysis
   - non-Cartesian graph/mesh tests
   - spectral or Green-function operators
5. Preserve the ordered-update guardrail: the simulation index is not physical time.
