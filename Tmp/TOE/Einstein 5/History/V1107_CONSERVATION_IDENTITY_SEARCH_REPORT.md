# V1107 Conservation Identity Search

**Status:** GR-bridge conservation search / no GR claim  
**Purpose:** Search for a discrete continuity-style identity linking source change and curvature-flux divergence.

## Identity Candidate

```text
Δrho + lambda * div(F_curvature) ≈ 0
```

## Overall Results

| mode               |   mean_normalized_R |   mean_abs_R |   mean_abs_global_R |   mean_source_change_norm |   mean_div_flux_norm |
|:-------------------|--------------------:|-------------:|--------------------:|--------------------------:|---------------------:|
| balanced_transport |             1.40347 |     0.120553 |             0.17213 |                   1.54811 |              8.07985 |
| local_permutation  |             1.15864 |     0.23319  |             0.29353 |                   3.07794 |              7.54243 |
| value_mutation     |             1.17633 |     0.347462 |             7.66837 |                   4.52309 |              8.31994 |

## Comparison

```json
{
  "local_permutation_normR": 1.1586419379881987,
  "balanced_transport_normR": 1.40346614971548,
  "value_mutation_normR": 1.1763276821392832,
  "transport_vs_mutation_advantage": -0.2271384675761967,
  "permutation_vs_mutation_advantage": 0.01768574415108448
}
```

## Interpretation

```text
A lower normalized residual for admissible or balanced transport updates supports a conservation-like bridge; otherwise the conservation criterion remains open.
```

## Scientific Meaning

This targets the weakest bridge criterion:

```text
conservation / Bianchi-like residual closure
```

It does not claim a Bianchi identity. It checks whether a continuity-like toy residual closes better for admissible recoverability updates.

## Claim Boundary

```text
Continuity-residual toy search only; no Bianchi identity, Einstein equation, or GR claim.
```

## Next Step

```text
V1108 — Conservation Criterion Status Update
```
