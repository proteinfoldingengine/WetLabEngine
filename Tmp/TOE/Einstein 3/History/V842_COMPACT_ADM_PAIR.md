# V842 Compact ADM-like Equation Pair

## Purpose

V841 showed ADM-like role separation.

V842 tests whether this can be reduced to a compact equation pair:

```text
H  ~ F(access_curv, A)
M_i ~ F(J_i, ∂τJ_i, ∇·J)
```

## Summary

```text
H compact source R²:        0.807
H compact + K R²:           0.878

Mx compact M source R²:     0.846
My compact M source R²:     0.848

Mx minimal M source R²:     0.847
My minimal M source R²:     0.848

best pair feature set:      compact_ADM_pair_with_K
best pair overall R²:       0.859
best pair min R²:           0.823
best pair corr:             0.947
```

## Overall

| feature set | mean R² | min R² | corr |
|---|---:|---:|---:|
| compact_ADM_pair_with_K | 0.859 | 0.823 | 0.947 |
| compact_ADM_pair | 0.834 | 0.748 | 0.935 |
| compact_M_source | 0.824 | 0.703 | 0.930 |
| minimal_M_source | 0.562 | -0.020 | 0.950 |
| compact_H_with_K | 0.298 | -0.067 | 0.400 |
| compact_H_source | 0.275 | -0.062 | 0.388 |

## By constraint

| feature set | constraint | mean R² | min R² | corr |
|---|---|---:|---:|---:|
| compact_ADM_pair_with_K | H | 0.884 | 0.840 | 0.941 |
| compact_H_with_K | H | 0.878 | 0.832 | 0.938 |
| compact_ADM_pair | H | 0.810 | 0.748 | 0.905 |
| compact_H_source | H | 0.807 | 0.748 | 0.903 |
| compact_M_source | H | 0.777 | 0.703 | 0.888 |
| minimal_M_source | H | -0.010 | -0.020 | nan |
| minimal_M_source | Mx | 0.847 | 0.827 | 0.952 |
| compact_M_source | Mx | 0.846 | 0.833 | 0.952 |
| compact_ADM_pair | Mx | 0.845 | 0.833 | 0.952 |
| compact_ADM_pair_with_K | Mx | 0.845 | 0.833 | 0.952 |
| compact_H_source | Mx | 0.014 | -0.062 | 0.174 |
| compact_H_with_K | Mx | 0.013 | -0.067 | 0.174 |
| compact_M_source | My | 0.848 | 0.824 | 0.949 |
| minimal_M_source | My | 0.848 | 0.823 | 0.949 |
| compact_ADM_pair_with_K | My | 0.847 | 0.823 | 0.949 |
| compact_ADM_pair | My | 0.847 | 0.823 | 0.949 |
| compact_H_source | My | 0.005 | -0.020 | 0.087 |
| compact_H_with_K | My | 0.004 | -0.021 | 0.087 |

## Verdict

```text
compact_adm_pair_supported
```
