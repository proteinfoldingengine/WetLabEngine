# ASYMMETRY_SELECTION_PRINCIPLE_VERIFIER_SUMMARY.md

# Verifier Summary
## Intermediate retained-memory loading selection

## Status
**Executed stabilization-principle verifier. Candidate only.**

Verifier file:

```text
asymmetry_selection_principle_verifier.py
```

Execution log:

```text
asymmetry_selection_principle_verifier_run.log
```

## Captured output

```text
Asymmetry selection principle verifier
==================================================
Route:
underload + overload + critical-band + bridge-response penalties -> selected q=b/(1-a)
Tests intermediate-loading stabilization, not final derivation.

valid_samples: 100000
target_band_hits: 5150
target_band_hit_rate_percent: 5.15
selection_class: STABILIZATION_PLAUSIBLE
qopt_median_all: 1.2275231083861395
chiopt_median_all: 0.44892912501568116
A_median_all: 1.7975418904241978
B_median_all: 1.7810096224787921
C_median_all: 0.3154873000869417
D_median_all: 0.007858400277544472
q0_median_all: 1.9867353639387744
A_over_B_median_all: 1.0147875585407822
qopt_median_hits: 3.00026111275527
qopt_p10_hits: 2.7999420937032915
qopt_p90_hits: 3.2297560709039357
chiopt_median_hits: 0.24998368151803657
chiopt_p10_hits: 0.23642025290273805
chiopt_p90_hits: 0.2631619049293024
A_median_hits: 5.28344841448599
A_p10_hits: 0.4249661941036908
A_p90_hits: 22.30932516142066
B_median_hits: 0.539018569699225
B_p10_hits: 0.1375941795046336
B_p90_hits: 2.311026127939568
C_median_hits: 0.6627094128599387
C_p10_hits: 0.025401678128113205
C_p90_hits: 5.985785798765115
D_median_hits: 0.007836907743859256
D_p10_hits: 0.0002449060897038847
D_p90_hits: 0.2565046185481074
q0_median_hits: 2.960010550186321
q0_p10_hits: 0.9461211523725174
q0_p90_hits: 5.224007597005755
A_over_B_median_hits: 9.395868385300648
A_over_B_p10_hits: 1.1086512637511443
A_over_B_p90_hits: 26.786365026435636
```

## Interpretation

The verifier minimizes:

\[
\mathcal A(q)
=
\frac{A}{q}
+
Bq
+
C[\log(q/q_0)]^2
+
\frac{D}{\chi(q)(1-\chi(q))}.
\]

It tests whether an intermediate-loading stabilization principle can select:

\[
q\approx2.75\text{–}3.3.
\]

This is not yet derived from microscopic dynamics.

**End of summary.**
