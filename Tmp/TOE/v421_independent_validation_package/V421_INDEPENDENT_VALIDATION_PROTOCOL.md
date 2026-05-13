# V421 Independent Validation Protocol

## Purpose

V421 is not a discovery iteration. It is an independent validation package for the frozen V420 retained-atlas law candidate.

The goal is to test whether the V420 law generalizes to a new surrogate with different topology, noise, branching, recovery, fragmentation, and measurement-drift rules, without retuning the core law.

## Frozen V420 Law Candidate

The conserved adaptive object is trusted recursive recoverability:

```text
S_t = M_t × R_t × L_t
```

Where:

```text
M_t = adaptive safety margin
R_t = retained recovery capacity
L_t = retained lineage addressability
```

Survival requires:

```text
S_t > S_floor_conf(t)
M_t > M_floor_conf(t)
R_t > R_floor_conf(t)
L_t > L_floor_conf(t)
```

The confidence-adjusted floors are dynamically generated from internal observables and inflated by residual uncertainty.

## Frozen Guardrails

```text
If R confidence is low:
    preserve capacity; block aggressive repair.

If L confidence is low:
    block exit.

If estimates improve but realized outcomes do not confirm improvement:
    treat as drift;
    inflate floors globally;
    block product repair;
    block exit;
    enter preservation mode.
```

## What Must Not Be Changed

The following are frozen for validation:

1. The product structure `S = M × R × L`.
2. The use of factor floors and S floor.
3. Confidence inflation from residuals.
4. Cross-invariant drift guard.
5. Controller comparison set.
6. Pass/fail interpretation.

No coefficient retuning should be performed after seeing results.

## Independent Surrogate Requirements

The validation surrogate should differ from the V420 discovery surrogate in the following ways:

1. New topology generator.
2. New branching/fracture dynamics.
3. New noise process.
4. New recovery dynamics.
5. New missing-channel and measurement-drift cases.
6. New stress regimes.

The implementation in `v421_blind_validation.py` includes these changes.

## Controllers Compared

The validation compares:

1. `greedy_damage_minimizer`
2. `A_only`
3. `A_plus_L`
4. `S_constrained_dynamic_floors`
5. `S_residual_uncertainty`
6. `V420_full_guarded_law`

## Evaluation Metrics

Each controller is evaluated on:

```text
bad        = immediate/adaptive failure rate
harmed     = destructive intervention rate
reclosed   = delayed reclosure / false recovery rate
fidelity   = post-exit recovery fidelity
future_R   = retained future recovery capacity
attractor  = recovery-attractor entry rate
score      = peer-review composite score
```

The composite score intentionally does not reward bad-rate alone. Greedy controllers may reduce immediate bad outcomes while destroying future recoverability.

## Expected Validation Pattern

V420 does not need to have the lowest `bad` rate.

It should outperform alternatives on the law-shaped objective:

```text
low harm
low reclosure
high fidelity
high future_R
high attractor entry
```

## Pass Condition

V420 passes as a freeze candidate if:

```text
1. It is not dominated by another controller across harm, reclosure, fidelity, future_R, and attractor.
2. It strongly outperforms greedy damage minimization on destructive-recovery metrics.
3. It remains stable under noise, missing-channel, high-stress, and coordinated-drift regimes.
4. It does not require topology-specific retuning.
```

## Fail Condition

V420 fails or must branch if:

```text
1. A simpler controller matches or beats it across all recovery metrics.
2. Dynamic floors fail under unseen topology.
3. Residual uncertainty destabilizes the controller.
4. Cross-invariant drift guard does not reduce drift failures.
5. L_t adds no independent post-exit value in the new surrogate.
```

## Scientific Claim Boundary

This validation cannot prove the law universally. It can only test whether the V420 structure survives a new independent surrogate without retuning.

Supported claim if successful:

```text
V420 behaves like a robust retained-atlas adaptive-control law candidate across independent surrogate regimes.
```

Unsupported claim:

```text
This proves a universal law of all adaptive systems.
```
