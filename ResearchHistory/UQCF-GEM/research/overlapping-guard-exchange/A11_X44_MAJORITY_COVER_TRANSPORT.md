# A11.X44 — majority-cover transport beyond typed cover patterns

Exact analytical candidate. Scope f1bd8022142fa751948599cadf474fac28b71a0b; accepted analytical parent fee852f07ca8db8296197c41ab418b89a6437335.
No numerical execution or numbered certification.

## 1. Native carrier and typed conclusions

Fix a finite ordered palette P, original labelled root slots and SAME ORIGINAL positive floors a_i. A primitive adds or removes ONE incidence in ONE root. Larger intermediate supports are permitted; no label/root is added, no floor weakened and no simultaneous move or geometry is imposed.

Supply m>=4 nonempty role groups B_j,D_j partitioning P with equal positive corresponding sizes b_j, and SAME nonempty actual masks Q_i subset G=[m]. Put
    A_i=union_{j in Q_i}B_j,
    C_i=union_{j in Q_i}D_j,
    N_i=sum_{j in Q_i}b_j,
and require 0<a_i<=N_i. The template transversal is EXACT FOUR. Let
    H4={I subset G: |I|=4 and I intersects every Q_i}
be the family of ALL four-role covers.

**X44M (majority-cover transport).** If |H4|>binomial(m,4)/2, then for EVERY permutation pi of G there is a deterministically chosen I in H4 with pi(I) in H4. For any adjacent partition exchange realizing pi, FOUR SAME ACTUAL labels cover both endpoint tuples and every add-before-delete primitive. No fixed cover type, unchanged owner or group multiplicity beyond nonemptiness is required.

**X44R (direct renewable repair).** Suppose a supplied lower cycle theorem gives, for every unfinished restored partition, a finite add-before-delete handover to a next restored partition, preserving tau>=3, all original floors and a strictly decreasing endpoint-progress measure. If the SAME actual mask template and majority condition renew at every restored boundary, X44M upgrades that SAME path directly to 3<=tau<=4. It preserves any one-toggle endpoint event count already proved for the lower path. This is a reusable upper-interface theorem, not an independent lower repair theorem.

**X44F (two-small-root sparse separation family).** For EVERY h>=3, put m=3h and partition roles G=S disjoint-union T disjoint-union U with all three blocks of size h. Declare ALL co-triple masks G minus J for J in binomial(G,3), plus the two actual roots S and T. The template is exact four and its four-cover family has strict majority. X42 localized lower repair applies using either S or T; X44M gives DIRECT event-minimum band repair for ALL positive equal corresponding group sizes and all same original positive floors<=N_i.

This family lies outside X39's all-mask width premise, outside X43's typed one-plus-three condition for EVERY possible supplied original root, and has no singleton mask in ANY partition-union representation of the same endpoint. The endpoints were already symmetry-connected by accepted L. The advance is a broader renewable upper interface and a strict structural separation, not new connectivity or universal accessibility.

## 2. Majority intersection theorem

Let Omega=binomial(G,4), a finite set. For a permutation pi of G, define
    pi^{-1}(H4)={I in Omega: pi(I) in H4}.
The induced action on four-subsets is a bijection, so
    |pi^{-1}(H4)|=|H4|>|Omega|/2.
Two subsets of a finite universe, each larger than half, must intersect:
    |H4 intersect pi^{-1}(H4)|
      >=2|H4|-|Omega|>0.
Choose the least member I of this intersection under the fixed lexicographic role order. This is a literal eligible deterministic choice. By definition, I and pi(I) both hit every ACTUAL mask. Exact template four makes each a minimum role cover.

The strict half threshold is sufficient for EVERY permutation with no knowledge of its cycle type. Equality is not enough for the bare set-intersection argument: two half-sized subsets of an even universe can be disjoint. No converse or realizability of that abstract sharpness example as a mask-template cover family is claimed.

This result neither enumerates covers computationally nor chooses them randomly. It is a finite cardinality theorem on the actual declared cover family.

## 3. SAME four physical labels through a prescribed exchange

At a restored partition E, suppose the lower mechanism selects a simple ownership cycle and one actual misplaced label in each cycle role. Let pi be the resulting role permutation: it sends each cycle role to the next and fixes other roles. Define one representative z_j for every role:
- at a cycle role, z_j is the selected label currently in that group;
- elsewhere, z_j is the least current label in the nonempty group.

The z_j are distinct because the current groups partition P. At the next restored partition F, z_j has owner pi(j). For the deterministic I supplied by X44M, put K={z_j:j in I}. These are FOUR SAME actual labels. Their old owner set is I and their next owner set is pi(I), so K hits every old E_i and every next F_i.

In an add-before-delete handover, an active root contains E_i throughout expansion and F_i throughout contraction. An untouched root is old; a completed root is next. Hence the SAME K hits EVERY physical support at EVERY single-incidence prefix. The four labels may all move and their owner-role types may change arbitrarily. No unselected label, fixed H, b_j>=2 or X43 bipartition is used.

This proves only the upper bound tau<=4. Pair witnesses and tau>=3, actual next-root availability, primitive legality and same-slot floors must come from the supplied lower theorem on the SAME path. X44R explicitly requires those obligations rather than treating cover transport as repair by itself.

At each restored boundary, the role mask template is unchanged, so H4 and its strict majority are unchanged. The theorem applies afresh to ANY next cycle permutation; the new four labels can differ from the previous four. Upper protection is renewed rather than consumed.

## 4. Composition with X42 lower repair

For the family in Section 5, use accepted X42L. More generally this paragraph records the exact inherited composition, without extending X42's source.

A restored ownership graph is balanced because current and destination role groups have equal sizes. If labels remain misplaced, it contains a simple directed cycle. X42 selects such a cycle and actual labels, derives a simultaneous original-root order from actual pair witnesses, and edits every scheduled root by adding literal absent next incidences before deleting literal old-only incidences.

Throughout that lower handover every palette pair has an ACTUAL common old/new witness or an untouched old witness until a new witness completes. Thus tau>=3 at every primitive. The active root contains an old or next support of cardinality N_i, preserving its SAME ORIGINAL floor a_i even at saturation. Finite conditional root choices and literal incidence lists supply every next primitive.

Completing a cycle restores every b_j,N_i and the SAME masks. It fixes selected labels at final owners, removes balanced arcs and strictly decreases the number of incorrectly owned labels. If unfinished, another cycle exists. The lower sufficient inputs and majority cover family therefore renew together. Repetition terminates at every D_j and FULL original labelled/noncompact C_i.

Each label remains at its original owner until one resolving cycle and then moves directly to its final owner. Common incidences stay fixed; each original differing incidence toggles once. X44M adds tau<=4 to this SAME path, so DIRECT 3<=tau<=4 and the primitive count remains exactly
    sum_i |A_i symmetric_difference C_i|.
No A conversion is used. The minimum is a combinatorial endpoint-event count, not measured runtime.

## 5. Infinite two-small-root family

Fix h>=3, m=3h and disjoint S,T,U of size h. Original ACTUAL masks are:
- Q_J=G minus J for EVERY three-role set J subset G;
- ONE S;
- ONE T.
There are binomial(m,3)+2 labelled original roots, with no duplicate co-triple masks.

### Exact four and exact cover family

Every three-role set J misses Q_J, so no three roles cover the co-triple roots. Every four-role set intersects every Q_J, because a four-set cannot be contained in the three-set complement J. Adding S,T cannot lower transversal. Four-covers exist, for example a set with one role from S, one from T and any two other distinct roles. Hence the full template transversal is EXACT FOUR.

A four-set covers all co-triples automatically. It covers the two additional roots exactly when it meets both S and T. Therefore
    |H4|=binomial(3h,4)-2binomial(2h,4)+binomial(h,4),
by inclusion-exclusion: subtract sets avoiding S or avoiding T and add those avoiding both, which lie in U.

Its excess over half the full universe has twice-value
    2|H4|-binomial(3h,4)
      =binomial(3h,4)-4binomial(2h,4)+2binomial(h,4)
      =h(h-1)(19h^2+37h-18)/24.
The factorization follows by expanding binomial(x,4)=(x^4-6x^3+11x^2-6x)/24. It is strictly positive for h>=3 (indeed for h>=2). Thus H4 is a strict majority, symbolically for every parameter, without enumeration.

### Actual lower witness counts

For a role pair K, co-triple root Q_J avoids K exactly when K subset J. There are m-2 choices of the third role of J. Thus EVERY pair has at least m-2 actual avoiding original roots, before counting possible avoidance by S or T. Using the actual S root for X42 localization gives p=h and
    alpha>=m-2, rho>=m-2.

The central binomial coefficient is coordinate-monotone, so
    binomial(alpha+rho,alpha)>=binomial(2m-4,m-2).
The middle coefficient is at least binomial(2m-4,2), and
    binomial(2m-4,2)-2h(m-3)
      =(3h-2)(6h-5)-2h(3h-3)
      =12h^2-21h+10>0
for h>=3. Therefore X42's strict lower condition
    binomial(alpha+rho,alpha)>2p(m-3)
holds. All obligations use the SAME original co-triple/root identities; no per-pair duplicate capacity is invented.

X42 supplies complete lower repair at arbitrary original positive floors<=N_i, including saturation. X44 supplies the direct upper bound for all positive corresponding b_j. Together they prove X44F.

## 6. Separation from prior sufficient cover classes

X39 requires every original mask to have width at least m-3. The actual S and T roots have width h<m-3=3h-3, so its dense-width premise fails.

X43 could choose only an ACTUAL original root as its block. Choosing S fails its EVERY one-block/three-complement cover property: select one S role and three U roles; this four-set misses T because h>=3. Choosing T fails symmetrically. Choosing a co-triple root Q_J gives block size p'=m-3 and complement size n'=3, violating X43's n'>=p'+3 requirement. These exhaust all original masks. Thus NO original root supplies X43's sufficient input.

There is no singleton mask in ANY partition-union representation of the SAME endpoint. Co-triple roots distinguish every pair of roles: for a!=b choose a three-set J containing a but not b; Q_J omits a and contains b. Hence all role incidence profiles across original roots are distinct. Any cell in any union-partition representation must be profile-homogeneous, because every root is a union of complete cells. It cannot merge different roles. Every original root contains at least h>=3 distinct profiles, so no root can be a single cell. This excludes X41's singleton direct-input representation at the endpoint, not a safe route to another state or native connectivity.

X40's global rho condition actually holds strongly here because rho>=m-2; X44 does not claim a lower-protection advance beyond X42/X40 on this family. Its new content is upper-cover transport outside X43's typed property and X39's dense all-root class. Prior X39/X43 domains remain valid.

## 7. Saturated singleton-group long-cycle control

Set b_j=1 for EVERY role. Take one source label x_j in each role and destination owner j+1 in a fixed cyclic order listing all S roles, then all T roles, then all U roles. The ownership graph is one directed m-cycle; every palette label moves and there is NO unselected label.

Use saturated SAME ORIGINAL floors:
- a_S=a_T=h;
- every co-triple root has a_J=m-3=3h-3.
All floors are at least three, and the carrier has two distinct grades. Every mask is a nonempty proper subset of the connected cycle, so every original root changes.

X42 lower protection plus X44 majority transport gives a direct minimum-event {3,4} path. The four SAME upper-cover labels supplied by X44 may all change owners. The exact labelled destination is reached in one completed ownership cycle, while individual physical root changes still use a conditionally derived order.

Four disjoint floor-safe supports cannot fit ANYWHERE. There are only two low-floor slots; any four distinct original slots require at least
    2h+2(m-3)=8h-6>m=3h
palette incidences. This is a private/disjoint preparation obstruction, not native disconnection.

The full cycle/rootwise original endpoint union is two-covered. Choose the selected label on the block-boundary edge from the last S role to the first T role and the selected label from the last T role to the first U role. Their combined role footprint contains four distinct roles, meets S and T, and therefore is a four-cover of the whole template. Each of the TWO labels hits every root union through its two-role footprint collectively; equivalently the pair's four roles cover every mask. Thus tau of the whole-union tuple is at most two, making simultaneous whole-union preparation unsafe. The conclusion is a method limit only, not failure of every whole-root order or path.

Because all role profiles are distinct and each has one label, no SAME-state regrouping creates a group of size two or an unselected representative. This control simultaneously lies outside X41 direct singleton input and X43 typed cover transport, while X44 completes it.

## 8. Advance, limits and publication obligations

X44M is a general upper-interface theorem: strict majority of actual minimum four-covers guarantees compatible SAME-label transport for every prescribed ownership permutation. It replaces X43's special typed cover construction within a wider but different sufficient domain. Some X43 families have cover density below half, so neither theorem contains the other.

X44F proves the new interface is nonempty and structurally distinct. X42/X34 supply lower protection and root ordering; X40 supplies the inherited cycle/event accounting; X43 supplies the prior scarce-representative comparison. Certified L already connects these symmetry endpoints. No new native connectivity classification or independent lower theorem is claimed.

The strict majority condition, SAME supplied exact-four template, equal positive corresponding group sizes and a separately valid renewable lower cycle mechanism remain inputs. Failure at half or below is not a no-cover-transport or no-path theorem; X43 itself works below half. Arbitrary access to a qualifying representation, unequal corresponding sizes, templates lacking either cover condition, below-bound/unlocalized lower repair and unrestricted mixed-floor/directed/higher-target/nested universality remain OPEN. Stronger compatible-grade research remains parallel.

No scientific commands/tests/enumerations, numerical workflow, implementation, benchmark, integration merge, numbered certification, literature-originality or physical energy/metric/gravity/fundamental-time result. v16.55/v16.54, frozen prior proofs and ALL original evidence remain unchanged. Separate efficiency implementation/fixtures/benchmarks remain unstarted and independently scoped.

Fresh independent whole review must check X44M/X44R/X44F together: strict majority intersection and SAME-label lift, separation of upper/lower duties, renewal/progress/exact restoration/event minimum, exact family cover count/factorization and lower witness inequality, exhaustive X39/X43/singleton separation, saturated no-unselected control, disjoint/whole-union method limits and all inherited-domain qualifications.
