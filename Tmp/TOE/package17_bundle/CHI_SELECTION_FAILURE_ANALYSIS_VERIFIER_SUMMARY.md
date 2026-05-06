# CHI_SELECTION_FAILURE_ANALYSIS_VERIFIER_SUMMARY.md

# Verifier Summary
## Failure analysis for block-derived \(\chi\)-selection

## Status
**Executed failure analysis.**

Verifier file:

```text
chi_selection_failure_analysis_verifier.py
```

Execution log:

```text
chi_selection_failure_analysis_verifier_run.log
```

## Captured output

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

## Interpretation

The verifier confirms that block-derived \(\chi\)-selection is mainly controlled by the loading anchor \(q_{\mathrm{block}}\).

Broad samples center \(q_{\mathrm{block}}\) near \(\Lambda\approx1\), selecting \(\chi\approx0.5\).

Target hits require \(q_{\mathrm{block}}\) shifted upward toward \(\sim3\).

**End of summary.**
