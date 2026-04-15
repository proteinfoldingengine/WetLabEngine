# Retained-Core with Conditional Context Hypothesis

## Working memo v3 — activation frontier strengthened by state-sufficiency failure landscape

## Abstract

Repeated pressure tests support a reliability-layer model in which stable realization is not fully determined by visible state alone.

The best surviving empirical architecture is:

`Lambda_t = sigma(U_t + C_t)`

with universal retained core:

`U_t = z(|d_t|) - 1.5 z(rho_t)`

The main open problem remains context activation. The strongest current candidate principle is now clearer: context should activate when present-state description ceases to be a sufficient statistic for future reliability.

## What is now established

- Visible-state-only descriptions were often incomplete.

- A universal retained core repeatedly improved transition-reliability separation.

- Direct retained-state forcing failed.

- Simple regimes were well described by the retained core alone.

- Metastable, folding-like, and excitable regimes required added context.

## Best current model

Proposed transition:

`G~_(t+1) = F(G_t, R_t)`

Universal retained core:

`U_t = z(|d_t|) - 1.5 z(rho_t)`

Reliability field:

`Lambda_t = sigma(U_t + C_t)`

Interpretation:

`P(stable realization of G~_(t+1) | G_t, R_t, C_t) = Lambda_t`

## Context split that survived testing

Regime A-like dynamics: C_t ≈ 0

Regime B/C-like dynamics: C_t must encode branch stability opposed by switching, oscillation, and over-commitment penalties

Pulse/excitable regime: core-only already works somewhat, but modest context improves separation

## Activation frontier strengthened

The strongest current activation candidate is state-sufficiency failure:

`delta_t = | P(success | state+retained) - P(success | state) |`

Interpretation:

Low delta_t means visible state is mostly enough.

High delta_t means visible state is not enough, so retained/path structure is adding real predictive information.

## State-sufficiency failure landscape result

Mean delta by regime from the latest landscape test:

Regime A: 0.0516

Regime B: 0.2276

Regime C: 0.2279

Regime D: 0.2107

Share above the global 75th-percentile threshold:

Regime A: 0.0805

Regime B: 0.4599

Regime C: 0.4579

Regime D: 0.4200

This is the clearest evidence so far that the regimes which needed context are also the regimes where state-only sufficiency fails most strongly.

## What failed

- Memory as direct force.

- Hard accept/reject transition rules.

- One universal context-free scalar.

- Current derived activation attempts from local heuristics alone.

- Current derived activation attempts from local matched-state divergence or crude state-insufficiency estimators.

## Open problem now isolated

The main unresolved issue is not the retained core. It is the activation law for context.

Best conceptual statement:

`Context should activate when present-state description ceases to be a sufficient statistic for future reliability.`

Current practical activation estimators still underperform the stronger hand-specified context architecture, but the regime-level state-sufficiency landscape now supports the principle itself.

## Best current research question

Under what first-principles condition does the system require context at all?

Equivalently: when does

`P(success | state) ≠ P(success | state, retained/path structure)`

in a way large enough to require C_t?

## Clean next-step conclusion

The theory program should now treat the universal retained core as the current survivor, treat state-sufficiency failure as the strongest activation principle so far, and treat the exact activation estimator as the major open derivation target.
