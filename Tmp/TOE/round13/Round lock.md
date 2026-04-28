# Round 13 Lock Statement
## The Scaling Relations Moonshot

Round 13 is now locked as the next major external Bridge challenge.

## Objective
Test whether the frozen baryonic-memory Bridge framework can reproduce the two most important low-scatter galactic scaling relations on a large locked public corpus:

- **BTFR** — Baryonic Tully-Fisher Relation
- **RAR** — Radial Acceleration Relation

This round is not limited to per-galaxy rotation-curve improvement. It explicitly asks whether the same framework recovers the global population laws.

## Scope
Round 13 is restricted to **galactic-scale kinematics** and associated baryonic scaling relations.

It does **not** include:
- cluster dynamics,
- gravitational lensing,
- cosmology,
- or non-galactic observables.

## Core principle
No per-galaxy parameter tuning is allowed once the corpus and scoring protocol are locked.

## Data policy
Round 13 uses a **locked public corpus**.

The corpus must be:
- public,
- reproducible,
- documented,
- and frozen before execution.

Acceptable sources may include a unified public rotation-curve corpus assembled from public surveys, provided the final inclusion list is explicitly published.

## Inclusion rules
Each included galaxy must satisfy the locked minimum data requirements needed to compute:
- a rotation curve,
- a baryonic mass estimate,
- a flat-velocity estimate,
- radial observed acceleration,
- radial baryonic acceleration.

If a galaxy cannot support those quantities under the published rules, it is excluded before execution.

## Required locked definitions

### 1. Flat velocity definition
A single explicit rule must be frozen for estimating `V_flat`.

Example acceptable approaches:
- median velocity over a pre-defined outer stable radial window,
- asymptotic fit under a frozen formula,
- or final stable-bin average under a frozen quality rule.

The definition must be identical for all galaxies.

### 2. Baryonic mass definition
A single explicit rule must be frozen for computing total baryonic mass `M_baryon`.

This must specify:
- gas mass handling,
- stellar mass handling,
- stellar mass-to-light assumptions or source values,
- bulge treatment where applicable,
- and missing-data policy.

### 3. Observed acceleration definition
A single explicit rule must be frozen for:
\[
g_{\mathrm{obs}}(r) = \frac{V_{\mathrm{obs}}^2(r)}{r}
\]

### 4. Baryonic acceleration definition
A single explicit rule must be frozen for:
\[
g_{\mathrm{bar}}(r) = \frac{V_{\mathrm{bar}}^2(r)}{r}
\]

where `V_bar` must be constructed from the locked baryonic input policy.

## Scoring outputs

### Per-galaxy outputs
For each galaxy, the pipeline must emit:
- galaxy identifier
- number of usable radial points
- baryonic baseline RMSE
- Bridge RMSE
- improvement
- `V_flat`
- `M_baryon`
- BTFR coordinates
- radial `g_obs`
- radial `g_bar`
- any locked diagnostic flags

### Aggregate outputs
The pipeline must emit:
- positive improvement rate
- mean RMSE improvement
- BTFR fitted slope
- BTFR scatter
- RAR scatter
- catastrophic outlier count

## Win condition
Round 13 is counted as won only if all of the following hold on the locked corpus:

1. aggregate rotation-curve performance remains positive
2. BTFR slope falls in the expected observational band under the locked measurement rule
3. BTFR scatter is low and competitive relative to the baryonic baseline
4. RAR shows the expected transition structure with low scatter
5. catastrophic outliers remain limited under the locked failure rule

## Catastrophic outlier rule
A catastrophic outlier rule must be frozen before execution.

Example:
- a galaxy with Bridge degradation worse than a locked threshold
- or a galaxy whose BTFR / RAR residual exceeds a locked multiple of the corpus scatter

## Falsification policy
Round 13 fails if:
- the pipeline requires per-galaxy retuning,
- the corpus changes after lock,
- the measurement definitions change after execution begins,
- or the model fails the locked aggregate criteria.

## Closeout principle
Round 13 is intended to test whether the Bridge framework reproduces **population-level laws**, not merely selected curve improvements.

That is why this round matters.
