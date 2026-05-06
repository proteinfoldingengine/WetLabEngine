# GRAPH_COVARIANT_DIVERGENCE.md

# Graph-Covariant Divergence
## Replacing finite-difference memory-stress divergence with antichain graph divergence

## Status
**Live derivation target. First graph-divergence pass. Not continuum covariant derivative closure.**

`Bianchi_CLOSURE_STATUS.md` identified the next blocker:

\[
D^a\mathcal S_{ab}^{\mathrm{mem}}
\]

must be computed on the antichain spatial graph, not by a simple index finite difference.

This file attacks:

\[
\mathcal G_k,h_{ab}^{(k)},\mathcal S_{ab}^{\mathrm{mem},k}
\longmapsto
D^a\mathcal S_{ab}^{\mathrm{mem},k}.
\]

This file does **not** prove continuum covariant divergence. It defines a graph-compatible divergence operator on antichain spatial graphs and verifies weak-memory scaling.

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

# 1. Input objects

Given a causal antichain slice \(A_k\), prior files provide:

\[
\mathcal G_k=(A_k,E_k,W_k),
\]

\[
h_{ab}^{(k)},
\]

and projected memory stress:

\[
\mathcal S_{ab}^{\mathrm{mem},k}(i)
\]

at graph node \(i\).

---

# 2. Edge-direction graph divergence

## Definition 1
Let \(X_i^a\) be embedded graph coordinates from the antichain graph metric proxy.

For each edge \(i\to j\), define unit edge direction:

\[
u_{ij}^a
=
\frac{X_j^a-X_i^a}{\|X_j-X_i\|}.
\]

Define graph divergence:

\[
(D^aS_{ab})(i)
\approx
\sum_{j\in N(i)}
W_{ij}
u_{ij}^a
\left[
S_{ab}(j)-S_{ab}(i)
\right].
\]

The result is a spatial vector at node \(i\).

This is graph-compatible because it uses:
- graph neighbors;
- edge weights;
- embedded edge directions;
- tensor differences across graph edges.

---

# 3. Weak-memory scaling

## Lemma candidate 1
If:

\[
S_{ab}^{\mathrm{mem}}=O(\eta_{\mathrm{mem}})
\]

for interaction-dominated terms, then:

\[
D^aS_{ab}^{\mathrm{mem}}=O(\eta_{\mathrm{mem}}).
\]

If only kinetic terms are present:

\[
S_{ab}^{\mathrm{kin}}=O(\eta_{\mathrm{mem}}^2),
\]

so:

\[
D^aS_{ab}^{\mathrm{kin}}=O(\eta_{\mathrm{mem}}^2).
\]

The verifier checks both scalings.

---

# 4. Verifier implementation

## Status
**Implemented as `graph_covariant_divergence_verifier.py`. Execution log captured.**

The verifier constructs:
- a connected spatial graph;
- graph embedding coordinates;
- positive-definite spatial metric;
- projected memory stress tensors;
- graph-compatible divergence.

It checks:

1. finite graph divergence;
2. graph connectivity;
3. total divergence \(O(\eta)\) scaling;
4. kinetic-only divergence \(O(\eta^2)\) scaling;
5. no hard singular failures.

## Captured verifier output

```text
Graph covariant divergence verifier
==================================================
Route:
antichain graph + projected stress S_ab -> graph-compatible D^a S_ab
Checks finite divergence and weak-memory scaling.

PASS: 91.6
SOFT_FAIL: 8.4
HARD_FAIL: 0.0
graph_div_norm_median_median: 0.00031640429181109715
graph_div_half_ratio_median: 0.4978963633431301
kinetic_half_ratio_median: 0.24999998906354332
finite_fraction_median: 1.0
graph_connectivity_fraction_median: 1.0
```

---

# 5. What this file establishes

### Established at current proof level

1. A graph-compatible divergence operator is explicit.
2. The operator acts on projected memory stress tensors.
3. It uses antichain graph geometry rather than arbitrary index order.
4. Weak-memory scaling is verified.

### Not yet proved

1. This is not continuum \(D^aS_{ab}\).
2. Embedding-gauge dependence remains.
3. Christoffel / connection terms are not explicitly derived.
4. Boundary flux terms are not included.
5. Lapse/shift dependence is not included.
6. Continuum convergence is not shown.

---

# 6. Integration into Bianchi branch

This file upgrades:

```text
MEMORY_EXCHANGE_CURRENT_ADM.md
```

by replacing simple spatial finite differences with:

\[
Q_a^{\mathrm{mem}}
\sim
D^b_{\mathcal G}\mathcal S_{ab}^{\mathrm{mem}}.
\]

This strengthens the ADM Bianchi/conservation proxy.

---

# 7. Next derivation target

The next file should be:

```text
GRAPH_DIVERGENCE_CLOSURE_STATUS.md
```

Its job:
- audit whether graph divergence is strong enough to replace finite-difference divergence;
- update the Bianchi closure status;
- identify remaining gaps to continuum covariant derivative.

---

# Honest status line

> `GRAPH_COVARIANT_DIVERGENCE.md` replaces the arbitrary finite-difference divergence proxy with a graph-compatible divergence over antichain spatial geometry. It verifies weak-memory scaling but does not yet prove continuum covariant divergence.

**End of file.**
