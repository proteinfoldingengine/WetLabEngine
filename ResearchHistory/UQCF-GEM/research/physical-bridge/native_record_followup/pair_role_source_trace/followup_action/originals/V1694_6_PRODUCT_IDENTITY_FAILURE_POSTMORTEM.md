# V1694.6 — Product Identity Failure Postmortem and Identity-Form Decision

**Verdict:** `D_EQUALS_RHO_PLUS_Q_PRODUCT_IDENTITY_DISCARDED_FOR_NOW`

## Bottom line

V1694.5 tested the cleanest version of the product identity so far:

```text
D_ΓR_Γ^⊕ = ρ_support^⊕ + Q_A^⊕
```

with disjoint support/current and boundary terms.

It failed decisively.

## V1694.5 core numbers

```json
{
  "graph_cases": 9,
  "comparison_cases": 21,
  "stationarity_pass_rate": 1.0,
  "positive_action_reduction_rate": 1.0,
  "boundary_support_disjointness_rate": 1.0,
  "support_current_disjointness_rate": 1.0,
  "product_identity_pass_rate": 0.0,
  "mean_E_norm": 0.0010218964448680593,
  "mean_valid_null_min_norm": 7.11642399870178e-05,
  "valid_advantage_mean": -0.0009507322048810414,
  "mean_Q_rho_overlap_cosine": 0.9808410798185537,
  "Q_contains_support_rate": 0.0,
  "rho_contains_boundary_rate": 0.0
}
```

## What this means

The failure is no longer explained by:

```text
bad stationarity
event-label current
Q/ρ contamination
missing support-boundary decomposition
```

Those were addressed.

The identity still failed.

## Key diagnosis

Even when built from disjoint sources:

```text
Q_A
ρ_support
```

project into nearly the same product-dual direction.

```text
mean_Q_rho_overlap_cosine ≈ 0.9808
```

That makes the additive identity ill-conditioned and likely overcorrected.

## Scientific decision

Discard this as the active product identity:

```text
D_ΓR_Γ^⊕ = ρ^⊕ + Q^⊕
```

Keep:

```text
Φ_⊕
D1/D2 structure
retained pair tests
support-boundary audit
```

But search for a different invariant.

## Next branch

```text
V1695 — Product Curvature Invariant Search
```

Candidate directions:

```text
source-free residual structure
D/Q angle or alignment invariant
orthogonal component after support-boundary projection
pairwise covariance/rank signature of Φ_⊕
scale-stable ratio invariant
```

## Safe claim

The product probe has meaningful bilinear retained-pair structure, but the additive source-balanced identity `D=rho+Q` failed and should be discarded for now.
