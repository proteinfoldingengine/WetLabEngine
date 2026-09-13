# v13.28 RGCL Origin / Source-to-Coframe Pairing Audit — Design

## Purpose

Determine whether the already-frozen UQCF-GEM retained ontology contains a canonical target-blind source→geometry pairing that fixes both source type/embedding and a nonzero absolute coupled-source magnitude, without consulting any ADM/Einstein residual and without inserting a free scale.

## Governing stop rule

Allowed gate outcomes are only:

- `DERIVED`
- `OBSTRUCTED`
- `REQUIRES_NEW_AXIOM`

If every frozen candidate is obstructed and no existing calibrated negative-weight object is present, the gate outcome is `REQUIRES_NEW_AXIOM` and this source-to-GR coupling branch stops. Do not introduce another missing-law name.

## Frozen inputs

Audit only structures already certified upstream:

1. Genesis/source grade plus retained measure/support.
2. PGRL/BKM source-response pairing.
3. RESA solder/coframe structure.
4. QMAR metric-affine response and exact covariance/trace identities.

Upstream facts used as premises:

- exact PGRL reparameterization gauge `P -> a P`, `lambda -> lambda/a` leaves the finite state path unchanged;
- source tangent/current/QMAR response are degree-one in source amplitude at a fixed state/tangent point;
- BKM metric, retained measure/support, state-point geometry, and supplied solder/coframe are degree-zero under that source reparameterization;
- v13.11 shows source-to-solder/coframe response is not selected by PGRL/QMAR: the same quantum response admits different solder lifts;
- v13.26 finds no ontology-native absolute observer/source calibration;
- v13.27 proves the implemented source-selection rules determine at most a projective coupled-source ray.

## Main theorem target — scale-weight pairing obstruction

Let `G0` denote any frozen geometry-side object of source-scale weight zero and let `S1` denote a first-order source object of weight one. Consider candidate pairings built from contractions, linear maps, tensor products, and scalar multiplication using the frozen objects, with no externally calibrated coefficient.

- Any source-linear pairing `F(G0,S1)` has weight one: `F(G0,a S1)=a F(G0,S1)`.
- Such a pairing respects source extensivity but its magnitude inherits the arbitrary source normalization.
- Any normalization or ratio that removes the positive scale becomes weight zero and is constant along source rays; it can encode direction/projective data but not an extensive absolute magnitude.
- A nonzero source-extensive, source-parameterization-independent magnitude therefore requires a compensating object of weight `-1` or an independently calibrated cross-domain scalar.

The audit must determine whether any of the four frozen candidate classes supplies such an object or a law canonically equivalent to it.

## Candidate adjudications to test

### A. Genesis/source grade + retained measure/support

Measure/support can weight or localize a retained source but are weight zero. Protected source grade is extensive/weight one. Their pairing remains weight one; normalizing it erases amplitude. They also do not supply a unique coframe/tensor embedding. Expected outcome: `OBSTRUCTED` unless an upstream calibrated inverse-weight object is found.

### B. PGRL/BKM pairing

At fixed state, BKM `K` is weight zero and the source tangent is weight one. BKM duals/norms therefore scale with source amplitude; the quadratic form scales as `a^2`. Parameterization-invariant finite increments require the arbitrary source-coordinate increment and do not define a universal local coupling. Expected outcome: `OBSTRUCTED`.

### C. RESA solder/coframe

A supplied solder can map an already-normalized source direction into a geometric type, but it is weight zero and does not fix magnitude. Upstream v13.11 additionally shows the source-to-solder tangent is nonunique for the same quantum response. Expected outcome: `OBSTRUCTED` for a canonical RGCL.

### D. QMAR response/covariance

QMAR is covariant but degree-one in the source generator. Covariance and exact trace identities constrain form, not normalization. Hidden-completion non-autonomy also prevents visible geometry from becoming an autonomous source law. Expected outcome: `OBSTRUCTED`.

## Fresh controls

Implement deterministic algebraic controls over 256 random trials and source scales `{0.2,0.5,2,5,11}`:

- four representative source-linear pairings corresponding to the four candidate classes;
- maximum relative linear-scaling error;
- maximum normalized direction drift under positive rescaling;
- BKM quadratic scaling error under `a^2`;
- positive control in which an explicit inverse-weight calibration `g(a)=g0/a` cancels the source scaling.

These controls are implementation witnesses of the weight algebra, not evidence that the toy matrices are physical observables.

## Deliverables

Create `ResearchHistory/UQCF-GEM/v13/v13.28/` with:

- `REPORT.md` — theorem, candidate-by-candidate audit, fresh controls, adjudication and stop rule;
- `SUMMARY.json` — machine-readable status and numerical controls;
- `CHECKER.py` — deterministic reproduction of the fresh controls and assertions of the frozen adjudication.

Update:

- `ResearchHistory/UQCF-GEM/STATUS.md`;
- `ResearchHistory/UQCF-GEM/README.md`;
- `ResearchHistory/UQCF-GEM/CHANGELOG.md`.

## Claim boundary

A successful negative gate is a theorem about the current frozen ontology/candidate class. It is not a theorem that no deeper theory can generate a coupling, and it is not evidence for physical gravity. If the gate closes negatively, the next lawful move requires either one explicit new axiom or an independently calibrated physical observable.