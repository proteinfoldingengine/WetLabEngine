# TRACE_DX_SCALING_FULL_HELDOUT_RESULT.md

# Trace dx-Scaling Full Held-Out Campaign Result
## Global heat-trace zero-mode normalization survives full grid/amplitude and held-out testing

## Status
**Strong empirical pass. The global heat-trace zero-mode seam is now reduced to a clean dx² normalization theorem target. Not a proof yet.**

Campaign classification:

```text
TRACE_DX_SCALING_FULL_HELDOUT_PROMISING
```

---

# 1. Runtime

```text
Torch available: True
Device: cuda
GPU: Tesla T4
N = 8, 10, 12, 14, 16, 18
amp = 0.05, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25
n_rows = 54
```

The run included:
- flat reference \(a=0\) for every \(N\);
- 54 non-flat geometries;
- all-data fit;
- held-out grid test;
- held-out amplitude test.

---

# 2. Main result

The corrected heat-trace object is:

\[
\Delta B(N,a)=B_{\mathrm{trace}}(N,a)-B_{\mathrm{trace}}(N,0).
\]

The coefficient is:

\[
C_\Delta(N,a)=\frac{\int R(a)\,dV}{\Delta B(N,a)}.
\]

The full campaign fit:

\[
C_\Delta(dx)\approx -c\,dx^q.
\]

All-data fit:

```text
c = 14.502529893688841
q = 1.9849207102448094
```

Therefore the empirical law is:

\[
\boxed{
C_\Delta(dx)\approx -14.50\,dx^{1.985}
}
\]

and, to leading order,

\[
\boxed{
\int R\,dV
\approx
-C_0\,dx^2
\left[
B(a)-B(0)
\right]
}
\]

with:

\[
C_0\approx 14.5.
\]

---

# 3. Full-fit performance

All-fit metrics:

```text
all_fit_I_rel_error_mean: 0.009164835194534949
all_fit_I_rel_error_max:  0.025850011880313026
all_fit_C_scaled_cv:      0.011353037411602757
```

Interpretation:

```text
mean prediction error: ~0.92%
max prediction error:  ~2.59%
scaled coefficient CV: ~1.14%
```

This is strong for a heat-trace zero-mode diagnostic over 54 geometries.

---

# 4. Held-out grid test

Train on:

```text
N <= 14
```

Held out:

```text
N = 16, 18
```

Train-grid fit:

```text
train_N_fit_c = 14.72695190092229
train_N_fit_q = 2.0189617815213863
```

Held-out grid performance:

```text
heldout_N_n: 18
heldout_N_I_rel_error_mean: 0.024083768891099127
heldout_N_I_rel_error_max:  0.03890021785670383
heldout_N_C_scaled_cv:      0.009933346650250639
```

Interpretation:

```text
mean held-out grid error: ~2.41%
max held-out grid error:  ~3.89%
scaled coefficient CV:    ~0.99%
```

This is a real extrapolation test. The dx law survives.

---

# 5. Held-out amplitude test

Train on middle amplitudes:

```text
0.08, 0.10, 0.12, 0.15, 0.18, 0.20, 0.22
```

Held out:

```text
0.05, 0.25
```

Amplitude fit:

```text
train_amp_fit_c = 14.511835571173217
train_amp_fit_q = 1.9849207758165188
```

Held-out amplitude performance:

```text
heldout_amp_n: 12
heldout_amp_I_rel_error_mean: 0.0118354564116453
heldout_amp_I_rel_error_max:  0.02650821412647256
heldout_amp_C_scaled_cv:      0.014899872093369433
```

Interpretation:

```text
mean held-out amplitude error: ~1.18%
max held-out amplitude error:  ~2.65%
scaled coefficient CV:         ~1.49%
```

The amplitude extrapolation is also strong.

---

# 6. Why this matters

Before these tests, the global heat trace looked unstable because the raw heat-trace slope was dominated by the flat graph spectrum:

\[
B_{\mathrm{raw}}.
\]

The corrected object:

\[
\Delta B = B(a)-B(0)
\]

removes the background graph spectral term.

Once the flat trace is subtracted, the remaining curvature signal follows a nearly pure dx² law.

This means the global heat-trace zero-mode is not arbitrary calibration. It has a reproducible normalization structure:

\[
\int R\,dV
\sim
-dx^2\Delta B.
\]

---

# 7. The theorem target is now precise

The candidate theorem should be stated as:

## Global Heat-Trace Zero-Mode Theorem Candidate

For the weighted conformal graph Laplacian:

\[
L=(D-W)/dx^2,
\]

with heat trace:

\[
H_a(t)=\mathrm{Tr}(e^{-tL_a})(4\pi t)^{3/2},
\]

and linear slope \(B(a)\) over the admissible window \(t\sim dx^2\), define the flat-subtracted trace slope:

\[
\Delta B(a)=B(a)-B(0).
\]

Then, for the tested conformal torus family,

\[
\int_\Sigma R(a)\,dV
=
-C_0\,dx^2\Delta B(a)
+
O(dx^\alpha)
+
O(a^3)
\]

with empirical:

```text
C0 ≈ 14.5
q ≈ 2
```

The remaining proof obligations are:

1. Derive the \(dx^2\) exponent.
2. Derive or identify the continuum limit of \(C_0\).
3. Derive the finite-window correction terms.
4. Extend beyond the single conformal torus family.
5. Connect the trace zero mode to the local heat diagonal estimator.

---

# 8. Updated seam status

## Closed diagnostically / strongly constrained

```text
raw trace problem identified
flat-background subtraction validated
dx² scaling law validated across grids and amplitudes
held-out prediction passed
```

## Still open mathematically

```text
proof of dx² law
proof of constant C0
proof of heat-window admissibility
extension to non-conformal perturbations
connection to full Einstein-Hilbert theorem
```

---

# 9. Relation to ADM operator-kinetic result

The best ADM full operator-kinetic action result had:

```text
ADM_action_rel_error_max ≈ 0.01905
K_action_rel_error_max ≈ 4e-10
```

The kinetic branch is already operator-derived and essentially exact in the controlled conformal setting.

This new result attacks the remaining spatial/global heat seam.

Therefore the current ADM bridge status is:

```text
kinetic term: operator-derived
global spatial zero mode: dx² heat-trace law validated
local spatial curvature: sign/shape strong, normalization theorem still open
full ADM action: strongest pass so far
GR derivation: still open
```

---

# 10. Next file

The next derivation file should be:

```text
GLOBAL_HEAT_TRACE_ZERO_MODE_THEOREM.md
```

Its purpose:

Turn the empirical law

\[
\int R\,dV
\approx
-14.5\,dx^2\left[B(a)-B(0)\right]
\]

into a derivation.

The next numerical file should be:

```text
COLAB_MULTI_GEOMETRY_TRACE_DX_SCALING.py
```

Purpose:

Test whether the same \(dx^2\) law survives:
- different conformal modes;
- mixed Fourier modes;
- anisotropic conformal perturbations;
- possibly weak non-conformal metric perturbations.

---

# 11. Report-out language

```text
Milestone: global heat-trace zero mode passed held-out validation.

After subtracting the flat graph spectrum, the heat-trace curvature signal obeys a clean dx² normalization law. Across N=8,10,12,14,16,18 and nine amplitudes, C_delta = ∫R dV / [B(a)-B(0)] fits C_delta ≈ -14.50 dx^1.985. The all-fit mean error is ~0.92%, max error ~2.59%. Held-out grids N=16,18 predict with mean error ~2.41%, max ~3.89%. Held-out amplitudes predict with mean error ~1.18%, max ~2.65%.

This does not prove the theorem yet, but it turns the global heat-trace zero-mode calibration into a concrete dx² normalization law.
```

---

# Honest status

> `TRACE_DX_SCALING_FULL_HELDOUT_RESULT.md` records a strong held-out empirical pass for global heat-trace normalization. The heat zero-mode seam is not closed mathematically, but it is now sharply constrained: flat-subtracted heat-trace slope scales as \(dx^{-2}\int R\,dV\), or equivalently \(C_\Delta(dx)\sim -14.5dx^2\).

**End of file.**
