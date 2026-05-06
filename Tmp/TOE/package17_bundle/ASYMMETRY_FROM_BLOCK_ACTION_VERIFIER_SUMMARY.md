# ASYMMETRY_FROM_BLOCK_ACTION_VERIFIER_SUMMARY.md

# Verifier Summary
## Testing block-action derivation of the asymmetry parameters

## Status
**Executed decisive asymmetry verifier.**

Verifier file:

```text
asymmetry_from_block_action_verifier.py
```

Execution log:

```text
asymmetry_from_block_action_verifier_run.log
```

## Captured output

```text
Asymmetry from block action verifier
==================================================
Route:
block constants -> derived A/B and q0 -> check target asymmetry

valid_samples: 149702
joint_AoverB_q0_hits: 0
joint_hit_rate_percent: 0.0
q_target_hits: 2313
q_target_hit_rate_percent: 1.5450695381491228
A_over_B_median_all: 1.0084773693271405
A_over_B_p90_all: 1.3270892805064372
A_over_B_p99_all: 2.757816717495087
q0_median_all: 0.16450296031662284
q0_p90_all: 14.971886602722599
q_median_all: 0.17173892183619727
chi_median_all: 0.8534324339681527
K_int_over_KU_median_all: 0.002392767006814339
K_x_over_KU_median_all: 0.00012374725418004388
qtarget_A_over_B_median: 1.0551950124012912
qtarget_q0_median: 3.0557388536727226
qtarget_q_median: 3.0042832761743385
qtarget_chi_median: 0.24973258159582365
qtarget_K_U_median: 1.2202527830522194
qtarget_K_x_median: 0.0009616894892550711
qtarget_K_int_median: 0.015405887936981687
qtarget_beta_s_median: 0.5657134760249485
qtarget_beta_f_median: 0.26073826859393756
qtarget_G_star_median: 0.09130077157826098
qtarget_eps_over_sigma_median: 1.7500639286778896
qtarget_If_over_Is_median: 0.21624097303552464
closure_class: NOT_FOUND
```

## Interpretation

The verifier tests whether current block-action quantities naturally produce:

\[
A/B\approx7.5\text{–}9.5,
\qquad
q_0\approx3.
\]

Under the tested mapping, this requires:

\[
K_{\mathrm{int}}+K_x\gg K_U.
\]

If the joint target is rare or absent, the \(\chi\)-selection seam remains open.

**End of summary.**
