# A11.X24 — weighted actual protection and the pair-partition obstruction

Scope: 7ed53d30e502f627f77e7d0f607e288843025b1d.
Parent analytical publication: f08b5e6a7495fad378b9d5c36f51720a95c5c5c3.
Certified baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Candidate for fresh independent whole-argument analytical review. No numerical execution.

## 1. Statements and native domain

Fix a finite ordered palette P of k labels, r labelled slots and original positive floors a_i<=k. A support A_i is any subset of P of size at least a_i. A primitive adds or removes ONE incidence in ONE root, retaining that original floor. Temporary larger supports, repeated edits and changes to background roots remain permitted. Exact endpoints have transversal four.

**X24W — individual-floor necessary protection inequalities.** Every exact-four endpoint satisfies

sum_i binomial(k-a_i,3) >= binomial(k,3).

For every label x let I_x be ALL actual slots missing x. Their original floors satisfy

sum_(i in I_x) binomial(k-1-a_i,2) >= binomial(k-1,2).

Only actually avoiding slots appear in the second sum. Binomial coefficients count subsets, with value zero when the nonnegative upper argument is below the lower argument. Every a_i in I_x is at most k-1. These are necessary inequalities, not existence or connectivity criteria.

For any actual complementary pair-cover on a v-label palette, equality between its total pair capacity and binomial(v,2) forces every pair to occur exactly once. Consequently distinct labelled blocks intersect in at most one label, and at each vertex u,

sum_(blocks B containing u) (|B|-1) = v-1.

Failure of either consistency condition makes the capacity inequality STRICT. Bounds on block sizes also cannot attain equality unless all relaxations used to obtain the bound are equalities. This elementary shared-incidence test strengthens a capacity count; it never treats overlapping witness systems as independent.

**X24G — five-root guard with individual floor grades.** On a palette of at most seven labels, an actual family of FIVE roots of size at least three and transversal at least three contains at most TWO roots whose actual size is at least four. Therefore at an exact-four endpoint on eight labels with original floors three/four, if degree(x)=r-5 then at most two original floor-four slots avoid x. Equivalently at least f-2 of the f original floor-four slots contain x. This last bound is useful when f>=2; it is not a new independent capacity.

**X24E — exact-eight-label structural slack and complete mixed repair.** On eight labels with every original floor three or four:
- no exact-four endpoint exists with r<8;
- at r=8, exact four forces every original floor to be three and every original endpoint already has exactly twenty-four incidences;
- at r=9, exact four forces f<=4, where f counts original floor-four slots.

Hence EVERY pair of exact-four endpoints on ANY such carrier with r<=9 has finite native repair with 3<=tau<=4, restoring EVERY original labelled/noncompact destination support. At r=9 no separate incidence-budget hypothesis is needed: feasibility itself gives S=27+f<=31<32.

The repair mechanism is inherited X14/X15 within newly supplied structural hypotheses. This does not claim that every profile with f<=4 is feasible, that every pair requires a positive defect, or that all mixed carriers are solved.

## 2. Actual witnesses and the weighted count

Exact four means every three-label set K fails to hit at least one ACTUAL root. Its complement B_i=P minus A_i therefore contains K. The actual complementary blocks jointly cover all triples. Counting each block's triples, with overlaps allowed, gives

binomial(k,3) <= sum_i binomial(k-|A_i|,3)
             <= sum_i binomial(k-a_i,3).

This is a necessary count of the SAME supports. It is the individual-floor version of the elementary complementary-cover reasoning in the baseline and X16, not an originality claim.

For fixed x, ALL actual roots avoiding x have transversal at least three: a two-label cover of them, together with x, would hit the entire exact-four tuple. They live in P minus {x}. Every pair of those remaining labels must miss an ACTUAL avoiding root. Relative complements B_i=(P minus {x}) minus A_i, i in I_x, cover all pairs. Hence

binomial(k-1,2) <= sum_(i in I_x) binomial(k-1-|A_i|,2)
               <= sum_(i in I_x) binomial(k-1-a_i,2).

No capacity from a slot containing x is assigned to this avoiding system. The same slot can participate in several x-systems, so these inequalities do not give separate pools. Summing the ACTUAL pair capacities over x gives exactly three times the actual triple-capacity sum, since every three-set has three choices of its distinguished x. The raw summed count alone is consequently not a new independent constraint. The new strengthening below comes from impossibility of equality within an actual shared pair system.

For a pair-cover with exactly binomial(v,2) total actual pair incidences, every required pair occurs at least once and the total equals their number, so it occurs exactly once. Two distinct labelled blocks sharing two labels would duplicate that pair. At a vertex u, each containing block contributes |B|-1 partners, and every other vertex is a partner exactly once. This proves the vertex equation and X24W. These necessary tests are not asserted sufficient for existence.

## 3. Equality cannot supply the five-root graded guard

Suppose five actual roots on a palette V of seven labels have size at least three, transversal at least three, and at least three roots of size at least four. A family on fewer labels can be embedded into seven labels without altering its supports or transversal, so it suffices to use |V|=7.

Its actual relative complementary blocks cover all twenty-one pairs. If four or more roots have size at least four, their pair capacity is at most

4*binomial(3,2)+binomial(4,2)=18<21,

an immediate contradiction. Thus the only possible remaining case has exactly three roots of size at least four and two others of size at least three. Their maximum total pair capacity is

3*binomial(3,2)+2*binomial(4,2)=21.

Coverage would force equality throughout: exactly three three-blocks and two four-blocks, with every pair covered exactly once. Denote the two four-blocks B,C. They intersect in at least one vertex because 4+4>7, and in at most one because pair coverage is unique. Thus their intersection has exactly one vertex.

Choose u in B minus C, which is nonempty. It belongs to exactly one of the two four-blocks. The vertex equation from Section 2 would read

3 + 2n = 6,

where n is the number of the three three-blocks containing u. No integer n satisfies it. Contradiction.

This proves X24G for larger native supports too: larger roots only reduce their complement pair capacities; equality had forced the exact sizes. No geometry, design catalogue, enumeration or independent capacities enter the proof.

At an exact-four eight-label endpoint with degree(x)=r-5, I_x has exactly five actual roots and is an actual three-guard on seven labels. Its original floor-four roots have actual size at least four, so X24G leaves at most two of them there. The remaining original high slots contain x, giving degree_high(x)>=f-2. This uses actual joint incidences, not a statement that additional high slots can be manufactured.

## 4. Exact preparation and forced slack

For an original exact-four endpoint choose a supplied minimum four-label cover H. In every slot retain an a_i-subset meeting H, deleting all excess incidences individually in palette order. If unfinished, an excess incidence outside the retained subset supplies the next deletion. Every root keeps its original floor and an H-label. Deletion cannot lower tau, while H remains a cover, so every preparation primitive is EXACT four. Total excess strictly decreases; save every reverse edit.

For any exact-four endpoint with minimum floor three on eight labels, the actual avoiding family lies on seven labels. Accepted X14G proves that four roots of minimum size three requiring three labels need at least ceil(15/2)=8 labels; three such roots need nine labels. Fewer than three cannot require three labels. Hence every actual avoiding family has at least FIVE roots, and every actual label degree is at most r-5, even before preparation.

Let f count original floor-four slots. Every exact compaction therefore has S=3r+f incidences and

3r+f <= 8(r-5).

For 4<=r<=7 this is impossible even at f=0; r<4 is already impossible because tau<=r. Thus exact four requires r>=8.

At r=8 the right side is twenty-four and S=24+f, forcing f=0. Original endpoint degrees are at most three, so the original total is at most twenty-four and also at least twenty-four. All original supports are triples and all eight degrees are exactly three. Larger intermediate supports remain allowed.

At r=9 apply the triple capacity inequality to the exact compact tuple:

56=binomial(8,3)
 <= (9-f)*binomial(5,3)+f*binomial(4,3)
 =90-6f.

Thus f<=5. If f=5, compact incidence is S=32 and every label degree is at most r-5=4. All eight label degrees must consequently equal FOUR.

For EACH of these eight labels, its avoiding family has exactly five roots. X24G requires at most two of the five original floor-four roots to avoid that label. Thus at least three original floor-four roots contain each label. Summing the SAME high-slot incidences over all labels yields at least 8*3=24. But five compact floor-four supports have exactly 5*4=20 incidences. Contradiction.

Hence f<=4 and S<=31<4*8. This is strict slack forced by actual exact-endpoint pair consistency. Original endpoints may be larger; the conclusion concerns their legal exact original-floor compactions, with the original endpoints restored later.

These are necessary feasibility statements. They prove no disconnection and do not assert every surviving floor profile exists. A genuine mixed existence control on nine slots is the eight-root two-core tuple

123,124,134,234,567,568,578,678

with a ninth support 1235 of original floor four. Its first eight roots already require four labels; H1256 hits all nine, so the full tuple has exact four. This demonstrates a nonempty mixed domain. It does not assume arbitrary endpoints have this structure.

## 5. Complete repair and every next edit

At r=8 the forced original degree bound D=3 satisfies X14C's q4 condition r>=2D+2. The already accepted saturated pending-cycle construction, upper removal and exact endpoint restoration apply with the original labelled floors.

At r=9 both arbitrary endpoints admit the Section 4 exact compactions of their ORIGINAL row sizes, degree at most M=D=4 and S<=31<32. X15N's requirements are

D<=M, S<Dk, r>=D+M+1,

namely 4<=4, S<32, 9>=9. No degree leveling is needed. We explain the complete inherited construction rather than mistake strict capacity for a path.

At a completed compact boundary pair each row's present non-destination labels with its absent destination labels. A pending edge x->y has that row's colour; its source is present and its destination absent. The actual balance identity is

out(v)-in(v)=degree_current(v)-degree_destination(v).

If a pending edge ends at degree less than four, add its destination then delete its source in that row. This retains its original floor and degrees at most four.

If pending edges remain without such a move, their destination labels are full. Each full label with an incoming edge has an outgoing edge by the identity and destination degree<=4. Following edges supplies a simple directed cycle with distinct labels. Strict incidence S<32 supplies an EXISTING palette label z of degree less than four, outside the full cycle.

If z is missing from a cycle row, buffer one cycle source there by add z then delete the source. Process the other cycle edges backward into the travelling hole, and finally replace the buffered z by that row's intended cycle destination. If every cycle row contains z, a full cycle source has four incident rows, whereas fewer than four rows contain z. Therefore an ACTUAL row outside the cycle contains the source and misses z. Buffer that source in the outside row, process the whole cycle backward, then restore the outside row's exact original incidence. This is the eligible alternative when a spare label occupies all cycle rows.

Every transfer adds before deleting. Distinct cycle labels and disjoint row surplus/deficit sets keep every subsequent source present and destination absent, including repeated nonadjacent row colours. The buffer label is outside the cycle. The outside buffer row is not a cycle row. All borrowed incidences are restored, each completed macro returns original row sizes, and all actual degrees remain at most four throughout.

For EVERY pair K of palette labels, at every such primitive,

number of roots hit by K <= sum_(x in K) degree(x) <=8<9.

Hence at least one ACTUAL labelled root misses K; select the first in slot order as its witness. This handles every pair, including buffer labels, entirely background pairs and labels absent from the endpoints. Smaller covers also miss a root. Thus the preliminary repair has tau>=3 throughout. No independent witness capacities or geometrically restricted paths are used.

At completed boundaries strict slack is restored; the balance identity again supplies a greedy move or eligible cycle whenever pending differences remain. Each completed macro resolves at least one pending surplus/deficit pair, and any temporary displacement of a correct outside-buffer incidence is restored. The nonnegative pending count strictly decreases at macro boundaries. Each macro is finite, so repair terminates at the EXACT compact labelled destination. The proof does not claim per-primitive destination monotonicity of the temporary buffer.

Concatenate source exact preparation, this complete compact LOWER repair and reversed saved destination preparation. All joins are their actual tuples and both original full endpoints are exact four. The finite lower path might rise above four; it has finite upper bound r because roots stay nonempty. ONLY NOW apply baseline maximum-layer Theorem A on the native union-closed carrier. It yields a finite path with tau in {3,4} and the SAME full original labelled endpoints. Converted primitives can differ from the preliminary schedule.

This proves X24E. Repetition at another exact destination uses the same proved construction; renewal within the path requires restored incidence/buffer structure, not return to exact four after every macro.

## 6. What was removed and what remains

The new general protection statement preserves individual original-floor capacities and detects impossible equality using the actual shared blocks. The concrete consequence removes the separate strict-incidence hypothesis for every feasible nine-root eight-label mixed3/4 carrier: exact consistency supplies it automatically.

Every surviving pair in that carrier consequently belongs to the previously conditional X16R/X15N repair class. We do NOT claim a newly connected feasible pair that violated those accepted numerical inequalities; the advance is proving that the ostensibly missing budget is forced, and rejecting the equality case with a general witness-consistency obstruction. Nor is the pair-partition obstruction a native path obstruction: it excludes a proposed endpoint guard/profile, while all actual endpoints have complete repair.

Uniform X15/X20, X22 and X23 remain unchanged. Unresolved mixed3/4 carriers are still outside ALL accepted classes; for eight labels their root counts can now exclude r<=9. This is a consequence of derived guard structure, not an invitation to run separate root-count campaigns. Seek stronger individual-grade consistency or reusable coupled handover beyond these sufficient domains.

Original destination-directed scheduling, arbitrary mixed floors/higher targets, unrestricted nested universality and physical interpretation remain open. Conditional child lifting retains inherited exact-child interfaces and fixed-root clearance. Unit repair is an upper bound, not a positive minimum for every pair. Ordered repair and retained recoverability do not introduce fundamental time.

Dependencies read at the parent analytical publication: A11_X14_SATURATED_INCIDENCE_RENEWAL.md Sections 2–7; A11_X15_UNIVERSAL_FLOOR_THREE_REPAIR.md Sections 1–6; A11_X16_PALETTE_GUARD_BOUNDS.md Sections 2–4. Exact compaction and maximum-layer A are read at baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, demos/v16.54-parent-support-connectivity/GENERAL_PARENT_CONNECTIVITY.md Sections 1–3 and 6. Frozen sources and applicable domains are checked, not rewritten or recertified.

No scientific enumeration, numerical tests, workflows, implementation, benchmark or run IDs. No certified integration merge. v16.55 remains OPEN with prospective execution, independent reconstruction/rejecting controls, inherited stack, reproduction/durable evidence, exact review and post-merge audit gates unsatisfied. Certified v16.54 and accepted separate efficiency design remain unchanged; efficiency runner execution and measured speedup remain unstarted.
