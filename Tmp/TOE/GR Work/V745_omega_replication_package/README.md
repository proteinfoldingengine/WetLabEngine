# V745 Ω Candidate Replication Package

## Purpose

This package reproduces the Ω branch after the V744 freeze.

Core result:

> In a synthetic recoverability system, observable response geometry produces a bounded Ω-like conformal response factor whose dynamics are directionally predictable after coarse-graining.

## What this is

A simulation / instrumentation package for:

1. bounded Ω candidate extraction,
2. Ω dynamic consistency,
3. coarse-grained Ω evolution-law candidate,
4. held-out validation of the frozen coarse-grained law,
5. strict claim boundaries.

## What this is not

This is not:

- physical GR,
- Einstein equations,
- actual spacetime curvature,
- a coordinate-covariant metric tensor,
- real-world validation.

## Run order

```bash
python v745_replicate_omega_branch.py
```

This will produce:

```text
outputs/v745_omega_replication_results.json
outputs/v745_omega_run_metrics.csv
```

## Expected pattern

```text
bounded Ω separates capacity
passive controls remain near chance
null k_gap collapses near chance
coarse-grained Ω law has directional held-out predictive structure
```
