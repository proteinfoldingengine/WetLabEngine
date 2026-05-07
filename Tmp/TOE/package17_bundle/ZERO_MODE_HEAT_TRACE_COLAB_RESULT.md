# ZERO_MODE_HEAT_TRACE_COLAB_RESULT.md

# Zero-Mode Heat Trace Colab Result
## Recovering integrated scalar curvature from the global heat trace

## Status
**Major zero-mode diagnostic milestone. Not theorem closure.**

This file records the Colab/T4 run of `zero_mode_heat_trace_colab_test.py`.

The result is strong:

```text
classification: ZERO_MODE_HEAT_TRACE_COLAB_PROMISING
```

The missing ADM spatial curvature zero mode:

\[
\int_\Sigma \sqrt h\,R^{(3)}d^3x
\]

is strongly encoded in global heat-trace observables.

---

# 1. Device and setup

The run used:

```text
Torch available: True
Device: cuda
GPU: Tesla T4
```

Grid ladder:

```text
N = 8, 10, 12, 14
```

Amplitudes:

```text
a = 0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25
```

Total geometries completed:

```text
32
```

Heat trace object:

\[
H(t)=\mathrm{Tr}(e^{-tL})(4\pi t)^{3/2}.
\]

Expected continuum expansion:

\[
H(t)\approx V+\frac{t}{6}\int R\,dV.
\]

The tested predictor is the fitted linear slope:

\[
6B_{\mathrm{trace}}.
\]

---

# 2. Campaign summary

```text
classification: ZERO_MODE_HEAT_TRACE_COLAB_PROMISING
all_N_promising: true
N_completed: 8, 10, 12, 14
n_geometries_completed: 32
```

Strongest global summary:

```text
min_heat_trace_linear_slope_R2_int_RdV: 0.9999491238093349
max_heat_trace_linear_slope_relative_error_int_RdV: 0.004442398491249186
```

That means the heat-trace slope predicts integrated scalar curvature across all tested \(N\) with about:

```text
< 0.45% relative error
```

after fitted calibration.

---

# 3. Per-grid results

## N=8

```text
heat_trace_linear_slope_R2_int_RdV: 0.9999590525
relative_error: 0.0039854181
classification: ZERO_MODE_HEAT_TRACE_PROMISING
```

Best integrated-curvature predictor:

```text
trace_quad_slope_6b
R2: 0.9999988292
relative_error: 0.0006739228
```

## N=10

```text
heat_trace_linear_slope_R2_int_RdV: 0.9999496722
relative_error: 0.0044183932
classification: ZERO_MODE_HEAT_TRACE_PROMISING
```

Best integrated-curvature predictor:

```text
trace_quad_slope_6b
R2: 0.9999998737
relative_error: 0.0002213714
```

## N=12

```text
heat_trace_linear_slope_R2_int_RdV: 0.9999491238
relative_error: 0.0044423985
classification: ZERO_MODE_HEAT_TRACE_PROMISING
```

Best integrated-curvature predictor:

```text
trace_quad_slope_6b
R2: 0.9999972196
relative_error: 0.0010385236
```

## N=14

```text
heat_trace_linear_slope_R2_int_RdV: 0.9999512659
relative_error: 0.0043478709
classification: ZERO_MODE_HEAT_TRACE_PROMISING
```

Best integrated-curvature predictor:

```text
mean_degree_deficit
R2: 0.9999933018
relative_error: 0.0016119091
```

The heat-trace slope itself still passed strongly at \(N=14\).

---

# 4. Interpretation

This is the cleanest zero-mode result so far.

Earlier, the direct-heat ADM spatial action test showed:

```text
local curvature shape/density: right
action integral without mean restoration: wrong
zero mode: missing
```

Now this test shows:

```text
the zero mode is recoverable from the global heat trace
```

Specifically:

\[
\mathrm{Tr}(e^{-tL})(4\pi t)^{3/2}
\]

contains a slope feature that tracks:

\[
\int \sqrt h\,R^{(3)}d^3x.
\]

This aligns directly with the continuum heat-kernel expansion.

---

# 5. Updated ADM spatial action path

We now have two pieces:

## Local mode

The dx-normalized direct heat diagonal recovers the centered local curvature field:

\[
R^{(3)}-\langle R^{(3)}\rangle.
\]

## Zero mode

The global heat trace recovers the integrated curvature:

\[
\int \sqrt h\,R^{(3)}d^3x.
\]

Together, these suggest an autonomous spatial curvature reconstruction:

\[
R^{(3)}_{\mathrm{recon}}
=
R^{(3)}_{\mathrm{local,centered}}
+
R^{(3)}_{\mathrm{zero-mode}}.
\]

This is the next target.

---

# 6. What is genuinely established

Established diagnostically:

1. Global heat-trace slope tracks integrated scalar curvature across amplitudes.
2. The result passes for \(N=8,10,12,14\).
3. The result is robust over 32 geometries.
4. The heat-trace slope is a heat-kernel-native zero-mode observable.
5. Best predictors often use the quadratic trace slope, suggesting \(O(t^2)\) terms matter but do not destroy the signal.

---

# 7. What remains open

Still not established:

1. No fitted calibration.
2. No theorem for graph heat-trace convergence.
3. No proof of heat-window validity.
4. No multi-family 3D conformal test.
5. No combined autonomous ADM spatial action test yet.
6. No extrinsic curvature terms.
7. No action variation.
8. No Einstein equations.

So this is:

```text
zero-mode diagnostic milestone
```

not:

```text
ADM/GR closure
```

---

# 8. Next target

The next file should be:

```text
AUTONOMOUS_ADM_SPATIAL_ACTION_TEST.md
```

Purpose:

Combine:

```text
local dx-normalized direct heat curvature field
+
global heat-trace zero mode
```

to reconstruct the full \(R^{(3)}\) field without analytic mean insertion.

Then retest:

\[
\int_\Sigma N\sqrt h\,R^{(3)}d^3x.
\]

This is the first real autonomous ADM spatial curvature action test.

---

# 9. Report-out language

```text
Milestone: heat-trace zero mode passed.

Across 32 Colab/T4 geometries, the global heat trace Tr(exp(-tL))(4πt)^(3/2) recovered the ADM spatial curvature zero mode ∫√h R^(3)d^3x with R² > 0.99994 and relative error < 0.0045 across N=8,10,12,14.

This closes the diagnostic gap exposed by the direct ADM spatial-action test: local curvature came from the heat diagonal, and the missing mean mode now comes from the heat trace.

Still not theorem closure. Next step: autonomous ADM spatial-action reconstruction.
```

---

# Honest status line

> `ZERO_MODE_HEAT_TRACE_COLAB_RESULT.md` records a major zero-mode diagnostic milestone: the global heat trace strongly predicts integrated scalar curvature across amplitudes and grid sizes. The next step is to combine this zero mode with the local heat curvature field to test autonomous ADM spatial-action recovery.

**End of file.**
