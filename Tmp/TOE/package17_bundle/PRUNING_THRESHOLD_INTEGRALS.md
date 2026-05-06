# PRUNING_THRESHOLD_INTEGRALS.md

# Pruning Threshold Integrals
## Explicit \(\varepsilon^*\)-dependence of slow/fast retained-memory input terms

## Status
**Analytic integral pass. Assumes Gaussian microscopic fluctuation law.**

`CHI_TARGET_PARAMETER_REGIME.md` reduced the target \(\chi_*\approx0.2667\) condition to:

\[
w_s\beta_s I_s+w_f\beta_f I_f
\approx
2.75\mathcal G_*
\left[
\mu_G-(w_s\alpha_s c_s+w_f\alpha_f c_f)
\right].
\]

The missing objects are:

\[
I_s=\mathbb E[|\xi|],
\]

\[
I_f=\mathbb E[|\xi|\Theta(|\xi|-\varepsilon^*)].
\]

This file evaluates those integrals for the assumed microscopic noise law.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Assumption**
- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**
- **Closure status**

Nothing here should be interpreted as proving the Gaussian noise law is forced.

---

# 1. Noise assumption

## Assumption 1
Let the microscopic fluctuation be Gaussian:

\[
\xi\sim\mathcal N(0,\sigma_\xi^2).
\]

Then:

\[
p(\xi)=
\frac{1}{\sqrt{2\pi}\sigma_\xi}
\exp\left(
-\frac{\xi^2}{2\sigma_\xi^2}
\right).
\]

The pruning threshold is:

\[
\varepsilon^*\ge0.
\]

---

# 2. Slow-channel integral

## Definition 1
The slow-channel input is:

\[
I_s
=
\mathbb E[|\xi|].
\]

For Gaussian \(\xi\):

\[
I_s
=
2\int_0^\infty
x
\frac{1}{\sqrt{2\pi}\sigma_\xi}
\exp\left(
-\frac{x^2}{2\sigma_\xi^2}
\right)
dx.
\]

Evaluate:

\[
\int_0^\infty
x
e^{-x^2/(2\sigma_\xi^2)}dx
=
\sigma_\xi^2.
\]

Thus:

\[
I_s
=
\sqrt{\frac{2}{\pi}}\sigma_\xi.
\]

---

# 3. Fast/pruned-channel integral

## Definition 2
The fast-channel input is:

\[
I_f(\varepsilon^*)
=
\mathbb E[|\xi|\Theta(|\xi|-\varepsilon^*)].
\]

By symmetry:

\[
I_f
=
2\int_{\varepsilon^*}^{\infty}
x
\frac{1}{\sqrt{2\pi}\sigma_\xi}
\exp\left(
-\frac{x^2}{2\sigma_\xi^2}
\right)
dx.
\]

Using:

\[
\int_{\varepsilon}^{\infty}
x
e^{-x^2/(2\sigma^2)}dx
=
\sigma^2
e^{-\varepsilon^2/(2\sigma^2)},
\]

we obtain:

\[
I_f(\varepsilon^*)
=
\sqrt{\frac{2}{\pi}}\sigma_\xi
\exp\left(
-\frac{(\varepsilon^*)^2}{2\sigma_\xi^2}
\right).
\]

Therefore:

\[
\frac{I_f}{I_s}
=
\exp\left(
-\frac{(\varepsilon^*)^2}{2\sigma_\xi^2}
\right).
\]

---

# 4. Updated target-\(\chi\) condition

The target condition from `CHI_TARGET_PARAMETER_REGIME.md` was:

\[
w_s\beta_s I_s+w_f\beta_f I_f
\approx
\Lambda_{\mathrm{target}}\mathcal G_*
\left[
\mu_G-(w_s\alpha_s c_s+w_f\alpha_f c_f)
\right],
\]

where:

\[
\Lambda_{\mathrm{target}}
=
\frac{1-\chi_{\mathrm{target}}}{\chi_{\mathrm{target}}}.
\]

Substitute:

\[
I_s=\sqrt{\frac{2}{\pi}}\sigma_\xi,
\]

\[
I_f=
\sqrt{\frac{2}{\pi}}\sigma_\xi
\exp\left(
-\frac{(\varepsilon^*)^2}{2\sigma_\xi^2}
\right).
\]

Then:

\[
\sqrt{\frac{2}{\pi}}\sigma_\xi
\left[
w_s\beta_s
+
w_f\beta_f
\exp\left(
-\frac{(\varepsilon^*)^2}{2\sigma_\xi^2}
\right)
\right]
\approx
\Lambda_{\mathrm{target}}\mathcal G_*
\left[
\mu_G-(w_s\alpha_s c_s+w_f\alpha_f c_f)
\right].
\]

This is the explicit pruning-threshold target condition.

For:

\[
\chi_{\mathrm{target}}=0.2667,
\]

\[
\Lambda_{\mathrm{target}}\approx2.75.
\]

---

# 5. Interpretation

The pruning threshold suppresses the fast channel exponentially:

\[
I_f/I_s
=
e^{-(\varepsilon^*)^2/(2\sigma_\xi^2)}.
\]

Therefore:

- small \(\varepsilon^*/\sigma_\xi\): fast channel active;
- large \(\varepsilon^*/\sigma_\xi\): fast channel suppressed;
- target \(\chi\approx0.2667\) requires sufficient total retained-memory input from slow + fast channels.

If \(\varepsilon^*\) is too high, the fast channel cannot help reach the required:

\[
\Lambda_*\approx2.75.
\]

---

# 6. Solving for threshold ratio

Let:

\[
C
=
\Lambda_{\mathrm{target}}\mathcal G_*
[
\mu_G-(w_s\alpha_s c_s+w_f\alpha_f c_f)
].
\]

The target condition is:

\[
\sqrt{\frac{2}{\pi}}\sigma_\xi
\left[
w_s\beta_s
+
w_f\beta_f
e^{-r^2/2}
\right]
=
C,
\]

where:

\[
r=\frac{\varepsilon^*}{\sigma_\xi}.
\]

Then:

\[
e^{-r^2/2}
=
\frac{
C/(\sqrt{2/\pi}\sigma_\xi)-w_s\beta_s
}{
w_f\beta_f
}.
\]

A real solution exists only if:

\[
0<
\frac{
C/(\sqrt{2/\pi}\sigma_\xi)-w_s\beta_s
}{
w_f\beta_f
}
\le1.
\]

If so:

\[
r
=
\sqrt{
-2\ln
\left[
\frac{
C/(\sqrt{2/\pi}\sigma_\xi)-w_s\beta_s
}{
w_f\beta_f
}
\right]
}.
\]

Thus:

\[
\varepsilon^*
=
\sigma_\xi r.
\]

---

# 7. Verifier implementation

## Status
**Implemented as `pruning_threshold_integrals_verifier.py`. Execution log captured.**

The verifier compares the analytic formulas against Monte Carlo sampling and checks:

1. \(I_s\) analytic vs sampled;
2. \(I_f\) analytic vs sampled;
3. \(I_f\le I_s\);
4. \(I_f\) decreases monotonically with \(\varepsilon^*\);
5. the ratio \(I_f/I_s\) has the expected exponential form.

## Captured verifier output

```text
Pruning threshold integrals verifier
==================================================
Route:
Gaussian noise -> I_s and I_f(eps*) closed forms

PASS: 74.0
SOFT_FAIL: 26.0
HARD_FAIL: 0.0
I_s_analytic_median: 1.2601587425606637
I_f_analytic_median: 0.13499393517283803
ratio_analytic_median: 0.15623545037286146
rel_err_s_median: 0.0015088314750812176
rel_err_f_median: 0.007974246953227595
```

---

# 8. What this file establishes

### Established under Gaussian noise

1. Slow-channel input:
   \[
   I_s=\sqrt{2/\pi}\sigma_\xi.
   \]

2. Fast/pruned-channel input:
   \[
   I_f=\sqrt{2/\pi}\sigma_\xi e^{-(\varepsilon^*)^2/(2\sigma_\xi^2)}.
   \]

3. The target-\(\chi\) condition now has explicit \(\varepsilon^*\)-dependence.

4. Fast-channel contribution is exponentially controlled by:
   \[
   \varepsilon^*/\sigma_\xi.
   \]

### Not yet established

1. Gaussian noise is not yet derived from microscopic dynamics.
2. Non-Gaussian fluctuation laws are not analyzed here.
3. \(\sigma_\xi\) must be measured or derived.
4. This does not prove the target \(\chi\) regime is forced.

---

# 9. Next derivation target

The next file should be:

```text
CHI_NATURALNESS_FROM_PRUNING.md
```

Its job:

Use the explicit \(I_s,I_f(\varepsilon^*)\) formulas to test whether:

\[
\chi_*\approx0.2667
\]

is naturally produced across broad pruning/noise regimes, or whether it requires tuning.

---

# Honest status line

> `PRUNING_THRESHOLD_INTEGRALS.md` makes the pruning threshold dependence explicit under a Gaussian fluctuation law. It shows the fast retained-memory channel is exponentially suppressed by \((\varepsilon^*/\sigma_\xi)^2/2\), but it does not prove Gaussian noise or target-\(\chi\) naturalness.

**End of file.**
