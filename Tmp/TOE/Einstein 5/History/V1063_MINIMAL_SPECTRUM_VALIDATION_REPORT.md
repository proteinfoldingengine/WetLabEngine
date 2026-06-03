# V1063 Minimal Spectrum Validation

**Status:** physics-only validation  
**Purpose:** Validate the V1062 minimal passing spectrum candidate.

## Candidate

```text
multiplicity_profile
```

## Result

```text
Multiplicity profile remained collision-free through N=35 in the integer-partition model; scalar sum+moment fails at N=6; full subset-sum remains collision-free through N=20.
```

## Summary

| spectrum                 |   tested_through_N |   first_failure_N |   injective_through_N |   collision_classes_at_maxN |
|:-------------------------|-------------------:|------------------:|----------------------:|----------------------------:|
| multiplicity_profile     |                 35 |               nan |                    35 |                           0 |
| scalar_sum_moment        |                 35 |                 6 |                     5 |                         329 |
| full_subset_sum_spectrum |                 20 |               nan |                    20 |                           0 |

## Interpretation

```text
Multiplicity profile is a compact complete encoding for integer-partition Ω classes in the tested range, but it is close to a canonical representation of Ω and should not be overclaimed as a non-tautological universal spectrum.
```

## Scientific Meaning

The reviewer’s correction forced a better distinction:

```text
scalar invariants are too compressed
full subset spectra are sufficient but may be overcomplete
multiplicity profile is smaller and collision-free in the integer-partition model
```

However, because Ω in the clean-room integer-partition model is essentially the partition structure itself, multiplicity profile may be close to a canonical representation of Ω.

So this does **not** prove universal minimality.

It identifies a bounded minimal spectrum candidate for this clean-room model.

## Updated Boundary

```text
Admissibility-complete spectra must be rich enough to distinguish Ω classes.
The minimal complete spectrum depends on the Ω map.
```

## Next Step

```text
V1064 — Non-Tautological Minimality Test
```

Test spectra smaller than multiplicity_profile but richer than scalar traces.
