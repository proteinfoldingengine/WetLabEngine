# SPATIAL_GRAPH_CURVATURE.md

# Spatial Graph Curvature
## Candidate replacement for spectral \(R^{(3)}\) placeholder in causal-slice ADM action

## Status
**Live derivation target. First explicit spatial graph-curvature pass. Not continuum \(R^{(3)}\) closed.**

`ADM_ACTION_WITH_LAPSE.md` still uses a spectral placeholder for:

\[
R^{(3)}_k.
\]

This file attacks:

\[
\mathcal G_k,h_{ab}^{(k)}
\longmapsto
R^{(3)}_k.
\]

It replaces the pure spectral placeholder with explicit graph-curvature estimators:
- Forman-Ricci-style edge curvature;
- Ollivier-style neighbor-overlap curvature proxy;
- normalized slice scalar curvature proxy.

This file does **not** prove continuum spatial curvature. It provides a more explicit graph-curvature object for the ADM proxy.

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

# 1. Prior placeholder

`ADM_ACTION_WITH_LAPSE.md` used:

\[
R^{(3)}_{\mathrm{proxy},k}
\]

from graph spectral roughness.

This was finite but not geometrically explicit.

The new target is a curvature estimator based directly on the spatial graph:

\[
\mathcal G_k=(A_k,E_k,W_k).
\]

---

# 2. Forman-style edge curvature

## Definition 1
For each edge:

\[
e_{ij}\in E_k,
\]

define a first Forman-style curvature proxy:

\[
F_{ij}
=
(4-\deg(i)-\deg(j))W_{ij}.
\]

This is a simplified weighted graph curvature proxy.

It captures whether an edge lies in:
- sparse branch-like structure;
- dense locally connected structure;
- or high-degree hub-like distortion.

## Failure condition 1
If Forman curvature diverges or is dominated by degree artifacts, it cannot serve as \(R^{(3)}\).

---

# 3. Ollivier-style overlap curvature proxy

## Definition 2
For neighboring nodes \(i,j\), define:

\[
O_{ij}
=
\frac{|N(i)\cap N(j)|}{|N(i)\cup N(j)|}.
\]

This is a cheap Ollivier-like proxy: adjacent nodes have positive curvature when their neighbor measures overlap strongly.

It is not optimal transport Ollivier curvature, but it is finite, local, and graph-native.

## Derivation target A
Replace the overlap proxy with true Ollivier-Ricci curvature using Wasserstein distance between neighbor measures.

---

# 4. Scalar slice curvature proxy

## Definition 3
Define slice scalar curvature proxy:

\[
R^{(3)}_{\mathrm{graph},k}
=
\langle O_{ij}\rangle_{e\in E_k}
+
\frac{\langle F_{ij}\rangle_{e\in E_k}}{|E_k|}.
\]

This combines:
- overlap curvature for local graph geometry;
- degree-weighted Forman correction.

## Observation
This is still a graph-curvature proxy. It is better than a pure spectral placeholder, but it is not continuum \(R^{(3)}\).

---

# 5. Verifier implementation

## Status
**Implemented as `spatial_graph_curvature_verifier.py`. Execution log captured.**

The verifier tests:

1. enough valid antichain spatial slices;
2. enough graph edges;
3. finite Forman curvature distribution;
4. finite Ollivier-overlap proxy;
5. finite scalar \(R^{(3)}_{\mathrm{graph}}\);
6. bounded curvature spread.

## Captured verifier output

```text
Spatial graph curvature verifier
==================================================
Route:
antichain spatial graph + h_ab proxy -> Forman/Ollivier-like R3 graph curvature proxy
This is not continuum R^(3), but replaces the pure spectral placeholder.

PASS: 90.0
SOFT_FAIL: 1.6666666666666667
HARD_FAIL: 8.333333333333334
n_slices_median: 9.0
median_edges_median: 213.5
forman_median_median: -14.999999999984999
forman_iqr_median: 4.986625436539217
ollivier_proxy_median_median: 0.3157894736842105
scalar_R3_median_median: 0.26992776747543495
finite_fraction_median: 1.0
```

---

# 6. What this file establishes

### Established at current proof level

1. A graph-native \(R^{(3)}\) proxy is defined.
2. Forman-style edge curvature is explicit.
3. Ollivier-style overlap curvature is explicit.
4. Slice scalar curvature proxy is explicit.
5. The verifier confirms finite stable curvature estimates in sampled regimes.

### Not yet proved

1. True Ollivier-Ricci curvature is not implemented.
2. Continuum \(R^{(3)}\) convergence is not shown.
3. Curvature normalization is not uniquely derived.
4. Graph curvature is not yet coupled to \(h_{ab}\) beyond graph construction.
5. Boundary terms remain open.

---

# 7. Updated ADM action target

Replace the spectral placeholder in `ADM_ACTION_WITH_LAPSE.md`:

\[
R^{(3)}_{\mathrm{proxy},k}
\]

with:

\[
R^{(3)}_{\mathrm{graph},k}.
\]

The action becomes:

\[
S_{\mathrm{proxy}}^{(N,R_3)}
=
\sum_k
N_k\sqrt{\det h_k}
\left(
R^{(3)}_{\mathrm{graph},k}
+
K_{ab}K^{ab}
-
K^2
\right)
\Delta k.
\]

---

# 8. Next derivation target

The next file should be:

```text
ADM_ACTION_WITH_GRAPH_CURVATURE.md
```

Its job is to integrate measured lapse and explicit spatial graph curvature into the ADM-like action proxy and test whether the action remains finite and stable.

---

# Honest status line

> `SPATIAL_GRAPH_CURVATURE.md` replaces the pure spectral spatial-curvature placeholder with explicit graph-curvature proxies. It strengthens the ADM action ingredients but does not yet prove continuum \(R^{(3)}\) convergence.

**End of file.**
