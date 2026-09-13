# UQCF-GEM v15.02 — Shared-Label Equivariance / Natural Source Representation Gate

**Date:** 2026-09-13  
**Series:** v15 — provenance/source representation origin  
**Base:** `main` at `20508e1a5e3a6d30ced7a17041626b3b81718afe`  
**Branch:** `research/v15.02-shared-label-equivariance`

## 1. Purpose

v15.01 established two facts simultaneously:

1. the fixed 25-dimensional compatibility support is an explicit orthonormal support of a 125-dimensional tripartite quantum parent,
   \[
   L:\mathbb C^{25}\to\mathbb C^{125},\qquad L^\dagger L=I_{25},
   \]
   and a supplied parent Hermitian source class compresses canonically by
   \[
   C_L(A)=L^\dagger A L;
   \]
2. no audited frozen Genesis/provenance/source artifact supplies a provenance-certified Hermitian source class or support-preserving tangent on that same parent.

v14.04 had already shown that an arbitrary cross-space intertwiner is not harmless bookkeeping: different supplied intertwiners produce inequivalent projective source rays and inequivalent downstream first-contact/dual responses.

Therefore v15.02 must not invent another parent source operator or intertwiner.

The next lawful question is narrower:

> Do the retained source/current sector and the five-level factors of the compatibility parent already carry a common finite label/symmetry representation from which a nontrivial parent source class follows equivariantly?

The gate is specifically designed to distinguish a genuine common representation from the superficial observation that both audited controls happen to contain the number five.

## 2. Frozen ontology and governance

The following remain mandatory:

- Primitive/pre-pruning ontology is atemporal.
- Do not use entropy or physical time as a source selector.
- Do not consult Newtonian, Einstein, ADM, gravitational, cosmological, or empirical target residuals when constructing or selecting a representation.
- Do not fit a coupling, operator, factor placement, or label bijection to downstream v14.03 success.
- Do not vectorize/reshape the 6-D Genesis field into a five-level amplitude space.
- Do not pad/truncate an unrelated carrier to dimension five or 125.
- Do not identify two carriers merely because their dimensions/cardinalities coincide.
- Any genuinely new representation axiom must be labeled **NEW ASSUMPTION** and is outside this gate unless separately approved.

The gate is target-blind. The certified v14.03 chain may be used only after an upstream representation has been selected by the frozen source/label structure itself.

## 3. Frozen source-side and compatibility-side objects

### 3.1 Retained source/current control

The v13.25 retained source/current finite control has:

- five nodes;
- seven directed edges;
- source vector \(s\in\mathbb R^5\);
- conserved/response-selected current \(J\) on the edge set, satisfying \(BJ=s\) in the finite control;
- cycle dimension three.

This is a finite source/current control. The integer `5` is not itself a physical identification with the compatibility labels.

### 3.2 Compatibility parent

The archived v9.167–v9.171 compatibility laboratory uses three five-level systems

\[
\mathcal H_A\otimes\mathcal H_{B_1}\otimes\mathcal H_{B_2},
\qquad
\dim \mathcal H_A=\dim \mathcal H_{B_1}=\dim \mathcal H_{B_2}=5,
\]

so the parent Hilbert space has dimension \(5^3=125\).

The fixed open-phase completion supplies the support isometry

\[
L:\mathbb C^{25}\to \mathcal H_A\otimes\mathcal H_{B_1}\otimes\mathcal H_{B_2}.
\]

The compatibility construction distinguishes the central factor \(A\) from the two equal-partner factors \(B_1,B_2\), while preserving an explicit partner-exchange symmetry between \(B_1\) and \(B_2\).

### 3.3 Important label-role distinction

The compatibility code contains several five-valued index roles:

- basis labels on \(A\);
- basis labels on \(B_1\);
- basis labels on \(B_2\);
- values appearing in the arrangement arrays \(V_A,V_B\).

These roles must not be silently identified with one another or with retained source nodes. The audit must record which permutation acts on which role and whether the archived construction is covariant under that action.

## 4. What counts as a shared label carrier

A literal semantic statement such as “source node 2 is quantum basis state 2” is **not required** and would in fact be too basis-dependent.

Instead, v15.02 asks for an equivariant common carrier.

Let \(\mathcal N\) be the five-element retained-node set and let \(\mathcal L\) be a five-element quantum label set for one factor. A candidate identification \(\phi:\mathcal N\to\mathcal L\) is admissible only if changes of identification are pure gauge under an already-earned permutation action.

For a permutation \(\pi\in S_5\), let \(R_\pi\) act on node data and let \(U_\pi\) be the corresponding permutation unitary on \(\mathbb C^5\).

A source-to-operator map \(F\) is equivariant when

\[
F(R_\pi d)=U_\pi F(d)U_\pi^\dagger.
\]

A change of node↔basis bijection counts as harmless gauge only when the *entire relevant compatibility construction* transforms covariantly with the same action. It is not enough that \(U_\pi\) exists abstractly on \(\mathbb C^5\).

The audit therefore has two logically separate questions:

1. **Label-action question:** Is there an archived common permutation action on the retained source carrier and the relevant compatibility-label carrier?
2. **Factor-action question:** If yes, does that common carrier select a unique parent action on \(A\otimes B_1\otimes B_2\), up to already-earned gauge/projective equivalence?

The gate cannot close positively unless both questions close.

## 5. Natural source operators permitted by the gate

The following maps are allowed because they are representation-theoretically canonical once a common five-label carrier is earned. They are not by themselves evidence that the carrier is shared.

### 5.1 Scalar/node source representation

For a retained node-source vector \(s\in\mathbb R^5\), define the centered Hermitian operator

\[
D(s)=\operatorname{diag}(s)-\frac{\mathbf 1^Ts}{5}I_5.
\]

The trace/identity component is removed because v14.03 already quotients sources by

\[
P\sim aP+bI,\qquad a>0.
\]

For any permutation \(\pi\),

\[
D(R_\pi s)=U_\pi D(s)U_\pi^\dagger.
\]

Thus \(D\) is exactly permutation-equivariant.

Controls must include:

- constant source \(s=c\mathbf 1\Rightarrow D(s)=0\);
- nonconstant balanced source;
- positive rescaling \(s\to as\), which must preserve the positive projective class;
- node relabeling covariance.

### 5.2 Directed-current representation

If the retained graph nodes share the same label carrier, orient the edge current into an antisymmetric \(5\times5\) matrix \(K(J)\):

\[
K_{ij}(J)=J_{i\to j}-J_{j\to i}.
\]

Then

\[
P_J=iK(J)
\]

is Hermitian and permutation-equivariant:

\[
P_{R_\pi J}=U_\pi P_JU_\pi^\dagger.
\]

This representation is admissible only for the actual directed node-current data in the frozen finite control. Missing reverse edges are treated as zero current; no new edges or cycle flows may be invented.

Controls must include:

- zero current \(J=0\Rightarrow P_J=0\);
- current reversal \(J\to -J\Rightarrow P_J\to-P_J\) recorded as orientation reversal, not silently identified with the positive projective source class;
- permutation covariance;
- source/current balance preservation on the graph side.

### 5.3 Combined scalar/current representation

The gate must **not** choose a relative coefficient between \(D(s)\) and \(P_J\) unless the frozen ontology supplies it.

A family

\[
D(s)+\alpha P_J
\]

with unfixed \(\alpha\) is therefore evidence of nonuniqueness, not a tunable model family. The audit must report whether scalar and current sectors individually or jointly admit a canonical placement.

## 6. Parent factor actions

Even with a shared five-label carrier, a nontrivial ambiguity may remain: on which parent factor does the operator act?

For a single-factor Hermitian operator \(Q\in\operatorname{Herm}(5)\), the minimal symmetry-respecting candidate placements are:

### 6.1 Central-factor action

\[
A_A(Q)=Q\otimes I\otimes I.
\]

### 6.2 Equal-partner action

Because \(B_1,B_2\) are an equal-partner pair, partner exchange forbids selecting only one partner without further structure. The minimal partner-symmetric action is

\[
A_B(Q)=\frac12\bigl(I\otimes Q\otimes I+I\otimes I\otimes Q\bigr).
\]

### 6.3 Fully symmetric action

\[
A_{\rm all}(Q)=\frac13\bigl(Q\otimes I\otimes I+I\otimes Q\otimes I+I\otimes I\otimes Q\bigr).
\]

These normalizing prefactors do not carry scientific scale because the downstream input is projective. They simply choose convenient representatives.

### 6.4 Forbidden placements

The audit must reject as canonical candidates:

- \(I\otimes Q\otimes I\) alone;
- \(I\otimes I\otimes Q\) alone;
- arbitrary linear combinations of factor actions;
- weights optimized against hidden norm, boundary radius, dual-ray alignment, GR/ADM behavior, or any downstream result.

A single-partner placement may be used only as a negative symmetry control.

## 7. Exact equivariance tests

Let the diagonal permutation action on the parent be

\[
\mathcal U_\pi=U_\pi\otimes U_\pi\otimes U_\pi.
\]

Every candidate parent action must satisfy

\[
A_*(U_\pi Q U_\pi^\dagger)
=
\mathcal U_\pi A_*(Q)\mathcal U_\pi^\dagger
\]

to numerical precision.

The compatibility construction itself must then be transformed consistently. If \(L\) is transformed to \(L_\pi=\mathcal U_\pi L V_\pi^\dagger\) for the induced support-coordinate unitary \(V_\pi\), compression must satisfy

\[
L_\pi^\dagger A_\pi L_\pi
=
V_\pi(L^\dagger A L)V_\pi^\dagger.
\]

The audit may not assume the existence of \(V_\pi\). It must derive or solve for the support action from the transformed support projector/subspace and classify whether the transformed compatibility support is genuinely the same representation.

A permutation that changes the compatibility model to an inequivalent arrangement rather than a gauge-equivalent copy is not part of the common gauge group.

## 8. Automorphism/equivariance groups to audit

The implementation must compute, not presume, the relevant finite groups.

### 8.1 Source-side group

For the retained five-node finite control, enumerate node permutations and identify:

- permutations preserving the directed graph incidence structure;
- permutations preserving the particular source/current realization when required;
- the distinction between graph automorphism covariance and source-state stabilizer symmetry.

### 8.2 Compatibility-side group

For each frozen compatibility arrangement `V_A` and `V_B`, enumerate label permutations and determine which transformations preserve the stipulated compatibility construction up to a unitary relabeling/gauge transformation.

The audit must explicitly separate:

- row/central-factor relabeling;
- partner-factor relabeling;
- arrangement-value relabeling;
- simultaneous relabelings required by the actual formulas.

### 8.3 Common group

The candidate common equivariance group is the intersection after typing the actions correctly. A cardinality match is insufficient.

A useful common group need not be all of \(S_5\), but it must be nontrivial and sufficient to make the node↔quantum-label identification natural up to gauge. If the intersection is trivial and there is no separate archived semantic/functorial identification, the gate cannot claim a shared label carrier.

## 9. Compression to the v14.03 support source

For each lawful parent candidate \(A\), compute

\[
P=L^\dagger A L.
\]

Remove only the already-earned affine identity freedom when comparing source classes. For Hermitian \(P,Q\), define a projective-affine equivalence residual by minimizing

\[
\frac{\|Q-(aP+bI)\|_{\rm HS}}{\max(1,\|Q\|_{\rm HS})},\qquad a>0,
\]

with the closed-form least-squares solution for \(a,b\) followed by the positivity check on \(a\).

Do not normalize away inequivalence.

If a candidate compresses to a central class only, it is PGRL-null and cannot count as a positive source representation.

## 10. Factor-action uniqueness test

For each source object that survives the common-label audit, compare the compressed projective rays from

\[
A_A(Q),\quad A_B(Q),\quad A_{\rm all}(Q).
\]

There are three possible structural cases:

1. the frozen ontology independently singles out one placement;
2. multiple placements survive, but all compress to the same positive projective class for the frozen compatibility support;
3. multiple placements survive and compress to inequivalent projective classes.

Only cases 1 or 2 can support a unique source ray.

Case 3 must be adjudicated as factor-action nonuniqueness.

## 11. Downstream v14.03 control

Only after a source ray is selected upstream, pass the resulting \([P]_+\) through the certified v14.03 machinery:

\[
[P]_+
\to
[\Pi_{\rm hid}\dot X_P]
\to
X_*(P)
\to
[g(P)].
\]

This downstream run is a **sufficiency/control layer only**. It cannot choose:

- the shared-label identification;
- the common permutation group;
- the scalar/current representation;
- the parent factor placement;
- any relative scalar/current coefficient.

If different upstream candidates produce different downstream boundaries/dual rays, that is evidence that the upstream ambiguity is physically/structurally consequential within the model.

## 12. Positive controls

Two explicit controls are required and must be labeled non-scientific.

### 12.1 Supplied shared-label control

Artificially declare a node↔quantum-label bijection and a parent factor placement. Verify:

- exact permutation equivariance;
- compression covariance;
- noncentral projective source when appropriate;
- successful v14.03 source/contact/dual chain.

Classification:

`SUPPLIED_SHARED_LABEL_AND_FACTOR_ACTION_NOT_PROVENANCE_DERIVATION`.

### 12.2 Deliberately incompatible relabeling control

Use a label permutation/action that is not in the computed compatibility-side equivariance group and verify that it is rejected as gauge-equivalent.

Classification:

`INCOMPATIBLE_LABEL_ACTION_REJECTED`.

These controls demonstrate sensitivity of the gate; neither may affect adjudication.

## 13. Primary adjudication outcomes

### 13.1 `SHARED_LABEL_EQUIVARIANCE_INDUCES_SOURCE_RAY`

All of the following must hold:

- an archived nontrivial common label/equivariance carrier is certified;
- the source representation \(D(s)\) and/or \(iK(J)\) is type-correct under that carrier;
- factor placement is uniquely selected by frozen structure or all surviving placements are projectively equivalent after compression;
- the compressed source is noncentral/nonzero for at least one actual frozen source/current fixture;
- covariance controls pass;
- the downstream v14.03 chain closes without influencing upstream selection.

This would be a major architectural breakthrough candidate and must be reported explicitly as such, while still not claiming gravity, stress-energy, spacetime, or Einstein equations.

### 13.2 `SHARED_LABEL_BUT_FACTOR_ACTION_NONUNIQUE`

Use when:

- a common nontrivial label/equivariance carrier is certified;
- at least two factor placements remain equally lawful under the frozen ontology;
- their compressed projective source classes are inequivalent.

This localizes the missing principle to factor action/representation placement.

### 13.3 `NO_CERTIFIED_SHARED_LABEL_CARRIER`

Use when:

- the apparent five-element correspondence is only cardinality coincidence;
- no nontrivial common equivariance/functorial identification is certified;
- or a node↔basis bijection changes the compatibility construction in a way not accounted for by gauge covariance.

This leaves v15.01's representation stop intact.

### 13.4 `CENTRAL_ONLY_OR_PGRL_NULL`

Use as a secondary/diagnostic classification when an otherwise lawful shared carrier yields only central compressed sources.

### 13.5 `UNRESOLVED_EQUIVARIANCE_AUDIT`

Reserved strictly for numerical/implementation failure. It must not be used to hide structural nonuniqueness or a negative theorem.

## 14. Scientific claim boundaries

Even a positive v15.02 result would establish only a natural representation bridge within the frozen finite model:

\[
\text{retained source/current}
\to
[A]_+
\to
[P]_+
\to
X_*
\to
[g].
\]

It would **not** derive:

- an absolute source magnitude;
- an observer energy calibration;
- physical stress-energy;
- a source-to-coframe/solder law;
- physical metric or spacetime;
- physical time;
- Newton's law;
- Einstein equations;
- an absolute gravitational coupling;
- Pillar 3 closure.

v13.26 and v13.28 absolute-scale/coupling obstructions remain intact regardless of v15.02.

## 15. Reproducibility rules

The gate must be deterministic and exact wherever feasible:

- enumerate finite permutations rather than sample them randomly;
- hash all archived source artifacts used in adjudication;
- pin Python/NumPy/SciPy as in the current certified research workflows;
- avoid any adjudication statistic that depends on an arbitrary SVD/null-basis orientation;
- when a subspace comparison is required, compare projectors/principal angles, not basis-vector identities;
- separate theorem checks from floating telemetry;
- bind the final checker to the frozen machine-readable summary only after the scientific thresholds have passed independently.

The known v14.02 SVD-basis-sensitive telemetry flake must not be reproduced in this gate design.

## 16. Implementation artifacts after spec approval

After the written spec is approved, implementation will create:

- `ResearchHistory/UQCF-GEM/v15/v15.02/shared_label_audit.py`
- `ResearchHistory/UQCF-GEM/v15/v15.02/CHECKER.py`
- `ResearchHistory/UQCF-GEM/v15/v15.02/SUMMARY.json`
- `ResearchHistory/UQCF-GEM/v15/v15.02/REPORT.md`
- `.github/workflows/uqcf-v1502-shared-label-equivariance.yml`
- canonical `README.md` / `STATUS.md` updates only after exact-SHA scientific certification.

TDD sequence:

1. RED checker/workflow with missing implementation module;
2. production audit implementation;
3. first GREEN scientific run;
4. freeze report/summary from the exact successful run;
5. bind checker to frozen archive;
6. certify final branch head;
7. fast-forward to `main` only after clean diff;
8. post-merge v15.02 plus preserved v15.01/v14.04/v14.03/v14.02/v14.01/v13.28 safeguards.

## 17. Stop rule

If v15.02 does not certify a shared label carrier or leaves inequivalent factor placements, stop.

Do not continue by choosing a favorite factor, a convenient label bijection, a fitted scalar/current mixture, or the placement that gives the most gravity-like downstream result.

The next continuation would require either:

1. a newly discovered frozen symmetry/functorial structure that removes the ambiguity; or
2. an independently motivated representation principle explicitly labeled **NEW ASSUMPTION** and separately approved.
