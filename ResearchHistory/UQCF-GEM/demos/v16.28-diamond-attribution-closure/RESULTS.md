# v16.28 — Exact diamond criterion for event attribution

This continues completed v16.27 without altering its objects or historical results. Read PROOFS.md D1–D7, the preregistration and PUBLICATION_EVIDENCE.json together. The scientific execution is distinct from the subsequent documentation/publication commit.

| Required question | Adjudicated answer |
|---|---|
| Which retained operation is now classified? | Actual per-event increment attribution on any fixed finite same-union retained refinement. It is path-independent exactly when all reachable commuting-deletion diamonds have zero mixed difference; equivalently the existing consistency-order function is additive in uniquely determined event coefficients, or modular on the event-ideal lattice. D1–D5. |
| What does the .27 obstruction become? | Every attribution-dependent endpoint contains a nonzero four-state diamond, which constructs two full legal paths with differing event increments and equal totals. The .27 counterexample remains valid; its diamond has value -1. D2–D3,D6. |
| Is a splitting or new response carrier assumed? | No. Coefficients, when they exist, are actual increments evaluated after the strict predecessors of each event. They are not fitted allocations. Source/response carriers from earlier work are not identified with these integer quantities. |
| Can attribution be compared across orders? | Yes, by the same event identities and four actual retained states. The sign measures a change in event attribution when another enabled event is deleted first. It is NOT oriented circulation, holonomy, curvature or failure of pruning composition. |
| What genuinely passed code? | 198 tests, complete reconstruction of all 3,486 endpoint refinements, 34,562 reachable states, 45,488 diamonds and 56,498 full legal paths in the original bounded universe, plus the complete relabeled/storage-reversed copy. All diamond, path-attribution, additive and modular classifications agree. |
| What remains open? | Physical realization of the formal source cone; selection of a physical response law; the operational quantum bridge; simpler structural/computational criteria beyond enumerating reachable states. No physical geometry or time law follows. |

## 1. The exact equivalence

Fix actual initial and final indexed retained views Y and Z with the same union. Let E be the removed (view,node) incidences, ordered by within-view descendant-before-ancestor precedence. A reachable deleted set S is exactly an order ideal of E. Define F(S)=h of the current remaining cover.

For distinct enabled e,f define

    D(S;e,f)=F(S union {e,f})-F(S union {e})-F(S union {f})+F(S).

The following four conditions are equivalent for EVERY finite admissible endpoint interval:

1. Every removed event receives the same ACTUAL increment on every legal complete deletion order.
2. D(S;e,f)=0 for every reachable enabled pair.
3. There are unique actual event coefficients w_e satisfying F(S)=F(empty)+sum_{e in S}w_e on every reachable S.
4. F(A)+F(B)=F(A union B)+F(A intersection B) for every two reachable ideals A,B.

When the coefficients exist,

    w_e=F(Pred(e) union {e})-F(Pred(e)),

where Pred(e) is the strict-predecessor ideal. For the inherited h these coefficients are in {0,1}. This is a reconstruction from earned data, not an added response law or a preferred average over paths.

The direct argument is in D4: every enabling context of e extends Pred(e) by events incomparable with e. A zero diamond says such an addition does not change e's marginal. Induction makes the marginal constant in every legal context; telescoping then gives the additive formula. The modular identity implies each diamond vanishes by taking A=Se and B=Sf. Conversely any nonzero diamond extends to two full legal paths with a common prefix and suffix and only e,f swapped.

This supplies the general characterization left open by .27, not merely another witness. The ordinary order-ideal/valuation mathematics is background rather than a claim of novel abstract mathematics.

## 2. Positive closure is not restricted to zero response

Of the 3,486 original endpoints, **2,395** admit order-independent actual event coefficients. Among these, **1,302** have at least one coefficient equal to one; the other **1,093** have a constant h on the whole interval. Thus the positive side is not just a vacuous all-zero result.

The remaining **1,091** endpoints are attribution-dependent, and each has a nonzero diamond and an explicit pair of legal swapped paths. These independently reproduce .27's classifications through a different criterion.

The weights are canonical only within the stated endpoint interval. A change of initial/final refinement can change an event's admissible contexts and its coefficient. No global context-free weight is asserted.

## 3. Both signs occur, without a nonzero loop total

The .27 example on a root with two children has four values 1,2,2,2 and hence D=-1. With two initial full views pruned respectively to opposite one-child views, the four values are 1,1,1,2, giving D=+1. Repeated INITIAL views in the latter are an explicit separate control, not silently added to the primary distinct-initial-view enumeration.

Both signs also occur in the original primary universe: **3,344 negative**, **1,868 positive**, and **40,276 zero** diamonds. Each value is reconstructed from actual child-cover minima. The atomic bound limits D to -1,0,1.

A nonzero mixed difference does NOT mean the sum around a closed state cycle is nonzero. For all four-state diamonds, the two paths have equal total F(Sef)-F(S). The reassignment between their two events is equal and opposite. Consequently D is neither a geometric curvature nor a new noncommutativity of the retained pruning maps.

A chain-ordered control with events (0,1),(0,3) has unique coefficients [1,0] and one legal path. Identity and single-event controls are likewise accepted. These establish the positive boundaries without selecting them as the outcome of the full audit.

## 4. Complete bounded verification

The input parent archive is the completed .27 raw certificate, SHA-256 `1397e6d798c73126fc547afffb4bb7f681645bd83665af9b7ae6a66e472c866d`. The producer uses only its actual endpoint descriptions; the old path classifications do not determine the new verdict.

The producer enumerates predecessor-closed event masks and uses subset-union dynamic programming for child covers. The verifier imports no producer or inherited adjudicator. It reconstructs shapes by Prüfer sequences, legal endpoints independently, all event permutations filtered by the proved precedence relation, and h by exhaustive view subfamilies. It then evaluates all ideal-pair modular identities and actual complete-path event maps, rather than assuming the proposed diamond equivalence.

| Original-coordinate coverage | Count |
|---|---:|
| Rooted unordered tree shapes, at most four vertices | 8 |
| Same-union endpoint refinements | 3,486 |
| Reachable state occurrences | 34,562 |
| Enabled-pair diamonds | 45,488 |
| Zero / negative / positive diamonds | 40,276 / 3,344 / 1,868 |
| Complete legal deletion paths reconstructed | 56,498 |
| Distinct unordered ideal-pair modular checks | 250,666 |
| Attribution-independent endpoints | 2,395 |
| Independent endpoints with nonzero actual coefficient | 1,302 |
| Attribution-dependent endpoints | 1,091 |

The universe is .27's exact frozen one: at most four distinct initial views; final indexed views may repeat; two through five removed incidences. The entire universe is repeated under the specified root-preserving relabeling, indexed-view reversal and vertex-storage reversal. Every transported state, diamond and existing coefficient is checked. Copies are equivalence controls, not independent physical observations.

Complete raw certificates contain **3,527,777 bytes**, compressed losslessly to **57,956 bytes**. Raw SHA-256: `daedbb1ac332aa8c8058700b9f3a6b0eaa2a9d0a3341918b42a6b0495ba94df4`. All states, event identities, predecessor relations, diamonds, positive coefficients and negative swapped-path witnesses are included. All complete paths are additionally available in the hash-bound parent .27 archive and are independently reconstructed for comparison.

## 5. Rejecting checks and failure history

All **28 new tests** and **170 inherited retained-research tests** passed: **198 total**. Fourteen named corrupt-certificate rejection reasons are recorded, with additional coverage/domain controls. The suite rejects wrong mixed differences, wrong state values, Boolean-for-integer substitutions, missing states/diamonds/endpoints/shapes, foreign origins, invented weights, false independent labels, invalid witnesses and false relabelings. Correct reordered records, an admissible positive-sign counterexample and genuine independent intervals pass. In particular a wrong coefficient vector with the same endpoint sum is rejected: telescoping alone does not certify event attribution.

Run **36628336757** is wiring RED, not mathematical verification: all 28 tests failed because implementations were absent. The first implementation run **36628829369** passed 27 tests but correctly rejected my purported positive relabeling fixture because it changed the final union. The fixture—not the validator or domain—was corrected. This is an invalid test input, not a scientific counterexample or a secretly expected substantive RED. FIXTURE_CORRECTION.md and the original failed archive preserve the distinction.

Corrected scientific GREEN: **36629091598**, job **109613462788**, attempt **1**, execution SHA **02954512b3e84e62a978dfe56f6007c501ef3b7f**. Python **3.11.16**, inherited test dependencies SymPy **1.13.3** and mpmath **1.3.0**. All 15 commands returned exit code zero. The primary implementations use only the Python standard library.

Original scientific artifact **11061821105** is 91,794 bytes, SHA-256 `31fe8aab386f318d4679962da638d4a01cb3f3d95f6772dfec13c0029e78997a`. Its downloaded ZIP SHA, CRC, all listed member checksums, source snapshot and full scientific outputs were inspected. The publication workflow separately retrieves the original RED, failed-fixture and GREEN archives, reruns the complete campaign, requires equality of five scientific files, then performs scoped non-force commit and read-back verification. Exact publication provenance is recorded separately in PUBLICATION_EVIDENCE.json.

## 6. Interpretation and limits

.27 refuted universal event-wise attribution. .28 determines exactly when attribution IS possible and when a small actual-state witness refutes it. No extra event allocation, source model, coupling, response operator, inner product, or geometric target was supplied to force this conclusion.

The characterization still may require exponentially many ideals; no efficient polynomial-time general decision algorithm is claimed. Self-review is documented in REVIEW.md. Algorithmic independence of the verifier is not independent authorship, and written proofs are not proof-assistant formalizations.

The source-cone interpretation and physical realization questions remain separate. This stage neither proves nor refutes a fundamental time primitive in other theories. It preserves the program's intended ordering convention:

**Time is pruning / ordered recoverability update.**
