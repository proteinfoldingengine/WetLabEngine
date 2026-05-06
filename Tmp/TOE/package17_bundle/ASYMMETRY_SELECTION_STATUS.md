# ASYMMETRY_SELECTION_STATUS.md

# Asymmetry Selection Status
## Status audit for the \(\chi\approx0.2667\) loading-selection problem

## Status
**Closure audit. Selection plausible, not derived.**

This file audits the current state of the \(\chi\)-selection branch after:

```text
CHI_TARGET_PARAMETER_REGIME.md
PRUNING_THRESHOLD_INTEGRALS.md
CHI_NATURALNESS_FROM_PRUNING.md
CHI_SELECTION_PRINCIPLE.md
CHI_SELECTION_FROM_BLOCK_ACTION.md
CHI_SELECTION_FAILURE_ANALYSIS.md
RETAINED_MEMORY_LOADING_ASYMMETRY.md
ASYMMETRY_SELECTION_PRINCIPLE.md
```

The central question is:

\[
\text{Is } \chi\approx0.2667 \text{ derived, naturally selected, or merely reachable?}
\]

Current answer:

```text
selection plausible, not derived
```

---

# 1. Target recap

The bridge coefficient is:

\[
\chi_*=\frac{1}{1+\Lambda_*}.
\]

The target is:

\[
\chi_*\approx0.2667.
\]

Therefore:

\[
\Lambda_*
=
\frac{1-\chi_*}{\chi_*}
\approx2.75.
\]

Equivalently, the loading anchor must satisfy:

\[
q_{\mathrm{block}}=\frac{b}{1-a}\approx2.75\text{–}3.3.
\]

---

# 2. What has been established

## 2.1 Target condition

`CHI_TARGET_PARAMETER_REGIME.md` established:

\[
b\approx2.75(1-a).
\]

In micro-to-block parameters:

\[
w_s\beta_s I_s+w_f\beta_f I_f
\approx
2.75\mathcal G_*
\left[
\mu_G-(w_s\alpha_s c_s+w_f\alpha_f c_f)
\right].
\]

Status:

```text
exact target condition derived
```

---

## 2.2 Pruning threshold dependence

`PRUNING_THRESHOLD_INTEGRALS.md` established, under Gaussian noise:

\[
I_s=\sqrt{\frac{2}{\pi}}\sigma_\xi,
\]

\[
I_f
=
\sqrt{\frac{2}{\pi}}\sigma_\xi
\exp\left[
-\frac{1}{2}
\left(
\frac{\varepsilon^*}{\sigma_\xi}
\right)^2
\right].
\]

Status:

```text
epsilon-star dependence explicit under Gaussian noise
```

---

## 2.3 Naturalness under broad pruning/noise sampling

`CHI_NATURALNESS_FROM_PRUNING.md` found:

```text
hit_rate_percent: 0.8588%
naturalness_class: RARE_BUT_REACHABLE
```

Status:

```text
reachable but not natural under broad pruning/noise priors
```

---

## 2.4 Free selection principle

`CHI_SELECTION_PRINCIPLE.md` introduced:

\[
\mathcal F(\Lambda)
=
\frac{A}{\Lambda}
+
B\Lambda
+
\frac{C}{\chi(1-\chi)}
+
S(\Lambda-q)^2.
\]

Verifier result:

```text
hit_rate_percent: 5.066%
naturalness_class: SELECTION_PLAUSIBLE
```

Status:

```text
selection plausible if balance coefficients are free
```

---

## 2.5 Block-action selection

`CHI_SELECTION_FROM_BLOCK_ACTION.md` tied coefficients to:

\[
K_U,\quad K_x,\quad K_{\mathrm{int}}.
\]

Verifier result:

```text
hit_rate_percent: 3.824%
selection_class: RARE_BLOCK_SELECTION
```

Status:

```text
reachable but rare when coefficients are block-derived
```

---

## 2.6 Failure diagnosis

`CHI_SELECTION_FAILURE_ANALYSIS.md` found:

```text
failure_mode: ANCHOR_CENTERED_NEAR_LAMBDA_1
corr_Lopt_q: 0.985
```

Meaning:

\[
\Lambda_{\mathrm{opt}}
\]

is overwhelmingly controlled by:

\[
q_{\mathrm{block}}.
\]

Broadly:

\[
q_{\mathrm{block}}\approx1
\Rightarrow
\chi\approx0.5.
\]

Target hits require:

\[
q_{\mathrm{block}}\approx3.3.
\]

Status:

```text
main failure mode identified
```

---

## 2.7 Loading asymmetry test

`RETAINED_MEMORY_LOADING_ASYMMETRY.md` found:

### Broad sampling

```text
target hit rate: 1.505%
q median: 0.176
chi median: 0.851
```

### Memory-biased sampling

```text
target hit rate: 2.540%
q median: 14.53
chi median: 0.064
```

Interpretation:

```text
broad sampling underloads memory
strong memory bias overloads memory
target is an intermediate transition band
```

Status:

```text
intermediate-band hypothesis supported
```

---

## 2.8 Asymmetry selection principle

`ASYMMETRY_SELECTION_PRINCIPLE.md` introduced:

\[
\mathcal A(q)
=
\frac{A}{q}
+
Bq
+
C\left[\log\left(\frac{q}{q_0}\right)\right]^2
+
\frac{D}{\chi(q)(1-\chi(q))}.
\]

Verifier result:

```text
target_band_hit_rate_percent: 5.15%
selection_class: STABILIZATION_PLAUSIBLE
```

Target-hit medians:

```text
qopt_median_hits: 3.0003
chiopt_median_hits: 0.24998
A_over_B_median_hits: 9.396
q0_median_hits: 2.960
```

Status:

```text
intermediate-loading stabilization is plausible
```

---

# 3. Current classification

The current status of:

\[
\chi\approx0.2667
\]

is:

```text
not derived
not broadly natural
selection plausible
requires deeper asymmetry derivation
```

More specifically:

\[
\chi\approx0.2667
\]

is selected if the system can justify:

\[
A/B\approx7.5\text{–}9.5
\]

and:

\[
q_0\approx3.
\]

Those are now the real theorem targets.

---

# 4. What would count as closure?

The \(\chi\)-selection seam could be upgraded to:

```text
selection-derived
```

only if we derive:

\[
A/B\approx7.5\text{–}9.5
\]

and:

\[
q_0\approx3
\]

from the retained-memory/block action.

That means deriving:

\[
\text{underload penalty} \gg \text{overload penalty}
\]

and an internal critical loading scale:

\[
q_0\approx3.
\]

Until then, the result remains:

```text
stabilization plausible
```

not:

```text
first-principles derived
```

---

# 5. Safe claims

Safe:

```text
The target \(\chi\approx0.2667\) is reachable but rare under broad pruning/noise sampling.
```

Safe:

```text
A free balance functional can select the target at non-negligible rates.
```

Safe:

```text
A block-action-derived selection functional can reach the target, but only rarely.
```

Safe:

```text
The main failure mode is that the block loading anchor is centered near \(\Lambda\approx1\).
```

Safe:

```text
An intermediate retained-memory stabilization principle makes target selection plausible.
```

---

# 6. Unsafe claims

Do not claim:

```text
\(\chi\approx0.2667\) has been derived.
```

Do not claim:

```text
The current pruning law naturally selects \(\chi\approx0.2667\).
```

Do not claim:

```text
The asymmetry selection principle is first-principles closed.
```

Do not claim:

```text
This closes the GR derivation.
```

---

# 7. Impact on GR derivation program

This branch matters because the memory-action coefficients depend on:

\[
\chi(1-\chi).
\]

Specifically:

\[
Z_R
=
\chi(1-\chi)
\sigma_{\nabla\Lambda}^2
\left(\frac{dx}{dt}\right)^2,
\]

\[
\lambda_{\mathrm{int}}
=
\chi(1-\chi)\rho_{\mathrm{mat}}.
\]

So until \(\chi\) is selected, the coefficient branch is:

```text
micro-to-block constrained but not fully derived
```

The GR program is still alive, but this seam is not closed.

---

# 8. Next theorem target

The next file should be:

```text
ASYMMETRY_FROM_BLOCK_ACTION.md
```

Purpose:

Derive or reject:

\[
A/B\approx7.5\text{–}9.5,
\qquad
q_0\approx3,
\]

from:

\[
K_U,\quad K_x,\quad K_{\mathrm{int}},
\quad
a,\quad b,
\quad
I_s,\quad I_f,
\quad
\varepsilon^*.
\]

If this succeeds, \(\chi\)-selection becomes much stronger.

If this fails, \(\chi\approx0.2667\) should be marked as:

```text
phenomenological fixed point / selected regime
```

until deeper physics is supplied.

---

# 9. Recommended report-out

Use this externally:

```text
Milestone: the \(\chi\)-selection bottleneck is now sharply localized.

The framework can reach \(\chi\approx0.2667\), but broad pruning/noise dynamics do not naturally select it. Strong memory bias overshoots it.

The target appears to live in an intermediate retained-memory stabilization band.

Next theorem: derive the asymmetry that selects that band, or mark \(\chi\) as phenomenological.
```

---

# Honest final status

> `ASYMMETRY_SELECTION_STATUS.md` classifies the \(\chi\approx0.2667\) fixed point as selection-plausible but not derived. The next decisive theorem is whether the retained-memory/block action forces \(A/B\approx7.5\text{–}9.5\) and \(q_0\approx3\).

**End of file.**
