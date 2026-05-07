# HEAT_NORMALIZATION_CAMPAIGN_QUICK_RESULT.md

# Heat Normalization Campaign — Quick Colab Result
## Analysis of local heat scaling and trace zero-mode failure mode

## Status
**Mixed result. Useful diagnostic. Not theorem closure.**

The Colab quick campaign completed on:

```text
Device: cuda
GPU: Tesla T4
QUICK_MODE: True
N = 8, 10, 12
amp = 0.08, 0.15, 0.22
```

Campaign classification:

```text
HEAT_NORMALIZATION_THEOREM_TARGET_MIXED
```

This is not a failure. It identifies two important issues in the heat-normalization program.

---

# 1. Local heat result

Best reported candidate:

```text
sign: -6
p: 2.0
corr_mean: 0.96106
corr_min: 0.92687
scale_cv: 0.12109
relL2_mean: 0.25860
relL2_max: 0.37538
```

The important part is not \(p=2\). The important part is:

```text
sign = -6
corr_mean ≈ 0.961
corr_min ≈ 0.927
```

So the local heat slope \(B_i\) has the correct curvature shape after negative sign.

---

# 2. Why \(p\) was not truly identified

The campaign compared:

\[
\widehat R_i=\mathrm{sign}\cdot B_i/dx^p.
\]

But then it allowed a fitted scale for every candidate:

\[
R_{\mathrm{scaled}}=s(\widehat R-\langle\widehat R\rangle).
\]

For a fixed grid \(dx\), changing \(p\) only multiplies the candidate by a constant:

\[
B_i/dx^p.
\]

That constant is absorbed by the fitted scale \(s\).

Therefore:

```text
correlation and centered relative L2 are identical across p.
```

Observed:

```text
all -6 candidates have corr_mean = 0.961063...
all -6 candidates have relL2_mean = 0.258602...
```

So the quick campaign did not prove \(p=2\). It only proved:

```text
negative local heat slope tracks curvature shape
```

The exponent \(p\) must be identified by **cross-grid amplitude stability without per-grid refitting**, or by direct theorem.

---

# 3. Trace zero-mode result

Trace summary:

```text
C_trace_required_mean: -0.03874
C_trace_required_cv:   0.84625
trace_raw_6_rel_error_mean: 333.79
classification: mixed
```

This looks bad, but the cause is clear.

The raw trace slope is dominated by the flat/background graph spectral term:

```text
N=8, amp=0.08:  trace_slope ≈ -82.90
N=8, amp=0.15:  trace_slope ≈ -83.23
N=8, amp=0.22:  trace_slope ≈ -83.77
```

The curvature signal is the small change in slope with geometry, not the absolute raw slope.

The previous successful zero-mode campaign worked because it effectively calibrated across amplitudes and learned this background offset. The theorem version must explicitly subtract the flat/reference trace slope.

---

# 4. Correct trace target

Instead of:

\[
I_R \sim C B_{\mathrm{raw}},
\]

use:

\[
I_R(a)-I_R(0)
\sim
C_{\Delta}
\left[
B(a)-B(0)
\right].
\]

For the conformal torus reference:

\[
I_R(0)=0.
\]

So:

\[
I_R(a)
\sim
C_{\Delta}
\Delta B(a).
\]

This is the correct global heat-trace theorem target.

---

# 5. Revised next campaign

The next Colab campaign should test:

## Local branch

Use a global scale learned on one subset and evaluate on held-out grids/amplitudes.

Report:

```text
heldout_relL2 by p
heldout_action_error by p
scale_cv across grids by p
```

This can identify \(p\) more honestly.

## Trace branch

Compute:

```text
B_flat(N) at amp=0
Delta_B(N,amp)=B(N,amp)-B_flat(N)
C_delta_required=I_R/Delta_B
```

Then test whether:

```text
C_delta_required
```

is stable across \(N\) and amplitude.

---

# 6. Updated interpretation

The quick campaign establishes:

```text
local heat sign/shape: good
local dx exponent: not identified by current test
raw trace slope: wrong object
trace delta slope: next object to test
```

---

# 7. Next file

```text
COLAB_HEAT_NORMALIZATION_DELTA_TRACE_CAMPAIGN.py
```

Purpose:

1. Add amp=0 flat reference.
2. Use trace slope difference:
   \[
   \Delta B=B(a)-B(0)
   \]
3. Test \(C_\Delta=I_R/\Delta B\).
4. Test local \(p\) using held-out scale rather than per-candidate refitting.

---

# Honest status

> The quick heat-normalization campaign did not close the heat theorem. It identified the correct next correction: use background-subtracted trace slopes and avoid per-grid scale fitting when trying to determine the local dx exponent.

**End of file.**
