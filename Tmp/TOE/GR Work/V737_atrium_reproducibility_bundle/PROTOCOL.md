# V737 Protocol

## Assay design

Each pair shares:

```text
same target field
same passive baseline
same perturbation mask / amplitude
same stochastic seed
same observation window
```

Only restorative capacity differs.

## Forbidden leakage

The certified metric must not include:

```text
direct k
label
oracle capacity
post-hoc class threshold
```

## Certified scalar class

```text
A =
    restoration residual
  + contraction failure
  + trajectory deviation
  + curvature-like residual
  + observation-window boundary
  + metric strain
```

## Pass criteria

1. Passive mean AUC near 0.5.
2. Passive curvature AUC near 0.5.
3. Observable Atrium scalar AUC materially above chance.
4. Signal weakens as k_gap shrinks.
5. k_gap = 0 collapses near chance.
6. Perturbation-family holdouts retain signal directionally.

## Claim boundary

Allowed:

```text
An operational response-geometry scalar tracks hidden restorative capacity under passive-equivalent synthetic assays.
```

Not allowed:

```text
This derives GR.
This is a metric tensor.
This proves a physical law in the real world.
```
