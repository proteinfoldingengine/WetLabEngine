# UQCF-GEM v13.08 — LCSP Integrability / Source Superselection Algebra Gate

**Date:** 2026-09-12

## Adjudication

v13.08 gives both a generic no-go and a special exact positive result.

### Generic result

Across an explicit connected generic LC-compatible family, the stacked tangent map over the 9D fixed local-Pauli PGRL source class has

`rank = 9`, `nullity = 0`.

Thus no nonzero fixed traceless local source generator is tangent everywhere on that family.

### Positive result

A symmetry-selected retained subfamily **does** admit an exact finite nontrivial source algebra.

The sufficient executed structure is:

1. equal faithful local marginals with one common BKM radial axis;
2. cyclically identical pair connected correlations;
3. axial transverse degeneracy `D_x=D_y`;
4. polar transports lying in the corresponding common U(1);
5. compatible RESA solder closure.

Then the common radial source

`P_n = (1/sqrt(3)) sum_i n.sigma_i`

commutes with the retained state in the canonical frame and its full ETL/PGRL flow preserves the LC sector.

## Exact finite-flow control

Baseline state/source commutator:

`0.000e+00`.

Baseline nonzero holonomy angle:

`0.81`.

Across finite source strengths from `s=-0.4` through `s=0.8`:

- maximum QTC defect: `1.103e-15`;
- maximum solder-closure defect: `1.512e-14`;
- maximum polar-transport shift: `1.376e-14`;
- maximum holonomy-angle shift: `1.599e-14`.

So this is not merely a tangent result.

It is an exact finite LC-preserving PGRL flow in the executed symmetry sector.

## Covariant rotated orbit

Rotate the entire retained configuration by a common physical/frame rotation and rotate the source with its BKM radial axis.

The same result persists over the tested connected orbit.

Maximum orbit QTC defect:

`3.056e-15`.

Maximum orbit solder closure:

`2.599e-14`.

Thus the source is best viewed as a covariant one-dimensional source line bundle rather than one fixed laboratory-axis operator.

## Source algebra

The preserving physical source space is one-dimensional modulo identity.

Finite ETL composition is additive:

`rho --s1 P--> --s2 P--> = rho --(s1+s2) P-->`

with error

`4.875e-16`.

The Hermitian Lie bracket vanishes:

`i[P,P]=0`

with norm

`0.000e+00`.

Therefore this is an **abelian source superselection algebra** in the symmetry-selected sector.

The identity source is separately trivial because normalized ETL removes it:

identity-tilt error

`3.182e-16`.

## Generic no-go still stands

The positive result does not rescue generic fixed sources.

For the explicit connected generic LC family, the stacked tangent singular values are

`[1.9100929407506684, 1.9023337910930338, 1.0609562412686293, 1.057339291581509, 0.6456520565248209, 0.6445482828114824, 0.1879994338029362, 0.053226416526870664, 0.03985944134241829]`

with full rank 9.

So the globally fixed traceless source intersection is zero in that tested class.

## Symmetry is doing real work

Break the axial/cyclic pair structure while keeping the initial state QTC-compatible.

Initial QTC defect remains

`1.469e-16`.

Under the same radial source, the defect becomes nonzero:

`[{'s': 0.1, 'max_QTC': 1.3153882892151643e-05}, {'s': 0.2, 'max_QTC': 3.1286670836776663e-05}, {'s': 0.4, 'max_QTC': 7.91342387763813e-05}, {'s': 0.8, 'max_QTC': 0.00019583666008247898}]`.

Therefore exact finite preservation is not a generic consequence of PGRL, positivity, or QTC alone.

It depends on the symmetry-selected stabilizer structure.

## Scientific interpretation

The new picture is:

`metric-affine parent`
contains
`generic LC sector not source invariant`

but also contains

`special symmetry-selected LC submanifold`
with
`nontrivial exact abelian PGRL source algebra`.

That is the first finite source dynamics we have found that:
- remains inside Q=0;
- preserves the discrete torsion-like closure condition;
- retains nonzero relational holonomy;
- composes exactly under finite source insertion.

This is substantial internal progress.

But the symmetry selecting this source sector has not been derived from the ontology, so no broader gravity breakthrough is declared.

## Status

- generic fixed local source algebra: **TRIVIAL IN TESTED CLASS**
- symmetry-selected source algebra: **NONTRIVIAL 1D ABELIAN**
- finite LC-preserving PGRL flow: **CLOSED IN EXECUTED SYMMETRY SECTOR**
- nonzero holonomy preserved: **YES**
- generic LCSP: **NOT DERIVED**
- conditional special-sector LCSP: **CLOSED FOR THE EXECUTED SOURCE LINE**
- metric-affine parent: **REMAINS GENERIC**
- Pillar 3: **OPEN**

## Next — v13.09

### Symmetry-Origin / Einstein-Sector Source Selection Gate

The next question is now sharper and more promising:

Why does the successful cyclic/axial stabilizer structure exist?

Test whether global consistency, provenance symmetry, relational identity, or source grading can derive the stabilizer conditions that make

`P_n`

an exact LC-preserving source.

Then classify whether the one-dimensional abelian line is forced, or whether a larger nonabelian LC-preserving source algebra can exist.
