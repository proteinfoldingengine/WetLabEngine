# CHI_SELECTION_PRINCIPLE_VERIFIER_SUMMARY.md

# Verifier Summary
## Candidate variational selection principle for \(\chi\)

## Status
**Executed selection-principle verifier. Candidate only.**

Verifier file:

```text
chi_selection_principle_verifier.py
```

Execution log:

```text
chi_selection_principle_verifier_run.log
```

## Captured output

```text
Chi selection principle verifier
==================================================
Route:
candidate balance functional -> selected Lambda* and chi*
This tests plausibility of a selection principle, not final derivation.

valid_samples: 100000
target_hits: 5066
hit_rate_percent: 5.066
naturalness_class: SELECTION_PLAUSIBLE
Lambda_opt_median_all: 1.1054058557693487
chi_opt_median_all: 0.4749678059741997
A_median_all: 1.0008773810867964
B_median_all: 0.9897794221920191
C_median_all: 0.0254503615180091
S_median_all: 0.3145678329747716
q_median_all: 1.0181497309142418
Lambda_opt_median_hits: 2.7524526710413353
Lambda_opt_p10_hits: 2.5509582549607996
Lambda_opt_p90_hits: 2.990459113202914
chi_opt_median_hits: 0.26649236850267644
chi_opt_p10_hits: 0.25059773114611794
chi_opt_p90_hits: 0.28161412446991424
A_median_hits: 2.945467663999203
A_p10_hits: 0.26699951397242205
A_p90_hits: 8.11491282120507
B_median_hits: 0.39607220149356537
B_p10_hits: 0.13089169074273926
B_p90_hits: 2.3006066737474655
C_median_hits: 0.02414177396275554
C_p10_hits: 0.0018821935999916541
C_p90_hits: 0.32235984097707526
S_median_hits: 0.18174502317717867
S_p10_hits: 0.018870015038210765
S_p90_hits: 4.737167202619503
q_median_hits: 2.7677533542558184
q_p10_hits: 0.28393778937984904
q_p90_hits: 5.074943266209216
Lambda_target: 2.749531308586427
```

## Interpretation

The verifier minimizes the candidate balance functional:

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

It tests whether this kind of balance can select:

\[
\chi\approx0.2667.
\]

This is a selection-principle candidate, not a first-principles derivation.

**End of summary.**
