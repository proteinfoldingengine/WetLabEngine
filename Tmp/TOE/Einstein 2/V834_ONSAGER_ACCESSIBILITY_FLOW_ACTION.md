# V834 Onsager Accessibility-Flow Action Test

## Purpose

V833 showed the correct action is likely first-order dissipative / Onsager-like, not conservative second-order.

V834 tests a first-order accessibility-flow law:

```text
∂τJ = -aJ - b∇·J - cAJ - d(uJ)
```

and then checks whether the resulting flow source predicts ADM-like momentum.

## Summary

```text
best model: full_first_order
mean M R²: 0.026
min M R²: -0.009
corr: 0.157
mean dJ residual: 0.5138
```

## Overall

| model | mean M R² | min M R² | corr | dJ residual |
|---|---:|---:|---:|---:|
| full_first_order | 0.026 | -0.009 | 0.157 | 0.5138 |
| weighted_onsager | 0.024 | -0.013 | 0.138 | 0.5161 |
| plain_onsager | 0.023 | -0.012 | 0.134 | 0.5167 |

## By constraint

| model | constraint | mean M R² | min M R² | corr | dJ residual |
|---|---|---:|---:|---:|---:|
| full_first_order | Mx | 0.035 | 0.006 | 0.201 | 0.5042 |
| full_first_order | My | 0.016 | -0.009 | 0.114 | 0.5233 |
| plain_onsager | Mx | 0.035 | 0.013 | 0.181 | 0.5071 |
| plain_onsager | My | 0.011 | -0.012 | 0.087 | 0.5263 |
| weighted_onsager | Mx | 0.036 | 0.011 | 0.183 | 0.5064 |
| weighted_onsager | My | 0.012 | -0.013 | 0.094 | 0.5258 |

## Verdict

```text
onsager_first_order_action_partial
```

## Interpretation

If this holds, the formal principle should be dissipative accessibility-flow stationarity rather than conservative Euler-Lagrange stationarity.
