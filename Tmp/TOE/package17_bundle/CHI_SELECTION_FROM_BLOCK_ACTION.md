# CHI_SELECTION_FROM_BLOCK_ACTION.md

# Chi Selection From Block Action
## Testing whether the \(\chi\)-selection functional can be derived from block-action constants

## Status
**Block-derived selection candidate. Not unique microscopic derivation.**

`CHI_SELECTION_PRINCIPLE.md` introduced a candidate balance functional:

\[
\mathcal F(\Lambda)
=
\frac{A}{\Lambda}
+
B\Lambda
+
\frac{C}{\chi(\Lambda)(1-\chi(\Lambda))}
+
S(\Lambda-q)^2.
\]

That file showed the target:

\[
\chi_*\approx0.2667
\]

is selection-plausible under a broad positive balance family.

This file asks the harder question:

> Can \(A,B,C,S,q\) be tied to the block-action constants \(K_t,K_U,K_x,K_{\mathrm{int}}\)?

This is a necessary step before claiming \(\chi\) selection is derived rather than phenomenological.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Lemma candidate**
- **Theorem candidate**
- **Derivation target**
- **Failure condition**
- **Closure status**

Nothing here should be interpreted as a full derivation of \(\chi\) from first principles.

---

# 1. Block action constants

From `COEFFICIENT_CLOSURE_FROM_MICRO_TO_BLOCK.md`:

\[
K_t=1+w_s\alpha_s+w_f\alpha_f,
\]

\[
K_U=K_t(1-a),
\]

\[
K_x=K_t\chi(1-\chi)\sigma_{\nabla\Lambda}^2,
\]

\[
K_{\mathrm{int}}
=
K_t\chi(1-\chi)\rho_{\mathrm{mat}}.
\]

These define:
- memory potential stiffness;
- spatial coherence weight;
- matter coupling weight;
- kinetic/time normalization.

---

# 2. Candidate block-derived selection functional

## Definition 1
Define:

\[
\chi(\Lambda)=\frac{1}{1+\Lambda}.
\]

Use the same balance structure:

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

Now tie coefficients to block quantities:

\[
A_{\mathrm{block}}\sim K_U+K_{\mathrm{int}},
\]

\[
B_{\mathrm{block}}\sim K_U,
\]

\[
C_{\mathrm{block}}\sim K_x+K_{\mathrm{int}},
\]

\[
q_{\mathrm{block}}\sim\Lambda_*=\frac{b}{1-a},
\]

\[
S_{\mathrm{block}}\sim\frac{K_U}{1+K_x+K_{\mathrm{int}}}.
\]

These identifications are candidate mappings, not final uniqueness claims.

---

# 3. Why these identifications are plausible

## 3.1 \(A_{\mathrm{block}}\)

The term:

\[
\frac{A}{\Lambda}
\]

penalizes insufficient memory loading.

A natural block source is:

\[
K_U+K_{\mathrm{int}},
\]

because insufficient memory undermines both the memory well and matter-memory interaction.

## 3.2 \(B_{\mathrm{block}}\)

The term:

\[
B\Lambda
\]

penalizes excessive memory domination.

A natural source is:

\[
K_U,
\]

because the restoring potential resists displacement from the stable memory loading state.

## 3.3 \(C_{\mathrm{block}}\)

The term:

\[
\frac{C}{\chi(1-\chi)}
\]

penalizes weak bridge responsiveness.

A natural source is:

\[
K_x+K_{\mathrm{int}},
\]

because both spatial coherence and matter coupling depend on the bridge factor:

\[
\chi(1-\chi).
\]

## 3.4 \(q_{\mathrm{block}}\)

The anchor:

\[
q
\]

should be the micro-to-block fixed loading:

\[
q_{\mathrm{block}}=\Lambda_*=\frac{b}{1-a}.
\]

## 3.5 \(S_{\mathrm{block}}\)

The anchor strength is naturally proportional to memory restoring stiffness:

\[
K_U,
\]

and suppressed by large coherence/coupling flexibility:

\[
1+K_x+K_{\mathrm{int}}.
\]

Thus:

\[
S_{\mathrm{block}}\sim
\frac{K_U}{1+K_x+K_{\mathrm{int}}}.
\]

---

# 4. Stationarity equation

Because:

\[
\frac{1}{\chi(1-\chi)}
=
\Lambda+2+\frac{1}{\Lambda},
\]

the functional becomes:

\[
\mathcal F_{\mathrm{block}}
=
\frac{A_{\mathrm{block}}+C_{\mathrm{block}}}{\Lambda}
+
(B_{\mathrm{block}}+C_{\mathrm{block}})\Lambda
+
2C_{\mathrm{block}}
+
S_{\mathrm{block}}(\Lambda-q_{\mathrm{block}})^2.
\]

The stationarity equation is:

\[
-\frac{A_{\mathrm{block}}+C_{\mathrm{block}}}{\Lambda^2}
+
(B_{\mathrm{block}}+C_{\mathrm{block}})
+
2S_{\mathrm{block}}(\Lambda-q_{\mathrm{block}})
=
0.
\]

Equivalently:

\[
2S_{\mathrm{block}}\Lambda^3
+
(B_{\mathrm{block}}+C_{\mathrm{block}}-2S_{\mathrm{block}}q_{\mathrm{block}})\Lambda^2
-
(A_{\mathrm{block}}+C_{\mathrm{block}})
=
0.
\]

---

# 5. Verifier implementation

## Status
**Implemented as `chi_selection_from_block_action_verifier.py`. Execution log captured.**

The verifier samples block-action constants and computes:

\[
A_{\mathrm{block}},
B_{\mathrm{block}},
C_{\mathrm{block}},
S_{\mathrm{block}},
q_{\mathrm{block}}.
\]

Then it minimizes:

\[
\mathcal F_{\mathrm{block}}(\Lambda)
\]

and tests how often the optimum satisfies:

\[
\chi_{\mathrm{opt}}\approx0.2667.
\]

## Captured verifier output

```text
Chi selection from block action verifier
==================================================
Route:
block constants -> selection coefficients -> Lambda optimum
Tests block-derived plausibility, not unique derivation.

valid_samples: 99860
target_hits: 3819
hit_rate_percent: 3.824354095734028
selection_class: RARE_BLOCK_SELECTION
Lambda_opt_median_all: 1.0387433444143614
chi_opt_median_all: 0.49049822908790647
q_block_median_all: 1.0068674915323035
chi_micro_median_all: 0.4982890022535409
a_median_all: 0.10445783889072627
b_median_all: 0.8216350082081985
K_U_median_all: 1.243143913637109
K_x_median_all: 0.0008032285446019105
K_int_median_all: 0.013938898165227061
A_median_all: 1.3179716202048146
B_median_all: 1.243143913637109
C_median_all: 0.05516180436089352
S_median_all: 1.0933161681861772
Lambda_opt_median_hits: 2.771541338824044
Lambda_opt_p10_hits: 2.533388827446085
Lambda_opt_p90_hits: 2.990459113202914
chi_opt_median_hits: 0.2651435872400638
chi_opt_p10_hits: 0.25059773114611794
chi_opt_p90_hits: 0.2830144229336896
q_block_median_hits: 3.3224997357979547
q_block_p10_hits: 3.014923139685374
q_block_p90_hits: 3.7971863069361893
chi_micro_median_hits: 0.23134761390919903
chi_micro_p10_hits: 0.20845552908085382
chi_micro_p90_hits: 0.249070770706249
a_median_hits: 0.10545654641828751
a_p10_hits: 0.024358668573941433
a_p90_hits: 0.3683179409143863
b_median_hits: 2.9390365714050097
b_p10_hits: 2.099547102099264
b_p90_hits: 3.4434989801392724
K_U_median_hits: 1.2422962903200332
K_U_p10_hits: 0.9789373013226547
K_U_p90_hits: 1.5482749641763125
K_x_median_hits: 0.0006637008558377016
K_x_p10_hits: 1.2322505238077745e-06
K_x_p90_hits: 0.325645318465903
K_int_median_hits: 0.014530710984297826
K_int_p10_hits: 0.0005809427262449695
K_int_p90_hits: 0.3241620765899138
A_median_hits: 1.3119055718693864
A_p10_hits: 1.0219638092434826
A_p90_hits: 1.7027183570997462
B_median_hits: 1.2422962903200332
B_p10_hits: 0.9789373013226547
B_p90_hits: 1.5482749641763125
C_median_hits: 0.052767172315975594
C_p10_hits: 0.001387524458127408
C_p90_hits: 0.5918622771190887
S_median_hits: 1.100027945229216
S_p10_hits: 0.6998139815874771
S_p90_hits: 1.4478988213282142
```

---

# 6. What this file establishes

### Established

1. A block-action-derived version of the \(\chi\)-selection functional is explicit.
2. The stationarity equation remains cubic.
3. Selection coefficients can be tied to \(K_U,K_x,K_{\mathrm{int}}\).
4. The target \(\chi\) can be tested without free \(A,B,C,S,q\).

### Not yet established

1. The coefficient identifications are plausible but not uniquely derived.
2. \(q_{\mathrm{block}}\) inherits the micro-to-block loading fixed point rather than explaining it from a deeper principle.
3. The selection functional is not yet derived by varying the full block action.
4. Target selection may still depend on priors over block constants.

---

# 7. Interpretation rule

If the verifier reports:

```text
BLOCK_SELECTION_PLAUSIBLE
```

then block constants can plausibly generate the target-selection balance.

If it reports:

```text
RARE_BLOCK_SELECTION
```

then the block-derived version is possible but not natural.

If it reports:

```text
NOT_FOUND
```

then this candidate block selection route fails.

---

# 8. Next derivation target

The next file should depend on verifier outcome.

If plausible:

```text
CHI_SELECTION_CLOSURE_STATUS.md
```

If rare or failed:

```text
CHI_SELECTION_FAILURE_ANALYSIS.md
```

---

# Honest status line

> `CHI_SELECTION_FROM_BLOCK_ACTION.md` ties the \(\chi\)-selection functional to block-action constants and tests whether target selection remains plausible without free phenomenological coefficients. It does not yet prove the mapping is unique or derived from variation of the full block action.

**End of file.**
