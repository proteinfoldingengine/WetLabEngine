# Retained-Information State Theorem Note
## Theorem shape, support, and falsifier

## Theorem shape
There exist dynamical systems for which no predictor based only on instantaneous visible state \(G_t\) can match the predictive performance of a predictor based on \((G_t, R_t)\), where \(R_t\) is retained-information state.

Equivalently:
current visible state need not be state-complete.

## Sketch of support
1. Construct a bounded two-state system with visible state \(x_t\) and retained state \(r_t\).
2. Show that pairs with nearly identical \(x_t\) but different \(r_t\) can diverge in future behavior.
3. Show that predictors using \((x_t, r_t)\) outperform predictors using \(x_t\) alone.
4. Conclude that state completeness can fail when retained-information is omitted.

## What this establishes
- The retained-information-state problem is mathematically coherent.
- It is physically interpretable.
- It is simulation-testable.

## What this does not establish
- It does not prove that all natural systems require retained-information state.
- It does not prove the full UQCF-GEM TOE.
- It does not identify the final correct physical observable \(R_t\).

## UQCF-GEM implication
The bridge phase narrowed the TOE to this theorem-shaped problem.
The next real test is to see whether a retained-information state exists in real telemetry systems such as C3++.
