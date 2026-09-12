# UQCF-GEM v13.03 — Non-Metricity Continuum Fate / Metric-Compatible Projection No-Go Gate

**Date:** 2026-09-12

## Adjudication

The original continuum test must be corrected.

**Raw discrete non-metricity `N_h -> 0` does NOT imply emergent metric compatibility.**

Across a shrinking edge, any smooth finite metric-affine non-metricity produces a metric mismatch of order `h`.

The correct continuum observable is the edge-length-normalized logarithmic metric distortion

`Q_h = (1/ell_h) log G_h`

with

`G_h = K_j^-1/2 O_ij^T K_i O_ij K_j^-1/2`.

Because `G_h` is symmetric positive definite, its matrix logarithm is well defined on the faithful sector.

The actual Levi-Civita/metric-compatibility criterion is:

`Q_h -> 0`

or equivalently

`N_h = o(ell_h)`

in a convergent smooth sector.

## 1. Gauge-covariant logarithmic non-metricity density

Under independent endpoint frame changes,

`G_h -> R_j G_h R_j^T`

and therefore

`Q_h -> R_j Q_h R_j^T`.

Fresh errors:
- full Q-density covariance: `1.600e-14`;
- trace norm invariance: `4.885e-15`;
- shear norm invariance: `1.310e-14`.

Thus trace/Weyl-like and traceless/shear-like parts can be defined directly on the continuum density without choosing a frame.

## 2. Smooth quantum BKM tower: the decisive control

Take faithful qubit marginals with one smooth Bloch-radius field

`r(x)=0.24+0.18 x`

and use shrinking connected correlations

`C_h = h C_0`.

Positive scalar scaling leaves the polar transport fixed; in this diagonal control `O=I`.

Every two-qubit pair state remains strictly positive throughout the tested ladder.

The raw dimensionless defect satisfies

`||N_h|| ~ h^1.010676`.

So:

`N_h -> 0`.

But the normalized logarithmic density converges to a finite nonzero tensor.

Analytic continuum limit:

`Q_* = [[0.04007373797382734, 0.0, 0.0], [0.0, 0.04007373797382734, 0.0], [0.0, 0.0, 0.12182829327673736]]`.

Norm:

`0.134364958204`.

Deepest executed error to the analytic limit:

`1.158e-05`.

The span of the final four density norms is only

`8.108e-05`.

Therefore a perfectly smooth quantum/BKM refinement can have

`N_h -> 0`

while

`Q_h -> Q_* != 0`.

This is a regular metric-affine continuum, not emergent Levi-Civita compatibility.

## 3. Exact metric-compatible control

When

`K_j = O_ij^T K_i O_ij`

at every level, the logarithmic density vanishes.

Maximum executed density norm:

`2.912e-12`.

This is the true QTC/metric-compatible null.

## 4. Persistent O(1) raw mismatch is too singular

Keep incompatible endpoint BKM metrics fixed while the edge length tends to zero.

Then raw `N_h` stays constant:

fitted exponent

`0.000000`.

The density diverges as

`||Q_h|| ~ h^-1.000000`.

Thus a finite raw mismatch on arbitrarily short edges does **not** describe a finite metric-affine continuum.

It describes a singular/nonregular limit.

## 5. O(h) mismatch is still not enough for convergence

I also built a refinement ladder whose mismatch amplitude is O(h) but whose coefficient alternates between two lawful values.

The logarithmic density remains bounded but oscillates.

Tail even/odd density gap:

`0.104769528008`.

So another correction follows:

`N_h=O(h)`

is sufficient only for bounded non-metricity density, not for existence of a continuum tensor.

A Cauchy/regularity condition is still required.

## 6. Why the current architecture cannot choose among these fates

The same shrinking full-rank correlation scaffold can support:
- exact metric compatibility;
- smooth finite nonzero metric-affine non-metricity;
- divergent non-metricity;
- bounded but nonconvergent non-metricity.

The difference is carried by how the endpoint marginal states / BKM metrics refine.

But v12.11 already found that score-solder subdivision is natural only under an additional affine/transport-consistent score refinement; generic intermediate score data do not preserve the coarse response.

Therefore the present retained architecture has no theorem selecting the cross-scale BKM metric path.

The continuum fate of the v13.02 non-metricity channel is **not derived**.

## 7. Metric-compatible projection is not an innocent repair

Given local selected q metrics, write their square roots as S_i.

The original retained transport in q-orthonormal coordinates is

`A_ij = S_i O_ij S_j^-1`.

If A is not orthogonal, one can mathematically replace it by

`U_ij = polar(A_ij)`.

This gives a metric-compatible transport and is the nearest orthogonal matrix in the chosen q-orthonormal Frobenius norm.

But this is a NEW transport rule.

Fresh three-edge loop control:

- original loop is similar to the raw polar-holonomy loop with error `6.710e-16`;
- original loop trace: `2.91295271122`;
- projected metric-compatible loop trace: `2.9094117239`;
- gauge-invariant trace shift: `0.00354098731909`.

Thus the projection changes holonomy.

It is not a gauge transformation.

Moreover metric compatibility itself does not uniquely select a repaired connection: composing one repaired orthogonal edge map with another allowed orthogonal twist remains metric compatible.

A second metric-compatible repair changed the loop trace again by

`0.0505696266487`.

Therefore:

**project to Levi-Civita/metric compatibility**

is not a derived operation.

The nearest-polar choice becomes unique only after introducing another minimal-distortion principle.

## 8. Relation to the older retained non-metricity result

An older, separate retained-recombination connection showed scale-stable non-metricity under its own coupled coarse-graining.

That is important architectural precedent, but it is not evidence that the new BKM/polar defect has the same RG fate.

The two connections must remain distinguished.

## Updated continuum classification

The correct scaling hierarchy is:

- `N_h=o(h)` -> metric compatibility can emerge;
- `N_h~h Q_*` -> finite nonzero metric-affine continuum;
- `N_h=O(h)` but non-Cauchy coefficient -> no unique continuum non-metricity tensor;
- `N_h=O(1)` -> non-metricity density diverges like `1/h`.

This replaces the naive test `N_h -> 0`.

## Status

- logarithmic BKM non-metricity density: **DERIVED**
- raw `N_h -> 0` as Levi-Civita criterion: **REJECTED**
- finite nonzero metric-affine continuum: **EXPLICITLY REALIZABLE**
- emergent metric compatibility: **NOT DERIVED**
- cross-scale non-metricity regularity: **NOT DERIVED**
- metric-compatible projection: **NOT LICENSED AS DERIVED PHYSICS**
- TFHC: **ONLY AFTER `Q_h -> 0` OR AN INDEPENDENT QTC LAW**
- Pillar 3: **OPEN**

No broader scientific breakthrough is declared.

## Next — v13.04

### Score-Metric Refinement Regularity / Non-Metricity Density Convergence Gate

Now audit whether anything already retained forces

`Q_h`

to converge or vanish:

- PGRL / BKM score construction;
- RESA subdivision;
- score-refinement naturality;
- CRCL / AVT;
- polar transport composition.

If none controls the cross-scale endpoint BKM metrics, isolate the minimal score-metric transport regularity law and stop there rather than replacing the retained connection by a metric-compatible one.
