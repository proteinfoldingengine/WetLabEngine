# V1303 — Momentum Propagation Test

## Status

Completed.

## Purpose

V1302 corrected the earlier setup and showed the normalized momentum primitive selects legitimate transport.

V1303 tests whether that selection propagates across ordered slices.

## Case Summary

| regime                 |   valid_winner_rate |   mean_valid_weight |   mean_ADM_M_residual |   mean_ADM_M_std |   mean_continuity_residual |   mean_continuity_std |   mean_B_like_residual |   mean_flow_coherence |
|:-----------------------|--------------------:|--------------------:|----------------------:|-----------------:|---------------------------:|----------------------:|-----------------------:|----------------------:|
| closure_only           |            0.666667 |            0.290212 |             0.687571  |        0.269978  |                   0.644023 |              0.18781  |              0.0261337 |              0.726926 |
| closure_plus_momentum  |            1        |            0.99987  |             0.155802  |        0.133514  |                   0.426911 |              0.240714 |              0.0194249 |              0.978808 |
| identity_plus_momentum |            1        |            1        |             0.0112171 |        0.0176228 |                   0.349614 |              0.248681 |              0.0194236 |              0.999782 |
| momentum_only          |            1        |            0.99987  |             0.163276  |        0.139965  |                   0.426911 |              0.240714 |              0.0194249 |              0.976709 |

## Interpretation

A strong pass means:

```text
valid path wins
ADM_M residual remains stable across slices
continuity residual remains stable across slices
flow coherence remains nontrivial
```

## Next

V1304 should compare momentum propagation against source-flow/B-like propagation to see whether the two frozen branches can be unified without one swallowing the other.
