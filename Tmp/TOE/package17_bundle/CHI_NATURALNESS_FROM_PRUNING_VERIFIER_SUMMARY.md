# CHI_NATURALNESS_FROM_PRUNING_VERIFIER_SUMMARY.md

# Verifier Summary
## Naturalness of \(\chi_*\approx0.2667\) under pruning/noise sampling

## Status
**Executed naturalness verifier. Not first-principles selection.**

Verifier file:

```text
chi_naturalness_from_pruning_verifier.py
```

Execution log:

```text
chi_naturalness_from_pruning_verifier_run.log
```

## Captured output

```text
Chi naturalness from pruning verifier
==================================================
Route:
broad pruning/noise sampling with explicit I_s,I_f -> chi* distribution

valid_samples: 249539
target_hits: 2143
hit_rate_percent: 0.858783596952781
chi_median_all: 0.8527751752703292
chi_p10_all: 0.061434340623868114
chi_p90_all: 0.9983735550437378
Lambda_median_all: 0.17264201515129765
logLambda_distance_median: 3.1382145421049943
hit_a_median: 0.11863619656071525
hit_b_median: 2.4152643015811384
hit_G_star_median: 0.09804365580627097
hit_beta_s_median: 0.5458242221063235
hit_beta_f_median: 0.257958959177852
hit_eps_over_sigma_median: 1.7629387008820712
hit_I_f_over_I_s_median: 0.21140566010193304
hit_sigma_median: 1.678014439167241
naturalness_class: RARE_BUT_REACHABLE
```

## Interpretation

The verifier samples broad pruning/noise regimes with explicit:

\[
I_s,\quad I_f(\varepsilon^*)
\]

and computes the resulting:

\[
\chi_*.
\]

This measures whether the target appears naturally under the chosen sampling prior.

**End of summary.**
