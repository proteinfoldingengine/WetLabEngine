# CAUSAL_SLICE_LORENTZIAN_METRIC.md

# Causal Slice Lorentzian Metric
## Candidate assembly of local Lorentzian metric from causal time and antichain spatial geometry

## Status
**Live derivation target. First causal-slice Lorentzian assembly pass. Not curvature closed.**

`ANTICHAIN_GRAPH_METRIC.md` produced a verifier-backed spatial metric proxy:

\[
\mathcal G_k
\longmapsto
h_{ab}^{(k)}.
\]

This file attacks the next seam:

\[
(\tau,h_{ab})
\longmapsto
g_{\mu\nu}.
\]

The construction uses:
- causal rank / longest-chain depth as time;
- antichain graph metric as spatial geometry;
- a first lapse-only ADM-like assembly.

This file does **not** derive curvature, Einstein-Hilbert convergence, or full diffeomorphism covariance.

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

The corrected causal-set route now has:

\[
\text{causal order}
\Rightarrow
\tau
\]

from longest-chain depth, and:

\[
A_k
\Rightarrow
h_{ab}^{(k)}
\]

from antichain graph geometry.

The next target is assembling:

\[
g_{\mu\nu}
=
\begin{pmatrix}
-N^2+N_aN^a & N_b \\
N_a & h_{ab}
\end{pmatrix}.
\]

The first pass sets shift to zero:

\[
N_a=0.
\]

Thus:

\[
g_{\mu\nu}
=
\begin{pmatrix}
-N^2 & 0 \\
0 & h_{ab}
\end{pmatrix}.
\]

---

# 2. Causal time

## Definition 1
Let \(d(e_i)\) be longest-chain depth.

Define a first time function:

\[
\tau_i=\Delta\tau\,d(e_i).
\]

Here \(\Delta\tau\) is a coarse-grained causal-rank step.

## Failure condition 1
If longest-chain depth does not define a stable monotone time function, the Lorentzian assembly fails.

---

# 3. Spatial metric proxy

## Definition 2
For each antichain slice \(A_k\), the spatial metric proxy is:

\[
h_{ab}^{(k)}\sim C^{-1}_{ab},
\]

where:

\[
C^{ab}
=
\langle
\Delta X^a\Delta X^b
\rangle_{\text{graph neighbors}}.
\]

The embedded coordinates \(X^a\) come from graph Laplacian embedding of the antichain spatial graph.

## Failure condition 2
If \(h_{ab}\) is singular, ill-conditioned, or not positive definite, the local spatial metric fails.

---

# 4. Lorentzian assembly

## Definition 3
The first block Lorentzian metric candidate is:

\[
g_{\mu\nu}^{(k)}
=
\begin{pmatrix}
-N_k^2 & 0 \\
0 & h_{ab}^{(k)}
\end{pmatrix}.
\]

In the first verifier:

\[
N_k=1.
\]

## Lemma candidate 1
If:

\[
N_k^2>0
\]

and:

\[
h_{ab}^{(k)}
\]

is positive definite, then:

\[
g_{\mu\nu}^{(k)}
\]

has Lorentzian signature:

\[
(-,+,+,+).
\]

This is algebraic and does not yet prove physical covariance.

---

# 5. Shift and lapse targets

## Derivation target A
Derive lapse:

\[
N_k
\]

from causal-rank spacing, interval density, or longest-chain normalization.

## Derivation target B
Derive shift:

\[
N_a
\]

from slice-to-slice drift of antichain embeddings.

The current file sets \(N_a=0\), so it covers only the simplest block-diagonal Lorentzian assembly.

---

# 6. Verifier implementation

## Status
**Implemented as `causal_slice_lorentzian_metric_verifier.py`. Execution log captured.**

The verifier tests:

1. longest-chain depth/time correlation;
2. antichain graph spatial metric rank;
3. spatial metric condition number;
4. assembled Lorentzian signature;
5. assembled metric condition number.

## Captured verifier output

```text
Causal slice Lorentzian metric verifier
==================================================
Route:
longest-chain time + antichain spatial h_ab -> ADM-like block g_mu_nu

PASS: 78.75
SOFT_FAIL: 13.75
HARD_FAIL: 7.5
n_slices_used_median: 8.5
depth_time_corr_median: 0.9777411078654019
median_h_rank_median: 3.0
median_h_condition_median: 2.0462149979338617
signature_fraction_median: 1.0
median_g_condition_median: 88.24840056647994
```

---

# 7. What this file establishes

### Established at current proof level

1. The causal-set route now assembles a local block Lorentzian metric.
2. The spatial block \(h_{ab}\) comes from antichain graph geometry.
3. The time block comes from longest-chain depth.
4. Lorentzian signature is tested directly.
5. Failure conditions are explicit.

### Not yet proved

1. Lapse is not derived.
2. Shift is not derived.
3. Slice matching across time is not handled.
4. Curvature from the assembled metric is not computed.
5. Coordinate/gauge covariance is not proven.
6. This is not yet an Einstein-Hilbert limit.

---

# 8. Updated proof-chain status

The corrected causal-to-metric chain is now:

```text
CAUSAL_ORDER_DERIVATION.md
        ↓
CAUSAL_SET_RECONSTRUCTION.md
        ↓
ANTICHAIN_SPATIAL_GEOMETRY.md
        ↓
ANTICHAIN_GRAPH_METRIC.md
        ↓
CAUSAL_SLICE_LORENTZIAN_METRIC.md
        ↓
CURVATURE_ESTIMATION.md
```

---

# 9. Next derivation target

The next file should be:

```text
CAUSAL_SLICE_CURVATURE.md
```

Its job:

\[
g_{\mu\nu}^{(k)}
\longmapsto
R_{\mu\nu},
R
\]

using slice-to-slice variation and antichain spatial geometry.

---

# Honest status line

> `CAUSAL_SLICE_LORENTZIAN_METRIC.md` gives the first verifier-backed assembly of a local Lorentzian metric from causal rank time and antichain spatial metric proxies. It supports Lorentzian signature structurally, but lapse, shift, curvature, and covariance remain open.

**End of file.**
