# A7: a tight seven-root obstruction to completed two-label accessibility

Status: frozen analytical candidate; independent review pending. Parent: 36a82844a5ef83fc8386c37a9427064519043511. Scope: the completed-state graph in RESEARCH_BRIEF.md, not general primitive connectivity. No enumeration, tests or workflow execution.

## 1. Exact labelled endpoints

Take the fixed palette P={1,2,3,4,5,6,7}, seven labelled root slots, uniform positive floor a_i=4, and q=3. Let the complement blocks be

    B_1=123, B_2=145, B_3=167, B_4=246,
    B_5=257, B_6=347, B_7=356.

Here 123 denotes the subset {1,2,3}, not an added incidence or geometric primitive. Define A_i=P minus B_i. For any two distinct root indices s,t, define C by interchanging A_s and A_t and leaving all other labelled supports fixed. This gives a finite symbolic family of endpoint pairs, and arbitrary palette relabelling gives equivalent instances. The term Fano refers only to the displayed seven-triple incidence design.

Each support has size four. Every pair of palette labels lies in exactly one displayed block: the triples containing 1 partition the six other labels into 23,45,67; the remaining pairs occur in 246,257,347,356, with no repetition. Thus every two-label set misses at least one root support. Every singleton also misses a root. The triple {1,2,4} is not a displayed block, hence is contained in none of these size-three complements and hits every A_i. Therefore tau(A)=3, and slot interchange gives tau(C)=3.

## 2. Tight covering forces every completed vertex to be a triple design

For any admissible tuple X let E_i=P minus X_i. Floors imply |E_i|<=3. The condition tau(X)>=3 is equivalent to every pair of labels lying in at least one E_i. Indeed a pair hits all root supports exactly when it is contained in no complement; with seven labels any smaller hitting set could be extended to a pair.

There are 21 palette pairs. Seven complements cover at most

    sum_i binomial(|E_i|,2) <= 7*3 = 21

pair occurrences. Coverage forces equality throughout. Hence all E_i have size three and every pair occurs in exactly one block. All complements are distinct. Each point lies in exactly three blocks, since its six partner pairs are covered two at a time.

Every such completed tuple actually has tau=3: only seven of the 35 palette triples can equal blocks, and any other triple hits every root support. This also rules out an escape through completed states above q. This tightness argument covers all admissible support sizes, not merely a selected compact subclass.

## 3. Every eligible edge is a whole-palette transposition

Fix a completed tuple X and two distinct labels u,v. A proposed completed neighbor Y has the same incidences outside {u,v} and the same set of roots containing at least one of u,v, exactly as required by RESEARCH_BRIEF.md.

In complements, the roots containing BOTH u,v are therefore fixed. There is exactly one such triple {u,v,w}. Roots containing neither are also fixed: their outside-pair part already has size three, and Section 2 forces size three at the destination. Every remaining root contains exactly one of u,v; its fixed outside-pair part has size two, so its only choices are to retain or swap its single role label. There are two u-only and two v-only blocks.

Put V=P minus {u,v,w}, a four-element set. The outside-pair parts of the two u-only blocks form a perfect matching on V, since each pair {u,x}, x in V, must occur once. The v-only blocks give a second perfect matching. These matchings share no edge, since that would repeat a pair of labels in two blocks. Their union is a connected four-cycle.

Assign each of these four blocks a switch indicator e in {0,1}. At each x in V its incident u-block and v-block must still supply exactly one occurrence of {u,x}. This imposes

    (1-e_u)+e_v=1, hence e_u=e_v.

The four-cycle is connected, so all four indicators coincide. Thus either nothing changes, or every single-role block swaps u and v. In the latter case the whole tuple is exactly the global palette transposition (u v) applied to X. The both-role and neither-role blocks were already invariant under that transposition.

Consequently every graph edge from every reachable completed tuple is a global palette transposition. Conversely global palette transpositions are eligible: they preserve floors, transversal number, outside-pair incidences and pair occupancy. Each component is exactly a palette-permutation orbit of a labelled tuple. The argument needs neither a classification of all seven-point designs nor numerical graph search.

## 4. A lone root-slot interchange lies outside that orbit

Suppose a palette permutation sigma carried A to C for a chosen s!=t. In complement notation it would interchange B_s and B_t and fix each of the other five blocks setwise.

The incidence signatures of palette points with respect to those five individually fixed blocks are distinct. To see this, any two distinct points x,y each lie in three blocks, and exactly one block contains both. Their full seven-block signatures therefore differ in four block positions. Removing the two positions s,t leaves at least two differences. Thus no two points have equal signatures on the fixed five blocks.

A permutation preserving each of those five blocks must preserve every point's signature, so it fixes every palette point. It is the identity and cannot interchange the two distinct blocks B_s,B_t. This contradiction proves that A,C lie in different completed-state components.

**Theorem A7-N.** The universal accessibility assertion in RESEARCH_BRIEF.md is false. It fails for k=r=7, uniform floor four and target three, for every endpoint pair obtained by interchanging two labelled root slots in the displayed tuple. Completed states above the target do not evade the obstruction.

The fixed labelled root slots are essential to this conclusion. Quotienting out their permutations would change the declared graph and remove these particular endpoint distinctions; that quotient was not the A7 question.

## 5. The same endpoints have an explicit primitive one-unit path

The method obstruction is not a primitive barrier. Here is a direct construction without invoking a separate root-permutation dependency.

Write U=A_s and V=A_t. Let S agree with A outside s,t and have support U union V at BOTH s,t. For any hitting set H of S, H hits U union V, so it hits at least one of U,V. Adding at most one label from the missed support, when necessary, makes it hit both U,V and all unchanged roots. Therefore

    tau(A)<=tau(S)+1, so tau(S)>=2.

Also S contains A coordinatewise, hence tau(S)<=3. Expand A to S by single-incidence additions, then contract S to C by single-incidence deletions. During expansion every tuple contains A; during contraction every tuple contains C. These facts give tau<=3. Every intermediate tuple is coordinatewise contained in S, giving tau>=tau(S)>=2. Every intermediate support contains its corresponding starting or destination support, so its floor four holds.

There are finitely many additions/deletions on the original palette and original root slots. The exact labelled destination is reached with tau in {2,3}. There are no simultaneous primitive changes or extra labels/slots. For the displayed design any two different complement triples meet in one point, so |U union V|=6: two additions in each exchanged slot, followed by two deletions in each, suffice. This gives eight primitive moves.

The intermediate tuple S is generally outside the tau>=3 completed graph; Section 2 shows that its size-six exchanged supports cannot be a completed vertex. Allowing defect-bearing states is exactly what the restricted method omits in this example.

## 6. Scientific decision and next obligation

This is a negative answer for the specified completed two-label exchange class and a positive one-unit primitive construction for the same endpoints. It closes the declared mathematical question negatively if independently accepted. It does not close universal higher-floor primitive connectivity, native lifting, implementation certification, originality or any physical interpretation.

A revised exchange graph could add safe root-slot transpositions for equal floors alongside distributed two-label exchanges. The explicit path in Section 5 supplies those added edges. Whether that enlarged graph connects different incidence structures remains a NEW OPEN question; this document neither proves it nor silently replaces A7's declared relation. Unequal floors require checking each exchanged destination against its own floor.

This obstruction occurs at q=3 and floor four. It does not settle the earlier diagnostic proposal with q=4 and floor three. A7 was expressly formulated over all positive floors and q>=3, so this counterexample suffices for A7's universal assertion.

No new scientific computation or certification run was launched. The seven-triple data are exact symbolic input to the proof; the obstruction covers every permitted completed-state move analytically. General root primitive and full nested accessibility remain open.
