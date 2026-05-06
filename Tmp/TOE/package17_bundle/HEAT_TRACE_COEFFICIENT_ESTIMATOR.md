# HEAT_TRACE_COEFFICIENT_ESTIMATOR.md

# Heat Trace Coefficient Estimator
## First fixed-window attempt to extract the curvature coefficient from graph heat trace

## Status
**Coefficient-extraction diagnostic. Not curvature closure.**

`HEAT_KERNEL_CURVATURE_ACTION.md` established the correct first-principles target:

\[
\mathrm{Tr}(e^{-t\Delta})
\sim
(4\pi t)^{-d/2}
\left[
V+\frac{t}{6}\int R\,dV+O(t^2)
\right].
\]

The previous spectral diagnostic used generic heat-trace area/slope and was weak.

This file targets the actual coefficient:

\[
\frac{1}{6}\int R\,dV.
\]

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving GR.

---

# 1. Continuum target

Define:

\[
Y(t)=H(t)(4\pi t)^{d/2},
\]

where:

\[
H(t)=\mathrm{Tr}(e^{-t\Delta}).
\]

Then:

\[
Y(t)
\sim
V+\frac{t}{6}\int R\,dV+O(t^2).
\]

So fitting:

\[
Y(t)\approx A_0+A_1t
\]

in a valid small-\(t\) window gives:

\[
\widehat{\int R\,dV}=6A_1.
\]

---

# 2. Graph estimator

Use a weighted graph Laplacian:

\[
L_{\mathcal G}=\frac{D-W}{h^2},
\]

where \(h\) is the median neighbor spacing.

The graph heat trace is:

\[
H_{\mathcal G}(t)=\mathrm{Tr}(e^{-tL_{\mathcal G}}).
\]

The estimator uses a fixed heat-time window tied to graph spacing:

\[
t=c h^2,
\]

with fixed \(c\)-values.

No per-geometry calibration is allowed.

---

# 3. Verifier implementation

## Status
**Implemented as `heat_trace_coefficient_estimator_verifier.py`. Execution log captured.**

The verifier tests the estimator on:

```text
plane
sphere
saddle
perturbed sphere
```

It reports the estimated heat coefficient:

\[
6A_1.
\]

## Captured verifier output

```text
Heat trace coefficient estimator verifier
==================================================
Route:
scaled unnormalized graph Laplacian -> fixed h^2 heat window -> coefficient of t
No per-geometry calibration. Diagnostic only.

kind,intR_coeff_median,intR_coeff_std,A0_median,h_median
plane,28.262619527284944,24.654759746054616,3.8643381836962636,0.21656729111416584
sphere,-32.949554905351704,7.3467437467326935,10.576674833059272,0.3649239975171181
saddle,7.132411053602986,9.370161280352955,5.125091235113048,0.2431453612152054
perturbed_sphere,-26.988372415509854,8.114307205327256,10.852814353976832,0.37258820477121013
separation_sphere_plane_coeff: 0.9999999999999837
separation_saddle_plane_coeff: 0.5969823482817084
classification: COEFFICIENT_DIAGNOSTIC_PROMISING
```

---

# 4. Interpretation rule

This is only a diagnostic.

A useful estimator should show:

1. flat geometry near a baseline;
2. sphere separated from plane;
3. saddle separated from plane;
4. stable variance;
5. no per-geometry calibration.

If it fails, the issue is likely one of:

```text
wrong graph Laplacian scaling
bad heat-time window
boundary contamination
sampling density effects
dimension mismatch
```

---

# 5. What this file establishes

### Established

1. The heat-coefficient extraction target is explicit.
2. The verifier now estimates the actual \(t\)-coefficient rather than generic heat-trace features.
3. The no-fitting rule is preserved.

### Not yet established

1. Valid heat-time scaling window.
2. Boundary correction.
3. Dimension-consistent 3D spatial tests.
4. Convergence to \(\int R\,dV\).
5. ADM action convergence.

---

# 6. Next derivation target

If the result is weak, the next file should be:

```text
HEAT_KERNEL_FAILURE_ANALYSIS.md
```

If promising, the next file should be:

```text
CURVATURE_REFERENCE_GEOMETRY_TESTS.md
```

---

# Honest status line

> `HEAT_TRACE_COEFFICIENT_ESTIMATOR.md` targets the actual heat-trace curvature coefficient using a fixed graph rule and fixed heat window. It is an essential first-principles diagnostic, but not yet proof of graph-to-continuum curvature convergence.

**End of file.**
