# UQCF-GEM v15.01 — Common-Parent Representation Audit Design

**Date:** 2026-09-13  
**Status:** DESIGN FROZEN PENDING USER REVIEW  
**Branch:** `research/v15.01-common-parent-representation`

## 1. Purpose

v14.04 localized the upstream missing structure to a representation/intertwiner problem:

\[
\text{Genesis/provenance carrier}
\xrightarrow{\;?J\;}
[P]_+
\to X_*
\to[g].
\]

v15.01 asks whether this apparent cross-space map is unnecessary because the provenance/source carrier and the v14 compatibility support are already descendants of one frozen common quantum parent.

The gate does **not** invent a new intertwiner. It audits whether an already-earned parent object, source operator/covector or source tangent, and the already-earned compatibility support together induce the positive projective source ray consumed by v14.03.

The target question is:

\[
\boxed{
\text{Does frozen provenance/source structure already define a parent-space source class whose descent to the archived compatibility support is canonical?}
}
\]

If yes, the v14.04 missing \(J\) is replaced by a common-parent descent already present in the ontology. If no, the v14.04 stop remains irreducible relative to the current frozen stack.

## 2. Frozen compatibility parent and support

The archived quantum compatibility laboratory constructs the tripartite parent Hilbert space

\[
\mathcal H_Q
=\mathcal H_A\otimes\mathcal H_{B_1}\otimes\mathcal H_{B_2}
\cong\mathbb C^{5^3}
=\mathbb C^{125}.
\]

At the frozen audit point `FIXED_T = 21/41`, each archived family (`V_A`, `V_B`) constructs an orthonormal support isometry

\[
L:\mathcal H_{\rm supp}\to\mathcal H_Q,
\qquad L^\dagger L=I_k,
\]

with

\[
k=25.
\]

Coefficient-space density operators \(X\in\mathrm{Herm}(25)\) represent parent-space states by

\[
T=LXL^\dagger.
\]

The v14.02/v14.03 support is therefore a concrete orthonormal support of an explicit \(125\)-dimensional quantum parent, not a free-standing abstract carrier.

This earned \(L\) is frozen and may be reused. It may not be replaced by another support embedding.

The parent state \(T\) is rank-25 inside the 125-D parent; the faithful state used by v14.03 is the coefficient/support state \(X_0\succ0\). v15.01 must not silently treat \(T\) as faithful on all of \(\mathcal H_Q\).

## 3. Exact parent-to-support descent

For a Hermitian parent-space source/log-density covector

\[
A=A^\dagger\in\mathrm{Herm}(\mathcal H_Q),
\]

define its support compression

\[
C_L(A)=L^\dagger A L\in\mathrm{Herm}(25).
\]

This map is linear, typed, and parameter-free.

### 3.1 Positive-projective descent theorem

v14.03 uses the support equivalence

\[
P\sim aP+bI_{25},
\qquad a>0.
\]

Because \(L^\dagger L=I_{25}\), the corresponding parent equivalence descends exactly:

\[
C_L(aA+bI_{125})
=aC_L(A)+bI_{25}.
\]

Therefore a parent-space positive-projective class \([A]_+\) canonically determines

\[
[C_L(A)]_+.
\]

No absolute parent source normalization is required for this step.

### 3.2 Parent/support gauge covariance theorem

Let \(U\in U(125)\) be a parent-coordinate change and \(V\in U(25)\) a support-coordinate change, with

\[
L'=ULV^\dagger,
\qquad A'=UAU^\dagger.
\]

Then

\[
C_{L'}(A')
=VC_L(A)V^\dagger.
\]

Thus common-parent compression has exactly the support-coordinate covariance required by v14.03.

This is analytic. Numerical tests are regression controls only.

### 3.3 The relevant parent equivalence is weaker than full parent-operator uniqueness

v14.03 needs only the compressed projective support class. Define

\[
A_1\sim_L A_2
\iff
C_L(A_2)=aC_L(A_1)+bI_{25}
\quad\text{for some }a>0,b\in\mathbb R.
\]

Any addition \(B\) satisfying

\[
L^\dagger B L=0
\]

is invisible to the v14.03 consumer.

Therefore a positive result does **not** require a unique \(125\times125\) source operator. It requires a unique noncentral class in the quotient actually seen through \(L\).

### 3.4 Alternate route: support-preserving parent tangent descent

A frozen provenance object may supply a parent-state tangent rather than a covector.

If a Hermitian trace-zero tangent \(\delta T\) is certified and is support-preserving to first order,

\[
\delta T=\Pi\,\delta T\,\Pi,
\qquad
\Pi=LL^\dagger,
\]

then it has a unique coefficient tangent

\[
\delta X=L^\dagger\delta T L.
\]

Because \(X_0\succ0\), the frozen PGRL/BKM tangent map on the support is invertible modulo identity: a support tangent determines a unique projective source class \([P]_+\) whenever it lies in the trace-zero tangent space of normalized states.

Thus an already-earned support-preserving parent source tangent may also close

\[
\delta T\to\delta X\to[P]_+.
\]

This route is admissible only if the source meaning of \(\delta T\) is independently frozen. It may not be reconstructed from the desired v14.03 boundary or dual ray.

If a candidate tangent has a first-order component outside \(\mathrm{ran}(L)\), record

`SUPPORT_CHANGING_PARENT_TANGENT_NOT_V1403_COMPATIBLE`

rather than projecting away that component and pretending the existing fixed-support v14.03 pipeline is complete.

## 4. What counts as a genuine common parent

A candidate common-parent source is acceptable only if the frozen archive already supplies one of:

1. a Hermitian provenance/source covector \(A_{\rm prov}\in\mathrm{Herm}(125)\);
2. a certified support-preserving parent source tangent from which the frozen faithful-support PGRL map determines \([P]_+\);
3. a more primitive frozen parent object together with an already-earned natural map into one of the preceding types.

A common parent is a **typed representation relationship**, not a semantic resemblance.

The following are insufficient by themselves:

- both objects being called “quantum”;
- both being called “Genesis” or “source”;
- equal vector-space dimension;
- existence of a state \(T\) without a source object;
- a field, graph current, ledger, or scalar grade without a frozen map into the parent quantum representation.

If two candidate parents have equal dimension but different certified factorization, symmetry action, or ontology role, they are not identified merely by dimension.

## 5. Candidate classes to audit

### Class A — Archived compatibility parent

Audit

`Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py`.

Record for both `V_A` and `V_B`:

- parent factorization \(A\otimes B_1\otimes B_2\);
- parent dimension 125;
- support dimension 25;
- support isometry \(L\);
- support projector \(\Pi=LL^\dagger\);
- parent state \(T=LX_0L^\dagger\);
- whether any archived object in the lab is explicitly certified as a provenance/source covector or provenance/source tangent on \(\mathcal H_Q\).

The existence of \(T\) and \(L\) verifies the compatibility parent/support relation but does **not** establish provenance sourcehood.

### Class B — Frozen Genesis/provenance carriers

Audit the v14.04 inventory and exact archive matches, including:

- Genesis root / append-only ledger / source-origin identity;
- protected retained source grade;
- retained graph source/current package satisfying \(BJ=s\);
- archived 6-D Genesis/pruning field carrier;
- any additional nontrivial provenance carrier found by the frozen search protocol.

For each candidate record:

1. path and content hash;
2. carrier type and dimension/factorization if defined;
3. certified transformation law;
4. whether it already lives on the exact \(A\otimes B_1\otimes B_2\) parent;
5. whether an already-frozen natural map into \(\mathrm{Herm}(125)\) exists;
6. whether an already-frozen support-preserving parent tangent exists;
7. whether the object is source-sensitive rather than merely provenance-validating;
8. whether its descent through the **existing** \(L\) yields a unique noncentral positive-projective support class.

### Class C — Existing finite quantum source demonstrations

Audit frozen quantum-source examples such as the v13.27 six-qubit demonstration.

These may contain genuine PGRL source operators inside their declared model, but they count for v15.01 only if the archive already certifies the same parent representation or an independently earned natural functor into the compatibility parent.

The v13.27 six-qubit carrier is \(\mathbb C^{64}\), whereas the compatibility parent is \(\mathbb C^{125}\). No padding, reshaping, truncation, random embedding, or arbitrary isometry is permitted.

An explicitly chosen demo source operator is a PGRL positive control, not provenance evidence.

### Class D — Common-parent sufficiency controls

As implementation controls only, supply deterministic noncentral

\[
A_{\rm ctrl}\in\mathrm{Herm}(125)
\]

and verify

\[
P_{\rm ctrl}=L^\dagger A_{\rm ctrl}L
\]

is a valid noncentral support source and closes through the frozen v14.03 pipeline.

Also construct a support-preserving parent tangent control

\[
\delta T_{\rm ctrl}=L\,\delta X_{\rm ctrl}L^\dagger
\]

and verify recovery of its projective support source class using the existing faithful-support PGRL tangent inverse.

Both controls must be labeled

`SUPPLIED_COMMON_PARENT_CONTROL_NOT_PROVENANCE_DERIVATION`.

They prove sufficiency of the common-parent mechanism, not that Genesis selects either control.

## 6. Parent existence and source selection are separate statuses

The gate must separately report:

- `compatibility_parent_exists`;
- `compatibility_parent_support_verified`;
- `provenance_same_parent_candidate_count`;
- `certified_parent_source_covector_count`;
- `certified_support_preserving_parent_tangent_count`;
- `support_changing_parent_tangent_count`;
- `unique_compressed_projective_class`.

This prevents the already-earned compatibility parent from being confused with the still-open provenance/source selection problem.

## 7. Cross-family requirement

The audit must run on both archived compatibility families `V_A` and `V_B`.

A parent-source candidate may compress differently because the frozen supports differ, but its **construction rule and parent transformation law** must be the same frozen law. It may not use the downstream result of one family to choose the source for the other.

A claimed common-parent derivation must either:

- apply lawfully to both frozen families; or
- state an independently frozen family-conditioning variable that explains why the source object differs.

## 8. Prohibited constructions / anti-circularity rules

Forbidden scientific selectors include:

- defining \(A_{\rm prov}=LP_{\rm desired}L^\dagger\) from the desired v14.03 source;
- choosing a parent source to maximize alignment with a v14.02/v14.03 dual ray;
- reconstructing the parent source from first-contact geometry;
- discarding a support-changing parent tangent without a frozen reason;
- padding or reshaping the six-qubit demo into the 125-D compatibility parent;
- vectorizing the 6-D Genesis field and declaring its coordinates to be quantum amplitudes;
- SVD/PCA/random-isometry or arbitrary basis alignment between provenance and parent spaces;
- treating equal dimension as identification;
- selecting a parent map from ADM/Einstein residuals, gravitational targets, galaxy data, or any downstream physical fit;
- using physical time or entropy as a primitive selector;
- treating semantic labels as a typed map.

The gate is target-blind.

## 9. Primary adjudication hierarchy

### Outcome 1 — `COMMON_PARENT_INDUCES_SOURCE_RAY`

Use only if frozen provenance/source structure supplies, on the same compatibility parent, either:

- a parent source class whose compression is projectively unique and noncentral; or
- a certified support-preserving parent source tangent whose faithful-support PGRL inverse is projectively unique and nontrivial.

Required conditions:

- the compatibility parent/support is verified;
- sourcehood is independently frozen;
- no arbitrary representation link is introduced;
- the descended \([P]_+\) is noncentral/PGRL-active;
- the descended class is unique up to \(P\sim aP+bI\);
- parent/support covariance closes;
- the construction works lawfully across the frozen family audit;
- no target fitting is used.

### Outcome 2 — `COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE`

Use if provenance and compatibility genuinely share an already-earned parent representation, but multiple lawful frozen parent-source constructions descend to inequivalent support projective classes.

This localizes the missing principle to **parent-source selection**, not cross-space representation.

### Outcome 3 — `NO_COMMON_PARENT_REPRESENTATION`

Use if the audited frozen provenance carriers do not share the exact archived compatibility parent and no already-earned natural parent map connects them to it.

This preserves the v14.04 representation-link obstruction.

### Verification stop — `UNRESOLVED_COMMON_PARENT_AUDIT`

Use only for missing/malformed required artifacts or an implementation inability to adjudicate a frozen test. It is not a scientific result.

## 10. Secondary typed statuses

Always report the compatibility-side fact independently:

`COMPATIBILITY_PARENT_SUPPORT_VERIFIED`

if

\[
T=LXL^\dagger,
\qquad
L^\dagger L=I,
\qquad
\Pi^2=\Pi=\Pi^\dagger
\]

close under the frozen tolerances.

Other allowed secondary statuses include:

- `NO_PROVENANCE_SOURCE_OBJECT_ON_PARENT`;
- `SUPPORT_CHANGING_PARENT_TANGENT_NOT_V1403_COMPATIBLE`;
- `SUPPLIED_COMMON_PARENT_CONTROL_NOT_PROVENANCE_DERIVATION`.

## 11. Planned executable controls

### 11.1 Parent/support reconstruction

For `V_A` and `V_B` at frozen `FIXED_T`:

- load \(L,X_0,T\);
- verify dimensions \(125\leftarrow25\);
- verify \(L^\dagger L=I_{25}\);
- verify \(T=LX_0L^\dagger\);
- verify \(\Pi=LL^\dagger\) is Hermitian and idempotent;
- verify \(\Pi T\Pi=T\).

### 11.2 Compression covariance

For deterministic parent unitary \(U\) and support unitary \(V\), set

\[
L'=ULV^\dagger,
\qquad A'=UAU^\dagger,
\]

and verify

\[
L'^\dagger A'L'=V(L^\dagger A L)V^\dagger.
\]

### 11.3 Positive-projective descent

For frozen positive scales and scalar shifts verify

\[
C_L(aA+bI_{125})
=aC_L(A)+bI_{25}
\]

at machine precision.

### 11.4 Parent-source positive control

Construct deterministic noncentral parent controls without downstream target objects, compress through frozen \(L\), and pass through the frozen v14.03 pipeline.

Require at least one control per archived family to produce:

- nonzero hidden PGRL tangent;
- simple radial first contact;
- rank-1 v14.02 dual ray.

### 11.5 Parent-tangent positive control

Construct a deterministic support trace-zero tangent \(\delta X\), lift it by

\[
\delta T=L\delta X L^\dagger,
\]

then recover \(\delta X\) and its projective PGRL source class. Check reconstruction and projective invariance.

### 11.6 Archive parent inventory

Machine-readable inventory must include at least:

- compatibility tripartite parent;
- Genesis ledger/scalar provenance;
- 6-D Genesis/pruning field;
- retained graph source/current;
- v13.27 six-qubit quantum-source demonstration;
- any additional exact-match parent candidate discovered before implementation freeze.

For each record: path, hash, carrier type/dimension/factorization, transformation law, source status, common-parent status, parent-map status, tangent status, and adjudication.

## 12. Strongest allowed positive interpretation

If `COMMON_PARENT_INDUCES_SOURCE_RAY` is certified, the earned chain becomes either

\[
\boxed{
\text{provenance}
\to[A_{\rm prov}]_+
\xrightarrow{L^\dagger(\cdot)L}
[P]_+
\to X_*
\to[g]
}
\]

or, for a frozen support-preserving source tangent,

\[
\boxed{
\text{provenance}
\to\delta T_{\rm prov}
\to\delta X
\to[P]_+
\to X_*
\to[g].
}
\]

This would be a major architectural breakthrough because the v14.04 direct representation gap would be replaced by common-parent descent already present in the frozen quantum structure.

It would still **not** derive gravity, stress-energy, a source-to-coframe law, spacetime, Einstein equations, or Pillar 3 closure.

## 13. Strongest allowed negative interpretations

If `NO_COMMON_PARENT_REPRESENTATION` is certified:

\[
\boxed{
\text{the compatibility support has an explicit quantum parent, but frozen provenance/source carriers are not represented on that same parent.}
}
\]

Then v14.04's missing representation link is not an artifact of forgetting the support parent.

If `COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE` is certified:

\[
\boxed{
\text{common parent exists; provenance-to-parent-source selection is nonunique.}
}
\]

That is narrower and would identify parent-source selection as the remaining missing law.

## 14. Relationship to prior gates

- **v14.04 preserved:** v15.01 tests a possible common-parent escape from an arbitrary direct intertwiner; it does not assume success.
- **v14.03 preserved:** once \([P]_+\) is supplied, hidden tangent, radial first contact, and local dual ray remain certified.
- **v14.02 preserved:** specified smooth boundary points carry objective-independent intrinsic dual rays.
- **v14.01 preserved:** arbitrary weighted source-to-defect maps remain nonunique.
- **v13.26 preserved:** absolute source normalization remains underived.
- **v13.28 preserved:** absolute source-to-geometry coupling remains underived.

Common-parent descent is projective and cannot be used to reopen absolute-coupling claims.

## 15. Stop rule

If no frozen provenance/source class or lawful support-preserving provenance source tangent exists on the compatibility parent, and no already-earned natural map connects a provenance carrier to that parent, stop with

`NO_COMMON_PARENT_REPRESENTATION`.

Do not manufacture a parent source by lifting the desired \([P]\) through \(L\).

If a common parent is certified but multiple inequivalent descended source classes survive, stop with

`COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE`.

Continuation then requires one of:

1. a previously unexamined frozen artifact that supplies the missing parent-source selection;
2. an explicitly labeled **NEW ASSUMPTION** introducing a representation/source principle; or
3. an independently motivated information-theoretic construction that canonically generates the parent source without consulting downstream gravity/geometry targets.

## 16. Breakthrough criterion

Declare a scientific breakthrough only if all of the following are certified:

1. provenance/source structure is genuinely represented on the same frozen quantum parent as the compatibility support;
2. the parent source class or parent source tangent is independently earned rather than supplied for a control;
3. descent through the frozen support gives a unique noncentral positive-projective \([P]_+\);
4. that \([P]_+\) closes through the already-certified v14.03 chain;
5. covariance/projective controls close for both archived families;
6. all previous claim boundaries remain intact.

Anything weaker is a structural localization result, not a gravity derivation.