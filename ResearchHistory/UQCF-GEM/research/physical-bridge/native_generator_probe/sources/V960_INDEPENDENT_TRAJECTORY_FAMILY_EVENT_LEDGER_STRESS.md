# V960 Independent Trajectory-Family Event-Ledger Stress

## Verdict

`independent_trajectory_family_event_ledger_stress_certified`

Closed for V960 independent stress: **True**

## Purpose

V959 certified V930 + V957. V960 tests a harder independently generated trajectory family.

## Stress domain

```text
trajectory rows: 14148
path rows: 432
seeds: [84011, 84047, 84089]
resolutions: [10, 28, 40]
geometries: 6
protocols: 8
```

## Result

```text
clean rejections: 0
clean false-nonrejected: 0
adversarial false-nonrejected total: 0
adversarial rejected total: 1975
Q-only exception false-nonrejected: 0
symbol-membership-only false-nonrejected: 1027
```

## Criteria

| criterion                                    | passed   |
|:---------------------------------------------|:---------|
| stress_clean_event_ledger_exact_no_rejection | True     |
| stress_adversarial_zero_false_nonrejected    | True     |
| stress_qonly_exception_preserved             | True     |
| stress_full_variant_no_false_nonrejected     | True     |
| stress_symbol_membership_only_fails          | True     |

## Interpretation

The event-ledger stack has now transferred beyond one fresh domain into a harder independent trajectory-family stress domain.
