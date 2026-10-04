# A11.X34 — derived coupled witness handover and reusable completion

Scope freeze: efd6dea7b73809e4c1f8fb2daf1ab7936c87eacc.
Analytical parent: eb676d5ddb63c2a45715d3590ab99fc70ce1f5a5.
Status: exact candidate for fresh independent whole-argument review. Analytical only.
The completed bounded v16.55 certificate and certified v16.54 sources are unchanged.

## 1. Statements and native domain

Fix an ordered palette P of k>=4 labels, r labelled slots and ORIGINAL positive floors a_i<=k. Legal roots E_i subset P satisfy |E_i|>=a_i. A primitive toggles ONE incidence in ONE slot. The motivating mixed-floor domain has a_i>=3; the argument also works for arbitrary positive floors. No slot permutation, new label, spare slot or compact-support restriction is used.

For every two-label set K define the ACTUAL witness sets

    U_K={i: A_i intersect K is empty},
    V_K={i: C_i intersect K is empty}.

Assume tau(A),tau(C)>=3, so these sets are nonempty. Pair protection is exactly tau>=3: every pair misses an actual root. A smaller hitting set could be extended to a pair, since k>=4.

Define

    Psi(A,C)=sum over K with U_K intersect V_K empty
                         1/binomial(|U_K|+|V_K|,|U_K|).

**X34C — derived completion.** If Psi(A,C)<1, there is a deterministic finite native path A -> C preserving tau>=3 and every original floor, restoring the FULL original labelled destination. Each root is processed once, by all missing destination additions followed by all old-only deletions. The preliminary path has exactly sum_i |A_i symmetric_difference C_i| primitive moves. A conditional version supplies an eligible continuation from every root-order prefix whose conditional count remains below one.

**X34R — reusable actual-redundancy class.** Fix rho>=1 with

    binomial(k,2)/binomial(2rho,rho)<1.

On any fixed original carrier, ALL states having at least rho actual missed roots for EVERY pair satisfy X34C between any two of them. Consequently every finite chain of such specified states can be reached completely in order. No reserve is consumed: each full destination restores the same actual redundancy condition for another handover. The intermediate paths need only preserve level three.

**X34B — exact endpoint band.** For ORIGINAL exact-four A,C satisfying X34C, accepted maximum-layer theorem A converts the COMPLETE lower path to a finite native path with tau in {3,4}, reaching exactly C. For a chain whose first/last states are exact four, first concatenate the complete lower paths and only then apply A to the entire original-ended path. The converted path need not retain the one-pass schedule or length bound.

**X34F — genuinely combined control.** Section 5 constructs an infinite mixed-floor family with no three-guard at all in the componentwise source/destination UNION tuple. A specified legal prefix reaches level THREE where neither the completed new roots nor the remaining old roots independently form a three-guard. Its conditional count is nevertheless strictly below one, deriving an eligible continuation to the exact destination. At both endpoints X33's actual simultaneously-good-label guard placement fails. This is a limitation of that entry mechanism, not native disconnection or failure of every older sufficient theorem.

The general safe-order criterion is inherited from A2. The new claim is the quantitative derivation of order availability, its conditional continuation certificate and reusable actual-redundancy class. X32's conditional-expectation principle is acknowledged; here it orders changes to shared roots rather than placing destination tokens outside all edits.

## 2. Actual protection along an ordered handover

Take a permutation of ALL labelled slots. For slot i, add labels in C_i minus A_i individually, in palette order, then delete labels in A_i minus C_i individually. An already-equal root needs no primitives but may retain its place in the ordering argument.

Floors hold during additions because the root contains A_i; during deletions it contains C_i. Every support remains a subset of P and of A_i union C_i. Every intermediate support is permitted by the original carrier. No grade or support token is moved to another slot.

For a pair K with a common index i in U_K intersect V_K, BOTH endpoint supports at i avoid K. Thus its whole union and every intermediate support avoid K. The index may change support; it need not be an unchanged old guard.

For disjoint U_K,V_K, the inherited one-pass order condition is

    first(V_K) < last(U_K).

Before the first V_K slot is completed, the last U_K slot is still untouched, including through the first V_K slot's active union, so its ACTUAL old support avoids K. After completion the first V_K slot's ACTUAL destination support avoids K and persists. This covers every primitive, not just completed row boundaries. Different pairs can use different witnesses at different stages, including the SAME shared labelled roots; no independent pair capacities are assumed.

Conversely, if every U_K slot precedes every V_K slot, during the last U_K root's union there is no old missed root left elsewhere and no new missed root ready. The active union meets K because its index is not in V_K. Every other root also meets K. Thus this particular whole-root method loses lower protection.

Call this ordering failure B_K. It is a method event, not a native obstruction. Common-index pairs have no such event. Section 3 derives an order avoiding ALL B_K simultaneously.

## 3. Counting derives an eligible next slot

Count ALL r! permutations of the actual labelled slots. For disjoint U_K,V_K of sizes u,v, their relative u+v positions are uniformly occupied by the two sets. Exactly one of the binomial(u+v,u) possible old/new patterns has ALL old indices before ALL new indices. Thus

    fraction of permutations satisfying B_K = 1/binomial(u+v,u).

This is finite counting, not a randomized scientific execution. By summing indicator functions, Psi(A,C) is the mean NUMBER of failed pair events. Shared roots create dependencies between events, but linearity of this sum needs NO independence.

For an ordered prefix D of distinct completed slots, let Psi(D) be the mean number of B_K over ALL full permutations extending that EXACT ordered prefix. It is explicitly computable from actual endpoint witnesses, without searching a native graph:

- Common-index pair: contribution zero.
- Disjoint pair, with NO V_K slot yet in D: let u' be the number of U_K slots outside D and v=|V_K|. Contribution is 1/binomial(u'+v,u'). In particular it is one if u'=0.
- Disjoint pair, with a V_K slot in D: contribution is zero if any U_K slot remains outside D, or if any U_K slot occurs after the first V_K slot inside D. Otherwise every U_K slot already precedes the first V_K slot, and contribution is one.

These cases are exhaustive and exact. Slots belonging to neither witness set only dilute positions, not their relative pattern.

If m=r-|D|>0, extension permutations partition equally by their next labelled slot. Therefore

    Psi(D) = (1/m) sum over i outside D Psi(D followed by i).

There EXISTS an i outside D with Psi(D followed by i)<=Psi(D). Choose the least such index. Starting at any prefix with Psi(D)<1, repeat this rule. The number of unchosen slots decreases strictly; an eligible next choice exists whenever it is positive. At a full permutation Psi is an integer counting bad pairs. It stays strictly below one, so is ZERO.

This supplies a finite order rather than assuming that a potential can decrease or that a compatible order exists. It also proves that any prefix CERTIFIED by Psi(D)<1 has a complete safe extension. It does NOT claim that every lower-safe prefix has that certificate or can finish by this method.

One can first complete the order analytically and then execute its legal primitive list. Every prefix, including any previously supplied certified prefix, belongs to a bad-event-free completion, so Section 2 proves safety during all its active roots. Once a chosen root is begun, the missing destination additions and then old-only deletions give an eligible primitive whenever that root is unfinished. Their number is finite and decreases by one at each edit. The outer unprocessed-slot count decreases on completion. This proves next-edit existence, termination and full labelled restoration separately.

## 4. Derived bounds and renewal

For integers u,v>=rho,

    binomial(u+v,u)>=binomial(2rho,rho).

Indeed increasing either u or v weakly increases the binomial coefficient, by the ratios (u+v+1)/(u+1) and (u+v+1)/(v+1). Thus every noncommon pair contributes at most 1/binomial(2rho,rho). There are at most binomial(k,2) pairs. This proves X34R.

The sharper X34C criterion can succeed without uniform redundancy. At exact four every pair has at least TWO missed roots: if only one root misses K, add one label from that nonempty root to get a hitting set of size at most three; if none misses K, K itself hits. Hence if at most FIVE pairs lack common source/destination indices, Psi<=5/binomial(4,2)=5/6<1. This is a sufficient actual-overlap corollary, not a claim that all exact endpoints have few such pairs.

Renewal means restoration of a certified next-stage input, not requiring exact-four reset at every unfinished handover. For a finite specified chain E^0,...,E^m in the redundancy class, apply X34C independently to each adjacent pair on the SAME fixed carrier. Each segment restores its full labelled endpoint, including the actual witness multiplicities required for the next segment. Alternatively use the conditional prefix theorem inside a segment; Section 5 supplies a critical level-three example. There is no disappearing reserve and no borrowing of a root with another floor.

A is the ONLY inherited connectivity conversion needed: positive floors, arbitrary allowed incidence additions and componentwise unions, fixed palette/slots, finite lower path and exact-four original endpoints all match its domain. Apply it after the full path exists. Intermediate upper excursions in that lower path are allowed. A preserves original endpoints, floors and single-incidence legality but does not promise the preliminary move count or destination monotonicity.

No exact compaction, minimum-cover selection, guard buffer, palette slack, element-cover argument, symmetry or mixed-grade slot permutation is used. Their applicability is neither presumed nor claimed absent. The same-slot requirement of X5 is not an input here.

## 5. Infinite mixed-floor family with interdependent protection

### 5.1 Fixed carrier and explicit endpoint construction

Let k>=8, P any ordered k-label palette,

    N=binomial(k,3), D=N+1, h=k-3.

Declare one original floor-three slot, N labelled base slots of original floor h indexed by all triples Q, and D further labelled floor-h slots. These are original endpoint slots, not roots added during repair. The two original grades are distinct since h>=5.

Choose disjoint triples T,S. Source low root is T; its base high root at Q is P minus Q; every further high root is P minus T.

There exists a permutation pi of the triples with Q intersect pi(Q) empty for EVERY Q. Here is a self-contained finite construction. Make a bipartite graph with all triples on each side, joining disjoint triples. Every vertex has d=binomial(k-3,3)>0 neighbors. For any left subset X, its d|X| edges enter at most d|Neighbors(X)| available incidences, so |Neighbors(X)|>=|X|. Starting with a partial matching, choose an unmatched left vertex and explore alternating paths. If no unmatched right vertex were reachable, every reachable right vertex would be matched back into the reachable left set, which additionally contains the unmatched starting vertex. All neighbors of that left set are reachable right vertices, giving strictly fewer neighbors than left vertices, a contradiction. Thus an augmenting path exists. Choose the least shortest path under the fixed orders and augment; unmatched count decreases. A complete matching results and defines pi. No simulation or numerical enumeration is used.

Destination low root is S; base root at Q is P minus pi(Q); every further high root is P minus S. All supports meet their ORIGINAL labelled floors.

At either endpoint the base complements are ALL triples. Any set of at most three labels is contained in one of these triples, whose actual root misses it. Thus tau>=4. Every four-label set hits each high support, since a three-label complement cannot contain it; choose a four-set meeting the low triple. Therefore BOTH endpoints are EXACT FOUR.

Every pair K is contained in exactly k-2 base triples, giving at least k-2 ACTUAL missed roots at EACH endpoint. Since

    binomial(2k-4,k-2)>=binomial(2k-4,2)>binomial(k,2)

for k>=8, X34R applies with rho=k-2. The second strict inequality follows from
(2k-4)(2k-5)-k(k-1)=3k^2-17k+20>0 for k>=8.
The first inequality follows from unimodality toward the central binomial coefficient. This is an infinite structurally specified family, not a checklist of campaigns.

### 5.2 No static union guard and failure of the X33 entry mechanism

Every base high union is

    (P minus Q) union (P minus pi(Q)) = P,

because the two triples are disjoint. Every further high union is P because T,S are disjoint. The low union is T union S. The whole union tuple has tau=ONE: any label in T union S hits every root. No subfamily of these source/destination union supports is a three-guard. All high supports change. Thus safety cannot be supplied by a static family of union-compatible protecting roots.

At the source, X33's actual simultaneously-good label must belong to T because the floor-three grade has just one root and a good label may be absent from at most floor(1/2)=0 such roots. For any x in T, however, the high grade has

    g_high(x)=binomial(k-1,2)+D > N
             =floor((N+D)/2)

roots avoiding x. Hence NO label is good simultaneously in the two original grades. At the destination replace T by S for the identical obstruction. Also X33's derived grade bad-count bounds are k-3 and 5, whose sum is k+2, so its strict carrier bound does not apply. This diagnoses that particular actual entry/placement mechanism only.

No claim is made that this family falls outside X32, degree-cap methods or every earlier connectivity theorem. Its role is to prove an interdependent handover with no static union guard and no X33 good-label entry. The new mathematical content is derived order/continuation availability.

### 5.3 A critical level-three prefix with neither side independently protecting

Choose K={x,y} with x in T and y outside T. The low source meets K, and the further source high roots P minus T meet K through y. Thus the source missed-root set U_K consists EXACTLY of the k-2 base slots Q containing K.

Choose any u outside K. There is a unique base slot b with pi(Q_b)=K union {u}. Its source triple Q_b is disjoint from K, so b is NOT in U_K.

Supply this prefix: complete b first, then complete all k-2 slots in U_K, in their fixed order. The prefix has k-1 slots.

K is protected by old U_K roots while b is installed, then by the installed destination support at b. For EVERY OTHER pair J, at most ONE of its k-2 old base witnesses is among these k-1 slots. If J shares one label with K, just one triple containing K can contain J, and Q_b cannot contain J because it avoids K. If J is disjoint from K, no triple containing K contains J, and only Q_b can do so. Therefore at least k-3 untouched ACTUAL old base witnesses protect J at every primitive in this prefix.

At the completed prefix:
- ALL remaining old roots meet K: every source witness to K was processed.
- All completed new roots admit a two-label hitting set L={x,z}, where z is outside K union {u}. The new root at b contains z. Every other processed slot has old triple containing K and hence its new triple pi(Q) avoids K; its new support contains x.
Thus neither the remaining old family nor the completed new family independently forms a three-guard.

The COMBINED actual tuple still has tau>=3 by the witnesses just proved. Its ONLY missed root for K is b: other completed new supports meet K through x, and all remaining old supports meet K. Adding z from that root to K hits the entire tuple, so tau<=3. Its hitting number is EXACTLY THREE.

### 5.4 Derived completion survives that critical prefix

For K, B_K is already impossible: a new witness b preceded all old witnesses.

For every J!=K, at least k-3 source witnesses remain. If a destination J witness has already been processed, B_J is impossible because an old witness still occurs later. Otherwise ALL its at least k-2 destination witnesses remain. Section 3's exact conditional fraction is then at most

    1/binomial(2k-5,k-3).

Common-index events still have contribution zero. Therefore the specified prefix satisfies

    Psi(prefix)<=binomial(k,2)/binomial(2k-5,k-3)<1.

Indeed binomial(2k-5,k-3)>=binomial(2k-5,2), and
(2k-5)(2k-6)-k(k-1)=3(k-2)(k-5)>0 for k>=8.

X34C's conditional construction now supplies the next eligible root and a finite completion to the FULL exact-four destination. This particular level-three prefix is proved extendible; we have not inferred extension from safety alone. No exact-four reset is required before continued progress.

Every full endpoint of the family again has k-2 actual witnesses per pair, regardless of its low triple, chosen triple permutation or duplicate supports complementary to the low triple. Thus arbitrarily many finite adjacent handovers in this fixed carrier can use X34R. For the especially coupled control choose adjacent disjoint low triples and a disjoint-triple matching each time. The same original slots/floors are retained; labels and roots are never added by a move.

## 6. Scientific meaning, inherited limits and remaining obligation

The mechanism is a progressive transfer of ACTUAL missed-root obligations. Shared root identities are accounted for jointly by ordering events. A quantitative count proves an eligible continuation at every certified prefix, even when old and new families separately have two-label transversals. Full endpoint restoration renews the actual input for repeated use.

This strengthens A2's assumed safe-order/acyclic certificate by DERIVING one from witness multiplicities. It differs from X32's placement leaving a source witness outside ALL patches and X33's separately placed grade-compatible guards. It does not require a whole old or whole new guard to stay intact throughout the critical stage.

The inequality is sufficient, not necessary or sharp. Psi>=1 can coexist with a safe root order, and absence of a whole-root order still permits interleaved edits, temporary incidences, repeated changes and other native paths. The accepted bounded-participation incompleteness result forbids treating this method as universally complete. No native disconnection theorem follows from a failed bound or failed placement.

The universal mixed-floor root question, stronger destination-directed scheduling question and unrestricted nested question remain separate. X34B alone does not guarantee a child interface. No new physical law, numerical execution, efficiency result or numbered certification is claimed.

Next obligation: derive the strict conditional bound from weaker endpoint structural constraints, or establish an interleaved/repeated overlapping handover where the whole-root ordering method has no compatible order. In either case prove actual witnesses, legal next edits, shared capacity, renewal and complete original-ended restoration before A conversion.

## 7. Dependency anchors for whole-argument review

All at analytical parent eb676d5ddb63c2a45715d3590ab99fc70ce1f5a5 unless stated:
- SEQUENTIAL_HANDOVER.md, blob b754237cf56ab4592eec82c81ebf00817f85ab43: inherited exact one-pass ordering criterion.
- A11_GLOBAL_SCHEDULE_REDUCTION.md, blob 02324d7054b847a0c105b95e2eec3e918483b0d1: broader I11 criterion and limits.
- A11_X30_LOCALIZED_DEFECT_RENEWAL.md, blob 4d1bbd6234ff99d1d0643a77faa460674f711d66: prior localized patch.
- A11_X32_WITNESS_PRESERVING_PLACEMENT.md, blob 7adf1d9fecece6afa0370d48d033bead5762a7c3: prior conditional expectation for placement.
- A11_X33_SIMULTANEOUS_GRADE_GUARDS.md, blob ef93c4010d7f22c1db18c349de06ad9f54a429a1: exact actual good-label condition.
- METHOD_COMPLETENESS_DECISION.md and METHOD_LIMITS.md: restricted-method failures do not establish native barriers.
- Certified v16.54 GENERAL_PARENT_CONNECTIVITY.md at 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, blob 922ae44713c6810c5a99716c52ecb37738a880a6: ONLY connectivity dependency A, positive-floor union-closed root domain.

No frozen dependency is modified. Scope discloses all preliminary reasoning known before freeze. Independent review must assess this ENTIRE argument, not just the local union moves or final inequality.
