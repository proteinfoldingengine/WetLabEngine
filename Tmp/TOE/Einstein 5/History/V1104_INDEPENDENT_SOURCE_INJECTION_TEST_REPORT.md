# V1104 Independent Source Injection Test

**Status:** GR-bridge nontriviality test / no GR claim  
**Purpose:** Test whether an externally injected source field predicts changes in Ω-derived curvature.

## Method

```text
Independent source S is not used to define curvature.
S perturbs retained geometry through a response kernel.
Curvature K is computed only from the resulting Ω-geometry.
Measure ΔK = K_after - K_before.
```

## Trend

| kind          |   amp_vs_deltaK_norm_corr |   source_norm_vs_deltaK_norm_corr |   mean_abs_source_deltaK_corr |   mean_shuffled_corr |   mean_random_corr |
|:--------------|--------------------------:|----------------------------------:|------------------------------:|---------------------:|-------------------:|
| center_delta  |                  0.654654 |                          0.654654 |                      0.581468 |         -0.00119133  |        -0.00074584 |
| two_pole      |                  0.654654 |                          0.654654 |                      0.58763  |         -0.00222683  |        -0.00344167 |
| dipole        |                  0.654654 |                          0.654654 |                      0.594384 |         -0.000604529 |         0.0096048  |
| random_sparse |                  0.648833 |                          0.648833 |                      0.54082  |         -0.0049235   |         0.00285931 |

## Key Metrics

```json
{
  "version": "V1104",
  "title": "Independent Source Injection Test",
  "physics_only": true,
  "purpose": "Test whether an externally injected source field, not used to define curvature, predicts changes in \u03a9-derived curvature proxy.",
  "method": "Independent source S perturbs retained geometry through a response kernel; curvature is computed only from resulting \u03a9-geometry.",
  "mean_source_norm_deltaK_corr": 0.6531985082266801,
  "mean_abs_source_deltaK_corr": 0.5760754759774127,
  "mean_shuffled_corr": -0.002236548429402374,
  "mean_random_corr": 0.0020691518244185317,
  "interpretation": "The source/curvature bridge is stronger if independent source norm predicts curvature change and beats shuffled/random source controls.",
  "claim_boundary": "Independent-source toy test only; no GR, Einstein equation, or physical stress-energy claim."
}
```

## Interpretation

```text
The source/curvature bridge is stronger if independent source norm predicts curvature change and beats shuffled/random source controls.
```

## Scientific Meaning

This directly addresses the V1103 boundary:

```text
source and curvature were previously construction-linked.
```

V1104 separates them by injecting a source field independently and measuring whether Ω-curvature changes track that source.

## Claim Boundary

```text
Independent-source toy test only; no GR, Einstein equation, or physical stress-energy claim.
```

## Next Step

```text
V1105 — Independent Source Bridge Audit
```
