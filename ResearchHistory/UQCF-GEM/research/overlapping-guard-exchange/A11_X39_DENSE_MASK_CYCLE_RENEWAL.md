# A11.X39 — derived reserve-free renewal for arbitrary ownership cycles

Scope 87009d0a9bb4ed3b07e2308a5444a1749e0cde24; analytical parent 97b818b0953ebc76efaff42e427ae9512df1a1db.
Status: exact mathematical candidate for fresh independent whole-argument review.
No scientific execution, code, benchmark or numbered certification.

## 1. Native objects and exact claims

Fix a finite ordered palette P, r labelled ACTUAL roots and SAME ORIGINAL positive floors a_i. A primitive adds/removes ONE incidence in ONE actual root. Native larger supports, temporary incidences and repeated changes remain permitted; this theorem constructs a stricter event-unique path without imposing that restriction on native admissibility.

Supply m>=4 group roles, nonempty source/destination partitions B_j,D_j of the SAME palette, and the SAME nonempty actual mask Q_i at each slot. Require

    |B_j|=|D_j|=b_j>0,
    |Q_i|>=m-3,
    A_i=union_{j in Q_i}B_j,
    C_i=union_{j in Q_i}D_j,
    N_i=sum_{j in Q_i}b_j,
    0<a_i<=N_i.

A is exact FOUR. Section 2 derives exactness of C and the needed ACTUAL protecting family; alternatively both original endpoints may already be declared exact four. Group roles describe supplied actual incidence patterns; they are not extra root slots, geometry or new primitives. The width assumption is an openly sufficient structural condition, not a change to the native rules.

**X39D — exactness derives complementary witnesses.** At least ONE ACTUAL root mask equals the complement of EVERY three-index set. Hence r>=binomial(m,3); every group-index pair has at least m-2 actual missed roots, and EVERY four-index set is a minimum template cover. Additional ORIGINAL roots/multiplicities are allowed, with any masks of width at least m-3 and their own positive floors.

**X39C — arbitrary-cycle witness bound.** For a directed simple misplaced-label cycle of length l, 2<=l<=m, define its exact next partition by moving each selected label to its own final group. If l<=3, every palette pair has an actual common old/new witness. If l>=4, the ONLY noncommon pair obligations are pairs of selected labels on disjoint cycle edges; there are exactly l(l-3)/2. Both actual endpoint witness sets for each have at least m-2 roots, so

    Psi_cycle <= [l(l-3)/2]/binomial(2m-4,m-2) < 1.

The strict inequality holds for ALL m>=4 and all eligible lengths. Shared labelled roots are counted jointly through X34's exact conditional mean, with no independence or separate capacities.

**X39R — reserve-free complete renewable repair.** These endpoints admit a deterministic finite native path with3<=tau<=4 at EVERY primitive, even with all original floors SATURATED a_i=N_i. Balanced actual ownership supplies an eligible cycle whenever unfinished; the derived bound supplies an eligible full handover for EVERY such cycle. Completed cycles restore all group/root sizes, strictly decrease incorrect labels and renew the same derived witness input. The full original labelled/noncompact C is restored. Every destination-only incidence toggles ONCE, every source-only incidence ONCE, common incidences remain fixed; the primitive count is exactly sum_i |A_i symmetric_difference C_i|. This is an analytical minimum-event count, NOT a runtime benchmark.

**X39F — unbounded long-cycle control.** Section 6 supplies all m>=5,t>=1 oriented m-cycle inputs with saturated or unequal original floors. No short ownership cycle exists, no four disjoint floor-safe roots fit anywhere, every actual root changes, and expanding an entire cycle union gives an actual two-cover. Nevertheless X39R completes repair. At t>=2 the first completed cycle restores every size while ALL original roots remain unfinished; an eligible next long cycle is derived.

This removes X37's reserve and X38's short-cycle restriction WITHIN the supplied dense-mask family. It does not remove arbitrary-template/equal-group-size hypotheses or subsume every sparser template accepted by X38/X37. All endpoints here were ALREADY palette-symmetry connected by L. The advance is a derived event-minimal, reserve-free renewal interface, not a new connectivity classification, universal numerical coverage or established literature-originality claim.

## 2. Exact-four consistency forces the actual protecting roots

Choose any three distinct group indices J and one actual label from each nonempty B_j. Exact-four A requires an ACTUAL root missing that three-label set. Its supplied mask Q_i must avoid J. Thus Q_i is contained in the m-3-index complement of J; the width premise forces equality:

    Q_i={1,...,m} minus J.

Different J require different actual slots, because their masks differ. These roots are not manufactured; they already exist in the original tuple and original floor vector.

A label cover at any restored partition induces its set of group owners. Any at-most-three owner indices are contained in some J, whose actual complementary root misses them; this excludes every at-most-three actual cover. Conversely ANY four distinct group indices intersect every Q_i, because a Q_i of width>=m-3 cannot fit into their m-4-index complement. Representatives of those four nonempty groups hit every actual root. Every restored partition is therefore exact FOUR, with a supplied actual minimum cover.

For a group-index pair S, every J of size three containing S gives a different actual missed root. There are exactly m-2 such J. Additional original root masks or duplicates can increase witness counts, never remove these actual witnesses. This proves X39D at every restored partition; it is renewed automatically when group sizes and root masks are restored.

No exact compaction, guard token relocation, added slot/label or original-floor exchange is involved. The consistency argument works on the supplied original supports, including larger original root masks and arbitrary b_j.

## 3. Actual ownership cycles and complete pair accounting

At a structural boundary E represent actual roots by a partition L_j with sizes b_j. For every incorrectly owned label x draw the arc from its current group u to its destination group v. Correct labels have no arc. Cancelling correct labels from equal current/destination group counts shows incoming=outgoing at every group.

If any arc remains, follow outgoing arcs: an entered vertex of positive indegree has positive outdegree by balance. Finiteness yields a directed simple cycle. Choose the lexicographically least simple cycle, with least available palette label on each edge. Its distinct labels x_1,...,x_l initially occupy distinct groups i_1,...,i_l and finally belong to i_2,...,i_l,i_1.

Define a palette permutation sigma(x_t)=x_(t-1), cyclic subscripts, with other labels fixed. Applying sigma to E makes x_t occupy group i_(t+1): its inverse x_(t+1) was in that group. Each group exchanges exactly one outgoing and incoming label. The exact next partition F restores all b_j and N_i and fixes these selected labels.

In the ACTUAL union U_i=E_i union F_i, every selected label x_t has expanded footprint {i_t,i_(t+1)}. Each ordinary label has one unchanged group role.

For EVERY palette pair K:
- Two ordinary labels use at most two expanded roles.
- One selected and one ordinary label use at most three.
- Two selected labels on adjacent cycle edges use at most three.
In all these cases choose a three-index J containing their footprint. The ACTUAL root with mask complement J misses K at BOTH endpoints and through its entire union. It is a common actual witness, even if that root changes other incidences.

The remaining case consists of two selected labels on DISJOINT cycle edges, possible only at l>=4. Their source owner set S and destination owner set T each contain TWO indices and are disjoint, so their full footprint has four. No actual Q_i of width>=m-3 can avoid four indices, so old/new witness sets have NO common root. Both have at least m-2 actual members by Section 2.

A simple undirected l-cycle for l>=4 has binomial(l,2) edge pairs, exactly l of them adjacent. Therefore the count of these noncommon ACTUAL palette-pair obligations is

    d_l=binomial(l,2)-l=l(l-3)/2.

Each selected label is distinct, so these are genuine distinct two-label sets, not duplicate records assigned to independent resources. For l2 its two expanded links coincide; for l3 every pair of links is adjacent; both have d_l=0. This exhausts ALL palette pairs, including all ordinary labels outside the cycle and all large-support roots. It does not check only one anchor subsystem.

## 4. Derived handover, eligible edits, original floors and upper cover

### 4.1 A strict bound for every cycle length

For noncommon K write u=|U_K|,v=|V_K|. Both are at least m-2, and binomial(u+v,u) is nondecreasing in either argument. Thus each inherited X34 bad-event fraction is at most1/binomial(2m-4,m-2). Section 3 yields the claimed Psi_cycle bound.

Let n=m-2>=2, B_n=binomial(2n,n), R_n=(n+2)(n-1)/2. At n2, B_2=6>2=R_2. For n>=2,

    B_(n+1)/B_n=2(2n+1)/(n+1)>3,
    3R_n-R_(n+1)=(2n^2-6)/2>0.

Induction gives B_n>R_n for every n>=2. Since l<=m, d_l<=m(m-3)/2=R_(m-2), proving strict Psi_cycle<1 for every possible simple cycle, independently of palette size, group cardinalities, root multiplicities and original floors. For short cycles Psi=0.

### 4.2 Literal conditional construction and actual pair protection

Use the accepted X34 deterministic ordering construction on EXACT adjacent E,F and their actual missed-root sets. Its premises are satisfied: both endpoints exact4, SAME positive original floors, finite fixed palette/slots, actual count<1. We restate its certificate to identify the actual next move, not merely assert that a safe order exists.

For a pair with a common root index, that root's entire union misses the pair. For disjoint U_K,V_K, a whole-root replacement order is safe when

    first(V_K)<last(U_K).

Before the first new witness finishes, the last old witness is untouched, including while that first new root is active. Afterward the completed new witness persists. These are actual endpoint roots on the SAME original slots, accounting for shared pair obligations jointly.

For an ordered prefix D of completed root indices, let Psi(D) be the exact mean number of bad events over all permutations of the remaining labelled indices appended to D. X34 supplies its actual witness formula: common witnesses contribute zero; if no V_K index is yet completed and u' old witnesses remain, contribution is1/binomial(u'+v,u'); if a V_K index has completed, contribution is zero unless all old witnesses preceded the first such index, when it is one.

The extensions split equally by their next actual index:

    Psi(D)=average_{i outside D}Psi(D followed by i).

Choose the least index whose conditional value is no larger than Psi(D). Such an index exists whenever an unprocessed root remains. Starting below one and decreasing the remaining-root count reaches a full order with integer bad-event count below one, hence ZERO. This constructs a complete safe order and proves conditional eligible continuation. Dependencies between pairs cause no problem: the mean sums actual bad-event indicators without requiring independence.

For each root in that finite order, add every F_i minus E_i label individually in palette order, then remove every E_i minus F_i label individually. Each listed addition is actually absent and each deletion actually present; common incidences are fixed. Addition prefixes contain E_i; deletion prefixes contain F_i. Both have size N_i and meet SAME original a_i, so every intermediate support stays at least N_i, including saturation. A nominal replacement already present is not double-counted: only actually absent additions are performed, and the full destination support remains contained during contraction.

For every forbidden pair, the just-proved old/new/common witness rule supplies an ACTUAL missing root at every single-incidence prefix, including active union supports. No root's capacity is allocated separately to different witnesses. An already equal root needs no primitive but can retain its position in the ordering certificate. A silent cycle uses no native no-op. Literal remaining root/label lists supply the next legal primitive throughout each handover. Extension is proved for these certified prefixes, not all arbitrary safe prefixes.

### 4.3 Actual FOUR-label cover at every primitive

Unlike a general X34 handover, this cycle has an ACTUAL four-label set hitting BOTH E and F rootwise. For l>=4 choose any four selected cycle labels. Their source owners are four distinct indices and their destination owners also four distinct indices. For l2/3 choose all selected labels and one label from each of 4-l distinct outside groups; these ordinary labels are unchanged. At both endpoints the owner set has exactly four indices.

Every such owner set meets every Q_i by width>=m-3, so these SAME four actual labels hit each E_i and each F_i. At an active root, expansion contains E_i and contraction contains F_i; other roots are old or completed new. Thus this same actual four-cover hits the entire physical tuple at EVERY primitive.

Together with actual pair witnesses this gives3<=tau<=4 DIRECTLY, preserving the event-unique schedule and minimum count. A's general complete-lower-path conversion is NOT invoked. No upper-layer assumption is applied to an unfinished prefix.

## 5. Renewed eligibility, finite progress and full restoration

Complete the supplied root order for the selected cycle. The partition is now F, all group sizes b_j and actual root cardinalities N_i are restored, including saturated floors. The exactness/width argument of Section 2 supplies the same actual witness lower bound again. No finite reserve has been consumed and none must be replenished.

Every selected label now has its final owner, with no correct label displaced. Remove the corresponding cycle arcs. Balance persists because one incoming and one outgoing arc is removed at every involved group. Unlike X38, NO condition on remaining cycle lengths is needed: any nonempty balanced residual graph again supplies a simple cycle, and Section 4's strict bound holds for ANY length up to m. This gives an eligible next handover whenever unfinished.

The nonnegative number of incorrectly owned labels strictly decreases by l after each finite exchange. Each exchange has finitely many root/label edits with explicit eligibility. The sequence terminates at zero and EVERY group becomes D_j. Consequently each SAME labelled actual root is precisely its FULL original destination C_i, including all noncompact incidences.

An original label remains in its original group until its unique resolving cycle, then moves directly to its final group. A root containing both old and final group indices retains the common incidence throughout; one containing neither stays absent; a root containing exactly one has the corresponding original differing incidence added/deleted ONCE. Other cycles do not touch that label. Thus the total native primitive count is exactly sum_i |A_i symmetric_difference C_i|, the unavoidable toggle minimum for these endpoints. This is not a runtime, execution or efficiency benchmark.

For any finite specified chain of group partitions on the SAME masks/cardinalities/floors, reconstruct the balanced ownership graph for each next leg. Exactness and dense width derive every new witness input, and the same theorem supplies complete repair. Full endpoints are restored; inside a handover protection may remain at level3 with certified next edits. Renewal does not mean an exact-four reset after each individual incidence. Arbitrary safe-prefix extension remains unproved.

## 6. Infinite saturated long-cycle family and repeated unfinished roots

For ALL m>=5,t>=1 take existing disjoint t-label cells B_jj and B_(j,j+1) for j=1,...,m, cyclic j+1. Source groups are rows and destination groups columns. Each group has b_j=2t, palette k=2mt. Actual root masks are all complements of three-index sets, ordered lexicographically by the excluded triple. Thus r=binomial(m,3), each root size N=2t(m-3), and both endpoints are exact FOUR.

Two ORIGINAL floor profiles are openly specified:
- saturated: every a_i=N;
- unequal: the first floor(r/2) slots have a_i=N, all remaining slots a_i=N-1.
Both are positive (N>=4) and fixed. X39R covers both without reserve or floor exchange.

Misplaced ownership is exactly t parallel copies of the directed m-cycle. There are NO shorter simple ownership cycles, so neither a short-cycle decomposition nor X38's graph condition is available on these inputs. This excludes that stated ownership method only, not arbitrary palette-transposition paths or every original whole-root order.

Every Q_i is a nonempty proper subset of a connected cycle, so there is at least one cycle edge entering it and one leaving it. Accordingly EVERY actual root changes between the original endpoints. Four disjoint floor-safe roots cannot fit anywhere: even the mixed profile has minimum N-1 and

    4(N-1)-k=6t(m-4)-4>0

for all m>=5,t>=1. This is a palette/floor obstruction to four private roots, not native disconnection.

An entire m-cycle union is unsafe. Choose selected labels on edges1->2 and3->4. Their union roles span four distinct indices and hit every root mask; they form an actual two-cover of the full expanded tuple. The same labels also two-cover the whole original A/C union. Every label's union footprint has at most two indices, and an actual complementary-triple mask avoids it, so no singleton covers that union. Its transversal is EXACTLY TWO. No subfamily of those actual union roots is a three-guard; contracted auxiliary supports are not excluded.

X39C instead derives d_m=m(m-3)/2 actual noncommon obligations, each with at least m-2 old and new roots, and strict count<1. For the unpadded control there are exactly m-2 witnesses on each side. Complete the deterministic witnessed root order, never expanding the whole tuple simultaneously. The common actual four-cover is any four selected cycle labels, while progressive actual old/new witnesses exclude every pair.

At t>=2, after the FIRST completed cycle each proper Q_i has lost at least one selected old-only label and gained at least one selected destination-only label, so it differs from the original A_i. At least one more cell-copy label remains on each crossing edge, so a source-only incidence still present is absent from original C_i; the root also differs from C_i. Therefore ALL binomial(m,3) actual roots are unfinished relative to BOTH original endpoints, yet EVERY cardinality N and all original floors are restored. The residual ownership graph is exactly t-1 copies of the same long cycle. Section 5 supplies another eligible handover; repeat t times and restore the exact labelled C.

This is an unbounded structural family in cycle length and repeated use, not a checklist of isolated carrier runs. No numerical enumeration is executed. No claim asserts that every whole-original-root order fails on this family or that this directed construction is the only native route.

## 7. Inherited domains, scientific advance and remaining obligation

At parent97b818b0953ebc76efaff42e427ae9512df1a1db:
- A11_X34_COUPLED_WITNESS_HANDOVER.md (accepted candidateed68d5be73e986bab193c1393d7c1c1f066660f3, blobb9b4fde21b3b830f99e158ad909d2ac440d8e469): actual bad-event fractions and conditional averaging used in Section 4.
- SEQUENTIAL_HANDOVER.md: exact whole-root actual-witness criterion inherited through X34.
- A11_X38_TRIANGLE_CYCLE_RENEWAL.md, blobabb8304dd3c76356ada9ab5d92b2aae516bdc5a3: short-cycle reserve-free comparison and full-union long-cycle obstruction.
- A11_X37_SHARED_ROLE_CYCLE_RENEWAL.md, blobf057022ba890a74a37c30b4983a1be9000f8914a: arbitrary-cycle adjacent-link lift with original reserve; no saturated extension is inferred.
- A11_GLOBAL_SCHEDULE_REDUCTION.md (I11): event-unique scheduling context, not an existence dependency.

At certified466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, demos/v16.54-parent-support-connectivity/OVERLAPPING_CLIQUE_EXCHANGE.md, blob865f0797892a2e5e869ec2180d3c842026889445: L already connects all these equal-group-size endpoints by palette permutations at their same original floors. Its unrestricted path can use repeated/non-destination incidences. J/M/N, exact compaction, guard-buffer, palette-room and element-cover results are not needed for this proof. A's conversion is unnecessary because Section 4.3 supplies direct upper protection. Frozen sources/implementations are not rewritten or recertified.

The new derivation combines exact endpoint consistency, actual witness multiplicity and cycle-local event count. It shows why replacement protection is available on the existing shared roots, supplies an eligible root order and native primitive, and restores the same structure for arbitrarily many further cycles. This is more than declaring accessibility or listing safe moves: it proves availability, renewal and complete exact destination restoration. X34's ordering/counting mechanism and L's connectivity are openly inherited; no new universal or literature-originality claim is made.

Dense-mask group representation and equal corresponding sizes remain sufficient inputs. Extending to sparser actual templates without reserve, unequal group sizes, or deriving template accessibility from arbitrary exact-four endpoints remains OPEN. X38's arbitrary-template short-cycle result and X37's reserve-bearing broader cycles remain valid and are not subsumed outside this dense family. General A11 directed/root mixed/higher-target/nested universality and stronger compatible-grade directions stay separate.

No numerical science/tests/workflows, implementation, new efficiency fixture/benchmark, integration merge or numbered certification. v16.55 remains CLOSED/CERTIFIED in its approved bounded scope, v16.54 and every original archive remain unchanged. Separate efficiency work remains unstarted and independently scoped. This concerns ordered repair/retained recoverability, not fundamental time, physical energy/metric/gravity.

Fresh whole review must inspect X39D/C/R/F together: derived actual co-triple slots and minimum covers, all pair cases, exact cycle orientation/count, strict binomial inequality, actual shared witnesses/capacities, conditional next-index and next-incidence existence, common FOUR cover, saturated same-slot floors, repeated eligibility/termination, silent edits, full restoration, event minimum, infinite mixed/saturated controls, all unfinished roots after first cycle, and inherited novelty/method limits.
