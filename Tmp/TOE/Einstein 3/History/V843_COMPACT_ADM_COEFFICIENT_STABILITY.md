# V843 Compact ADM-like Coefficient Stability Audit

## Purpose

V842 supported a compact ADM-like equation pair.

V843 tests whether the compact pair has stable transferable coefficients under leave-one-case-out validation.

## Compact pair tested

```text
H  ~ access_curv + A + K + K²
Mx ~ Jx + ∂τJx + ∇·J
My ~ Jy + ∂τJy + ∇·J
```

## Performance

| constraint | mean R² | min R² | corr |
|---|---:|---:|---:|
| H | 0.896 | 0.869 | 0.948 |
| Mx | 0.845 | 0.825 | 0.936 |
| My | 0.843 | 0.820 | 0.936 |

## Coefficient stability

| constraint | mean coefficient CV | max coefficient CV |
|---|---:|---:|
| H | 0.364 | 1.364 |
| Mx | 0.678 | 1.941 |
| My | 0.156 | 0.391 |

## Coefficients

| constraint | term | mean coef | std coef | abs CV |
|---|---|---:|---:|---:|
| H | A | -0.05649 | 0.00151 | 0.027 |
| H | K | -0.00020 | 0.00028 | 1.364 |
| H | K2 | 0.08127 | 0.00427 | 0.053 |
| H | access_curv | 0.14820 | 0.00175 | 0.012 |
| Mx | J | -0.00004 | 0.00009 | 1.941 |
| Mx | dJ | 0.07947 | 0.00261 | 0.033 |
| Mx | divJ | 0.00517 | 0.00030 | 0.059 |
| My | J | 0.00034 | 0.00013 | 0.391 |
| My | dJ | 0.07853 | 0.00255 | 0.033 |
| My | divJ | 0.00323 | 0.00015 | 0.045 |

## Summary

```text
H mean R²:  0.896
Mx mean R²: 0.845
My mean R²: 0.843

H coefficient CV:  0.364
Mx coefficient CV: 0.678
My coefficient CV: 0.156
```

## Verdict

```text
compact_adm_coefficients_transfer_but_not_frozen
```

## Interpretation

High R² with unstable coefficients means the compact law transfers structurally,
but coefficient normalization/derivation is not frozen yet.
