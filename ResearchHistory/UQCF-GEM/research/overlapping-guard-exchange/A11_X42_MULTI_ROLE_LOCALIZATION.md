# A11.X42 — multi-role protection without a singleton representation

Exact analytical candidate. Scope b8c3c4eab45df3c4d070e20b74d447c1d5f3b295; accepted analytical parent e6ecdb3f7b811e76fa2c787ebc691ff7aa2bf772.
No numerical execution or numbered certification.

## 1. Fixed carrier and typed sufficient statements

Fix a finite ordered palette P, r labelled ACTUAL original roots and their SAME ORIGINAL positive floors a_i. Supports may grow; a primitive adds or removes ONE incidence in ONE root. No new labels, slots, lowered floors, simultaneous primitives or imposed geometry.

Supply m>=4 nonempty partition groups B_j,D_j of P with equal positive corresponding cardinalities b_j, and SAME nonempty actual masks Q_i subset G=[m]. Endpoints are A_i=union_{j in Q_i}B_j and C_i=union_{j in Q_i}D_j. Put N_i=sum_{j in Q_i}b_j; require 0<a_i<=N_i. Template transversal is EXACT FOUR and a minimum four-role cover H is supplied. Masks/groups are an actual incidence certificate, not native restrictions on intermediate supports.

Supply ONE original slot whose mask is S, with 1<=p=|S|<=m. It need not be a singleton or a set of incidence-indistinguishable roles. Define actual role-pair avoidance
    w(K)=number of original indices i with Q_i intersect K empty,
    rho=min_{|K|=2}w(K),
    alpha=min_{|K|=2, K intersect S nonempty}w(K).
These count the SAME original labelled indices across all obligations. Exact-four consistency forces rho>=2 and alpha>=rho.

**X42L.** If binomial(alpha+rho,alpha)>2p(m-3), the supplied endpoints have deterministic finite ORIGINAL-ended lower-protected repair tau>=3 at the same original floors, including saturation. Every original common incidence stays fixed, every original differing incidence toggles once, and FULL labelled/noncompact C is restored.

**X42B.** Only AFTER this complete finite lower path between original exact-four endpoints exists, accepted A supplies a native {3,4} path with exact outer ends and same palette/slots/floors. Event minimum, schedule and internal waypoints are not guaranteed after conversion.

**X42U.** If the supplied minimum cover H also has b_j>=2 for each j in H, X42L itself stays directly in {3,4}, with exactly sum_i |A_i symmetric_difference C_i| primitives, the endpoint toggle minimum. Existing unselected cover representatives renew before every cycle; no root-floor reserve is required.

**X42F.** For EVERY p>=2 and n>=5p, a declared sparse template with m=p+n roles, one p-role mask, one copy of each rest co-pair mask and p broad distinguishing masks meets X42 with alpha=n-1,rho=2. NO singleton mask is possible in ANY partition-union representation of its source tuple. Nevertheless it has complete repeated direct minimum-event repair at saturated unequal floors through length-m cycles.

X42 is a new sufficient actual-witness localization interface, not a new connectivity classification. L already connects the equal-size-pattern endpoints. Supplied template accessibility, unequal group sizes and unrestricted mixed-floor/directed/higher-target/nested questions remain open. X41's sharper one-role asymmetric beta condition remains valid separately; the conservative rho bound here is not asserted to improve every X41 inequality.

## 2. Exact consistency and actual common witnesses

Any actual label cover induces a set of owner roles hitting all masks; representatives of H conversely hit all actual roots. Nonempty groups therefore make every restored realization exact FOUR.

If a role pair K had no avoiding root, it would cover the template. If it had only one avoiding slot i, adding one role of its nonempty Q_i to K would give a cover of size at most three. Thus w(K)>=2 and rho>=2. Every role footprint of size at most three is likewise missed by some ACTUAL original mask, otherwise it would itself be a cover. This requires no dense complementary-triple pattern.

The supplied S root misses every footprint disjoint from S. One actual root can share arbitrarily many such obligations. This is not an independent reserve per pair; all obligations will be coordinated in ONE actual root order.

## 3. Multi-role localization on any ownership cycle

At a restored partition E, each label not yet in its final D-group supplies an arc from its current owner to its final owner. Remove correct labels from bookkeeping. Equal current/destination sizes give balanced incoming/outgoing multiplicities at each role. A nonempty finite balanced loop-free directed graph contains a simple cycle: an entered vertex cannot be a dead end, and a repeated vertex in a walk supplies a simple cycle. Choose the least cycle and least arc labels using fixed finite orders.

Selected labels x_t move from distinct i_t to i_(t+1), cyclically, for 2<=l<=m. Exactly one label leaves/enters each involved group, so the next partition F restores every b_j and N_i and fixes all selected labels at final owners. Equivalently sigma(x_t)=x_(t-1) has inverse x_(t+1) initially in the required destination group; this agrees with the owner move.

In each actual union E_i union F_i an unselected label has one fixed owner, and selected x_t has two-role footprint {i_t,i_(t+1)}. Pairs of unselected labels, unselected/selected pairs and pairs of adjacent selected edges have footprint of size<=3 and therefore an ACTUAL common witness throughout its entire union and every partial support.

Only selected labels on DISJOINT cycle edges can lack a common witness. If their footprint avoids S the original S root supplies such a witness. Thus every noncommon obligation uses a disjoint edge pair with at least one edge incident to S.

For l<=3 there are none. For l>=4, each cycle edge is disjoint from l-3 other cycle edges. If s=|S intersect {i_1,...,i_l}|, at most 2s edges are incident to S (edges with both ends in S may be counted twice in this incidence bound). Counting each disjoint pair from an incident edge gives at most
    2s(l-3) <= 2p(l-3) <= 2p(m-3)
noncommon obligations. A pair with both edges incident to S may be counted twice; that only enlarges this valid UPPER bound. Additional masks may supply further common witnesses. There is no claim that the count is exact or sharper than all other counts. If S avoids the cycle there are no noncommon obligations.

A remaining pair's union footprint meets S, so at least ONE of its old/new two-role owner sets meets S. Otherwise neither endpoint owner set would meet S, contradicting the footprint intersection. Its actual old/new missed-root sets U_K,V_K therefore have cardinalities at least alpha,rho in one orientation, or rho,alpha in the other. If both owner sets meet S, both counts are at least alpha>=rho, still satisfying the bound. For a genuinely noncommon pair U_K and V_K are disjoint sets of the SAME ORIGINAL indices.

This covers EVERY physical two-label pair, including ordinary labels inside S and pairs with both ends or both footprints overlapping S. No singleton assumption, independent per-role protection system or separate capacity allocation is used.

## 4. Conditional simultaneous handover and literal primitive legality

For disjoint actual old/new witness sets U,V of sizes u,v, the exact fraction of full labelled root orders with all U before all V is 1/binomial(u+v,u): only one of the possible U/V relative words is bad. This is inherited X34 counting. Binomial(u+v,u) increases in each positive coordinate and is symmetric in them. Thus a localized noncommon pair has bad-event fraction at most 1/binomial(alpha+rho,alpha).

By linearity, without independence, the exact mean number of bad pairs obeys
    Psi_cycle <= 2p(m-3)/binomial(alpha+rho,alpha) < 1.
All actual identities and overlapping obligations use ONE original-root order. The S root itself may change; it is not assumed untouched. For obligations whose footprint avoids S, its entire old/new union continues missing the pair even during those changes.

Derive the next root explicitly using inherited X34 conditional averaging. For a completed-root prefix D, average over all full extensions. A common-witness pair contributes zero. If no member of V has appeared, let u' be the number of U still remaining; the contribution is 1/binomial(u'+v,u'), where v=|V|. Once a first V has appeared, contribution is one if all U preceded that first V and zero otherwise. These are exact cases on ACTUAL indices, including value one when u'=0 before any V.

Full extensions split into equally many continuations for each possible next root. Hence Psi(D) is the average of Psi(D,i). Pick the least remaining i with Psi(D,i)<=Psi(D), which exists whenever roots remain. The conditional count stays below one. At a complete order it is an integer number of bad events, so is zero. Thus first(V_K)<last(U_K) simultaneously for every noncommon K. This supplies an eligible next root at every generated prefix rather than assuming a good ordering or extension of arbitrary safe prefixes.

At each scheduled slot, add all actually absent F_i minus E_i incidences individually in palette order, then delete all E_i minus F_i incidences individually. An addition is absent and a deletion present; common incidences are fixed. During expansion the root contains E_i, during contraction it contains F_i, both of size N_i>=a_i. Every intermediate meets its SAME ORIGINAL floor at its SAME labelled slot, even when a_i=N_i and when another included role already contains a nominal replacement label. Arbitrary larger supports are native. Literal finite incidence lists supply each next primitive; equal supports supply no native no-op.

A common witness misses the pair throughout its whole union. Otherwise an untouched actual old witness survives through the first new witness's active edits by first(V)<last(U); after completion that actual new witness protects the pair. Therefore every forbidden pair is missed at EVERY primitive. Because |P|>=m>=4, any cover of size<=1 would extend to a two-label cover; excluding all pairs proves tau>=3.

## 5. Genuine reuse, progress and complete endpoint restoration

Completing one cycle restores every b_j, N_i, SAME mask, supplied S root, alpha,rho, template exactness and H. No protective resource is spent. Removing one incoming/outgoing selected arc per involved role preserves balance. If incorrect labels remain, another simple cycle exists and the SAME strict bound works for ANY such cycle, independently of its length or number of S contacts.

Incorrect-owner count strictly decreases by l after each finite handover; no correct label moves. This well-founded integer measure, eligible next-cycle argument, finite root order and finite primitive lists prove termination at D_j and FULL original labelled/noncompact C_i.

Each label remains at its original owner until its one resolving cycle, then moves directly to its final owner. Masks containing both owners retain its incidence; masks containing neither remain absent; masks containing exactly one toggle its original endpoint-differing incidence once. Other cycles do not edit it. The preliminary lower path therefore has exactly sum_i |A_i symmetric_difference C_i| primitives. Physically silent bookkeeping cycles may be omitted as native no-ops. Repeated endpoint legs renew the input; event counts are per leg, not one global unique-event count across a chain revisiting states.

For X42B first complete the entire ORIGINAL-ended lower path, then apply certified A with q=4: same fixed palette/slots, positive original floors, arbitrary allowed additions/unions, exact-four outer ends and lower bound three match its domain. Conversion gives {3,4} and exact outer-end restoration but not schedule/minimum/internal-waypoint preservation. Do not convert unfinished handovers. On a complete concatenation only outer endpoints are thereby guaranteed.

For X42U select an existing UNSELECTED label in each group of supplied H. Since a simple cycle selects at most one label per group and b_j>=2 in those four groups, four distinct such labels exist. Their owners remain fixed at H at BOTH adjacent partition endpoints. They hit every old/new root; every partial active support contains one such endpoint, so the SAME four labels hit every primitive. This directly proves tau<=4 in addition to lower protection and retains the minimum count. Restored group sizes renew the choice for the next cycle. These are upper-cover representatives, not added palette ingredients or floor slack. Protection may remain at level three within a handover.

## 6. Distinguishable multi-role sparse family with no singleton representation

Fix EVERY p>=2 and n>=5p; m=p+n. Let S={1,...,p}, R={p+1,...,m}, |R|=n. Declare ORIGINAL masks:
- ONE S;
- ONE R minus {u,v} for every unordered pair {u,v} in R;
- ONE G minus {s} for each s in S.
There are r=1+binomial(n,2)+p labelled slots, without duplicate masks or replicas. All supports are nonempty. The broad distinguishing masks are declared original relationships, not roots installed during the repair.

The base S/co-pair family has transversal four: a cover must use at least one S-role and at least three R-roles; every R-pair is missed by its matching high mask, while every R-triple hits all high masks. H={p,p+1,p+2,p+3} covers this family. It also hits every broad G minus {s} root because a four-role set cannot lie in its one-role complement. Thus the full actual template is exact FOUR.

No broad root avoids any two-role pair: its complement has only one role. Pair-avoiding counts therefore remain the base counts:
- a pair entirely in S is avoided by all binomial(n,2) high roots;
- one S-role and one R-role u is avoided by exactly n-1 high roots whose excluded pair contains u;
- a pair {u,v} inside R is avoided by precisely S and its matching high root.
Consequently alpha=n-1 and rho=2.

The criterion follows for ALL n>=5p:
    binomial(n+1,2)-2p(n+p-3)
      = [n^2+(1-4p)n-4p^2+12p]/2.
Write n=5p+d, d>=0. The difference becomes
    [p^2+17p+(6p+1)d+d^2]/2 > 0.
Thus fixed minimum pair redundancy two suffices across unbounded p,n, using actual large asymmetric counts where needed, with no root replication.

The broad roots prevent the naive block collapse back into X41. At either endpoint, every role has a distinct ORIGINAL incidence profile:
- two S-roles a,b are distinguished by G minus {a}, which omits a and contains b;
- an S-role and R-role are distinguished by the S root;
- two R-roles u,v are distinguished by R minus {u,z} for z in R distinct from u,v.
Such z exists because n>=10. Every label of one group has exactly that role's profile.

In ANY representation of the SAME source tuple as unions of a partition's nonempty cells, every cell must consist of labels with identical original-root membership: a root cannot contain only some labels of a cell. Therefore a cell cannot merge two of these distinct role profiles. The S root contains p>=2 distinct profiles; each high root contains n-2>=2, and each broad root contains m-1>=2. NO original root can be exactly one cell. Refining cells cannot change this. Hence NO singleton mask exists in ANY partition-union representation at this endpoint (and similarly at the destination). This is stronger than merely lacking one in the supplied certificate. It does not exclude safely acquiring a different state, applying a different mechanism or native repair. It is an X41 direct-input representation obstruction, not disconnection.

The family also fails X40's global rho test: denominator six whereas m>=12 gives m(m-3)/2>=54. Dense co-triple masks excluding triples J wholly in R are absent: their complements contain all S and n-3>=1 R-roles; S contains no R, high roots contain no S, and every broad root omits an S-role. S width p<m-3 violates X39's dense-width premise. No new connectivity classification is inferred; exact nonuniform X34 counting is the inherited tool being made structurally available.

## 7. Saturated long-cycle controls and reusable unfinished roots

For EVERY p,n above and t>=1, use existing disjoint t-label diagonal cells B_jj and forward cells B_(j,j+1), cyclic j. Source groups are rows, destination groups columns. Every b_j=2t, palette k=2tm. SAME ORIGINAL floors are saturated:
    a_low=2tp,
    a_high=2t(n-2),
    a_broad=2t(m-1).
All are at least four and unequal, since p>=2,n>=5p. Every H group has at least two labels, so X42U directly proves repeated {3,4} minimum-event repair for all these parameters.

The low root has the unique smallest floor; all other floors are at least 2t(n-2). Any four distinct original slots require total size at least
    2t[p+3(n-2)] > 2t(p+n)=k,
because n>3. Four disjoint floor-safe supports cannot fit ANYWHERE. This is a private-root preparation obstruction, not a native no-path result.

The misplaced ownership graph comprises t parallel copies of a directed m-cycle, and has no shorter simple cycle. Every mask is a nonempty proper subset of that connected cycle, so has an entering and leaving edge and changes in every selected cycle.

Selected labels on p->p+1 and p+2->p+3 two-cover the whole cycle and full original endpoint union. The first hits S via p. Their combined R-footprint has three distinct roles p+1,p+2,p+3, at least one in every high mask because only two R-roles are excluded. Each selected label has a two-role footprint, which cannot be wholly excluded by any broad root's one-role complement. Thus broad unions are hit too. Whole-union preparation is unsafe. No assertion excludes all whole-original-root orders or arbitrary contracted auxiliary guards.

For t>=2, after the FIRST complete cycle every root has lost a selected source-only crossing label and gained a selected next-only crossing label, so differs from A_i. An unselected original source-only crossing label remains in its support and is absent from C_i, so it also differs from C_i. ALL original roots remain unfinished relative to BOTH original endpoints. Yet all cardinalities, masks, S, alpha,rho and cover multiplicities have renewed. Residual ownership is exactly t-1 copies of the same long cycle. The next handover exists, and exactly t cycles finish FULL labelled C.

These are symbolic all-parameter proofs. No numerical enumeration, sample, run or benchmark supports or is needed for them. Direct event minimum is mathematical, not measured efficiency.

## 8. Dependencies, genuine advance and remaining hypotheses

Inherited X34 supplies actual bad-event fractions/conditional averaging/shared-witness handover; X40 supplies balanced cycle bookkeeping, general endpoint/event accounting and renewable upper representatives; X41 motivates singleton localization and asymmetric counting. X42 proves localization around an ACTUAL multi-role support S and a conservative asymmetric alpha/rho bound, with a structural family impossible to represent as any singleton template. X41's sharper singleton-specific beta condition remains accepted unchanged.

Certified A is used only after complete lower outer-ended repair; L already connects the symmetry-related endpoints. No frozen dependency is recertified. No arbitrary mixed-floor root permutation, canonical-state access, compaction assumption, supplied short-cycle decomposition, independent per-pair capacity or whole-union safety is inferred.

The direct-input advance removes the singleton representation requirement of X41 under explicit multi-role localization and asymmetric count conditions, even with all roots saturated and all roots unfinished between repeated long handovers. It is not a proof that arbitrary endpoints possess such a small support/template/count margin, nor a claim exact X34 counting previously failed.

Same supplied exact-four patterns, equal positive group sizes, original positive floors, an actual S root and the strict bound remain inputs. Direct upper/minimum additionally needs the H representatives. Arbitrary accessibility, unequal group sizes, scarce upper representatives, unlocalized/below-bound handovers and unrestricted mixed-floor/directed/higher-target/nested universality remain OPEN. Stronger compatible-grade availability stays parallel.

No science commands/tests/workflows, numerical execution, implementation, benchmark, integration merge, numbered certification, literature-originality, physical energy/metric/gravity or fundamental-time claim. v16.55/v16.54 certificates, earlier analytical results and all original evidence remain unchanged. Separate efficiency implementation/fixtures/benchmarks remain unstarted and independently scoped.

Fresh whole review must assess the full theorem and separation/control together: every pair localization and double-count bound, asymmetric orientation/shared actual identities, eligible conditional next root and literal primitive, original floors at saturation, renewed next-cycle existence and finite descent/full exact restoration, lower-converted-direct domains, all-parameter counts/inequality, profile distinction and impossibility of ANY singleton union representation, every saturated long-cycle/unfinished control, plus inherited dependency and novelty limits.
