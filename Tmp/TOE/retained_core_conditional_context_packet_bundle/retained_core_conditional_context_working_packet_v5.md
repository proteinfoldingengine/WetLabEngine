# Retained-Core with Conditional Context Hypothesis

## Working memo v5 — hybrid observables locked, dual activation derived

## Abstract

Repeated pressure tests now support a hybrid reliability architecture rather than a single activation law.

The best current model is:

`Lambda_t = sigma(U_t + chi_class,t * C_class,t + chi_band,t * C_band,t)`

with universal retained core:

`U_t = z(|d_t|) - 1.5 z(rho_t)`

The context correction now has hybrid geometry: B/C-like regimes are best described by class-structured context, while D-like regimes are best described by a continuous transition-band correction.

## What is now locked

- Visible-state-only descriptions were often incomplete.

- A universal retained core repeatedly improved transition-reliability separation.

- Simple A-like regimes were best described by the core alone.

- B/C-like regimes required class-structured context.

- D-like regimes were better described as a transition band than a hard class.

## Locked hybrid reliability model

`Lambda_t = sigma(U_t + chi_class,t * C_class,t + chi_band,t * C_band,t)`

`U_t = z(|d_t|) - 1.5 z(rho_t)`

`P(stable realization of G~_(t+1) | G_t, R_t) = Lambda_t`

## Locked observables

Transition-band depth:

`Z_band,t = u1 * EMA(Delta_t)~ + u2 * Var_local(Delta_t)~ + u3 * G_rel,t~`

`where Delta_t = | P(success | G_t, R_t) - P(success | G_t) |`

Class-separatrix distance:

`D_class,t = 1 - H_class,t~`

where H_class,t is local future path-class entropy from a 3-state future label {-1, 0, +1}.

Best current future path-class label parameters:

`horizon = 18, eps_boundary = 0.12, theta_mu = 0.10, theta_persist = 0.70, theta_boundary = 0.34`

## Empirical lock on the hybrid geometry

- A-like states remained unresolved and core-sufficient.

- B/C-like states showed genuine partial future branch commitment under the improved 3-state label.

- D-like states remained unresolved and band-dominated.

- The transition-band observable remained the strongest overall signal.

- The improved class-separatrix observable became directionally correct and usable.

## Derived class activation

`chi_class,t = sigma(alpha_c * (1 - D_class,t) - theta_c)`

Interpretation:

Class activation rises when the system approaches a branch separatrix, meaning local future path-class entropy is high and class distance is small.

## Derived band activation

`chi_band,t = sigma(alpha_b * Z_band,t - theta_b)`

Interpretation:

Band activation rises when persistent state-sufficiency failure, local insufficiency heterogeneity, and local reliability slope indicate entry into a transition band.

## Derived hybrid correction logic

A-like regimes: chi_class,t ≈ 0 and chi_band,t ≈ 0

B/C-like regimes: chi_class,t > 0 and chi_band,t relatively weak

D-like regimes: chi_band,t > 0 while chi_class,t stays weak or ambiguous

This is why a single activation law failed: it tried to compress class ambiguity and transition-band geometry into one scalar.

## First-principles interpretation

State sufficiency can fail in two distinct geometries.

Class-mode failure: matched present states bifurcate into different future path classes.

Band-mode failure: reliability changes continuously across a marginal transition zone.

Therefore the context correction is hybrid by construction, not ad hoc.

## What remains open

The exact closed-form construction of C_class,t and C_band,t remains open.

A deeper first-principles action or variational derivation for the two activations remains open.

But the observable layer is now much sharper than before: the hybrid boundary is no longer just an intuition.

## Clean current conclusion

The best current theory packet is now hybrid: a universal retained core, class-structured context for B/C-like dynamics, and transition-band context for D-like dynamics.
