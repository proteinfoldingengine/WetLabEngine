# BOUNDARY_FLUX_TERMS.md

# Boundary Flux Terms
## Graph-boundary flux accounting for ADM/Bianchi conservation proxies

## Status
**Live derivation target. First graph-boundary flux pass. Not continuum boundary-term closure.**

`GRAPH_DIVERGENCE_CLOSURE_STATUS.md` identified boundary flux as the next conservation blocker.

Even with a graph-compatible divergence,

\[
D^a_{\mathcal G}\mathcal S_{ab}^{\mathrm{mem}},
\]

finite antichain slices can exchange flux through their graph boundary.

This file attacks:

\[
\partial A_k
\longmapsto
\text{graph boundary flux}.
\]

This file does **not** derive continuum boundary terms. It defines a graph-boundary flux proxy and verifies weak-memory scaling.

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

# 1. Why boundary flux is needed

A conservation law on a finite region has both interior divergence and boundary flux:

\[
\int_{A_k} D^aS_{ab}
+
\int_{\partial A_k} S_{ab}n^a
=
\text{source/sink}.
\]

The previous graph divergence improved the interior term. This file adds the boundary term.

---

# 2. Graph boundary nodes

## Definition 1
For an antichain spatial graph:

\[
\mathcal G_k=(A_k,E_k,W_k),
\]

define graph-boundary nodes as nodes with either:
- high radial distance from the graph centroid in embedded coordinates;
- or low graph degree / local density.

This gives a first boundary set:

\[
\partial A_k
=
\{i\in A_k : r_i \ge r_q \text{ or } \deg(i)\le d_q\}.
\]

This is a graph proxy, not a topological boundary theorem.

---

# 3. Boundary normal proxy

## Definition 2
For boundary node \(i\), define outward normal proxy:

\[
n_i^a
=
\frac{X_i^a-\bar X^a}{\|X_i-\bar X\|}.
\]

where \(\bar X\) is the embedded graph centroid.

---

# 4. Boundary flux proxy

## Definition 3
Given projected memory stress:

\[
\mathcal S_{ab}^{\mathrm{mem}}(i),
\]

define boundary flux at node \(i\):

\[
\Phi_i
=
n_i^a
\mathcal S_{ab}^{\mathrm{mem}}(i)
n_i^b.
\]

The total graph-boundary flux proxy is:

\[
\Phi_{\partial A}
=
\sum_{i\in\partial A_k}
w_i\Phi_i.
\]

The verifier uses the median absolute boundary-node flux as a stability diagnostic.

---

# 5. Weak-memory scaling

## Lemma candidate 1
If:

\[
\mathcal S_{ab}^{\mathrm{mem}}=O(\eta_{\mathrm{mem}})
\]

then:

\[
\Phi_{\partial A}=O(\eta_{\mathrm{mem}}).
\]

If only kinetic stress contributes:

\[
\mathcal S_{ab}^{\mathrm{kin}}=O(\eta_{\mathrm{mem}}^2),
\]

then:

\[
\Phi_{\partial A}^{\mathrm{kin}}=O(\eta_{\mathrm{mem}}^2).
\]

---

# 6. Verifier implementation

## Status
**Implemented as `boundary_flux_terms_verifier.py`. Execution log captured.**

The verifier constructs:
- an antichain-like spatial graph;
- embedded coordinates;
- graph-boundary nodes;
- projected memory stress;
- boundary normal proxies;
- boundary flux values.

It checks:

1. finite boundary flux;
2. boundary fraction is nontrivial;
3. flux is weak-memory suppressed;
4. total flux scales as \(O(\eta)\);
5. kinetic-only flux scales as \(O(\eta^2)\).

## Captured verifier output

```text
Boundary flux terms verifier
==================================================
Route:
graph boundary nodes + projected stress -> boundary flux proxy
Checks finite flux and weak-memory scaling.

PASS: 88.4
SOFT_FAIL: 11.6
HARD_FAIL: 0.0
boundary_fraction_median: 0.3888888888888889
flux_abs_median_median: 5.12362974652485e-05
flux_half_ratio_median: 0.49838122090563597
kinetic_half_ratio_median: 0.24999991906027905
finite_fraction_median: 1.0
```

---

# 7. What this file establishes

### Established at current proof level

1. A graph-boundary set is explicit.
2. A boundary normal proxy is explicit.
3. A memory-stress boundary flux proxy is explicit.
4. Weak-memory scaling is verified.

### Not yet proved

1. Boundary detection is heuristic.
2. Normals are embedding-dependent.
3. No graph Stokes theorem is proved.
4. Boundary flux is not yet integrated into the total residual verifier.
5. Continuum boundary convergence is not shown.

---

# 8. Integration into Bianchi branch

The conservation branch should now track:

\[
\mathcal B^{(k)}
=
Q_{\mathrm{mem}}^{(k)}
+
Q_{\mathrm{mat}}^{(k)}
+
\Phi_{\partial A}^{(k)}.
\]

At this stage, \(\Phi_{\partial A}\) is a diagnostic boundary flux term, not a closed correction.

---

# 9. Next derivation target

The next file should be:

```text
CONSERVATION_WITH_BOUNDARY_FLUX.md
```

Its job:

\[
Q_{\mathrm{mem}}
+
Q_{\mathrm{mat}}
+
\Phi_{\partial A}
\approx0
\]

at ADM graph-proxy level.

---

# Honest status line

> `BOUNDARY_FLUX_TERMS.md` adds a graph-boundary flux proxy for projected memory stress and verifies weak-memory scaling. It strengthens conservation accounting on finite antichain slices but does not prove continuum boundary-term closure.

**End of file.**
