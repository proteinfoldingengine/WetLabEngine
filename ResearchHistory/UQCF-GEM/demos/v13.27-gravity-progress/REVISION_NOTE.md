# Peer-review revision execution note — UQCF-GEM v13.27

This note records execution of the five minimum revisions requested in `REVIEW_2.md`. It does not upgrade the scientific claim.

## Disposition

The revised artifact is framed as a **finite quantum-relational path plus a projective coupling obstruction**, not as a gravity derivation.

The scientifically interesting claim is that the package implements a concrete, reproducible route from finite quantum states through information-geometric and graph-transport/source structures and reaches a precise positive-scale obstruction without using Newtonian or Einstein dynamics as a selector.

Physical spacetime, stress-energy, absolute gravitational coupling, ADM constraint closure, and Einstein equations remain un-derived.

## Revision 1 — public title and README rescope

Executed.

The public README now leads with:

> **A Finite Quantum-Relational Path and a Projective Coupling Obstruction**

The homogeneity theorem appears before numerical certification or dashboard material. The README explicitly separates derived finite-model objects, modeling choices, implementation controls, and unresolved physical claims.

## Revision 2 — remove “ADM-like sector” language

Executed.

The dashboard and public copy no longer describe an “ADM-like sector.” The retained object is described as a **DeWitt-like quadratic-form diagnostic** on represented `q=(K+epsilon I)^-1` variables.

The `D=-4.5` pure-trace and `D=2` traceless values are identified as algebraic identities / implementation controls. The artifact explicitly states that it contains no lapse, shift, Hamiltonian constraint, diffeomorphism constraint, spatial-slice metric construction, or ADM constraint algebra.

## Revision 3 — promote and qualify the homogeneity lemma

Executed.

At a fixed state/tangent point, with graph and state-point geometry held fixed,

\[
(s,y)\mapsto(c s,c y),\qquad c>0,
\]

implies

\[
J_0\mapsto cJ_0,\qquad a_*\mapsto ca_*,\qquad J\mapsto cJ,
\]

so a coupled-source representative obeys

\[
\Sigma\mapsto c\Sigma.
\]

Therefore only the projective class `[Sigma]` is selected by the frozen rules.

The revised text explicitly states that this is **not** invariance of the whole `rho_lambda` family under arbitrary generator scaling at fixed `lambda`.

## Revision 4 — relabel stress-completion diagnostic

Executed.

The former “spatial-stress completion” scalar is now named

`toy_block_underdetermination_distance`

and is classified as a `CONTROL`. The two matrices are hand-declared and are not represented as a physical `T_{mu nu}` decomposition or reconstruction.

## Revision 5 — add raw polar determinant and pre-clip holonomy audits

Executed and included in telemetry, the portable scientific fingerprint, the checker, documentation and dashboard.

### Raw polar audit

Canonical 25-frame scan:

```text
frames:                                25
edges per frame:                       8
raw O(3) polar factors audited:        200
raw factors with det < 0:              200
raw reflection fraction:               1.0
```

This is a substantive methodological result. In this example, the closest unconstrained orthogonal factor is a reflection on every sampled edge/frame instance. Therefore the subsequent proper-rotation `SO(3)` factor is an explicit orientation-preserving projection choice, not a rare numerical cleanup and not something uniquely forced by the raw polar decomposition.

The projective homogeneity theorem does not depend on interpreting this chosen `SO(3)` factor as physical transport.

### Pre-clip holonomy audit

Authoritative pinned GitHub result:

```text
min raw cosine argument:                -1.0000000000000004
max raw cosine argument:                 1.0
pi-angle events:                         9
clip events above 1e-12:                 0
max clip excess:                         4.440892098500626e-16
adjudication:                             GENUINE_PI_WITHIN_TOLERANCE_NO_CLIP
```

The pi-angle events are therefore not meaningful clipping artifacts at the declared threshold. They remain finite `SO(3)` group diagnostics conditional on the explicit orientation-preserving projection; they are not identified with continuum curvature.

## Frozen revised certification

Portable scientific fingerprint:

`f632e656cc2ea1fc5d61b395080d7259ecfed21c9bd8379626da49f44d6c38fc`

Reference raw telemetry hash, diagnostic only:

`0056223006f943b596e20509c4e77f0020eee3de4064ac83cd9a5ab6a3010f91`

The checker now enforces the new audit counts/tolerances together with the existing state-faithfulness, BKM-positivity, balance, projective-ray, PGRL-reparameterization, cycle-rank and claim-boundary gates.

## Remaining research claim

The revised artifact supports this statement:

> We implement and test a concrete finite quantum-relational path from exact quantum states to information-geometric, declared transport, loop, and graph source/current structures without using Newtonian or Einstein dynamics as selectors. At a fixed state/tangent point, the frozen source-selection rules are positively homogeneous and therefore determine at most a projective coupled-source class. The construction does not determine an absolute gravitational coupling and does not derive physical Einstein equations.

The next research gate must audit named ontology-native source→geometry pairings. Allowed outcomes are only:

- `DERIVED`
- `OBSTRUCTED`
- `REQUIRES_NEW_AXIOM`

A no-go in the frozen ontology **or** a repair that works only by inserting a freely chosen dimensionful scale counts as failure of the target-blind derivation at that point.
