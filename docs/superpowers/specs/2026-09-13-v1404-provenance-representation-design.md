# UQCF-GEM v14.04 — Provenance Representation / Intertwiner Gate Design

**Date:** 2026-09-13  
**Status:** DESIGN FROZEN PENDING USER REVIEW  
**Branch:** `research/v14.04-provenance-representation`

## 1. Purpose

v14.03 certified the conditional chain

\[
[P]_+
\longrightarrow
[\Pi_{\rm hid}\dot X_P]
\longrightarrow
X_*(P)
\longrightarrow
[g(P)]
\]

for a **supplied** positive projective Hermitian source/log-density covector
\(P\in\mathrm{Herm}(25)\) on the archived compatibility support.

The remaining upstream question is now sharply typed:

\[
\text{Genesis / provenance}
\;?\;
\longrightarrow
[P]_+.
\]

v14.04 asks whether the already-frozen provenance/source-grading machinery contains a canonical representation law that produces the typed projective source object consumed by v14.03, without inserting a basis identification or embedding by hand.

This gate does **not** search arbitrary formulas from provenance data into \(25\times25\) matrices. It audits representation compatibility and naturality first.

## 2. Frozen source and target types

### 2.1 Provenance-side data

The frozen Genesis/provenance stack contains objects of the following kinds:

- Genesis root / source-origin identity;
- append-only ledger roots / ordered event identities;
- witness registry and quorum validity;
- retained-sequence identity;
- label-transport equivalence / provenance consistency;
- source-flow closure and source/current balance certificates;
- protected retained source grading / source amount on the retained side;
- scalar or dimensionless certification margins;
- in some archived demonstration engines, a separate finite field carrier (for example the 6-D Genesis/pruning field representation).

These objects certify identity, order, consistency, amount/flow, and—in some model-specific engines—fields on their own carrier spaces.

### 2.2 v14.03 support-side source

The v14.03 consumer requires

\[
P=P^\dagger\in\mathrm{Herm}(\mathcal H_{\rm supp}),
\qquad
\mathcal H_{\rm supp}\cong\mathbb C^{25},
\]

modulo

\[
P\sim aP+bI,
\qquad a>0,
\]

because positive scaling and identity shift leave the v14.03 projective source-selection result invariant.

The physical/gauge content used by v14.03 is therefore the positive projective class

\[
[P]_+.
\]

The support coefficient basis is itself a coordinate gauge: v14.03 explicitly certified covariance under support-coordinate unitaries. Therefore the natural target is the projective quotient of Hermitian operators under both support-coordinate conjugation and the already-earned positive affine equivalence.

### 2.3 Type mismatch to be audited

The archive currently does not certify an identification

\[
\mathcal K_{\rm prov}\cong\mathcal H_{\rm supp}
\]

or a natural representation link

\[
J:\mathcal K_{\rm prov}\to\mathcal H_{\rm supp}.
\]

For a provenance carrier larger than the 25-dimensional support, \(J\) may necessarily be a compression/partial map rather than an isometry. Such a choice still requires independent justification.

v14.04 must determine whether a representation link is already implicit/earned, is impossible for gauge-trivial provenance, or remains extra structure.

## 3. Candidate theorem A — Projective Support-Gauge Centrality No-Go

Let \(D_{\rm prov}\) denote provenance data that carry no certified action of the support-coordinate gauge group \(U(25)\).

Suppose one attempts a natural projective source representation

\[
F:D_{\rm prov}\to \mathrm{Herm}(25)/\!\sim,
\]

where

\[
P\sim aP+bI,\qquad a>0.
\]

A support-coordinate change

\[
U\in U(25)
\]

acts on a representative by conjugation,

\[
P\mapsto UPU^\dagger.
\]

Because \(D_{\rm prov}\) is support-gauge trivial, naturality need only require the **projective class** to be invariant:

\[
[UPU^\dagger]_+=[P]_+
\qquad\forall U\in U(25).
\]

Equivalently, for each \(U\), there may exist \(a_U>0\) and \(b_U\in\mathbb R\) such that

\[
UPU^\dagger=a_U P+b_U I.
\]

This weaker projective condition still forces \(P\) to be central.

**Proof target.** The right-hand side commutes with \(P\), so projective invariance for every \(U\) implies

\[
[UPU^\dagger,P]=0
\qquad\forall U\in U(25).
\]

If \(P\) has two distinct eigenvalues, choose a unitary that mixes eigenvectors from distinct eigenspaces. Then \(UPU^\dagger\) does not commute with \(P\), contradiction. Hence \(P\) has only one eigenvalue and

\[
P=\lambda I.
\]

v14.03 already certifies the identity-source control

\[
P=\lambda I
\Longrightarrow
\dot X_P=0.
\]

Therefore:

\[
\boxed{
\text{support-gauge-trivial provenance}
\Longrightarrow
[P]_+=[I]
\Longrightarrow
\text{PGRL-null source}
}
\]

for any natural projective map depending only on those gauge-trivial provenance objects.

This is an exact representation-theoretic theorem target, not a sampled numerical claim.

## 4. Candidate theorem B — Representation-Link Requirement for Nontrivial Provenance Carriers

A richer provenance object may live in its own carrier

\[
\mathcal K_{\rm prov}
\]

with a provenance-side operator/tensor/source object \(P_{\rm prov}\).

To produce a support-side Hermitian source for v14.03 requires a typed representation link such as

\[
J:\mathcal K_{\rm prov}\to\mathcal H_{\rm supp}
\]

and then, where type-correct,

\[
P_J = J P_{\rm prov}J^\dagger.
\]

If provenance-side transformation laws are certified, \(J\) must satisfy the corresponding intertwining/naturality relation. If no such group action is certified, the object should be called a **representation link** rather than an intertwiner, and its canonicality must be justified by other frozen structure.

An arbitrary dimension match, reshaping, truncation, random isometry, Fourier map, PCA alignment, singular-vector alignment, or target-optimized embedding is **not** a derivation.

If no frozen structure selects \(J\), then the map provenance \(\to[P]\) remains underdetermined.

## 5. Audit classes

v14.04 will audit exactly three representation classes.

### Class A — Gauge-trivial ledger/scalar provenance

Examples:

- Genesis root identity;
- event hashes / append-only roots;
- witness/quorum validity;
- ordering validity;
- provenance/certification booleans;
- scalar source grade;
- scalar similarity, closure, or provenance margins.

Question:

> Can these support-gauge-trivial objects naturally produce a noncentral projective class \([P]_+\)?

Expected theorem test: **no**, by projective support-gauge centrality.

Required control: construct deterministic noncentral Hermitian operators and verify that their projective conjugation orbit is nontrivial, while a central operator remains invariant.

The computational control is implementation evidence; the theorem does not depend on finite sampling.

### Class B — Frozen nontrivial provenance carriers

Audit concrete archived carriers such as:

- 6-D Genesis/pruning fields;
- retained graph/source vectors or currents when available;
- any certified operator/tensor carrier explicitly tied to provenance.

For each carrier record:

1. carrier type/dimension;
2. transformation law actually certified in the archive;
3. whether a map into the compatibility support already exists;
4. whether that map is canonical/natural or stipulated;
5. whether changing an admissible representation link changes \([P]_+\).

A demonstration/visualization map to geometry does not automatically count as a representation map to the v14.03 support.

### Class C — Declared-link positive/ambiguity control

Supply an explicit representation link \(J\) as **external declared structure**. For a small fixture with \(\dim\mathcal K\le25\), use isometries so the control is mathematically clean.

Then verify

\[
P_J=J P_{\rm prov}J^\dagger
\]

can produce a noncentral source ray and drive the certified v14.03 chain

\[
[P_J]_+\to X_*(P_J)\to[g(P_J)].
\]

Next vary \(J\) within a deterministic family preserving the same provenance-side input and the same declared isometry constraints.

If the resulting projective source rays or downstream first-contact/dual rays differ, that is direct constructive evidence that an unfixed representation link is genuine missing information.

The positive control must be labeled **supplied representation link**, not derived provenance physics.

## 6. Canonicality / naturality rules

A provenance→source representation counts as derived only if all of the following hold:

1. **Typed:** domain and codomain are explicitly defined.
2. **Projectively natural:** coordinate/gauge changes preserve the output class, not necessarily one arbitrary representative.
3. **Source-sensitive:** nontrivial provenance/source variation can produce a noncentral projective source ray.
4. **No target fitting:** no ADM/Einstein residual, gravitational observable, or desired v14.03 dual ray is used to choose the map.
5. **No arbitrary basis bridge:** no arbitrary index ordering, reshaping, truncation, random seed, SVD/PCA frame, or unearned metric selects the representation.
6. **Projective consistency:** output is evaluated only up to the already-earned equivalence \(P\sim aP+bI\), \(a>0\).
7. **Archive traceability:** every structural ingredient used to define the map is tied to a frozen prior artifact or explicitly labeled new assumption.

## 7. Exact adjudication hierarchy

The primary v14.04 outcome is chosen by the following hierarchy.

### Outcome 1 — `DERIVED_PROVENANCE_SOURCE_RAY`

Use only if a frozen, independently motivated representation link already exists and uniquely determines the positive projective support-source ray up to the v14.03 equivalence.

This requires:

- a nontrivial provenance-side carrier;
- certified transformation laws where applicable;
- a natural map/link into the support carrier;
- projective uniqueness under all permitted gauges;
- no target-dependent fitting.

### Outcome 2 — `CENTRAL_ONLY_PGRL_NULL`

Use if the audited frozen provenance data are support-gauge trivial and the only natural projective support-side Hermitian representation is central:

\[
[P]_+=[I],
\]

hence PGRL-null.

This is the sharpest possible result for Class A.

### Outcome 3 — `REQUIRES_NEW_REPRESENTATION_LINK`

Use if nontrivial provenance carriers exist, but no frozen natural map/link identifies them with the v14.03 support space, and different supplied admissible links yield inequivalent projective source rays and/or inequivalent v14.03 downstream selections.

This is the expected broader branch outcome if Class A is centrally obstructed while Class B has nontrivial carriers without a certified link.

### Verification stop — `UNRESOLVED_REPRESENTATION_AUDIT`

Use only for implementation/numerical inability to adjudicate a declared test. It is not a scientific result.

## 8. Primary combined gate logic

The combined gate should prefer the most informative ontology-level status.

- If a frozen natural nontrivial representation is found: `DERIVED_PROVENANCE_SOURCE_RAY`.
- Else if the archive contains only support-gauge-trivial provenance objects: `CENTRAL_ONLY_PGRL_NULL`.
- Else if nontrivial provenance carriers exist but require an unfixed bridge into support space: `REQUIRES_NEW_REPRESENTATION_LINK`.

The Class-A projective-centrality theorem may still be recorded as a theorem even when the combined gate outcome is `REQUIRES_NEW_REPRESENTATION_LINK`, because the latter accounts for richer carriers.

## 9. Planned executable controls

The implementation plan should include deterministic controls sufficient to verify, but not define, the theorem/audit.

### 9.1 Centrality controls

For \(d=25\):

- construct deterministic noncentral Hermitian matrices;
- conjugate by a fixed predeclared family of unitary matrices;
- test projective equivalence directly under \(P\sim aP+bI\);
- verify generic noncentral conjugates leave the original projective class;
- verify \(\lambda I\) remains invariant;
- use the complete 25-dimensional Heisenberg–Weyl unitary 1-design (\(25^2=625\) unitaries) as an exact finite twirl regression control:

\[
\frac1{625}\sum_{a,b}W_{ab}PW_{ab}^\dagger
=
\frac{\mathrm{Tr}P}{25}I.
\]

The exact centrality theorem is analytic; the Weyl twirl is a deterministic regression control only.

### 9.2 PGRL-null control

Reuse v14.03's stable Fréchet tangent implementation and verify

\[
P=\lambda I\Rightarrow \|\dot X_P\|\approx0
\]

under the frozen tolerance.

### 9.3 Declared-link controls

Construct a small deterministic provenance carrier fixture \(\mathcal K\) and operator \(P_{\rm prov}\), together with at least two supplied isometric links \(J_1,J_2\) into \(\mathbb C^{25}\).

Verify:

- both satisfy the declared isometry constraints;
- both produce valid noncentral support-source operators;
- the resulting projective source classes are tested for equivalence under \(P\sim aP+bI\);
- when inequivalent, feed them through the frozen v14.03 pipeline and quantify hidden-direction, first-contact, and dual-ray separation.

This fixture is a **positive/ambiguity control**, not evidence that Genesis chooses either link.

### 9.4 Frozen archive type inventory

Machine-readable metadata should record for each audited frozen candidate:

- source path / artifact;
- domain type;
- codomain if any;
- certified symmetry/transformation law;
- whether a support-space map exists;
- whether that map is natural;
- adjudication.

## 10. Claim boundaries

Even `DERIVED_PROVENANCE_SOURCE_RAY` would establish only the upstream representation arrow

\[
\text{provenance}\to[P]_+.
\]

Together with v14.03 it would yield a longer conditional chain

\[
\text{provenance}
\to[P]_+
\to X_*
\to[g].
\]

It would **not** by itself derive:

- absolute source magnitude;
- observer calibration;
- source-to-solder/coframe law;
- stress-energy;
- absolute source→geometry coupling;
- physical metric or spacetime;
- Einstein equations;
- Pillar 3 closure.

If the gate lands on `REQUIRES_NEW_REPRESENTATION_LINK`, that does not mean no deeper theory can supply one. It means the current frozen ontology does not yet contain the required representation link.

## 11. Relationship to prior gates

### v14.03

Preserved. v14.03 remains a positive **conditional** result for supplied \([P]_+\).

### v14.02

Preserved. The boundary-local intrinsic dual ray remains derived once a smooth first-contact point is supplied/selected.

### v14.01

Preserved. Arbitrary source→higher-incidence weighting remains nonunique. v14.04 does not revive that family.

### v13.26

Preserved. Absolute source normalization remains underived. v14.04 works projectively and does not attempt to fix amplitude.

### v13.28

Preserved. Absolute source→geometry coupling remains stopped pending new axiom or independent calibration.

## 12. Stop rule

If the archive audit finds no frozen natural provenance→support representation link and the declared-link controls demonstrate genuine projective/downstream ambiguity, **stop**.

Do not create a v14.05 that simply invents another embedding.

A continuation of this branch would then require one of:

1. an explicitly new representation axiom, independently motivated and clearly labeled as a new assumption; or
2. a newly discovered prior artifact that already defines the required natural representation link; or
3. an independently motivated physical/information-theoretic structure that canonically identifies the two representation spaces without using the desired downstream result.

## 13. Expected strongest defensible interpretation

If the likely combined outcome is confirmed, the architecture becomes

\[
\boxed{
\text{Genesis / provenance}
\to
\text{nontrivial provenance carrier}
\xrightarrow{\;\text{missing natural }J\;}
[P]_+
\to
X_*
\to
[g]
}
\]

with the analytic sub-theorem

\[
\boxed{
\text{gauge-trivial provenance alone}
\to
[P]_+=[I]
\to
\text{PGRL-null}
}.
\]

That would localize the remaining upstream missing structure to a **representation/intertwiner law**, rather than a weighting function, absolute scale, or boundary selector.
