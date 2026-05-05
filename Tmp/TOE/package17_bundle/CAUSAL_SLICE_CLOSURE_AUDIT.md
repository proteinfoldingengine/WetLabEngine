# CAUSAL_SLICE_CLOSURE_AUDIT.md

# Causal Slice Closure Audit
## Status map after failed order-distance embedding and corrected causal-set route

## Status
**Audit document. Not a proof.**

This file audits the causal-to-metric subchain that emerged while tightening `CONTINUUM_LIMIT.md`.

It does not claim the causal-slice route is closed.

Its purpose is to answer:

1. What failed?
2. What recovered?
3. Which seams are verifier-backed?
4. Which seams remain proxy-only?
5. What can be safely reintegrated into `CONTINUUM_LIMIT.md`?

---

# 1. Why this audit exists

The original continuum-limit chain required an emergent metric:

```text
discrete geometry / retained-memory data
        ↓
g_mu_nu
        ↓
R_mu_nu, R
        ↓
Einstein-Hilbert action
```

The first naive order-distance route failed:

```text
ORDER_DISTANCE_EMBEDDING.md
```

with:

```text
PASS: 0.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 100.0%
```

That failure forced a pivot to a causal-set-style route:

```text
causal order
    -> longest-chain time
    -> antichain spatial slices
    -> antichain graph metric
    -> causal-slice Lorentzian metric
    -> causal-slice curvature proxy
    -> ADM-like action proxy
```

This audit summarizes the corrected branch.

---

# 2. Failed branch

## 2.1 ORDER_DISTANCE_EMBEDDING.md

Status:

```text
FAILED
```

Attempted chain:

```text
causal order
    -> interval cardinality N(i,j)
    -> order distance d_ord = N(i,j)^(1/D_eff)
    -> MDS embedding
    -> metric
```

Verifier result:

```text
PASS: 0.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 100.0%
```

Diagnostic result from `ORDER_DISTANCE_FAILURE_ANALYSIS.md`:

```text
comparable_density_median: 0.2149
D_eff_median: 3.279
triangle_violation_rate_median: 0.25
local_missingness_median: 0.96875
mds_positive_rank_median: 0.0
```

Conclusion:

> Interval-cardinality order distance is not a complete metric distance matrix. It is timelike / volume-like and sparse over comparable pairs. It cannot be naively fed to Euclidean MDS to recover local geometry.

This branch should remain in the repo as an honest falsified path.

---

# 3. Corrected causal-set route

The corrected route is:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
ORDER_DISTANCE_FAILURE_ANALYSIS.md
        ↓
CAUSAL_SET_RECONSTRUCTION.md
        ↓
ANTICHAIN_SPATIAL_GEOMETRY.md
        ↓
ANTICHAIN_GRAPH_METRIC.md
        ↓
CAUSAL_SLICE_LORENTZIAN_METRIC.md
        ↓
CAUSAL_SLICE_CURVATURE.md
        ↓
ADM_CAUSAL_SLICE_ACTION.md
```

This route does not treat causal intervals as a complete Euclidean distance matrix. Instead it separates:

- time from longest chains;
- space from antichains;
- spatial adjacency from causal-profile similarity;
- spatial metric proxy from antichain graph embedding;
- Lorentzian metric from causal time + spatial metric.

---

# 4. Seam-by-seam causal audit

| Seam | File | Status | Verifier result | Main limitation |
|---|---|---:|---|---|
| Causal partial order | `CAUSAL_ORDER_DERIVATION.md` | Verifier-backed candidate | PASS 84.0%, SOFT 16.0%, HARD 0.0% | Update order not proven physical time |
| Interval scaling | `CAUSAL_INTERVAL_GEOMETRY.md` | Verifier-backed, coordinate-assisted | PASS 87.5%, SOFT 2.5%, HARD 10.0% | Proper time still coordinate-assisted |
| Order-only distance proxy | `ORDER_ONLY_METRIC_RECONSTRUCTION.md` | Verifier-backed proxy | PASS 88.75%, SOFT 1.25%, HARD 10.0% | Does not reconstruct metric |
| Naive order embedding | `ORDER_DISTANCE_EMBEDDING.md` | Failed | HARD 100.0% | Causal distance not full metric distance |
| Failure analysis | `ORDER_DISTANCE_FAILURE_ANALYSIS.md` | Closed diagnostic | Confirms missingness / nonmetric failure | Diagnostic only |
| Causal-set reconstruction | `CAUSAL_SET_RECONSTRUCTION.md` | Verifier-backed candidate | PASS 95.0%, HARD 5.0% | Spatial adjacency still modest/proxy |
| Antichain spatial geometry | `ANTICHAIN_SPATIAL_GEOMETRY.md` | Verifier-backed candidate | PASS 92.0%, HARD 8.0% | No spatial metric yet |
| Antichain graph metric | `ANTICHAIN_GRAPH_METRIC.md` | Verifier-backed candidate | PASS 92.5%, HARD 7.5% | Metric proxy, not full metric proof |
| Causal-slice Lorentzian metric | `CAUSAL_SLICE_LORENTZIAN_METRIC.md` | Verifier-backed candidate | PASS 78.75%, SOFT 13.75%, HARD 7.5% | Lapse/shift not derived |
| Causal-slice curvature | `CAUSAL_SLICE_CURVATURE.md` | Proxy / verifier-backed | PASS 80.0%, SOFT 2.5%, HARD 17.5% | Curvature proxies, not Ricci scalar |
| ADM causal-slice action | `ADM_CAUSAL_SLICE_ACTION.md` | Proxy / verifier-backed | PASS 95.0%, HARD 5.0% | Not full ADM/EH action |

---

# 5. What is now stronger than before

## 5.1 The failed branch improved the proof discipline

The 100% hard fail in `ORDER_DISTANCE_EMBEDDING.md` prevented an overclaim.

The original temptation was:

```text
causal order -> distance -> embedding -> metric
```

The verifier showed that was invalid.

This is a meaningful scientific improvement.

---

## 5.2 The corrected branch separates time and space

The corrected route no longer asks interval cardinality to do everything.

Instead:

```text
longest chains -> time
antichains -> space
causal profiles -> spatial adjacency
graph Laplacian -> spatial metric proxy
ADM assembly -> Lorentzian metric proxy
```

That is structurally closer to causal-set reasoning.

---

## 5.3 The antichain spatial route is much stronger

`ANTICHAIN_SPATIAL_GEOMETRY.md` produced:

```text
neighbor_precision_median: 0.686
neighbor_recall_proxy_median: 0.738
graph_connectivity_fraction_median: 1.0
laplacian_rank_median: 37.25
```

This is the strongest evidence so far that spatial structure can be recovered from causal order in the synthetic setting.

---

## 5.4 The antichain graph metric is viable

`ANTICHAIN_GRAPH_METRIC.md` produced:

```text
median_embedding_corr_median: 0.641
median_stress_median: 0.303
median_metric_condition_median: 2.03
median_metric_rank_median: 3.0
```

This supports a spatial metric proxy:

```text
G_k -> graph embedding -> h_ab
```

---

## 5.5 The Lorentzian assembly is viable but stricter

`CAUSAL_SLICE_LORENTZIAN_METRIC.md` produced:

```text
PASS: 78.75%
SOFT_FAIL: 13.75%
HARD_FAIL: 7.5%

signature_fraction_median: 1.0
median_h_rank_median: 3.0
median_g_condition_median: 88.25
```

The signature result is strong, but conditioning needs lapse/normalization work.

---

## 5.6 The ADM-like action proxy is finite

`ADM_CAUSAL_SLICE_ACTION.md` produced:

```text
PASS: 95.0%
HARD_FAIL: 5.0%

action_proxy_median: 1536.53
action_abs_proxy_median: 1713.27
median_K_norm_median: 0.164
median_R3_proxy_median: 0.451
finite_fraction_median: 1.0
```

This supports action-like assembly, but not a true Einstein-Hilbert derivation.

---

# 6. What remains open

## 6.1 Physical origin of update time

Still open:

```text
microscopic update order -> physical causal time
```

The route assumes update order is physically meaningful.

This is a major open seam.

---

## 6.2 Coordinate-free dimension

`CAUSAL_INTERVAL_GEOMETRY.md` remains partially coordinate-assisted.

The order-only proxy helps, but dimension is not fully robust or manifold-certified.

---

## 6.3 Lapse and shift

Current Lorentzian metric assembly uses:

```text
N = 1
N_a = 0
```

Open target:

```text
causal slice density / rank spacing -> N
slice-to-slice graph drift -> N_a
```

---

## 6.4 True spatial curvature

`ADM_CAUSAL_SLICE_ACTION.md` uses a graph spectral proxy for:

```text
R^(3)
```

Open target:

```text
antichain graph metric -> true graph / Regge / embedded spatial curvature
```

---

## 6.5 Full Ricci scalar

`CAUSAL_SLICE_CURVATURE.md` uses velocity, acceleration, and log-volume curvature proxies.

Open target:

```text
(h_ab, N, N_a, K_ab, R^(3)) -> R^(4)
```

---

## 6.6 Variational principle

The ADM proxy is not yet varied.

Open target:

```text
delta S_geom = 0
```

and compatibility with:

```text
FIELD_EQUATION_VARIATION.md
```

---

## 6.7 Memory coupling

The causal-slice geometric route has not yet been coupled back to:

```text
S_mem
T_mu_nu^mem
Q_nu
```

---

# 7. Reintegration guidance for CONTINUUM_LIMIT.md

## 7.1 Safe update

`CONTINUUM_LIMIT.md` can now be updated to say:

> The original emergent-metric seam split into two branches. A naive order-distance embedding route failed and was retained as a falsified path. A corrected causal-set-style route using longest chains, antichains, causal-profile spatial adjacency, graph metric proxies, and ADM-like slice action diagnostics is verifier-backed but still not closed.

## 7.2 Unsafe update

Do not say:

> The framework derives the Lorentzian metric and Einstein-Hilbert action from causal order.

That remains unsupported.

## 7.3 Safe claim

Safe claim:

> A corrected causal-slice pipeline now exists and is verifier-backed through local Lorentzian metric assembly and ADM-like action proxy construction, but it remains proxy-level pending lapse, shift, true spatial curvature, Ricci scalar, and variational closure.

---

# 8. Recommended next file

The next file should be:

```text
LAPSE_SHIFT_DERIVATION.md
```

Purpose:

```text
causal rank spacing, slice density, and slice-to-slice graph drift
        ->
N, N_a
```

Why this is next:

- `CAUSAL_SLICE_LORENTZIAN_METRIC.md` currently assumes \(N=1\).
- `ADM_CAUSAL_SLICE_ACTION.md` currently assumes zero shift.
- A real ADM route requires both.

---

# 9. Bottom-line audit

## What is recovered

The causal-to-metric seam recovered after a hard failure.

The corrected branch now has verifier-backed pieces for:

1. causal order,
2. interval scaling,
3. causal-set reconstruction,
4. antichain spatial adjacency,
5. antichain graph metric,
6. Lorentzian slice assembly,
7. curvature proxies,
8. ADM-like action proxy.

## What is not closed

The branch does not yet prove:

```text
causal order -> full Lorentzian metric
```

or:

```text
causal-slice action -> Einstein-Hilbert action
```

or:

```text
delta S -> Einstein field equations
```

## Honest final status

> The naive order-distance embedding path failed. The corrected causal-set/antichain path is substantially stronger and verifier-backed through ADM-like action proxies, but it remains a proxy-level derivation program. The next decisive seam is deriving lapse and shift.

**End of file.**
