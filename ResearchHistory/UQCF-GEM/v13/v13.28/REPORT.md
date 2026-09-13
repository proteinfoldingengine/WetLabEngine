# UQCF-GEM v13.28 — RGCL Origin / Source-to-Coframe Variational Pairing Gate

**Date:** 2026-09-12

## Adjudication

The four frozen ontology-native pairing classes do **not** supply a canonical target-blind source→geometry coupling with a nonzero absolute magnitude.

The gate outcome is:

`REQUIRES_NEW_AXIOM`

and the present source-to-GR coupling branch is stopped pending either:

1. one explicit new source→geometry axiom with independent motivation; or
2. one independently calibrated physical cross-domain observable.

No Einstein/ADM residual was used as a selector, no coupling constant was fitted, and no new “missing-law” placeholder is introduced.

This does **not** mean that no deeper theory can generate a coupling. It is a branch-stop theorem for the current frozen ontology and the four audited candidate classes.

## 1. Exact source-scale ambiguity being audited

The ETL/PGRL family has the exact reparameterization

`P -> a P`,

`lambda -> lambda/a`,

which leaves the finite state path unchanged.

At one fixed state/tangent point:

- the state-point geometry (`K`, retained measure/support, supplied solder/coframe, fixed graph data) has source-scale weight `0`;
- source tangents, retained source/current and first-order QMAR response have weight `1`.

The physical problem is therefore sharper than merely “finding a scalar.” A lawful source→geometry bridge must distinguish physical source amount from arbitrary source-coordinate normalization.

## 2. Scale-Weight Pairing Obstruction Theorem

Let `G0` be any frozen geometry-side object of source-scale weight zero and let `S1` be a nonzero first-order source object of weight one.

For every source-linear pairing in the audited closure class,

`F(G0, a S1) = a F(G0, S1)`.

Thus the pairing is source-extensive, but its magnitude inherits the arbitrary positive source normalization.

If one instead removes that scale by normalizing or by taking a ratio of equally weighted source quantities, the resulting object has weight zero and is constant along the positive source ray. It can encode direction/projective information, but it cannot preserve an extensive absolute source magnitude.

Therefore, within this candidate class, a nonzero source-extensive and source-parameterization-independent coupling requires one additional object with compensating weight `-1`, or a law canonically equivalent to such a calibrated cross-domain quantity.

The frozen audit finds no such object.

Equivalently: the current ontology cannot tell, using these candidates alone, whether a positive change of source amplitude is a physical increase of source amount or a reparameterization of the same source path in the units needed to set an absolute geometry-side coupling.

This theorem is deliberately scoped. It does not exclude every imaginable nonlinear extension or deeper ontology.

## 3. Candidate A — Genesis/source grade + retained measure/support

Protected source grading fixes retained source amount/extensivity on the retained side. Retained measure/support can localize or weight that source.

But both problems required by RGCL remain:

1. the retained grade does not choose a unique coframe/tensor embedding;
2. multiplying the grade by any frozen weight-zero measure/support object preserves the positive source weight and therefore does not generate an absolute retained-to-geometry conversion factor.

Normalizing the source removes the scale but leaves only a ray/direction.

**Verdict: `OBSTRUCTED`.**

## 4. Candidate B — PGRL/BKM source-response pairing

At a fixed faithful state the BKM information metric `K` is determined by the state and has source-scale weight zero.

For a source tangent `u`, the BKM dual and norm behave schematically as

`K u -> a K u`,

`sqrt(u^T K u) -> a sqrt(u^T K u)`

under `u -> a u`, while the quadratic form scales as

`u^T K u -> a^2 u^T K u`.

So BKM supplies a canonical state-space duality once the source tangent is given, but it does not convert the arbitrary positive source normalization into an absolute geometry-side coupling.

Dividing by the BKM norm makes a direction invariant, but exactly by discarding the amplitude that RGCL needs.

A finite parameterization-invariant increment can be formed by multiplying the tangent response by the inverse-rescaled source coordinate increment, but that constructs a path increment, not a universal local coupling magnitude.

**Verdict: `OBSTRUCTED`.**

## 5. Candidate C — RESA solder/coframe structure

RESA is the strongest candidate for the tensor/type part of the problem because a supplied solder/coframe can map internal directions into declared geometric components.

However:

- the supplied solder has source-scale weight zero and therefore cannot cancel source amplitude;
- more importantly, v13.11 already established that the source-to-solder/coframe tangent is not selected by the quantum source response.

For the same PGRL state tangent and the same induced `dot K` and `dot O`, v13.11 exhibited different admissible solder/coframe lifts producing different torsion-like closure responses, including a canceling lift.

Thus the current ontology does not contain a unique source→solder variational law. A supplied solder may conditionally provide a type map, but it does not create the missing law or its absolute coefficient.

**Verdict: `OBSTRUCTED`.**

## 6. Candidate D — QMAR response + exact covariance identities

QMAR is an exact first-order source-response map on the faithful finite stratum and is covariant under the tested local frame transformations.

But QMAR is linear in the source generator:

`QMAR(aP) = a QMAR(P)`.

Covariance therefore constrains how the response transforms; it does not choose an absolute scalar coefficient.

The exact BKM trace/Weyl identities similarly impose structural relations and null directions, not a coupling magnitude.

There is a second boundary already certified upstream: identical visible geometric variables can have different response jets because hidden completion data remain relevant. Therefore visible geometry does not become an autonomous source state from which an absolute coupling can be reconstructed.

Identifying a QMAR response norm with the coupled source would be a new constitutive law.

**Verdict: `OBSTRUCTED`.**

## 7. Fresh deterministic controls

The checker uses 256 deterministic generic trials with source scales

`a = [0.2, 0.5, 2, 5, 11]`.

Four representative linear maps model the scale algebra of the four audited candidate classes. These random matrices are algebraic witnesses only; they are not physical observables.

Remote GitHub certification on the pinned implementation produced:

```text
max relative linear-scaling error                 1.297966683051917e-15
max normalized direction drift                    1.009936878496612e-15
max relative BKM quadratic scaling error          9.652568951447787e-16
minimum baseline candidate norm                   0.27598617345303345
```

The numerical control confirms the exact algebra used in the theorem:

- source-linear candidate outputs retain weight one;
- normalized directions are invariant to machine precision;
- the BKM quadratic form carries weight two.

These values are implementation checks, not evidence for physical gravity.

## 8. Positive control — what would be sufficient

The checker also supplies an explicit artificial object of weight `-1`:

`g(a) = g0/a`.

Then a weight-one candidate obeys

`g(a) F(aS) = g0 F(S)`.

The maximum relative positive-control mismatch was

`1.2662957816923526e-15`.

So the obstruction is not “coupling is impossible.” One compensating calibrated cross-domain quantity is mathematically sufficient.

The point is that no such calibrated object or equivalent law exists among the four frozen candidates.

## 9. Combined adjudication

Candidate verdicts:

```text
Genesis/source grade + retained measure/support    OBSTRUCTED
PGRL/BKM source-response pairing                   OBSTRUCTED
RESA solder/coframe structure                      OBSTRUCTED
QMAR response/covariance identities                OBSTRUCTED
```

No audited candidate fixes both:

- a canonical source→geometry/coframe type; and
- a nonzero absolute coupling magnitude independent of source reparameterization.

Therefore the gate outcome is

`REQUIRES_NEW_AXIOM`.

This is stronger than saying “RGCL is still missing.” The frozen candidate search is now closed. Continuing this branch by simply naming another internal bridge would violate the adopted stop rule.

## 10. What survives

This gate does not retract:

- finite-state QMAR;
- BKM trace/Weyl exactness;
- the finite metric-affine kinematic stack;
- source-current balance and conditional current selection;
- the projective coupled-source ray `[Sigma]`;
- the controlled external ADM/Einstein correspondence harness for a supplied source package.

It also does not show that gravity is impossible to derive from a deeper theory.

It shows only that the current frozen source→geometry candidate set cannot supply the missing absolute coupling law.

## 11. Program consequence

The source-to-GR coupling branch is now:

`STOPPED_PENDING_NEW_AXIOM_OR_INDEPENDENT_CALIBRATION`.

The branch may restart only if one of the following is explicitly introduced and independently justified:

1. a new source→geometry/coframe axiom with its own physical or information-theoretic motivation; or
2. an independently calibrated observable connecting retained source units to geometry-side units.

A freely chosen dimensionful multiplier is an inserted calibration, not a derivation. Fitting that multiplier to an Einstein/ADM residual remains forbidden.

## Status

- Genesis/measure-support pairing: **OBSTRUCTED**
- PGRL/BKM pairing: **OBSTRUCTED**
- RESA solder/coframe pairing: **OBSTRUCTED**
- QMAR/covariance pairing: **OBSTRUCTED**
- scale-weight pairing obstruction: **CLOSED FOR AUDITED CANDIDATE CLASS**
- RGCL from frozen candidate set: **NOT DERIVED**
- v13.28 gate outcome: **REQUIRES_NEW_AXIOM**
- source-to-GR coupling branch: **STOPPED PENDING NEW AXIOM OR INDEPENDENT CALIBRATION**
- physical stress-energy coupling: **OPEN**
- physical Einstein equations: **NOT DERIVED**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major no-go / branch-stop result relative to the current frozen ontology**.