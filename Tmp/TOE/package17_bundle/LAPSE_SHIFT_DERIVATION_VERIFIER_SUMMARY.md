# LAPSE_SHIFT_DERIVATION_VERIFIER_SUMMARY.md

# Verifier Summary
## Lapse and shift from causal slice data

## Status
**Executed structural verifier. Shift remains proxy-level.**

Verifier file:

```text
lapse_shift_derivation_verifier.py
```

Execution log:

```text
lapse_shift_derivation_verifier_run.log
```

## Captured output

```text
Lapse and shift derivation verifier
==================================================
Route:
rank spacing + slice density -> lapse N
slice-to-slice antichain embedding drift -> shift proxy N_a

PASS: 93.33333333333333
SOFT_FAIL: 0.0
HARD_FAIL: 6.666666666666667
n_slice_pairs_median: 8.5
lapse_median_median: 1.0000000000000098
lapse_cv_median: 0.06078055543310073
shift_norm_median_median: 0.06788315909892383
shift_finite_fraction_median: 1.0
hidden_shift_corr_median: -0.09750757047375347
```

## Interpretation

The verifier tests:
- lapse from causal rank spacing and slice density;
- shift proxy from slice-to-slice antichain embedding drift.

Lapse is structurally viable. Shift remains gauge-dependent until slice alignment / graph matching is implemented.

**End of summary.**
