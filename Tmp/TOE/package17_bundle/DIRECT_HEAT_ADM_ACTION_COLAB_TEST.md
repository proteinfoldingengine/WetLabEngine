# DIRECT_HEAT_ADM_ACTION_COLAB_TEST.md

# Direct Heat ADM Action Colab Test
## Testing the ADM spatial-curvature action using dx-normalized direct heat \(R^{(3)}\)

## Status
**Colab test script prepared. Not yet executed.**

`HEAT_CURVATURE_TO_ADM_ACTION.md` showed that the recovered 3D curvature signal can assemble into the ADM spatial curvature term:

\[
\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x.
\]

However, that test used the conductance proxy at larger grids.

This file prepares the stronger test: use the actual dx-normalized direct heat estimator:

\[
\widehat R_{\mathrm{heat}}^{(3)}
=
\frac{-6B_i}{dx}.
\]

Then assemble:

\[
I_R^{\mathrm{heat}}
=
\sum_i N_i\sqrt{h_i}\,\widehat R_i^{(3)}\,dx^3.
\]

---

# 1. What this test evaluates

This test evaluates only the spatial curvature term:

\[
I_R=\int_\Sigma N\sqrt h\,R^{(3)}\,d^3x.
\]

It does not include:

```text
extrinsic curvature
shift vector
causal slicing
time evolution
action variation
Einstein equations
```

So it is not full ADM closure.

---

# 2. Important zero-mode issue

The local heat estimator is primarily a centered curvature-shape estimator.

Therefore the script reports two versions:

## Mean-restored version

\[
\widehat R_{\mathrm{action}}
=
s(\widehat R-\langle\widehat R\rangle)+\langle R\rangle.
\]

This tests whether the recovered local curvature density assembles correctly when the curvature zero mode is supplied.

## No-mean-restoration version

\[
\widehat R_{\mathrm{action}}
=
s(\widehat R-\langle\widehat R\rangle).
\]

This tests whether the action can be recovered autonomously without the analytic curvature mean.

Expected:

```text
mean-restored should pass first
no-mean may fail
```

If no-mean fails, the next seam is zero-mode recovery.

---

# 3. Prepared script

Script created:

```text
direct_heat_adm_action_colab_test.py
```

Recommended first run:

```text
N = 8, 10, 12, 14
```

Use T4 GPU.

---

# 4. What to report back

After running in Colab, send:

1. `DIRECT HEAT ADM ACTION SUMMARY`
2. `CSV_ROWS`
3. GPU or CPU used.

---

# 5. Pass condition

A promising result requires:

```text
local_corr_R > 0.75
mean-restored action relative error < 0.15
mean-restored density correlation > 0.95
```

The no-mean result is tracked separately as the zero-mode test.

---

# Honest status line

> `DIRECT_HEAT_ADM_ACTION_COLAB_TEST.md` prepares the direct heat version of the ADM spatial-curvature action diagnostic. It tests whether dx-normalized local heat curvature can assemble into \(\int N\sqrt hR^{(3)}d^3x\), while separately exposing the zero-mode problem.

**End of file.**
