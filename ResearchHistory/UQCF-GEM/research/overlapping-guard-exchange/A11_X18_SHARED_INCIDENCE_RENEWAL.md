# A11.X18 — shared-incidence guard bounds and reusable unequal-capacity handovers

Scope: 010dfa6e8dcf03fe55f279f12ebc7bde038da190.
Parent analytical publication: b850c5ec552ee588104caa8a68cfefefa3d4cd9e.
Certified baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen analytical candidate for fresh independent WHOLE-ARGUMENT review.

## 1. Statement and actual certificate

Fix a finite ordered palette P, r labelled original root slots, positive original floors a_i, and exact-q endpoints E,C, q>=3. A primitive toggles ONE incidence in ONE root, preserving its original floor. Choose supplied minimum q-covers and legal cover-retaining exact floor compactions B of E and Z of C. In particular |B_i|=|Z_i|=a_i and both compact tuples are EXACT q.

Choose fixed nonnegative integer capacities D_x for each original palette label x, with

degree_B(x)<=D_x and degree_Z(x)<=D_x.

These are sufficient construction bounds, not additional native admissibility rules. Capacities may differ, may be zero, and need not sum to the original floor total S. No extra slot, incidence or label is supplied by a capacity.

Choose any fixed F_i subset B_i intersect Z_i and put U_i=B_i union Z_i. For a forbidden set K of q-2 labels define its actual fixed-overlap correction

b_F(K)=sum_i max(|F_i intersect K|-1,0).

This counts repeated hits in the SAME actual rows. It does not assume independent witness systems. At q4 it is just c_F(x,y), the number of actual rows whose fixed F_i contains both x and y.

**Theorem X18R (shared-incidence renewal/completion).** Suppose for EVERY K subset P of size q-2 at least one of these actual certificates holds:

1. **Capacity/overlap certificate:** sum_(x in K) D_x + 1 - b_F(K) < r.
2. **Union witness:** some ACTUAL slot i has U_i intersect K empty.

Then E and C admit a finite native path with hitting number in {q-1,q}, restoring EVERY original labelled/noncompact destination support.

The constructive preliminary path preserves tau>=q-1 and all original floors. Every completed transfer boundary satisfies degree(x)<=D_x; each primitive has at most ONE label exceeding its own capacity, and its excess is at most one. All F_i incidences remain fixed and each row stays within U_i. Completed cycles restore their entire previous label degree vector and supply the next progress move. No spare label, spare column capacity, reserved root count, compatible guard placement or slot permutation is needed.

At q4 the first certificate is the pair inequality

D_x+D_y-c_F(x,y)<=r-2.

Every pair is checked on the same labelled incidence system. A pair failing this inequality must have the second actual witness; ignoring it is invalid.

This is a new sufficient coupled-renewal certificate and complete construction, not a new universal mixed-floor theorem. The construction transparently extends X14's actual cycle mechanism. Concrete controls below compare certificates without falsely claiming new connectivity for already-solved endpoint pairs.

## 2. Derived hit bound and all lower witnesses

At any preliminary vertex A, let n_i=|A_i intersect K|. The exact hit-count identity is

number of roots hit by K
= sum_(x in K) degree_A(x) - sum_i max(n_i-1,0).

Since F_i subset A_i throughout, n_i>=|F_i intersect K|. Thus

number of roots hit by K <= sum_(x in K) degree_A(x) - b_F(K).

At most one column has degree D_x+1; all others have degree at most their own D_x. Hence the right side is at most sum_(x in K)D_x+1-b_F(K). Under certificate 1 this is STRICTLY less than r, so an actual existing root misses K. Select the first missed slot in the supplied order; that defines W_A(K) without inventing a support.

Under certificate 2 the supplied actual root i remains a subset of U_i and therefore misses K at every primitive, regardless of column degrees. This is a witness from a legal moving root, not a frozen-background restriction on native connectivity.

These alternatives may be chosen separately for each K. They concern the SAME path, original columns and rows; no separate reserve or capacity is assigned to different pairs. Together they protect every forbidden (q-2)-set. Every smaller set can be extended to a (q-2)-set on the same palette since exact feasibility implies k>=q; a root missing that extension also misses the smaller set. Therefore tau(A)>=q-1 at every primitive. This covers pairs containing the overfull label, unrelated pairs, labels used only at one endpoint and unused labels.

Shared fixed incidences improve the hit bound rather than supplying a guard by themselves. Merely retaining a high-transversal collection of smaller F_i does NOT imply that larger moving supports preserve that transversal; the exact hit-count inequality is the justification.

## 3. Eligible transfers and blocked-cycle existence with unequal capacities

At a completed-transfer boundary the current row sizes are a_i. Pair each current surplus label in A_i minus Z_i with a deficit label in Z_i minus A_i, using palette order. Initially fix those pairs and remove an edge only after its transfer is complete. Write x->y coloured i for a pair. Its source is an actual present non-destination incidence; its destination is an actual absent destination incidence. It never changes F_i.

The balance identity is

outgoing pending count(v)-incoming pending count(v)
= degree_A(v)-degree_Z(v).

If a pending edge ends at y with degree_A(y)<D_y, add y in its row and then remove x. Both edits are eligible: y is an unprocessed deficit and x an unprocessed surplus. The row first grows to a_i+1 then returns to a_i. All columns stay within their own capacities. Each primitive decreases the symmetric difference from Z by one and stays inside U_i.

If differences remain and no such greedy edge exists, every label with an incoming pending edge is full at its OWN capacity D_v. The balance identity and degree_Z(v)<=D_v imply that such a label has an outgoing pending edge too. Follow edges to obtain a directed cycle and extract a simple cycle. Every cycle vertex has an incoming edge and is therefore full. Zero-capacity labels cannot lie on this cycle because a full zero-degree label has no outgoing surplus incidence. A cycle has at least two distinct vertices because no row has the same label as both surplus and deficit.

This supplies an actual progress move whenever the destination is unmet. No capacity averaging, equal-capacity inference or unjustified outside-buffer comparison is made. In particular, a full column of capacity D_x need not have more occupants than an underfull column of a different, larger capacity; this proof never uses that false inference.

## 4. Multiple-overlap cycle renewal

Let the eligible simple cycle be x_1->x_2,...,x_m->x_1, m>=2, each edge retaining its actual row colour.

First add x_2 in the row of x_1->x_2, then remove x_1. Column x_2 temporarily has degree D_(x_2)+1; x_1 has degree D_(x_1)-1.

Process the preceding cycle edges in reverse order:

x_m->x_1, x_(m-1)->x_m, ..., x_2->x_3.

At every such transfer the destination is the travelling underfull column. Adding there restores its OWN capacity, not the capacity of another label. Removing the source makes that source underfull; the last source is x_2, whose removal instead closes the initial overfull column.

At every primitive there is at most one overfull column and its excess is one. Every other column stays at most its own D_x. At some addition instants there is no underfull column, but the one-overfull certificate still holds; no spare-capacity claim is needed there.

Distinct cycle labels ensure no earlier transfer removes a later source incidence or installs a later destination incidence. Within any row, original surplus and deficit sets are disjoint. Adjacent cycle edges cannot share a row colour, since their shared label would otherwise be both surplus and deficit in that row. Repeated nonadjacent colours are harmless: completed transfers return the row to a_i before its next transfer, and the directed incidences are distinct.

Every primitive therefore exists and is floor-safe. It changes only a surplus or deficit, never a correctly placed F_i incidence, and keeps the support within its endpoint union. The shared-count/union certificate from Section2 protects every forbidden set at all addition and deletion instants.

A completed cycle restores EVERY label's previous degree and EVERY row's original compact size. It resolves all its selected pending pairs. The remaining balance identity and degree bounds consequently recur. If differences remain, Section3 supplies another greedy move or cycle. Renewal need not restore exact q: it restores the rigorous structure guaranteeing the next move, even at level q-1.

The symmetric difference from Z strictly decreases by one at EVERY preliminary primitive, including cycle edits. The finite potential and supplied next move prove termination at exactly Z. This proof does not infer completion of arbitrary safe prefixes outside its declared invariant.

## 5. Exact original destination and upper conversion

Exact compaction is an actual primitive path. Retain an a_i-subset of E_i meeting a supplied minimum q-cover, then delete every other incidence singly. The cover supplies tau<=q; deletion cannot decrease tau, so every intermediate stays EXACT q and respects its own original floor. Save this path. Do the same at C to obtain Z, saving its reverse. The theorem assumes the chosen compact endpoints satisfy the certificate; no convenient compaction is presumed to have it.

Concatenate E->B, the finite lower schedule B->Z, and the reversed exact compaction Z->C. The path uses the original palette and labelled slots, restores all noncompact incidences, and maintains tau>=q-1. Every root remains nonempty, so tau<=r is a finite upper bound.

Apply accepted maximum-layer Theorem A at certified baseline 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f to THIS complete finite path between the ORIGINAL exact-q endpoints. Its native union closure and positive-floor hypotheses hold. It converts the path to the required band {q-1,q} without changing either endpoint.

The lower schedule and converted path are explicitly different. The lower schedule is destination-directed between the chosen compact tuples and has length equal to their initial symmetric difference. Maximum-layer conversion may change order, use temporary/repeated incidences or have greater length. No original A11 directed universality or efficiency bound follows.

For a finite sequence of exact endpoints where each adjacent pair supplies this certificate, concatenate the converted complete legs at exact joins. Each leg fully restores its original destination; no borrowed resource or deficit accumulates. The local cycle argument also renews its invariant at every completed cycle. These are distinct, both proved renewal statements.

## 6. Comparison with the uniform degree certificate

Taking D_x=D for all x and F_i empty recovers X14C's lower safety inequality r>=(q-2)D+2. Thus X18R retains the accepted construction and removes the assumption that the forbidden-cover estimate must use a common maximum with no shared-hit correction.

At q4 it can instead use the two capacities for each pair, subtract the actual fixed pair codegree, and use an actual endpoint-union missed row for exceptional pairs. Failure of all these sufficient certificates for a pair makes THIS construction unavailable; it is not a native disconnection or necessary higher barrier.

No total S<sum D_x condition is needed, because the one-overfull cycle is legal even when every useful column is full. The construction does not extend the strict-slack outside-buffer argument by comparing unequal capacities.

## 7. Valid symbolic certificate control and inherited connectivity

This control checks strict gain over whole-carrier degree-budget certificates. It is ALREADY connected by an accepted actual multiple-overlap union bridge and is not claimed as newly resolved research.

Fix m>=22. Use mutually disjoint palette groups Q of m labels, U={a,b,c,d,e,f}, V0,V1,W0,W1 of four labels each. Thus k=m+22. There are six original labelled slots with floors (m+3,m+3,m+3,6,4,4).

The source B is
Q union {a,b,c}; Q union {d,e,f}; Q union {a,d,e}; U; V0; W0.

The destination Z is
Q union {b,c,f}; Q union {a,d,e}; Q union {a,d,e}; U; V1; W1.

Every root is already at its original floor. The first four roots require exactly two hitting labels: a Q label and a U label hit them, while no single label lies in all four. In the source, {a,b,c} intersect {d,e,f} is empty; in the destination, {b,c,f} intersect {a,d,e} is empty. The last two roots use separate private groups outside Q union U and each requires another label. Thus both full tuples are EXACT four with explicitly supplied four-covers consisting of a Q label, a U label, one label of V0/V1 and one of W0/W1.

Choose D_x as the maximum of its actual endpoint degrees and F_i=B_i intersect Z_i. Q labels and a,d,e have D=3; b,c,f have D=2; private labels have D=1. The U row contributes one incidence to EVERY a,...,f at both endpoints and must be included in these degrees. The fixed common Q/a rows are row3 (one); Q/d and Q/e rows are rows2,3 (two); Q/b and Q/c have row1; Q/f has none.

For two Q labels the corrected pair count is 3+3-3=3, satisfying certificate1. However Q with a has count 3+3-1=5, exceeding r-2=4; no all-pairs capacity-only claim is made.

Instead verify the SAME hybrid certificate for every pair:
- Every pair entirely within Q union U is missed by the ACTUAL row5 endpoint union V0 union V1, so certificate2 applies. This includes the pairs failing the corrected count.
- A pair with one label in Q union U and one private label has capacity sum at most 3+1=4; subtracting a nonnegative fixed codegree only improves this. Certificate1 applies.
- A pair of two private labels has capacity sum at most 1+1=2, so certificate1 applies.

These categories exhaust all palette pairs. The count and actual union witnesses concern the same native schedule and rows. No independent capacity system is introduced.

Scalar X14 cannot apply to these unique floor compactions: their maximum degree is three, requiring r>=8 rather than six. Any whole-carrier X15N parameters have M>=3 and r>=D+M+1, so D<=2. But S=3m+23>2(m+22)=2k for m>=22. No such X15N parameter choice works. X17's mixed profile also does not cover this profile, since floors m+3 and six/four exceed three while remaining below k-2=m+20.

These exclusions are NOT exclusions of every accepted method. In fact the old guard on slots {4,5,6} and destination guard on the SAME three slots have union bridge U,V0 union V1,W0 union W1, a family of three pairwise-disjoint actual supports requiring three labels. The accepted general bridge lemma in GUARD_HANDOVER.md therefore connects the pair with three shared guard slots. This is disclosed explicitly; the example is a certificate comparison and a method-limit control, not a new previously unresolved carrier.

The NEW statement is Section1's reusable general construction with eligible progress at every unfinished boundary, for arbitrary mixed original floors and all pairs/forbidden sets satisfying its declared witnesses. Further work must derive these witnesses for genuinely remaining classes before announcing a new universal carrier closure.

## 8. Rejected exploratory control and its precise classification

Before the proof freeze, an exploratory variant used Q plus {x,v3,u2}, Q plus {y,u1,p}, Q plus {x,w3,u3}, followed by {x,u1,u2,u3,u4,u5}, {v1,v2,v3,v4}, {w1,w2,w3,w4}. It was intended as an exact-four control with overlapping incidence handovers.

It is NOT exact four: {u1,v3,w3} hits all six roots. The failed exact-endpoint premise invalidates its use as a theorem application or new exact-four carrier. It does not refute Section1, whose exact endpoint inputs remain mandatory; it proves no native disconnection. The control was rejected analytically before freezing this candidate, with no numerical execution. The valid control in Section7 proves its exact endpoint premise directly.

The first frozen X18 candidate d6953eb4ccf10c9ceb216665b117d9a1940f3443 also contained a degree-count error in that valid control: it omitted row4=U and claimed capacities2 for a,d,e and1 for b,c,f. The independent reviewer caught this before acceptance. Section7 now includes the actual U incidences and uses the theorem's actual row5 union witness for the affected pairs. The general theorem and its proof are unchanged; the rejected capacity-only check is not presented as accepted evidence.

## 9. Dependencies, discovery and explicit remaining obligation

The frozen baseline GENERAL_PARENT_CONNECTIVITY.md supplies cover-retaining exact compaction and maximum-layer Theorem A. Accepted X14 supplies the related uniform-capacity one-overfull cycle; here Sections3/4 prove unequal-capacity eligibility/renewal explicitly rather than relying on an unstated generalization. X15N is used only for the transparent budget exclusion in Section7; X17 only for the scope comparison. The actual general union bridge is acknowledged as applicable to that control. No frozen source is rewritten or recertified.

The derived guard estimate counts shared hits exactly enough to retain actual missed roots even when a common maximum-degree estimate is too large. The renewable structure is an unequal-capacity pending graph with one temporary overfull column and a travelling hole. It does not assume three independent witness systems, an untouched fixed number of reserve roots, or restoration of exactness after each cycle.

This packet establishes a reusable coupled-renewal lemma AND finite exact endpoint completion under an explicit actual certificate. Its remaining scientific obligation is to derive the per-label/common-incidence or union-witness certificate for new unresolved endpoint classes, or provide another renewing witness where it fails. The control is already solved and is not promoted to a new unresolved carrier, and certificate failure is not a negative native theorem.

X15 universal original-floor-three target-four ROOT closure and X16/X17 accepted classes remain unchanged. Original A11 destination-directed universality, unrestricted mixed-floor/higher-target and nested universality remain open. Conditional native child lifting retains the baseline interfaces; no root obstruction is promoted to nested necessity.

Native paths are not restricted to compact, destination-directed or frozen-background schedules by this sufficient construction. No arbitrary mixed-floor permutation, weakened floor, new label/slot or geometry is introduced. Unit repair is an upper bound, not an assertion of a positive minimum for every pair. Use ordered repair/retained recoverability; no fundamental time, physical energy/metric/gravity or originality claim.

No enumeration, scientific tests/workflows/run IDs, implementation, benchmark, numbered v16.55 certification or integration merge. Certified v16.54 and separate accepted efficiency design remain unchanged; runner implementation, fixture execution and measured speedup remain unstarted.
