# CAUSAL_SET_RECONSTRUCTION.md

# Causal Set Reconstruction
## Replacement route after naive order-distance embedding failure

## Status
**Live derivation target. First causal-set-style reconstruction pass. Not metric-closed.**

`ORDER_DISTANCE_EMBEDDING.md` produced a genuine hard failure:

```text
PASS: 0.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 100.0%
```

`ORDER_DISTANCE_FAILURE_ANALYSIS.md` diagnosed why:

\[
d_{\mathrm{ord}}(i,j)=N(i,j)^{1/D_{\mathrm{eff}}}
\]

is not a complete metric distance. It is timelike/volume-like and sparse over comparable pairs. It does not directly supply spatial distances between incomparable events.

This file replaces the failed route with a causal-set-style reconstruction:

```text
causal order
    -> longest chains
    -> antichain spatial slices
    -> interval-volume dimension
    -> spatial adjacency within slices
    -> local Lorentzian reconstruction
```

This file does **not** prove metric reconstruction. It provides the first corrected route after the failed MDS path.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Observation**
- **Definition**
- **Lemma candidate**
- **Derivation target**
- **Failure condition**
- **Pivot recommendation**

---

# 1. Why this file exists

## Observation 1
The naive chain:

\[
\text{interval cardinality}
\to
\text{order distance}
\to
\text{Euclidean MDS}
\to
\text{metric}
\]

failed because causal order is not a complete spatial distance matrix.

Causal order naturally supplies:
- timelike relation,
- longest-chain depth,
- interval volume,
- antichains,
- and causal neighborhoods.

Therefore reconstruction must use causal-set-native structures.

---

# 2. Causal-set reconstruction objects

## Definition 1: Longest-chain time
For comparable events:

\[
e_i\prec e_j,
\]

define:

\[
L(i,j)
\]

as the longest-chain length.

Define event depth:

\[
d(e_j)=\max_i L(i,j).
\]

This is the first order-only time/rank function.

---

## Definition 2: Antichain slices
An antichain is a set of mutually incomparable events:

\[
A=\{e_i:\neg(e_i\prec e_j),\neg(e_j\prec e_i)\text{ for all }i\ne j\}.
\]

A rank slice is approximated by:

\[
A_k=\{e_i:d(e_i)=k\}.
\]

These are candidate spatial slices.

---

## Definition 3: Causal profiles
For event \(e_i\), define its causal profile:

\[
P_i=(\mathrm{Past}(i),\mathrm{Future}(i)).
\]

Two events in the same antichain are spatially near if their causal profiles are similar.

This replaces naive interval-distance MDS.

---

# 3. Spatial adjacency within antichains

## Definition 4
For events \(e_i,e_j\in A_k\), define causal-profile similarity:

\[
S(i,j)
=
\frac{
P_i\cdot P_j
}{
\|P_i\|\|P_j\|
}.
\]

Candidate spatial neighbors are the highest-similarity events within the same antichain.

## Failure condition 1
If causal-profile similarity does not identify stable neighborhoods within antichains, spatial reconstruction from order alone fails.

---

# 4. Interval-volume dimension

## Definition 5
For comparable events:

\[
e_i\prec e_j,
\]

define interval cardinality:

\[
N(i,j)=|I(i,j)|.
\]

A dimension proxy is estimated from:

\[
\log(N(i,j)+1)
\sim
D_{\mathrm{eff}}\log(L(i,j)+1)+C.
\]

This uses only order data:
- interval cardinality,
- longest-chain length.

## Failure condition 2
If \(D_{\mathrm{eff}}\) does not stabilize, the causal set is not manifoldlike enough for continuum reconstruction.

---

# 5. Reconstruction theorem candidate

## Lemma candidate 1
If:

1. longest-chain depth gives a stable time/rank function;
2. rank slices are approximate antichains;
3. causal-profile similarity gives stable spatial adjacency;
4. interval-volume dimension stabilizes;
5. local adjacency supports metric fitting;

then the causal order supports a causal-set-style route to local Lorentzian geometry.

This is not yet proved.

---

# 6. Verifier implementation

## Status
**Implemented as `causal_set_reconstruction_verifier.py`. Execution log captured.**

The verifier tests:

1. comparable density;
2. longest-chain depth/time correlation;
3. rank-slice antichain validity;
4. median slice size;
5. interval-volume dimension proxy;
6. causal-profile spatial-neighbor precision.

Coordinates are used only for synthetic evaluation of whether causal-profile neighbors recover hidden spatial neighbors.

## Captured verifier output

```text
Causal set reconstruction verifier
==================================================
Route:
causal order -> longest-chain depth -> antichain slices -> causal-profile spatial adjacency
Coordinates are used only for synthetic evaluation of spatial-neighbor precision.

PASS: 95.0
SOFT_FAIL: 0.0
HARD_FAIL: 5.0
comparable_density_median: 0.21352458979027422
n_slices_median: 9.0
median_slice_size_median: 30.0
antichain_violation_median: 0.0
depth_time_corr_median: 0.9720695249464243
dim_proxy_median: 2.9930602008438965
spatial_neighbor_precision_median: 0.14204848494949832
```

---

# 7. What this file establishes

### Established at current proof level

1. The failed MDS route is replaced with a causal-set-native route.
2. Longest-chain time/rank is explicitly defined.
3. Antichain spatial slices are explicitly defined.
4. Causal-profile spatial adjacency is introduced.
5. Interval-volume dimension remains part of the reconstruction.
6. A verifier tests the corrected route.

### Not yet proved

1. Spatial adjacency precision is likely modest and must improve.
2. Antichain slicing by rank is only a first approximation.
3. The route is tested only on synthetic flat data.
4. Curved causal sets are not tested.
5. Local Lorentzian metric fitting from antichain neighborhoods is not implemented.
6. Manifoldlikeness is not proven.

---

# 8. Updated proof-chain status

The corrected causal-to-metric chain is:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
ORDER_DISTANCE_FAILURE_ANALYSIS.md
        ↓
CAUSAL_SET_RECONSTRUCTION.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
```

The failed route remains documented:

```text
ORDER_DISTANCE_EMBEDDING.md  [FAILED]
```

---

# 9. Next derivation target

The next file should be:

```text
ANTICHAIN_SPATIAL_GEOMETRY.md
```

Its job:

\[
A_k
\longmapsto
\text{spatial adjacency}
\longmapsto
h_{ab}
\]

where \(h_{ab}\) is a spatial metric candidate on a causal slice.

This is now the next concrete seam.

---

# Honest status line

> `CAUSAL_SET_RECONSTRUCTION.md` replaces the failed naive order-distance embedding route with a causal-set-native reconstruction program using longest chains, antichains, interval volumes, and causal-profile spatial adjacency. It is verifier-backed as a structural route, but it does not yet recover a full spatial metric or Lorentzian geometry.

**End of file.**
