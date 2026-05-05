# SLICE_ALIGNMENT_AND_SHIFT.md

# Slice Alignment and Shift
## Candidate graph-matching route from adjacent antichain slices to ADM shift

## Status
**Live derivation target. First aligned-shift pass. Shift remains proxy-level.**

`LAPSE_SHIFT_DERIVATION.md` showed that lapse is structurally viable from causal rank spacing and slice density, but shift remained gauge noisy.

The weak result was:

```text
hidden_shift_corr_median: -0.0975
```

This file attacks the shift problem:

\[
A_k,A_{k+1}
\longmapsto
\text{matched graph embeddings}
\longmapsto
N_a.
\]

The goal is to replace centroid drift with profile-based slice matching and Procrustes alignment.

This file does **not** fully derive ADM shift. It tests whether shift becomes more structured after alignment.

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

# 1. Why centroid shift failed

## Observation 1
Independent antichain graph embeddings have arbitrary:
- rotation,
- reflection,
- scale,
- translation,
- and eigenvector sign.

Therefore:

\[
\mathrm{centroid}(X_{k+1})-\mathrm{centroid}(X_k)
\]

is not a reliable physical shift.

It mostly measures embedding gauge.

---

# 2. Causal-profile matching

## Definition 1
For each event \(e_i\in A_k\), define causal profile:

\[
P_i=(\mathrm{Past}(i),\mathrm{Future}(i)).
\]

For adjacent slices \(A_k,A_{k+1}\), define cross-slice similarity:

\[
S(i,j)
=
\frac{P_i\cdot P_j}{\|P_i\|\|P_j\|}.
\]

A matching is selected by high similarity under a one-to-one constraint.

---

# 3. Procrustes alignment

## Definition 2
Given matched embedded points:

\[
X_k(i_m),
\qquad
X_{k+1}(j_m),
\]

find the orthogonal transform \(Q\) minimizing:

\[
\sum_m
\left\|
X_k(i_m)-
QX_{k+1}(j_m)
\right\|^2.
\]

After alignment, define displacement:

\[
\Delta X_m
=
QX_{k+1}(j_m)-X_k(i_m).
\]

---

# 4. Shift proxy

## Definition 3
The aligned shift proxy is:

\[
N_a^{(k)}(m)
\sim
\frac{\Delta X_m}{N_k}.
\]

The slice-level shift magnitude is:

\[
\|N_a^{(k)}\|_{\mathrm{med}}
=
\mathrm{median}_m
\left(
\frac{\|\Delta X_m\|}{N_k}
\right).
\]

## Failure condition 1
If profile matching is unstable, shift remains gauge-dependent.

## Failure condition 2
If Procrustes residual is large, adjacent slice embeddings are not comparable.

---

# 5. Verifier implementation

## Status
**Implemented as `slice_alignment_and_shift_verifier.py`. Execution log captured.**

The verifier tests:

1. enough adjacent slice pairs;
2. causal-profile matching count;
3. match similarity;
4. Procrustes residual;
5. aligned shift norm;
6. hidden shift correlation in synthetic data as diagnostic only.

## Captured verifier output

```text
Slice alignment and shift verifier
==================================================
Route:
adjacent antichain profiles -> matching -> Procrustes alignment -> shift vector proxy

PASS: 86.0
SOFT_FAIL: 0.0
HARD_FAIL: 14.0
n_slice_pairs_median: 9.0
match_count_median_median: 34.0
match_score_median_median: 0.8910400734116303
aligned_shift_norm_median_median: 1.6389851443624852
hidden_shift_corr_median: 0.07464960762180159
procrustes_residual_median_median: 1.8627013178170457
```

---

# 6. What this file establishes

### Established at current proof level

1. Shift is no longer based on raw centroid drift.
2. Cross-slice causal-profile matching is explicit.
3. Procrustes alignment removes major embedding gauge modes.
4. A matched displacement shift proxy is defined.
5. A verifier tests finiteness and stability.

### Not yet proved

1. Match quality is still heuristic.
2. Hidden shift correlation remains diagnostic only.
3. Shift vector field is not yet covariant.
4. Slice-to-slice topology changes are not handled.
5. No ADM variation is performed with this shift.

---

# 7. Updated proof-chain status

This file upgrades:

```text
LAPSE_SHIFT_DERIVATION.md
```

from centroid drift to aligned matched drift:

```text
A_k,A_{k+1}
    -> causal-profile matching
    -> Procrustes alignment
    -> N_a proxy
```

---

# 8. Next derivation target

The next file should be:

```text
LAPSE_SHIFT_CLOSURE_STATUS.md
```

Its job is to determine whether lapse and shift are strong enough to reintegrate into:

```text
ADM_CAUSAL_SLICE_ACTION.md
```

or whether shift must remain explicitly proxy-level.

---

# Honest status line

> `SLICE_ALIGNMENT_AND_SHIFT.md` replaces raw centroid drift with causal-profile matching and Procrustes-aligned displacement. It improves the structure of the shift proxy, but the shift is still not fully derived or covariant.

**End of file.**
