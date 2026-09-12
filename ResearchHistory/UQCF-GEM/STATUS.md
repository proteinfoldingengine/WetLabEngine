# UQCF-GEM Current Status

**As of:** 2026-09-12  
**Latest completed gate:** v13.27 — Projective Coupled-Source / Direct `kappa T` Bridge Gate  
**Next gate:** v13.28 — RGCL Origin / Source-to-Coframe Variational Pairing Gate

## Current scientific picture

The generic retained geometry remains most honestly organized as a **metric-affine parent**:

```text
Gamma = Gamma_LC + K(T) + L(Q)
```

The post-QRSL / post-RSCL program now separates the source-to-GR bridge into three distinct questions:

```text
retained source/current
→ source origin, balance, support, current selection

absolute observer source split
→ (T_obs,kappa_obs)
→ blocked by RSCL common-scale gauge

coupled geometric source
→ Sigma_obs = kappa_obs T_obs
→ projective source ray survives
→ absolute coupled-source magnitude and full tensor completion blocked by missing RGCL
```

The controlled observer ADM/Einstein correspondence remains a heldout correspondence harness for a supplied source package. It is not permitted to select the missing source coupling.

## Latest result — v13.27

**A direct target-blind `Sigma_obs = kappa_obs T_obs` bridge is not derived from the current frozen ontology.**

v13.25-v13.26 removed one false requirement: the theory does not need to separate `T_obs` and `kappa_obs` if the field equation only uses their product.

But quotienting that unit gauge exposes a second ambiguity:

```text
Sigma_obs -> c Sigma_obs,  c>0.
```

This rescales the coupled source itself and is therefore a missing retained-to-geometry coupling strength, not merely a choice of stress-energy units.

### Projective nonuniqueness theorem

Every currently frozen retained-only structural condition on the coupled-source side is homogeneous:

- source-current balance;
- frame covariance;
- support under positive scaling;
- null-source behavior;
- first-order QMAR source linearity.

Therefore, if one nonzero candidate `Sigma_1` passes those gates, then

```text
Sigma_c = c Sigma_1
```

passes the same gates for every positive `c` unless an additional target-independent geometric calibration fixes `c`.

v13.26 established that the frozen ontology contains no such calibration.

Thus the frozen structure can select at most a ray `[Sigma_obs]`, not a unique coupled-source magnitude.

### Fresh projective source controls

Across 64 generic current realizations on a fixed connected 5-node / 7-edge incidence architecture and positive scales

```text
c = {0.1,0.2,0.5,1,2,5,10},
```

fresh controls gave:

```text
max source-balance residual              = 8.748e-15
max normalized source-ray direction drift= 3.760e-16
support pattern                           = preserved exactly
```

So balance, support, and source direction do not determine the magnitude of the coupled source.

### QMAR does not calibrate `Sigma_obs`

QMAR is first-order linear in the source generator. Combined with the exact PGRL gauge

```text
P -> a P
t -> t/a,
```

one has

```text
(dt/a) QMAR(aP) = dt QMAR(P).
```

Fresh 64-trial generic linear-response controls gave:

```text
max reparameterized increment mismatch   = 3.598e-15
max response scaling identity error       = 3.648e-14
max normalized response-direction drift  = 3.652e-16
```

QMAR therefore supplies source-response direction and a response path conditional on the source parameterization. It does not fix the universal retained-to-geometric coupling amplitude.

Equating a QMAR norm with `|Sigma_obs|` would add a new constitutive law.

### Full stress-tensor completion remains open

Even if coupled energy and momentum projections were known, a full observer stress tensor has a spatial stress block:

```text
Sigma = [[sigma_rho, sigma_j^T],
         [sigma_j,   Sigma_S  ]].
```

A fresh control produced two symmetric tensors with identical coupled `rho,j` projections but:

```text
projection mismatch             = 0
full tensor Frobenius distance  = 0.770672344821
```

Therefore scalar/current source data do not determine the full `kappa T` tensor.

This does not invalidate a deliberately limited Hamiltonian/momentum-constraint correspondence that uses only the scalar/vector projections. It blocks promotion of that limited package to full physical stress-energy.

### Positive calibration control

One independent target-blind calibrated equation

```text
z = q^T Sigma_obs
```

fixes the ray magnitude immediately.

For a synthetic true coupling `c=2.7`, the positive control recovered

```text
c = 2.6999999999999993
absolute error = 8.882e-16.
```

The missing content is therefore precise: one lawful cross-domain geometric calibration or an independently derived source-to-coframe coupling law is sufficient.

## New missing law

**RGCL — Retained Geometric Coupling Law**

RGCL must derive, before any ADM/Einstein residual is consulted:

```text
retained / PGRL / source-current data
->
Sigma_obs
```

including:

1. the declared observer/geometric source tensor or constraint-source type;
2. source-to-coframe/directional embedding;
3. nonzero universal coupling magnitude;
4. covariance and source/null behavior.

A source-to-coframe variational pairing could supply RGCL if it is already forced by the retained ontology. An independently calibrated physical source observable could also supply it. Fitting the coupling against an Einstein residual cannot.

## Preserved results

- finite-state QMAR: **PRESERVED**;
- exact BKM trace/Weyl integrability: **PRESERVED**;
- metric-affine parent kinematics: **PRESERVED**;
- response-selected retained current/Pillar 2: **PRESERVED CONDITIONAL**;
- PGRL/QMAR source-response direction: **PRESERVED**;
- QRSL no-go and RATS seal: **PRESERVED**;
- RSCL no-go: **PRESERVED**;
- projective retained source/coupled-source ray: **PRESERVED**;
- internal represented Path-A ADM-like assembly: **PRESERVED**;
- controlled vacuum and source-coupled weak ADM/Einstein correspondence: **PRESERVED AS CONTROLLED EXTERNAL CORRESPONDENCE**.

## Open boundaries

- MEA/BIFL metric selection remains explicit/conditional.
- Source-to-solder/coframe response is not derived.
- HCPR remains irreducible relative to the frozen ledger.
- Geometry-only autonomous evolution remains obstructed by hidden completion.
- QRSL is irreducible relative to the current frozen ontology.
- RATS remains sealed.
- Ontology-native quantum continuum refinement remains unavailable.
- RSCL is irreducible relative to the current frozen ontology.
- Direct target-blind `Sigma_obs` is not derived.
- Full coupled stress-tensor completion is not derived.
- RGCL is missing.
- Physical stress-energy coupling remains open.
- True third-party validation remains open.
- Full physical Einstein equations are not derived.
- Pillar 3 remains **OPEN**.

## Next gate — v13.28

**RGCL Origin / Source-to-Coframe Variational Pairing Gate**

Audit only structures already frozen upstream:

- Genesis/source grade paired with retained measure/support;
- PGRL/BKM source-response pairing;
- RESA solder/coframe structure;
- QMAR metric-affine response and exact covariance identities.

Ask whether any of them already forces a canonical target-blind source-to-coframe pairing or equivalent intrinsic construction that fixes both the coupled-source type and magnitude.

Do not introduce an Einstein-targeted action or fit a coupling constant to the ADM/Einstein residual.

If no frozen candidate selects RGCL, freeze RGCL as irreducible relative to the current ontology and stop this source-to-GR coupling branch until one explicit new axiom or independently calibrated physical observable is introduced.
