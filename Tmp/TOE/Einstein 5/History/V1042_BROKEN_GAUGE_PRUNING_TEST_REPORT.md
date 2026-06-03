# V1042 Broken Gauge Pruning Test

**Status:** physics-only iteration  
**Purpose:** Test when pruning-order equivalence breaks.

## Background

V1041 found that content-preserving pruning orders formed one Ω-equivalence class.

V1042 introduces non-admissible transformations:

```text
delete content
duplicate content
sort/scramble content
collapse symbols
overwrite retained positions
```

## Results

```text
Transforms tested: 10
Gauge-preserving transforms: 2
Broken transforms: 8
Min Jaccard vs identity: 0.020986
Max visible-fraction shift: 0.360560
```

## Interpretation

```text
Content-preserving pruning orders preserve the Ω gauge class, while non-admissible pruning operations break Ω equivalence by deleting, duplicating, or distorting retained content.
```

## Physics Meaning

This gives the model a clean distinction:

```text
admissible pruning transformations
    preserve recoverability geometry

non-admissible pruning transformations
    break recoverability geometry
```

So the gauge-like class is not trivial. It is bounded by retained-content preservation.

## Time-as-Pruning Meaning

If τ is pruning order, then:

```text
different τ paths can be equivalent
only when they preserve retained recoverability content.
```

When pruning destroys or duplicates retained origin structure, the emergent Ω geometry changes.

## Claim Boundary

This does not assume spacetime or physical time.

It tests recoverability-order invariance in the finite it-from-bit model.

## Next Physics Step

```text
V1043 — Admissibility Law Candidate
```

Formalize the rule:

```text
Pruning transformations are gauge-equivalent iff they preserve retained content
up to Ω-invariant recoverability structure.
```
