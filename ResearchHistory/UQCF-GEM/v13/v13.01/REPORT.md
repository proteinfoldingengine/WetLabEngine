# UQCF-GEM v13.01 — Metric-Origin Branch Stop / Minimal Ensemble Axiom and HLCB Dependency Gate

**Date:** 2026-09-12

## Adjudication

The metric-origin search is now formally stopped inside the current BKM/naturality architecture.

The smallest explicit conditional metric input is:

**MEA — Minimal Ensemble Axiom**

1. **BIFL:** the physical score second moment is isotropic under the full BKM isometry group;
2. one universal positive per-protected-source second-moment normalization `c_*`.

Then

`q_i = c_* K_i^-1`.

Neither clause is currently derived.

But v13.01 finds an important simplification:

**the numerical value of a universal constant `c_*` is not needed to test the Holonomy–Levi-Civita bridge.**

The connection bridge depends on metric shape, transport compatibility, and torsion—not on one overall constant spatial scale.

## 1. Local SMI closes conditionally

Before v12.99, Path-A q and RESA solder geometry were independent channels, so defining a coframe from q would have been circular.

That changed with SSQRT.

SSQRT constructs q directly from score-solder second moments on the same RESA fiber:

`D^2(xi)=xi^T q xi`.

Once MEA selects the second moment, q is already a quadratic form on the retained solder germ.

Choosing a coframe `e` satisfying

`e^T e=q`

is therefore only a representation of that already-selected local metric.

Fresh symmetric-square-root error:

`6.981e-15`.

A rotated coframe `R e` gives the same q with error:

`7.331e-15`.

Therefore:

**LOCAL SMI = CLOSED CONDITIONAL ON MEA.**

This does not make MEA derived.

## 2. A new independent bridge appears: QTC

Define:

**QTC — Quadratic Transport Compatibility**

With the archive convention that `O_ij` transports vectors from `V_j` into `V_i`, metric compatibility is

`q_j = O_ij^T q_i O_ij`.

Equivalently under universal MEA scale:

`K_j = O_ij^T K_i O_ij`.

If QTC holds and `S_i^T S_i=q_i`, `S_j^T S_j=q_j`, then

`U_ij = S_i O_ij S_j^-1`

is an orthogonal transport in q-orthonormal coordinates.

Fresh positive control:

- QTC residual: `0.000e+00`;
- BKM K transport residual: `3.611e-16`;
- induced orthogonality error: `1.139e-15`.

Changing the coframe gauges at both endpoints changes `U_ij` only by the expected endpoint orthogonal conjugation.

Gauge-relation error:

`2.375e-16`.

Gauge orthogonality error:

`1.008e-15`.

## 3. Local metric selection does not imply QTC

Take two perfectly positive local BKM metric shapes and apply MEA separately.

They need not have the same normalized spectrum.

Fresh incompatible control:

- relative QTC residual: `0.177058173667`;
- normalized spectral-shape gap: `0.0558197589883`;
- induced q-frame transport orthogonality defect: `0.359607163441`.

Orthogonal congruence preserves eigenvalue shape.

Therefore no endpoint coframe gauge can repair a generic mismatch of this kind.

Thus:

**MEA/BIFL does not imply QTC.**

This is consistent with the existing Score–Solder architecture: local score covariance is certified under frame changes, but generic physical edge transport/refinement of the score field is not derived.

## 4. Overall constant scale does not block HLCB

Rescale both endpoint metrics by the same constant:

`q_i -> c q_i`,
`q_j -> c q_j`.

The q-orthonormal induced transport is unchanged.

Fresh error:

`2.607e-16`.

For a smooth metric, constant rescaling also leaves the Levi-Civita connection unchanged because the inverse-metric and derivative factors cancel.

Fresh Christoffel error under an 11x global rescaling:

`1.570e-16`.

Therefore the **value** of universal `c_*` is irrelevant to the question

`omega_R ?= omega_LC`.

It remains relevant to:
- physical length units;
- dimensional curvature magnitude;
- coupling normalization.

## 5. But a varying normalization is real geometry

Let the normalization vary with the germ.

Then the Levi-Civita connection changes.

Fresh variable-scale Christoffel defect:

`0.584486075279`.

Likewise different endpoint scale factors destroy q-orthogonality of the same retained transport.

Fresh discrete orthogonality defect:

`2.72179412618`.

So v13.01 sharpens the normalization requirement:

HLCB does **not** need the absolute value of `c_*`, but it does require the scale to be universal/constant over the sector being identified.

A state-dependent normalization would become an additional Weyl/non-metric field rather than a harmless units choice.

## 6. Coframe choice does not contaminate TFHC

The remaining torsion test is genuinely gauge invariant.

For a smooth x-dependent local frame rotation:

`e' = R(x)e`

and

`omega' = R omega R^-1 - dR R^-1`.

Then

`T' = R T`.

Fresh nontrivial x-dependent gauge control:

- base Levi-Civita torsion norm: `0.000e+00`;
- transformed torsion norm: `1.571e-16`;
- full tensor covariance error: `1.571e-16`.

A nonzero contorsion remained nonzero:

- original torsion norm: `0.350535051409`;
- gauge-transformed norm: `0.350535051409`;
- covariance error: `1.571e-16`.

Therefore the outcome of TFHC cannot be changed by selecting a convenient square root of q.

## 7. Final HLCB dependency map

After freezing metric origin, the bridge is:

`MEA/BIFL`
-> local score-solder q
-> **QTC**
-> q-orthogonal retained connection
-> **TFHC**
-> Levi-Civita identification.

The precise theorem is:

If MEA selects local q, QTC makes the retained connection metric-compatible with that q, and TFHC gives

`T=de+omega_R wedge e=0`,

then the uniqueness of the torsion-free metric connection yields

`omega_R=omega_LC(q)`,

and the v12 holonomy curvature is the curvature consumed by the Path-A Ricci/ADM channel.

If QTC fails, the connection is already non-metric relative to q and the Levi-Civita identification stops before torsion.

If QTC passes but TFHC fails, the surviving defect is metric-compatible contorsion.

## Status

- metric-origin search inside current BKM/naturality stack: **STOP**
- MEA: **EXPLICIT CONDITIONAL INPUT / NOT DERIVED**
- local SMI: **CLOSED CONDITIONAL ON MEA**
- QTC: **NOT DERIVED**
- TFHC: **NOT DERIVED**
- HLCB: **OPEN, REDUCED TO QTC + TFHC AFTER MEA**
- absolute value of universal c_* for HLCB: **NOT REQUIRED**
- absolute physical metric normalization: **STILL OPEN**
- Pillar 3: **OPEN**

No broader scientific breakthrough is declared.

## Next — v13.02

### Quadratic Transport Compatibility Origin / BKM-Holonomy Naturality Gate

Audit whether the retained pair transport itself intertwines the local BKM score metrics:

`K_j ?= O_ij^T K_i O_ij`.

Under the universal MEA scale this is exactly QTC.

If it closes, proceed immediately to the real torsion test.

If it fails, quantify the resulting non-metricity defect and do not force a Levi-Civita projection.
