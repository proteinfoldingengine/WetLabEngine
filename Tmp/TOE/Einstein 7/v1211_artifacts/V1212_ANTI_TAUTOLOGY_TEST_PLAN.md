# V1212 Plan — Alternative Closure Metric / Anti-Tautology Test

## Goal

Test whether the supported B-like/source-flow branch is real or merely circular.

## Concern

U_info includes closure_imbalance.

Downstream result measures B_like_residual.

This creates tautology risk.

## Test

Use one closure term for pruning:

```text
training closure = linear source-flow reconstruction residual
```

Then evaluate with different held-out closure metrics:

```text
1. nonlinear source-flow closure
2. spectral source-flow closure
3. derivative closure
4. lagged source-flow closure
5. mutual-information-like closure proxy
```

## Pass condition

Closure-driven pruning improves held-out closure metrics, not just the metric used inside U_info.

## Strong pass

```text
valid retained weight improves
training closure improves
held-out closure metrics improve
source-flow alignment improves
ADM-like claims remain bounded
```

## Fail

Only the exact training closure improves.
