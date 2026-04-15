# Retained-Core with Conditional Context Hypothesis

## Working memo v2 — architecture locked, activation problem isolated

## Abstract

Repeated pressure tests support a reliability-layer model in which stable realization is not fully determined by visible state alone.

The best surviving empirical architecture is:

`Lambda_t = sigma(U_t + C_t)`

with universal retained core:

`U_t = z(|d_t|) - 1.5 z(rho_t)`

The major open problem is now sharply isolated: deriving when context should activate, rather than hand-specifying it by regime.

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

## What failed

- Memory as direct force.

- Hard accept/reject transition rules.

- One universal context-free scalar.

- Current derived activation attempts from local heuristics alone.

- Current derived activation attempts from local matched-state divergence or state-insufficiency estimators.

## Open problem now isolated

The main unresolved issue is not the retained core. It is the activation law for context.

Best conceptual statement:

`Context should activate when present-state description ceases to be a sufficient statistic for future reliability.`

Current practical estimators for that activation remain weaker than the stronger hand-specified context architecture.

## Best current research question

Under what first-principles condition does the system require context at all?

Equivalently: when does

`P(success | state) ≠ P(success | state, retained/path structure)`

in a way large enough to require C_t?

## Clean next-step conclusion

The theory program should now treat the universal retained core as the current survivor and the context-activation law as the major open derivation target.
