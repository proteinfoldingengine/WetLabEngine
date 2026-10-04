# A11.X41 — localized asymmetric protection and single-copy renewal

Exact analytical candidate. Scope 20d78a3ebb425ef1b06c8e3381494b879ef87ff9; accepted parent ffce5926f2338de6c17e186869d2ed0a21d01c44.
No scientific execution or numbered certification.

## 1. Carrier, structural hypothesis and typed conclusions

Fix a finite ordered palette P and r labelled ACTUAL original root slots. Each slot has the SAME ORIGINAL positive floor a_i throughout; every primitive adds or removes ONE incidence in ONE root, and supports can temporarily grow. No added labels/slots, weakened floors or simultaneous moves.

Supply m>=4 role indices, nonempty masks Q_i subset [m], and partitions B_j,D_j of P with equal positive corresponding sizes b_j. Actual endpoints are A_i=union_{j in Q_i} B_j and C_i=union_{j in Q_i} D_j. Put N_i=sum_{j in Q_i} b_j and require 0<a_i<=N_i. Require template transversal EXACT FOUR, supply its minimum four-role cover H, and require an actual original slot with mask {h}. This singleton is a supplied structural relationship, not a new root installed by the proof.

Groups/masks describe actual incidences; they impose no new geometry or native restrictions on intermediate supports. Other roots may overlap arbitrarily. All counts below use ORIGINAL labelled slots, never separately imagined capacities.

For each role pair S let w(S)=number of i with Q_i intersect S empty. Define
    alpha=min_{u!=h} w({h,u}),
    beta=min_{u,v!=h, u!=v} w({u,v}).
Exact-four consistency forces alpha,beta>=2, as in X40W.

**X41L.** If binomial(alpha+beta,alpha)>2(m-3), every pair A,C in this supplied class admits a deterministic finite lower-protected path tau>=3, respecting all same original floors including saturation, to FULL exact labelled/noncompact C. The path retains common incidences and toggles each original endpoint-differing incidence once.

**X41B.** AFTER constructing the complete finite X41L lower path between the original exact-four endpoints, inherited theorem A yields a native band path 3<=tau<=4 restoring C with the same palette/slots/floors. Its schedule, event minimum and internal waypoints are not guaranteed to survive conversion.

**X41U.** If the supplied minimum four-role cover H has b_j>=2 for every j in H, X41L itself stays in the band and has exactly sum_i |A_i symmetric_difference C_i| primitive edits, the endpoint toggle minimum. This uses renewable existing upper-cover representatives, not root-floor reserve.

**X41F.** One singleton {1} plus ONE actual copy of every rest-mask complementary to a pair meets X41 for ALL m>=5. It has alpha=m-2, beta=2, rho=2. X40's global sufficient inequality fails for EVERY m>=6, but X41 proves complete repeated direct minimum-event repair for the saturated long-cycle controls below. No root replication is needed.

This is a sufficient scheduling and renewable-protection theorem. Equal-size pattern endpoints already symmetry-connect by inherited L. It is not a new connectivity classification or a literature-originality claim. It does not prove arbitrary endpoints admit the singleton/template representation.

## 2. Exact endpoint consistency

A label hitting set induces a cover of the actual masks by its owner roles. Conversely one actual label from each role of H gives a four-label cover. Nonempty partition groups therefore make every restored mask realization exact FOUR.

If a role pair S had no avoiding slot it would itself cover the template. If it had only one avoiding slot i, any role of the nonempty Q_i added to S would make a cover of size at most three. Both contradict exact four. Thus w(S)>=2 for every role pair and alpha,beta>=2. Duplicate masks, if supplied, count only as distinct original slots; X41F has none.

Every role footprint of at most three indices is avoided by an ACTUAL root, or it would be a cover of size at most three. No complementary-triple mask or minimum mask width is required. The singleton {h} moreover avoids every footprint not containing h, irrespective of its size.

## 3. Localization of every possible pair obligation

At a restored partition E, draw one arc current owner -> final D-owner for each misplaced label. Correct labels are removed from this bookkeeping graph. Equal current/destination cardinalities imply equal incoming/outgoing multiplicities at each vertex. A finite nonempty balanced graph with no loops contains a simple directed cycle: an entered vertex has an outgoing arc, so following arcs cannot stop, and repetition supplies a simple cycle. Fix deterministic finite orders and choose the least cycle and least labels on its arcs.

Write its distinct vertices i_1,...,i_l cyclically, with selected x_t moving from i_t to i_(t+1), 2<=l<=m. Exchange one selected label in/out at each cycle group and leave all others fixed. The next partition F has the same b_j and actual root sizes N_i, and selected labels are at their final owners. Equivalently the palette permutation sigma(x_t)=x_(t-1) has inverse x_(t+1) originally in the required next group.

In the physical root union E_i union F_i:
- an unselected label has one fixed owner role;
- a selected label x_t has footprint {i_t,i_(t+1)}.

Two unselected labels, an unselected/selected pair, or adjacent selected edges have combined footprint at most three. Section 2 supplies an actual root avoiding both labels in its ENTIRE union, hence every partial support in that root. This covers ordinary labels at h as well; do not assume the singleton itself avoids such labels.

Only pairs of selected labels on disjoint edges can lack an actual common old/new witness. If their combined footprint does not contain h, the original singleton supplies one. Therefore every remaining obligation comes from disjoint cycle edges with one edge incident to h.

If h is outside the cycle, there are NO noncommon obligations. Length-two/three cycles likewise have none by the three-role argument. If h lies on a simple cycle of length l>=4, precisely TWO cycle edges are incident to it. Each is disjoint from l-3 other edges. Those two incident edges are adjacent, so they cannot jointly form one of the counted pairs; there is no double count. Hence at most
    e_l=2(l-3)
pair obligations can lack a common witness. Additional actual masks can still make some of those common; this is an upper bound, not an asserted exact count.

For a remaining pair, one selected edge enters h or leaves h and the other avoids h. On a leaving edge, the source owner pair contains h and the destination pair does not. On an entering edge, the destination pair contains h and the source pair does not. Distinct disjoint edges guarantee each pair comprises two different roles. Thus the actual old/new witness sets U_K,V_K have sizes at least alpha,beta in one orientation or beta,alpha in the other. There is no requirement that the two counts be equal. If the pair is noncommon, these two sets of ORIGINAL indices are disjoint.

Every physical pair K has now been accounted for: common witnesses for footprints of size<=3 and footprints avoiding h, or one of the localized asymmetric old/new obligations. Totals alone are not used to infer a witness.

## 4. A derived complete order on the SAME actual roots

For disjoint actual sets U,V of sizes u,v, the fraction of full labelled root orders with all U before all V is exactly 1/binomial(u+v,u): among the binomial relative U/V words only U...UV...V is bad. This is inherited X34 counting, not a new probability principle or randomized execution.

The denominator increases in each positive coordinate. Indeed binomial(u+1+v,u+1)/binomial(u+v,u)=(u+v+1)/(u+1)>1, and likewise for v. It is symmetric in u,v. Each localized pair thus contributes at most 1/binomial(alpha+beta,alpha) to the exact mean bad-event count. All common pairs contribute zero. Consequently, for a cycle containing h with l>=4,
    Psi_cycle <= 2(l-3)/binomial(alpha+beta,alpha)
              <= 2(m-3)/binomial(alpha+beta,alpha) < 1.
Other cycles have Psi_cycle=0. Linearity needs no independence. ALL obligations use the SAME root slots and their simultaneous full order.

Here is the eligible next choice, not merely an assumed good order. For each completed-root prefix D, take the exact conditional mean Psi(D) over all full extensions. For a noncommon pair whose first V has not occurred, its remaining u' old witnesses and v new witnesses contribute 1/binomial(u'+v,u'). Once a V has occurred, the contribution is one if all U preceded the first V, and zero otherwise. The U,V identities and completed prefix determine this exactly. Equal root supports may be included in the combinatorial order and later yield no native edits.

The extension set splits into equal-size classes by its next root. Thus Psi(D) is the mean of Psi(D,i) over remaining roots. Pick the least i with Psi(D,i)<=Psi(D), which exists whenever roots remain. The count stays strictly below one. On a full order it is an integer number of bad pairs, hence zero. The resulting order has first(V_K)<last(U_K) for EVERY noncommon pair simultaneously.

For each ordered root, add each actually absent F_i minus E_i incidence individually in palette order, then delete each E_i minus F_i incidence individually. All additions are absent, all deletions present, and common incidences are retained. During expansion the actual root contains E_i; during contraction it contains F_i. Each has size N_i>=a_i. Floors remain legal at the SAME original slot, even when a_i=N_i and when another included role already made a nominal replacement present. Finite literal lists supply an eligible primitive inside each active root, and the finite root order supplies the next active root.

A common witness avoids the pair throughout its whole union. Otherwise an untouched old witness exists while the first new witness is being changed, because first(V)<last(U); after that first new witness completes it supplies the protection. These are actual roots, and the statement applies to every individual incidence prefix. Every forbidden two-label hitting set is missed, so tau>=3 throughout.

Nothing assumes an arbitrary safe prefix can finish. Continuation is proved for the generated conditional-count prefixes, actual inner edit lists and restored cycle boundaries.

## 5. Reuse, progress, exact restoration and upper protection

Each completed handover restores all b_j, N_i, actual masks, exact-four template, singleton slot, alpha,beta and supplied H. No witness capacity is consumed. Removing one incoming/outgoing selected arc per cycle vertex preserves balance. If any incorrect labels remain, another simple cycle exists, and the SAME inequality handles it irrespective of its length or whether it includes h.

The number of incorrectly owned labels decreases by l at each completed finite exchange, and no correctly owned label moves. This well-founded integer measure and derived next-cycle existence prove termination at D_j and FULL C_i. Every original common incidence stays fixed. A label changes owner once, directly from its original to its final owner: masks containing both retain it, masks containing neither omit it, and masks containing exactly one toggle its original differing incidence once. Therefore the lower path's primitive count is exactly sum_i |A_i symmetric_difference C_i|. Bookkeeping cycles that change no actual incidence can be omitted as native no-ops without harming descent.

X41B uses accepted A only after the COMPLETE finite original-ended lower path exists. Fixed finite palette/slots, positive original floors, arbitrary native additions/unions and exact-four outer ends match its domain. A gives the {3,4} band, but may repeat toggles or change schedule; event minimum and internal waypoint preservation are not claimed after conversion. For a finite chain, construct the full lower concatenation before converting it if only outer endpoints are to be guaranteed. Lower event counts are per leg, not one global count across a chain revisiting states.

For X41U, a simple cycle selects at most one label per group. If b_j>=2 for every j in the minimum four-role H, choose an UNSELECTED existing label in each H group. These four distinct labels keep their owners across the adjacent E,F partitions and cover both root tuples. Every physical partial root contains either its old or new support, so the SAME four labels cover every primitive. This proves tau<=4 separately from lower protection and preserves the preliminary minimum count. Restored b_j renews the choice before each subsequent cycle.

These are already-existing upper-cover representatives, not original floor slack or a spare lower-protection root. No exact reset is required after each primitive; level three is permitted. No benchmark is executed or implied by the mathematical count.

## 6. An all-m single-copy sparse family below X40's global test

For every m>=5 declare original masks:
    ONE {1};
    ONE [2,...,m] minus {u,v} for each unordered rest pair {u,v}.
There are r=1+binomial(m-1,2) slots. These are all ORIGINAL inputs; no copies or slots are introduced along the path. Singleton forces role1 into every cover. Every rest pair is missed by its matching high mask, while every rest triple hits all high masks. Thus the exact template transversal is FOUR with H={1,2,3,4}.

For pairs {1,u}, exactly m-2 high roots avoid the pair (excluded pairs containing u); the singleton does not. Hence alpha=m-2. For pairs {u,v} outside1, exactly the singleton and the matching high root avoid the pair. Hence beta=rho=2.

The localized denominator is binomial(m,2). It exceeds 2(m-3) for ALL m>=5:
    binomial(m,2)-2(m-3)=(m^2-5m+12)/2>0.
The quadratic has negative discriminant, or equals ((m-2)(m-3)+6)/2>0. Thus X41 works with one copy at every m. The global X40 scalar test instead uses binomial(2rho,rho)=6 and requires 6>m(m-3)/2, which fails for EVERY m>=6. This is a failure of that SUFFICIENT TEST, not of the X40 native construction, exact nonuniform X34 counting or connectivity. X41 refines the counting method and its structural availability domain; no independent conditional-expectation discovery is claimed.

At m>=5 all complementary-triple masks whose excluded triple J avoids1 are absent: their complements contain1 and at least one other role, whereas the singleton is the only declared mask containing1. X39's dense-width premise fails (singleton width1<m-3). Missing complementary-triple witnesses are replaced by one actual root sharing many obligations, and by asymmetric existing high witnesses where the singleton participates in the handover.

For every t>=1 use existing disjoint t-label diagonal cells B_jj and forward cells B_(j,j+1), cyclic j. Source groups are rows, destination groups columns, all b_j=2t and k=2mt. Original floors are SATURATED: low2t and all high2t(m-3), unequal. H meets the direct-cover condition, so X41U gives minimum-event band repair for all m,t, including unbounded cycle lengths at FIXED minimum pair redundancy two.

Four disjoint floor-safe supports cannot exist ANYWHERE: at most one slot has the low floor, so any four distinct original slots have floor sum at least 2t+3*2t(m-3)=2t(3m-8)>2tm=k for m>4. This is a limitation of disjoint private-root preparation, not native disconnection.

The misplaced graph comprises t parallel copies of one directed m-cycle and has no shorter simple cycle. Every actual mask is a nonempty proper subset of that connected cycle, so has both an entering and a leaving edge; every root changes. The entire-cycle and full original endpoint union have a two-cover: selected labels on 1->2 and 3->4 hit the low root through1 and expose three rest roles2,3,4, at least one of which each high mask includes because it excludes only two. Whole-union preparation is therefore unsafe. This does not prove every whole-original-root order fails or exclude arbitrary contracted auxiliary guards.

At t>=2, after the first completed cycle every original root has lost/gained a selected crossing label and still contains an unselected source-only crossing label. It differs from BOTH original endpoints. Nevertheless every group/root size, singleton, alpha,beta and cover multiplicity has renewed; the residual graph has exactly t-1 copies of the same long cycle. Another eligible witnessed handover exists. Exactly t cycles finish the exact original destination. These are symbolic all-parameter proofs, not enumerated evidence.

## 7. Dependencies, actual advance and remaining obligations

Inherited X34 supplies actual bad-order fractions, shared-root conditional averaging and old-until-new handover; X40 supplies general cycle bookkeeping, exactness-derived pair redundancy, event-minimum accounting and the independent upper-cover representative mechanism. X41 proves NEW localization around an actual singleton and asymmetric alpha/beta bound, and applies it to one-copy unbounded saturated sparse controls. X40's replicated constructor remains valid unchanged.

Certified A and L are used only in their accepted domains: A converts complete lower paths; L already supplies symmetry connectivity for same-floor partition-related endpoints. No compaction, maximum-layer waypoint assumption, mixed-floor permutation, external design, numerical certificate or physical law is added. Earlier X37/X38/X39/X40 claims and controls are untouched.

This removes the growing uniform redundancy/replication requirement of the X40 scalar application for this structural family. It does not prove universal access to a singleton template or all below-bound sparse templates. The actual singleton, SAME supplied masks, equal nonempty corresponding group sizes and asymmetric binomial bound remain explicit hypotheses; X41U additionally assumes renewable cover representatives. Scarce upper representatives, templates without such localization, unequal sizes and arbitrary template accessibility remain open. Broader mixed-floor/directed/higher-target/nested universality and the stronger compatible-grade direction stay separate.

No scientific commands, numerical execution, implementation, benchmark, integration merge or numbered certification. v16.55/v16.54 and all original evidence remain preserved. Separate efficiency implementation/fixtures/benchmarks remain unstarted and independently scoped.

Fresh independent whole review must check the singleton localization and orientation, all pair cases, shared actual capacities, exact bad-event count/conditional next choice, floor legality, next-cycle existence/renewal, finite termination/exact restoration, lower/converted/direct domain separation, all-m one-copy counts and failed global scalar comparison, saturated controls and dependency/novelty limits together.
