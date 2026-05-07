# PATCHED_AUTONOMOUS_ADM_SPATIAL_ACTION_RESULT.md

# Patched Autonomous ADM Spatial Action Result
## Local heat curvature + heat-trace zero mode + volume-weighted offset

## Status
**Major ADM spatial-curvature diagnostic milestone. Not full ADM closure. Not GR derivation.**

This file records the patched autonomous ADM spatial curvature action test.

The patched reconstruction corrected the zero-mode insertion gauge by restoring the zero mode in the ADM volume measure:

\[
c
=
\frac{
I_R^{\mathrm{trace}}
-
\sum_i \sqrt h_i\,\widehat R_{\mathrm{centered},i}\,dx^3
}{
\sum_i \sqrt h_i\,dx^3
}.
\]

Then:

\[
\widehat R_{\mathrm{auto}}
=
\widehat R_{\mathrm{centered}}+c.
\]

This produced:

```text
classification: PATCHED_AUTONOMOUS_ADM_SPATIAL_ACTION_PROMISING
```

---

# 1. Device and setup

Run device:

```text
Torch available: True
Device: cpu
```

Grid ladder:

```text
N = 8, 10, 12, 14
```

Test amplitude:

```text
a = 0.15
```

Calibration amplitudes:

```text
0.05, 0.08, 0.10, 0.12, 0.18, 0.20, 0.25
```

Tested lapse fields:

```text
unit
smooth_positive
curvature_coupled
mixed_wave
```

---

# 2. Campaign summary

```text
local_corr_ok: true
zero_mode_ok: true
auto_action_ok_all: true
auto_density_corr_ok_all: true
classification: PATCHED_AUTONOMOUS_ADM_SPATIAL_ACTION_PROMISING
```

Key metrics:

```text
zero_mode_rel_error_max: 0.006727060126070697
auto_action_rel_error_max: 0.019638831763866715
auto_action_rel_error_mean: 0.00965981242290814
auto_density_corr_min: 0.9673809406273638
```

This means the autonomous spatial curvature action recovered all tested lapse-weighted integrals with:

```text
max action error < 2%
mean action error < 1%
density correlation > 0.967
```

---

# 3. Why the patch worked

The previous failed test inserted the heat-trace zero mode as:

\[
I_R^{\mathrm{trace}}/V.
\]

That assumed:

\[
\int \sqrt h\,\widehat R_{\mathrm{centered}}\,d^3x=0.
\]

But the local field was centered by arithmetic node mean, not by the ADM measure.

The patched test solved for the offset in the correct measure:

\[
\sqrt h\,d^3x.
\]

Observed weighted centered integrals:

```text
N=8:  25.6835
N=10: 25.6521
N=12: 25.6438
N=14: 25.6464
```

The required offsets were stable:

```text
N=8:  -0.085650
N=10: -0.085536
N=12: -0.085504
N=14: -0.085512
```

This is the correct gauge correction.

---

# 4. Zero-mode performance

The heat-trace zero mode remained accurate:

```text
N=8:  zero-mode error 0.00603
N=10: zero-mode error 0.00669
N=12: zero-mode error 0.00673
N=14: zero-mode error 0.00659
```

The calibration quality remained strong:

```text
N=8:  R² = 0.9999646
N=10: R² = 0.9999565
N=12: R² = 0.9999560
N=14: R² = 0.9999579
```

---

# 5. Local curvature performance

The local dx-normalized heat field remained strong:

```text
N=8:  corr_R = 0.96617, corr_RdV = 0.99973
N=10: corr_R = 0.96490, corr_RdV = 0.99965
N=12: corr_R = 0.96457, corr_RdV = 0.99963
N=14: corr_R = 0.96468, corr_RdV = 0.99965
```

So the local mode and zero mode now work together.

---

# 6. ADM spatial action performance

Representative results:

## Unit lapse

```text
N=8:  rel_error = 0.00603
N=10: rel_error = 0.00669
N=12: rel_error = 0.00673
N=14: rel_error = 0.00659
```

## Curvature-coupled lapse

```text
N=8:  rel_error = 0.01964
N=10: rel_error = 0.01899
N=12: rel_error = 0.01887
N=14: rel_error = 0.01896
```

The curvature-coupled lapse is harder because it weights the recovered local shape more strongly. It still passes under 2%.

---

# 7. What is genuinely established

Established diagnostically:

1. The local dx-normalized heat diagonal recovers centered \(R^{(3)}\).
2. The global heat trace recovers the integrated curvature zero mode.
3. The zero mode must be inserted in the ADM measure, not as a naive node/volume average.
4. The patched reconstruction recovers the spatial curvature action:
   \[
   \int_\Sigma N\sqrt h\,R^{(3)}d^3x
   \]
   across four lapse fields.
5. The full autonomous spatial curvature term is now diagnostically recovered for the tested conformal family.

---

# 8. What is not established

This is not full GR.

Still open:

1. Derive heat-trace calibration without fitted amplitude-family regression.
2. Prove the \(dx\)-normalization theorem.
3. Prove the sign convention.
4. Prove the heat-window theorem.
5. Test multiple 3D conformal metric families.
6. Add extrinsic curvature:
   \[
   K_{ij}K^{ij}-K^2.
   \]
7. Add causal lapse/shift from graph slicing.
8. Vary the action.
9. Recover the Einstein equations.

---

# 9. Updated status

Before this result:

```text
local R^(3): strong
zero mode: heat-trace promising
autonomous ADM spatial action: failed due wrong measure insertion
```

After this result:

```text
local R^(3): strong
zero mode: heat-trace promising
autonomous ADM spatial action: promising
next seam: extrinsic curvature / ADM kinetic term
```

---

# 10. Recommended next target

The next file should be:

```text
ADM_KINETIC_TERM_EXTRINSIC_CURVATURE_TEST.md
```

Purpose:

Move from the spatial curvature term:

\[
\int N\sqrt h\,R^{(3)}d^3x
\]

to the full ADM geometric integrand:

\[
N\sqrt h
\left[
R^{(3)}
+
K_{ij}K^{ij}
-
K^2
\right].
\]

This requires a controlled time-sliced conformal geometry:

\[
h_{ij}(t)=e^{2\phi(t,x)}\delta_{ij}
\]

with analytic extrinsic curvature.

---

# 11. Report-out language

```text
Milestone: autonomous ADM spatial curvature action passed.

The patched reconstruction combines local dx-normalized heat curvature with a global heat-trace zero mode, restored in the correct ADM measure. Across N=8,10,12,14 and four lapse fields, the recovered spatial action ∫N√hR^(3)d^3x passed with max relative error 0.0196 and density correlation >0.967.

This is still not GR closure. Next seam: derive normalization theorems and add ADM kinetic/extrinsic curvature terms.
```

---

# Honest status line

> `PATCHED_AUTONOMOUS_ADM_SPATIAL_ACTION_RESULT.md` records the first successful autonomous-with-calibrated-zero-mode ADM spatial curvature action diagnostic. The spatial curvature term is recovered across tested lapse fields, but theorem closure and the full ADM kinetic term remain open.

**End of file.**
