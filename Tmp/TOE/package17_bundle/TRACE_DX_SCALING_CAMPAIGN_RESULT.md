# TRACE_DX_SCALING_CAMPAIGN_RESULT.md

# Trace dx-Scaling Campaign Result
## Background-subtracted global heat-trace coefficient law

## Status
**Promising pass. The global heat-trace zero-mode coefficient now has a clean dx-scaling law. Not theorem closure yet.**

The campaign tested the corrected trace object:

\[
\Delta B(N,a)=B_{\mathrm{trace}}(N,a)-B_{\mathrm{trace}}(N,0),
\]

with:

\[
C_\Delta(N,a)=\frac{\int R(a)\,dV}{\Delta B(N,a)}.
\]

Then it fit:

\[
|C_\Delta(dx)|=c\,dx^q.
\]

Campaign classification:

```text
TRACE_DX_SCALING_PROMISING
```

---

# 1. Runtime

```text
Torch available: True
Device: cpu
QUICK_MODE: True
N = 8, 10, 12, 14
amp = 0.08, 0.15, 0.22
```

Although GPU was available, the run executed on CPU.

---

# 2. Fitted scaling law

The fitted law was:

\[
C_\Delta(dx)\approx -c\,dx^q
\]

with:

```text
c = 14.731126261127983
q = 2.018919072510212
```

So, to leading order:

\[
C_\Delta(dx)\approx -14.73\,dx^{2.019}.
\]

Given the fitted exponent is very close to 2, the theorem target should be:

\[
C_\Delta(dx)\sim -C_0\,dx^2.
\]

Equivalently:

\[
\int R\,dV
\approx
-C_0\,dx^2\,[B(a)-B(0)].
\]

---

# 3. Stability metrics

The normalized coefficient:

\[
\frac{C_\Delta}{dx^q}
\]

was highly stable:

```text
C_scaled_mean: -14.731606240503963
C_scaled_std:  0.12413668521200961
C_scaled_cv:   0.008426554659782606
```

The prediction error was low:

```text
I_prediction_rel_error_mean: 0.006886266934539485
I_prediction_rel_error_max:  0.013669402058552868
```

This is a strong result.

---

# 4. Why this matters

Earlier raw trace tests failed because the trace slope was dominated by the flat/background graph spectrum.

This campaign used:

\[
B(a)-B(0)
\]

and revealed a clean grid-scaling law.

So the global heat-trace theorem target is no longer vague calibration. It is now:

\[
\boxed{
\int R\,dV
=
-C_0\,dx^2
\left[
B(a)-B(0)
\right]
+
o(1)
}
\]

with empirical:

\[
C_0\approx 14.73.
\]

---

# 5. Per-grid coefficient behavior

The raw \(C_\Delta\) values were:

## N=8

```text
-9.1443
-9.0922
-9.0090
```

## N=10

```text
-5.7826
-5.7460
-5.6876
```

## N=12

```text
-4.0019
-3.9764
-3.9357
```

## N=14

```text
-2.9598
-2.9413
-2.9118
```

The coefficient changes with \(N\), but after dividing by \(dx^{2.0189}\), it becomes nearly constant.

---

# 6. Resulting theorem target

The global trace theorem should now be written as:

## Candidate theorem

For the weighted conformal graph Laplacian:

\[
L=(D-W)/dx^2,
\]

with heat trace:

\[
H(t)=\mathrm{Tr}(e^{-tL})(4\pi t)^{3/2},
\]

and linear slope \(B(a)\) over the admissible heat window \(t\sim dx^2\), the background-subtracted slope satisfies:

\[
\int_\Sigma R(a)\,dV
=
-C_0\,dx^2
\left[
B(a)-B(0)
\right]
+
O(dx^\alpha)
+
O(a^3).
\]

Empirical fit:

```text
C0 ≈ 14.7311
q ≈ 2.0189
```

The next proof problem is deriving:

```text
why exponent is 2
why coefficient is approximately 14.73
what continuum constant it converges toward
```

---

# 7. Important caveat

This is a quick-mode campaign:

```text
N = 8, 10, 12, 14
amp = 0.08, 0.15, 0.22
```

Before calling it theorem-grade, run:

```text
N = 8, 10, 12, 14, 16, 18
amp = 0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25
```

and then test held-out prediction.

---

# 8. Current status update

Before this campaign:

```text
raw global trace coefficient: unstable
delta trace coefficient: amplitude-stable but N-dependent
```

After this campaign:

```text
delta trace coefficient: follows clean dx^q law
q ≈ 2.019
C_scaled CV ≈ 0.0084
max prediction error ≈ 1.37%
```

This is a major improvement.

---

# 9. Next target

The next file should be:

```text
GLOBAL_HEAT_TRACE_ZERO_MODE_THEOREM.md
```

Purpose:

Turn the empirical law:

\[
\int R\,dV
\approx
-14.73\,dx^2\Delta B
\]

into a derivation.

A second useful file is:

```text
COLAB_TRACE_DX_SCALING_FULL_CAMPAIGN.py
```

Purpose:

Run the full grid and amplitude set, then perform held-out prediction.

---

# 10. Report-out language

```text
Milestone: background-subtracted heat trace passed.

The raw global heat trace was dominated by the flat graph spectrum, but after subtracting the flat reference slope B(0), the coefficient C_delta = ∫R dV / [B(a)-B(0)] follows a clean dx-scaling law. Across N=8,10,12,14 and amplitudes 0.08,0.15,0.22, the fit gives C_delta ≈ -14.73 dx^2.019 with scaled CV ≈0.0084 and max prediction error ≈1.37%.

This does not prove the theorem yet, but it turns the zero-mode calibration into a concrete dx² normalization law.
```

---

# Honest status

> `TRACE_DX_SCALING_CAMPAIGN_RESULT.md` records a strong empirical pass for the global heat-trace zero-mode normalization. The next step is deriving the \(dx^2\) law and coefficient, then rerunning the full held-out campaign.

**End of file.**
