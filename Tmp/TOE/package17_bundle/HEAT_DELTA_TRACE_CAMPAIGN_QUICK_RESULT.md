# HEAT_DELTA_TRACE_CAMPAIGN_QUICK_RESULT.md

# Heat Delta-Trace Campaign — Quick Result
## Background-subtracted heat trace and remaining dx-scaling law

## Status
**Mixed but highly informative. The raw trace problem is fixed; the remaining problem is dx/N scaling. Not theorem closure.**

The corrected Colab campaign ran with:

```text
Device: cpu
QUICK_MODE: True
N = 8, 10, 12
amp = 0.08, 0.15, 0.22
```

Campaign classification:

```text
HEAT_DELTA_TRACE_TARGET_MIXED
```

This is a materially better result than the raw-trace campaign because it confirmed that the heat-trace signal becomes amplitude-stable once the flat/background trace slope is subtracted.

---

# 1. What changed

The previous raw trace test used:

\[
C_{\mathrm{raw}}=\frac{\int R\,dV}{B_{\mathrm{raw}}}.
\]

That failed because \(B_{\mathrm{raw}}\) is dominated by the flat graph spectrum.

The corrected test used:

\[
\Delta B(N,a)=B(N,a)-B(N,0)
\]

and:

\[
C_\Delta(N,a)=\frac{\int R(a)\,dV}{\Delta B(N,a)}.
\]

This is the correct theorem object.

---

# 2. Main result

Trace delta summary:

```text
C_delta_required_mean: -6.26396058645194
C_delta_required_std:  2.2481427068445163
C_delta_required_cv:   0.358901157792495
C_delta_required_min: -9.144263182019806
C_delta_required_max: -3.935687194202831
```

Still mixed overall, but the structure is now clear.

---

# 3. Within-grid amplitude stability is strong

For each \(N\), \(C_\Delta\) is stable across amplitudes.

## N=8

```text
amp=0.08: C_delta = -9.1443
amp=0.15: C_delta = -9.0922
amp=0.22: C_delta = -9.0090
```

Approximate range:

```text
-9.14 to -9.01
```

## N=10

```text
amp=0.08: C_delta = -5.7826
amp=0.15: C_delta = -5.7460
amp=0.22: C_delta = -5.6876
```

Approximate range:

```text
-5.78 to -5.69
```

## N=12

```text
amp=0.08: C_delta = -4.0019
amp=0.15: C_delta = -3.9764
amp=0.22: C_delta = -3.9357
```

Approximate range:

```text
-4.00 to -3.94
```

This is important: the coefficient is **not wandering with amplitude**. It is primarily changing with grid scale.

---

# 4. Discovered dx-scaling law

The coefficient magnitude decreases as \(N\) increases:

```text
N=8:  C_delta ≈ -9.08
N=10: C_delta ≈ -5.74
N=12: C_delta ≈ -3.97
```

Since:

\[
dx = \frac{2\pi}{N},
\]

this suggests:

\[
C_\Delta(N)\propto -dx^q
\]

or equivalently:

\[
C_\Delta(N)\propto -N^{-q}.
\]

A quick log-ratio estimate gives roughly:

\[
q\approx 2.8 \text{ to } 3.0.
\]

That points to a likely volume-element scaling:

\[
C_\Delta \sim -c\,dx^3.
\]

Check:

\[
\frac{C_\Delta}{dx^3}
\]

is approximately stable:

```text
N=8:  -9.08 / 0.7854^3 ≈ -18.75
N=10: -5.74 / 0.6283^3 ≈ -23.14
N=12: -3.97 / 0.5236^3 ≈ -27.69
```

Not constant yet, but far more coherent than the raw coefficient. The remaining variation may come from finite-grid heat-window effects or missing prefactors from the graph volume normalization.

---

# 5. Local heat branch

The local result remained the same:

```text
best sign: -6
corr_mean: 0.96106
corr_min: 0.92687
```

Again, \(p\) is not truly identified because every candidate gets an independent scale.

The valid conclusion is:

```text
negative local heat slope tracks curvature shape
dx exponent still requires cross-grid or theorem constraint
```

---

# 6. Correct next theorem target

The global trace theorem should now be stated as:

\[
\int R\,dV
=
C_\Delta(dx)\left[B(a)-B(0)\right]+o(1)
\]

with:

\[
C_\Delta(dx)\sim -c\,dx^q.
\]

The next campaign should fit:

\[
q
\]

directly using:

```text
N = 8, 10, 12, 14, 16
```

and then test whether:

\[
\frac{C_\Delta}{dx^q}
\]

stabilizes.

---

# 7. Immediate next file

```text
COLAB_TRACE_DX_SCALING_CAMPAIGN.py
```

Purpose:

1. Compute flat-subtracted trace slope:
   \[
   \Delta B=B(a)-B(0)
   \]

2. Compute:
   \[
   C_\Delta=\frac{I_R}{\Delta B}
   \]

3. Fit:
   \[
   |C_\Delta| = c\,dx^q
   \]

4. Report:
   ```text
   q_fit
   c_fit
   residuals
   C_delta / dx^q stability
   held-out prediction error for I_R
   ```

---

# 8. Current status

```text
raw trace slope: wrong object
delta trace slope: correct object
amplitude stability: strong within each N
dx/N scaling: unresolved but structured
local heat sign/shape: strong
local p exponent: unresolved
```

---

# Honest status

> The delta-trace campaign did not close heat normalization, but it transformed the failure into a clean dx-scaling problem. The next step is to fit and test the exponent \(q\) in \(C_\Delta(dx)\sim -c\,dx^q\).

**End of file.**
