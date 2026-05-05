# LAPSE_SHIFT_DERIVATION.md

# Lapse and Shift Derivation
## Candidate route from causal slice structure to ADM lapse and shift

## Status
**Live derivation target. First lapse/shift pass. Not ADM closed.**

`CAUSAL_SLICE_CLOSURE_AUDIT.md` identified lapse and shift as the next decisive seam.

Earlier files used the simplifying assumptions:

\[
N=1,
\qquad
N_a=0.
\]

This file attacks:

\[
\text{causal rank spacing, slice density, and slice-to-slice graph drift}
\longmapsto
N,\;N_a.
\]

This is a first-pass derivation program, not a completed ADM gauge construction.

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

# 1. ADM role of lapse and shift

The ADM metric is:

\[
g_{\mu\nu}
=
\begin{pmatrix}
-N^2+N_aN^a & N_b \\
N_a & h_{ab}
\end{pmatrix}.
\]

Previous causal-slice files used:

\[
N=1,\qquad N_a=0.
\]

That is acceptable for a first verifier, but not enough for a derived continuum limit.

---

# 2. Lapse from causal rank spacing

## Definition 1
Let causal slices be indexed by longest-chain depth:

\[
k=d(e).
\]

Let slice volume proxy be:

\[
V_k=|A_k|.
\]

Define first-pass lapse:

\[
N_k
=
\frac{\Delta k}{\sqrt{V_k/\bar V}},
\]

or, for adjacent slices:

\[
N_{k,k+1}
=
\frac{k_{+1}-k}{\sqrt{(V_k+V_{k+1})/(2\bar V)}}.
\]

Interpretation:
- rank spacing supplies causal time separation;
- slice density/volume normalizes proper-time scale.

## Failure condition 1
If \(N_k\le0\), singular, or wildly unstable, causal-rank time cannot supply ADM lapse.

---

# 3. Shift from slice-to-slice graph drift

## Definition 2
Let \(X_k\) be the graph-Laplacian embedding of antichain slice \(A_k\).

The first-pass shift proxy is slice-to-slice embedding drift:

\[
N_a^{(k)}
\sim
\frac{
\mathrm{centroid}(X_{k+1})-\mathrm{centroid}(X_k)
}{
N_k
}.
\]

Because slice embeddings have independent gauges, this is only a weak proxy until slice matching and Procrustes alignment are implemented.

## Failure condition 2
If slice-to-slice graph embeddings cannot be aligned, shift remains gauge-dependent.

---

# 4. Stronger shift target

## Derivation target A
Replace centroid drift with point-correspondence-free graph matching:

\[
A_k
\leftrightarrow
A_{k+1}
\]

using:
- shared causal futures/pasts,
- optimal transport between causal profiles,
- spectral graph alignment,
- Procrustes alignment after matching.

Then define:

\[
N_a
\]

as the drift vector field between aligned slices.

---

# 5. Verifier implementation

## Status
**Implemented as `lapse_shift_derivation_verifier.py`. Execution log captured.**

The verifier tests:

1. enough valid slice pairs;
2. finite positive lapse;
3. lapse coefficient of variation;
4. finite shift proxy;
5. hidden shift correlation in synthetic data as an evaluation-only diagnostic.

## Captured verifier output

```text
Lapse and shift derivation verifier
==================================================
Route:
rank spacing + slice density -> lapse N
slice-to-slice antichain embedding drift -> shift proxy N_a

PASS: 93.33333333333333
SOFT_FAIL: 0.0
HARD_FAIL: 6.666666666666667
n_slice_pairs_median: 8.5
lapse_median_median: 1.0000000000000098
lapse_cv_median: 0.06078055543310073
shift_norm_median_median: 0.06788315909892383
shift_finite_fraction_median: 1.0
hidden_shift_corr_median: -0.09750757047375347
```

---

# 6. What this file establishes

### Established at current proof level

1. A first lapse formula is defined from rank spacing and slice density.
2. A first shift proxy is defined from slice embedding drift.
3. The verifier tests finiteness and stability.
4. The lapse result is structurally stronger than the shift result.

### Not yet proved

1. Shift remains gauge-dependent.
2. Slice-to-slice correspondence is not solved.
3. Lapse normalization is not uniquely derived.
4. No ADM variation is performed.
5. No proof of coordinate/gauge covariance.

---

# 7. Updated proof-chain status

This file upgrades:

```text
CAUSAL_SLICE_LORENTZIAN_METRIC.md
```

from:

```text
N=1, N_a=0
```

toward:

```text
N=N[k,V_k], N_a=N_a[X_k,X_{k+1}]
```

The next seam is graph matching / slice alignment.

---

# 8. Next derivation target

The next file should be:

```text
SLICE_ALIGNMENT_AND_SHIFT.md
```

Its job:

\[
A_k,A_{k+1}
\longmapsto
\text{matched graph embeddings}
\longmapsto
N_a.
\]

---

# Honest status line

> `LAPSE_SHIFT_DERIVATION.md` gives the first verifier-backed lapse and shift derivation targets from causal slice data. Lapse is structurally viable from rank spacing and slice density, while shift remains a gauge-dependent proxy pending slice alignment.

**End of file.**
