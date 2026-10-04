# A11.X37 — shared-role cycle renewal through genuinely overlapping roots

Scope: 0bcd78348096d477936db8c32fc8963ce51fbd45.
Parent: 0ac4e31b0dc1e0f9082429ddc077e39590ac78f6.
Status: exact analytical candidate for fresh independent whole-argument review.
No scientific execution, implementation or numbered certification.

## 1. Typed statement and openly sufficient hypotheses

Fix a finite ordered palette P, r labelled ACTUAL roots and their ORIGINAL positive floors a_i. The primitive toggles ONE incidence in ONE actual root. Larger supports and temporary/repeated incidences remain native permissions.

A supplied incidence certificate consists of m>=4 named groups and a nonempty subset Q_i of {1,...,m} at each actual root, with template transversal EXACTLY FOUR: every three group indices are avoided by some actual Q_i, and a supplied four-index set H meets every Q_i. Groups are names for actual label-incidence roles, not new native geometry, slots or primitives.

Source B_1,...,B_m and destination D_1,...,D_m are partitions of the SAME P, with nonempty group sizes |B_j|=|D_j|=b_j. The ACTUAL endpoints are

    A_i=union_{j in Q_i} B_j,
    C_i=union_{j in Q_i} D_j,
    N_i=sum_{j in Q_i} b_j.

They can overlap heavily. Require a_i<=N_i for singleton Q_i, and a_i<=N_i-1 for every multigroup Q_i. The latter is ONE existing incidence above the SAME original root floor; it is NOT a weakened floor. All actual original floors are positive.

**X37L — complete shared-role lift.** These endpoints admit a finite destination-directed native path with3<=tau<=4, restoring EVERY original labelled support C_i. Each original destination-only incidence is added ONCE, each source-only incidence deleted ONCE, and every common incidence retained.

**X37C — coupled cardinality and pair witnesses.** Along its logical cycles any actual union-template support has size at least N_i-1; singleton templates never fall below N_i. At every physical primitive EVERY palette pair misses an actual root. The same shared incidences jointly enforce cardinalities and witnesses; capacities are not allocated independently per obligation.

**X37R — renewal and eligible progress.** Every completed cycle restores all group cardinalities b_j and all actual root sizes N_i, renewing the original-floor reserve even when roots remain unfinished relative to A,C. Whenever a label's group assignment is incorrect, a proved eligible simple cycle exists. Incorrect labels strictly decrease across finite completed cycles; literal packet edits provide continuation inside them, including at level3.

**X37O — overlapping EVERY-whole-order separation control.** Section5 gives an infinite genuinely overlapping endpoint family, with r8 actual roots and unequal original floors, for which EVERY one-pass whole-root source-union-destination order fails, while X37L completes the repair. This family has four private template roots and is already protected under J; no contrary claim is made.

**X37F — no private-root guard needed for the lift.** A second infinite family has r20 actual overlapping roots, template all triples on six groups, unequal high original floors and EXACT FOUR. No four disjoint floor-safe actual roots fit ANYWHERE on its fixed carrier. Its whole endpoint union has a two-cover, yet X37L supplies complete destination-directed renewal. This control is NOT claimed to have no whole-root order; it establishes a different structural gain.

**X37S — sharp one-incidence bound for the chosen method.** The second control with saturated original floors N_i instead has a declared four-cycle that cannot be lifted by ANY rotation of the prescribed adjacent-link packet procedure: a shared root loses one actual incidence while its nominal replacement was already present through another role. This is a rigorously characterized obstruction to that METHOD, not native disconnection.

All these endpoint classes are already symmetry-connected by accepted palette exchange L: equal group sizes permit a palette bijection mapping each B_j to D_j. The new statement is a derived DESTINATION-DIRECTED, incidence-minimal, reusable unfinished-support interface with explicit coupled floor accounting, extending X36 beyond disjoint endpoint roots. Connectivity novelty, general A11 scheduling, arbitrary overlapping templates, arbitrary mixed-floor or nested universality are not claimed.

## 2. Exact endpoints and the actual owner graph

At an endpoint each label has exactly one group owner, while an actual root may contain labels from MANY groups. A transversal of actual roots yields group owners hitting every Q_i. Thus it needs at least four labels. Conversely choose one label from each nonempty group indexed by H; these four labels hit all actual roots. Both endpoints are EXACT FOUR, with supplied actual minimum covers. No compaction or removal of minimum-cover labels occurs.

At a structural boundary E keep a partition L_1,...,L_m with |L_j|=b_j, and actual supports E_i=union_{j in Q_i}L_j. For every misplaced label x draw the arc from its current group p to its destination group q. Correct labels give no arc. Incoming minus outgoing at every group is zero, because current and destination cardinalities agree. If any arc remains, a vertex with an outgoing arc also has an incoming arc. Following outgoing arcs, with balanced nonzero degrees at visited vertices, produces a directed cycle in the finite group-index graph. Extract a simple cycle; choose its least index/labels deterministically. The distinct cycle arc labels x_1,...,x_l have distinct current owners i_1,...,i_l, and destination owners i_2,...,i_l,i_1, with l>=2.

The graph uses label GROUP indices, not added actual root slots. Unlike X36, groups do not represent independent native roots or independently usable capacity. The floor calculation below is on each ORIGINAL actual Q_i simultaneously.

## 3. Logical cycle, exact shared-size bound and physical packets

Use X36's logical list:

    add group-role i_2 to x_1;
    for t=l,l-1,...,2:
        add group-role i_{t+1} to x_t;
        remove group-role i_{t+1} from x_{t+1};
    finally remove group-role i_2 from x_2.

Indices are cyclic, x_{l+1}=x_1, i_{l+1}=i_1. A role addition/deletion here is bookkeeping, NOT a native simultaneous edit. Section3.3 supplies all actual single-incidence primitives.

Every logical group receives its incoming label before losing its outgoing label. At completion the partition and all b_j are restored; cycle labels now have their destination owners. During the cycle each label occupies one group or, for at most two labels, two groups. With two duplicated labels their two group links share a group. For l2 the two links coincide.

### 3.1 Exact logical union sizes

Let c=i_2 be the initial recipient. At a phase with ONE duplicated label on link{u,v}, the group cardinalities differ from boundary values ONLY by one extra label in group c. For any actual template Q,

    |union_{j in Q} L_j|
      = N_Q + 1(c in Q) - 1(u in Q and v in Q).

There is just one duplicate to subtract. This is at least N_Q-1.

At a phase with TWO duplicate links{u,v},{v,w}, the extra group occupancies are one in c and one in the common group v. Their groups are distinct in the declared cycle. Subtract the two duplicated labels, separately even if the links coincide:

    |union_{j in Q} L_j|
      = N_Q +1(c in Q)+1(v in Q)
        -1(u in Q and v in Q)-1(v in Q and w in Q).

The last three terms equal
1(v in Q)*(1-1(u in Q)-1(w in Q)), at least-1.
Thus this union also has size at least N_Q-1. At unduplicated boundaries it has size N_Q.

For singleton Q no link's two distinct endpoints lie in Q, so the negative terms vanish; its size never falls below N_Q. For multigroup Q the single original incidence reserve N_Q>=a_i+1 suffices at ALL phases. This is a joint count on the SAME actual root, including the fact that a replacement label can already be present through another group. It is not one reserve assigned separately to each edge or forbidden pair.

### 3.2 Every actual pair through unfinished supports

For a label x let F(x) be its currently active group indices. They have size one or two. At most two labels have size two, and their links share an index. Therefore for EVERY two-label set K,

    |union_{x in K} F(x)|<=3.

Since template transversal is four, an ACTUAL Q_i avoids that union. The actual union support at i misses K. This covers two ordinary labels, one duplicate plus an ordinary label, both duplicates together, and all possible group locations, simultaneously. The least such actual index can be selected as an explicit pair witness.

### 3.3 Lifting a role packet to actual primitives

For a logical addition of a role v to a currently single-role label x at u, add x individually at every actual root whose Q_i contains v but NOT u, using the actual root order. Roots containing both already have x, and roots containing neither are untouched. Each addition is genuinely absent.

For a logical removal of role u from a duplicated label x at{u,v}, delete x individually at every actual root whose Q_i contains u but NOT v. Roots containing both retain the common actual incidence through v. Each listed deletion is genuinely present. Packets with no affected actual root use no primitive; their bookkeeping still progresses.

During an addition packet every current support CONTAINS its pre-packet logical union support and is a SUBSET of its fully expanded logical union support. During a deletion packet every support CONTAINS its post-packet logical union support and is a SUBSET of its pre-packet logical union support.

The relevant logical endpoint sizes are at least each original floor by Section3.1. Additions cannot violate a floor; every deletion prefix contains the floor-safe final support. Thus EACH physical primitive is legal at its SAME original root, even if the logical group sizes alone would misleadingly suggest no loss.

For lower protection, use the expanded/pre-deletion role sets. Every physical support is a subset of its logical union support at that phase. A Q_i avoiding the at-most-three group roles of a pair actually misses both labels in its physical support too. All actual roots' pair witnesses therefore persist throughout every partial packet.

For upper protection, every logical group is nonempty: its size is b_j or b_j+1. Choose one label from each group in the supplied four-index template cover H; these at most four labels hit the logical union tuple. During additions the physical tuple contains its pre-packet logical tuple; during deletions it contains its post-packet logical tuple. The corresponding four-cover therefore hits it. This directly proves tau<=4 at EACH primitive, alongside tau>=3. Maximum-layer conversion is unnecessary.

The next physical edit inside a packet is supplied by the finite affected-root list and is absent/present as shown. At each logical step the next packet is the literal remaining cycle list. Such certified level-three prefixes are extendible; no arbitrary-safe-prefix extension theorem is claimed.

## 4. Renewal, termination and exact original labelled restoration

Every completed cycle fixes its l distinct misplaced labels and displaces no correct label. It restores the partition with original group sizes b_j, hence restores each ACTUAL root cardinality N_i and its one-incidence original-floor reserve. This reserve is renewed by the actual relationships, not consumed or replenished with an extra label/root. A root may still differ from both original endpoints.

Rebuild the balanced owner graph. Whenever the incorrect-label count is positive, Section2 supplies another eligible simple cycle. That nonnegative count strictly decreases; each cycle has at most m logical edges and finitely many root edits per packet. Repetition terminates. All label group owners then match destination D, so EVERY actual E_i=C_i in its ORIGINAL labelled slot, with all full noncompact supports restored.

An original label x with source group u and destination group v changes an actual root incidence only if Q_i contains exactly one of u,v. Such an incidence is added/deleted ONCE in that label's unique resolving cycle. If Q_i contains both, it remains present throughout; if neither, it remains absent. Correct labels never move. Hence the total native primitive count is exactly

    sum_i |A_i symmetric_difference C_i|.

This is the unavoidable minimum toggle count for those endpoints, a mathematical bound and not an executed benchmark. Some group reassignments between identical incidence-pattern groups can be physically silent; they still terminate the finite supplied-certificate bookkeeping and do not introduce native moves.

Any finite chain of endpoint partitions with these SAME group sizes/template/floors admits repeated complete repair; each actual endpoint and representation are restored before the next leg. The mechanism renews inside unfinished cycles at level3 and at completed cycles restores exact4 structural boundaries. It does not impose an exact-reset requirement on other native repair mechanisms.

## 5. Overlap with a proved EVERY-whole-root-order obstruction

For every t>=1 partition P into sixteen disjoint cells B_pq of size t, p,q in{1,2,3,4}. Source groups are rows, destination groups columns; b_j=4t,k16t.

Use FOUR actual singleton templates {j}, original floors4t, and FOUR actual three-of-four templates, original floors12t-1. These are r8 ORIGINAL labelled slots, not resources added during repair. Every multigroup support has its required one-incidence reserve. Both endpoints are exact4 and have substantial pre-existing overlap: each triple-template root contains three entire singleton groups. Every triple-template support changes from source rows to destination columns.

In any proposed whole-root source-union-destination order, inspect the boundary immediately after TWO singleton roots have completed. The other two singletons remain old. Choose one cell label at each intersection of an old singleton row and a distinct completed singleton column. Their actual pair K hits all four singleton supports. Its source role set has two distinct indices, as does its destination role set.

EVERY three-of-four template intersects every two-index set. Therefore K hits every other actual root whether that root is old or completed-new at this whole-root boundary. No root is active at a completed boundary. All eight actual roots are hit by K, so tau<=2. This defeats EVERY root ordering, including arbitrary placements of the four overlapping roots; alternative witnesses cannot rescue that visited state.

X37L supplies the legal destination-directed {3,4} repair on exactly these endpoints/floors. The projected singleton path also falls under X36's necessary two-unfinished participation argument. Connectivity was ALREADY supplied by protected J/K, and the private roots supply the template's exact4 lower witnesses. This control establishes pre-existing overlap AND every-order separation; it is not used to claim absence of an independent private-root guard.

## 6. Genuine overlap without any possible four disjoint roots

For every t>=1 partition P into thirty-six disjoint cells B_pq of size t, p,q in{1,...,6}. Source groups are rows and destination groups columns. Now b_j=6t,k36t.

Declare the TWENTY actual templates Q_i to be all three-subsets of the six group indices, ordered lexicographically. Their transversal is4: any three-index set is missed by its complementary triple template; any four-index set hits every triple. Supply H={1,2,3,4}.

Each actual endpoint root has size N_i=18t. Assign the first ten ORIGINAL floors18t-1 and the other ten18t-2. All are positive (at least16), unequal, and retain the needed one-incidence reserve. Source/destination actual roots overlap whenever their triples share a group; most do. Original supports are noncompact and their full restored sizes are part of the conclusion.

No FOUR floor-safe disjoint roots can exist ANYWHERE on this carrier: four minimum floors total at least4(18t-2)>36t=k. This is an actual palette/floor obstruction to private-root protection, not a disconnection claim. In the endpoint tuple even three actual roots cannot be pairwise disjoint, because their template triples cannot be disjoint within six nonempty groups.

The full source/destination UNION tuple has an actual two-cover: choose x in cell B_12 and y in B_34. A union root contains x when its template meets{1,2}, and y when it meets{3,4}. Every triple on six indices meets{1,2,3,4}; thus the pair hits every union root. No subfamily of these actual union roots is a three-guard. Auxiliary contracted supports are not excluded.

Yet X37L supplies full reusable repair on this nonprotected overlapping family. Consider the group cycle1->2->3->4->1 with labels x_1 in B_12,x_2 in B_23,x_3 in B_34,x_4 in B_41. Perform its first TWO full addition packets. Role links are{1,2} and{4,1}; the logical/actual union tuple has tau3: these two labels plus any label from group3 hit all templates because their total group footprint is{1,2,3,4}; every pair still has at most three roles and an actual missing triple template.

Twelve actual roots have received a new incidence at this stage: six containing2 but not1, and six containing1 but not4; these sets are disjoint. All twelve are unfinished relative to both original endpoints: every source/destination root differs by9t deletions and9t additions, so one added incidence cannot complete it.

In the next deletion packet root Q={1,4,5} loses x_1. It did NOT receive x_4 as a new incidence: x_4 was already present through group4. Its support size becomes N_Q-1, and its original floor is still respected. This is genuine shared-role capacity coupling, which a per-bin incoming-before-outgoing floor argument would miss. Subsequent cycle packets restore all N_i sizes, renewing the reserve and guaranteeing continued cycles until the exact full C.

These endpoints are ALREADY symmetry-connected by L, via the palette transpose (p,q,cell-index)->(q,p,cell-index). The new result is the simultaneous actual-floor accounting, actual-pair certificate and derived event-unique continuation through overlap; no new connectivity classification or impossibility of all whole-root orders is claimed for this second control.

## 7. Sharp method obstruction when the one-incidence reserve is absent

Keep the same twenty triple templates and six groups, but take saturated ORIGINAL floors a_i=N_i at all roots. This is a DIFFERENT carrier, openly specified for the method-limit control, not an alteration of floors on the successful carrier. Exact4 endpoints still exist and are symmetry-connected by L.

Choose the same four-cycle. If the first addition is1->2, after adding4->1 and deleting1's outgoing label, Q={1,4,5} loses that outgoing incidence while its replacement was already present through4. Its size is N_Q-1, so the displayed deletion is illegal. Omitting it stalls this prescribed packet list; substituting another mechanism is outside the tested method.

For ANY rotation of this directed four-cycle choose initial recipient c. Of its four directed edges, exactly two avoid c. After the appropriate deletion packet one of those edges{u,v} is the sole remaining duplicate link. There exists an index w outside the cycle, and the ACTUAL template Q={u,v,w} excludes c. Section3.1 then gives EXACT size N_Q-1. The saturated floor is violated. Thus no choice of starting edge salvages the prescribed adjacent-link cycle lift with these floors.

This proves both that the one-unit cardinality loss can be attained and that the one-incidence reserve is sharp as a UNIVERSAL sufficient bound for THIS lifted cycle procedure. It does not prove every possible destination-directed schedule fails, forbid decompositions using other cycles, or establish native disconnection. L supplies a native unit-band route despite this method obstruction. Nor is one spare incidence necessary for every input/template/cycle; singleton roots and many multigroup masks never incur the loss.

## 8. Dependencies, advance and remaining obligation

Frozen X36 supplies the reverse logical-cycle pattern, its adjacent-link invariant and the participation comparison on the private-root control; it does NOT supply the multigroup floor bound, which is proved here. I11 defines unique destination events and actual floor/pair scheduling; X37 derives a complete feasible event permutation under explicit template/reserve hypotheses, not merely checks a proposed sequence.

Accepted protected J/K already covers Section5. Global palette exchange L covers both fixed-group-size endpoint classes and the saturated method-limit control; its general path may use extra/repeated non-destination incidences. We neither rewrite those frozen proofs nor recertify their implementations. A's complete-lower-path conversion is not needed because both band bounds are proved directly at every packet prefix.

References:
- At parent0ac4e31b0dc1e0f9082429ddc077e39590ac78f6, A11_X36_INTERLEAVED_CYCLE_RENEWAL.md and its whole review/closeout; A11_GLOBAL_SCHEDULE_REDUCTION.md (I11); UNBOUNDED_REPAIR_PARTICIPATION.md.
- At certified466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, demos/v16.54-parent-support-connectivity/PROTECTED_EXCHANGE.md (J/K), OVERLAPPING_CLIQUE_EXCHANGE.md (L/M), GENERAL_PARENT_CONNECTIVITY.md (A).

The conceptual advance is a reusable joint capacity/witness interface for pre-existing overlapping roots. A nominal replacement can already occur in a root through another role; this loses an actual incidence and must be counted. The proved one-incidence bound and restored cardinalities explain why the same finite reserve can support repeated completion. Actual missed-root witnesses follow simultaneously from the shared role footprint, including all partial packet edits.

Template/partition representations, equal group sizes and the original-floor reserve are sufficient hypotheses. Accessibility of this template class from arbitrary exact-four endpoints, arbitrary endpoint incidence patterns, zero-reserve handovers and unrestricted mixed/directed/higher-target/nested connectivity remain open. No claim turns a failed template/reserve/cycle test into disconnection. Stronger compatible-grade research remains a parallel direction.

Fresh review must inspect the positive lift and limited obstructions together, every actual pair, physical packet floors, shared cardinalities, cycle existence, renewed reserves, literal next edits, finite progress, full labelled restoration, distinct control claims and inherited novelty domains. v16.55/v16.54 certificates and original evidence remain unchanged; separate efficiency implementation/fixture/benchmark stays unstarted and independently gated. No numerical run, science/test/workflow execution, implementation, benchmark, integration merge, new numbered stage, physical energy/metric/gravity or fundamental-time claim. Originality relative to literature has not been established.
