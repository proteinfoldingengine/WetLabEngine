# V421 Blind Independent Validation Report

## Summary

This run tests the frozen V420 retained-atlas law candidate on an independent surrogate with new topology, noise, missing-channel, high-stress, fragmentation, delayed-recovery, and coordinated-drift regimes.

Frozen law:

```text
S_t = M_t × R_t × L_t
```

Survival requires confidence-adjusted dynamic floors for S and each factor M/R/L.

## Aggregate Results

| controller                   |    bad |   harmed |   reclosed |   fidelity |   future_R |   attractor |   score |
|:-----------------------------|-------:|---------:|-----------:|-----------:|-----------:|------------:|--------:|
| V420_full_guarded_law        | 0.4694 |   0.0784 |     0.4718 |     0.4766 |     0.5211 |      0.5469 |  2.1759 |
| S_residual_uncertainty       | 0.4758 |   0.0821 |     0.5034 |     0.4650 |     0.5067 |      0.5246 |  2.2605 |
| S_constrained_dynamic_floors | 0.4899 |   0.0887 |     0.5358 |     0.4521 |     0.4902 |      0.4987 |  2.3619 |
| A_plus_L                     | 0.5217 |   0.1416 |     0.5891 |     0.4152 |     0.4482 |      0.4498 |  2.6320 |
| A_only                       | 0.5345 |   0.1648 |     0.6219 |     0.3954 |     0.4265 |      0.4226 |  2.7698 |
| greedy_damage_minimizer      | 0.5056 |   0.6800 |     0.7848 |     0.2598 |     0.2315 |      0.2845 |  4.1049 |

## Interpretation

Best composite controller:

```text
V420_full_guarded_law
```

V420 full guarded law:

```text
bad      0.4694
harmed   0.0784
reclosed 0.4718
fidelity 0.4766
future_R 0.5211
attractor 0.5469
score    2.1759
```

Greedy damage minimizer:

```text
bad      0.5056
harmed   0.6800
reclosed 0.7848
fidelity 0.2598
future_R 0.2315
attractor 0.2845
score    4.1049
```

## Peer-Review Finding

The V420 full guarded law is not optimized for lowest immediate bad rate. It is optimized for low destructive recovery: lower harm, lower reclosure, higher post-exit fidelity, higher future retained recovery capacity, and higher attractor entry.

If V420 is the best or near-best composite controller and strongly dominates greedy minimization on harm/reclosure/fidelity/future_R, the freeze candidate survives this independent validation.

## Regime Table

| regime              | controller                   |    bad |   harmed |   reclosed |   fidelity |   future_R |   attractor |   score |
|:--------------------|:-----------------------------|-------:|---------:|-----------:|-----------:|-----------:|------------:|--------:|
| clean               | greedy_damage_minimizer      | 0.3581 |   0.4497 |     0.6128 |     0.3860 |     0.3673 |      0.4624 |  3.0775 |
| clean               | A_only                       | 0.3738 |   0.0934 |     0.4604 |     0.4850 |     0.5113 |      0.5855 |  2.0728 |
| clean               | A_plus_L                     | 0.3629 |   0.0864 |     0.4338 |     0.4969 |     0.5239 |      0.6077 |  1.9865 |
| clean               | S_constrained_dynamic_floors | 0.3446 |   0.0709 |     0.4164 |     0.5110 |     0.5395 |      0.6281 |  1.8888 |
| clean               | S_residual_uncertainty       | 0.3396 |   0.0653 |     0.4006 |     0.5164 |     0.5465 |      0.6393 |  1.8392 |
| clean               | V420_full_guarded_law        | 0.3411 |   0.0660 |     0.3847 |     0.5215 |     0.5529 |      0.6513 |  1.8065 |
| noisy               | greedy_damage_minimizer      | 0.4354 |   0.5930 |     0.7036 |     0.3208 |     0.2891 |      0.3645 |  3.6587 |
| noisy               | A_only                       | 0.4577 |   0.1285 |     0.5279 |     0.4457 |     0.4705 |      0.5077 |  2.3976 |
| noisy               | A_plus_L                     | 0.4439 |   0.1129 |     0.4954 |     0.4620 |     0.4884 |      0.5344 |  2.2771 |
| noisy               | S_constrained_dynamic_floors | 0.4201 |   0.0747 |     0.4495 |     0.4911 |     0.5215 |      0.5774 |  2.0641 |
| noisy               | S_residual_uncertainty       | 0.4021 |   0.0719 |     0.4174 |     0.5043 |     0.5379 |      0.6044 |  1.9648 |
| noisy               | V420_full_guarded_law        | 0.3969 |   0.0676 |     0.3874 |     0.5150 |     0.5511 |      0.6250 |  1.8848 |
| missing_channel     | greedy_damage_minimizer      | 0.4606 |   0.6405 |     0.7456 |     0.2920 |     0.2609 |      0.3249 |  3.8786 |
| missing_channel     | A_only                       | 0.4911 |   0.1354 |     0.5678 |     0.4256 |     0.4540 |      0.4715 |  2.5400 |
| missing_channel     | A_plus_L                     | 0.4818 |   0.1184 |     0.5345 |     0.4436 |     0.4734 |      0.4996 |  2.4177 |
| missing_channel     | S_constrained_dynamic_floors | 0.4399 |   0.0797 |     0.4765 |     0.4793 |     0.5134 |      0.5542 |  2.1546 |
| missing_channel     | S_residual_uncertainty       | 0.4213 |   0.0722 |     0.4336 |     0.4982 |     0.5365 |      0.5907 |  2.0190 |
| missing_channel     | V420_full_guarded_law        | 0.4106 |   0.0681 |     0.3977 |     0.5106 |     0.5519 |      0.6142 |  1.9217 |
| high_stress         | greedy_damage_minimizer      | 0.6119 |   0.8524 |     0.8733 |     0.1821 |     0.1353 |      0.1769 |  4.7844 |
| high_stress         | A_only                       | 0.6567 |   0.2287 |     0.6866 |     0.3445 |     0.3700 |      0.3266 |  3.2017 |
| high_stress         | A_plus_L                     | 0.6460 |   0.1877 |     0.6523 |     0.3694 |     0.3979 |      0.3537 |  3.0263 |
| high_stress         | S_constrained_dynamic_floors | 0.6116 |   0.0997 |     0.5732 |     0.4213 |     0.4581 |      0.4161 |  2.6304 |
| high_stress         | S_residual_uncertainty       | 0.6023 |   0.0932 |     0.5408 |     0.4328 |     0.4736 |      0.4380 |  2.5370 |
| high_stress         | V420_full_guarded_law        | 0.5954 |   0.0870 |     0.5059 |     0.4475 |     0.4916 |      0.4634 |  2.4371 |
| fragmentation_heavy | greedy_damage_minimizer      | 0.5682 |   0.7435 |     0.8644 |     0.1990 |     0.1891 |      0.2081 |  4.4924 |
| fragmentation_heavy | A_only                       | 0.5986 |   0.1910 |     0.7127 |     0.3440 |     0.3973 |      0.3438 |  3.0987 |
| fragmentation_heavy | A_plus_L                     | 0.5813 |   0.1607 |     0.6739 |     0.3689 |     0.4248 |      0.3762 |  2.9264 |
| fragmentation_heavy | S_constrained_dynamic_floors | 0.5402 |   0.0966 |     0.6125 |     0.4132 |     0.4756 |      0.4335 |  2.6024 |
| fragmentation_heavy | S_residual_uncertainty       | 0.5310 |   0.0880 |     0.5817 |     0.4253 |     0.4917 |      0.4574 |  2.5064 |
| fragmentation_heavy | V420_full_guarded_law        | 0.5252 |   0.0847 |     0.5472 |     0.4382 |     0.5078 |      0.4824 |  2.4157 |
| delayed_recovery    | greedy_damage_minimizer      | 0.5590 |   0.7395 |     0.8581 |     0.2147 |     0.1831 |      0.2198 |  4.4525 |
| delayed_recovery    | A_only                       | 0.5828 |   0.2045 |     0.7229 |     0.3524 |     0.3765 |      0.3465 |  3.1231 |
| delayed_recovery    | A_plus_L                     | 0.5689 |   0.1754 |     0.6916 |     0.3761 |     0.4025 |      0.3766 |  2.9694 |
| delayed_recovery    | S_constrained_dynamic_floors | 0.5323 |   0.1035 |     0.6276 |     0.4224 |     0.4551 |      0.4360 |  2.6300 |
| delayed_recovery    | S_residual_uncertainty       | 0.5161 |   0.0974 |     0.6006 |     0.4337 |     0.4706 |      0.4600 |  2.5375 |
| delayed_recovery    | V420_full_guarded_law        | 0.5099 |   0.0924 |     0.5653 |     0.4467 |     0.4868 |      0.4848 |  2.4425 |
| coordinated_drift   | greedy_damage_minimizer      | 0.5463 |   0.7412 |     0.8358 |     0.2239 |     0.1957 |      0.2350 |  4.3899 |
| coordinated_drift   | A_only                       | 0.5806 |   0.1720 |     0.6750 |     0.3704 |     0.4058 |      0.3767 |  2.9548 |
| coordinated_drift   | A_plus_L                     | 0.5669 |   0.1499 |     0.6425 |     0.3893 |     0.4265 |      0.4003 |  2.8208 |
| coordinated_drift   | S_constrained_dynamic_floors | 0.5404 |   0.0954 |     0.5949 |     0.4265 |     0.4684 |      0.4458 |  2.5630 |
| coordinated_drift   | S_residual_uncertainty       | 0.5182 |   0.0869 |     0.5488 |     0.4442 |     0.4899 |      0.4826 |  2.4193 |
| coordinated_drift   | V420_full_guarded_law        | 0.5065 |   0.0830 |     0.5144 |     0.4567 |     0.5056 |      0.5071 |  2.3228 |

## Claim Boundary

This does not prove a universal law. It tests whether the frozen V420 structure generalizes to a new surrogate without retuning.
