# V923 Full-Stack Geometry–Information Bridge Visualization

## Verdict

`v923_full_stack_visualization_recomputed_from_v921_data`

Certified: **True**

Rows: **840**  
Input: `/mnt/data/v921_ternary_source_role_primitive_blind_regeneration_audit/v921_ternary_endpoint_scores.csv`  
Observable quotient column: `v921_observable_quotient`

## Lift ladder

| lift                          |   symbol_count |   accuracy |   false_cases |   collision_rows |
|:------------------------------|---------------:|-----------:|--------------:|-----------------:|
| observable_quotient_only      |              1 |   0.628571 |           312 |              662 |
| best_binary_source_role_lift  |              2 |   0.916667 |            70 |              306 |
| ternary_source_role_primitive |              3 |   1        |             0 |                0 |
| full_four_family_source_lift  |              4 |   1        |             0 |                0 |

## Minimal exact lift

The first exact closure appears at:

```text
3 source-role symbols
```

The certified ternary primitive is:

```text
active_source             -> source_active_role
passive_source            -> source_basin_eligible_nonactive_role
structured_source         -> source_basin_eligible_nonactive_role
rejected_or_broken_source -> source_rejected_or_broken_role
```

## What the visualization means

The left panel visualizes the observable quotient / basin view. It is allowed to be source-degenerate.

The right panel adds a discrete information lift. The Z-axis is **not physical space or time**. It is a discrete source-role index:

```text
Z=0 rejected/broken
Z=1 basin-eligible nonactive
Z=2 active
```

## Claim boundary

YES:
- The figure is derived from the actual V921 blind endpoint cohort.
- The lift ladder is recomputed in this script.
- Observable-only and binary closure fail.
- Ternary source-role closure succeeds in this branch.

NO:
- No 1/f ledger claim.
- No CMB / black-hole claim.
- No physical-time claim.
- No GR / Einstein equation / spacetime curvature / continuum-closure claim.
