# ORDER_ONLY_METRIC_RECONSTRUCTION.md

# Order-Only Metric Reconstruction
## Candidate route from causal order alone to distance and metric proxies

## Status
**Live derivation target. First order-only reconstruction pass. Not metric-closed.**

`CAUSAL_INTERVAL_GEOMETRY.md` showed that causal intervals can carry interval-size scaling information, but it still used coordinate-assisted proper time:

\[
\tau_{ij}.
\]

This file attacks the next seam:

\[
(e_i\prec e_j)
\longmapsto
d_{\mathrm{causal}}(i,j),
\quad
D_{\mathrm{eff}},
\quad
g_{\mu\nu}
\]

without assuming external coordinates in the reconstruction.

This file does **not** derive a full metric. It defines the first order-only distance proxies and tests whether they correlate with hidden proper-time structure in synthetic data.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as a completed proof unless explicitly stated.

---

# 1. Goal of this file

A causal order gives only relations:

\[
e_i\prec e_j.
\]

To reconstruct geometry without coordinates, we need order-only quantities such as:

- longest-chain length;
- interval cardinality;
- causal depth;
- dimension estimates from interval scaling;
- neighborhood structure from shared past/future.

The goal is to define the first order-only metric proxies.

---

# 2. Order-only inputs

## Definition 1
Let \(C_{ij}\) be the causal relation matrix:

\[
C_{ij}=1
\quad\Longleftrightarrow\quad
e_i\prec e_j.
\]

No coordinate data is allowed in the reconstruction step.

Coordinates may be used only in synthetic verification as hidden ground truth.

---

# 3. Longest-chain distance

## Definition 2
For comparable events:

\[
e_i\prec e_j,
\]

define the longest-chain length:

\[
L(i,j)
=
\max
\{
n:
e_i\prec e_{k_1}\prec\dots\prec e_{k_n}\prec e_j
\}.
\]

In causal-set theory, longest-chain length is a natural order-only proxy for proper time.

## Failure condition 1
If \(L(i,j)\) does not correlate with physical/proper time in controlled tests, the order-only reconstruction route fails.

---

# 4. Interval-cardinality distance proxy

## Definition 3
Define the interval:

\[
I(i,j)=\{e_k:e_i\prec e_k\prec e_j\}.
\]

Let:

\[
N(i,j)=|I(i,j)|.
\]

If interval volume scales as:

\[
N(i,j)\sim \tau_{ij}^{D},
\]

then an order-only distance proxy is:

\[
d_{\mathrm{ord}}(i,j)
=
N(i,j)^{1/D_{\mathrm{eff}}}.
\]

where \(D_{\mathrm{eff}}\) is estimated from order-only scaling between interval cardinality and longest-chain length.

---

# 5. Effective dimension from order-only scaling

## Definition 4
Estimate dimension from:

\[
\log(N(i,j)+1)
\approx
D_{\mathrm{eff}}\log(L(i,j)+1)+C.
\]

This uses only:
- causal interval size,
- longest-chain length.

## Failure condition 2
If this regression is unstable or produces nonphysical \(D_{\mathrm{eff}}\), order-only dimension reconstruction remains unsupported.

---

# 6. Metric reconstruction target

## Derivation target A
Use order-only distances to reconstruct a local metric candidate.

Possible route:

1. construct order-distance matrix:
   \[
   d_{\mathrm{ord}}(i,j);
   \]

2. select local neighborhoods by causal closeness;

3. embed local neighborhoods using multidimensional scaling or graph embedding;

4. fit local signed metric using causal/time ordering.

This is not implemented yet.

## Failure condition 3
If order-only distance proxies cannot support stable local neighborhoods, metric reconstruction cannot proceed without external coordinates.

---

# 7. Verifier implementation

## Status
**Implemented as `order_only_metric_reconstruction_verifier.py`. Execution log captured.**

The verifier:

1. generates synthetic causal events with hidden coordinates;
2. builds only the causal relation matrix;
3. reconstructs:
   - longest-chain distances,
   - interval cardinalities,
   - order-only dimension proxy,
   - order-only distance proxy;
4. compares order-only proxies to hidden proper-time-like separation only for evaluation.

## Captured verifier output

```text
Order-only metric reconstruction verifier
==================================================
Reconstruction uses only causal relation:
longest-chain distance, interval cardinality, order-distance proxy
Coordinates are used only for hidden evaluation correlation.

PASS: 88.75
SOFT_FAIL: 1.25
HARD_FAIL: 10.0
dim_estimate_median: 3.2651871821498584
order_distance_tau_corr_median: 0.9537979483187051
chain_tau_corr_median: 0.880014698938312
comparable_pairs_median: 11765.5
```

---

# 8. What this file establishes

### Established at current proof level

1. Longest-chain distance is defined as an order-only time proxy.
2. Interval-cardinality distance is defined.
3. Effective dimension can be estimated without directly using coordinates.
4. A verifier tests correlation against hidden proper-time structure.
5. Failure modes are explicit.

### Not yet proved

1. Full local metric reconstruction is not implemented.
2. The order-only dimension estimate is not yet robust enough to claim manifold dimension.
3. The method is tested only on synthetic flat causal data.
4. Curved spacetime and variable density are not tested.
5. The embedding/gauge problem remains open.

---

# 9. Theorem candidate

## Theorem candidate 1
Suppose:

1. longest-chain length tracks proper time;
2. interval cardinality tracks causal volume;
3. \(D_{\mathrm{eff}}\) stabilizes under refinement;
4. order-distance neighborhoods are stable;
5. local embeddings from order-distance data converge.

Then causal order alone supports a coordinate-free metric reconstruction route.

This theorem is **not yet proved**.

---

# 10. Updated proof-chain status

This file strengthens the causal-geometry side:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
ORDER_ONLY_METRIC_RECONSTRUCTION.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
        ↓
CURVATURE_ESTIMATION.md
```

The next hard seam is local embedding and metric fitting from order-only distances.

---

# 11. Next derivation target

The next file should be:

```text
ORDER_DISTANCE_EMBEDDING.md
```

Its job:

\[
d_{\mathrm{ord}}(i,j)
\longmapsto
\text{local embedding}
\longmapsto
g_{\mu\nu}.
\]

This is the next metric-reconstruction bottleneck.

---

# Honest status line

> `ORDER_ONLY_METRIC_RECONSTRUCTION.md` gives the first order-only distance and dimension reconstruction route using longest-chain length and interval cardinality. It reduces coordinate dependence, but it does not yet reconstruct a local metric or prove manifoldlikeness.

**End of file.**
