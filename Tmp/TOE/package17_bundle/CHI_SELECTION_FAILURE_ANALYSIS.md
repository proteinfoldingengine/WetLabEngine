# CHI_SELECTION_FAILURE_ANALYSIS.md

# Chi Selection Failure Analysis
## Why block-action selection usually prefers \(\chi\approx0.49\) instead of \(\chi\approx0.2667\)

## Status
**Failure analysis. Not a new selection proof.**

`CHI_SELECTION_FROM_BLOCK_ACTION.md` tied the selection functional to block-action constants and found:

```text
selection_class: RARE_BLOCK_SELECTION
```

The broad median selected:

\[
\Lambda_{\mathrm{opt}}\approx1.04,
\qquad
\chi_{\mathrm{opt}}\approx0.49.
\]

The target is:

\[
\Lambda_{\mathrm{target}}\approx2.75,
\qquad
\chi_{\mathrm{target}}\approx0.2667.
\]

This file diagnoses why the block-derived selection functional usually misses the target.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Observation**
- **Definition**
- **Lemma candidate**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving or disproving the whole framework.

---

# 1. Prior result

The block-derived selection functional was:

\[
\mathcal F_{\mathrm{block}}(\Lambda)
=
\frac{A_{\mathrm{block}}}{\Lambda}
+
B_{\mathrm{block}}\Lambda
+
\frac{C_{\mathrm{block}}}{\chi(1-\chi)}
+
S_{\mathrm{block}}(\Lambda-q_{\mathrm{block}})^2.
\]

with:

\[
q_{\mathrm{block}}=\Lambda_*=\frac{b}{1-a}.
\]

The verifier found:

```text
Lambda_opt_median_all: 1.0387
chi_opt_median_all: 0.4905
q_block_median_all: 1.0069
```

This already suggests the main failure mode:

\[
q_{\mathrm{block}}\approx1
\quad\Rightarrow\quad
\Lambda_{\mathrm{opt}}\approx1.
\]

---

# 2. Core diagnosis

## Observation 1
The anchor term:

\[
S_{\mathrm{block}}(\Lambda-q_{\mathrm{block}})^2
\]

strongly pulls the optimum toward:

\[
q_{\mathrm{block}}.
\]

If broad sampling makes:

\[
q_{\mathrm{block}}\approx1,
\]

then the selected optimum naturally becomes:

\[
\Lambda_{\mathrm{opt}}\approx1,
\]

which implies:

\[
\chi_{\mathrm{opt}}\approx\frac12.
\]

That is exactly what the verifier observed.

---

# 3. Target-hit regime

For target hits in `CHI_SELECTION_FROM_BLOCK_ACTION.md`, the median was:

```text
q_block_median_hits: 3.3225
Lambda_opt_median_hits: 2.7715
chi_opt_median_hits: 0.2651
```

So the target is selected only when the micro-to-block fixed loading anchor is already high:

\[
q_{\mathrm{block}}\sim3.3.
\]

This is close to the target loading:

\[
\Lambda_{\mathrm{target}}\approx2.75.
\]

Therefore the selection functional does not independently discover the target from a broad neutral prior. It mostly follows the block loading anchor.

---

# 4. Verifier diagnostics

## Status
**Implemented as `chi_selection_failure_analysis_verifier.py`. Execution log captured.**

The verifier resamples block-derived selection and computes:
- medians for all samples and target hits;
- correlations between \(\Lambda_{\mathrm{opt}}\) and \(q_{\mathrm{block}}\);
- whether target selection is mainly anchor-driven.

## Captured verifier output

```text
Chi selection failure analysis verifier
==================================================
Route:
block-derived selection distribution -> failure mode diagnostics

valid_samples: 119784
target_hits: 4402
hit_rate_percent: 3.6749482401656315
target_Lambda: 2.749531308586427
Lopt_median_all: 1.0365881564542432
Lopt_median_hits: 2.7578854937686526
chiopt_median_all: 0.4910172912627695
chiopt_median_hits: 0.26610709710506236
q_median_all: 0.998801965324675
q_median_hits: 3.315916356957126
A_over_B_median_all: 1.0116670011434734
A_over_B_median_hits: 1.0115242112430394
C_median_all: 0.05464488776238266
C_median_hits: 0.05047162799920772
S_median_all: 1.092587333066997
S_median_hits: 1.098768890823941
K_int_median_all: 0.014020695372054505
K_int_median_hits: 0.013983243380433802
K_x_median_all: 0.0008055904983470647
K_x_median_hits: 0.0007092113765262904
b_median_all: 0.8176571237797277
b_median_hits: 2.9264134678772606
a_median_all: 0.10436139980318407
a_median_hits: 0.10127752524432615
corr_Lopt_q: 0.9852490801625345
corr_Lopt_A_over_B: -0.021645160583836132
corr_Lopt_C: -0.12165271864973083
corr_Lopt_S: 0.0918838993198832
q_shift_factor_hits_vs_all: 3.3198937047337904
failure_mode: ANCHOR_CENTERED_NEAR_LAMBDA_1
```

---

# 5. Mathematical reason

The stationarity equation is:

\[
-\frac{A+C}{\Lambda^2}
+
(B+C)
+
2S(\Lambda-q)
=
0.
\]

If \(S\) is non-negligible, then:

\[
\Lambda
\]

is pulled toward \(q\).

If:

\[
A\approx B,
\]

and \(C\) is small, then without the anchor the balance:

\[
\frac{A}{\Lambda}+B\Lambda
\]

selects:

\[
\Lambda\approx\sqrt{A/B}\approx1.
\]

Thus there are two independent reasons for \(\Lambda\approx1\):

1. the anchor \(q\) is broadly centered near 1;
2. the \(A/B\) balance is also broadly centered near 1.

Target selection requires breaking this symmetry.

---

# 6. What extra principle is needed?

To select:

\[
\Lambda\approx2.75,
\]

one of the following must be derived:

## Option 1: high-loading anchor principle

Show that the true block loading anchor is not broad-log-uniform but concentrated near:

\[
q_{\mathrm{block}}\approx3.
\]

That means proving:

\[
\frac{b}{1-a}\approx3
\]

from the microscopic pruning/noise law.

## Option 2: asymmetric memory-insufficiency penalty

Show that:

\[
A/B\gg1
\]

naturally, so the balance:

\[
\frac{A}{\Lambda}+B\Lambda
\]

selects:

\[
\Lambda\approx\sqrt{A/B}\approx2.75.
\]

That requires:

\[
A/B\approx(2.75)^2\approx7.56.
\]

But the current block mapping usually gives:

\[
A/B\approx1.
\]

## Option 3: additional retained-memory selection law

Introduce and derive an additional principle:

```text
retained-memory loading must exceed geometry loading by a stability margin
```

This would be a real new theorem obligation, not a free parameter.

---

# 7. Failure condition

The current block-derived selection route fails as a derivation of:

\[
\chi\approx0.2667
\]

unless it can derive at least one of:

\[
q_{\mathrm{block}}\approx3,
\]

or:

\[
A/B\approx7.5,
\]

or an equivalent retained-memory loading asymmetry.

Without that, the route only shows:

```text
χ≈0.2667 is reachable but rare.
```

---

# 8. Updated status

The honest status is:

```text
χ target selection remains open.
```

More precisely:

```text
block-action selection can reach χ≈0.2667, but broad block priors prefer χ≈0.49 because the loading anchor and A/B balance are centered near Λ≈1.
```

---

# 9. Recommended next file

The next file should be:

```text
RETAINED_MEMORY_LOADING_ASYMMETRY.md
```

Its job:

Test whether the microscopic retained-memory recursion implies:

\[
\frac{b}{1-a}\approx3
\]

or:

\[
A/B\approx7.5.
\]

If it does, \(\chi\)-selection may become derivable.

If it does not, \(\chi\approx0.2667\) remains phenomenological/reachable rather than derived.

---

# Honest status line

> `CHI_SELECTION_FAILURE_ANALYSIS.md` identifies the main failure mode: block-derived selection usually lands near \(\Lambda\approx1\) because both the loading anchor and \(A/B\) balance are centered there. Target \(\chi\approx0.2667\) requires a derived retained-memory loading asymmetry that has not yet been shown.

**End of file.**
