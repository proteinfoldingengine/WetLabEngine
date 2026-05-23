# V925 Source-Role Closure Hardening

## Verdict

`source_role_closure_hardened_and_closed_for_current_branch`

Closed for current branch: **True**

This audit hardens V923/V924 and stops the loop for this branch unless a new out-of-domain cohort is introduced.

## Closure object

```text
C = (Q_obs, S_ternary)
```

where `Q_obs` is the observable quotient / geometry-like basin layer and:

```text
S_ternary ∈ {
  source_active_role,
  source_basin_eligible_nonactive_role,
  source_rejected_or_broken_role
}
```

## Final lift ladder

| lift                          |   symbols |   accuracy |   false_cases |   collision_rows_train |
|:------------------------------|----------:|-----------:|--------------:|-----------------------:|
| observable_quotient_only      |         1 |   0.628571 |           312 |                    662 |
| best_binary_source_lift       |         2 |   0.916667 |            70 |                    306 |
| ternary_source_role_primitive |         3 |   1        |             0 |                      0 |
| full_four_family_source       |         4 |   1        |             0 |                      0 |

Minimal exact source-symbol count: **3**

## Closure criteria

| criterion                   | passed   |
|:----------------------------|:---------|
| observable_only_fails       | True     |
| binary_lifts_fail           | True     |
| ternary_exact               | True     |
| four_overcomplete           | True     |
| targeted_corruption_breaks  | True     |
| random_noise_degrades       | True     |
| single_error_code_protects  | True     |
| compact_code_not_protective | True     |

## Perturbation stress

Worst targeted role flip:

```text
source_basin_eligible_nonactive_role → source_rejected_or_broken_role
affected rows: 360
accuracy: 0.571429
false cases: 360
```

Random role corruption degrades accuracy monotonically: **True**

## Minimal ECC protection

Minimal single-error-correcting binary encoding for the ternary role:

```json
{
  "source_active_role": "00000",
  "source_basin_eligible_nonactive_role": "00111",
  "source_rejected_or_broken_role": "11001"
}
```

The compact 2-bit code does not protect against single-bit corruption. The minimal distance-3 redundant code does.

## Domain boundary

Leave-one-observable-quotient-out testing creates unseen discrete quotient keys. That is a domain-of-definition boundary, not an in-domain closure failure. V925 therefore does **not** claim parametric generalization to unseen quotient families.

## Final scientific statement

```text
E_OSC / Q_obs gives admissible form.
S_ternary gives minimal source legitimacy.
C = (Q_obs, S_ternary) is exact and minimal for in-domain closure.
```

## Claim boundary

No physical spacetime, GR, Einstein equations, continuum limit, CMB, black-hole, or 1/f ledger claim. The ternary source-role is a discrete information primitive, not a physical dimension.
