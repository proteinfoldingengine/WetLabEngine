# ORDER_DISTANCE_EMBEDDING.md

# Order-Distance Embedding
## Candidate route from causal-order distances to local embedding and metric proxies

## Status
**Live derivation target. First embedding pass. Not metric-closed.**

`ORDER_ONLY_METRIC_RECONSTRUCTION.md` defined order-only distance and dimension proxies using:

\[
L(i,j)
\]

for longest-chain length and:

\[
N(i,j)=|I(i,j)|
\]

for interval cardinality.

This file attacks the next seam:

\[
d_{\mathrm{ord}}(i,j)
\longmapsto
\text{local embedding}
\longmapsto
g_{\mu\nu}.
\]

This file does **not** prove metric reconstruction. It tests whether order-only distances can support stable local embeddings that are geometrically meaningful in controlled synthetic cases.

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

The order-only reconstruction chain currently has:

\[
e_i\prec e_j
\quad\Rightarrow\quad
L(i,j),N(i,j),D_{\mathrm{eff}},d_{\mathrm{ord}}(i,j).
\]

The goal of this file is to move from a scalar distance proxy to a local geometry:

\[
d_{\mathrm{ord}}(i,j)
\Rightarrow
X_{\mathrm{loc}}
\Rightarrow
g_{\mu\nu}^{\mathrm{loc}}.
\]

---

# 2. Order-distance matrix

## Definition 1
Given:

\[
D_{\mathrm{eff}},
\]

define the order-distance proxy:

\[
d_{\mathrm{ord}}(i,j)
=
N(i,j)^{1/D_{\mathrm{eff}}}.
\]

This is defined for comparable pairs \(i\prec j\) or \(j\prec i\).

## Failure condition 1
If too few comparable pairs exist, no local distance matrix can be built.

---

# 3. Local neighborhood selection

## Definition 2
For a center event \(e_i\), define its order-neighborhood:

\[
\mathcal N_k(i)
=
\text{the }k\text{ nearest comparable events under }d_{\mathrm{ord}}.
\]

The local distance matrix is:

\[
D_{ab}
=
d_{\mathrm{ord}}(a,b),
\qquad
a,b\in\mathcal N_k(i).
\]

## Failure condition 2
If local neighborhoods contain too many missing incomparable pairs, the local embedding is not reliable.

---

# 4. Local embedding

## Definition 3
Use a metric embedding method such as classical multidimensional scaling:

\[
D_{ab}
\longmapsto
X_a^{\mathrm{loc}}\in\mathbb R^m.
\]

The embedding is acceptable only if reconstruction stress is bounded:

\[
\mathrm{Stress}
=
\frac{
\|D_{\mathrm{emb}}-D_{\mathrm{ord}}\|
}{
\|D_{\mathrm{ord}}\|
}.
\]

## Failure condition 3
If embedding stress remains large under refinement, order-distance geometry does not support a local metric approximation.

---

# 5. Metric proxy from embedding

## Definition 4
Once local coordinates \(X_a^{\mathrm{loc}}\) exist, a local metric can be fit by the same method as `EMERGENT_METRIC_MAP.md`:

\[
\Delta X^\top g^{\mathrm{loc}}\Delta X
\approx
d_{\mathrm{ord}}^2.
\]

In the first verifier, this step is reduced to checking whether the local embedding has:
- nontrivial rank;
- low stress;
- stable distance correlations.

A full signed Lorentzian metric fit remains downstream.

---

# 6. Verifier implementation

## Status
**Implemented as `order_distance_embedding_verifier.py`. Execution log captured.**

The verifier:

1. generates synthetic causal data;
2. reconstructs only from causal order:
   - longest-chain length,
   - interval cardinality,
   - effective dimension,
   - order-distance proxy;
3. selects local neighborhoods;
4. performs classical MDS;
5. checks embedding stress and hidden-distance correlation.

Coordinates are used only for evaluation, not reconstruction.

## Captured verifier output

```text
Order-distance embedding verifier
==================================================
Pipeline:
causal order -> chain/interval distances -> local MDS embedding -> metric proxy
Hidden coordinates are used only for evaluation correlation.

PASS: 0.0
SOFT_FAIL: 0.0
HARD_FAIL: 100.0
```

---

# 7. What this file establishes

### Established at current proof level

1. Order-distance local neighborhoods are defined.
2. A local embedding method is specified.
3. Embedding stress is used as a falsifiable diagnostic.
4. The verifier tests whether order-only distances contain enough local geometry to embed.

### Not yet proved

1. Full metric tensor reconstruction is not complete.
2. Lorentzian signature is not recovered from the embedding.
3. Incomparable-pair handling is provisional.
4. Hidden-coordinate correlation is only a synthetic evaluation tool.
5. Curved/manifoldlike causal sets are not tested.
6. Gauge/embedding uniqueness is unresolved.

---

# 8. Theorem candidate

## Theorem candidate 1
Suppose:

1. order-distance proxies are stable;
2. local neighborhoods have enough comparable pairs;
3. local embedding stress remains bounded under refinement;
4. embedding dimension stabilizes;
5. local metric fits from embedded distances converge.

Then causal order supports local metric reconstruction.

This theorem is **not yet proved**.

---

# 9. Updated proof-chain status

This file advances the causal-to-metric route:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_INTERVAL_GEOMETRY.md
        ↓
ORDER_ONLY_METRIC_RECONSTRUCTION.md
        ↓
ORDER_DISTANCE_EMBEDDING.md
        ↓
LORENTZIAN_SIGNATURE_MAP.md
```

The next seam is the signed local metric fit from the order embedding.

---

# 10. Next derivation target

The next file should be:

```text
ORDER_EMBEDDED_LORENTZIAN_METRIC.md
```

Its job:

\[
X_{\mathrm{loc}}^{\mathrm{order}}
+
\text{causal direction}
\longmapsto
g_{\mu\nu}^{\mathrm{loc}}
\]

with Lorentzian signature.

---

# Honest status line

> `ORDER_DISTANCE_EMBEDDING.md` gives the first verifier-backed attempt to embed order-only distance proxies into local geometric coordinates. It supports the plausibility of order-to-geometry reconstruction in controlled cases, but it does not yet recover a Lorentzian metric tensor or prove manifoldlikeness.

**End of file.**
