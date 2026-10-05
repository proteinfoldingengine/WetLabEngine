# A11.X53 - sparse omitted-cover compatibility and conditioned renewal

Analytical parent: ae827216f6c15fa497698a1e27a9df29edef8984.
Scope: f03acbcf84f92695e39408a9139d52a6168ac722.
Exact candidate for fresh independent whole-argument review. Analytical only.

## 1. Native family and main theorem

Fix m>=8 cyclic roles G={0,...,m-1} and singleton physical labels P={x_s:s in G}. Let pi(x_s)=x_(s-1), indices modulo m. Thus physical x_s moves from source role s to destination role s+1.

Let H be a nonempty supplied family of four-role sets with
    |H|<=m-4.
For every four-set J not in H declare n_J>=1 ORIGINAL labelled copies of type
    Q_J=G minus J.
Their physical endpoint supports are
    A_J={x_s:s not in J},
    C_J=pi(A_J)={x_s:s not in pi(J)}.
Each copy has its SAME ORIGINAL positive floor at most m-4.

Define
    K0={0,1,2,3},
    K2=pi(K0)={m-1,0,1,2},
    L={0,1,4,5}.
Require the compatibility conditions
    K0 in H,
    K2 not in H,
    pi^(-1)(K0) not in H,
    L not in H,
    pi^(-1)(L) not in H.
These ensure that the four original types used by the upper relay actually exist.

**X53R - sparse omitted-cover repair.**
Every such pair of endpoints admits a deterministic finite native path with
    3<=tau<=4
at every primitive, all original floors retained, full labelled and noncompact destination restoration, and exactly
    sum_(J not in H) n_J |J symmetric-difference pi(J)|
primitive incidence changes. This is the mathematical endpoint-toggle minimum.

The path processes complete copy blocks in a type order conditioned to satisfy
    Q_L < Q_(pi^-1 K0) < Q_K2 < Q_(pi^-1 L).
The physical covers K0,L,K2 protect all old/new copy coexistence. Exact conditional averaging on the SAME type-order domain proves that an order satisfying those upper constraints and every actual lower pair obligation exists and supplies an eligible next type.

**X53W - exact moving-witness characterization.**
For a physical pair B={x_s,x_t}, put
    F(B)={s,t,s+1,t+1}.
It has an actual common endpoint-union witness exactly when some retained J outside H contains F(B). Hence B needs an old-to-new witness transfer exactly when
    every four-set extension of F(B) belongs to H.
This characterizes all moving lower obligations created by the omitted-cover family; shared roots and overlaps are not counted as separate capacities.

**X53N - renewal.**
Every finite supplied chain of forward rotations in the SAME cyclic role order repeats the construction after exact restoration. Counts are minimum per leg, not necessarily between outermost endpoints.

The whole endpoint-union tuple has hitting number exactly two, and every original type changes. Thus no permanent three-guard made from actual full endpoint unions or unchanged roots proves this result. Contracted auxiliary guards and other native constructions are not excluded.

H is a supplied structural certificate. The size and compatibility conditions are sufficient, not necessary. No arbitrary-accessibility or universal result is asserted.

## 2. Exact endpoint four-covers

For a physical four-set I,
    I misses A_J exactly when I=J.
Therefore I hits every source root exactly when I belongs to H. The complete source four-cover family is H. The destination four-cover family is pi(H).

No triple T hits every source root. It has exactly m-3 four-set extensions. Since |H|<=m-4, at least one extension J lies outside H; the declared Q_J misses T. Smaller sets extend to triples and are missed too. Since H is nonempty, some four-set hits every root. Hence tau(A)=4. Relabelling gives tau(C)=4.

Positive labelled copies do not alter endpoint hitting sets. They are original slots, not resources introduced during repair.

## 3. Exact common-witness characterization

A full endpoint union A_J union C_J avoids B={x_s,x_t} exactly when A_J and C_J both avoid B. Source avoidance means s,t in J. Since C_J has physical complement pi(J), destination avoidance means s,t in pi(J), equivalently s+1,t+1 in J. Thus
    A_J union C_J avoids B
exactly when
    F(B) subset J.

Because J has size four, the possibilities are:
- if |F(B)|=4, a common witness exists exactly when F(B) is outside H;
- if |F(B)|<=3, it exists exactly when at least one four-set extension of F(B) is outside H.

This proves X53W. It also shows directly that one retained root can protect several physical pairs; the proof never allocates its capacity independently.

For boundary witness counts, a source root avoids B whenever J contains {s,t}. There are C(m-2,2) such four-sets in total, at most |H| omitted. The same count holds at the destination by relabelling. Hence every pair has at least
    rho=C(m-2,2)-|H|
actual old witnesses and at least rho actual new witnesses.

Exact-four endpoints already imply these sets are nonempty. The displayed lower bound is stronger and uniform.

## 4. Three-cover coexistence chain

For any physical four-set K, its source exception is exactly type Q_K when K is outside H, and empty when K belongs to H. Its destination exception is exactly type Q_(pi^-1 K) when pi^-1 K is outside H, and empty when K belongs to pi(H).

For K0,L,K2, the compatibility hypotheses give:
    U_0=empty,
    V_0={b}, b=Q_(pi^-1 K0);

    U_1={a}, a=Q_L,
    V_1={d}, d=Q_(pi^-1 L);

    U_2={c}, c=Q_K2,
    V_2=empty.

The four complement sets L, pi^-1 K0, K2 and pi^-1 L are distinct for every m>=8. Thus a,b,c,d are distinct actual original types.

Any total type order satisfying
    a<b<c<d
has a before b and c before d. X51's chain lemma therefore gives a physical cover meeting BOTH endpoint supports of every active type:
- K0 before b;
- L from b through every block before d;
- K2 from d onward.

This includes the active b and d blocks. The cited set hits all earlier destination types, all later source types, both endpoints of the active type, all simultaneous old/new copies and the enlarged active copy. Changing which existential cover is cited is not an incidence primitive.

The endpoint-cover pair K0,K2 alone fails the X50 orientation on this conditioned order: its source exception c occurs after its destination exception b. Intermediate L bridges that declared conflict. Other two-cover choices are not excluded, so no cover-minimum claim is made.

## 5. Conditional lower-witness construction on the same order domain

For each physical pair B let
    O_B={types J:A_J misses B},
    T_B={types J:C_J misses B}.
Pairs with O_B intersect T_B nonempty have an actual union witness and impose no event. For a noncommon pair the sets are disjoint. Its lower bad event is
    every O_B type precedes every T_B type.
In an unrestricted uniformly random total type order its exact probability is
    1/C(|O_B|+|T_B|,|O_B|).
Because both witness counts are at least rho, this is at most
    1/C(2rho,rho).

Let Z be the nonnegative integer number of lower bad events and let D be the order event a<b<c<d. The four types are distinct, so
    Prob(D)=1/24.
There are at most C(m,2) physical pairs. Therefore
    E[Z]<=C(m,2)/C(2rho,rho),
and nonnegativity gives
    E[Z | D]<=24 C(m,2)/C(2rho,rho).

The right side is strictly below one. Indeed |H|<=m-4 gives
    rho>=C(m-2,2)-(m-4)
        =(m^2-7m+14)/2
        >=m+3,
where the last difference is (m-1)(m-8)/2. Central binomial maximality gives
    C(2rho,rho)>=C(2rho,3)>=C(2m+6,3).
Finally
    C(2m+6,3)>24 C(m,2)
because after multiplying by six the difference is
    (2m+6)(2m+5)(2m+4)-72m(m-1)
      =8m^3-12m^2+220m+120>0.
Thus E[Z | D]<1.

This is an exact finite existence bound, not an independence assumption. All pair events and the upper precedence event share the SAME actual type order.

For constructive continuation, at a generated ordered prefix h consider all valid full extensions satisfying D. A prefix is retained only if this set is nonempty. Partition these extensions by eligible next type i. The class weights are their exact positive extension counts divided by the total; they are generally UNEQUAL. The conditional mean of Z at h is the weighted average of the next-class conditional means. Hence some eligible next i has mean no larger than the current mean. Choose the least such i.

The mean stays below one, the number of unchosen types strictly decreases and every chosen prefix has a valid completion satisfying D. At a full order the conditional mean equals integer Z<1, so Z=0. This supplies a finite deterministic type order satisfying both the three-cover chain and all lower pair transfers. It may be factorially expensive to evaluate; no efficiency implementation or bound is claimed.

## 6. Every primitive on actual copied slots

Process types in the constructed order. Within each type process its n_J original labelled copies in labelled order. For each copy add all absent destination-only incidences, then delete all present source-only incidences, using palette order.

During additions the active support contains A_J; during deletions it contains C_J. Both have size m-4, so every same original floor at most m-4 is legal, including saturation and unequal copy floors.

For a pair with a common type witness, every copy of that type avoids the pair throughout its endpoint-containing edit. For a noncommon pair, Z=0 means
    first(T_B)<last(O_B).
Until the first new witness type begins to complete, a later untouched old witness type remains. During the first new type's entire copy block that later old type remains untouched. After the first copy of the new type completes, an actual new witness persists. This proves tau>=3 at every primitive for arbitrary positive multiplicities.

Equivalently, select the active actual copy as its type representative and an actual endpoint copy of every other type. The representative tuple lies on the lower-safe type path. Extra copies cannot destroy an avoiding witness.

Section 4 supplies tau<=4 on the SAME primitives. Hence the actual path is directly in the one-unit band; maximum-layer conversion is not used.

Every listed addition is absent and every deletion present. Finite type, copy and incidence lists supply each next primitive. The pending-edit count decreases by one. Common incidences remain fixed, all lists finish, and every labelled root reaches its full noncompact destination.

The primitive total is
    sum_(J not in H) n_J |A_J symmetric-difference C_J|
      =sum_(J not in H) n_J |J symmetric-difference pi(J)|.
Every endpoint-differing incidence must change at least once on any native path. This attains the endpoint-toggle minimum.

## 7. Moving protection and lack of a permanent union guard

Consider B_star={x_0,x_2}. Its footprint is K0. A retained four-set J contains that footprint only if J=K0, but K0 belongs to H and its complementary root is absent. By X53W, B_star has no common union witness. Indeed it hits every actual endpoint union.

No singleton hits all endpoint unions. For x_s, an endpoint union avoids it whenever retained J contains {s,s+1}. There are C(m-2,2) such four-sets, more than |H|<=m-4, so at least one is retained. Therefore the complete endpoint-union tuple has hitting number exactly two.

Every retained type changes. A four-set invariant under the transitive full cyclic shift would be empty or all G, impossible for m>=8. Thus there is no unchanged background root.

Additional members of H can create additional moving obligations. Precisely those pairs whose footprint-extension family lies inside H require transfer. For example the even cyclic-window family H={W_t:t even}, W_t={t,t+1,t+2,t+3}, satisfies |H|=m/2<=m-4 and the compatibility exclusions. Its m/2 diagonal pairs have four-point footprints in H. This accepted alternating family is a control contained in the new general class, not claimed as newly discovered here.

The novelty is the arbitrary supplied H theorem and joint conditioned order, not the already-known special family. A failed size bound or compatibility exclusion does not prove disconnection.

## 8. Renewal and limits

At a completed forward leg the same omitted mask family H, positive original copy counts and original floors are restored on the next singleton role partition. Rename existing physical representatives by their current roles. The exact cover characterization, witness counts, compatibility exclusions, four distinguished types and strict conditional margin recur unchanged.

For every finite supplied chain of forward rotations in this SAME cyclic role order, rebuild the conditional type order and execute its finite copy blocks. Every leg reaches its exact labelled endpoint directly in {3,4}. Protection may remain at level three internally; it need not reset to exact four after each block. Concatenation is finite. The incidence minimum is per leg; revisited outer incidences prevent a general global-minimum claim.

This theorem permits linearly many omitted roots and potentially many transferring lower obligations. It remains a dense complementary-four construction with singleton roles, a supplied H, a full cyclic ownership rotation and four explicit compatibility exclusions. It does not prove arbitrary endpoints can acquire this representation, unequal corresponding role sizes, sparse declared root families, an all-order multicover obstruction, or unrestricted mixed-floor, directed, higher-target or nested universality.

Frozen X34/X35 supply the actual pair-order criterion. X49 retains its failed generic copy lift. X50/X51 supply the coexistence interfaces; X52 supplies the physical convention and conditioned-order lemma, reproved here where used. Frozen sources are not rewritten or recertified. Native symmetry connectivity was already known; the advance is a direct minimum-event renewable explanation for a larger structural class.

No scientific commands/tests, numerical workflow, implementation, benchmark, integration merge, numbered certification, literature-originality or physical claim. Certified v16.55/v16.54 and all evidence remain preserved. Separate efficiency runner/fixtures/benchmarks remain unstarted.

Next: remove the dense complementary-four carrier, derive compatible relays when the strict conditional count fails, or obtain an all-order structural obstruction without confusing it with native disconnection.
