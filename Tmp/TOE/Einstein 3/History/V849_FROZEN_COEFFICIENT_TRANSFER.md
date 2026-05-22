# V849 Frozen-Coefficient Transfer Test

## Purpose

V848 produced a stable compact ADM-like law candidate.

V849 freezes coefficients from a mixed training set and applies them to unseen regimes without refitting.

## Frozen law

```text
H          ~ ac_n + A_n + K_n + K2_n
M_parallel ~ Jmag + dJ_frame + div_n
M_perp     ~ Jmag + dJ_frame + div_n
```

## Performance

| constraint | mean R² | min R² | corr |
|---|---:|---:|---:|
| H | 0.888 | 0.871 | 0.943 |
| M_parallel | 0.881 | 0.821 | 0.943 |
| M_perp | 0.892 | 0.855 | 0.951 |

## Frozen coefficients

| constraint | term | coefficient |
|---|---|---:|
| H | intercept | -0.293527 |
| H | ac_n | 0.697589 |
| H | A_n | -0.218603 |
| H | K_n | 0.000168 |
| H | K2_n | 0.019050 |
| M_parallel | intercept | 0.061029 |
| M_parallel | Jmag | -0.016372 |
| M_parallel | dJ_frame | 1.142206 |
| M_parallel | div_n | -0.020051 |
| M_perp | intercept | 0.018332 |
| M_perp | Jmag | -0.004896 |
| M_perp | dJ_frame | 1.171787 |
| M_perp | div_n | -0.021543 |

## Case scores

| constraint | case | R² | corr |
|---|---|---:|---:|
| H | standard_s1670 | 0.890 | 0.943 |
| H | standard_s1671 | 0.875 | 0.935 |
| H | radial_s1672 | 0.914 | 0.956 |
| H | shear_s1673 | 0.871 | 0.934 |
| H | counterrot_s1674 | 0.904 | 0.951 |
| H | pulse_s1675 | 0.875 | 0.938 |
| M_parallel | standard_s1670 | 0.845 | 0.924 |
| M_parallel | standard_s1671 | 0.890 | 0.944 |
| M_parallel | radial_s1672 | 0.962 | 0.987 |
| M_parallel | shear_s1673 | 0.947 | 0.981 |
| M_parallel | counterrot_s1674 | 0.821 | 0.912 |
| M_parallel | pulse_s1675 | 0.821 | 0.913 |
| M_perp | standard_s1670 | 0.863 | 0.937 |
| M_perp | standard_s1671 | 0.889 | 0.943 |
| M_perp | radial_s1672 | 0.948 | 0.984 |
| M_perp | shear_s1673 | 0.942 | 0.978 |
| M_perp | counterrot_s1674 | 0.855 | 0.930 |
| M_perp | pulse_s1675 | 0.858 | 0.931 |

## Summary

```text
overall mean R²: 0.887
overall min R²: 0.821
```

## Verdict

```text
frozen_coefficients_transfer_supported
```
