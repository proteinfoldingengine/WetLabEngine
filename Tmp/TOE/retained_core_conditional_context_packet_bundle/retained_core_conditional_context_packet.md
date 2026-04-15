# Retained-Core with Conditional Context Hypothesis

## Pressure-Tested Working Model for Transition Reliability

## Abstract

These experiments support a reliability-layer view of dynamics in which stable realization is not fully determined by visible state alone. The best-performing working model is a bounded reliability field:

Lambda_t = sigma(U_t + C_t)

where U_t is a universal retained core and C_t is a conditional context field that becomes important in path-dependent regimes. A working empirical form for the universal core is:

U_t = z(|d_t|) - 1.5 z(rho_t)

Across the tested regimes, U_t was sufficient in simpler dynamics, while branch-stability or excitable-memory context was required in metastable, folding-like, or pulse-like regimes.

## Core Claim

Transition reliability is governed by a universal retained core, with additional context fields required only in regimes where path dependence, metastability, branch instability, or excitable memory materially affect which futures are stably reachable.

## Model

Proposed transition:

G~_(t+1) = F(G_t, R_t)

Universal retained core:

U_t = z(|d_t|) - 1.5 z(rho_t)

Reliability field:

Lambda_t = sigma(U_t + C_t)

Interpretation:

P(stable realization of G~_(t+1) | G_t, R_t, C_t) = Lambda_t

## Interpretation of Terms

d_t behaves like retained directional structure strength. Its sign is not universal, but its magnitude repeatedly carried reliability signal.

rho_t behaves like retained destabilization burden. Stronger rho_t generally reduced reliability, and its weight repeatedly settled above 1, with 1.5 the best tested working value.

C_t is not arbitrary context. It is the extra information needed when the same apparent present state can still belong to different future-stability classes.

## Regime Summary

Regime A-like: best described by Lambda_t ≈ sigma(U_t). Context was unnecessary and often harmful.

Regime B/C-like: best described by Lambda_t ≈ sigma(U_t + B_t - P_t), where B_t is branch stability and P_t is switching, oscillation, or over-commitment penalty.

Folding-path regime: after calibrating the success criterion, the richer branch context restored a strong monotone reliability ordering, while core-only was weak.

Out-of-family pulse regime: core-only already worked somewhat, but a light pulse/refractory context improved separation further.

## What Was Falsified

- Direct retained-state forcing.
- Sign-aware forcing laws.
- Hard accept/reject transition laws.
- One universal scalar without context.
- Current attempts to derive a universal activation law from local features or nearest-neighbor divergence.
## What Survived

- Visible-state-only descriptions are incomplete in the tested systems.
- Retained-state variables improve transition-reliability separation.
- Retained state belongs more naturally in a reliability/readiness layer than in a force law.
- The universal retained core transfers across multiple regimes.
- Context is conditional and becomes necessary in branch-structured or excitable regimes.
## Best Current Formal Hypothesis

For a class of dynamical systems, transition reliability is better represented by a bounded retained reliability field Lambda_t = sigma(U_t + C_t), where U_t is a universal retained core derived from retained directional structure and retained destabilization, and C_t is a context field required only in regimes with meaningful path dependence or instability memory.

## Open Problem

We do not yet have a successful derived law for when C_t should activate strongly enough to replace hand-switched regime context.

## Compact One-Line Conclusion

Transition reliability appears to be governed by a universal retained core, with additional context fields activated only when the regime has meaningful path dependence, branch instability, metastability, or excitable memory.

