# UQCF-GEM v13.27 — Projective Coupled-Source / Direct `kappa T` Bridge Gate

**Date:** 2026-09-12

## Adjudication

The direct coupled-source bridge does **not** close from the current frozen ontology.

Quotienting the v13.25-v13.26 ambiguity between `T_obs` and `kappa_obs` is useful, but it does not by itself derive

`Sigma_obs = kappa_obs T_obs`.

A second ambiguity survives:

`Sigma_obs -> c Sigma_obs`, `c>0`.

This is not the RSCL unit gauge. RSCL showed that

`(T_obs,kappa_obs) -> (a T_obs,kappa_obs/a)`

leaves one fixed `Sigma_obs` unchanged.

v13.27 shows that the frozen retained constraints do not select **which magnitude of `Sigma_obs`** couples retained source structure to observer geometry in the first place.

The retained stack can preserve source origin, balance, support, response-selected current, covariance, and source-response direction. These data can constrain a projective source ray. They do not supply a target-blind geometric coupling normalization.

Therefore:

**the projective coupled-source class may be retained, but the nonzero coupled-source magnitude is not derived.**

## 1. Projective Coupled-Source Nonuniqueness Theorem

Let `D_ret` contain the frozen retained source data:

- Genesis/source provenance;
- protected source grading;
- a conditionally selected retained current `J`;
- source balance `B J = s`;
- PGRL/QMAR source-response data;
- recoverability-response rank/stability;
- retained covariance/support certificates.

Suppose a target-blind candidate bridge constructed from these data produces a nonzero coupled source `Sigma_1`.

Every presently frozen structural gate on the coupled-source side is homogeneous:

- source/current balance is linear;
- frame covariance commutes with scalar multiplication;
- positive rescaling preserves support;
- the null source remains null;
- first-order QMAR response is linear in the source generator.

Hence, for every `c>0`,

`Sigma_c = c Sigma_1`

passes the same retained-only structural tests unless an additional scalar calibration law fixes `c`.

v13.26 proved that none of the current ontology-native normalization candidates supplies such an observer/geometric calibration.

Therefore no unique nonzero `Sigma_obs` can be selected from those structural conditions alone.

At most they determine a ray

`[Sigma_obs] = { c Sigma_obs : c>0 }`.

This is an exact type-level nonuniqueness result relative to the current frozen ontology.

It does **not** claim that no deeper law can determine the coupling magnitude.

## 2. Fresh projective source controls

A fixed connected 5-node / 7-edge incidence architecture was used, followed by 64 generic current realizations.

For each retained current `J`, define

`s = B J`.

Then rescale the full source/current package by

`(s,J) -> (c s,c J)`

for

`c = [0.1,0.2,0.5,1,2,5,10]`.

Across all trials:

- maximum source-balance residual: `8.748e-15`;
- maximum normalized source-ray direction change: `3.760e-16`;
- source/current zero/nonzero support pattern: preserved exactly under every positive scale.

So balance, support, and projective direction cannot select the coupled-source magnitude.

## 3. QMAR does not fix the missing coupling constant

v13.11 already established first-order QMAR source linearity:

`QMAR(a P) = a QMAR(P)`

on the fixed faithful state/stratum.

v13.26 established the exact PGRL reparameterization gauge

`P -> a P`,

`t -> t/a`,

which leaves the exponential-family state path unchanged.

Therefore the source-response tangent amplitude rescales while the reparameterized finite path increment does not:

`(dt/a) QMAR(aP) = dt QMAR(P)`.

Fresh generic linear-response controls over 64 random response operators and source directions gave:

- maximum reparameterized response-increment mismatch: `3.598e-15`;
- maximum source-linearity scaling identity error: `3.648e-14`;
- maximum normalized response-direction change: `3.652e-16`.

Thus QMAR canonically supplies source-response **direction and path response once a source parameterization is declared**. It does not create a universal source-to-geometric coupling magnitude.

Identifying a QMAR response norm with `|Sigma_obs|` would be a new constitutive law, not a consequence of QMAR itself.

## 4. Full `kappa T` has an additional tensor-completion obstruction

Even if the coupled ADM constraint-source projections were known, a full stress tensor contains more information.

Relative to an observer split, write schematically

`T = [[rho, j^T], [j, S]]`,

where `S` is the spatial stress block.

The scalar/current data constrain at most the `rho` and `j` projections. They do not determine `S`.

Fresh control constructed two symmetric coupled-source tensors with identical coupled `rho` and `j` projections but different spatial stress blocks.

Results:

- constraint-projection mismatch: `0.000e+00`;
- full coupled-tensor Frobenius distance: `7.70672344821e-01`.

So identical coupled energy/momentum projections do not determine the full `Sigma_obs = kappa T_obs` tensor.

This matters for a full Einstein-equation claim. It does not invalidate using only the scalar/vector projections in a deliberately limited Hamiltonian/momentum-constraint correspondence test.

The archive boundary is consistent with this result: source-to-solder/coframe response, a metric-affine action, and a stress-energy constitutive law remain un-derived.

## 5. Why an Einstein/ADM residual cannot choose `c`

Once geometry is supplied, an Einstein/ADM residual can generally prefer one member of the family

`Sigma_c = c Sigma_1`.

But using that residual to determine `c` would define the source coupling by the gravitational equation we are trying to test.

That is circular.

The required order is:

`retained source data -> lock Sigma_obs -> evaluate ADM/Einstein residual held out`.

Not:

`retained source data + Einstein residual -> fit Sigma_obs`.

Therefore the existing controlled source-coupled correspondence remains evidence about a supplied source package, not a selector for the missing coupling.

## 6. Positive control: one independent geometric calibration is sufficient

The obstruction is precise rather than vague.

If a target-independent calibrated observable supplies one scalar equation

`z = q^T Sigma_obs`

with predeclared `q`, then for a candidate ray `Sigma_obs=c Sigma_1`,

`c = z / (q^T Sigma_1)`

whenever the denominator is nonzero.

A fresh positive control with true `c=2.7` recovered

`c = 2.6999999999999993`

with absolute error

`8.882e-16`.

So one lawful cross-domain calibration, or an independently derived source-to-coframe coupling law with an absolute coefficient, is enough to break the ambiguity.

The current frozen ontology contains neither.

## 7. Missing object

Define:

**RGCL — Retained Geometric Coupling Law**

RGCL must provide a target-blind map

`retained/PGRL/source-current data -> Sigma_obs`

that fixes, before any ADM/Einstein residual is consulted:

1. the observer/geometric tensor type or the explicitly declared constraint-source projection;
2. the source-to-coframe/directional embedding;
3. the universal coupled-source magnitude;
4. frame covariance;
5. source/null behavior.

An independently derived variational source-to-coframe pairing could supply RGCL. An independently calibrated cross-domain source observable could also supply it. Fitting `c` to an Einstein residual cannot.

## 8. What survives

v13.27 does not erase the retained source stack.

Preserved:

- Genesis/source provenance;
- protected retained source amount;
- source-current balance;
- conditional response-selected current shape/support;
- PGRL/QMAR source-response direction;
- frame covariance;
- the RSCL no-go;
- the projective retained source/coupled-source ray;
- controlled source-coupled ADM/Einstein correspondence as a heldout correspondence harness once a source package is supplied.

Not derived:

- unique nonzero `Sigma_obs` magnitude;
- complete `kappa T` tensor from retained scalar/current data;
- source-to-coframe constitutive law;
- physical stress-energy coupling;
- full physical Einstein equations.

## Status

- RSCL no-go: **PRESERVED**
- projective source ray: **PRESERVED / IDENTIFIABLE IN THE DECLARED RETAINED SOURCE SPACE**
- direct target-blind `Sigma_obs`: **NOT DERIVED**
- QMAR as absolute `Sigma_obs` calibration: **NO**
- full coupled stress-tensor completion: **NOT DERIVED**
- Einstein/ADM residual as coupling selector: **FORBIDDEN / CIRCULAR**
- RGCL: **MISSING**
- physical stress-energy identification: **OPEN**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major projective coupled-source nonuniqueness theorem and geometric-coupling boundary**.

## Next — v13.28

### RGCL Origin / Source-to-Coframe Variational Pairing Gate

Do not invent an Einstein-targeted coupling constant.

Audit whether the frozen retained ontology already contains a canonical target-blind pairing between source data and the existing RESA/coframe/solder structure that could generate the coupled source by variation or an equivalent intrinsic construction.

Test only existing candidates:

- Genesis/source grade paired with retained measure/support;
- PGRL/BKM source-response pairing;
- RESA solder/coframe structure;
- QMAR metric-affine response and exact covariance identities.

Ask whether any candidate fixes both the tensor/source projection and coupling magnitude without consulting ADM/Einstein residuals.

If not, freeze RGCL as irreducible relative to the current ontology and stop this source-to-GR coupling branch until one explicit new axiom or independently calibrated physical observable is introduced.
