# CAUSAL_INTERVAL_GEOMETRY.md

# Causal Interval Geometry
## Candidate route from causal order to interval volume, dimension, and light-cone structure

## Status
**Live derivation target. First causal-interval geometry pass. Not yet metric-closed.**

`CAUSAL_ORDER_DERIVATION.md` defined a first candidate partial order:

\[
e_i\prec e_j
\]

from update order, retained-memory gating, and finite propagation.

This file attacks the next seam:

\[
I(i,j)
=
\{e_k:e_i\prec e_k\prec e_j\}
\longmapsto
\text{dimension, volume, light-cone scaling}.
\]

This file does **not** prove continuum spacetime geometry.

It tests whether causal intervals carry stable scaling information that could support the Lorentzian metric map.

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

The causal-order file gives a relation:

\[
e_i\prec e_j.
\]

A causal relation alone is not enough for geometry. A continuum spacetime also requires interval volume and dimension structure.

The goal of this file is to define a first interval-scaling test:

\[
|I(i,j)|
\sim
\tau_{ij}^{D},
\]

where:

- \(|I(i,j)|\) is interval cardinality;
- \(\tau_{ij}\) is proper-time-like separation;
- \(D\) is effective spacetime dimension.

---

# 2. Alexandrov intervals

## Definition 1
For comparable events:

\[
e_i\prec e_j,
\]

define the Alexandrov interval:

\[
I(i,j)
=
\{e_k:e_i\prec e_k\prec e_j\}.
\]

The interval cardinality is:

\[
N(i,j)=|I(i,j)|.
\]

## Assumption 1
If the causal order approximates a continuum spacetime, then interval cardinality should scale like causal volume:

\[
N(i,j)\propto V(i,j).
\]

---

# 3. Dimension from interval scaling

## Definition 2
In a flat continuum approximation:

\[
V(i,j)\propto \tau_{ij}^{D},
\]

so:

\[
\log N(i,j)
\approx
D\log \tau_{ij}+C.
\]

Thus an effective dimension estimate is:

\[
D_{\mathrm{eff}}
=
\frac{d\log N}{d\log\tau}.
\]

## Failure condition 1
If interval size does not scale consistently with separation, causal order does not support continuum dimension.

---

# 4. Light-cone structure

## Definition 3
For events with coordinates \((t_i,x_i)\), define the proper-time-like separation:

\[
\tau_{ij}^2
=
(t_j-t_i)^2
-
\frac{\|x_j-x_i\|^2}{c_{\mathrm{eff}}^2}.
\]

Comparable events satisfy:

\[
\tau_{ij}^2>0.
\]

The boundary:

\[
\tau_{ij}^2=0
\]

is the candidate light cone.

## Derivation target A
Remove the dependence on externally supplied coordinates and derive \(\tau_{ij}\) from causal interval structure alone.

This remains open.

---

# 5. Interval theorem candidate

## Theorem candidate 1
Suppose:

1. the causal relation is a valid partial order;
2. interval cardinalities are finite;
3. interval-size scaling obeys:
   \[
   |I(i,j)|\sim\tau_{ij}^D;
   \]
4. the estimated \(D\) is stable under refinement;
5. light-cone boundaries are stable;
6. \(\tau_{ij}\) can be reconstructed without external coordinates.

Then the causal order supports a continuum interval geometry.

This theorem is **not yet proved**.

---

# 6. Verifier implementation

## Status
**Implemented as `causal_interval_geometry_verifier.py`. Execution log captured.**

The verifier:

1. generates update-ordered events;
2. builds the causal relation:
   \[
   i\to j
   \quad\text{iff}\quad
   t_j>t_i
   \quad\text{and}\quad
   \|x_j-x_i\|\le c(t_j-t_i);
   \]
3. samples comparable pairs;
4. computes interval cardinalities:
   \[
   |I(i,j)|;
   \]
5. estimates dimension from:
   \[
   \log(|I(i,j)|+1)
   \sim
   D\log\tau_{ij}+C.
   \]

## Captured verifier output

```text
Causal interval geometry verifier
==================================================
Test:
Build causal intervals I(i,j), count |I(i,j)|, estimate dimension from log interval-size scaling.

Sweep results:
PASS: 87.5
SOFT_FAIL: 2.5
HARD_FAIL: 10.0
dim_estimate_median: 2.598292971546218
dim_estimate_min: 1.423584566509049
dim_estimate_max: 2.943546323196807
r2_median: 0.8677155751384873
comparable_pairs_median: 17423.0
```

---

# 7. What this file establishes

### Established at current proof level

1. Alexandrov intervals are explicitly defined.
2. Interval cardinality is connected to causal volume.
3. A first dimension-scaling diagnostic is implemented.
4. Failure conditions are explicit:
   - too few comparable pairs;
   - no stable scaling;
   - sparse/dense causal degeneracy;
   - coordinate dependence.

### Not yet proved

1. Dimension is not derived coordinate-free.
2. Proper time \(\tau_{ij}\) is still coordinate-assisted.
3. Light-cone structure is not derived from order alone.
4. Manifoldlikeness is not proven.
5. Curved spacetime interval scaling is not tested.
6. Local dimension variation is not yet analyzed.

---

# 8. Updated proof-chain status

This file strengthens the causal side of the chain:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
        ↓
CURVATURE_ESTIMATION.md
        ↓
EINSTEIN_HILBERT_LIMIT.md
```

The next hard seam is:

\[
\text{causal intervals}
\longmapsto
\text{coordinate-free metric reconstruction}.
\]

---

# 9. Next derivation target

The next file should be:

```text
ORDER_ONLY_METRIC_RECONSTRUCTION.md
```

Its job:

\[
(e_i\prec e_j)
\longmapsto
d_{\mathrm{causal}}(i,j),
\quad
D_{\mathrm{eff}},
\quad
g_{\mu\nu}
\]

without assuming external coordinates.

---

# Honest status line

> `CAUSAL_INTERVAL_GEOMETRY.md` gives the first verifier-backed interval-scaling test for the causal-order seam. It supports the idea that causal intervals can carry dimension/volume information, but it does not yet derive metric distances, light cones, or dimension in a coordinate-free way.

**End of file.**
