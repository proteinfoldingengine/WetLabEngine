# A11.X36 — reusable interleaved ownership cycles when every whole-root order fails

Scope freeze: 4bdd30b3dac6ef539bcf42d704d5b42b5746419b.
Analytical parent: f0753c98c1ac2d21e24b9d0c2ed80248024c1741.
Status: exact candidate for fresh independent whole-argument review. Analytical only.
Completed bounded v16.55 and certified v16.54 remain unchanged.

## 1. Statements, native carrier and comparison

Fix a finite ordered palette P, q>=3 labelled ACTUAL root slots, and ORIGINAL floors a_i>=1. Every E_i is a subset of P of size at least a_i. A primitive adds or removes ONE incidence in ONE root. Let A,C be exact-q endpoints on these q slots: r=q. Supports may exceed floors and may leave labels unused. The conclusions below include arbitrary unequal original floors.

**X36I — derived interleaved completion.** There is a deterministic native A -> C path with tau in {q-1,q}. It uses exactly the destination additions C_i minus A_i and source deletions A_i minus C_i, each ONCE; all common incidences remain fixed. At each primitive every ORIGINAL same-slot floor holds. It restores the FULL labelled/noncompact C. At completed exchanges the supports are pairwise disjoint; this renews the construction even if MANY roots still differ from BOTH original endpoints.

**X36W — actual unfinished-support protection.** During a direct transfer at most one label is duplicated across actual roots. During a cycle at most two labels are duplicated, and when there are two, their incidence links share an actual root. All other labels occur in at most one root. Any set of q-2 labels therefore hits at most q-1 roots. An actual missed root exists at EVERY primitive. At q=4 this explicitly supplies W_E(K) nonempty for EVERY two-label set K.

**X36O — no whole-root order.** Suppose q>=4 and A_i intersect C_j is nonempty for EVERY i,j. NO root ordering can safely complete each root once via its source-union-destination bridge before starting another, with tau>=q-1. For target4, every order's two-completed/two-old boundary has an actual two-label hitting set. This excludes the precise A2/X35 whole-root method, not merely a chosen witness diagram or a failed sufficient inequality.

**X36P — unfinished participation really is necessary.** In that cross-intersecting family, EVERY native path retaining tau>=q-1 visits a state with at least q-2 roots differing from BOTH their OWN original source and destination supports. In particular target4 requires at least TWO unfinished roots on every such path, even with repeated changes and arbitrary larger supports.

**X36F — infinite unequal-floor target-four controls.** Section 7 specifies actual exact-four endpoints for every integer t>=2, with k=16t+1, four labelled slots and unequal ORIGINAL floors (4t,4t,4t-1,4t-2). Original source/destination size vectors are different. X36O/P apply, while X36I supplies complete native {3,4} repair. An explicit four-cycle exhibits two unfinished roots jointly protected at level3 and renews an exact4 partition with all FOUR roots unfinished relative to the original endpoints. Continuation to C is guaranteed from that restored structural boundary.

These are new SCHEDULING/RENEWAL statements within an already connected protected endpoint class. Accepted protected-root theorem J/K already connects these endpoints, including unused labels and variable part sizes, through a canonical partition. Its two-root swaps are a prior local interleaving mechanism. We do NOT claim newly established endpoint connectivity outside all prior theorems, universal arbitrary-r mixed-floor repair, or discovery of a native barrier. X36 derives a destination-directed completion for the entire r=q exact-q domain and a rigorous separation from EVERY source-union-destination root order, using a reusable multi-root cycle with no spare label or root.

The construction permits several roots to be unfinished. It does not impose destination monotonicity on native admissibility; it happens to solve this class inside A11's stricter destination-directed subclass.

## 2. Exactness forces a disjoint-support boundary

With q nonempty actual roots, tau<=q. If two roots intersect, one label hits both, and one label from each of the other q-2 roots gives a cover of size at most q-1. Consequently tau=q forces ALL q roots pairwise disjoint. Conversely q pairwise-disjoint nonempty roots require q labels and have tau=q.

Both original endpoints therefore have disjoint supports. Their sizes need not match, and neither need cover P. At a disjoint intermediate boundary E define an owner f_E(x) in {0,1,...,q}: the UNIQUE root containing x, or0 if x is unused. Destination owner g(x) is defined from C. Owner0 is only notation for unused palette labels; it is NOT an actual root, slot, buffer, floor change or new resource.

For each misplaced label x with f_E(x)!=g(x), put an arc f_E(x) -> g(x), labelled by x. There are no self arcs. Parallel arcs are allowed. Define D(E) as the number of misplaced labels. For each actual i, and likewise the bookkeeping index0,

    outgoing(i)-incoming(i)=|E_i|-|C_i|,

where E_0,C_0 are the unused-label sets. Labels correct at i cancel; every other current label contributes outgoing and every missing destination label incoming. This identity concerns the SAME actual label assignment, not separate capacities for each pair.

Every completed exchange below moves only misplaced labels to their ACTUAL destination. Already-correct labels are never moved. A new disjoint boundary is restored after each exchange.

## 3. Direct exchanges and original-floor eligibility

If an arc 0 -> j exists, add its unused label x to root j. It was absent everywhere, so the new boundary is disjoint. Floors are preserved. This fixes x.

For an arc i -> 0 with i actual, if |E_i|>a_i, remove x from i. All roots remain nonempty and disjoint, at their original floors. This fixes x.

For an arc i -> j with i,j actual and |E_i|>a_i, do these TWO primitives:

1. add x to j;
2. remove x from i.

The addition is genuine because current supports are disjoint. The donor's one-unit surplus proves the deletion floor. The intermediate has just one duplicated label x, belonging to i,j; every other label occurs at most once. Its transversal is q-1: x hits those two roots, one label from each remaining root supplies the upper bound, and no q-2 labels cover all roots. The completed state is again disjoint and exact q.

These exchanges supply a literal next primitive and fix a label. They do not require the donor to exceed its DESTINATION size, only its ORIGINAL floor. If that choice changes size in an inconvenient direction, the finite misplaced-label measure still decreases and the remaining destination continues to meet all original floors.

## 4. A cycle MUST exist in the blocked case

Suppose D(E)>0, no unused-label addition is available, and no misplaced actual donor has |E_i|>a_i. Then vertex0 has no outgoing arc. Every actual vertex with at least one outgoing arc has |E_i|=a_i, since E is legal. Because |C_i|>=a_i, the degree identity gives

    incoming(i)>=outgoing(i)>0.

Start with any outgoing actual vertex. Follow an incoming arc backwards to its predecessor; that predecessor is also an outgoing actual vertex. It cannot be0 because0 has no outgoing arcs. Continue backwards. Finitely many actual vertices force repetition, yielding a directed cycle among ACTUAL roots. Extract a simple directed cycle; it has length l between2 andq, since there are no self arcs.

Write it as i_1 -> i_2 -> ... -> i_l -> i_1, with arc labels x_1,...,x_l. These labels are DISTINCT, each currently in its own unique root i_t and destined for i_{t+1}; indices are cyclic. Distinctness follows from unique current ownership and the simple cycle's distinct source vertices.

Thus a decreasing exchange exists whenever D>0: a direct exchange, or a cycle derived from floor feasibility. No potential is supplied without next-move existence. For determinism use the palette/index orders to select the least eligible direct arc; if none, the least simple directed cycle and least labelled arc at each edge. A simple cycle may also be chosen earlier; the same proof applies even when a direct exchange is available.

## 5. Literal cycle edits and the coupled protection invariant

For the declared simple cycle, perform:

1. add x_1 to i_2;
2. for t=l,l-1,...,2, add x_t to i_{t+1}, then delete x_{t+1} from i_{t+1}, where x_{l+1}=x_1 and i_{l+1}=i_1;
3. finally delete x_2 from i_2.

For l=2 this is exactly add x_1 to i_2; add x_2 to i_1; delete x_1 from i_1; delete x_2 from i_2. For l=4 it is:

    add x_1 to i_2;
    add x_4 to i_1; delete x_1 from i_1;
    add x_3 to i_4; delete x_4 from i_4;
    add x_2 to i_3; delete x_3 from i_3;
    delete x_2 from i_2.

Every addition is to its actual destination and every deletion from its current source. No other incidence is touched. At completion each root on the cycle has received its incoming label and lost its outgoing one, so its boundary SIZE is unchanged and all these labels are fixed.

### Floors, presence and shared capacity

Each root receives its incoming label BEFORE its outgoing label is deleted. The initial recipient i_2 retains the added x_1 until its own outgoing x_2 is deleted last. Other roots first receive one label, then lose their outgoing label. Their sizes are always either their starting boundary size or that size+1. Every original same-slot floor holds, including unequal floors and roots exactly at their floors. Each addition's label was absent at that root, and its deletion's original source copy has not previously been removed. There is no independent-capacity allocation to different pair obligations.

### Actual duplicated-label links

After the first addition the only duplicated label is x_1, whose incidence link is {i_1,i_2}. Before the first loop deletion the duplicated labels are x_1 and x_l, with links {i_1,i_2} and {i_l,i_1}; they share i_1 (for l2 they have the SAME two indices). The deletion removes the old x_1 copy, leaving ONLY x_l duplicated.

At each subsequent loop addition the old duplicated label x_{t+1} has link {i_{t+1},i_{t+2}} and the new duplicate x_t has link {i_t,i_{t+1}}; they share i_{t+1}. Deleting x_{t+1} from i_{t+1} leaves only x_t duplicated. The last deletion removes the last duplicate. All indices here are cyclic. At no time is there a label on three roots, or two duplicated-label links on disjoint pairs of roots.

This is a maintainable structure of ACTUAL partial supports, not an old/new root classification. A root's two concurrent labels can protect several obligations jointly; their real incidence links are used once, with the real root cardinality above. No witness is assigned an independent share of a root's floor.

### Every forbidden set and every actual pair witness

For any label z define I_E(z)={i:z in E_i}, including the possibility of an empty set. All I_E(z) have size at most1 except the at-most-two duplicated labels. If a set H contains one duplicated label, the union of its incidence sets has size at most |H|+1. If it contains two, the duplicated-label links share a root, so those two labels cover at most THREE roots; every other label adds at most one. Again

    |union_{z in H} I_E(z)|<=|H|+1.

Thus |H|=q-2 implies that at least one of the q actual roots is missed. At q4, for EVERY pair K={x,y}, choose the least actual index outside I_E(x) union I_E(y). It exists, its current support actually avoids K, and it is an explicit member of W_E(K).

This simultaneously covers every pair inside any label grouping, mixed pairs and all other pairs. It uses the SAME actual incidences for all obligations. It is not a per-step numerical hitting-number recalculation.

The resulting lower bound is tau>=q-1. Nonempty q roots give tau<=q. Whenever one duplicated label exists, using it and one label from every other root gives tau<=q-1. With two adjacent duplicated labels, they hit at most three roots but actually hit the two or three incident roots; choose one label from each remaining root, yielding at most q-1. Thus every state with a duplicate is exactly q-1, and every disjoint boundary is exactly q. This includes floor-saturated cycles. No upper-layer conversion is required for this construction.

### Why the next unfinished edit remains eligible

At each interior cycle prefix the displayed finite remaining list supplies the next present deletion or absent addition, with the incoming-before-outgoing floor certificate. The one-/two-adjacent-link invariant persists after that primitive. A level-(q-1) prefix therefore has certified continuation, even while several roots are unfinished. This does not claim every arbitrary safe prefix has an extension.

## 6. Renewal, termination and exact destination restoration

A completed direct exchange fixes one misplaced label. A completed cycle fixes l distinct misplaced labels and moves no correct label. Every completed boundary again has disjoint nonempty supports at ORIGINAL floors. Recompute the owner graph from those ACTUAL supports; the proof of Section4 supplies the next exchange whenever D>0. No last reserve is spent: the renewed resource is this assignment and duplication-link structure, not an untouched independent old guard.

D is a nonnegative integer and decreases at every completed exchange. Every exchange has finitely many legal primitives (one/two for a direct exchange,2l for a cycle), so repetition terminates. D=0 means every palette label has its full destination ownership, including all unused labels. Therefore E_i=C_i for EVERY labelled slot; original noncompact support sizes and common incidences are fully restored.

Each destination-only incidence is added exactly once and each source-only incidence deleted exactly once. A completed correct label never moves again. Therefore the total primitive count is

    N=sum_i |A_i symmetric_difference C_i|.

Every primitive also removes one still-pending endpoint incidence event. This is a mathematical minimum primitive count, since any path between the endpoints must toggle every differing incidence at least once. It is NOT an executed benchmark, implementation timing or numerical campaign.

Any finite specified chain of exact-q endpoints on these same q actual slots and original floors admits repeated X36I repairs. Each complete endpoint is restored before the next ownership graph is formed. Exact-q boundaries are available in this particular mechanism; no claim makes an exact reset necessary for other renewable mechanisms. Internally, the cycle certificate renews progress at level q-1.

For target4 the construction is directly within{3,4}; no A application is needed. If a future generalization establishes only a complete lower path on a larger carrier, A may be invoked only AFTER completing that path between original exact endpoints, with its union-closed positive-floor domain checked. No conversion of an unfinished prefix is assumed here.

## 7. Every whole-root order fails: explicit unequal-floor controls

### 7.1 General cross-intersection obstruction

Take q>=4, disjoint exact-q endpoints with EVERY A_i intersect C_j nonempty. In a chosen whole-root order, inspect the boundary after exactly TWO roots have completed to their destination supports. There are two completed-new roots and q-2 unchanged-old roots. Pair those two new roots with TWO distinct old roots. Each selected old/new pair has an actual intersection label. These two labels hit the paired four roots; one label from every remaining q-4 old root hits everything. The boundary therefore has tau<=q-2, violating tau>=q-1.

For q4 this uses exactly two intersection labels and proves a forbidden two-cover. The argument applies to EVERY ordering and is independent of alternative witness choices.

It also directly violates the X35 exact criterion. For q4 let J={j,h} be the first two completed indices and I={i,l} the other two. Choose x in A_i intersect C_j and y in A_l intersect C_h. They are distinct because the source parts are disjoint, and lie in different destination parts. The pair K={x,y} has ACTUAL U_K=J and V_K=I. Thus ALL old witnesses have changed before ANY new witness completes: first(V_K)>last(U_K). No common or alternative witness is overlooked. The pair chosen may depend on the tested root ordering; that is sufficient to exclude all orders.

Whole-root unions may use arbitrary addition/deletion orders within their specified add-all-then-delete bridge. The already visited completed boundary defeats them regardless. The obstruction does not exclude interleavings, repeated roots, arbitrary temporary supports or other native routes.

### 7.2 Every lower path needs several unfinished roots

Classify each actual slot at a state E relative to its OWN original endpoints: old if E_i=A_i, new if E_i=C_i, otherwise unfinished. The endpoint supports at a slot are different: complete cross-intersection with q disjoint source/destination parts gives at least q-1 labels in A_i minus C_i and at least q-1 labels in C_i minus A_i. In particular no one-incidence primitive can change directly from old to new or vice versa.

Write their counts o,n,d, with o+n+d=q. Every old source root intersects every new destination root. Pair min(o,n) old/new roots and choose one actual intersection label for each pair; choose one label from each unpaired or unfinished nonempty root. Thus

    tau(E)<=max(o,n)+d.

Along any native one-incidence path the integer n-o changes by at most1 at each primitive, starts at-q and ends atq. It visits0. At that state o=n=(q-d)/2. Lower protection implies

    q-1<=tau(E)<=(q+d)/2,

so d>=q-2. This includes ANY repeated changes, nonmonotone schedules, larger intermediate supports and all original positive floors. It is the inherited participation counting IDEA specialized and sharpened at r=q, not a claim the earlier r=m+1 higher-target theorem already supplied this target4 control. It is not a barrier above one: X36I supplies the unit-band repair.

### 7.3 Parameterized target4 family and supplied minimum covers

For every integer t>=2 declare DISJOINT label cells B_ij for 1<=i,j<=4. Every cell has t labels except B_12, which has t+1. These are just named subsets of the finite ordered palette P; no new geometric native rule. Then k=16t+1. Set

    A_i=union_j B_ij,
    C_i=union_j B_ji,
    ORIGINAL floors=(4t,4t,4t-1,4t-2).

The source size vector is(4t+1,4t,4t,4t) and destination size vector(4t,4t+1,4t,4t). All supports meet the SAME original floor vector, whose unequal values are at least6. No slot/label/floor changes during repair.

Both endpoints partition P into four nonempty actual supports, so tau=4. Choosing one label from each A_i gives an actual minimum four-cover of A; one from each C_i gives one for C. Every A_i intersect C_j=B_ij is nonempty. X36O excludes EVERY whole-root order, and X36P forces at least TWO unfinished roots on every lower-protected path. The source/destination support size multisets happen to agree, but individual sizes change at labelled slots; no permutation is used by X36I.

Choose x_1 in B_12, x_2 in B_23, x_3 in B_34, x_4 in B_41. They form a misplaced four-cycle1->2->3->4->1. Begin its legal exchange at A even if a direct exchange is also eligible. After add x_1 to2 and add x_4 to1, the duplicated links are{1,2} and{4,1}. These are ACTUAL partial supports at two unfinished roots. The set consisting of x_1,x_4 and any label of the unchanged root3 hits all roots; no pair does by Section5. Hence this prefix is exactly tau3. The next literal edit is delete x_1 from1, whose added x_4 already supplies its floor replacement.

Finish the displayed eight-primitive cycle. The roots are again a disjoint partition and exact4, each having one correctly delivered label and having lost one misplaced label. All FOUR roots are now unfinished relative to their own original A_i,C_i: each differs from A_i by that exchange and still contains labels from other B_ij cells that lie outside C_i (t>=2). No root has completed its original destination. Nevertheless the renewed ACTUAL disjoint-support certificate guarantees another eligible exchange and complete termination at C.

This is repeated repair through several unfinished roots, not a single successful local move. The direct/cycle algorithm handles EVERY subsequent actual boundary and preserves original floors even where its donor is saturated. It is finite for every t, not a numerical sample.

The whole endpoint union tuple has tau<=2: choose a label in B_12 and one in B_34; these hit unions at indices1,2 and3,4 respectively. Therefore no subfamily of these ACTUAL union roots is a three-guard. This excludes using those unions as an unchanged guard; it does not exclude auxiliary contracted supports or other prior protected-root repairs. Several partial supports carry the protection instead.

## 8. Dependencies, novelty, limitations and review checklist

Inherited sources are frozen:
- A2 SEQUENTIAL_HANDOVER.md, blob b754237cf56ab4592eec82c81ebf00817f85ab43, and X35 candidate974d0356b78c294804c3db49686e1e0f32dcd90a/proof blob d180465540c1fcc4abb282cfc386933f9515caf6: the exact chosen whole-root criterion. X36 excludes EVERY such order on its controls rather than failing a sufficient count.
- I11 A11_GLOBAL_SCHEDULE_REDUCTION.md, blob02324d7054b847a0c105b95e2eec3e918483b0d1: destination-directed unique endpoint incidence events, floors and actual pair-protection intervals. X36 derives their joint feasible schedule on r=q exact-q endpoints; it does not merely restate interval feasibility.
- Certified v16.54 PROTECTED_EXCHANGE.md at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, blob c74251d4823c468effe2f56a59215f1d141c07ba: J/K already give unit-band connectivity, partition leveling and two-root swap repair. X36 acknowledges those prior constructions. The additional destination-directed cycle availability, full endpoint-event restoration and NO-whole-order/necessary-participation separation are the claims here.
- UNBOUNDED_REPAIR_PARTICIPATION.md, blob bdab80fa21cf830f5ee012f616d075489ef93e57: endpoint-relative counting technique and warning that fixed buffer participation cannot be universally complete. X36 does not claim a fixed two-duplicate invariant suffices on arbitrary carriers; its disjoint r=q domain is crucial.
- Maximum-layer A, GENERAL_PARENT_CONNECTIVITY.md at the same certified baseline, blob922ae44713c6810c5a99716c52ecb37738a880a6: direct band bounds make conversion unnecessary here. No unfinished-prefix conversion is invoked.

No maximum-degree, global symmetry, arbitrary mixed-floor root permutation, exact compaction, guard-buffer, palette-room or element-cover lemma is assumed by this proof. Their accepted conclusions, including connectivity of this protected class, remain valid. Palette size permits all given supports; no spare unused label is required by the blocked cycle. The temporary duplications come only from existing destination incidences.

The theorem is restricted to r=q, where exactness forces disjoint supports; r=q4 controls are also protected under J. It does not resolve overlapping exact endpoint supports at r>q, arbitrary mixed-floor root universality, higher-target arbitrary-r universality, unrestricted nested repair, or all A11 destination-directed scheduling. Extending the adjacent-link invariant to genuinely overlapping endpoints must account for pre-existing shared incidences; they cannot be ignored or independently allocated. Failure of X36's structural hypothesis is not disconnection, and a failed proposed interleaving is not proof no native route exists.

Scientific interpretation: unfinished roots can jointly maintain a reusable protection structure while completing one another. The precise mechanism is incoming-before-outgoing replacement plus adjacent duplication links, derived next-cycle availability and strict completed-exchange progress. It adds no physical energy/metric/gravity or fundamental-time claim. Originality relative to mathematical literature is not established.

Review must check the obstruction and positive construction on the SAME carrier, all pairs and shared capacities, original floors at each actual primitive, source/destination differences and unused labels, blocked-case cycle existence, literal continuation at level3, renewal through unfinished roots, finite termination, exact labelled/noncompact restoration and inherited novelty domains. No numerical execution, tests, run IDs, implementation/benchmark, integration merge or new numbered certification. Completed bounded v16.55 and separate unstarted efficiency work remain separate.
