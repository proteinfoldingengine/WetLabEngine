# V1213 — Post Anti-Tautology Verdict Upgrade

## Status

Completed.

## Prior Verdict

```text
WEAK PASS
```

## Updated Verdict

```text
PASS for the narrow B-like/source-flow bridge inside tested simulations
```

## Why the Verdict Upgraded

V1211 identified the main concern:

```text
closure_imbalance is part of U_info
B_like_residual is measured downstream
therefore tautology risk remains
```

V1212 directly tested this concern.

The result:

```text
linear closure pressure improved all five held-out closure metrics
```

These held-out metrics were not the exact training closure used inside U_info:

```text
1. nonlinear closure
2. spectral closure
3. derivative closure
4. lagged closure
5. mutual-proxy closure
```

V1212 also improved:

```text
valid retained weight
valid winner rate
source-flow alignment
flow coherence
```

## Key V1212 Result

```json
{
  "heldout_improved_count": 5,
  "heldout_metric_improved": {
    "delta_heldout_nonlinear_closure": true,
    "delta_heldout_spectral_closure": true,
    "delta_heldout_derivative_closure": true,
    "delta_heldout_lagged_closure": true,
    "delta_heldout_mutual_proxy_closure": true
  }
}
```

## Upgraded Claim

```text
Within the tested synthetic information-to-geometry simulations, path-certified admissibility with closure pressure robustly produces source-flow-consistent retained histories, improving B-like closure across multiple held-out closure definitions and stabilizing ordered-slice source-flow propagation.
```

## Remaining Boundaries

- Does not establish full ADM-like H/M constraint recovery.
- Does not establish physical GR or Einstein equations.
- Does not yet prove universality beyond tested simulation families.
- Still needs external clean-room replication.


## Interpretation

This is now stronger than the V1211 weak pass.

The B-like/source-flow result is not merely the exact training metric being optimized.

The closure pressure generalized across independent held-out closure definitions.

That supports the narrow bridge:

```text
admissibility
→ closure pressure
→ source-flow consistency
→ B-like closure propagation
```

The ADM-like H/M branch remains unresolved and should stay outside the claim.

## Next

V1214 should produce the final supported-bridge report and replication instructions.
