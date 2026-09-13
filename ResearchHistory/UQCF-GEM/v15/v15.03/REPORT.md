# v15.03 — Graph-Site Factorization / Local-Gauge Source Lift Gate

**Status:** CLOSED / measured on branch; final exact-SHA certification pending archival binding  
**Primary outcome:** `NO_CERTIFIED_GRAPH_SITE_FACTORIZATION`  
**Scientific breakthrough:** `false`  
**Pillar 3:** `OPEN`

## Question

Can the frozen retained five-node source graph be promoted, without a new assumption, to a graph-indexed quantum tensor-factor carrier that supplies the operator-valued projective source ray needed upstream of v14.03?

The gate separated four issues that must not be conflated:

1. whether the exact retained graph already has a certified node-to-quantum-site factorization;
2. what independent local-gauge covariance permits from state-independent scalar/current source data;
3. whether admitting an already-existing quantum state as context makes a noncentral source law unique;
4. whether any genuine five-site carrier is naturally connected to the certified `C^125` compatibility parent.

## Primary result

The frozen archive contains graph-indexed quantum models and certified independent local-frame covariance, but it does **not** certify that the exact retained five-node/seven-edge source graph is a five-factor quantum carrier.

Therefore

\[
\boxed{\texttt{NO_CERTIFIED_GRAPH_SITE_FACTORIZATION}}
\]

is the primary hierarchical result.

This is not the same statement as “graph-site quantum models are impossible.” They exist in the archived stack. The missing object is the **typed identification of this exact retained source graph with nontrivial quantum subsystems**, together with a lawful carrier relation to the compatibility parent.

---

# I. THEOREMS

## 1. Five-site / `C^125` arithmetic obstruction

A genuine five-site quantum carrier requires

\[
\mathcal H_G=\bigotimes_{i=1}^{5}\mathcal H_i,
\qquad d_i=\dim\mathcal H_i\ge2.
\]

If it were literally the already-certified compatibility parent, it would require

\[
\prod_{i=1}^{5} d_i=125=5^3.
\]

No such five-tuple exists. The executable integer-factor search found zero solutions.

Hence

\[
\boxed{\texttt{FIVE_NONTRIVIAL_SITE_CARRIER_CANNOT_EQUAL_C125_PARENT}}.
\]

At least two factors in any five-factor integer decomposition of 125 would have to be one-dimensional. Such padding does not represent all five retained nodes as nontrivial quantum sites and is prohibited by the frozen gate.

This theorem prevents a graph-site carrier from being identified with the current `C^125` parent by relabeling or reshaping.

## 2. State-independent local-gauge centrality theorem

Let the retained graph/source/current data carry no internal quantum-frame action, and let

\[
F(G,s,J,\ldots)\in\mathrm{Herm}(\mathcal H_G)
\]

be a deterministic state-independent source lift. Independent local-frame naturality requires

\[
F
=
\left(\bigotimes_i U_i\right)
F
\left(\bigotimes_i U_i^\dagger\right)
\]

for every independent collection of local unitaries.

The commutant of the full product local-unitary representation is the scalar center, so

\[
\boxed{F=\lambda I}.
\]

At the v14.03 projective/PGRL level, central generators are null. Therefore

\[
\boxed{\texttt{CENTRAL_PGRL_NULL}}.
\]

This is an analytic representation-theoretic result. The numerical controls below corroborate the implementation but are not the theorem's foundation.

## 3. Edge/current structure does not evade independent local gauge

A cross-factor object such as `SWAP_ij` is invariant if the two frames are tied, but not under independent frames in general.

The deterministic control measured

- independent-frame SWAP violation: `7.806681235326519`;
- tied-frame SWAP error: `2.5121479338940403e-15`.

Thus using a SWAP/intertwiner-like operator would require extra relative-frame structure. Weakening the gauge by tying frames is not an earned repair.

---

# II. REPRODUCIBLE COMPUTATION

## 1. Exact retained source fixture

AST parsing independently recovered the same source fixture from both archived finite-network artifacts:

- nodes: `[0,1,2,3,4]`;
- edges: `[(0,1),(1,3),(0,2),(2,4),(4,3),(1,2),(0,4)]`;
- source: `[-1,0,0,+1,0]`;
- incidence rank: `4`;
- cycle dimension: `3`.

The fixture fingerprint is

`94ca2cbc711167afa22bef2ff5876c0fda9def43fc15c4318377fa629511ca4b`.

## 2. Archive/type audit

The audited archive establishes:

- v13.15: graph-indexed quantum modeling exists, but the decisive example is a **4-node path**, not this retained graph;
- v13.11: independent local-frame covariance is certified;
- v13.27 demo: an explicit **six-qubit** graph model exists, but it is a declared controlled model, not a provenance derivation;
- the retained Gate-A small-network package contains the exact five-node/seven-edge/source fixture but no quantum-factor identity statement;
- v14.04: certified natural support-link count remains zero;
- v15.01: the compatibility parent is `C^125` with `C^25` support and same-parent provenance/source class count zero;
- v15.02: the node-to-five-level basis-label shortcut is not certified.

The resulting archive classifications are

`GRAPH_INDEXED_QUANTUM_MODELS_EXIST_BUT_EXACT_FACTOR_IDENTIFICATION_UNDERIVED`

and

`NO_EXACT_GRAPH_SITE_CARRIER`.

No frozen natural graph-site-to-compatibility-parent map was found.

## 3. Deterministic centrality controls

On the supplied five-qubit theorem fixture:

- identity invariance error: `2.57310042329926e-15`;
- noncentral single-site operator independent-frame violation: `7.999999999999999`;
- SWAP independent-frame violation: `7.806681235326519`;
- SWAP tied-frame error: `2.5121479338940403e-15`.

These controls cleanly distinguish the full independent local gauge from the weaker tied-frame action.

## 4. State-dependent covariant source families

Two five-qubit product-state controls were frozen before execution:

\[
r_A=(0.15,-0.31,0.42,0.63,-0.22),
\]

\[
r_B=(0.52,-0.18,0.27,-0.47,0.36).
\]

For each local state

\[
\rho_i=\frac12(I+r_i Z),
\]

we tested only the predeclared families

\[
f(x)=1,\quad x,\quad x^2,\quad \log x.
\]

The full source operator was

\[
P_f(s,\rho)
=
\sum_i s_i\,\iota_i\!\left[f(\rho_i)-\frac{\operatorname{Tr}f(\rho_i)}2I\right].
\]

All controls were faithful. Maximum local-gauge covariance error over the tested families was

`2.9707140272854356e-16`.

Maximum positive source-scaling projective residual was

`4.3624070492076246e-16`.

The constant family centered exactly to zero.

### Projective canonicality

Control A:

- linear vs square: `3.597533769998862e-16`;
- linear vs log: `0.03264343653690659`;
- square vs log: `0.032643436536906593`.

Control B:

- linear vs square: `9.437916079723832e-17`;
- linear vs log: `0.010460821683241842`;
- square vs log: `0.010460821683241812`.

The linear/square collapse is the expected qubit functional-calculus redundancy. The independently predeclared `log` family is nevertheless a lawful, covariant, noncentral projective source class that is not the same ray.

Therefore, on the **supplied** graph-site carrier and supplied state context,

\[
\boxed{\texttt{STATE_DEPENDENT_COVARIANT_SOURCE_LIFT_NONUNIQUE}}.
\]

This is a secondary structural result, not provenance evidence.

## 5. Current control boundary

The minimum-norm current satisfies balance to

`7.325053464011603e-16`,

but remains explicitly classified

`MIN_NORM_CURRENT_CONTROL_NOT_PROVENANCE_SELECTED`.

It does not participate in source-law selection.

---

# III. INTERPRETATION

v15.03 localizes the missing source representation more sharply.

A scalar/current source on a retained graph is not enough to define a noncentral quantum operator if each quantum site has its own independent internal frame. Without state context, covariance forces the lift into the center, which is PGRL-null.

Adding the quantum state changes the situation: the state itself carries internal-frame information, so functional calculus produces perfectly lawful noncentral covariant source operators. But covariance still does not choose **which** state function is the source law. The frozen `linear` and `log` constructions already give inequivalent positive projective rays.

So the missing principle is more specific than “associate graph nodes with quantum sites.” It would have to supply, without target fitting:

1. the exact retained-node-to-quantum-site carrier identification;
2. an operator-valued source representation law using whatever quantum-frame information is legitimately available;
3. a canonical choice within the state-dependent covariant family, if state context is used;
4. an earned natural map from that graph-site representation into the existing `C^125 -> C^25` compatibility stack.

The arithmetic theorem shows item 4 cannot be solved by declaring the five-site carrier to be the current parent.

---

# IV. UNRESOLVED PHYSICAL CLAIMS

v15.03 does **not** derive:

- a certified exact retained-node-to-quantum-site factorization;
- a natural graph-site-to-`C^125` compatibility-parent map;
- Genesis/provenance to the v14.03 projective support-source ray;
- an absolute source magnitude;
- observer source calibration;
- physical stress-energy;
- a source-to-coframe/solder law;
- physical metric or spacetime;
- an absolute gravitational coupling;
- Einstein equations;
- a physical time primitive;
- Pillar 3 closure.

The primitive/pre-pruning ontology remains atemporal. Nothing in this gate uses entropy, pruning, or physical time as a pre-pruning source selector.

---

# Stop rule

Do not continue this branch by:

- choosing a preferred Pauli/internal axis;
- privileging `log rho` because PGRL uses log coordinates;
- tying local frames together;
- padding or reshaping a five-site carrier into `C^125`;
- inventing a cross-carrier isometry;
- promoting the minimum-norm current into physics;
- using pruning/entropy as a pre-pruning selector;
- using ADM, Einstein, Newtonian, gravity, cosmology, or downstream v14.03 quality as a selector.

A lawful continuation requires either newly discovered frozen representation structure or an independently motivated operator-valued source/representation principle explicitly marked **NEW ASSUMPTION** before testing.

## CI evidence before archive binding

First implementation GREEN:

- SHA `86ddb310bd49e2db936a9822c4435ca582bc6abd`
- workflow run `34740917675`
- job `103680363634`
- SUCCESS

Telemetry exposure GREEN:

- SHA `6439d1d0a9a5ef606f79c30752242042dd0b83dc`
- workflow run `34740951623`
- job `103680449109`
- SUCCESS

Final exact-SHA certification is performed after `SUMMARY.json`, this report, checker binding, and research index/status updates are frozen.
