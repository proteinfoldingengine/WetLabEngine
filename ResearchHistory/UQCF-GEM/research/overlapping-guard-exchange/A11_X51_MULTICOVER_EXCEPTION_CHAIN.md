# A11.X51 - multi-cover exception-chain renewal

Analytical parent: c94851834d298aec31700bed14c537a3fc022299.
Scope: 523357d530147f608a80f95730c6604b0c9b7153.
Exact candidate for fresh whole-argument review. Analytical only.

## 1. Native types, actual witnesses and claims

Fix finite ordered palette P with at least four labels, labelled original root slots and SAME original positive floors. Every primitive toggles ONE incidence in ONE root. Larger intermediate supports remain permitted. No labels, slots, simultaneous moves or weakened floors are introduced.

As in X49/X50, a type t specifies an ordered pair (A_t,C_t) of original endpoint supports. Supply n_t>=1 original labelled copies. Each copy s has its own floor
    0<a_(t,s)<=min(|A_t|,|C_t|).
The full original source and destination have hitting number exactly four. Positive copies do not change the endpoint hitting sets of the one-representative-per-type tuple.

Supply h+1 physical sets K_0,...,K_h of at most four labels, h>=1. Put
    U_j={t: K_j misses A_t},
    V_j={t: K_j misses C_t}.
Require U_0 empty and V_h empty: the first covers the source and the last covers the destination. Intermediate sets need not cover either full endpoint.

**X51C (block-stable cover chain).** Let sigma be a total type order satisfying, for every j<h,
    every type in U_(j+1) strictly precedes every type in V_j.
Then at every active block a member of the chain hits BOTH active endpoint supports and all other currently restored type supports. This derives copy coexistence protection with no nestedness or disjoint-capacity assumption. Combined with a lower-safe one-representative type path, processing each original copy block add-before-delete gives a direct {3,4} path, legal original floors, finite termination, full labelled/noncompact restoration and the endpoint-toggle minimum.

**X51D (joint structural DAG certificate).** For every physical pair B define
    O_B={t: A_t misses B}, T_B={t: C_t misses B}.
For each pair without a common type witness choose one actual type v_B in T_B and u_B in O_B. Build the type graph with:
- ALL upper edges u -> v for u in U_(j+1), v in V_j, every j<h;
- lower witness edges v_B -> u_B for every noncommon pair.
If this graph is acyclic, its least-source topological order supplies BOTH hypotheses of X51C and a lower-safe type path. Thus the complete native direct-band, minimum-event, exact-restoration conclusion is constructed without the X49 joint mean or a supplied safe total order.

Self edges or cycles fail this sufficient certificate. Choosing compatible witness pairs is a substantial hypothesis, not forced by endpoint exactness. This does not assert universal acyclic selections.

**X51F (arbitrarily many necessary cover stages on a declared schedule).** For every h>=2 there is an exact-four family with arbitrary positive original copies and original floors<=k-4, k=4(h+1), and a specified lower-safe block schedule in which every K_j is the UNIQUE four-cover at a restored boundary. Hence any upper witness certificate for THAT SAME schedule needs all h+1 distinct physical four-sets. X51C constructs its direct repair and renews forward/reverse repetitions. This does not exclude a different two-cover root order, another method or native connectivity.

The control's fixed background is itself a permanent lower guard. Its novelty is unbounded required upper-cover stages for the declared schedule, not a new interdependent lower-witness family.

## 2. Exact active-block criterion

For a fixed type order let pos(t) be the integer position, q the number of types. Define
    L_j=max pos(U_j), with L_j=0 if U_j empty;
    b_j=min pos(V_j), with b_j=q+1 if V_j empty.

At active block p, earlier types have destination supports, later types source supports, and the active type must be hit at BOTH endpoints to protect simultaneous old/new copies.

A set K_j hits all these constraints exactly when
    L_j < p < b_j.
Indeed all its source exceptions must have completed strictly before p, and none of its destination exceptions may have completed or be active. Conversely those two conditions hit every required endpoint. Thus its block-valid integer interval is [L_j+1,b_j-1], possibly empty.

This differs from X49's mixed-prefix interval: at a copy block BOTH active endpoints are required. Simple adjacent type-prefix coverage does not imply this stronger condition. X49's failed unconditional copy lift remains failed.

For any supplied cover family, union of the block-valid intervals covers integers 1 through q exactly when a block-stable cover exists at every position, relative to that family. X51 now supplies a structural sufficient chain condition forcing this coverage.

## 3. Chain theorem without nested exception sets

The required cross precedence gives
    L_(j+1) < b_j
for every j<h. This includes empty sets under the conventions above: if U_(j+1) empty then 0<b_j; if V_j empty then L_(j+1)<q+1. If both are nonempty it is exactly every U_(j+1) before every V_j.

Fix any block position p, 1<=p<=q. Since V_h empty, b_h=q+1>p. Choose the LEAST j with b_j>p.
- If j=0, L_0=0<p because U_0 empty.
- Otherwise leastness gives b_(j-1)<=p. Cross precedence gives L_j<b_(j-1)<=p.

In either case L_j<p<b_j, so K_j is a coexistence cover at block p. No monotonicity of L_j or b_j, nested exceptional families or independence is used. Overlapping types participate in every actual obligation on the same order. A required self precedence cannot be satisfied and is rejected.

Use this same physical K_j throughout every copy of the active type. It hits all earlier destination roots, all later source roots, BOTH endpoints of every active-type copy, and hence every enlarged active support containing one of those endpoints. This proves tau<=4 at every primitive and boundary. Changing the existential cover witness between blocks is not an incidence edit.

The proof is finite and explicit: compute the exception positions, take the least j with b_j>p at each generated block. With h=1 it reduces to X50's two-cover argument. For h>1 it allows several genuine transitions, even though no single common four-cover persists.

## 4. Joint graph, actual lower safety and completion

Exact-four endpoints imply O_B and T_B are nonempty for every physical pair. If O_B intersects T_B, a representative type in the intersection avoids B at both endpoints. Its union and every intermediate support avoid B, independently of the order.

Otherwise X51D selects v_B in T_B and u_B in O_B, with graph edge v_B -> u_B. Since the sets are disjoint these are distinct types. A topological order makes the new witness type complete before the old witness type begins. Until v_B completes, untouched u_B avoids B, including while v_B is active; afterward v_B's completed destination avoids B throughout the rest of the type path. Thus every pair has an actual representative-type witness through every primitive.

A finite acyclic directed graph always has an indegree-zero vertex: otherwise following predecessor edges from any vertex would eventually repeat and give a directed cycle. Repeatedly choose the least such remaining type, remove it and its outgoing edges. Each next choice exists, the remaining-type count strictly decreases and all edges are respected. These are explicit eligible order choices, not an inference from a safe prefix.

The upper graph edges impose precisely X51C's cross precedence. The lower edges give the actual type-pair witnesses just proved. The union graph uses the SAME type identities; no lower/upper orders are chosen separately and no shared capacity is counted independently.

Now execute original copies in complete type blocks. At any active-copy primitive, take that actual copy as its representative and one existing endpoint copy of each other type. This selected tuple equals the corresponding lower-safe type state. Every pair misses an ACTUAL original support. Other copies cannot remove that witness. At type boundaries all representatives are endpoints. Therefore tau>=3 on the actual path.

For each copy add absent destination-only incidences, then remove present source-only incidences, in palette order. The active support contains A_t during additions and C_t during deletions, preserving its own original floor even when saturated. The finite scheduled lists supply the next primitive; zero-edit copies simply advance with no fictitious edit. All type blocks finish, every original full destination support is restored, and common incidences remain fixed.

The count is
    sum_t n_t |A_t symmetric-difference C_t|.
Every differing endpoint incidence must change at least once on any native path, so this count is minimum. Upper witness switches introduce no edit. No maximum-layer conversion is invoked.

For X51C with a separately supplied lower-safe type order, use the same actual-copy lower lift. For X51D, the graph constructs that order. The certificate is sufficient rather than necessary: a cycle rejects THESE chosen witness edges and cover-chain constraints, not all possible witness selections, orders, cover families or native routes.

## 5. Structural family forcing many cover identities

### 5.1 Endpoints and static exact-cover background

Fix h>=2, k=4(h+1), and an ordered palette partitioned into pairwise disjoint four-label sets K_0,...,K_h. They are names for declared physical subsets, not new ingredients during repair.

For every four-set J subset P other than the h+1 sets K_j, declare a static original root
    F_J=P minus J
at BOTH endpoints. Each has size k-4. Declare dynamic types a_j,b_j for 1<=j<=h:
    A_(a_j)=P minus K_j, C_(a_j)=P;
    A_(b_j)=P, C_(b_j)=P minus K_(j-1).
Every static or dynamic type may have ANY positive original labelled multiplicity. Each original floor may be any positive value<=k-4, including complete saturation at its smaller endpoint.

The static family's complete four-cover set is exactly {K_0,...,K_h}. A four-set I misses F_J iff I subset J iff I=J. Thus all other four-sets are rejected by their corresponding static root.

No three-set is a static cover. A three-set T is contained in at most ONE disjoint K_j, while it has k-3>=9 distinct four-set extensions. Choose an extension J not equal to any K_j; then F_J misses T. Smaller sets extend to triples and are missed too. Therefore static transversal is exactly four: each K_j covers it and no smaller set does. Static roots alone miss every forbidden pair, indeed every triple, so lower protection is permanent.

At the SOURCE dynamic a_j roots reject exactly K_j among the static four-covers, for j>=1; all b_j are P. Hence the full source has UNIQUE minimum cover K_0 and tau=4. At DESTINATION b_j reject exactly K_(j-1), for j<=h, while a_j are P. Hence the full destination has UNIQUE minimum cover K_h and tau=4. Positive copies leave these statements unchanged.

### 5.2 Ordered exception chain and primitive safety

Use the declared type schedule
    a_1,b_1,a_2,b_2,...,a_h,b_h,
with all static types first or anywhere, since their edits are empty. For j>=1 the cover K_j has source exception U_j={a_j}; U_0 is empty. For j<h it has destination exception V_j={b_(j+1)}; V_h is empty. Static roots are no exceptions.

The chain conditions are exactly
    a_(j+1) before b_(j+1), 0<=j<h,
which the schedule respects. Static roots supply common witnesses for every pair; no lower edges are needed. The upper graph is a disjoint collection of these dynamic edges, hence acyclic. The declared schedule is a topological order and is lower-safe. X51C/D apply, including arbitrary copy coexistence.

Explicitly, process a_j copies using cover K_(j-1), then b_j copies using K_j. Each a_j copy adds the FOUR missing K_j labels to reach P. Each b_j copy removes the FOUR K_(j-1) labels from P. Individual edits are literal and stay at size at least k-4. Static supports remain fixed. Every intermediate configuration is actually EXACT FOUR, since the static family forces tau>=4 and the derived covers give tau<=4. This family uses no deficit; do not infer that from the general theorem.

The path has exactly
    4 sum_(j=1..h)(n_(a_j)+n_(b_j))
primitives, the endpoint-toggle minimum, and restores all dynamic and static labelled roots.

### 5.3 Necessity of every stage on THIS schedule

Immediately after the b_j block completes, for 0<=j<=h (j=0 means source):
- the completed b_1,...,b_j destination supports exclude K_0,...,K_(j-1);
- the still old a_(j+1),...,a_h source supports exclude K_(j+1),...,K_h;
- every K_j meets all remaining constraints.

Since the static background allows no other four-set, K_j is the UNIQUE four-cover of that boundary tuple. This also handles j=h at the exact destination.

Consequently every direct upper certificate using sets of at most four labels for THIS completed-block schedule must use all h+1 distinct K_j. It cannot be shortened to two physical covers when h>=2, even by choosing arbitrary physical four-sets outside the initially supplied family: the static roots rule all others out.

In particular X50's source/destination two-cover pair is necessarily K_0,K_h. Here U_h={a_h} and V_0={b_1}. In the declared schedule b_1 precedes a_h for h>=2, so the two-cover relay fails on that SAME order. X51's intermediate covers bridge the gap.

This is not impossibility of every two-cover type order. For example one could complete all a_j blocks before all b_j blocks, making the endpoint pair usable. The necessity is explicitly schedule-relative, useful when retaining an independently supplied lower schedule. No native no-path or minimum upper-certificate over all paths is asserted.

### 5.4 Renewal and repeated restored legs

At a completed forward leg every original support equals its stated endpoint. For the reverse leg exchange source/destination, covers K_j with K_(h-j), and process
    b_h,a_h,b_(h-1),a_(h-1),...,b_1,a_1.
The source/destination exception calculation reverses: the cover chain conditions become b_j before a_j. Static exact covers and all individual floors are unchanged. X51C applies again, with the same actual static pair witnesses.

Any finite alternating chain of these two exact endpoints therefore reconstructs each cover chain and copy schedule, completes and reaches the exact labelled final destination. It may revisit incidences, so counts are minimum PER LEG only.

More generally X51C/D renew whenever each restored adjacent leg supplies its own qualifying cover chain and joint ordering certificate. There is no claim that every arbitrary next endpoint or arbitrary safe unfinished prefix does so.

## 6. Advance, inherited domains and remaining obligation

The structural discovery is that a chain of adjacent exception handovers can supply a global active-block cover without nested exception sets. The next cover's source exceptions must be repaired before the current cover's first destination exception becomes active. The least-available-cover proof makes this rigorous even if the valid intervals are nonmonotone or some intermediate cover never works.

X51D couples this upper structure to actual lower witness identities on ONE finite graph and supplies eligible next choices/termination when it is acyclic. It extends X50 beyond one cover switch and avoids X49's potentially expensive mean computation in this sufficient class. Finite graph checking is a mathematical constructor, not an executed benchmark or a general efficiency result.

The family demonstrates arbitrarily many unavoidable cover identities on a prescribed schedule, including positive copied slots and saturated or unequal original floors. Its fixed background already supplies a full lower guard; it is not a new lower-dependence mechanism or a new native connectivity class. It does not establish absence of all two-cover orders. The general theorem CAN use noncommon lower witnesses, but no new infinite family with noncommon lower obligations is demonstrated here.

Dependencies at the analytical parent: X34/X35 and SEQUENTIAL_HANDOVER supply the inherited actual pair-order criterion; X49 supplies the prefix/copy distinction and retains the rejected generic lift; X50 supplies the two-cover special case and lower-copy witness lift. Their source is unchanged. The interval and chain arguments here are proved directly. No compactness, grade permutation, spare-room, exact-compaction, guard-buffer or element-cover theorem is assumed. Maximum-layer theorem A is not used, and symmetry connectivity comparisons are not new claims.

Remaining: derive compatible lower witness selections and multi-cover chains from weaker endpoint structure, particularly with no permanent lower guard and no two-cover order available; or derive economical joint bounds when the graph is cyclic. Cycles and failed supplied chains are method failures, not disconnection. Arbitrary accessibility, unequal corresponding group sizes, below-X40 protection and unrestricted mixed-floor/directed/higher-target/nested universality remain open.

No numerical execution, workflow, implementation, benchmark, integration merge, numbered certification, literature-originality or physical claim. Certified v16.55/v16.54 and all original evidence remain preserved. Separate efficiency runner/fixtures/benchmarks remain unstarted and separately scoped.
