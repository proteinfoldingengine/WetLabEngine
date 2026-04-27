# Scoring Protocol — Round 12

## Goal
Compare the frozen Bridge prediction against the pure-baryonic baseline on a pre-registered unseen public galaxy subset.

## Per-galaxy scoring

### Baryonic baseline
For each radius:
\[
V_{\mathrm{bar}}(r_i) = \sqrt{\max(\mathrm{sign}(V_{\mathrm{gas}})V_{\mathrm{gas}}^2 + V_{\mathrm{disk}}^2 + V_{\mathrm{bul}}^2, 0)}
\]

### Bridge prediction
Use the frozen operator in `frozen_runner.py` to compute \(V_{\mathrm{bridge}}(r_i)\).

### Error metric
For each galaxy:
\[
\mathrm{RMSE}_{\mathrm{baryonic}} = \sqrt{\frac{1}{N}\sum_i (V_{\mathrm{obs},i}-V_{\mathrm{bar},i})^2}
\]

\[
\mathrm{RMSE}_{\mathrm{bridge}} = \sqrt{\frac{1}{N}\sum_i (V_{\mathrm{obs},i}-V_{\mathrm{bridge},i})^2}
\]

\[
\mathrm{Improvement} = \mathrm{RMSE}_{\mathrm{baryonic}} - \mathrm{RMSE}_{\mathrm{bridge}}
\]

A galaxy is a positive win if:
\[
\mathrm{Improvement} > 0
\]

## Aggregate scoring
Across all galaxies:
- positive improvement rate = fraction with improvement > 0
- mean RMSE improvement = arithmetic mean of per-galaxy improvements
- catastrophic failure count = number of galaxies whose improvement is worse than a predefined threshold

## Catastrophic failure
Default definition:
- a galaxy counts as catastrophic if improvement < -10 km/s

If a different threshold is chosen, it must be frozen before execution.

## Missing data policy
- Score only rows with finite `Rad`, `Vobs`, `Vgas`, `Vdisk`, `Vbul`
- No hidden row deletion
- No per-galaxy radius cropping unless explicitly pre-registered

## Reporting
Results must include:
- full per-galaxy table
- aggregate metrics
- exact galaxy list used
- exact code version / commit hash
