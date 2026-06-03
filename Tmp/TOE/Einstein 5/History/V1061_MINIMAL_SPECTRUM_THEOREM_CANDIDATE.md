# V1061 Minimal Spectrum Theorem Candidate

**Status:** physics-only theorem refinement  
**Purpose:** Convert the reviewer correction into a cleaner theorem candidate.

## Definition: Admissibility-Complete Spectrum

```text
A recoverability spectrum Π is admissibility-complete for Ω
iff Π is injective over Ω classes.
```

Formal condition:

```text
Π(E1) = Π(E2)  ⇒  Ω(E1) = Ω(E2)
```

## Theorem Candidate

```text
Ω-gauge admissibility can be certified by preserving any
admissibility-complete recoverability spectrum Π.
```

## Why This Replaces the Earlier Law

The earlier two-invariant law was too specific:

```text
Π_sum + Π_moment
```

The reviewer showed scalar versions fail at scale.

The mature law is:

```text
preserve enough recoverability spectrum to be injective over Ω classes.
```

## Injectivity Summary

| spectrum                 |   tested_through_N |   first_failure_N |   injective_through_N |
|:-------------------------|-------------------:|------------------:|----------------------:|
| scalar_sum               |                 30 |                 2 |                     1 |
| scalar_sum_moment        |                 30 |                 6 |                     5 |
| full_subset_sum_spectrum |                 20 |               nan |                    20 |

## Core Result

```text
In the integer-partition clean-room model, scalar traces are not admissibility-complete, while the full subset-sum spectrum is collision-free through the tested range.
```

## Physics Meaning

The key quantity is spectral completeness.

```text
Low-dimensional scalar traces compress away too much recoverability information.
A sufficiently rich spectrum prevents counterfeit Ω geometry.
```

This strengthens the time-as-pruning model:

```text
admissible pruning preserves the recoverability spectrum needed to keep Ω invariant.
```

## Claim Boundary

This is not yet a universal theorem over all spectra and all Ω maps.

It is a clean theorem candidate plus finite evidence.

## Next Step

```text
V1062 — Spectrum Minimality Search
```

Search for spectra smaller than full subset-sum but richer than scalar traces that remain injective over Ω classes.
