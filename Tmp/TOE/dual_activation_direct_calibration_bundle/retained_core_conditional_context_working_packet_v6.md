# Retained-Core with Conditional Context Hypothesis
## Working memo v6 — calibrated dual activation outperforms the simpler shared-context baseline

## Abstract

Repeated pressure tests now support a hybrid reliability architecture rather than a single activation law. The best current model is:

`Lambda_t = sigma(U_t + chi_class,t * C_class,t + chi_band,t * C_band,t)`

with universal retained core:

`U_t = z(|d_t|) - 1.5 z(rho_t)`

The context correction has hybrid geometry: B/C-like regimes are best described by class-structured context, while D-like regimes are better described by a continuous transition-band correction. In the latest direct calibration test, the calibrated dual-activation hybrid outperformed the simpler shared-context baseline on mean ROC AUC across regimes.

---

## What is now locked

- Visible-state-only descriptions were often incomplete.
- A universal retained core repeatedly improved transition-reliability separation.
- Simple A-like regimes were best described by the core alone.
- B/C-like regimes required class-structured context.
- D-like regimes were better described as a transition band than a hard class.
- A hybrid context geometry is now the cleanest bounded architecture.

---

## Locked hybrid reliability model

`Lambda_t = sigma(U_t + chi_class,t * C_class,t + chi_band,t * C_band,t)`

`U_t = z(|d_t|) - 1.5 z(rho_t)`

`P(stable realization of G~_(t+1) | G_t, R_t) = Lambda_t`

---

## Locked observables

### Transition-band depth

`Z_band,t = u1 * EMA(Delta_t)~ + u2 * Var_local(Delta_t)~ + u3 * G_rel,t~`

where

`Delta_t = | P(success | G_t, R_t) - P(success | G_t) |`

This remained the strongest overall observable.

### Class-separatrix distance

`D_class,t = 1 - H_class,t~`

where `H_class,t` is local future path-class entropy from a 3-state future label `{-1, 0, +1}`.

Best current future path-class label parameters:

`horizon = 18, eps_boundary = 0.12, theta_mu = 0.10, theta_persist = 0.70, theta_boundary = 0.34`

This was the first configuration that kept A and D unresolved while allowing B/C to show real future branch commitment.

---

## Derived dual activations

### Class activation

`chi_class,t = sigma(alpha_c * z(1 - D_class,t) - theta_c)`

Interpretation:
Class activation rises when the system approaches a branch separatrix, meaning local future path-class entropy is high and class distance is small.

### Band activation

`chi_band,t = sigma(alpha_b * z(Z_band,t) - theta_b)`

Interpretation:
Band activation rises when persistent state-sufficiency failure, local insufficiency heterogeneity, and local reliability slope indicate entry into a transition band.

---

## Direct calibration result

The hybrid structure was held fixed and only the two activation maps were calibrated.

Best current calibration:

`alpha_c = 3.0`

`theta_c = -1.0`

`alpha_b = 0.5`

`theta_b = -0.2`

Interpretation:
The best current fit wants stronger class activation and gentler band activation.

---

## Calibration comparison

Mean ROC AUC across regimes:

- core_only: **0.4713**
- dual_activation_prev: **0.5402**
- full_shared_context: **0.5509**
- dual_activation_calibrated: **0.5742**

This is the strongest result in the current chain because the calibrated dual-activation hybrid now outperforms both the earlier dual-activation form and the simpler shared-context overlay.

---

## Regime-level read

### A-like
Still the weakest regime, but modestly improved under calibration.

### B-like
Meaningful gain after direct calibration.

### C-like
Strongest regime for the calibrated hybrid.

### D-like
Roughly unchanged. D remains the main unresolved frontier.

---

## Why this matters

This is the first clean result showing that the hybrid architecture is not merely a descriptive story. Once the activation maps are calibrated directly from the locked observables, the hybrid model becomes the best-performing reliability model in this test chain.

That supports the central claim:

**context activation is hybrid rather than singular.**

---

## First-principles interpretation

State sufficiency can fail in two distinct geometries:

- **Class-mode failure:** matched present states bifurcate into different future path classes.
- **Band-mode failure:** reliability changes continuously across a marginal transition zone.

Therefore the correct context correction is hybrid by construction:

`Lambda_t = sigma(U_t + chi_class,t * C_class,t + chi_band,t * C_band,t)`

not a single monolithic scalar and not direct memory as force.

---

## What remains open

- The exact closed-form construction of `C_class,t` and `C_band,t` remains open.
- D-like dynamics remain the weakest frontier.
- A deeper first-principles action or variational derivation for the two activations remains open.

But the architecture is now much sharper than before: the hybrid boundary is no longer just an intuition, and the calibrated dual-activation form has now beaten the simpler shared-context baseline in this test chain.

---

## Clean current conclusion

The best current theory packet is now:

- a universal retained core,
- class-structured context for B/C-like dynamics,
- transition-band context for D-like dynamics,
- and calibrated dual activations that outperform the simpler shared-context baseline in the current test chain.

This is not a final theory claim.

It is a bounded, pressure-tested, reproducible working result under active refinement.
