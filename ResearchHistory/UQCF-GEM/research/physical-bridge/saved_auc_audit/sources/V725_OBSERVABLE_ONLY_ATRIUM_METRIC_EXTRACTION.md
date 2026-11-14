# V725 Observable-Only Atrium Metric Extraction

## Boundary

This is Step 3 only: extract an operational Atrium metric scalar from V723-style passive-equivalent perturbation-response assays.

It does **not** claim a GR metric tensor, Einstein equations, spacetime curvature, or universality.

## Assay

Each counterfactual pair has:

- same passive baseline,
- same pre-probe state,
- same perturbation mask,
- same perturbation amplitude,
- same relaxation noise schedule,
- same target field,
- same observation window,
- only `k` changes.

V723 result carried forward:

```text
passive burden = chance
active restoration = signal
```

V725 asks:

```text
What response geometry is the restoration signal living in?
```

## Extracted components

For each paired run, the script computes:

1. restoration distance,
2. local/global contraction rate,
3. trajectory deviation,
4. response curvature-like second variation,
5. observation-window boundary term,
6. k-dependent metric deformation as an external validation variable only. Direct k is not included in the certified metric.

## Candidate scalar

```text
g_atrium = adm_z
         + 1.50 * contraction_failure
         + 0.75 * trajectory_deviation
         + 0.75 * curvature_second_variation
         + 0.50 * observation_window_boundary
         + 0.25 * metric_strain
```

Where `adm_z` is the restoration-distance deficit normalized against the high-k admissible arm.

## Main result

```text
restoration_distance AUC: 1.000
adm_z AUC:                1.000
g_atrium_observable_only AUC: 0.998
g_atrium_with_k_oracle AUC:   0.999
passive_mean AUC:         0.500
passive_curvature AUC:    0.500
```

Passive-equivalence checks:

```text
max paired passive mean delta:      0
max paired passive curvature delta: 0
mean paired delta g_atrium:         5.532
```

## k-gap ablation

| k_gap | k_low | observable-only AUC | k-oracle AUC | adm_z AUC | passive mean AUC |
|---:|---:|---:|---:|---:|---:|
| 0.80 | 0.10 | 1.000 | 1.000 | 1.000 | 0.500 |
| 0.65 | 0.25 | 0.998 | 0.999 | 1.000 | 0.500 |
| 0.50 | 0.40 | 0.904 | 0.946 | 0.977 | 0.500 |
| 0.30 | 0.60 | 0.597 | 0.701 | 0.771 | 0.500 |
| 0.15 | 0.75 | 0.468 | 0.594 | 0.619 | 0.500 |
| 0.05 | 0.85 | 0.462 | 0.574 | 0.535 | 0.500 |
| 0.00 | 0.90 | 0.500 | 0.500 | 0.500 | 0.500 |

## Monotonic deformation scan

| k_low | k_gap | observable-only AUC | k-oracle AUC | mean paired delta g |
|---:|---:|---:|---:|---:|
| 0.85 | 0.05 | 0.457 | 0.572 | -0.183 |
| 0.75 | 0.15 | 0.488 | 0.600 | -0.049 |
| 0.60 | 0.30 | 0.601 | 0.709 | 0.426 |
| 0.45 | 0.45 | 0.817 | 0.881 | 1.606 |
| 0.30 | 0.60 | 0.988 | 0.994 | 4.190 |
| 0.15 | 0.75 | 1.000 | 1.000 | 11.229 |
| 0.05 | 0.85 | 1.000 | 1.000 | 272.246 |

## Interpretation

V725 cleanly supports this narrow statement:

> A composite response-geometry scalar can be extracted from passive-equivalent perturbation-response runs, separates hidden restorative capacity while passive burden is fixed, changes monotonically with k-dependent restoration capacity without direct k leakage, and collapses to null when the k-gap disappears.

## What remains unproven

V725 does not prove:

- tensor structure,
- coordinate invariance,
- perturbation-family invariance,
- Lyapunov functional derivation,
- GR compatibility,
- Einstein-like dynamics,
- real-world validity.

## Correct next order

```text
V726: Test metric invariance across perturbation families
V727: Derive Lyapunov/energy functional from metric
V728: Only then compare to GR-like structure
```
