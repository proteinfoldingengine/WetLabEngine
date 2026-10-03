# Accepted connectivity classes and remaining obligations

Source baseline: `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`, under `ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/`. Historical proof headers say candidate; their separate independent review records and final closeout govern acceptance. The original files are unchanged. This ledger summarizes scope, not a new certification of their implementations.

All statements concern fixed palette, labelled slots and positive floors. Unless stated otherwise, the output for two permitted exact-q endpoints is a primitive path with transversal in {q-1,q}.

| Accepted result / source | Required input | Output and boundary |
| --- | --- | --- |
| Targets 1 and 2; GENERAL_PARENT_CONNECTIVITY | Any feasible same-carrier endpoints | Direct expansion/contraction; target 1 stays exact |
| Upper-excursion removal; same source, A | A finite path maintaining tau>=q-1 between exact-q endpoints | Converts to the desired band; does not supply the lower-guard path |
| Arbitrary-arity target 3; same source, D | Exact target 3 | Element-cover buffering plus upper removal; not arbitrary pair-cover connectivity |
| Five-child target 4; same source, F | r=5, exact target 4 | Degree-two cycle buffering or saturated partition exchange |
| Saturated capacity; EXACT_ENDPOINT_CAPACITY, H/I | delta=sum_i(k-a_i)-(q-1)k=0, q>=3 | Classifies full roots plus a partition and connects all such endpoints; positive delta remains separate |
| All floors 2; FLOOR_TWO_CONNECTIVITY, O | a_i=2 for every slot | Graph star edits and renewed symmetrization reach a common form |
| Mixed floors 1/2; SINGLETON_ANCHOR_REDUCTION, Q | Every floor belongs to {1,2} | Anchor/residual-graph reduction; does not cover arbitrary higher floors |
| Enough singleton anchors; same source, P | At least q slots have floor 1 | Other floors may be arbitrary; reaches protected class |
| Renewable singleton anchors; A11_RENEWABLE_SINGLETON_ANCHORS, X2 (separate analytical branch) | q>=4, at least q-2 ORIGINAL floor-one slots | Arbitrary remaining positive floors; finite renewed guard path plus accepted upper removal; temporaries/repeated toggles allowed |
| Residual target-three anchor lift; A11_RESIDUAL_THREE_ANCHOR_LIFT, X3 (separate analytical branch) | q>=4, at least q-3 ORIGINAL floor-one slots | Arbitrary remaining positive floors; common residual carrier plus inherited target-three D, symmetry L and upper removal A; temporaries/repeated toggles allowed |
| Pair-anchor target four; A11_PAIR_ANCHOR_CONNECTIVITY, X4 (separate analytical branch) | q=4, at least one ORIGINAL floor-two slot | Arbitrary remaining positive floors; derived strict slack and direct residual {2,3} path lift to {3,4}; temporaries/repeated toggles allowed |
| Preserved pair-anchor profile; same source, X4H | q>=4, q-4 ORIGINAL floor-one slots plus a DISTINCT floor-two slot | Arbitrary other floors; preserved residual floor-two profile uses X4, then inherited upper removal; no universal target-four premise |
| Conditional triple anchor; A11_TRIPLE_ANCHOR_RENEWAL, X5 (separate analytical branch) | q=4, same original floor-three slot; each endpoint has a supplied compact triple meeting a minimum four-cover, and actual avoiding roots of residual transversal at least two | Direct {3,4} path for arbitrary other positive floors; strict-slack OR saturated residual capacity; three existing reserves renew each saturated owner swap; guard existence not universal |
| Protected roots; PROTECTED_EXCHANGE, J/K | Each endpoint has q pairwise disjoint roots | Connects that class; its existence requires sum of q smallest floors<=k, but accessibility from every endpoint is not proved |
| Safe symmetry exchanges; OVERLAPPING_CLIQUE_EXCHANGE, L/M | Label permutation, or root permutation with destination-compatible floors, at exact q | Connects symmetry-related endpoints, not arbitrary overlap types |
| Contraction clone guard; CONTRACTION_CLONE_GUARD, U/V/W | Slot-compatible prescribed clone; retained-family cover f and contraction cover lambda | Exact formula tau(new)=min(1+f,lambda); eligible clones or a globally terminating sequence are not guaranteed |
| Uniform modules; HYPEREDGE_STAR_RELOCATION, Y | Complete h-uniform cores on a partition, h>=3, q=k-m(h-1)>=3; extra roots contain core roots | Connects endpoints of this type at fixed r,k,h,q; not a universal normal form |
| Cyclic triples; CYCLIC_TRIPLE_CONNECTIVITY, AA | Three nonempty palette parts, all internal triples and directed AAB/BBC/CCA core triples, floor 3, redundant extras, k>=6 | Connects this class at fixed r,k and q=k-3; not all triple systems |
| Disjoint compatible guards; GUARD_BUFFER_CONNECTIVITY, AB | Actual t=q-1 guards on disjoint index sets | Two-phase handover for arbitrary floors; extended to one shared slot by the present candidate |
| Uniform slot bound; same source, AC | Uniform h, r>=2N with N=binomial(h+q-2,h) | Small guards can occupy disjoint existing slots; present candidate improves to 2N-1 |
| Palette room; PALETTE_SLACK_CONNECTIVITY, AE | k>=sum_i a_i | Split shared labels using currently unused labels already in P; does not follow from complementary capacity |
| Finite-support reduction; FINITE_SUPPORT_REDUCTION, AD | Compact endpoint pair, S=sum_i a_i | Preserves connectivity answer on a suitable subpalette of size<=3S+1; finiteness does not imply connectivity |

The exact-endpoint hierarchy supplies |N_A(X)|>=q-|X| and the local capacity inequalities. One-root replacement consumes at most one lower-guard unit, but the completed state need not renew exact redundancy. Complete-module normal forms are genuinely unavailable in some exact higher-floor carriers (MODULE_CAPACITY_OBSTRUCTION); those examples are not disconnection results and the cyclic class has its own successful method.

The present candidate targets a missing link: protection can transfer through one shared root, without requiring disjoint guards or palette room. The unresolved problem is a generally available, renewing exchange when multiple shared slots admit different missed-root sets. An exact characterization of one bridge's failure does not resolve general connectivity.

## A11.X2 extension and current boundary

A11.X2 is independently accepted at candidate 1cd572d2e90ba3880dc5598d260c14e8a92acc5c, receipt INDEPENDENT_A11_ANCHOR_REVIEW.md. It lowers the sufficient arbitrary-other-floor singleton count from q to q-2. It is not merged implementation certification or a change to the integrated baseline sources.

For q=4, two original floor-one slots now suffice for native one-unit connectivity of every exact-four endpoint pair. A11.X1's large carrier is therefore covered as a full native class. The proof supplies renewable protection and unconditional finite progress within this class. It does not guarantee destination-directed incidence monotonicity.

The original q=4/uniform-floor-three diagnostic has zero singleton-capable slots and remains OPEN unless its individual parameter class is already covered elsewhere in this ledger. Fewer than q-2 singleton-capable slots are not declared universally unresolved: previously accepted results still apply. No minimal-anchor necessity or universal root/nested closure is claimed.

## A11.X3 stronger sufficient class

A11.X3 is independently accepted at candidate d2f79a71983a135eb035ef4d4c1289bdf6409814, receipt INDEPENDENT_A11_RESIDUAL_REVIEW.md. It improves the sufficient arbitrary-other-floor count to q-3. For q=4, a SINGLE original floor-one slot suffices for native one-unit connectivity of all exact-four endpoint pairs. X2 remains correct and retains its separate six-move renewable-guard mechanism.

The new ingredient is a common residual carrier: every nonanchor slot with floor <=k-(q-3) can be prepared inside the complementary palette; larger-floor slots necessarily intersect the forced anchors and are redundant. Higher residual levels descend to exact three before the ALREADY accepted target-three theorem is invoked. Dependency applicability was reviewed; no baseline theorem is newly discovered or recertified.

Any remaining exact-four native counterexample, IF one exists, must have zero original floor-one slots. This does not declare every zero-anchor carrier unresolved: all earlier graph, protected, symmetry, palette-room, slot-bound and other sufficient classes remain valid. Original uniform-floor-three diagnostics outside those classes remain OPEN. Universal A11 destination-directed scheduling and general root/nested universality remain OPEN. No minimal or necessary anchor-count threshold is asserted.

## A11.X4: completed pair-anchor native connectivity

For target four, ONE ORIGINAL floor-two slot suffices for native one-unit connectivity of ALL exact-four endpoint pairs, with arbitrary positive floors elsewhere. Together with X3, every carrier containing an original floor one OR two is covered. Any hypothetical remaining native exact-four counterexample must have ALL floors at least three; none is claimed.

Compact and align the pair root T. Actual roots avoiding both pair labels have residual transversal two or three, and their complements cover every outside label. Exact-four endpoint triple coverage forces strict total residual capacity greater than the outside palette size. The inherited element-cover owner construction then transfers protection in a common labelled residual carrier. A separate upper-bound argument proves every residual primitive stays in {2,3}, so the main theorem lifts DIRECTLY to {3,4}, with finite progress and exact labelled restoration.

For q>=4, q-4 original floor-one slots PLUS a distinct original floor-two slot also suffice. This corollary preserves a specific residual floor profile before invoking X4; it assumes no universal target-four theorem. Main dependencies C/L and corollary A/X3 are inherited and domain-checked, not recertified.

A fixed triple anchor does not inherit this one-family preparation: the all-twenty-triples example would prepare to level two, but is itself already covered by the accepted uniform-slot theorem AC. This is a method failure, not disconnection. Renewal of THREE overlapping pair-indexed protection systems with shared capacities remains unresolved. Exclude other accepted classes before identifying an unresolved all-floor-at-least-three domain.

Evidence: A11_PAIR_ANCHOR_SCOPE.md; A11_PAIR_ANCHOR_CONNECTIVITY.md; INDEPENDENT_A11_PAIR_REVIEW.md; A11_PAIR_ANCHOR_CLOSEOUT.md. Candidate 6525e708393c345b01e2004163fcc738f1e4d486, independently ACCEPTED without corrections. Temporaries/repeated toggles are permitted; universal A11 destination-directed scheduling and general root/nested universality remain OPEN. Native lifting retains accepted child interfaces. No numerical campaign, implementation or new certification is assigned.


## A11.X5: conditional triple-anchor renewal without residual slack

At target four, a SAME ORIGINAL floor-three slot suffices for native {3,4} connectivity under an explicit endpoint condition: each endpoint supplies a compact triple inside that root meeting a minimum four-cover, and the other actual roots avoiding that triple have residual transversal at least TWO. This condition is not asserted universally.

Both endpoints prepare to the same labelled residual floor carrier, with actual residual transversal two or three. If residual capacity is strictly larger than the residual palette, inherited element-cover owner transfers apply with their upper band separately checked. If capacity is exactly saturated, exact-four triple coverage forces THREE existing ORIGINAL floor-n slots, n the residual palette size. Temporary attachments of two anchor labels let those roots jointly protect two temporarily ownerless outside labels. A four-incidence owner swap is followed by restoration of all three reserves, so the next swap remains available. The misplaced-owner count strictly decreases; every primitive stays DIRECTLY in {3,4} and every labelled destination support is restored.

This proves renewing protection at saturated residual capacity without creating a slot or label. The actual avoiding-root guard condition remains essential to this theorem's input, not a proved necessary condition for connectivity. Endpoints lacking a supplied qualifying compact triple remain outside X5 unless another accepted class applies. The twenty-triples example fails this guard condition but is already solved by AC, so is not a new unresolved domain.

Evidence: A11_TRIPLE_ANCHOR_SCOPE.md; A11_TRIPLE_ANCHOR_RENEWAL.md; INDEPENDENT_A11_TRIPLE_REVIEW.md; A11_TRIPLE_ANCHOR_CLOSEOUT.md. Candidate 3857dfcc33eccb2c01456a1273426ab9dd94bade. Inherited C/L and X4's residual band argument are domain-checked, not recertified; no universal floor-two theorem is misapplied to the residual carrier. X3/X4's universal target-four class with an original floor one or two remains accepted. A11 universal destination-directed scheduling, remaining floor-three cases outside accepted classes and general root/nested universality remain OPEN. Temporary incidences/repeated toggles are allowed; child-interface conditions govern native lifting. No numerical campaign or implementation certification is assigned.


## A11.X6: sharp X5 target-existence boundary

On the seven-label uniform-floor-three carrier, the X5-qualified exact-four class G_s is nonempty at any chosen labelled slot if and only if r>=13. Exact compaction retains the supplied minimum four-cover and guard; four residual triples plus coupled mixed-triple witness counting force thirteen slots. An explicit thirteen-slot state attains the bound. Therefore ALL G_s are empty at r<=12, allowing every floor-permitted support size. A cyclic (3,2,2) core supplies a feasible exact-four twelve-slot control, already connected within accepted AA. This is an empty-target obstruction to Route A, NOT native disconnection. For six labels exact four requires at least twenty slots; G_s is empty for any r, and the all-twenty-triples control is already solved by AC.

No arbitrary accessibility or new universal repair theorem is proved. At seven labels/r>=13, existence is distinct from reachability; at seven labels/r=12 a replacement mechanism must avoid reliance on X5's all-triple-avoiding family. Other accepted classes remain valid. Larger palettes, A11 destination-directed scheduling and unrestricted native/nested universality remain OPEN. No scientific run or implementation is initiated.

Evidence: A11_X6_SCOPE.md, A11_X6_GUARD_ACCESSIBILITY.md, INDEPENDENT_A11_X6_REVIEW.md and A11_X6_CLOSEOUT.md. Candidate 442fb7b839425a96b2ae248616b944f56f1229a0. This is analytical source freezing and review, not numerical preregistration.
