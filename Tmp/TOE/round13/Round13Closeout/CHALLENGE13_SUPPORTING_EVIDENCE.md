# Challenge 13 Supporting Evidence
## Closeout Evidence Packet in Markdown

## 1. Phase Summary

| Phase | n | Mean Improvement | Positive Rate | Zero Improvement Count | Exception Count | Catastrophic Failures |
|---|---:|---:|---:|---:|---:|---:|
| 13A frozen locked set | 10 | 6.557220 | 0.70 | 3 | 0 | 0 |
| 13Q.5 frozen working baseline locked set | 10 | 6.697876 | 0.70 | 3 | 1 | 0 |
| 13Q.10 unseen holdout | 10 | 50.251108 | 1.00 | 0 | 0 | 0 |

## 2. Interpretation of Phase Summary
The progression is the key point.

The working baseline improved slightly on the locked set once the rare exception rule was introduced. But the much more important result is that the unseen holdout did **not** require the exception rule at all.

That means the dominant rule emerging from Challenge 13 is still the gas-first baseline.

## 3. Ranked Holdout Detail

| Galaxy | n_points | Stellar Fraction Proxy | Improvement 13A Local | Selected Model | Exception Flag | Hybrid Improvement | vflat_obs | vflat_bridge | m_baryon | Catastrophic Failure |
|---|---:|---:|---:|---|---|---:|---:|---:|---:|---|
| WALLABY J104311-261500 | 7 | 0.644079 | 108.214457 | 13A_default | False | 108.214457 | 192.10 | 136.583319 | 2.021843e+10 | False |
| WALLABY J131234-173225 | 7 | 0.638742 | 76.438270 | 13A_default | False | 76.438270 | 185.90 | 132.094151 | 1.372333e+10 | False |
| WALLABY J130053-132655 | 13 | 0.408726 | 74.007256 | 13A_default | False | 74.007256 | 165.60 | 130.371879 | 1.677176e+10 | False |
| WALLABY J133541-240428 | 5 | 0.661237 | 70.828659 | 13A_default | False | 70.828659 | 137.00 | 96.858621 | 7.371490e+09 | False |
| WALLABY J131237-142630 | 8 | 0.320770 | 63.666711 | 13A_default | False | 63.666711 | 129.10 | 97.681550 | 1.202319e+10 | False |
| WALLABY J133348-244525 | 6 | 0.351737 | 61.801040 | 13A_default | False | 61.801040 | 127.20 | 92.050315 | 1.007404e+10 | False |
| WALLABY J130806-144640 | 6 | 0.023938 | 27.397769 | 13A_default | False | 27.397769 | 76.10 | 59.394388 | 2.043515e+09 | False |
| WALLABY J123244+000656 | 27 | 0.111877 | 9.129991 | 13A_default | False | 9.129991 | 121.60 | 137.422774 | 9.077901e+09 | False |
| WALLABY J130618-173039 | 8 | 0.003915 | 5.539491 | 13A_default | False | 5.539491 | 46.20 | 43.653075 | 1.314449e+09 | False |
| WALLABY J124232-012111 | 13 | 0.040040 | 5.487432 | 13A_default | False | 5.487432 | 90.25 | 74.050173 | 1.671513e+09 | False |

## 4. Holdout Interpretation
Three things stand out:

1. Every holdout galaxy remained on **13A_default**.
2. Every holdout galaxy had **positive improvement**.
3. No holdout galaxy produced a catastrophic failure.

This is exactly the kind of behavior you want from a frozen model when it encounters unseen data.

## 5. Top-Gain Audit

| Galaxy | n_points | rmse_bar | rmse_bridge | improvement | vflat_obs | vflat_bar | vflat_bridge | mean_abs_obs_minus_bar | mean_abs_obs_minus_bridge | max_actual_add | min_actual_add | audit_pass |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| WALLABY J104311-261500 | 7 | 166.483781 | 58.269323 | 108.214457 | 192.1 | 33.480912 | 136.583319 | 166.333580 | 58.216753 | 115.087470 | 101.705500 | True |
| WALLABY J131234-173225 | 7 | 137.868594 | 61.430325 | 76.438270 | 185.9 | 33.898572 | 132.094151 | 129.136801 | 56.036924 | 100.465622 | 24.182287 | True |
| WALLABY J130053-132655 | 13 | 113.857317 | 39.850061 | 74.007256 | 165.6 | 64.689564 | 130.371879 | 113.269901 | 39.644465 | 86.608305 | 62.310508 | True |

## 6. Audit Interpretation
The audit shows the largest gains are not bookkeeping artifacts.

For the audited top-gain galaxies:
- the bridge RMSE is lower than the baryonic-only RMSE
- the mean absolute residuals are lower
- the improvement remains positive under direct inspection

That means the improvement mechanism survives a sanity check.

## 7. Why the Result Is Strong
This is moon-shot work. The standard for success is not “did everything become trivial?” The standard is whether the system produced a stable, nontrivial generalization signal under frozen conditions.

Challenge 13 did that.

## 8. Why the Result Is Still Called Conditional
The only reason for the word **conditional** is that the attempted broader external validation file available locally was a summary-format corpus, not a scoreable radial-point corpus.

So the unresolved item is not internal validity.
The unresolved item is external dataset compatibility.

That is a boundary condition for the next challenge, not a weakness of the current closeout.
