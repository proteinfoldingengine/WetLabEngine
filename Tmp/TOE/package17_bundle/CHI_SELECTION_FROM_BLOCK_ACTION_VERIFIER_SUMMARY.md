# CHI_SELECTION_FROM_BLOCK_ACTION_VERIFIER_SUMMARY.md

# Verifier Summary
## \(\chi\)-selection from block-action constants

## Status
**Executed block-selection verifier. Candidate mapping only.**

Verifier file:

```text
chi_selection_from_block_action_verifier.py
```

Execution log:

```text
chi_selection_from_block_action_verifier_run.log
```

## Captured output

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

## Interpretation

The verifier maps block constants:

\[
K_U,K_x,K_{\mathrm{int}}
\]

to the selection-functional coefficients and minimizes:

\[
\mathcal F_{\mathrm{block}}(\Lambda).
\]

This tests whether target \(\chi\) selection remains plausible when the balance coefficients are tied to block-action objects.

**End of summary.**
