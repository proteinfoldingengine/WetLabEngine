# v16.29 — Local profile versus maximum aggregation: combined findings

Read with PROOFS.md L1–L7 and PUBLICATION_EVIDENCE.json. This is the next numbered foundational audit, not a new response model. Scientific SHA `5d09e6c28827f70412c5f8b05fd98af75d3b7e5f` is distinct from later documentation and publication commits.

| Required question | Adjudicated answer |
|---|---|
| Which operation is now classified? | The existing scalar diamond of h=max(1,max tau_v), in terms of the four actual local profiles. L1–L4 give an exact same-parent/distinct-parent law for every admitted finite same-union two-event square. |
| Does nonzero scalar D imply local mixed dependence? | No. Admissible retained controls have D_h=-1 and +1 while EVERY local D_v is zero. The negative example uses five vertices; the positive control uses six. |
| Does zero scalar D imply local independence? | No. A five-vertex retained example has a nonzero local D_v hidden by a constant larger global maximum. |
| Was a new carrier or law introduced? | No. The full tau profile was already defined in .24–.28. Background B is computed from unchanged entries, not supplied or fitted. No earlier source/response map is discarded. |
| What actually passed computation? | 228 tests, every 45,488 original .28 diamond and its transported copy, plus all 54,842 admissible two-event squares from distinct covers on trees through five vertices and their transported copies; six separately declared controls. Full raw states/profiles were independently reconstructed. |
| What remains open? | Structural simplifications for local cover interactions beyond this audit, physical attainability of the formal cone, physical response selection and the operational quantum bridge. No physical coupling, geometry or time result follows. |

## 1. The strongest result against a tempting extrapolation

A nonzero mixed difference of the global consistency-testing order does not necessarily represent a mixed dependence in any local child-cover constraint. The maximum operation itself can create it. Conversely, a zero scalar mixed difference does not certify that all local quantities are additive.

This does NOT invalidate v16.28. Its theorem classified its explicitly specified scalar F. It did not prove the same classification for the richer local profile. v16.29 determines the exact relation and the boundary of that extrapolation without replacing F with a preferred new observable.

## 2. Exact law from the existing data

For two enabled deletions e,f with fixed union U, let p and q be the parents of their removed nodes. Write D_v for the mixed difference of tau_v, and D_h for that of h.

**Different parents.** Each local count responds only to its own incidence deletion, so D_v=0 for every v. Nevertheless, if u=h(V_e)-h(V) and v=h(V_f)-h(V),

    D_h=-u*v,  u,v in {0,1}.

Therefore D_h=-1 exactly when both single deletions separately raise the previous maximum. They compete in the scalar summary; there is no mixed local-profile interaction.

**Same parent.** Let (a,b,c,d) be that parent's counts in the four states (V,V_e,V_f,V_ef), and let B=max(1,all unchanged local counts). Then

    D_h=max(B,d)-max(B,b)-max(B,c)+max(B,a).

The atomic bounds give a complete piecewise rule:

| Condition | Exact scalar mixed difference |
|---|---|
| B<=a | D_h=d-b-c+a, the local mixed difference |
| B=a+1 | D_h=+1 exactly for (a,b,c,d)=(a,a+1,a+1,a+2); otherwise zero |
| B>=a+2 | D_h=0 |

This follows by exhausting the six possible integer increment patterns allowed by the inherited 0/1 atomic bound, not by fitting to the enumeration. In the middle case a positive scalar mixed difference can arise while the local mixed difference is zero.

## 3. Explicit retained counterexamples

### Negative scalar interaction generated only by the maximum

On parent tree (-1,0,0,1,1), take

    V=({0,1,2},{0,1,3,4},{0,2},{0,1,4}), e=(0,2), f=(1,4).

These are actual root-containing prefix views. The two deletions are current leaves and the other views preserve the union throughout. The only changing local values are:

| State | tau_root | tau_1 | h |
|---|---:|---:|---:|
| V | 1 | 1 | 1 |
| V_e | 2 | 1 | 2 |
| V_f | 1 | 2 | 2 |
| V_ef | 2 | 2 | 2 |

Both local mixed differences vanish, but D_h=2-2-2+1=-1.

### Positive scalar interaction generated only by a threshold

On (-1,0,0,1,1,1), take

    V=({0,1,3,4,5},{0,1,3},{0,1,4},{0,2}), e=(0,3), f=(0,4).

The root count stays 2. The count at vertex 1 is (1,2,2,3), whose mixed difference is zero. The scalar values are (2,2,2,3), giving D_h=+1. This exact SIX-vertex witness is a declared control; it is not presented as exhaustive six-vertex coverage.

### A local interaction hidden by the maximum

On (-1,0,0,1,1), take

    V=({0,1,3,4},{0,1,3},{0,1,4},{0,2}), e=(0,3), f=(0,4).

Root tau is constantly 2; vertex 1 has (1,2,2,2), giving D_1=-1. Scalar h is constantly 2. Thus every scalar diamond in this two-event interval is zero while its local attribution is dependent.

EXAMPLES.json records every view, event, intermediate state, local count, scalar value and classification. No arbitrary profile vectors are substituted for admissible retained constructions.

## 4. What the bounded campaigns found

First, the hash-bound .28 archive was reaudited. It contains **45,488 original diamond occurrences**, including repeated current-cover configurations in different endpoint intervals. All **5,212 nonzero scalar diamonds** are locally transmitted; the other **40,276** have neither scalar nor local mixed difference. The full transported copy agrees.

That agreement is mathematically size-limited: through four vertices there can be at most one branching vertex. Every other local count is at most one, so h coincides with that single potentially nontrivial tau. This domain cannot expose competing branching maxima.

The new exhaustive extension contains all 17 rooted unordered tree shapes through five vertices, every cover of the whole tree by up to four distinct prefix views, and every unordered pair of simultaneous current-leaf deletions with unchanged final union:

| Original-coordinate classification | Count |
|---|---:|
| Complete admissible two-event squares | 54,842 |
| Local mixed difference transmitted to h | 5,755 |
| Nonzero h mixed difference with all local mixed differences zero | 32 |
| Nonzero local mixed difference hidden by h | 19 |
| Both scalar and local mixed differences zero | 49,036 |
| Same-parent / distinct-parent pairs | 50,133 / 4,709 |
| Negative / zero / positive scalar mixed differences | 3,163 / 49,055 / 2,624 |

Every case was repeated under the specified actual root-preserving relabeling, indexed-view reversal and storage reversal. The transported counts are identical. Copies are equivalence controls, not independent physical observations. The parent corpus and extension are reported separately, not added as independent samples.

The raw certificate includes **200,660 four-state records** across those original and transported corpora, plus six explicit controls. Its size is **97,275,232 bytes**, losslessly compressed to **1,731,596 bytes**. Raw SHA-256:

`19d291e2f51286051a1e1c2840ab2d5994b9f8fe52f88f574ad2460b7ba7e69b`

## 5. Verification rather than self-reporting

Producer child-cover minima use subset-union dynamic programming; the verifier uses direct exhaustive view subfamilies. Producer tree enumeration uses ancestor-first arrays; verifier shape coverage uses Pruefer sequences. It reconstructs all raw covers, event pairs, both deletion orders, every profile entry and the exact theorem prediction. It imports no producer or inherited adjudicator. Parent .28 scalar values are compared against newly computed values, not used to define them.

All **30 new tests** and **198 inherited retained-research tests** passed: **228 total**, all 16 campaign commands exiting zero. Fourteen named corrupted-certificate tests reject invented local interactions, false profiles/heights/classifications/predictions, missing fields and states, incorrect parent labels, foreign origins and Boolean-for-integer substitutions. Further controls reject malformed inputs, incomplete shape/pair coverage, duplicate pairs and false relabeling; valid reordered events/storage and both signs of actual examples are accepted.

Run **36636868485**, SHA **107f68a87b6813dff75679e3ee701359dfbd195f**, is wiring RED only: all 30 tests failed because the modules were absent. It is not called a substantive mathematical failure. The first complete implementation run passed the rejecting suite and complete audit; no false implementation bug or substantive RED is manufactured to embellish the record.

Scientific GREEN: **36637296991**, job **109640956245**, attempt **1**, execution SHA **5d09e6c28827f70412c5f8b05fd98af75d3b7e5f**. Python **3.11.16**, inherited dependencies SymPy **1.13.3**, mpmath **1.3.0**; primary implementations use the standard library. Original artifact **11065511674**, **1,765,998 bytes**, SHA-256 `f7d838b76750f2dc6319955147f56c5eea7016b3deb5132a833c718f847f4f30`. Downloaded ZIP SHA/CRC and all 25 manifest members were verified. Publication must additionally rerun and compare scientific files before the evidence commit is declared complete.

## 6. Scope and review

The full local profile was earned earlier; retaining it here avoids mistaking a nonlinear scalar summary for a local interaction law. The scalar h remains a useful exact consistency-testing order. Neither h nor its profile is being declared a physical field, amount of information loss, energy, curvature or time.

Review is self-review with an algorithmically independent verifier, not independent authorship. Written proofs are not proof-assistant formalizations. No new geometry, response law, coupling or operational quantum primitive was inserted. General computational complexity is not improved by this bounded audit.

**Time is pruning / ordered recoverability update.**
