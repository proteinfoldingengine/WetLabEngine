# CONTINUUM_LIMIT_CLOSURE_STATUS_V2.md

# Continuum Limit Closure Status V2
## Superseding seam audit after corrected causal ADM branch

## Status
**Closure audit. Not a proof.**

This file supersedes the earlier `CONTINUUM_LIMIT_CLOSURE_STATUS.md`.

It incorporates:

1. the original scalar-density memory-action route;
2. the coefficient / weak-memory verifier chain;
3. the failed naive order-distance embedding branch;
4. the corrected causal-set / antichain / ADM branch;
5. the measured-lapse update;
6. the graph-curvature update;
7. the finite-difference variation target;
8. the weak-memory field-equation proxy.

This file does **not** close seam 3.

It classifies each seam as:

```text
Closed
Verifier-backed candidate
Proxy / verifier-backed
Conditional
Failed
Open
```

No seam should be called “Closed” unless it is actually derived, not merely verified structurally.

---

# 1. Current top-level status

## Honest status

`CONTINUUM_LIMIT.md` is now best described as:

```text
Verifier-backed derivation program. Not GR closure.
```

It is no longer just a conceptual blueprint, because many previously schematic pieces now have:
- explicit candidate objects;
- verifier scripts;
- failure modes;
- and artifact logs.

But it still does not derive:
- the Einstein-Hilbert action;
- the Ricci scalar;
- Einstein's equations;
- exact memory stress-energy;
- physical time from microscopic update order;
- or fully covariant lapse/shift geometry.

---

# 2. Current proof-chain overview

## 2.1 Memory / coefficient branch

```text
CHI_FIXED_POINT.md
        ↓
MICRO_TO_BLOCK_ACTION.md
        ↓
DISCRETE_MEMORY_ACTION.md
        ↓
COEFFICIENT_DERIVATION.md
        ↓
CONTINUUM_LIMIT.md
```

## 2.2 Failed metric branch

```text
ORDER_DISTANCE_EMBEDDING.md  [FAILED]
        ↓
ORDER_DISTANCE_FAILURE_ANALYSIS.md
```

## 2.3 Corrected causal ADM branch

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
CAUSAL_SET_RECONSTRUCTION.md
        ↓
ANTICHAIN_SPATIAL_GEOMETRY.md
        ↓
ANTICHAIN_GRAPH_METRIC.md
        ↓
CAUSAL_SLICE_LORENTZIAN_METRIC.md
        ↓
LAPSE_SHIFT_CLOSURE_STATUS.md
        ↓
SPATIAL_GRAPH_CURVATURE.md
        ↓
ADM_ACTION_WITH_GRAPH_CURVATURE.md
        ↓
CAUSAL_ADM_VARIATION_TARGET.md
        ↓
CAUSAL_ADM_FIELD_EQUATION_PROXY.md
```

---

# 3. Master closure matrix

| Seam | File | Status | Evidence | Main limitation |
|---|---|---:|---|---|
| Bridge coefficient | `CHI_FIXED_POINT.md` | Verifier-backed candidate | fixed-point/loading verifier | Not microscopic uniqueness |
| Micro-to-block action constants | `MICRO_TO_BLOCK_ACTION.md` | Verifier-backed candidate | positive block constants verifier | Not uniquely derived |
| Discrete memory action | `DISCRETE_MEMORY_ACTION.md` | Verifier-backed candidate | stable action coefficient map | Not covariant/unique |
| Continuum coefficients | `COEFFICIENT_DERIVATION.md` | Verifier-backed candidate | CL-2 coefficient verifier | Scale constants remain |
| Scalar memory action | `CONTINUUM_LIMIT.md` / Option A | Verifier-backed candidate | weak-memory decoupling | Coefficients not microscopically derived |
| Field-equation variation, scalar branch | `FIELD_EQUATION_VARIATION.md` | Conditional / verifier-backed proxy | stress-energy scaling verifier | Full EH variation open |
| Naive order-distance embedding | `ORDER_DISTANCE_EMBEDDING.md` | Failed | 100% hard fail | Causal distance not full metric distance |
| Failure analysis | `ORDER_DISTANCE_FAILURE_ANALYSIS.md` | Closed diagnostic | identifies missingness/nonmetricity | Diagnostic, not construction |
| Causal order | `CAUSAL_ORDER_DERIVATION.md` | Verifier-backed candidate | partial-order verifier | Update order not proven physical time |
| Causal interval geometry | `CAUSAL_INTERVAL_GEOMETRY.md` | Verifier-backed / coordinate-assisted | interval scaling verifier | Proper time partly coordinate-assisted |
| Order-only metric proxy | `ORDER_ONLY_METRIC_RECONSTRUCTION.md` | Verifier-backed proxy | order-distance/time proxy | Not metric reconstruction |
| Causal-set reconstruction | `CAUSAL_SET_RECONSTRUCTION.md` | Verifier-backed candidate | chains + antichains verifier | Manifoldlikeness not proven |
| Antichain spatial geometry | `ANTICHAIN_SPATIAL_GEOMETRY.md` | Verifier-backed candidate | spatial adjacency verifier | Spatial metric not yet full |
| Antichain graph metric | `ANTICHAIN_GRAPH_METRIC.md` | Verifier-backed proxy | Laplacian metric proxy verifier | Graph/gauge dependence |
| Local Lorentzian metric | `CAUSAL_SLICE_LORENTZIAN_METRIC.md` | Verifier-backed candidate | signature verifier | Shift not closed |
| Causal-slice curvature | `CAUSAL_SLICE_CURVATURE.md` | Proxy / verifier-backed | slice curvature proxy verifier | Not Ricci/R scalar |
| ADM causal action | `ADM_CAUSAL_SLICE_ACTION.md` | Proxy / verifier-backed | finite action proxy | Fixed lapse in old version |
| Lapse derivation | `LAPSE_SHIFT_DERIVATION.md` | Verifier-backed candidate | stable lapse verifier | Normalization not unique |
| Slice alignment / shift | `SLICE_ALIGNMENT_AND_SHIFT.md` | Structured proxy / open | alignment verifier | Weak physical correlation |
| Lapse/shift closure | `LAPSE_SHIFT_CLOSURE_STATUS.md` | Audit | lapse accepted, shift diagnostic | Full shift open |
| ADM with measured lapse | `ADM_ACTION_WITH_LAPSE.md` | Verifier-backed proxy | action ratio stable | Shift excluded |
| Spatial graph curvature | `SPATIAL_GRAPH_CURVATURE.md` | Verifier-backed graph proxy | graph curvature verifier | Not continuum R3 |
| ADM with graph curvature | `ADM_ACTION_WITH_GRAPH_CURVATURE.md` | Verifier-backed proxy | finite integrated action | Not ADM/EH |
| ADM variation target | `CAUSAL_ADM_VARIATION_TARGET.md` | Verifier-backed proxy | finite gradient verifier | Not Einstein variation |
| ADM field-equation proxy | `CAUSAL_ADM_FIELD_EQUATION_PROXY.md` | Verifier-backed proxy | weak-memory source scaling | Not Einstein equation |
| Full continuum GR limit | `CONTINUUM_LIMIT.md` | Open / not closed | all above | EH/covariance/source closure open |

---

# 4. Verifier result summary

## 4.1 Failed branch

### `ORDER_DISTANCE_EMBEDDING.md`

```text
PASS: 0.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 100.0%
```

Result:

```text
Failed.
```

Reason:

```text
Interval-cardinality distance is not a full metric distance matrix.
```

---

## 4.2 Corrected causal-set branch

### `CAUSAL_SET_RECONSTRUCTION.md`

```text
PASS: 95.0%
HARD_FAIL: 5.0%
```

Key diagnostics:

```text
depth_time_corr_median: 0.972
antichain_violation_median: 0.0
dim_proxy_median: 2.993
spatial_neighbor_precision_median: 0.142
```

Status:

```text
Verifier-backed causal-set reconstruction candidate
```

---

## 4.3 Antichain spatial geometry

### `ANTICHAIN_SPATIAL_GEOMETRY.md`

```text
PASS: 92.0%
HARD_FAIL: 8.0%
```

Key diagnostics:

```text
neighbor_precision_median: 0.686
neighbor_recall_proxy_median: 0.738
graph_connectivity_fraction_median: 1.0
laplacian_rank_median: 37.25
```

Status:

```text
Strong verifier-backed spatial adjacency candidate
```

---

## 4.4 Antichain graph metric

### `ANTICHAIN_GRAPH_METRIC.md`

```text
PASS: 92.5%
HARD_FAIL: 7.5%
```

Key diagnostics:

```text
median_embedding_corr_median: 0.641
median_stress_median: 0.303
median_metric_condition_median: 2.03
median_metric_rank_median: 3.0
```

Status:

```text
Verifier-backed spatial metric proxy
```

---

## 4.5 Causal-slice Lorentzian metric

### `CAUSAL_SLICE_LORENTZIAN_METRIC.md`

```text
PASS: 78.75%
SOFT_FAIL: 13.75%
HARD_FAIL: 7.5%
```

Key diagnostics:

```text
depth_time_corr_median: 0.978
median_h_rank_median: 3.0
signature_fraction_median: 1.0
median_g_condition_median: 88.25
```

Status:

```text
Verifier-backed Lorentzian signature candidate
```

Caveat:

```text
Conditioning needs lapse/normalization refinement.
```

---

## 4.6 Lapse and shift

### `LAPSE_SHIFT_DERIVATION.md`

```text
PASS: 93.33%
HARD_FAIL: 6.67%
```

Key diagnostics:

```text
lapse_median_median: 1.0000
lapse_cv_median: 0.0608
```

Status:

```text
Lapse verifier-backed.
```

### `SLICE_ALIGNMENT_AND_SHIFT.md`

```text
PASS: 86.0%
HARD_FAIL: 14.0%
```

Key diagnostics:

```text
match_score_median: 0.891
hidden_shift_corr_median: 0.0746
```

Status:

```text
Shift structured but not closed.
```

---

## 4.7 Measured-lapse ADM action

### `ADM_ACTION_WITH_LAPSE.md`

```text
PASS: 94.0%
HARD_FAIL: 6.0%
```

Key diagnostics:

```text
lapse_cv: 0.0393
action_ratio_median: 1.0039
finite_fraction_median: 1.0
```

Status:

```text
Measured lapse safely reintegrated.
```

---

## 4.8 Spatial graph curvature

### `SPATIAL_GRAPH_CURVATURE.md`

```text
PASS: 90.0%
SOFT_FAIL: 1.67%
HARD_FAIL: 8.33%
```

Key diagnostics:

```text
forman_median: -15.0
ollivier_proxy_median: 0.316
scalar_R3_median: 0.270
finite_fraction_median: 1.0
```

Status:

```text
Verifier-backed graph curvature proxy.
```

---

## 4.9 ADM action with graph curvature

### `ADM_ACTION_WITH_GRAPH_CURVATURE.md`

```text
PASS: 86.0%
HARD_FAIL: 14.0%
```

Key diagnostics:

```text
R3_graph_median: 0.2644
action_graph_abs_median: 879.99
action_ratio_median: 0.6101
finite_fraction_median: 1.0
```

Status:

```text
Strongest ADM-like action proxy so far.
```

---

## 4.10 Variation and field-equation proxy

### `CAUSAL_ADM_VARIATION_TARGET.md`

```text
PASS: 100.0%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
grad_norm_median: 0.674
grad_norm_max_median: 1.548
finite_fraction_median: 1.0
nontrivial_fraction_median: 1.0
```

Status:

```text
Stable proxy variation.
```

### `CAUSAL_ADM_FIELD_EQUATION_PROXY.md`

```text
PASS: 100.0%
HARD_FAIL: 0.0%
```

Key diagnostics:

```text
euler_norm_median: 0.6801
source_norm_median: 0.00117
source_to_euler_ratio: 0.00161
weak_scaling_ratio: 0.5000
```

Status:

```text
Weak-memory sourced field-equation proxy.
```

---

# 5. What is stronger now

Compared to the original `CONTINUUM_LIMIT.md`, the package now has:

1. a tested scalar-density memory action route;
2. a tested coefficient bridge;
3. a documented failed metric branch;
4. a corrected causal-set reconstruction route;
5. antichain spatial geometry;
6. spatial graph metric proxy;
7. measured lapse;
8. explicit graph spatial curvature;
9. ADM-like action proxy;
10. finite-difference variation;
11. weak-memory source coupling.

This is a major strengthening of seam 3 as a falsifiable derivation program.

---

# 6. What remains open

## 6.1 Physical time

Still open:

```text
microscopic update order -> physical causal time
```

## 6.2 Coordinate-free manifoldlikeness

Still open:

```text
causal order -> coordinate-free dimension / topology / manifold approximation
```

## 6.3 Shift

Still open:

```text
slice alignment -> covariant N_a vector field
```

## 6.4 Continuum spatial curvature

Still open:

```text
R3_graph -> continuum R^(3)
```

## 6.5 ADM/EH convergence

Still open:

```text
S_proxy^(N,R3) -> S_ADM -> S_EH
```

## 6.6 Variational closure

Still open:

```text
Euler proxy -> ADM constraints/evolution equations
```

## 6.7 Exact memory stress-energy

Still open:

```text
weak source proxy -> exact T_mu_nu^mem projection
```

## 6.8 Covariance and boundary terms

Still open:

```text
proxy branch -> covariant continuum action with correct boundary terms
```

---

# 7. Safe claim

The safe public/repo claim is:

> The continuum-limit seam is now a verifier-backed derivation program with explicit candidate constructions for memory action, causal order, antichain spatial geometry, local Lorentzian metric proxy, measured lapse, graph spatial curvature, ADM-like action, finite-difference variation, and weak-memory source coupling. It also contains a documented failed metric-reconstruction route. It is not a derivation of GR.

---

# 8. Unsafe claims

Do not claim:

```text
GR has been derived.
```

Do not claim:

```text
Einstein-Hilbert has been recovered.
```

Do not claim:

```text
Einstein's equations have been derived.
```

Do not claim:

```text
R3_graph is continuum R3.
```

Do not claim:

```text
Shift is derived.
```

Do not claim:

```text
The metric is fully covariant.
```

---

# 9. Updated next technical target

The next technical target should be:

```text
MEMORY_STRESS_PROJECTION.md
```

Purpose:

```text
T_mu_nu^mem from scalar-density memory action
        ↓
project onto causal ADM slices
        ↓
S_ab^mem,k
```

Why this is next:

`CAUSAL_ADM_FIELD_EQUATION_PROXY.md` currently uses a weak-memory source proxy. The next real closure move is to replace that proxy with the projected stress tensor from the scalar-density memory action.

---

# 10. Honest final status

> `CONTINUUM_LIMIT_CLOSURE_STATUS_V2.md` shows that seam 3 has advanced from a blueprint to a verifier-backed derivation program with a corrected causal ADM branch and a documented failed path. However, every key GR-level object remains proxy-level or conditional. Seam 3 is not closed.

**End of file.**
