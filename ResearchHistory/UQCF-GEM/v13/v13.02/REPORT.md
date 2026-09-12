# UQCF-GEM v13.02 — Quadratic Transport Compatibility Origin / BKM-Holonomy Naturality Gate

**Date:** 2026-09-12

## Adjudication

**QTC is not derived by the current polar-correlation transport.**

More strongly, it is generically false.

The obstruction is structural:

- the retained polar transport `O_ij` is extracted from the connected pair-correlation tensor `C_ij`;
- the local BKM score metric `K_i` is determined by the local marginal state `rho_i`.

Those are distinct parts of the pair state.

A pair state can change its local marginals while keeping `C_ij`—and therefore the polar transport—fixed.

## 1. Exact local qubit BKM score metric

For a faithful qubit with Bloch vector

`r = r n`,

the centered BKM covariance of local Pauli score directions is

`K(r)=k_perp(I-n n^T)+k_parallel n n^T`

with

`k_perp = r/atanh(r) = 2r/log((1+r)/(1-r))`

and

`k_parallel = 1-r^2`.

For `0<r<1` these eigenvalues are distinct:

`k_perp > k_parallel`.

The numerical spectral implementation and this closed formula agreed to machine precision in all executed controls.

Thus a nonmaximally mixed qubit has a unique BKM radial eigendirection.

## 2. Same C, same O, different QTC result

Fix one full-rank connected correlation tensor

`C = [[0.11520961736999305, -0.023701577842296123, -0.011884682292224915], [0.023106071174361455, 0.09452090105540666, -0.021090918683704635], [0.024348583949485463, 0.02245071204794194, 0.0762491145908609]]`.

Its polar factor is the same nontrivial rotation in all three controls.

### Matched sector

Choose equal marginal Bloch radii and transport the j-side radial axis back with the polar map.

Results:

- state minimum eigenvalue: `0.1725`;
- fixed-C error: `1.993e-17`;
- fixed-O error: `3.713e-16`;
- QTC residual: `4.516e-16`.

QTC closes here.

### Spectral mismatch

Keep exactly the same C and O, but use marginal Bloch radii

`r_i=0.450`

and

`r_j=0.020`.

The pair state remains strictly positive.

QTC residual:

`0.130493879022`.

Dimensionless BKM non-metricity norm:

`0.226046294347`.

### Axis mismatch

Again keep the same C and O, now with equal marginal radii but misaligned radial axes.

QTC residual:

`0.0498641137074`.

Thus even equality of marginal spectra is not enough.

The polar transport must align the BKM eigendirections.

## 3. Exact qubit QTC criterion

For faithful nonmaximally mixed qubits,

**QTC holds iff**

`|r_i|=|r_j|`

and

`O_ij n_j = ± n_i`.

The sign is irrelevant because the BKM metric depends on the radial projector `n n^T`.

At the maximally mixed point `r=0`, `K=I`, so the radial-axis condition disappears.

Fresh randomized theorem controls:
- maximum compatible residual: `3.659e-15`;
- smallest radius-mismatch residual: `4.840e-03`;
- smallest axis-mismatch residual: `6.243e-04`.

This isolates exactly what polar correlation transport would have to do to become metric-compatible.

## 4. Gauge-covariant non-metricity observable

Define

`Delta_ij = K_j - O_ij^T K_i O_ij`.

Under independent local frame changes,

`Delta_ij -> R_j Delta_ij R_j^T`.

A useful dimensionless version is

`N_ij = K_j^-1/2 (O_ij^T K_i O_ij) K_j^-1/2 - I`.

Its trace and traceless/shear norms are gauge invariant.

Fresh gauge errors:
- Delta covariance: `6.779e-16`;
- total dimensionless norm: `3.608e-16`;
- trace-part norm: `6.661e-16`;
- shear-part norm: `4.580e-16`.

So QTC failure is not a coordinate artifact.

It defines an actual discrete BKM non-metricity channel.

No universal shear dominance is claimed for this new channel.

## 5. Generic pair-state survey

A fresh survey used `1000` generic full-rank random two-qubit density states.

QTC relative residual statistics:

- minimum: `0.00668083686838`;
- median: `0.107781169887`;
- 90th percentile: `0.227535035305`;
- maximum: `0.620230164088`;
- count below `1e-3`: `0`.

Median dimensionless non-metricity:

`0.193820631593`.

The trace/shear split varies across states:
- median shear/trace ratio: `1.05509108618`;
- fraction with shear norm larger than trace norm: `0.532`.

Thus generic polar transport is not approximately QTC in this random finite-state control.

## 6. Why current ontology does not force QTC

v10.12 defines

`O_ij = polar(C_ij)`

from connected observable correlations.

It is an isometry of the existing Hilbert-Schmidt observable frames.

It never claims to transport local marginal states or their BKM metrics.

v12.11 proves that local BKM scores transform covariantly under local frame changes and then uses O_ij to compare endpoint score vectors.

That also does not imply

`K_j=O_ij^T K_i O_ij`.

The explicit same-C countermodels prove that no theorem depending only on C, its polar factor, pair-state positivity, and covariance can recover QTC: all those data are identical while QTC changes.

## 7. Pillar-3 consequence

The HLCB sequence from v13.01 was

`MEA -> q -> QTC -> TFHC -> Levi-Civita`.

v13.02 shows that the current polar correlation transport generically stops at QTC.

Therefore we must **not** proceed by testing Cartan torsion and then calling a failure "contorsion" as though metric compatibility had already been established.

The earlier failure occurs first:

**non-metricity**.

Only in the special QTC-compatible sector is TFHC the next discriminator.

## Status

- MEA: **EXPLICIT CONDITIONAL INPUT / NOT DERIVED**
- local SMI: **CLOSED CONDITIONAL ON MEA**
- QTC origin from polar correlation transport: **EXHAUSTED / NOT DERIVED**
- QTC: **GENERALLY FALSE**
- discrete BKM non-metricity defect: **DERIVED**
- HLCB with current polar transport: **GENERICALLY BLOCKED AT METRIC COMPATIBILITY**
- TFHC: **ONLY A SPECIAL-QTC-SECTOR NEXT TEST**
- Pillar 3: **OPEN**

No broader scientific breakthrough is declared.

## Next — v13.03

### Non-Metricity Continuum Fate / Metric-Compatible Projection No-Go Gate

Do not replace the retained transport by Levi-Civita transport by hand.

Instead ask whether

`N_ij`

shrinks naturally under the already-admissible refinement/continuum sector.

Three outcomes are possible:

1. `N_h -> 0`: Levi-Civita compatibility emerges asymptotically and TFHC becomes the correct next gate.
2. `N_h -> N_* != 0`: a genuine metric-affine continuum survives.
3. no stable limit: another cross-scale transport regularity input is missing.

That is now the correct Pillar-3 discriminator.
