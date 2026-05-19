# V737 Atrium Metric Reproducibility Bundle

## Purpose

This bundle freezes and reproduces the strongest certified result from the V725–V736 branch:

> In passive-equivalent perturbation-response assays, passive burden remains chance while observable active response-geometry separates hidden restorative capacity.

## Certified object

Atrium Metric v1.0:

```text
observable run-level response-geometry scalar
```

## Minimal law

```text
passive burden = chance
active response geometry = signal
```

## What this bundle is

A reproducibility harness for:

1. passive-equivalent paired perturbation-response assays,
2. observable-only Atrium scalar extraction,
3. no direct-k leakage controls,
4. k-gap collapse,
5. perturbation-family holdout testing,
6. clean claim boundaries.

## What this bundle is not

It does not claim:

- GR recovery,
- Einstein equations,
- spacetime curvature,
- tensor metric,
- coordinate covariance,
- real-world validation.

## Run

```bash
python v737_reproduce_atrium_metric.py
```

Expected high-level pattern:

```text
Atrium scalar AUC: high
passive burden AUC: ~0.5
k_gap = 0 AUC: ~0.5
```
