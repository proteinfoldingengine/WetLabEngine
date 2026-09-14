# v15.28 — Pre-Time Constitutive Coupling Space / Provenance-Lift Gate

**Date:** 2026-09-14  
**Series:** UQCF-GEM / Retained Atlas — gravity-before-time program  
**Base:** `research/v15.27-target-origin` at `700a4639010100a12b73882d530ac2c2bbf1f71e`  
**Branch:** `research/v15.28-coupling-space`  
**Status:** DESIGN FROZEN FOR REVIEW — NO IMPLEMENTATION YET

## 1. Purpose

v15.25 killed bare compatibility as a gravity-before-time canary: the source equation alone permits both a distributed Hodge representative and exact local cancellation. v15.26 showed that a metric-free higher-incidence response operator can resolve all cycle degrees **once a response target is supplied**. v15.27 then proved that this target is not inherited from the source quotient alone and is not selected by microscopic inheritance, Hodge convenience, zero target, or topology + source-linearity + relabeling covariance.

The remaining missing object is therefore not “some selector.” It is a typed pre-time constitutive coupling

\[
\eta:\mathcal S_{\rm prov}\longrightarrow\mathcal Y_{\rm cyc}
\]

from a provenance-enhanced source representation to the higher-incidence/cycle-response representation.

v15.28 will **classify the complete coupling space permitted by already-earned representation structure before exposing any candidate to gravity-like observables**.

The primary adjudication quantity is

\[
 d_\eta
 =\dim \operatorname{Nat}^{\rm cov}_{\otimes}
   (\mathcal S_{\rm prov},\mathcal Y_{\rm cyc}),
\]

implemented in the finite audited setting as the dimension of the exact linear space of admissible equivariant intertwiners after all certified quotient/composition constraints are imposed.

The gate is successful as an audit whether the result is zero-, one-, or multi-dimensional. It must not manufacture a positive result.

---

## 2. Scientific question

For each already-earned provenance/source carrier with a certified transformation law and a certified relationship to the v15.26 chain complex, determine whether there exists a nonzero coupling

\[
\eta\in\operatorname{Hom}_G(\mathcal S_{\rm prov},\mathcal Y_{\rm cyc})
\]

that also satisfies every additional structure already earned for that carrier.

The decisive outcomes are:

\[
\boxed{
 d_\eta=
 \begin{cases}
 0,&\text{no admissible coupling from that structure},\\
 1,&\text{coupling form unique up to overall scale},\\
 >1,&\text{constitutive response remains underdetermined}.
 \end{cases}}
\]

A one-dimensional result fixes **form only**. It does not determine physical magnitude, gravity, a metric, time, or an actual record.

---

## 3. Frozen claim boundary

### 3.1 Frozen inputs that may be used

The gate may inspect and hash, but not rewrite:

- v15.27 exact-head source, report, tests, and release evidence;
- v15.26 response-selector/rank package;
- v15.25 pre-time gravity-canary package;
- v14.04 provenance-representation / missing-intertwiner result;
- v15.01–v15.03 representation-unification audits;
- the retained graph source/current carriers already frozen in v13;
- the frozen Genesis/provenance carriers already audited in v14.04;
- exact incidence, provenance, graph-label, tensor-factor, or symmetry actions explicitly certified in those artifacts.

No candidate may be admitted merely because it is mathematically convenient or resembles the desired target representation.

### 3.2 Prohibited selectors

The following must not enter the coupling-space constraints, candidate ranking, normalization, or adjudication:

- holonomy magnitude or remote-loop response;
- inverse-square behavior;
- Newtonian potential/acceleration;
- Einstein/ADM residuals;
- lensing, rotation curves, cosmological fits, or any other gravity target;
- a preferred metric, Hodge norm, minimum action, smoothness, radiality, or distance penalty;
- pruning, entropy, RCR, record probability, or physical time;
- an arbitrary source-to-target embedding, random isometry, PCA/SVD alignment, or hand-selected basis map;
- a downstream “looks gravitational” score;
- tuning a source normalization to improve a later canary.

The solver may use linear algebra to determine an intertwiner space. It may not use a physical-output objective to choose one member of that space.

### 3.3 No silent reopening of stopped branches

A candidate already classified as requiring a representation link remains conditional unless that link is independently certified. Renaming a supplied map as “provenance,” “natural,” or “constitutive” does not make it derived.

---

## 4. Typed target representation

The frozen pre-time chain complex is

\[
C_2\xrightarrow{B_2}C_1\xrightarrow{B_1}C_0,
\qquad B_1B_2=0.
\]

The source quotient lives in the balanced source space

\[
\mathcal Q=\operatorname{im}B_1\subset C_0.
\]

The source-invisible cycle space is

\[
\mathcal Z=\ker B_1\subset C_1.
\]

v15.26 introduced the metric-free response-coordinate operator

\[
R=[B_2^T;H]
\]

and established that its restriction to the cycle space is injective in the audited torus fixture:

\[
\operatorname{rank}(RZ)=\dim\mathcal Z.
\]

To prevent a preferred homology basis from becoming physical, v15.28 will treat the target abstractly as

\[
\mathcal Y_{\rm cyc}:=\operatorname{im}(R|_{\mathcal Z})
\cong \mathcal Z.
\]

The implementation may choose an exact coordinate basis for computation, but all reported coupling-space dimensions and equivalence classes must be invariant under invertible target-basis changes.

No Euclidean inner product on \(C_1\) or \(\mathcal Y_{\rm cyc}\) is physical input to the gate.

---

## 5. Eligible source/provenance representations

A source carrier is eligible for a coupling-space calculation only if all of the following are available from frozen evidence:

1. **Typed carrier:** a finite vector/operator space \(\mathcal S\).
2. **Certified action:** a specified action \(\rho_S(g)\) of the same structural symmetry/morphism group used on the target, or a certified natural map into a carrier with that action.
3. **Gauge/equivalence data:** any source-side null/equivalence subspace that must be quotiented is explicit.
4. **Composition law:** if tensor, direct-sum, or disjoint-union composition is claimed, that composition is already defined for the source carrier.
5. **Label relationship:** source and target labels are related structurally, not by a fitted or arbitrary bijection.

If any item is missing, the candidate receives

```text
NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK
```

and no artificial embedding is introduced to continue the calculation.

The gate must include the source quotient \(\mathcal Q\) itself as a baseline control. That control is expected to demonstrate that covariance alone need not imply uniqueness, consistent with v15.27.

Archived provenance carriers such as the Genesis field or retained graph source/current are audited under the same rule. A carrier being nontrivial is not sufficient; its relation to this target representation must be earned.

---

## 6. Structural symmetry and naturality

### 6.1 Primary finite symmetry group

For a torus-native source/target pair, the primary finite group is the exact combinatorial automorphism group generated by:

- periodic translations in both lattice directions;
- the square-cell dihedral symmetries that preserve the oriented chain-complex structure, with orientation signs carried explicitly where required.

All actions are induced from cell relabelings on vertices, edges, and faces. No geometric distance is used.

For a non-torus archived carrier, only symmetries explicitly certified for that carrier may be used. The gate must not enlarge its group action by analogy.

### 6.2 Equivariance equations

For every generator \(g\), an admissible coupling must satisfy

\[
\eta\,\rho_S(g)=\rho_Y(g)\,\eta.
\]

These equations are assembled into one exact homogeneous linear system on the entries of \(\eta\).

### 6.3 Quotient consistency

If \(N_S\subset\mathcal S\) is a certified source-side gauge/equivalence subspace, then

\[
\eta(N_S)=0.
\]

This prevents v15.27’s representative-dependence failure from re-entering through a larger source carrier.

### 6.4 Neutrality

The neutral source must map to the neutral response:

\[
\eta(0)=0.
\]

For linear candidates this is automatic and remains an explicit assertion.

### 6.5 Composition constraints

Composition is imposed **only where already defined**.

If a frozen carrier has a certified disjoint-union/direct-sum law, the coupling must satisfy the corresponding block composition

\[
\eta_{A\sqcup B}(s_A\oplus s_B)
=\eta_A(s_A)\oplus\eta_B(s_B).
\]

If a tensor/composition law is not certified for a candidate, the gate reports that absence instead of inventing one.

No locality, finite propagation speed, or factorization assumption is added merely to reduce \(d_\eta\).

---

## 7. Exact coupling-space solver

### 7.1 Coordinate construction

For signed-permutation/integer chain actions, source and target representations will be built with exact integer/rational arithmetic.

An exact basis of \(\ker B_1\) is obtained by rational row reduction, not by choosing an orthonormal basis. For each target automorphism, the transformed cycle basis is re-expanded exactly in that basis to obtain \(\rho_Y(g)\).

Any target-coordinate realization using \(R\) is a verification layer only. The adjudicated dimension must agree with the abstract cycle-space computation.

### 7.2 Constraint matrix

All equivariance, quotient, and certified composition constraints are stacked into

\[
M\,\operatorname{vec}(\eta)=0.
\]

The coupling-space dimension is

\[
 d_\eta=\dim\ker M.
\]

For the finite exact cases, rank/nullity is adjudicated exactly over rationals or exact algebraic/integer data. Floating SVD may be reported as a conditioning diagnostic but cannot change the exact rank verdict.

### 7.3 Basis invariance

The implementation must apply predeclared invertible changes of source and target coordinates and confirm that \(d_\eta\) is unchanged. Individual matrix entries of \(\eta\) are not physical.

---

## 8. Gate sequence

### Gate A — Frozen representation inventory

For every candidate carrier, record:

- artifact/hash;
- carrier dimension/type;
- certified symmetry action;
- gauge/equivalence relation;
- composition law, if any;
- certified relationship to the v15.26 target labels.

No coupling is solved before this table is frozen.

### Gate B — Solver validation controls

Before any ontology candidate is adjudicated, the exact solver must pass three synthetic preregistered controls:

1. a pair of representations with \(d_\eta=0\);
2. a pair with \(d_\eta=1\);
3. a multiplicity case with \(d_\eta>1\).

It must also pass arbitrary invertible basis changes without changing those dimensions.

### Gate C — Source-quotient baseline

Compute the admissible space from the source quotient \(\mathcal Q\) to \(\mathcal Y_{\rm cyc}\) under the frozen automorphism constraints.

This is a control, not a candidate physical derivation. If it is multi-dimensional, that reproduces the v15.27 lesson in representation-theoretic form. If it unexpectedly becomes one-dimensional or zero under the complete frozen group, that result is reported without examining gravitational behavior.

### Gate D — Provenance-enhanced candidates

For each eligible archived carrier, compute \(d_\eta\) with the exact same preregistered solver and constraints.

Candidate statuses are:

```text
NO_CERTIFIED_SOURCE_TARGET_REPRESENTATION_LINK
EQUIVARIANT_COUPLING_SPACE_ZERO
EQUIVARIANT_COUPLING_UNIQUE_UP_TO_SCALE
EQUIVARIANT_COUPLING_MULTI_DIMENSIONAL
CONDITIONAL_ON_SUPPLIED_INTERTWINER
```

A supplied-intertwiner sensitivity control is mandatory where v14.04-style ambiguity applies: two inequivalent supplied links must be shown to change the coupling result or downstream source representation when they are not naturally equivalent. This is a negative control, not an allowed selector.

### Gate E — Freeze before gravity exposure

If and only if an eligible candidate gives

```text
EQUIVARIANT_COUPLING_UNIQUE_UP_TO_SCALE
```

the gate will freeze a basis-independent description of that one-dimensional subspace before computing any holonomy or gravity-like observable.

A numerical representative may be normalized for regression, for example to unit coefficient norm in a declared coordinate basis, but that normalization is explicitly nonphysical. The remaining scale is recorded as unresolved.

No gravity canary is executed inside v15.28.

---

## 9. Preregistered adjudication

The gate-level verdict is determined without downstream physics:

### Case 1 — no certified common representation

```text
PRETIME_COUPLING_BLOCKED_BY_REPRESENTATION_LINK
```

Meaning: the archive does not yet provide a typed natural bridge from the candidate provenance carrier to the cycle-response representation.

### Case 2 — all eligible coupling spaces are zero

```text
PRETIME_COUPLING_SPACE_ZERO
```

Meaning: the imposed earned symmetries/quotients forbid a nontrivial constitutive coupling in the audited class.

### Case 3 — at least one eligible candidate has dimension greater than one and none has dimension one

```text
PRETIME_COUPLING_REMAINS_UNDERDETERMINED
```

Meaning: additional physical structure is still required. No member is chosen by hand.

### Case 4 — an eligible candidate has dimension one

```text
PRETIME_COUPLING_FORM_UNIQUE_UP_TO_SCALE
```

Meaning: the frozen structural requirements select the **form** of a nontrivial source→higher-incidence response coupling. This is the only outcome that permits a later v15.29 gravity canary.

It is not itself a gravity discovery.

If multiple distinct eligible candidates each yield one-dimensional but inequivalent coupling forms, the overall verdict remains underdetermined until their source representations are naturally identified.

---

## 10. Breakthrough rule

v15.28 triggers an upstream breakthrough alert only if all of the following hold:

1. the source carrier and target relationship are certified rather than supplied ad hoc;
2. the exact admissible coupling space is one-dimensional;
3. the result survives basis changes and all frozen symmetry/quotient/composition controls;
4. the unique form was frozen before any gravity-like observable was evaluated;
5. no prohibited selector entered the solver.

The alert wording must be:

```text
THEOREM / COMPUTATION:
A pre-time source→higher-incidence coupling form is unique up to scale in the audited representation class.

INTERPRETATION:
The ontology now constrains the form of a constitutive response before pruning/time.

NOT YET CLAIMED:
gravity, Newtonian scaling, GR, a physical metric, coupling strength, or empirical validation.
```

A zero- or multi-dimensional result is important branch information but is not labeled a gravity breakthrough.

---

## 11. Implementation architecture

No implementation begins until this design is reviewed and an implementation plan is approved.

The intended code boundary is one additive package:

```text
ResearchHistory/UQCF-GEM/demos/v15.28-coupling-space/
```

with focused components:

- `representation_inventory.py` — frozen carrier/action/type inventory only;
- `coupling_solver.py` — exact intertwiner/nullspace engine independent of UQCF claims;
- `coupling_gate.py` — applies preregistered constraints and emits the audit ledger;
- `replay.py` / `viewer.html` — visualization of representation multiplicities and verdicts only, not gravity fields;
- tests for solver controls, archived candidates, claim boundaries, and presentation;
- copied/hash-pinned baseline files required for deterministic reproduction.

The solver must not import holonomy scoring, Newton/GR comparators, pruning engines, or cosmology fitting code.

### Data flow

```text
frozen artifacts
    ↓
typed representation inventory
    ↓
certified common action / quotient data
    ↓
exact linear constraint matrix M
    ↓
ker(M) and d_eta
    ↓
basis-invariant verdict
    ↓
freeze one-dimensional form if present
```

Gravity-like observables are deliberately absent from this data flow.

---

## 12. Error handling / fail-closed rules

The implementation must stop rather than infer through any of these conditions:

- missing or unhashed frozen artifact;
- source carrier with no certified action;
- target/source labels related only by a supplied arbitrary embedding;
- inconsistent group action or broken group relations;
- non-invariant claimed gauge subspace;
- composition requirement requested where no composition law is certified;
- exact-rank result disagreeing across coordinate bases;
- numerical conditioning used to change an exact rank;
- candidate requiring a metric or gravity output to become unique;
- multiple inequivalent one-dimensional candidates with no natural identification.

Every stop reason is a scientific result and must be retained in the ledger.

---

## 13. Testing and evidence

Development uses tests-first RED→GREEN discipline.

Required new tests include:

- exact synthetic `d=0`, `d=1`, and `d>1` solver controls;
- group-relation consistency for every audited representation;
- exact equivariance of every returned coupling basis vector;
- source-gauge annihilation;
- neutral-source behavior;
- basis-change invariance of `d_eta`;
- abstract-cycle versus response-coordinate agreement;
- q-only baseline control;
- supplied-intertwiner ambiguity control where applicable;
- disjoint-union/composition tests only for carriers with certified composition;
- fail-closed tests for missing representation links;
- explicit flags asserting no holonomy selector, gravity target, pruning, entropy, or physical time;
- inherited v15.11–v15.27 selected regression stack.

GitHub Actions remains the certification surface. Publication must include source, report, exact ledger, test logs, offline inspector/video if produced, provenance, and SHA-256 checked release assets. `main` remains unchanged unless separately approved.

---

## 14. What v15.28 may and may not conclude

v15.28 may conclude that an already-earned representation structure permits zero, one, or multiple constitutive coupling forms.

It may **not** conclude:

- that a nonzero coupling is gravity;
- that its normalization is Newton’s constant or any other measured constant;
- that a cycle response is spatial curvature;
- that a metric has been derived;
- that physical time exists before pruning;
- that an outcome has become actual;
- that v14.04’s missing representation link has disappeared without a certified bridge;
- that a one-dimensional mathematical intertwiner is empirically correct.

If a unique form survives, v15.29 becomes a separate preregistered gravity canary. Only then may remote response, universality, scaling, and holonomy be exposed—and none of those may retroactively alter the frozen v15.28 coupling.

---

## 15. Design acceptance criterion

This design is ready for implementation planning when the user confirms that the intended next scientific question is:

> **Classify the full gravity-blind space of natural pre-time source→higher-incidence couplings from already-earned representations, and only if the form is unique up to scale freeze it for a later gravity canary.**

No implementation is authorized by the existence of this file alone.
