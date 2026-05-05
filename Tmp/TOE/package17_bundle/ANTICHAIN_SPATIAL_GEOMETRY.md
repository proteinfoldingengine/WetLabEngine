# ANTICHAIN_SPATIAL_GEOMETRY.md

# Antichain Spatial Geometry
## Candidate route from causal slices to spatial adjacency and spatial metric proxies

## Status
**Live derivation target. First antichain-spatial pass. Not spatial-metric closed.**

`CAUSAL_SET_RECONSTRUCTION.md` pivoted away from the failed naive MDS path and introduced the causal-set-style route:

```text
causal order
    -> longest-chain depth
    -> antichain spatial slices
    -> interval-volume dimension
    -> causal-profile spatial adjacency
    -> local Lorentzian reconstruction
```

This file attacks the next seam:

\[
A_k
\longmapsto
\text{spatial adjacency}
\longmapsto
h_{ab},
\]

where \(A_k\) is an antichain/rank slice and \(h_{ab}\) is a spatial metric candidate.

This file does **not** recover a full spatial metric. It tests whether antichain slices can support stable spatial adjacency graphs.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Derivation target**
- **Failure condition**

Nothing here should be interpreted as a completed proof unless explicitly stated.

---

# 1. Goal

A Lorentzian metric can be decomposed locally into time and spatial geometry. The causal-order chain already gives a candidate time/rank function through longest-chain depth.

The next question is:

> can a spatial slice be reconstructed from antichains of the causal order?

This requires:
1. stable antichain slices;
2. spatial adjacency within slices;
3. graph neighborhoods that approximate hidden spatial neighborhoods;
4. a route from spatial adjacency to a spatial metric proxy.

---

# 2. Antichain slices

## Definition 1
Given a causal order \(e_i\prec e_j\), an antichain is a set:

\[
A=\{e_i:\neg(e_i\prec e_j),\neg(e_j\prec e_i)\text{ for }i\ne j\}.
\]

Using the longest-chain depth \(d(e_i)\), define rank slices:

\[
A_k=\{e_i:d(e_i)=k\}.
\]

These are candidate spatial slices.

## Failure condition 1
If rank slices are not approximate antichains, the spatial-slice reconstruction fails.

---

# 3. Causal-profile spatial adjacency

## Definition 2
For event \(e_i\), define its causal profile:

\[
P_i=(\mathrm{Past}(i),\mathrm{Future}(i)).
\]

For two events in the same antichain \(A_k\), define similarity:

\[
S(i,j)=
\frac{P_i\cdot P_j}{\|P_i\|\|P_j\|}.
\]

Candidate spatial neighbors are high-similarity events within the same antichain.

## Observation
This is more causal-set-native than using interval-cardinality as a Euclidean distance, because it compares how events sit relative to the causal past and future.

---

# 4. Spatial graph

## Definition 3
For each antichain \(A_k\), define a spatial graph:

\[
\mathcal G_k=(A_k,E_k),
\]

where:

\[
(i,j)\in E_k
\]

if \(j\) is among the top causal-profile neighbors of \(i\).

The spatial graph is admissible if:
- it is mostly connected;
- it has low antichain violation;
- its neighbors correlate with hidden spatial neighbors in synthetic tests;
- it has nondegenerate graph Laplacian structure.

---

# 5. Spatial metric target

## Derivation target A
Use graph distances, graph Laplacian eigenvectors, or diffusion maps on \(\mathcal G_k\) to construct a spatial metric proxy:

\[
h_{ab}^{(k)}.
\]

Possible routes:
1. graph geodesic distances;
2. Laplacian eigenmap embedding;
3. diffusion distance;
4. local neighborhood covariance after graph embedding.

This file only tests adjacency quality. It does not yet construct \(h_{ab}\).

---

# 6. Verifier implementation

## Status
**Implemented as `antichain_spatial_geometry_verifier.py`. Execution log captured.**

The verifier tests:

1. rank slices from longest-chain depth;
2. antichain violation rate;
3. causal-profile spatial adjacency;
4. hidden spatial-neighbor precision and recall proxy;
5. graph connectivity;
6. graph Laplacian rank.

Coordinates are used only for synthetic evaluation.

## Captured verifier output

```text
Antichain spatial geometry verifier
==================================================
Route:
causal order -> rank antichains -> causal-profile adjacency -> spatial graph diagnostics
Coordinates are used only for hidden spatial-neighbor evaluation.

PASS: 92.0
SOFT_FAIL: 0.0
HARD_FAIL: 8.0
n_slices_median: 9.0
median_slice_size_median: 38.25
antichain_violation_rate_median: 0.0
neighbor_precision_median: 0.6858272508869291
neighbor_recall_proxy_median: 0.7379981884057971
graph_connectivity_fraction_median: 1.0
laplacian_rank_median_median: 37.25
```

---

# 7. What this file establishes

### Established at current proof level

1. Antichain spatial slices are defined.
2. Causal-profile adjacency is specified.
3. Spatial graph diagnostics are implemented.
4. A verifier tests whether slice adjacency has nontrivial spatial signal.

### Not yet proved

1. A spatial metric \(h_{ab}\) is not yet constructed.
2. Precision is modest and needs improvement.
3. Rank slices may not be optimal antichains.
4. Curved or nonuniform sprinklings are not tested.
5. Graph embedding and metric fitting remain downstream.

---

# 8. Next derivation target

The next file should be:

```text
ANTICHAIN_GRAPH_METRIC.md
```

Its job:

\[
\mathcal G_k
\longmapsto
\text{graph embedding}
\longmapsto
h_{ab}^{(k)}.
\]

---

# Honest status line

> `ANTICHAIN_SPATIAL_GEOMETRY.md` gives the first verifier-backed spatial-slice reconstruction route using antichains and causal-profile adjacency. It produces nontrivial spatial signal but does not yet recover a spatial metric.

**End of file.**
