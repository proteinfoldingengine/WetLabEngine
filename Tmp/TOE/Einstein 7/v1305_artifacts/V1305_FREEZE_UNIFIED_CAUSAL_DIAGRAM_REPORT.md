# V1305 — Freeze Unified Causal Diagram

## Status

Completed.

## Basis

V1304 — Bridge Unification Test.

## Frozen Diagram

```text
retained path identity
        ↓
 ┌──────────────────────┐
 │                      │
B-like/source-flow      ADM_M-like
closure propagation     momentum/transport propagation
```

## Core Result

V1304 found that:

```text
identity_only
=
identity_plus_closure
=
identity_plus_momentum
=
identity_closure_momentum
```

All of those regimes produced essentially the same strong result:

```text
valid_winner_rate ≈ 1.000
valid_weight      ≈ 1.000
ADM_M residual    ≈ 0.00036
flow_coherence    ≈ 1.000
B-like residual   ≈ 0.0212
```

By contrast:

```text
closure_only
```

was much weaker:

```text
valid_weight   ≈ 0.288
ADM_M residual ≈ 0.822
flow_coherence ≈ 0.660
```

## Interpretation

Closure alone can preserve some B-like/source-flow structure, but it does not recover momentum strongly.

Momentum can recover transport strongly once the normalized primitive is correct.

But the strongest result is that **retained path identity alone** recovers both:

```text
B-like closure
ADM_M-like propagation
```

So the best current causal diagram is:

```text
retained path identity
→ B-like closure
→ source-flow propagation

retained path identity
→ ADM_M-like transport
→ momentum propagation
```

## Claim-Hardened Statement

```text
Inside the tested synthetic transport simulations, retained path identity is the strongest common ancestor:
it recovers both B-like closure and ADM_M-like propagation, while closure alone does not recover momentum.
```

## What This Does Not Claim

This does not claim:

```text
physical GR
Einstein equations
full ADM derivation
physical spacetime curvature
universal law beyond tested simulations
```

## Why This Matters

This reorders the stack.

Previously:

```text
closure looked like the highest supported branch
```

Now:

```text
identity appears upstream of closure and momentum
```

That is a more valuable result.

It suggests the bridge may not be:

```text
closure → momentum
```

or:

```text
momentum → closure
```

but rather:

```text
retained path identity → both
```

## Next

V1306 should adversarially test this.

The key challenge is:

```text
Can an identity-matched counterfeit pass identity while breaking closure or momentum?
```

If yes, identity is not sufficient.

If no, retained path identity becomes the strongest unifying primitive found so far.
