# v15.03 — Graph-Site Factorization / Local-Gauge Source Lift Gate

**Date:** 2026-09-13  
**Series:** UQCF-GEM / Retained Atlas — v15 representation-unification audit  
**Base:** `main` at `5ba89e90b511824fb1dd03c36cc1afbf506bb0ed`  
**Branch:** `research/v15.03-graph-site-source-lift`

## 1. Purpose

v15.02 ruled out a specific shortcut: identifying the five retained source-graph nodes with the five **basis labels inside** each factor of the archived compatibility parent. All `5! = 120` node-to-basis-label identifications remained inequivalent under the earned gauge actions.

v15.03 tests a different and more ontology-native possibility:

\[
\text{retained graph node }i
\quad\longleftrightarrow\quad
\text{quantum subsystem }\mathcal H_i,
\]

rather than

\[
\text{retained graph node }i
\quad\longleftrightarrow\quad
\text{basis state }|i\rangle.
\]

The gate asks three logically separate questions:

1. Does the frozen archive already identify the retained five-node source graph with a graph-indexed quantum tensor-factor carrier?
2. If a graph-site factorization is granted, what operator-valued source lifts are permitted by independent local-unitary/frame covariance?
3. If the existing quantum state is admitted as context, does covariance select a unique projective source ray, or only a nonunique family?

A fourth compatibility check is mandatory:

4. Is any graph-site quantum carrier naturally related to the certified `C^125` compatibility parent consumed by v14.03/v15.01?

A positive graph-site source representation on a disconnected quantum carrier is not closure of the v14.03 chain.

---

## 2. Frozen claim boundary

### 2.1 Allowed frozen inputs

The gate may inspect and hash:

- `Tmp/TOE/ThePhysicsParadox/Physics101/phi lab.py`
  - five retained nodes;
  - seven directed edges;
  - balanced scalar source `s=[-1,0,0,+1,0]`;
  - incidence/cycle structure.
- `Tmp/TOE/ThePhysicsParadox/uqcf_gate_a_small_network_phi_simulation_package 2/`
  - the exact same five-node/seven-edge graph;
  - retained edge features such as ordered transfer distance, accessibility support, provenance compatibility, and active support;
  - finite source/current identifiability controls.
- `ResearchHistory/UQCF-GEM/v13/v13.15/`
  - prior exact use of graph vertices as quantum sites in ETL/QMAR controls;
  - site-local source covariance/locality results;
  - conditional commuting-Markov locality theorem.
- `ResearchHistory/UQCF-GEM/v13/v13.11/`
  - independent local-frame covariance of the QMAR response stack.
- `ResearchHistory/UQCF-GEM/demos/v13.27-gravity-progress/`
  - graph-indexed finite quantum tensor factors and local Pauli source controls;
  - explicitly a demonstration/controlled correspondence, not a provenance derivation.
- `Tmp/TOE/UQCF_Quantum_Compatibility_Lab/`
  - the certified compatibility parent
    \[
    \mathcal H_Q=\mathbb C^5_A\otimes\mathbb C^5_{B_1}\otimes\mathbb C^5_{B_2}\cong\mathbb C^{125};
    \]
  - support isometry `L : C^25 -> C^125`.
- v14.03, v14.04, v15.01, and v15.02 frozen gate packages.

### 2.2 Prohibited selectors

The gate must not select a source lift using:

- a preferred Pauli axis or internal basis chosen by hand;
- a preferred node-to-basis-label bijection;
- a Hamiltonian chosen because it yields desired downstream behavior;
- Einstein/ADM residuals;
- Newtonian/gravity targets;
- physical time or entropy as a pre-pruning source selector;
- the retained-branch-identity/pruning toy program as a pre-pruning selector;
- PCA/SVD/random-isometry alignment between carriers;
- downstream v14.02/v14.03 boundary or dual-ray quality;
- fitting to a desired source/current response.

### 2.3 Projective equivalence

All source selection remains projective as earned in v14.03:

\[
P\sim aP+bI,\qquad a>0.
\]

No absolute source magnitude is adjudicated here.

---

## 3. Typed structures

### 3.1 Retained source side

The frozen finite source fixture is

\[
G_{\rm src}=(V,E),\qquad |V|=5,\ |E|=7,
\]

with balanced source

\[
s\in\mathbb R^5,\qquad \mathbf 1^Ts=0,
\]

and retained current

\[
J\in\mathbb R^7,\qquad BJ=s.
\]

The source/current package carries node/edge incidence and graph covariance, but no certified internal quantum operator direction.

### 3.2 Generic graph-site quantum carrier

A graph-site factorization has the typed form

\[
\mathcal H_G=\bigotimes_{i\in V}\mathcal H_i.
\]

Independent local frame changes act as

\[
U_G=\bigotimes_i U_i.
\]

A Hermitian parent source must transform as

\[
P\mapsto U_G P U_G^\dagger.
\]

For a **genuine five-site quantum carrier**, every retained node must correspond to a nontrivial quantum subsystem:

\[
d_i=\dim\mathcal H_i\ge2\qquad(i=1,\ldots,5).
\]

### 3.3 Certified compatibility carrier

The already-certified v15.01 parent is

\[
\mathcal H_Q
=\mathbb C^5_A\otimes\mathbb C^5_{B_1}\otimes\mathbb C^5_{B_2}
\cong\mathbb C^{125},
\]

with support compression

\[
C_L(A)=L^\dagger A L.
\]

This is a three-factor parent with five-dimensional **internal basis labels**. It must not be silently reinterpreted as a five-site graph.

### 3.4 Exact five-site / `C^125` factorization obstruction

A genuine five-site carrier that were literally equal to the certified parent would require integers

\[
d_1,d_2,d_3,d_4,d_5\ge2
\]

with

\[
\prod_{i=1}^5 d_i=125=5^3.
\]

This is impossible. The integer `125` contains only three prime factors counting multiplicity. Any five-factor decomposition of `125` therefore contains at least two factors of dimension `1`, e.g.

\[
125=5\cdot5\cdot5\cdot1\cdot1,
\]

which does **not** represent all five retained nodes as nontrivial quantum sites.

Hence:

\[
\boxed{
\text{five nontrivial graph-site factors cannot literally equal the certified }\mathbb C^{125}\text{ parent}.
}
\]

This is an exact arithmetic/type obstruction, not a numerical result.

Therefore any genuine five-site source carrier must be a distinct representation and must have an independently earned natural map into the certified compatibility parent/support before it can close the v14.03 upstream source problem.

---

## 4. Gate A — Archive graph-site factorization audit

The executable audit must answer:

1. Does any frozen artifact identify the exact retained graph
   `[(0,1),(1,3),(0,2),(2,4),(4,3),(1,2),(0,4)]`
   with five nontrivial quantum tensor factors carrying the same node identities?
2. Does that identification survive as a typed structural statement rather than a plotting convention or demonstration choice?
3. If a graph-indexed quantum model exists on a different graph or different node count, record it as evidence that graph-site quantum modeling is available in the ontology, but **not** as the required exact identification.
4. If an exact five-site carrier exists, determine whether a frozen natural map from that carrier into the certified `C^125` compatibility parent is already present.

Required factorization statuses:

- `EXACT_GRAPH_SITE_FACTORIZATION_CERTIFIED`
- `GRAPH_INDEXED_QUANTUM_MODELS_EXIST_BUT_EXACT_FACTOR_IDENTIFICATION_UNDERIVED`
- `NO_GRAPH_INDEXED_QUANTUM_CARRIER_FOUND`

Required carrier statuses:

- `FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT`
- `NATURAL_MAP_TO_COMPATIBILITY_PARENT_CERTIFIED`
- `GRAPH_SITE_CARRIER_DISTINCT_FROM_COMPATIBILITY_PARENT`
- `NO_EXACT_GRAPH_SITE_CARRIER`

The exact dimension theorem forces the first status whenever the proposed exact graph-site carrier has five nontrivial factors and is compared with the certified `C^125` parent. No dimensional padding, trivial-site insertion, reshaping, or hidden factor suppression may turn one status into another.

---

## 5. Gate B — State-independent local-gauge centrality theorem

Assume a graph-site factorization is supplied, but the retained source data `(G,s,J,...)` themselves carry no internal quantum-frame action.

Let

\[
F(G,s,J,\ldots)\in\mathrm{Herm}(\mathcal H_G)
\]

be a deterministic source lift that does **not** use the current quantum state.

Independent local-frame naturality requires

\[
F(G,s,J,\ldots)
=
\Big(\bigotimes_iU_i\Big)
F(G,s,J,\ldots)
\Big(\bigotimes_iU_i^\dagger\Big)
\]

for all independent local unitaries `U_i`, because the retained scalar/current input is unchanged by those quantum-frame rotations.

The commutant of the full product local-unitary representation on
\(
\bigotimes_i\mathcal H_i
\)
is the center, hence

\[
\boxed{F(G,s,J,\ldots)=\lambda I}.
\]

At the v14.03 projective/PGRL level this is null:

\[
P\propto I
\Longrightarrow
\dot X_P=0.
\]

### 5.1 Edge/current loophole control

The audit must explicitly test and explain why edge/current structure does not evade the theorem by producing objects such as a SWAP/interchange operator between factors.

Under **independent** local frames,

\[
(U_i\otimes U_j)\,\mathrm{SWAP}_{ij}\,(U_i\otimes U_j)^\dagger
\neq \mathrm{SWAP}_{ij}
\]

generically unless the frames are tied together. Therefore choosing a cross-factor operator requires extra relative-frame/intertwiner information.

This is precisely the kind of missing representation data v14.04 isolated.

### 5.2 Deterministic controls

Use exact or deterministic product-unitary controls to verify:

- central operators remain invariant;
- predeclared noncentral local operators fail invariance under independent local rotations;
- tying all local frames together can enlarge the commutant, but that is a weaker gauge and is **not** the frozen independent-frame covariance used for adjudication.

The analytic theorem, not sampling, is primary.

---

## 6. Gate C — State-dependent covariant source families

The theorem above does not forbid a source lift that uses an already-existing quantum state as context.

If

\[
\rho\mapsto U_G\rho U_G^\dagger,
\]

then local reductions transform as

\[
\rho_i\mapsto U_i\rho_iU_i^\dagger.
\]

Therefore a functional-calculus family is automatically local-frame covariant:

\[
P_f(s,\rho)
=
\sum_i s_i\,\iota_i\!\left[
 f(\rho_i)
-\frac{\operatorname{Tr}f(\rho_i)}{d_i}I_i
\right].
\]

Here `iota_i` embeds a site operator into the full tensor product.

### 6.1 Frozen candidate functions

Predeclare before execution:

\[
f_1(x)=x,\qquad
f_2(x)=x^2,\qquad
f_3(x)=\log x.
\]

`log` is evaluated only for faithful local states.

Also include:

- constant `f(x)=1` as a null/central control;
- positive source scaling controls;
- independent local-unitary covariance controls.

No candidate may be chosen after observing any downstream boundary/dual behavior.

### 6.2 Deterministic supplied five-site state controls

To prevent tuning after execution, use exactly two predeclared faithful five-qubit product-state controls. These are **sufficiency/covariance fixtures only**, not provenance physics.

For control `A`, use signed Bloch radii

```text
r_A = [ 0.15, -0.31,  0.42,  0.63, -0.22 ]
```

For control `B`, use

```text
r_B = [ 0.52, -0.18,  0.27, -0.47,  0.36 ]
```

The reproducible coordinate representative is

\[
\rho_i^{(c)}=\frac12(I+r_i^{(c)}Z),
\]

so each local spectrum is

\[
\left(\frac{1+r_i^{(c)}}2,\frac{1-r_i^{(c)}}2\right)
\]

with `|r_i|<1`, hence every local state is faithful. The `Z` basis is only a supplied coordinate representative. Independent deterministic local unitaries must be applied to verify covariance; no physical axis is inferred.

Both controls are labeled:

`SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION`.

The controls are frozen before execution and may not be changed because of projective-residual outcomes.

### 6.3 Canonicality question

For the same supplied graph-site factorization, same state, and same retained source vector, compute the projective residuals between the centered rays

\[
[P_{f_a}]_+,
\qquad
[P_{f_b}]_+.
\]

If at least two predeclared lawful covariant families are noncentral and projectively inequivalent, covariance plus the state does not select a unique source law.

That result is

\[
\boxed{
\text{state context makes noncentral lifts possible}
\quad\text{but does not make them canonical}.
}
\]

### 6.4 Qubit functional redundancy control

For a single qubit, any analytic functional calculus `f(rho_i)` is diagonal in the same eigenbasis as `rho_i`; after trace-centering it therefore lies on the same local Bloch direction.

In particular, `f(x)=x^2` is included partly as a redundancy/control. This local collinearity does **not** imply the full embedded sources are projectively equivalent, because the proportionality coefficient can depend on the local spectrum and therefore vary by site.

The audit must compare the **full embedded source rays**. The most informative predeclared contrast is expected to be `x` versus `log x` on controls with unequal local spectra, but that expectation is not an adjudication rule.

No candidate may be dropped because it proves redundant, and no new candidate may be added because the frozen candidates happen to coincide.

### 6.5 Current-based pair lift boundary

A pair-state/current construction such as

\[
P_f^{(J)}
=
\sum_{e=(i,j)}J_e\,\iota_{ij}\!\left[
 f(\rho_{ij})-
 \frac{\operatorname{Tr}f(\rho_{ij})}{d_id_j}I_{ij}
\right]
\]

may be included only as structural/control evidence.

It may participate in scientific adjudication **only if** the current being used is a previously certified selected current for the exact same retained realization and carrier. The Gate-A minimum-norm current is a control, not a provenance-selected current. v13.25 current selection remains conditional on the response rank/stability gate.

Therefore no min-norm/Hodge/current convenience choice may be promoted into a source law in v15.03.

---

## 7. Gate D — Compatibility-parent relevance

Even a successful graph-site source representation does not feed v14.03 unless the carrier relation to the certified compatibility parent is earned.

The exact dimension theorem already proves that a genuine five-nontrivial-site tensor product cannot literally be the current `C^125` parent.

The gate must therefore distinguish:

```text
retained graph source
    -> graph-site quantum source on H_G
```

from

```text
retained graph source
    -> source on certified H_Q = C^125
    -> L^dagger(.)L
    -> [P]_+ consumed by v14.03.
```

For a genuine five-site carrier, the only lawful route to the second chain is an already-earned natural cross-carrier representation map. If no such map exists, record a carrier mismatch and stop. Do not create an intertwiner to make the test succeed.

---

## 8. Positive controls

Positive controls are sufficiency tests only and cannot adjudicate provenance derivation.

### 8.1 Supplied graph-site factorization control

The two deterministic five-qubit product-state controls from §6.2 are the only primary supplied graph-site fixtures for the state-dependent family audit.

They are labeled:

`SUPPLIED_GRAPH_SITE_FACTORIZATION_NOT_PROVENANCE_DERIVATION`.

No output from these fixtures can establish that the archive earns the factorization.

### 8.2 Supplied carrier map control

If useful, an explicit isometry/intertwiner from a graph-site control carrier into the compatibility parent may demonstrate downstream sufficiency, but must be labeled:

`SUPPLIED_CARRIER_MAP_NOT_DERIVED`.

Different supplied maps should be expected to reproduce the v14.04 ambiguity unless extra structure fixes them.

This control cannot participate in the primary adjudication.

---

## 9. Primary outcome taxonomy

The gate uses a hierarchical outcome.

### 9.1 Positive closure

`GRAPH_SITE_LOCAL_GAUGE_INDUCES_SUPPORT_SOURCE_RAY`

Requires all of:

1. exact retained-node -> quantum-site factorization is already certified;
2. an already-certified natural map from that genuine five-site carrier into the certified `C^125` compatibility parent/support exists;
3. the source lift is noncentral;
4. independent local-gauge covariance holds;
5. no inequivalent equally lawful source-lift family survives.

The literal-same-parent route is excluded by the five-site/125D dimension theorem.

This positive outcome would be an architectural breakthrough.

### 9.2 Archive factorization failure

`NO_CERTIFIED_GRAPH_SITE_FACTORIZATION`

The archive contains graph-indexed quantum models, but not a certified identity between the exact retained source graph and the five quantum tensor factors required for this branch.

### 9.3 Carrier mismatch

`GRAPH_SITE_CARRIER_NOT_COMPATIBILITY_PARENT`

A lawful graph-site quantum source carrier exists, but the exact theorem shows it cannot literally be the certified `C^125` parent, and no natural cross-carrier map is earned.

### 9.4 Gauge centrality stop

`STATE_INDEPENDENT_GRAPH_SOURCE_CENTRAL_PGRL_NULL`

A graph-site identification is available or supplied, but retained scalar/current data alone carry no internal quantum direction; independent local-frame covariance forces the state-independent source lift into the center.

### 9.5 State-dependent nonuniqueness

`STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE`

Using the existing quantum state allows noncentral covariant source operators, but multiple predeclared target-blind families produce projectively inequivalent source rays.

### 9.6 Numerical unresolved

`UNRESOLVED_GRAPH_SITE_SOURCE_LIFT_AUDIT`

Reserved only for genuine numerical failure after exact typing/theorem checks, not for scientific nonuniqueness.

---

## 10. Expected scientific interpretation

The likely hierarchy, to be tested rather than assumed, is:

```text
retained graph nodes
    -> graph-site identification may be more natural than basis-label identification
    -> BUT exact retained graph -> quantum factor identity may still be underived
    -> any genuine five-site carrier is provably distinct from the C^125 compatibility parent
    -> scalar/current data alone have no internal quantum direction
       -> independent local gauge forces central/null state-independent lift
    -> adding state context creates lawful noncentral covariant lifts
       -> multiple functional-calculus lifts may remain inequivalent
    -> a separately earned natural cross-carrier map is still required to reach v14.03
```

A negative result would localize the missing principle more sharply as an

**operator-valued source representation law with quantum-frame content plus a natural cross-carrier map into the certified compatibility parent**, not merely a node-label correspondence.

---

## 11. Breakthrough criterion

Set

`scientific_breakthrough = true`

only if the frozen archive itself supplies a target-blind, local-gauge-covariant, noncentral source representation on an earned exact graph-site carrier **and** an earned natural map into the certified compatibility parent/support, uniquely up to the already-earned projective equivalence.

A new no-go, centrality theorem, carrier mismatch, arithmetic factorization obstruction, or nonuniqueness localization is scientifically important but not a broad breakthrough.

---

## 12. Preserved boundaries

Regardless of v15.03 outcome:

- v13.28 absolute source->geometry coupling obstruction remains in force;
- v14.01 source->higher-incidence nonuniqueness remains in force;
- v14.02 canonical local dual ray remains conditional on a supplied boundary point;
- v14.03 supplied `[P]_+ -> hidden tangent -> X_* -> [g]` remains certified conditional;
- v14.04 representation-link obstruction remains in force;
- v15.01 compatibility-parent/support compression remains exact;
- v15.02 basis-label shared-carrier shortcut remains closed;
- Pillar 3 remains OPEN unless an independent later correspondence gate closes it.

No stress-energy tensor, physical metric/coframe/spacetime, absolute gravitational coupling, Einstein equation, or physical time primitive is derived here.

---

## 13. Stop rule

If v15.03 does not derive the source representation, stop.

Do not continue by:

- choosing a Pauli axis;
- choosing `f(x)=log x` merely because PGRL uses log-density coordinates;
- selecting the candidate with the best v14.03 boundary/dual behavior;
- tying local frames together to enlarge the commutant unless such tying is independently earned;
- declaring a graph-site control carrier to be the compatibility parent;
- padding with one-dimensional sites to evade the `125=5^3` obstruction;
- inventing a cross-carrier isometry;
- using a min-norm/Hodge current as though it were provenance-selected;
- importing pruning/entropy/lineage ordering as a pre-pruning source selector;
- using ADM/Einstein/gravity residuals.

Continuation after a negative result requires either:

1. newly discovered frozen cross-carrier representation structure; or
2. an independently motivated operator-valued source principle explicitly labeled **NEW ASSUMPTION** and approved before testing.
