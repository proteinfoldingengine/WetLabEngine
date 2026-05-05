# ADM_CAUSAL_SLICE_ACTION.md

# ADM Causal Slice Action
## Candidate action proxy from causal-slice Lorentzian geometry

## Status
**Live derivation target. First ADM-like action pass. Not Einstein-Hilbert closed.**

`CAUSAL_SLICE_CURVATURE.md` introduced finite slice-to-slice curvature-like diagnostics for the causal-slice metric sequence:

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
(h_{ab},N,N_a,K_{ab},R^{(3)})
\longmapsto
S_{\mathrm{geom}}.
\]

The current file does **not** derive the full ADM or Einstein-Hilbert action. It builds a first action proxy from:
- antichain spatial metric \(h_{ab}\),
- first-pass lapse \(N=1\),
- zero shift,
- finite-difference extrinsic curvature proxy,
- graph spectral intrinsic-curvature proxy.

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

# 1. ADM target

The ADM decomposition of the gravitational action has the schematic form:

\[
S_{\mathrm{ADM}}
=
\int dt\,d^3x\,
N\sqrt{h}
\left(
R^{(3)}
+
K_{ab}K^{ab}
-
K^2
\right)
\]

up to convention-dependent signs and boundary terms.

The causal-slice target is:

\[
S_{\mathrm{geom}}^{\mathrm{slice}}
=
\sum_k
N_k\sqrt{h_k}
\left(
R_k^{(3)}
+
K_{ab}^{(k)}K^{ab}_{(k)}
-
K_k^2
\right)
\Delta\tau_k.
\]

---

# 2. First-pass assumptions

## Definition 1
The first pass uses:

\[
N_k=1,
\qquad
N_a=0.
\]

Thus:

\[
K_{ab}^{(k)}
\approx
\frac12
\frac{
h_{ab}^{(k+1)}-h_{ab}^{(k)}
}{
\Delta\tau_k
}.
\]

## Failure condition 1
If lapse and shift cannot be derived from causal data, this file remains a proxy rather than a full ADM derivation.

---

# 3. Spatial curvature proxy

## Definition 2
The intrinsic spatial curvature proxy \(R^{(3)}_k\) is estimated from graph spectral roughness of the antichain spatial graph.

This is a placeholder for true graph/Ricci curvature.

## Derivation target A
Replace the spectral proxy with a real graph curvature estimator:
- Ollivier-Ricci curvature,
- Forman-Ricci curvature,
- Regge-like spatial deficit curvature,
- or finite-difference curvature on embedded antichain coordinates.

---

# 4. Extrinsic curvature proxy

## Definition 3
Given \(h_{ab}^{(k)}\), define:

\[
\dot h_{ab}^{(k)}
\approx
\frac{
h_{ab}^{(k+1)}-h_{ab}^{(k)}
}{
\Delta\tau_k
}.
\]

With first-pass \(N=1\), \(N_a=0\):

\[
K_{ab}^{(k)}
=
\frac12\dot h_{ab}^{(k)}.
\]

Then:

\[
K^{a}_{\ b}
=
h^{ac}K_{cb}.
\]

The kinetic ADM scalar is:

\[
K_{ab}K^{ab}-K^2
=
\mathrm{Tr}(K^2)-(\mathrm{Tr}K)^2.
\]

---

# 5. Action proxy

## Definition 4
The first action proxy is:

\[
S_{\mathrm{proxy}}
=
\sum_k
\sqrt{\det h_k}
\left(
R^{(3)}_{\mathrm{proxy},k}
+
K_{ab}^{(k)}K^{ab}_{(k)}
-
K_k^2
\right).
\]

This is not yet the Einstein-Hilbert action, but it tests whether the causal-slice ingredients can be assembled into a finite action-like scalar.

---

# 6. Verifier implementation

## Status
**Implemented as `adm_causal_slice_action_verifier.py`. Execution log captured.**

The verifier tests:

1. enough valid spatial metric slices;
2. finite \(\sqrt{\det h}\);
3. finite extrinsic-curvature proxy;
4. finite graph spectral \(R^{(3)}\) proxy;
5. finite ADM-like action sum;
6. action not dominated by singular metric slices.

## Captured verifier output

```text
ADM causal slice action verifier
==================================================
Route:
h_ab sequence -> K_ab proxy + R3 proxy -> ADM-like action sum
This is not full ADM/EH convergence.

PASS: 95.0
SOFT_FAIL: 0.0
HARD_FAIL: 5.0
n_slices_median: 9.0
action_proxy_median: 1536.5295729464574
action_abs_proxy_median: 1713.2725166548257
median_volume_median: 622.8593153687095
median_K_norm_median: 0.16377724219581252
median_R3_proxy_median: 0.4512541438778868
finite_fraction_median: 1.0
```

---

# 7. What this file establishes

### Established at current proof level

1. The causal-slice route now has a first ADM-like action scalar.
2. Extrinsic curvature proxy is explicit.
3. Spatial curvature placeholder is explicit.
4. The verifier checks finiteness and stability.

### Not yet proved

1. True \(R^{(3)}\) is not computed.
2. Lapse and shift are not derived.
3. Boundary terms are not addressed.
4. No convergence to Einstein-Hilbert is shown.
5. The action proxy is not yet variationally derived.
6. The memory/matter sectors are not coupled into this causal-slice action.

---

# 8. Theorem candidate

## Lemma candidate 1
If:

1. \(h_{ab}\) is derived from antichain graph geometry;
2. \(N\) and \(N_a\) are derived from causal slice evolution;
3. \(R^{(3)}\) is computed from spatial graph curvature;
4. \(K_{ab}\) converges under slice refinement;
5. the ADM sum converges;

then the causal-slice geometry supports a discrete geometric action approaching the Einstein-Hilbert action.

This is not yet proved.

---

# 9. Updated proof-chain status

The corrected causal geometry chain is now:

```text
CAUSAL_SLICE_LORENTZIAN_METRIC.md
        ↓
CAUSAL_SLICE_CURVATURE.md
        ↓
ADM_CAUSAL_SLICE_ACTION.md
        ↓
EINSTEIN_HILBERT_LIMIT.md
```

---

# 10. Next derivation target

The next file should be:

```text
CAUSAL_SLICE_CLOSURE_AUDIT.md
```

Its job is to audit the corrected causal route, update the status after the failed MDS branch, and identify the remaining hard gaps before reintegrating with `CONTINUUM_LIMIT.md`.

---

# Honest status line

> `ADM_CAUSAL_SLICE_ACTION.md` gives the first verifier-backed ADM-like action proxy from causal-slice geometry. It is a finite action-like scalar test, not a derivation of the Einstein-Hilbert action.

**End of file.**
