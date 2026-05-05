# LAPSE_SHIFT_CLOSURE_STATUS.md

# Lapse and Shift Closure Status
## Audit of ADM lapse and shift derivation status for causal-slice geometry

## Status
**Closure audit. Not a proof.**

This file audits the lapse/shift seam after two verifier-backed passes:

```text
LAPSE_SHIFT_DERIVATION.md
SLICE_ALIGNMENT_AND_SHIFT.md
```

The purpose is to determine whether the causal-slice ADM route can safely replace the earlier assumptions:

```text
N = 1
N_a = 0
```

with measured or derived quantities.

---

# 1. Prior state

Earlier files used the block-diagonal Lorentzian metric:

\[
g_{\mu\nu}
=
\begin{pmatrix}
-N^2 & 0 \\
0 & h_{ab}
\end{pmatrix}
\]

with:

\[
N=1,
\qquad
N_a=0.
\]

This was useful for first-pass signature and action tests, but it was not a derived ADM structure.

---

# 2. Lapse result

## Evidence

`LAPSE_SHIFT_DERIVATION.md` tested:

\[
N_k
\sim
\frac{\Delta k}{\sqrt{V_k/\bar V}},
\]

where:
- \(\Delta k\) is causal-rank spacing;
- \(V_k=|A_k|\) is antichain slice volume proxy;
- \(\bar V\) is median slice volume.

Verifier result:

```text
PASS: 93.33%
SOFT_FAIL: 0.0%
HARD_FAIL: 6.67%
```

Key diagnostics:

```text
n_slice_pairs_median: 8.5
lapse_median_median: 1.0000
lapse_cv_median: 0.0608
shift_finite_fraction_median: 1.0
```

## Audit classification

```text
Lapse status: verifier-backed candidate
```

## Interpretation

The lapse candidate is structurally viable.

It is:
- finite;
- positive;
- stable across slices;
- low-variance;
- derived from causal rank and slice density.

It is not yet uniquely derived, but it is strong enough to replace the fixed assumption:

```text
N = 1
```

with a measured lapse proxy:

```text
N = N[k,V_k].
```

---

# 3. Shift result: first centroid proxy

## Evidence

The first shift proxy in `LAPSE_SHIFT_DERIVATION.md` used centroid drift:

\[
N_a^{(k)}
\sim
\frac{
\mathrm{centroid}(X_{k+1})-\mathrm{centroid}(X_k)
}{
N_k
}.
\]

Verifier diagnostic:

```text
hidden_shift_corr_median: -0.0975
```

## Audit classification

```text
Centroid shift status: failed / gauge-noisy proxy
```

## Interpretation

Raw centroid drift is not physically reliable because independent graph embeddings have arbitrary:
- translation;
- rotation;
- reflection;
- scaling;
- eigenvector sign.

This shift estimate mostly measures embedding gauge.

---

# 4. Shift result: aligned slice proxy

## Evidence

`SLICE_ALIGNMENT_AND_SHIFT.md` replaced raw centroid drift with:

```text
adjacent antichain profiles
        ↓
causal-profile matching
        ↓
graph embedding
        ↓
Procrustes alignment
        ↓
matched displacement shift proxy
```

Verifier result:

```text
PASS: 86.0%
SOFT_FAIL: 0.0%
HARD_FAIL: 14.0%
```

Key diagnostics:

```text
n_slice_pairs_median: 9.0
match_count_median: 34.0
match_score_median: 0.891
aligned_shift_norm_median: 1.639
hidden_shift_corr_median: 0.0746
procrustes_residual_median: 1.863
```

## Audit classification

```text
Aligned shift status: structured proxy, not closed
```

## Interpretation

The aligned shift is better than centroid drift because:
- matching is explicit;
- match similarity is high;
- displacement is computed after Procrustes alignment;
- residual is finite;
- the hidden correlation improved from negative to weak positive.

However:

```text
hidden_shift_corr_median: 0.0746
```

is still too weak to claim physical shift recovery.

Thus \(N_a\) remains open.

---

# 5. Safe reintegration into ADM_CAUSAL_SLICE_ACTION.md

## Safe update

It is safe to update the ADM causal-slice action to use measured lapse:

\[
N_k
=
\frac{\Delta k}
{\sqrt{(V_k+V_{k+1})/(2\bar V)}}.
\]

This replaces:

```text
N = 1
```

with:

```text
N = N_k
```

as a verifier-backed candidate.

## Unsafe update

It is not yet safe to replace:

```text
N_a = 0
```

with the aligned shift as if it were physically derived.

The safer wording is:

```text
N_a = 0 in the main ADM proxy;
aligned N_a is logged as a diagnostic field only.
```

or:

```text
N_a may be included in an exploratory shifted-ADM variant, but it is not part of the main claimed derivation.
```

---

# 6. Updated ADM proxy recommendation

## Recommended main action

Use:

\[
S_{\mathrm{proxy}}^{(N)}
=
\sum_k
N_k\sqrt{h_k}
\left(
R^{(3)}_{\mathrm{proxy},k}
+
K_{ab}^{(k)}K^{ab}_{(k)}
-
K_k^2
\right)
\Delta k.
\]

with:

\[
N_a=0.
\]

## Recommended diagnostic variant

Track an exploratory shifted version:

\[
S_{\mathrm{proxy}}^{(N,N_a)}
\]

only as a diagnostic, with explicit label:

```text
not used for closure claims
```

until shift alignment improves.

---

# 7. Remaining shift closure targets

To close shift, the next work must improve:

## 7.1 Cross-slice correspondence

Current matching is profile-similarity greedy matching.

Needed:
- optimal transport matching;
- mutual nearest-neighbor filtering;
- causally constrained matching;
- persistence across multiple slices.

## 7.2 Gauge-stable embedding alignment

Needed:
- spectral sign stabilization;
- multi-slice Procrustes;
- temporal smoothing;
- graph-diffusion coordinates;
- reference-frame locking.

## 7.3 Vector-field shift

Current shift is a magnitude/displacement proxy.

Needed:

\[
N_a(x)
\]

as a spatial vector field over each slice.

## 7.4 Covariant role

Needed:
- proof that the shift enters ADM consistently;
- not merely as embedding drift.

---

# 8. Closure classification

| Quantity | Status | Evidence | Safe use |
|---|---:|---|---|
| \(N\) lapse | Verifier-backed candidate | PASS 93.33%, low CV | Main ADM proxy |
| raw centroid \(N_a\) | Failed proxy | hidden corr -0.0975 | Do not use |
| aligned \(N_a\) | Structured proxy / open | PASS 86%, hidden corr 0.0746 | Diagnostic only |
| full ADM \(N,N_a\) | Not closed | shift unresolved | Not yet |

---

# 9. Updated proof-chain status

The causal-slice action route should now be:

```text
CAUSAL_SLICE_LORENTZIAN_METRIC.md
        ↓
LAPSE_SHIFT_DERIVATION.md
        ↓
SLICE_ALIGNMENT_AND_SHIFT.md
        ↓
LAPSE_SHIFT_CLOSURE_STATUS.md
        ↓
ADM_CAUSAL_SLICE_ACTION.md
```

with the caveat:

```text
Use N_k in main action.
Keep N_a=0 in main action.
Log aligned N_a as diagnostic only.
```

---

# 10. Next derivation target

The next file should be:

```text
ADM_ACTION_WITH_LAPSE.md
```

Its job:

\[
S_{\mathrm{proxy}}^{(N)}
=
\sum_k
N_k\sqrt{h_k}
\left(
R^{(3)}
+
K_{ab}K^{ab}
-
K^2
\right)
\Delta k
\]

and to test whether measured lapse improves or destabilizes the ADM-like action proxy.

---

# Honest status line

> Lapse is strong enough to move from fixed \(N=1\) to measured \(N_k\) in the main ADM proxy. Shift is not closed. The aligned shift proxy is structurally better than centroid drift but remains diagnostic-only until cross-slice matching and gauge-stable vector-field recovery improve.

**End of file.**
