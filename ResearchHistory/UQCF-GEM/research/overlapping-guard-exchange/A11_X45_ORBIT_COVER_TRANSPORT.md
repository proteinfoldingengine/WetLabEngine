# A11.X45 — permutation-orbit cover transport below global majority

Exact analytical candidate. Scope 1fb37f8b170067ec494079ae8733b39c824aa54f; accepted analytical parent 090f684531de77a3c319c7419cab41b7c56e3f87.
No numerical execution, implementation, benchmark or numbered certification.

## 1. Native carrier and typed statements

Fix a finite ordered palette P, labelled original roots and their SAME ORIGINAL positive floors a_i. A primitive adds or removes ONE incidence in ONE root. Larger intermediate supports are permitted; no label/root is added, no floor weakened, and no simultaneous move, compactness or geometry is imposed.

Supply m>=4 nonempty role groups B_j,D_j partitioning P with equal positive corresponding sizes b_j, and SAME nonempty actual masks Q_i subset G=[m]. Put

    A_i=union_{j in Q_i} B_j,
    C_i=union_{j in Q_i} D_j,
    N_i=sum_{j in Q_i} b_j,

and require 0<a_i<=N_i. The template transversal is EXACT FOUR. Let

    H4={I subset G: |I|=4 and I intersects every Q_i}

be the family of ALL four-role covers.

At a restored partition E, suppose a lower mechanism selects one actual label on every role of a simple ownership cycle and fixes one representative outside it. The selected labels move to the next cycle roles, inducing a role permutation pi; the fixed representatives make pi the identity elsewhere. Suppose the lower handover processes roots so each partial active root contains its old endpoint during additions or its next endpoint during deletions, while every other root is old or completed next.

**X45C (exact representative criterion).** For that prescribed representative pool and pi, FOUR SAME representatives cover both restored endpoints if and only if

    H4 intersect pi^{-1}(H4) is nonempty.

Equivalently, in the directed cycle decomposition of pi acting on the four-subsets of G, some orbit has two consecutive vertices in H4. The least compatible four-set gives a deterministic eligible choice. More than half of one orbit is sufficient. A nonempty pi-invariant subfamily of H4 is sufficient. Neither condition requires global majority.

**X45R (renewable orbit-compatible upper interface).** If a complete lower-protected path is built from finitely many such restored handovers and the exact criterion holds for every chosen pi, the SAME physical path also has tau<=4 at every primitive. If the lower theorem separately gives tau>=3, same-slot floor legality, eligible next moves, finite descent and FULL exact destination restoration, the combined path is direct {3,4}. If each endpoint-differing incidence is toggled once by the lower path, that mathematical minimum is retained. Restoring the mask template renews the orbit test; X45 does not supply the lower theorem.

**X45F (vanishing-density block-orbit family).** For EVERY q>=2 and ell>=6, there is an exact-four template on m=q ell roles whose four-cover family has exactly m members and density

    m/binomial(m,4)=24/[(m-1)(m-2)(m-3)] -> 0.

With singleton source/destination groups and a destination permutation comprising q disjoint directed ell-cycles, accepted X40L plus X45R give q renewable long handovers, direct 3<=tau<=4, exact endpoint-event minimum and FULL labelled/noncompact restoration at arbitrary same original positive floors<=m-4, including complete saturation.

This family is outside X38's short-cycle condition, X39's width premise, X40U's unselected-cover condition, X43's one-plus-three size domain, X44's majority domain and every singleton-mask representation of the same endpoint. L already connects these symmetry endpoints. The advance is a permutation-sensitive upper interface and a sparse repeated separation, not new native connectivity or universal accessibility.

## 2. Exact compatibility and orbit formulation

At a restored partition E choose representatives z_j, one actual label per role: the selected cycle label on each cycle role and the least current label elsewhere. They are distinct because the groups partition P. At the next restored partition F, z_j has owner pi(j).

For a four-set I subset G put K_I={z_j:j in I}. At E, K_I hits every physical root exactly when I hits every Q_i, that is, I in H4. At F its owner-role set is pi(I), so K_I hits every next root exactly when pi(I) in H4. Therefore the SAME four representatives cover both endpoints exactly when I lies in H4 intersect pi^{-1}(H4). The least such I in the fixed lexicographic order is deterministic.

This is an if-and-only-if statement for the declared representative lift. It is not a claim that every possible four-label cover of arbitrary intermediate states must use this pool. Exact template four ensures any compatible representative set has four distinct owner roles; a repeated role would induce a template cover of size at most three.

The permutation pi acts bijectively on Omega=binomial(G,4), decomposing it into directed cyclic orbits. The intersection condition says precisely that for some I in H4, the next orbit vertex pi(I) also lies in H4. Thus the occupied vertices of some orbit contain an adjacent pair, including the wraparound edge.

An independent set in a cycle of length d has size at most floor(d/2). Hence if one orbit O satisfies

    |H4 intersect O|>floor(|O|/2),

it contains an adjacent occupied pair. This local condition can hold while H4 is an arbitrarily small fraction of all Omega. Also, if nonempty F subset H4 obeys pi(F)=F, then every I in F has pi(I) in F subset H4. Choosing the least I in F is sufficient. Local majority and invariance are sufficient corollaries, not necessary conditions; orbit adjacency itself is exact for this lift.

X44 follows as a different global sufficient argument: if |H4|>|Omega|/2, then H4 and pi^{-1}(H4) intersect for every pi. X45 trades that permutation-uniform density condition for knowledge of the actual prescribed pi.

## 3. Lift through every primitive and renewal

Let I be compatible and K_I the four physical representatives. Every untouched root is at its old endpoint and every completed root at its next endpoint. During additions the active support contains its old endpoint; during deletions it contains its next endpoint. K_I hits each of those endpoint supports and therefore every partial support. Thus tau<=4 at every primitive.

Nothing here proves tau>=3 or floor legality. Actual pair witnesses, a compatible root order, literal incidence availability and same-slot floors remain obligations of the lower theorem on the SAME path. X45 also does not derive a simple ownership cycle or a well-founded descent.

At a completed handover, every group size and actual mask is restored. Therefore H4 and the orbit criterion are again available for the next lower-selected cycle permutation, possibly with a different compatible I and four different physical representatives. Protection is renewed rather than consumed. Exact four need not be restored after each primitive; only the next restored partition boundary is used.

If every lower handover is finite, the lower progress measure strictly decreases after each, and the criterion holds at every boundary, concatenation reaches the exact destination. Since X45 adds no primitive, any lower proof that fixes common incidences and toggles every original differing incidence once keeps the exact count

    sum_i |A_i symmetric_difference C_i|.

No maximum-layer conversion is used for this direct conclusion.

## 4. The block-orbit template and its exact covers

Fix q>=2 and ell>=6. Partition G into q disjoint blocks

    G=B^1 disjoint-union ... disjoint-union B^q,

each supplied with a cyclic order and |B^s|=ell. Put m=q ell, so m>=12.

Let H consist of every cyclic interval of FOUR consecutive roles inside one block. Each block supplies ell distinct intervals, so |H|=q ell=m.

For every four-set J subset G with J notin H, declare ONE labelled original root with mask

    Q_J=G minus J.

There are binomial(m,4)-m original roots. Every mask has width m-4>=8. There are no other roots or duplicate masks.

For any four-set I and declared Q_J,

    I misses Q_J
    iff I subset J
    iff I=J,

because |I|=|J|=4. Consequently I hits every declared mask exactly when I is not one of the declared non-H sets. Therefore the family of ALL four-role covers is exactly

    H4=H.

It remains to exclude a smaller cover. Any three-set T belongs to at most two four-consecutive intervals: if T meets two blocks it belongs to none; inside one cyclic block, three distinct points fit into at most the two length-four intervals obtained by extending a consecutive triple at its two ends, and every nonconsecutive triple has no more choices. But T has m-3>=9 distinct four-set extensions T union {x}. At least one extension J is not in H. Then the declared Q_J misses T. Any set of fewer than three roles can be extended to a three-set and is missed as well. Thus no at-most-three role set covers, while every H member is a four-cover. The template transversal is EXACT FOUR.

The global cover density is

    |H4|/binomial(m,4)
      =m/binomial(m,4)
      =24/[(m-1)(m-2)(m-3)],

which is below one half for m>=12 and tends to zero as m grows. This is symbolic for the whole family, not a finite enumeration.

## 5. Actual pair redundancy and inherited lower repair

For a role pair K, the declared root Q_J avoids K exactly when K subset J. There are binomial(m-2,2) four-sets J containing K. We omit only those J in H.

A pair from different blocks lies in no H interval. A pair within one cyclic block lies in at most three four-consecutive intervals: an adjacent pair can occupy positions (1,2), (2,3) or (3,4), and larger cyclic separation gives no more. Adjacent pairs attain three because ell>=6. Hence the actual pair redundancy is exactly

    rho=min_K |{J notin H: K subset J}|
       =binomial(m-2,2)-3
       =m(m-5)/2.

For m>=12,

    rho-(m-3)=(m-1)(m-6)/2>=0.

Put n=m-3>=9. Coordinate monotonicity of the central binomial coefficient and maximality of its middle term give

    binomial(2rho,rho)
      >=binomial(2n,n)
      >=binomial(2n,2)
      =n(2n-1)
      >n(n+3)/2
      =m(m-3)/2.

The strict inequality is equivalent to 3n>5. Therefore accepted X40L applies to this actual template for every allowed equal corresponding group size and every same original positive floor, including saturation.

X40L supplies the independent lower obligations: a deterministic simple ownership cycle, an actual conditional root order simultaneously preserving every pair witness, literal add-before-delete primitive lists, tau>=3 at every primitive, same-slot floor legality, restored masks and group sizes, decreasing incorrect-owner count, and FULL labelled/noncompact destination restoration. It also fixes common incidences and toggles every endpoint-differing incidence once. X45 does not recertify or alter that frozen proof.

## 6. Singleton block rotations and q renewable long handovers

Give every role one actual label x_j. Thus all source groups B_j are singletons. In each block, let the destination owner of x_j be the next role in that block's cyclic order. Destination groups are also singletons. The misplaced ownership graph is the disjoint union of exactly q directed simple cycles, each of length ell>=6, with no shorter simple cycle.

At any unfinished restored boundary, X40 selects one of the remaining block cycles. Its induced permutation pi rotates that block once and fixes all other roles. The full H is pi-invariant: intervals in the active block rotate to intervals, while intervals in other blocks are fixed.

Choose the least interval I in the ACTIVE block. Then pi(I) is the next interval, so both lie in H4. The four representatives in K_I are all selected labels and all four change owner. They cover the old and next endpoints and every partial root by Sections 2–3. There is no unselected label in any active-cycle group and no fixed-label cover is being smuggled into the argument.

The X40 handover gives tau>=3, floors and the legal root schedule; X45 gives tau<=4 on the SAME primitives. Completing the block cycle fixes all ell selected labels at final owners and restores the exact template. The remaining ownership graph is the disjoint union of q-1 block cycles. Repeating gives exactly q finite long handovers. The incorrect-owner count falls by ell each time and reaches zero.

At termination every singleton group is its specified destination group and every labelled original root is its FULL noncompact destination support. Every endpoint-differing incidence toggles once and every common incidence stays fixed, so the direct {3,4} path has the mathematical minimum number of primitives.

Take arbitrary same original floors 0<a_J<=m-4. In particular the completely saturated choice

    a_J=m-4 for every original root

has no root-floor reserve and all floors are at least eight. The number q of renewed handovers and their common length ell can grow independently. This proves reusable low-density transport, not one fortunate exchange.

## 7. Separation from accepted sufficient classes

**X38.** Its reserve-free repeated theorem requires no simple ownership cycle longer than three. Here every nontrivial ownership cycle has length ell>=6.

**X39.** Its dense-width premise requires every actual mask to have width at least m-3. Every X45F mask has width exactly m-4.

**X40U.** Its direct upper argument requires two existing labels in each role of one minimum cover. Every role group here is a singleton, and every minimum cover contains four roles. X40L applies only as the lower theorem; X45 supplies the missing direct upper bound.

**X43.** It must choose an ACTUAL root mask S of size p with complement size n>=p+3. Every actual mask here has p=m-4 and complement size four, so the required inequality would be 4>=m-1, false for m>=12. This exhausts all actual roots before even testing its one-plus-three cover property.

**X44.** The exact cover density is below one half, so its strict-majority hypothesis fails. X45 does not contradict X44; it exploits only the actual block rotations, not every permutation.

**No singleton representation.** Distinct roles have distinct original incidence profiles. For roles a!=b, there are binomial(m-2,3) four-sets containing a and not b, while at most four H intervals contain a. Since m>=12, choose such a four-set J notin H. The original root Q_J omits a and contains b.

In any representation of the SAME endpoint as unions of nonempty partition cells, a cell must be profile-homogeneous: no original root may contain only part of a cell. Hence distinct roles cannot be merged into one cell. Every original root contains m-4>=8 distinct role profiles, so no root can be exactly one cell. Therefore X41's singleton direct-input hypothesis is unavailable in ANY partition-union representation of this endpoint. This does not exclude a safe path to a different representation or another repair theorem.

These are sufficient-method separations. They do not prove native disconnection outside X45 or failure of every alternative construction. Certified L already connects the endpoints by palette symmetry.

## 8. Saturated controls and unsafe global preparation

Under the saturated floors, four pairwise disjoint floor-safe supports would require at least

    4(m-4)>m=|P|

distinct palette incidences. Thus no four private/disjoint floor-safe roots can fit anywhere on this carrier. This is a preparation obstruction, not a no-path result.

The rootwise whole original endpoint union is two-covered. In one block take labels x_a and x_(a+2). Their old/new owner footprints are

    {a,a+1} and {a+2,a+3},

whose union I is four consecutive roles and hence lies in H4. For every root Q_J, I intersects Q_J. Therefore at least one of the two labels occurs in that root's source/destination union. The pair {x_a,x_(a+2)} hits every whole-union root, so its hitting number is at most two. Simultaneous whole-union preparation is unsafe.

Every original root changes between the endpoints. If Q_J were invariant under the product of block rotations, its complement J would be invariant. The orbits of that permutation on roles are the entire ell-role blocks. An invariant role set is a union of whole blocks, impossible for |J|=4<ell. Again this is a control on the declared endpoint pair, not an assertion about all intermediate roots after each completed block.

The accepted lower schedule transfers actual pair protection root by root while X45 transports a four-cover along the active block orbit. Neither requires disjoint private guards or the unsafe global union.

## 9. Exact advance and remaining obligation

X45 identifies the correct permutation-sensitive object: adjacency of actual minimum covers under the induced action on four-subsets. Global cover density can vanish; what matters for a prescribed handover is organized occupancy of its permutation orbits. The block family makes this organization renewable across arbitrarily many saturated long cycles, with all active cover labels moving.

The criterion is exact only for the declared representative lift. A failed intersection is not a no-path theorem, not failure of every four-label choice outside that pool, and not a lower-guard obstruction. The block family is a supplied equal-size mask representation; arbitrary endpoints need not admit it or reach it safely.

Same supplied exact-four template, equal positive corresponding group sizes, a typed one-label simple-cycle/endpoint-containing lower path and compatibility for each selected permutation remain inputs. The family obtains the lower path from X40's pair-redundancy bound. Unequal corresponding sizes, below-bound lower repair, deriving orbit compatibility from arbitrary endpoints, arbitrary permutation families, and unrestricted mixed-floor/directed/higher-target/nested universality remain OPEN. Stronger compatible-grade research remains parallel.

No scientific commands, enumeration, numerical workflow, implementation, benchmark, integration merge, new numbered certificate, literature-originality or physical energy/metric/gravity/fundamental-time claim. v16.55/v16.54, frozen sources and all original evidence remain unchanged. The separate efficiency implementation/fixtures/benchmarks remain unstarted and independently scoped.

Fresh independent whole review must check X45C/R/F together: the exact representative iff and orbit adjacency; local majority/invariance qualifications; every partial-root upper lift; exact cover-family/no-three-cover proof; pair redundancy and X40 inequality; shared lower/upper path; q-cycle renewal, progress, event minimum and exact restoration; all class separations/profile argument; saturated disjoint and two-cover whole-union controls; and every inherited-domain limitation.
