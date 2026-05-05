# CAUSAL_SLICE_CURVATURE.md

# Causal Slice Curvature
## Candidate curvature diagnostics from causal-slice Lorentzian metric assembly

## Status
**Live derivation target. First causal-slice curvature pass. Not full Riemann/Ricci closed.**

`CAUSAL_SLICE_LORENTZIAN_METRIC.md` assembled a local Lorentzian block metric:

\[
g_{\mu\nu}^{(k)}
=
\begin{pmatrix}
-N_k^2 & 0 \\
0 & h_{ab}^{(k)}
\end{pmatrix}.
\]

This file attacks the next seam:

\[
g_{\mu\nu}^{(k)}
\longmapsto
R_{\mu\nu},R.
\]

The current file does **not** compute the full Riemann tensor. It defines finite slice-variation curvature diagnostics and tests whether they are finite and stable.

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

The causal-slice metric provides a sequence:

\[
h_{ab}^{(k)}
\]

over causal-rank slices \(k\).

A full ADM curvature calculation would require:
- lapse \(N\),
- shift \(N_a\),
- extrinsic curvature \(K_{ab}\),
- intrinsic spatial curvature of \(h_{ab}\),
- and slice-to-slice derivative structure.

This first pass only tests whether finite slice-variation curvature proxies can be computed.

---

# 2. Metric velocity and acceleration

## Definition 1
Define slice metric velocity:

\[
V_h^{(k)}
=
\frac{\|h^{(k+1)}-h^{(k)}\|}{\Delta\tau_k}.
\]

Define slice metric acceleration:

\[
A_h^{(k)}
=
\frac{
\left\|
\frac{h^{(k+1)}-h^{(k)}}{\Delta\tau_k}
-
\frac{h^{(k)}-h^{(k-1)}}{\Delta\tau_{k-1}}
\right\|
}{
\Delta\tau
}.
\]

These are not curvature tensors, but they are first stability proxies for extrinsic-curvature-like behavior.

---

# 3. Log-volume curvature proxy

## Definition 2
For each spatial metric proxy:

\[
h_{ab}^{(k)},
\]

define log-volume:

\[
\ell_k
=
\frac12\log\det h^{(k)}.
\]

A scalar curvature-like slice proxy is:

\[
C_{\mathrm{vol}}^{(k)}
=
\left|
\ell_{k+1}-2\ell_k+\ell_{k-1}
\right|.
\]

This tracks second variation of spatial volume across causal time.

## Failure condition 1
If \(\det h^{(k)}\le0\) or log-volume variation is singular, curvature estimation fails.

---

# 4. Full ADM target

## Derivation target A
Replace the proxy diagnostics with ADM curvature:

\[
K_{ab}
=
\frac{1}{2N}
\left(
\dot h_{ab}
-
D_aN_b
-
D_bN_a
\right),
\]

and:

\[
R^{(4)}
=
R^{(3)}
+
K_{ab}K^{ab}
+
K^2
+
\text{boundary terms}
\]

(up to convention-dependent signs).

This requires:
- derived lapse,
- derived shift,
- spatial connection on antichain graph,
- intrinsic graph curvature for \(h_{ab}\).

---

# 5. Verifier implementation

## Status
**Implemented as `causal_slice_curvature_verifier.py`. Execution log captured.**

The verifier tests:

1. enough valid metric slices;
2. finite \(h_{ab}\) condition numbers;
3. finite metric velocity;
4. finite metric acceleration;
5. finite log-volume second variation;
6. stability under sampled causal-set regimes.

## Captured verifier output

```text
Causal slice curvature verifier
==================================================
Route:
slice Lorentzian metrics -> finite slice variation -> curvature proxies
This is not full Riemann/Ricci curvature.

PASS: 80.0
SOFT_FAIL: 2.5
HARD_FAIL: 17.5
n_metric_slices_median: 9.0
median_h_condition_median: 1.9882031855720235
median_metric_velocity_median: 57.63886410740121
median_metric_acceleration_median: 91.09527058275171
median_log_volume_curvature_median: 0.879519800945336
finite_fraction_median: 1.0
```

---

# 6. What this file establishes

### Established at current proof level

1. Slice-to-slice metric variation diagnostics are defined.
2. Log-volume curvature proxy is defined.
3. A verifier checks finite, stable curvature-like behavior.
4. Failure conditions are explicit.

### Not yet proved

1. Full ADM curvature is not computed.
2. Intrinsic spatial curvature of antichain graph is not computed.
3. Lapse and shift are not derived.
4. Boundary terms are not handled.
5. No Einstein-Hilbert action convergence is shown from this causal-slice geometry.

---

# 7. Theorem candidate

## Lemma candidate 1
If:

1. \(h_{ab}^{(k)}\) is positive definite on enough slices;
2. slice-to-slice derivatives are finite;
3. graph-intrinsic spatial curvature is defined;
4. lapse and shift are derived;
5. ADM curvature terms converge;

then causal-slice geometry supports a curvature scalar \(R\).

This is not yet proved.

---

# 8. Updated proof-chain status

The corrected causal-geometry chain is now:

```text
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
EINSTEIN_HILBERT_LIMIT.md
```

---

# 9. Next derivation target

The next file should be:

```text
ADM_CAUSAL_SLICE_ACTION.md
```

Its job:

\[
(h_{ab},N,N_a,K_{ab},R^{(3)})
\longmapsto
S_{\mathrm{geom}}.
\]

---

# Honest status line

> `CAUSAL_SLICE_CURVATURE.md` gives the first verifier-backed curvature-proxy diagnostics for the causal-slice Lorentzian metric route. It supports finite slice-to-slice curvature-like behavior, but it does not yet compute full ADM, Ricci, or scalar curvature.

**End of file.**
