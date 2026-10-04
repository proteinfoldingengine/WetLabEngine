# A11.X23 — graded guard access and exact protection on eight labels

Scope:9e1d1e4797e1cf7155b1e1866c0e71039516f7c6.
Parent analytical publication:2811d555e503b80bc40616244326ed7a01566960.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. Native setting and statements

Fix a finite ordered palette P of k labels, r labelled original slots and positive ORIGINAL floors a_i<=k. Let b=max a_i. A primitive adds or removes ONE incidence in ONE original root, retaining its floor. Larger temporary supports, background edits and repeated edits remain native. Endpoints have transversal EXACTLY FOUR.

For h>=1 let L_h={i:a_i<=h}, ell_h=|L_h| and S_h=sum_(i in L_h) a_i. At an exact original-floor compaction E*, define d_h(x)=|{i in L_h:x in E*_i}|. These are incidences in the SAME actual carrier, restricted only for counting; every other root remains present.

**Lemma X23A (graded exact-hub access).** Suppose a specified full exact-four hub Q has n designated support tokens of size h, including its m-token actual three-guard, and EVERY other token has size at least b. Suppose ell_h>=n. If an exact compact input E* has a label x with d_h(x)>=m-1, the original exact input has complete native{3,4} repair to the SAME full labelled Q. Thus two such inputs connect with full original labelled/noncompact destination restoration. The endpoint-independent sufficient condition is ceil(S_h/k)>=m-1.

Only the n designated tokens require capable-slot placement. The remaining tokens fit every original slot. This is a proved compatible full assignment, not arbitrary mixed compact-support permutation. A three-guard has at least three actual roots, so n>=m>=3.

**Theorem X23G (uniform base, arbitrary original padding floors).** Suppose an explicit n-root exact-four family has all supports of size h on existing palette labels, and an actual m-root three-guard. On ANY original positive-floor carrier with r>=n, ell_h>=n and ceil(S_h/k)>=m-1, EVERY exact-four pair has complete repair. Realize the n base tokens at capable slots; fill every other original slot with a support of size max(b,h) containing one base support. Original floors outside L_h are arbitrary, not required uniform, small or cover-automatic.

**Lemma X23F (fourteen-token exact-four module).** For any t>=1, on eight existing disjoint t-label blocks there is an explicit exact-four family of FOURTEEN supports of size4t with an actual SEVEN-root three-guard. Therefore if

r>=14, k>=8t, b<=4t, and ceil((sum a_i)/k)>=6,

EVERY exact-four pair on the original mixed carrier has complete native{3,4} repair, with full original restoration. Duplicate a hub root to pad; every full token fits every original floor.

**Theorem X23M (broad mixed-three/four consequences).** For original a_i in{3,4}, complete repair holds in EACH of these additional domains:
- k>=8 and r>=14, regardless of the number ell of original floor-three slots;
- k10 and ell>=6;
- k8 and ell>=9, or k9 and ell>=10;
- k7, r>=13 and ell>=10;
- k7 and r>=35, regardless of ell.

Uniform profiles and overlapping previously accepted classes are inherited; genuine mixed conclusions are new applications of proved access. X22 already supplies every k>=11 and every r6. No claim is made that every listed profile is feasible.

The main discovery is protection availability counted in the slots that can ACTUALLY receive it. No new labels, slots, weakened floors or temporary constraints are introduced. The one-unit excursion is an upper bound, not a positive minimum for every pair. General remaining mixed, directed, higher-target and unrestricted nested closure, and numbered v16.55 certification, remain open.

## 2. Exact source compaction and restricted incidence count

At any exact-four E choose a minimum four-cover H_E. Retain a_i labels in each root including a label of H_E that hits it; delete excess incidences individually. Original floor legality and H_E are retained, and deletion cannot lower transversal, so every primitive remains EXACT FOUR.

Whenever excess remains an excess incidence supplies the next deletion. Finite total excess decreases. Save the full reverse to restore every original incidence and labelled/noncompact support.

In the compact tuple the capable-slot incidence sum is exactly S_h. Sum_x d_h(x)=S_h, so some ACTUAL label has d_h(x)>=ceil(S_h/k). This is not the whole-carrier maximum degree; incidences outside L_h are neither discarded nor counted as available small-token placement room.

For a chosen x, let I be ALL existing roots avoiding x. Exact four forces this actual family to be a three-guard: a cover of at most two labels for I, together with x, would give a full cover of at most three. For every palette pair, some actual I root misses it.

Every capable slot containing x lies outside I. Therefore d_h(x)>=m-1 identifies at least m-1 DISTINCT ORIGINAL capable slots outside the actual source guard. This links incidence to legal support assignment, not just a scalar cover count.

## 3. Compatible FULL token placement, safety and complete return

Place m-1 designated hub guard tokens in those outside capable slots. Put the last guard token in any distinct remaining capable slot, outside I if available; otherwise inside I. Such a slot exists because ell_h>=n>=m. The placed actual destination guard J has |I intersect J|<=1.

Put the other n-m designated size-h tokens into distinct remaining capable slots. There are enough because ell_h>=n. Assign EVERY remaining token to a remaining original slot; its size>=b makes that final assignment legal. This injection extends to a bijection of ALL full hub tokens, with identical supports treated as distinct tokens if needed.

Thus the full permuted tuple Q' is legal at the ORIGINAL mixed floor vector and exact four. Baseline OVERLAPPING_CLIQUE_EXCHANGE M implements Q->Q' by native exact endpoint swaps. Process decreasing original floor order; an unfinished slot's desired token lies in an unfixed slot. The final assignment supplies its fit, and the displaced support fits the other slot by that floor order. Expand the two supports to their union, then contract to the new legal supports. The union can lower hitting number by at most one from exact four; each half contains its corresponding exact endpoint. Every primitive lies in{3,4}, floors hold, and every completed swap fixes a new slot without moving fixed slots. Save the full finite reverse Q'->Q.

Actual O1 supplies the LOWER construction E*->Q':
1. Hold I fixed while repairing J-minus-I slots to their full Q' supports, adding missing destination incidences before deleting old-only incidences.
2. At the possible shared slot s, expand E*_s to E*_s union Q'_s, then contract to Q'_s.
3. Hold the fully installed J guard fixed while repairing every remaining root to Q'.

During preparation every forbidden pair misses an unchanged source guard root. During shared handover the comparison family consists of source-exclusive supports, destination-exclusive supports and the shared union. If a palette pair hits every exclusive support, both actual guard inequalities force it to miss both shared endpoint supports, and hence their union. Otherwise an exclusive support is its actual witness. Current guarded roots are subsets of the comparison supports throughout this stage, so the missed witness persists. The completed destination guard protects final repair.

This accounts for EVERY palette pair, including pairs involving labels outside a base module or used only in high-floor roots. Smaller sets follow by padding, possible since exact four implies k>=4. No independent reserve capacity is invented for distinct pair obligations.

Each addition retains a legal current support; each deletion retains the complete destination support at that ORIGINAL floor. Every unfinished scheduled root supplies a missing or excess incidence for its next legal primitive. Scheduled symmetric difference decreases by one and finite phase/slot order terminates at the exact full Q'. The installed destination guard is reusable before remaining source guard roots are changed; exact-four resetting after every handover is unnecessary.

The middle construction is a finite lower path with tau>=3, which may exceed four. Apply baseline A ONLY between its actual exact-four endpoints E*,Q', on the original positive-floor union-closed carrier. Its converted finite path has tau in{3,4}. No schedule, path-length or efficiency property is inferred from conversion.

Prefix source exact compaction and append the saved reverse FULL exact hub permutation. This reaches the SAME original full labelled Q. Construct a second complete leg C->Q and reverse it; the join is the identical exact full Q, and reversed saved destination compaction restores EVERY original labelled/noncompact support of C. The same construction can be repeated between any finite chain of qualified exact endpoints. This proves X23A.

## 4. Exact padding with arbitrary original floors

For X23G choose n distinct original capable slots and place the specified size-h base family there. Since those original floors are<=h, these full support tokens are legal. Let B=max(b,h)<=k; the explicit base requires k>=h.

In each remaining EXISTING slot choose a B-support containing a selected base root, adding labels only from P until its size is B. This is a completed mathematical hub specification, not a simultaneous edit from an arbitrary input endpoint.

The base subfamily supplies the lower exact-four obligation. Any base minimum four-cover hits the selected base support and therefore EVERY containing padding root. Thus the full tuple is EXACT FOUR with a supplied minimum cover. Padding is allowed even when original high floors are not cover-automatic. Its actual guard is unchanged. Designate the n base tokens; all other tokens have size B>=b and fit every original slot.

The restricted source incidence condition supplies X23A. This proves complete native repair at the ORIGINAL mixed floor vector. We do not substitute n*h or b*r for S_h, do not discard the high roots, and do not weaken their floors. The full larger padding supports and original destinations are restored by the saved complete constructions.

## 5. Explicit fourteen-support module on eight labels

On U={1,...,7} use the already disclosed triple pattern

L1=123,L2=145,L3=167,L4=246,L5=257,L6=347,L7=356.

Their complements within U are

R1=4567,R2=2367,R3=2345,R4=1357,R5=1346,R6=1256,R7=1247.

Add an EXISTING eighth label8 and define T_j=L_j union{8}. The FOURTEEN actual hub roots are all R_j and all T_j, each of size FOUR.

The seven triple table from X11/X20 supplies each label's three pairs:
1:(23,45,67);2:(13,46,57);3:(12,47,56);4:(15,26,37);5:(14,27,36);6:(17,24,35);7:(16,25,34).
Thus each point occurs in THREE triples and every pair occurs in exactly ONE.

Two distinct L triples intersect in at most one label by pair uniqueness, and cannot be disjoint. If L_j,L_l were disjoint, a point a in L_j would need THREE other distinct triples to pair it with the three points of L_l. Those triples are distinct because a triple containing two L_l points would reuse that pair. Together with L_j this would give degree at least four for a, contrary to the displayed degree three. Hence every two distinct L triples intersect EXACTLY ONE.

Consequently every two distinct R complements intersect in exactly TWO labels, so a three-set cannot be contained in two different R_j. No displayed L triple is contained in any R_j, because that would make it disjoint from L_j. Each R_j has exactly FOUR three-subsets. Their seven families therefore account for28 distinct non-L triples. There are C(7,3)=35 triples on U and7 displayed L triples, so EVERY other triple is contained in exactly one R_j. This is an elementary specified-support count, not scientific enumeration or an external design theorem.

Now EVERY three-label set K in the eight-label palette misses an ACTUAL hub root:
- If8 belongs to K, its other two labels lie in some L_j by pair coverage; R_j misses all of K.
- If K=L_j within U, it misses R_j.
- If K is any other triple within U, it lies in R_j for some j and therefore misses its complementary root T_j.

Thus no three-cover exists and the full transversal is at least FOUR. The supplied H={1,2,4,8} hits every T_j via8. It hits every R_j because124 is not an L triple; missing R_j would mean124 subset L_j, hence equal to one of the displayed triples. Therefore H is a minimum FOUR-cover.

The ACTUAL seven-root family of all R_j is an exact-three guard, as already explicitly proved in X20: every pair belongs to an L triple and so misses its complement R_j, while124 hits all R_j. Its three-cover supplies the matching upper bound. The full hub has a seven-slot actual three-guard.

There is no asserted optimal root/guard count. This familiar explicit incidence pattern is not an originality claim or inserted geometry.

## 6. Existing label blocks and full mixed-floor access

Choose eight disjoint EXISTING t-label blocks B1..B8. Replace each index in the fourteen supports of Section5 by its whole block. All actual supports have size4t.

A cover of this fixed block module projects to the block indices it meets; selecting one existing representative for each covering index gives the converse cover. Hence the full actual module is EXACT FOUR, and the selected seven R roots form an ACTUAL three-guard. Representatives in B1,B2,B4,B8 supply a minimum four-cover.

This projection proves the hitting numbers of THIS fixed module. It is not a general cloning/path equivalence, and no simultaneous block edit is treated as a primitive. Later native edits are individual incidences and need not preserve block structure.

If r>=14 and b<=4t, all fourteen tokens fit every original slot. Pad with duplicates of a module root; exactness and the actual seven-slot guard persist. Extra palette labels do not help cover the module or remove its witnesses.

At exact source compaction let S=sum a_i. If ceil(S/k)>=6, some actual label has total degree>=6. Its actual avoiding family has a three-guard on r-d slots, leaving SIX outside slots for the seven-token destination guard. Since every full hub token fits every original floor, place six guard tokens outside and at most one inside, extending to a legal FULL permutation.

This is X21A with m7, or the full-compatible special case of Section3. M/O1/A give actual all-pair protection, eligible finite progress, renewed installation and SAME full module return. Both endpoint legs restore every original support. We never compact the size4t hub to unequal original floors before permutation. This proves X23F.

## 7. Graded triple reserves and arbitrary other original floors

Let ell be the number of ORIGINAL floor-three slots. Assume all other floors are at least three; floors1/2 already have universal X3/X4 repair and need no new claim here. Restricted incidence is S_3=3ell.

### Six-token wide triple module

The accepted X12 wide base at h3 has four triples on a four-label core and two disjoint private triples, using TEN labels and SIX tokens. It has exact transversal2+1+1=4, with one actual core triple plus the two private triples forming a THREE-slot guard.

X23G therefore proves complete repair for ANY original high-floor profile when

k>=10, ell>=6, and ceil(3ell/k)>=2, equivalently3ell>k.

All remaining original floors may be ANY values between4 and k. The padding supports of size b contain a core triple and fit every original slot. No whole-carrier incidence-budget or automatic-root hypothesis is required.

In particular k10,ell>=6 always satisfies the condition. This is a genuine mixed extension, not input module connectivity only.

### Eight-token two-core triple module

The accepted X12 two-core base at h3 uses ALL triples of two disjoint four-label cores: EIGHT tokens on EIGHT labels. Its exact transversal is2+2=4 and its actual five-slot three-guard is all four roots of the first core plus one root of the second.

X23G proves complete repair for arbitrary other original floors if

k>=8, ell>=8, and ceil(3ell/k)>=4, equivalentlyell>k.

At k8 it suffices that ell>=9; at k9 it suffices that ell>=10. These are structural restricted-incidence consequences; no finite passing count or enumeration is used.

Other grades h can use X23G when an explicit exact base/actual guard is supplied. Availability of such a base and its native palette room are required; not every floor vector is thereby covered.

## 8. Seven-label grouped hub with larger allowed pools

At k7 consider the accepted X11 six-triple guard

145,167,246,257,347,356.

Every pair hits at most five of the original seven L supports; deleting only123 leaves at least one of these six actually missed. Thus this selected family is a three-guard. Its COMPLETE minimum three-covers, proved in the frozen X11 source, are the seven L triples plus456,457,467,567.

Keep the SAME accepted cover groups but retain the FULL allowed pools rather than compacting all reserves to triples:

| Reserve support | Assigned three-covers |
| --- | --- |
| 4567 | 123 |
| 236 | 145,457 |
| 234 | 167,567 |
| 135 | 246,467 |
| 1346 | 257 |
| 1256 | 347 |
| 127 | 356,456 |

Each reserve misses every cover in its assigned group. All eleven minimum guard covers occur in these groups. The supplied H={1,2,3,4} hits every guard and reserve. Hence the thirteen-token completed hub is EXACT FOUR.

It has TEN designated triple tokens: six guard triples and four triple reserves. The other THREE reserves have size4. On a mixed-three/four carrier with ell>=10 and r>=13, assign the ten triple tokens to original floor-three slots and the three four-tokens to remaining slots. Further existing slots receive size4 supports containing a guard triple; these fit all original floors and retain exactness.

The guard has m6 designated triple tokens. Restricted source incidence gives

ceil(3ell/7)>=ceil(30/7)=5=m-1.

X23A therefore supplies complete native repair from EVERY exact input. This proves the k7,r>=13,ell>=10 branch of X23M.

This does not rewrite or recertify X11. Its actual complete-cover classification and allowed-pool partition are inherited. The new choice retains three legal FOUR-support pools, reducing the number of tokens needing floor-three slots from thirteen to TEN. It is meaningful only when paired with restricted-incidence accessibility; existence of the modified hub alone does not imply access.

No arbitrary original floors>4 are inferred in this seven-label mixed branch: the three four-tokens must actually fit their destinations. At k7 floors>=5 are cover-automatic and may be handled by the independently accepted positive lift when its retained theorem applies.

## 9. Full-compatible smaller-palette consequences

For original floors3/4 write S=3ell+4(r-ell)>=3r.

At k8,r>=14, Section6 with t1 has all tokens size4, b<=4, palette8 and an actual seven-slot three-guard. Since ceil(S/8)>=ceil(42/8)=6, X23F supplies EVERY exact pair.

At k9,r>=14, accepted X19's explicit fourteen-root floor-four shared-core hub on nine labels has an actual SIX-slot three-guard and all supports size4. They fit every original floor3/4. Source incidence supplies ceil(S/9)>=ceil(42/9)=5=m-1. Accepted X21A supplies complete mixed access, not X19's uniform input theorem. The explicit core/blocker support facts and supplied minimum four-cover are inherited.

At k10,r>=14, accepted X12's two disjoint complete four-uniform five-label cores give a TEN-token exact-four hub with an actual SIX-slot three-guard. Pad to r by duplicates. Every token is size4 and fits every original floor. Source incidence gives ceil(S/10)>=ceil(42/10)=5=m-1. Again X21A supplies complete mixed access in its actual full-compatible domain.

At k>=11, accepted X22 already supplies every root count, so no new coverage is claimed there. Together these branches prove EVERY mixed-three/four carrier at k>=8,r>=14 has complete repair.

For k7,r>=35, select seven palette labels and put ALL thirty-five four-subsets in existing slots, padding duplicates. Every three-label set has its ACTUAL complementary four-support present, so transversal is at least four. Any four-label set hits every root since two disjoint four-sets cannot fit in seven labels, giving exact FOUR and a supplied minimum four-cover.

All fifteen four-subsets of a selected six-label subset form an ACTUAL three-guard. Every pair leaves at least four of those six labels and hence misses an actual present four-root; every three labels of that subset hit all its four-roots. Outside seventh labels cannot help. The guard has m15.

All full tokens size4 fit every original floor. Source incidence yields ceil(S/7)>=ceil(105/7)=15>=m-1=14, supplying full compatible X21A access. This proves the k7,r>=35 branch without implying existence at smaller r or a sharp threshold.

All conclusions in Sections7-9 reach every original labelled/noncompact destination; neither a safe finite sequence supplied without availability nor a convenient canonical form is substituted for access. This completes X23M.

## 10. A mixed class beyond the whole-carrier capacity budget

On k10,r7, take six ORIGINAL floor-three slots and one ORIGINAL floor-five slot, with compact supports

123,124,134,234,567,{8,9,10},12358.

The first six supports form the wide triple base, of exact hitting number four. The size5 support CONTAINS the base support123 and creates no new obligation. H={1,2,5,8} hits everything, so full hitting number is EXACT FOUR.

Every root is already at its original floor, so floor compaction is unique. S=23 and maximum degree is4. Any X15N application must use M>=4 and satisfy r7>=D+M+1, hence D<=2. But S23>2k20 violates S<=Dk. No whole-carrier X15N parameter choice applies. X14's r>=2D+2 likewise fails for every cap D>=4.

The profile is genuinely mixed, contains no floor1/2, and the floor-five root is below the k-2=8 automatic threshold. Uniform X15/X20 and cover-automatic X17 do not by themselves give universal repair of this profile; X21's all-max-floor hub conditions also fail at k10,b5.

X23G DOES connect EVERY exact pair on this same original profile: ell6, restricted incidence18>k10, a six-token triple base and three-token actual guard. The floor-five root remains in the actual full carrier and is restored exactly; its floor is never weakened.

This demonstrates removal of the whole-carrier incidence-budget and low maximum-floor requirements. It is not asserted that every older conditional O1/union bridge fails on a chosen endpoint pair. The displayed module is inherited; the new theorem guarantees access and completion from arbitrary incidence types at the original unequal floors.

## 11. Consolidation, remaining domain and v16.55

The reusable resource is not simply the number of labels or total residual slots. Protection has to fit the ORIGINAL slots that receive its support tokens. Restricted incidence proves those receiving slots exist outside an ACTUAL avoiding-label guard. Large containing supports handle the other floors without consuming fictitious independent capacities.

The explicit fourteen-support module supplies exact-four protection on eight labels. Its supports fit all floor-three/four slots; restricted access is unnecessary there, because total incidence supplies the required six outside slots. The grouped seven-label construction uses a different balance: retain larger allowed pools where available, and count only the ten small tokens that still need capable slots.

In every construction, exactness, actual guard existence, compatible placement, primitive safety, next edit, renewed progress and full destination restoration are separately supplied. Exact hub joins prevent accumulated deficit across repeated repairs. Lower schedules may exceed four and are explicitly distinguished from converted band paths; no destination-directed or efficiency guarantee follows.

At target four, uniform floor3/4 remains universally closed; mixed3/4 k>=11 and r6 every palette remain X22. Additional X23 classes include k>=8,r>=14 and the restricted-floor-three reserve conditions. On k<=6 arbitrary positive profiles are already X17. Any unresolved mixed3/4 carrier must lie outside ALL these and inherited sufficient classes. These are necessary residual restrictions, not a checklist of numerical campaigns or proof every tuple exists.

Broader mixed-floor/higher-target/directed/nested universality remains OPEN. Root-to-child lifting requires inherited exact-child interfaces/fixed-root clearance. No negative native or nested barrier is inferred from failure of graded counts, one chosen hub, or a placement budget.

Frozen dependencies are read for applicability, not rewritten or recertified: baseline A/M/L/J/F and exact compaction at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f; actual O1, X11 grouped cover classification/pools, X12 exact triple/four-core hubs, X17 positive lift, X19 explicit shared-core hub, X20 complement support facts, X21 full-compatible access, and X22 prior mixed closure at parent2811d555e503b80bc40616244326ed7a01566960. The new module proof requires no external design/classification theorem.

Fresh whole-argument review must check the designated-token count versus original capable slots, restricted ORIGINAL incidence, ALL-root avoiding guard, compatible full M extension, O1 all-pair witnesses, floors/eligible primitives/progress/renewal, upper conversion at exact endpoints, SAME full hub and complete destination restoration, padding containing an actual base support, eight-label EVERY-three-set proof/block property, complete inherited grouped cover/pool hypotheses, mixed-domain arithmetic and honest novelty/control limits.

This is an analytical loop toward v16.55. No numerical enumeration, scientific test/workflow/run ID, implementation, benchmark, numbered CLOSED/CERTIFIED or integration merge. Prospective protocol/independent complete-domain reconstruction/rejecting controls/inherited GitHub execution/reproduced durable publication/exact merge-head review/post-merge audit remain numbered certification gates. Certified v16.54 and separately accepted efficiency baseline/design stay unchanged; runner implementation/execution/measured speedup remain unstarted. Ordered repair/retained recoverability; no fundamental time, inserted geometry, physical metric/energy/gravity or originality claim.
