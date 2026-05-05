# ORDER_DISTANCE_FAILURE_ANALYSIS.md

# Order-Distance Failure Analysis
## Diagnostic audit of the failed order-distance embedding seam

## Status
**Failure analysis. The naive embedding route is not supported.**

`ORDER_DISTANCE_EMBEDDING.md` attempted the chain:

\[
e_i\prec e_j
\Rightarrow
L(i,j),N(i,j),D_{\mathrm{eff}},d_{\mathrm{ord}}(i,j)
\Rightarrow
X_{\mathrm{loc}}
\Rightarrow
g_{\mu\nu}^{\mathrm{loc}}.
\]

The verifier result was:

```text
PASS: 0.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 100.0%
```

This file analyzes that failure.

The result should be treated as a real falsification of the naive route, not as a formatting or implementation inconvenience.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Observation**
- **Diagnosis**
- **Failure condition**
- **Patch target**
- **Pivot recommendation**

---

# 1. What failed

## Observation 1
The naive order-distance embedding route failed completely.

The attempted reconstruction was:

\[
d_{\mathrm{ord}}(i,j)
=
N(i,j)^{1/D_{\mathrm{eff}}},
\]

followed by local MDS embedding.

This route assumes that interval-cardinality distances behave enough like a metric distance to support local Euclidean-style embedding.

The verifier contradicted that assumption.

---

# 2. Why the failure matters

## Diagnosis 1
Causal order naturally encodes **timelike comparability**, not ordinary spatial distance.

A pair \(i,j\) is comparable only when one can causally precede the other:

\[
e_i\prec e_j.
\]

But spatial metric reconstruction also requires information about spacelike separation, where events are **incomparable**.

Therefore, an order-distance matrix built only from comparable intervals is structurally incomplete as a local metric distance matrix.

---

# 3. Diagnostic verifier

## Observation 2
A targeted diagnostic was implemented:

```text
order_distance_failure_diagnostic.py
```

Execution log:

```text
order_distance_failure_diagnostic_run.log
```

It checks:

1. comparable-pair density;
2. stability of \(D_{\mathrm{eff}}\);
3. local missingness of the distance matrix;
4. triangle inequality violation rate;
5. MDS Gram-matrix eigenvalue pathology;
6. positive-rank structure.

## Captured diagnostic output

```text
Order-distance failure diagnostic
==================================================
Diagnoses why naive order-distance MDS embedding hard-failed.

comparable_density_median: 0.2148500113606383
D_eff_median: 3.2793851235356826
triangle_violation_rate_median: 0.25
triangle_tested_median: 73.0
local_missingness_median: 0.96875
max_finite_neighbors_median: 147.5
mds_negative_eigen_fraction_median: 0.0
mds_positive_rank_median: 0.0
```

---

# 4. Dominant failure modes

## Diagnosis 2: Partial-order distances are not full metric distances

The causal relation gives distances only on comparable pairs.

Even if \(d_{\mathrm{ord}}\) is meaningful for timelike intervals, it does not directly define distances between spacelike-separated events.

Thus local MDS receives a distance matrix with:
- missing entries,
- artificial fills,
- and nonmetric causal distances.

## Diagnosis 3: Interval cardinality is volume-like, not distance-like

\[
N(i,j)
\]

counts causal volume.

The transformation:

\[
N(i,j)^{1/D_{\mathrm{eff}}}
\]

is a proper-time proxy only for suitable timelike intervals. It is not a general metric distance over arbitrary local neighborhoods.

## Diagnosis 4: MDS is the wrong first embedding method

Classical MDS assumes a symmetric metric distance matrix.

Causal order gives:
- directed order,
- timelike intervals,
- spacelike incomparability,
- and volume/chain statistics.

Therefore MDS is not the right primary reconstruction method unless the missing spacelike sector is supplied.

---

# 5. What is still valid

## Observation 3
The prior files are not invalidated:

- `CAUSAL_ORDER_DERIVATION.md` remains structurally viable.
- `CAUSAL_INTERVAL_GEOMETRY.md` remains useful for interval scaling.
- `ORDER_ONLY_METRIC_RECONSTRUCTION.md` remains useful for order-only time/dimension proxies.

What failed is specifically:

\[
d_{\mathrm{ord}}
\Rightarrow
\text{Euclidean local MDS embedding}.
\]

---

# 6. Correct pivot

## Pivot recommendation 1
Do not continue to `ORDER_EMBEDDED_LORENTZIAN_METRIC.md` using naive MDS.

Instead pivot to:

```text
CAUSAL_SET_RECONSTRUCTION.md
```

The reconstruction route should use causal-set-specific tools:

1. longest-chain length for timelike distance;
2. interval cardinality for volume;
3. antichain structure for spacelike slices;
4. nearest-neighbor relations within antichains for spatial geometry;
5. Myrheim-Meyer dimension or related dimension estimators;
6. sprinkling-density normalization;
7. causal diamonds for local light-cone structure.

---

# 7. Replacement reconstruction chain

## Patch target 1
Replace the failed chain:

```text
order distance -> MDS embedding -> metric
```

with:

```text
causal order
    -> time function / longest chains
    -> antichain spatial slices
    -> interval-volume dimension
    -> spatial adjacency within slices
    -> local Lorentzian reconstruction
```

This is more faithful to causal structure.

---

# 8. New failure conditions

## Failure condition 1
If antichain slices cannot be stably defined, spatial geometry cannot be reconstructed from order alone.

## Failure condition 2
If interval-volume dimension does not stabilize, the causal set is not manifoldlike.

## Failure condition 3
If longest chains fail to approximate timelike distance, causal metric reconstruction fails.

## Failure condition 4
If spatial adjacency within antichains is not recoverable, Lorentzian metric reconstruction requires external coordinates.

---

# 9. Updated status

## Observation 4
The causal-to-metric chain now has a fork:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
ORDER_ONLY_METRIC_RECONSTRUCTION.md
        ↓
ORDER_DISTANCE_EMBEDDING.md  [FAILED]
```

The correct replacement is:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
CAUSAL_SET_RECONSTRUCTION.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
```

---

# 10. Honest status line

> `ORDER_DISTANCE_EMBEDDING.md` produced a genuine hard failure. The naive conversion from interval-cardinality order distances to Euclidean MDS embeddings is not structurally supported. The correct next step is to pivot to causal-set-style reconstruction using chains, antichains, interval volumes, and spatial slice structure.

**End of file.**
