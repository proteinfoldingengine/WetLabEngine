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

v15.01 asks whether this apparent cross-space map is actually unnecessary because the provenance/source carrier and the v14 compatibility support are already descendants of one frozen common quantum parent.

The gate does **not** invent a new intertwiner. It audits whether an already-earned parent object, source operator/covector, and support inclusion together induce the projective source ray consumed by v14.03.

The target question is:

\[
\boxed{
\text{Does frozen provenance/source structure already define a parent-space source class whose compression to the archived compatibility support is canonical?}
}
\]

If yes, the v14.04 missing \(J\) is replaced by a common-parent compression already present in the ontology. If no, the v14.04 stop remains irreducible relative to the current frozen stack.

## 2. Frozen compatibility parent and support

The archived quantum compatibility laboratory constructs a global tripartite Hilbert space

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

Coefficient-space density operators \(X\in\mathrm{Herm}(25)\) represent global parent-space states by

\[
T=LXL^\dagger.
\]

Thus the v14.02/v14.03 support space is not a free-standing abstract carrier. It is a concrete orthonormal support of an explicit \(125\)-dimensional quantum parent.

This earned map is frozen and may be reused; it may not be replaced by another support embedding.

## 3. Exact compression map

For any Hermitian parent-space operator/covector

\[
A=A^\dagger\in\mathrm{Herm}(\mathcal H_Q),
\]

define its support compression

\[
C_L(A)=L^\dagger A L\in\mathrm{Herm}(25).
\]

This map is linear and needs no fitted parameter.

### 3.1 Projective descent theorem

v14.03 works with the positive projective equivalence

\[
P\sim aP+bI_{25},
\qquad a>0.
\]

Because \(L^\dagger L=I_{25}\), parent positive-projective equivalence descends exactly:

\[
C_L(aA+bI_{125})
=aC_L(A)+bI_{25}.
\]

Therefore a parent-space class

\[
[A]_+
\]

canonically determines a support-space class

\[
[C_L(A)]_+.
\]

No absolute parent source normalization is required for this step.

### 3.2 Parent/support gauge covariance theorem

Let \(U\in U(125)\) be a parent-space coordinate change and \(V\in U(25)\) a support-coordinate change with

\[
L' = U L V^\dagger,
\qquad A'=UAU^\dagger.
\]

Then

\[
C_{L'}(A')
=VC_L(A)V^\dagger.
\]

So common-parent compression has exactly the support-coordinate covariance required by v14.03.

This is an analytic theorem. Numerical checks are implementation regressions only.

## 4. What counts as a provenance/source parent object

A candidate common-parent source is acceptable only if the frozen archive already supplies a typed object that is one of:

1. a Hermitian source/log-density covector \(A_{\rm prov}\in\mathrm{Herm}(125)\);
2. a parent-space source tangent from which a unique positive-projective covector class is already certified by frozen PGRL/QMAR structure;
3. a more primitive frozen parent object together with an already-earned natural map into \(\mathrm{Herm}(125)\) whose source meaning is independently established.

Merely sharing the word “quantum,” “Genesis,” “source,” or “provenance” does not establish a common parent.

A state \(T\), a field, a graph current, or a lineage ledger is not automatically a source covector. The map from that object to a parent Hermitian source must itself be frozen and independently motivated.

## 5. Candidate classes to audit

v15.01 will audit the following frozen classes.

### Class A — Compatibility parent itself

Audit the actual archived objects in

`Tmp/TOE/UQCF_Quantum_Compatibility_Lab/uqcf_quantum_lab.py`.

Record:

- parent Hilbert-space dimension;
- support dimension;
- support isometry \(L\);
- parent global state \(T=LX_0L^\dagger\);
- target/marginal objects;
- whether any archived object is explicitly certified as a provenance/source covector on \(\mathcal H_Q\).

The existence of \(T\) and \(L\) alone establishes a parent/support relationship, but it does **not** establish a provenance source.

### Class B — Frozen Genesis/provenance carriers

Audit the v14.04 provenance inventory, including:

- Genesis root / append-only ledger / source-origin identity;
- protected retained source grade;
- retained graph source/current package satisfying \(BJ=s\);
- archived 6-D Genesis/pruning field carrier;
- other frozen nontrivial provenance carriers discovered by exact archive search.

For each candidate record:

1. carrier type;
2. dimension / factorization if defined;
3. certified transformation law;
4. whether it already lives on \(\mathcal H_Q\);
5. whether an already-frozen map into \(\mathrm{Herm}(\mathcal H_Q)\) exists;
6. whether that map is source-sensitive and natural;
7. whether compression through the **existing** \(L\) produces a noncentral projective support source class.

### Class C — Existing finite quantum source demonstrations

Audit frozen quantum source examples such as the v13.27 six-qubit finite demonstration.

These may provide genuine same-space PGRL source operators **inside their own declared model**, but they count for v15.01 only if the archive already certifies the same parent representation as the compatibility parent or a natural functor between the parent objects.

A six-qubit \(64\)-dimensional operator cannot be padded, reshaped, truncated, randomly embedded, or dimension-matched into \(\mathbb C^{125}\).

An explicitly chosen demo source operator is a positive control for PGRL mathematics, not provenance evidence.

### Class D — Common-parent compression positive control

As an implementation control only, supply a deterministic noncentral

\[
A_{\rm ctrl}\in\mathrm{Herm}(125)
\]

and verify

\[
P_{\rm ctrl}=L^\dagger A_{\rm ctrl}L
\]

is a valid noncentral support source and can be fed through the frozen v14.03 pipeline.

The control should also verify parent/support gauge covariance and positive-projective descent.

This control proves that **if** provenance supplies an appropriate parent-space class, the common-parent mechanism is sufficient. It does not claim Genesis selects \(A_{\rm ctrl}\).

## 6. The key distinction: parent existence vs source selection

The gate must not conflate these statements:

\[
\text{compatibility support has a parent quantum space}
\]

and

\[
\text{provenance selects a source covector on that parent}.
\]

The first statement is already true for the archived compatibility laboratory.

The second is the scientific question.

Therefore the gate must separately report:

- `compatibility_parent_exists`;
- `provenance_same_parent_candidate_count`;
- `certified_parent_source_class_count`;
- `unique_compressed_projective_class`.

## 7. Compression equivalence is weaker than full parent-operator uniqueness

v15.01 must not demand more than v14.03 needs.

Two parent operators \(A_1,A_2\) may differ outside the archived support while satisfying

\[
L^\dagger A_1L
\sim
L^\dagger A_2L.
\]

Such operators are equivalent for the v14.03 consumer.

Therefore a positive result requires uniqueness only of the **compressed positive-projective support class**, not uniqueness of the full \(125\times125\) parent operator.

Conversely, if frozen provenance admits two lawful parent source constructions with

\[
[L^\dagger A_1L]_+
\neq
[L^\dagger A_2L]_+,
\]

then the source representation remains nonunique even though both constructions share the same parent.

## 8. Prohibited constructions / anti-circularity rules

The following are forbidden as scientific selectors:

- defining \(A_{\rm prov}=LP_{\rm desired}L^\dagger\) from the desired v14.03 source;
- choosing \(A\) to maximize alignment with the v14.02/v14.03 dual ray;
- using the first-contact boundary or dual normal to reconstruct the parent source;
- padding or reshaping the six-qubit demo into the 125-D compatibility parent;
- vectorizing the 6-D Genesis field and declaring its coordinates to be quantum amplitudes;
- SVD/PCA/random-isometry alignment between provenance and parent spaces;
- selecting an embedding by ADM/Einstein residual, gravitational target, galaxy data, or any downstream physical fit;
- using physical time or entropy as a primitive selector;
- treating semantic labels (“Genesis,” “source,” “quantum”) as a typed map.

The gate is target-blind.

## 9. Primary adjudication outcomes

### Outcome 1 — `COMMON_PARENT_INDUCES_SOURCE_RAY`

Use only if frozen structure supplies a provenance/source parent class whose compression through the already-earned support is projectively unique and nontrivial:

\[
\text{provenance}
\to[A_{\rm prov}]_+
\xrightarrow{C_L}
[P]_+.
\]

Required conditions:

- compatibility parent and \(L\) are verified;
- provenance/source object lives on the same parent or reaches it through an already-frozen natural map;
- no arbitrary new identification is introduced;
- compressed support class is noncentral / PGRL-active;
- compressed class is unique up to \(P\sim aP+bI\);
- parent/support covariance closes;
- no target fitting is used.

A result here would connect provenance to the already-certified v14.03 chain.

### Outcome 2 — `COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE`

Use if provenance and the compatibility support genuinely share an already-earned parent representation, but frozen source/provenance structure allows multiple inequivalent compressed support source classes.

This localizes the missing principle to **parent-source selection**, not to a cross-space intertwiner.

### Outcome 3 — `NO_COMMON_PARENT_REPRESENTATION`

Use if the audited frozen provenance carriers do not share the archived \(125\)-D compatibility parent and no already-earned natural parent map connects them to it.

This preserves v14.04's representation-link obstruction.

### Verification stop — `UNRESOLVED_COMMON_PARENT_AUDIT`

Use only if a required archive artifact is missing, malformed, or the implementation cannot adjudicate a declared frozen test. It is not a scientific result.

## 10. Secondary typed status

Even if the primary outcome is `NO_COMMON_PARENT_REPRESENTATION`, report separately whether the compatibility parent itself is verified:

`COMPATIBILITY_PARENT_SUPPORT_VERIFIED`

with

\[
T=LXL^\dagger,
\qquad
L^\dagger L=I.
\]

This prevents a negative provenance result from obscuring the fact that the 25-D support already has a real parent quantum representation.

## 11. Planned executable controls

### 11.1 Parent/support reconstruction

For `V_A` and `V_B` at frozen `FIXED_T`:

- load \(L,X_0,T\);
- verify \(L^\dagger L=I_{25}\);
- verify \(T=LX_0L^\dagger\);
- verify dimensions \(125\leftarrow25\);
- verify support projector \(\Pi=LL^\dagger\) is Hermitian/idempotent.

### 11.2 Compression covariance control

Generate deterministic parent unitary \(U\) and support unitary \(V\), set

\[
L'=ULV^\dagger,
\qquad A'=UAU^\dagger,
\]

and verify

\[
L'^\dagger A'L'=V(L^\dagger A L)V^\dagger.
\]

### 11.3 Positive-projective descent control

For frozen positive scales and identity shifts verify

\[
C_L(aA+bI_{125})
=aC_L(A)+bI_{25}
\]

at machine precision.

### 11.4 Parent-source positive control

Construct deterministic noncentral parent controls without using downstream target objects. Compress each through the frozen \(L\), verify noncentrality, and pass the result through v14.03.

Require at least one control to produce:

- nonzero hidden PGRL tangent;
- simple radial first contact;
- rank-1 v14.02 dual ray.

The control is labeled `SUPPLIED_PARENT_SOURCE_NOT_PROVENANCE_DERIVATION`.

### 11.5 Archive parent inventory

Machine-readable inventory should include at least:

- compatibility tripartite parent;
- Genesis ledger/scalar provenance;
- 6-D Genesis/pruning field;
- retained graph source/current;
- v13.27 six-qubit source demonstration;
- any additional exact-match parent candidates discovered before implementation freeze.

For each record: path, hash, carrier dimension/type, source status, parent-map status, and scientific adjudication.

## 12. Strongest allowed positive interpretation

If `COMMON_PARENT_INDUCES_SOURCE_RAY` is certified, the earned upstream chain becomes

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

with the middle compression map exact, target-blind, projective, and covariant.

This would be a major architectural breakthrough because the missing v14.04 cross-space representation link would be replaced by a common-parent descent already present in the frozen quantum structure.

It would still **not** derive gravity, stress-energy, a source-to-coframe law, spacetime, Einstein equations, or Pillar 3 closure.

## 13. Strongest allowed negative interpretation

If `NO_COMMON_PARENT_REPRESENTATION` is certified, the result is:

\[
\boxed{
\text{the archived compatibility support has an explicit quantum parent,}
\quad
\text{but frozen provenance/source carriers are not represented on that same parent.}
}
\]

Then v14.04's missing representation link is not an artifact of forgetting the support parent. A genuinely new principle or newly discovered frozen map would still be required.

If `COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE` is certified instead, the missing structure is narrower:

\[
\boxed{
\text{common parent exists; provenance-to-parent-source selection is nonunique.}
}
\]

## 14. Relationship to prior gates

### v14.04

Preserved. v15.01 tests a possible way to eliminate the need for an arbitrary direct intertwiner; it does not assume that elimination succeeds.

### v14.03

Preserved. Once a positive projective support source \([P]_+\) is supplied, the hidden tangent, radial first contact and local dual ray remain certified.

### v14.02

Preserved. The specified smooth boundary point still has its objective-independent intrinsic local dual ray.

### v14.01

Preserved. Arbitrary weighted source-to-defect maps remain nonunique.

### v13.26 / v13.28

Preserved. Absolute source normalization and absolute source-to-geometry coupling remain underived. Common-parent compression is projective and does not attempt to fix either magnitude.

## 15. Stop rule

If the archive contains no certified provenance/source class on the compatibility parent and no frozen natural map into that parent, stop with

`NO_COMMON_PARENT_REPRESENTATION`.

Do not manufacture a parent source by lifting the desired \([P]\) through \(L\).

If the parent is shared but multiple inequivalent compressed source classes survive, stop with

`COMMON_PARENT_SOURCE_OPERATOR_NONUNIQUE`.

A subsequent gate may proceed only if:

1. a previously unexamined frozen artifact supplies the missing parent-source selection;
2. a genuinely new representation/source principle is explicitly introduced as **NEW ASSUMPTION**; or
3. an independently motivated information-theoretic construction canonically generates the parent source without using the desired downstream result.

## 16. Breakthrough criterion

Declare a scientific breakthrough only if all of the following are certified:

1. provenance/source structure is genuinely represented on the same frozen quantum parent as the compatibility support;
2. the parent source class is independently earned rather than supplied for the control;
3. compression through frozen \(L\) gives a unique noncentral positive-projective support source ray;
4. the resulting \([P]\) closes through the already-certified v14.03 chain;
5. all prior claim boundaries remain intact.

Anything weaker is a structural localization result, not a gravity derivation.