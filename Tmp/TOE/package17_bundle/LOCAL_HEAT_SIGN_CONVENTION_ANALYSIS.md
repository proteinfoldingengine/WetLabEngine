# LOCAL_HEAT_SIGN_CONVENTION_ANALYSIS.md

# Local Heat Sign Convention Analysis
## Diagnosing the sign reversal in local heat-curvature density recovery

## Status
**Sign-convention diagnostic. Sign flip is promising. Not curvature closure.**

`LOCAL_HEAT_CURVATURE_DENSITY_TEST.md` produced a strong but sign-reversed local curvature signal:

```text
corr_with_R:   -0.921
corr_with_RdV: -0.991
sign_match_fraction: 0.174
```

That result was not random failure.

It indicated that the local heat-diagonal estimator was seeing the analytic curvature-density pattern, but with the opposite sign.

This file tests whether the reversal is a convention issue or a deeper operator failure.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Observation**
- **Definition**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving graph-to-continuum curvature convergence.

---

# 1. Continuum sign convention issue

There are two common Laplacian conventions.

## Positive semidefinite convention

Many graph Laplacians use:

\[
L=D-W\ge0.
\]

The heat operator is:

\[
e^{-tL}.
\]

## Analyst convention

Many differential-geometry references use:

\[
\Delta=\nabla^a\nabla_a
\]

with sign conventions that may make \(\Delta\) nonpositive.

The heat operator may be written:

\[
e^{t\Delta}.
\]

These are equivalent if:

\[
L=-\Delta.
\]

But the sign of coefficients extracted from a graph-local fit can depend on how the discrete operator, heat diagonal, and curvature convention are matched.

---

# 2. What the previous test showed

The previous local estimate used:

\[
Y_i(t)=K_{\mathcal G}(t,i,i)(4\pi t),
\]

then fit:

\[
Y_i(t)\approx A_i+B_it.
\]

It interpreted:

\[
\widehat R_i=6B_i.
\]

But the result was strongly anti-correlated with analytic \(R_i\).

This suggests the current graph convention may require:

\[
\widehat R_i=-6B_i
\]

instead of:

\[
\widehat R_i=6B_i.
\]

---

# 3. Verifier implementation

## Status
**Implemented as `local_heat_sign_convention_analysis_verifier.py`. Execution log captured.**

The verifier compares:

1. the original local heat slope;
2. the explicit sign-flipped coefficient.

It reports correlations with:

\[
R(x,y)
\]

and:

\[
R(x,y)dV.
\]

## Captured verifier output

```text
Local heat sign convention analysis verifier
==================================================
Route:
original local heat slope vs explicit sign-flipped coefficient

original_corr_R: -0.920030024111805
original_corr_RdV: -0.9903831286957712
original_sign_match: 0.09876543209876543
original_pos_gt_neg: False
original_mean_pos_R: -0.11315492524324891
original_mean_neg_R: 0.11315492524324877
sign_flipped_corr_R: 0.920030024111805
sign_flipped_corr_RdV: 0.9903831286957712
sign_flipped_sign_match: 0.9012345679012346
sign_flipped_pos_gt_neg: True
sign_flipped_mean_pos_R: 0.11315492524324891
sign_flipped_mean_neg_R: -0.11315492524324877
classification: SIGN_CONVENTION_FLIP_PROMISING
```

---

# 4. Result

The original field is strongly anti-correlated:

```text
original_corr_R: -0.920
original_corr_RdV: -0.990
```

The sign-flipped field is strongly correlated:

```text
sign_flipped_corr_R: 0.920
sign_flipped_corr_RdV: 0.990
```

Sign agreement improves to:

```text
sign_flipped_sign_match: 0.901
```

Classification:

```text
SIGN_CONVENTION_FLIP_PROMISING
```

---

# 5. Interpretation

This is a major local-curvature diagnostic milestone.

The local heat signal is not random. It tracks the analytic curvature-density structure very strongly.

The problem is the coefficient sign under the current graph/operator convention.

However, the sign flip still needs theoretical justification before being used as a curvature theorem.

---

# 6. What this establishes

### Established

1. The local heat signal is structured.
2. The corrected sign yields strong correlation with analytic curvature.
3. The corrected sign yields strong correlation with analytic curvature density.
4. Sign matching improves above 90%.

### Not established

1. The sign flip has not yet been derived from a discrete-to-continuum operator theorem.
2. The result has not yet been checked under grid refinement.
3. The result has not yet been extended to 3D.
4. The relation to integrated ADM action is still open.

---

# 7. Next derivation target

```text
LOCAL_HEAT_CURVATURE_REFINEMENT.md
```

Purpose:

Test whether the sign-corrected local curvature field remains correlated with analytic \(R(x,y)\) under grid refinement.

If correlation persists or improves as:

\[
N\uparrow,\quad dx\downarrow,
\]

this becomes a major local curvature-density result.

---

# Honest status line

> `LOCAL_HEAT_SIGN_CONVENTION_ANALYSIS.md` shows that the local heat-diagonal signal is strongly aligned with analytic curvature after a consistent sign correction. The sign correction is promising but still needs theoretical justification and refinement testing.

**End of file.**
