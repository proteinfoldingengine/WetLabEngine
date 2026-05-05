# ORDER_ONLY_METRIC_RECONSTRUCTION_VERIFIER_SUMMARY.md

# Verifier Summary
## Order-only distance and dimension proxies

## Status
**Executed structural verifier. Not a full metric reconstruction.**

Verifier file:

```text
order_only_metric_reconstruction_verifier.py
```

Execution log:

```text
order_only_metric_reconstruction_verifier_run.log
```

## Captured output

```text
Order-only metric reconstruction verifier
==================================================
Reconstruction uses only causal relation:
longest-chain distance, interval cardinality, order-distance proxy
Coordinates are used only for hidden evaluation correlation.

PASS: 88.75
SOFT_FAIL: 1.25
HARD_FAIL: 10.0
dim_estimate_median: 3.2651871821498584
order_distance_tau_corr_median: 0.9537979483187051
chain_tau_corr_median: 0.880014698938312
comparable_pairs_median: 11765.5
```

## Interpretation

The verifier reconstructs longest-chain distance, interval cardinality, an order-only dimension proxy, and an order-distance proxy using only the causal relation.

Hidden coordinates are used only to evaluate correlation with proper-time-like separation.

This supports the order-only metric seam structurally, but does not prove:
- local metric reconstruction,
- manifoldlikeness,
- curved spacetime behavior,
- or coordinate/gauge independence.

**End of summary.**
