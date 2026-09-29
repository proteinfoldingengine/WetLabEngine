# v16.31 — Global retained-component factorization

Read with PROOFS.md G1–G8, PREREGISTRATION.md and PUBLICATION_EVIDENCE.json. The mathematical assertions have explicit assumptions and arguments; enumeration audits the implementation. Scientific execution SHA `cba4eed8fa73340efb7e81dc522a62ae2c07d51d` is distinct from subsequent documentation and durable publication.

| Required question | Adjudicated answer |
|---|---|
| Which retained operation is now closed? | The existing local-count profile on the ENTIRE finite same-union retained endpoint interval has a canonical parent-local, normalized component factorization. G1–G5. This extends the earlier single-cube argument without treating illegal states as legal. |
| What happens to the earlier obstruction? | Actual nonadditive dependence remains inside connected components. A retained three-event example has nonzero third-order coefficient -1. Nothing here erases the earlier source/response obstruction or identifies it with these integer coefficients. |
| Is any new splitting chosen? | No. The prerequisite ideal P_v and all local cube representatives are derived from actual retained ancestry. Component functions are uniquely determined by the existing tau values and normalization g_C(empty)=0. |
| Can components be combined freely? | Their FUNCTION VALUES reconstruct every legal history. Their candidate STATES are not necessarily freely combinable: predecessor constraints remain. A nonconstant three-state/four-candidate counterexample is proved in G6. |
| What genuinely passed code? | 268 tests; independent reconstruction of all 27,399 original endpoint refinements, 234,116 state occurrences, 376,568 complete legal paths, 295,810 diamonds and 226,488 local coefficients, plus the complete transported copy. All graph, cube, factor and profile identities were checked. |
| What remains open? | Physical source attainability, selection of a physical response law, and the operational quantum bridge. No Cartesian physical subsystem structure, metric, curvature, time law or efficient general algorithm is derived. |

## 1. Why the cube result now reaches every legal history

For fixed indexed initial/final retained views Y,Z, let E be removed (view,node) events. Descendants must be removed before ancestors within a view. A reachable deleted set S is an ideal of this order.

Let E_v contain the events at children of vertex v. These events form an antichain: within one view the nodes are siblings, and across views there is no ancestor precedence. Define

    P_v = union of strict predecessor sets of events in E_v.

P_v is an ideal, is disjoint from E_v, and enables every E_v event. Therefore **P_v union A is a legal retained state for every A subset E_v**. These are actual retained representatives, not an extension of the function to invented configurations.

Define f_v(A)=tau_v(P_v union A). Since the child-incidence family at v depends only on deleted children of v,

    tau_v(S)=f_v(S intersect E_v)

for every reachable history S. This is the missing step between .30's Boolean-cube factorization and a statement about full retained histories. The proof supplies both admissibility of all local arguments and equality to all other actual contexts.

## 2. Exact normalized factorization

Compute the integer inclusion-exclusion coefficients

    mu_v(B)=sum_{A subset B} (-1)^(|B|-|A|) f_v(A).

Two events are joined when their second mixed difference is nonzero at SOME background. This is an all-background definition. G4 proves it is equivalent to a nonzero coefficient whose support contains that pair.

Every nonzero coefficient support lies in one connected component. For each component C, set

    g_C(A)=f_v(A)-f_v(empty),  A subset C,

with the other E_v coordinates absent. All these values have actual retained lifts. Then for **every reachable S**,

    tau_v(S)=tau_v(empty)+sum_{C component of G_v} g_C(S intersect C).

The component functions are uniquely determined once g_C(empty)=0 is required. Any additive partition of these parent-local EVENT LABELS must keep the ends of each actual nonzero mixed-difference edge together, so it coarsens the connected-component partition. Isolated inactive events give zero factors. This is not a uniqueness statement about physical subsystems.

The vector profile is assembled coordinate by coordinate. The scalar h=max(1,max tau_v) is NOT claimed additive; all .29 maximum-only and masked effects remain valid.

## 3. Two boundaries that prevent overinterpretation

### Factorization of values is not Cartesian independence of states

Use X=(-1,0,0,1), initial views ({0,1,2,3},{0,1,3}) and final views ({0,2},{0,1,3}). There are two removed events: deleting node3 from view0, then node1 from view0. Each affects a different parent. Their interaction graph has no edge, and the local functions factor, with a nonzero root contribution.

But their candidate two-bit product has FOUR combinations while only THREE are legal. Deleting node1 while retaining its descendant3 in the same view is forbidden. Order constraints survive the function decomposition.

This distinction occurred in **2,535** of the original endpoint cases. This count concerns event-coordinate candidate products, not state-space dimension or physical entanglement.

### Higher-order dependence can remain within a component

On a root with three children, retain a full view plus the three singleton-child views. Prune only the full view to the root. The local function is

    f(A)=min(|A|+1,3).

Its third-order coefficient is -1. Every pair has zero mixed difference at the empty background but a nonzero difference when the third event is present. The all-background graph is connected.

A synthetic x1*x2*x3 checker has the same baseline-versus-all-background distinction. Thus .30's suggestion of a pure cubic invisible to ALL pairwise backgrounds was incorrect. A cubic can be invisible to the initial background only. The new tests explicitly reject a graph built only from baseline squares.

The full original audit contains **4,692 nonzero coefficients of order at least three**, in **3,016 endpoint cases**. Orders three, four and five contribute 3,188, 1,190 and 314 respectively, computed from the archived raw coefficients. They all stay inside one graph component. These are mathematical coefficients, not new physical many-body interactions.

A further five-vertex, six-view control has two genuinely nonzero same-parent components. Its local function is 2+OR(x1,x2)+OR(x3,x4). Each normalized factor has values [0,1,1,1]. This is a separate admitted control in test_review.py, not part of the exhaustive three-view five-vertex domain.

## 4. Exact bounded coverage

The frozen universe contains all rooted unordered shapes through four vertices with 1–4 distinct initial views and all shapes with five vertices with 1–3 distinct initial views. Every indexed final subview family with the same union and zero through five removed events is included. Final views can repeat. Cases are not filtered by outcome.

| Original-coordinate coverage | Count |
|---|---:|
| Rooted shapes through five vertices | 17 |
| Complete endpoint refinements | 27,399 |
| Actual reachable state occurrences | 234,116 |
| Complete legal deletion paths independently reconstructed | 376,568 |
| Enabled-pair diamond occurrences | 295,810 |
| Local truth-table entries / Mobius coefficients | 226,488 |
| Graph edges, counted per endpoint | 17,958 |
| Component occurrences | 60,725 |
| Components with nonzero normalized function | 14,874 |
| Cases with non-Cartesian event-state domain | 2,535 |
| Cases with a nonzero coefficient of order at least three | 3,016 |

There are 4,397 cases through four vertices and 23,002 at five vertices. The complete transformed copy reverses nonroot labels, indexed views and storage; the verifier checks actual transported states, prerequisite cubes, coefficients, graphs and component values. Copies are equivalence controls, not independent observations.

Raw certificates preserve every endpoint, event, predecessor mask, ideal profile, parent cube, coefficient, normalized component and edge witness: **34,246,257 uncompressed bytes**, losslessly compressed to **467,032 bytes**. Raw SHA-256:

`e95f9a46ca009c8f2ecf57148ae545b1c2b0f579ff7d236d253161b56bdc40f5`

The producer uses ancestor-first shape arrays, ideal masks, subset-union dynamic programming and an in-place subset transform. The independent verifier imports neither the producer nor any inherited adjudicator. It reconstructs shape coverage from Prufer trees, enumerates all legal deletion permutations, directly checks view-subfamily minima, computes coefficients by inclusion-exclusion, derives graphs from every global reachable diamond and checks the reconstruction everywhere. No fixed classification or count is accepted as its own evidence.

## 5. RED, GREEN and evidence correction

The identical mandatory document contract fails all three tests against the historical .30 verifier: missing sections, invented summaries and untyped empty-edge records were accepted. The new verifier rejects them. EVIDENCE_STATUS.md preserves the distinction between earlier producer computations and independently verified claims; .30's original files are unchanged.

| Role | Run | Execution SHA |
|---|---|---|
| Legacy contract RED plus new-module wiring RED | 36645517234 | fdeaf3294973e3fd8624795131b90433b54e5a6e |
| Provisional complete GREEN, before added review tests | 36645988251 | d54387c24491e47f742b057a8b5740806a3131fb |
| New verifier representation-boundary RED | 36646155826 | 61613616b8b7d78ffebfd3b75c3944662d18a2ba |
| Corrected scientific GREEN | 36646349715 | cba4eed8fa73340efb7e81dc522a62ae2c07d51d |

The review RED exposed a genuine defect: the verifier rejected a valid final retained subset when only its storage order changed. Three of the four review tests passed; the fourth raised ValueError at a literal tuple comparison. Replacing only that comparison with indexed set equality fixed the representation boundary. The raw scientific certificates, production summary, verification summary, examples and original 28-test output remained byte-identical to the provisional GREEN.

Final GREEN job **109670115263**, attempt **1**, passed **268 tests**: 35 current tests (28 core, three contract, four review) and 233 inherited retained-research tests. All 20 ordinary campaign commands returned zero. The old verifier's three expected failures are replayed and recorded separately, never counted among these passes. Keeping inherited regressions passing does not retroactively certify every older scientific claim.

Eleven named corrupted-case rejections plus coverage and review controls reject invented profiles, invalid types, incorrect predecessors or prerequisite cubes, missing states/local tables/edges/witnesses, incorrect coefficients or factors, false Cartesian claims, foreign provenance and incomplete or falsely relabeled enumeration. Valid identity, nonzero constrained chains, higher-order retained controls, reordered records and transported inputs pass.

Python 3.11.16; SymPy1.13.3/mpmath1.3.0 only for inherited tests. Primary computation uses the standard library. Original final GREEN ZIP artifact **11068762102**, 511,086 bytes, SHA-256 `d0ee376c6c2f7528cf4227e609fdfdf6a380d5e460fd773e0b6063e374c0b8cb`. Downloaded ZIP checksum, CRC and all 34 listed member checksums were verified. Source hashes and execution receipts distinguish science from later publication. Exact fresh-publication provenance is recorded in PUBLICATION_EVIDENCE.json.

## 6. Limits and review

Self-review with an algorithmically independent verifier, not independently authored review or proof-assistant formalization. The theorem covers arbitrary finite admitted endpoints; explicit implementations have declared resource guards (producer12/verifier8 events), and exhaustive publication is limited to five events and the frozen view limits.

No independence of physical subsystems, source attainability, response selection, Hilbert-space factorization, temporal coordinate, coupling or geometry is inferred. This campaign closes the reconstruction of an existing LOCAL CONSISTENCY FUNCTION over actual legal retained histories while preserving their order constraints.

**Time is pruning / ordered recoverability update.**
