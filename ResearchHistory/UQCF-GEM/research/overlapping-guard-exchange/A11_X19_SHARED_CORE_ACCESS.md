# A11.X19 — shared-core protection creates accessible exact-four hubs

Scope: 28e6eb836ab052bea9b1bf59b462f4f27dd3e328.
Parent analytical publication: d3da788b0c524c9bb53423bfd358bce56f9f4ac1.
Certified baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen analytical candidate for fresh independent WHOLE-ARGUMENT review.

## 1. Exact new statements

Fix an ORIGINAL uniform floor h>=2, a finite ordered palette P, r labelled original root slots and exact-four endpoints. Roots may have ANY size at least h, and every primitive changes ONE incidence in ONE root. Larger intermediate supports and temporary/repeated edits remain permitted. No label, root slot, weakened floor or geometry is added.

**Lemma X19H (shared-core exact hub).** On 2h+1 existing labels there is an explicit floor-h exact-four tuple with an actual three-guard on h+2 slots, using
- n_h=2h+6 slots when h is even;
- n_h=2h+8 slots when h is odd.

The tuple consists of two complete h-uniform cores sharing ONE existing label and a coupled family of four/even or six/odd actual blocking supports. Every three-cover of the two cores is missed by a supplied blocker. A minimum four-cover is explicitly retained. Additional original slots can be filled with duplicate legal supports without changing exactness.

**Theorem X19A (complete shared-core access).** Every exact-four endpoint pair on a uniform-original-floor-h carrier has finite native repair with tau in {3,4}, restoring the complete original labelled/noncompact destination, if

k=2h+1 and r>=n_h.

There is no shared-core, selected guard or X5-entry assumption on either INPUT endpoint. Exact compact incidence forces actual guard availability and placement at both endpoints. The new shared-core hub makes accepted X12A applicable where the disjoint two-core hub cannot fit.

More generally the constructor fits k>=2h+1 with r>=n_h and access follows whenever ceil(hr/k)>=h+1; at k>=2h+2 this general domain is already covered by the smaller accepted X12D hub, so it is not counted as new coverage.

**Corollary X19F (complete floor-four/nine-label connectivity).** EVERY exact-four endpoint pair on EVERY feasible nine-label carrier with ORIGINAL uniform floor four has complete native {3,4} repair. Exact endpoints below eleven slots are impossible. Existence at eleven through thirteen slots remains UNDECIDED here; existence at fourteen and above is supplied. Connectivity whenever endpoints exist is distinguished from feasibility.

**Lemma X19B (constructor blocker lower bound).** On the exact 2h+1-label carrier, completing the two declared shared cores to transversal at least four needs at least

ceil(h^2/floor(h^2/4))

additional actual supports of size at least h. This is four for even h and five for odd h>=3. The even construction attains the bound; optimality of the odd six-blocker construction is NOT proved. This is a lower bound for THIS declared preparation, not a native disconnection or higher-barrier theorem.

## 2. The shared cores and the missing exactness

Partition the selected existing 2h+1 labels as {x},U,V with |U|=|V|=h and U,V disjoint. No label is created. Set S={x} union U and T={x} union V.

In h+1 existing slots put ALL h-subsets of S, namely S minus {s} for s in S. In another h+1 slots put ALL h-subsets of T. Each core alone has transversal TWO: one core label s misses its actual root S minus {s}, while two distinct labels meet every root because a root omits only one core label. Labels outside a core cannot help hit its roots.

A set K of at most three labels hitting both cores must have at least two labels in S and at least two in T. Since S intersect T={x}, it must therefore be EXACTLY

K={x,u,v}, with u in U and v in V.

Conversely every such triple hits both cores. Thus the two cores together have transversal exactly THREE. Sharing the label x has saved palette room but lost exact-four protection. A hub cannot be called exact four until ALL h^2 of these actual three-cover obligations are blocked.

The relevant obligations are coupled: one blocker may avoid many (u,v) choices, and the same labelled roots supply the protections. They are not h^2 distinct required root slots or independent capacity systems.

## 3. General partition preparation supplies all blockers and a four-cover

Partition U into nonempty groups U_1,...,U_p and V into nonempty groups V_1,...,V_q, with p,q>=2, such that

|U_i|+|V_j|<=h for EVERY i,j.

Choose two U labels u0,u1 in different U groups and two V labels v0,v1 in different V groups. Put H={u0,u1,v0,v1}. Every root of either complete core meets H, since H contains two distinct labels in that core.

For each pair (i,j) let

L_(i,j)=(U minus U_i) union (V minus V_j).

Its size is 2h-|U_i|-|V_j|>=h. It omits x, every U_i label and every V_j label. It contains at least one of u0,u1 and at least one of v0,v1, because an omitted group cannot contain both selected labels from that side.

Choose an h-subset B_(i,j) of L_(i,j) that meets H: retain the first available selected H label in palette order, then fill to h with labels from L_(i,j). There are enough actual available labels. Place B_(i,j) in ONE original slot allocated for this pair. Every support has exactly its original floor h and uses only existing labels. No simultaneous incidence edit is claimed: this specifies a completed exact endpoint hub.

For EVERY three-cover {x,u,v} of the cores there is a group pair with u in U_i and v in V_j. The actual B_(i,j) misses all three labels. Thus no three-label set hits the completed family. Smaller sets cannot hit it either, since they could be extended to a three-set on this same palette. The chosen H hits every added B_(i,j) and every core root, so the complete hub is EXACT four.

This proves a general partition hub with 2h+2+pq existing slots, supplied minimum four-cover H and ALL forbidden three-cover witnesses. The actual chosen subsets need not be independently optimized for separate pairs; each fixed support serves all of its avoidance obligations simultaneously.

## 4. Even and odd constructions and the actual three-guard

If h is even, divide U into two halves of size h/2 and V into two halves of size h/2. Each group-size sum is h, so L_(i,j) has exactly h labels and is itself the required support. There are four blockers, giving n_h=2h+6.

If h is odd, write h=2t+1 with t>=1. Partition U into groups of size t and t+1. Partition V into three nonempty groups of size at most t. Such a partition exists because 3t>=2t+1 and 2t+1>=3: begin with one label in each group and distribute the remaining labels without exceeding t; total remaining capacity is 3t-3, at least 2t-2. Resolve all choices in palette order. Every group-size sum is at most (t+1)+t=h. Six blockers suffice, giving n_h=2h+8.

For BOTH constructions choose the following actual guard: ALL h+1 roots of the first core, together with the root V=T minus {x} already present in the second core. The complete first core uses S={x} union U and requires two labels; V uses a disjoint palette and requires one further label. Thus this guard has transversal exactly THREE on h+2 slots. No added blocker or spare root is needed for this guard.

For an explicit missed-root witness for EVERY pair K:
- If K contains at most one label of S, some actual first-core root misses K (if its only S label is s, use S minus {s}; with none, any first-core root misses it).
- If K contains two labels of S, K lies in S and misses the actual root V.
Singletons and the empty set have a missed guard root too. This accounts for all palette pairs, including labels outside the selected hub palette when embedded in a larger P.

If r>n_h, fill the remaining ORIGINAL slots with copies of a specified first-core support. H still hits all roots; the original exact-four subfamily and guard remain. Duplicate tokens are kept as separate labelled slots. No extra slot is introduced during a repair.

## 5. Exact compact source protection and safe hub access

Here we supply the hypotheses of accepted X12A, rather than assuming that a convenient exact hub is accessible.

At an arbitrary exact-four INPUT E, choose a minimum four-label cover H_E. In each original root retain an h-subset containing one actual label of H_E and delete excess incidences one at a time. Every deletion respects h, cannot lower tau and retains the four-cover; EVERY intermediate is EXACT four. Whenever excess remains an eligible deletion exists, and total excess decreases. Save the reverse to restore the original noncompact support.

The exact compact endpoint E* has hr actual incidences. Its maximum label degree d obeys d>=ceil(hr/k). The actual family I of ALL roots missing such a label z requires at least three hitting labels: a two-cover of that family together with z would cover E* with three labels, contradicting exact four. It has exactly r-d actual labelled slots and witnesses every forbidden pair.

The hub Q from Sections3/4 is EXACT four on the SAME full carrier and has an actual guard of m=h+2 slots. Access requires d>=m-1=h+1. At k=2h+1 and r>=n_h>=2h+2,

hr/k >= h*(2h+2)/(2h+1)
      = h + h/(2h+1) > h,

so ceil(hr/k)>=h+1. Therefore EVERY exact INPUT supplies the needed access budget. Padding the hub with original duplicate slots retains exactness. No input is assumed to have the hub shape, the same anchor slot, or X5's avoiding-triple family.

For completeness, the inherited construction aligns actual guards as follows. At least d>=m-1 existing slots lie outside I. Assign m-1 hub-guard support tokens to those slots and, if needed, the remaining guard token to one slot of I. Extend this to a permutation of the FULL exact-four hub's r labelled tokens. Uniform ORIGINAL floor h makes every swapped support compatible. Accepted endpoint-permutation Lemma M implements this full exact endpoint operation through safe primitive swaps; it is not a simultaneous move or a permutation of a bare level-three guard. Save the reverse.

Let Q** be that exact permuted hub and J its assigned guard. Then |I intersect J|<=1. The actual old and new guards therefore satisfy accepted O1. No arbitrary mixed-floor permutation is inferred.

## 6. Every primitive, all lower witnesses, renewed progress and full restoration

The preliminary source-to-Q** lower schedule is the accepted actual one-overlap handover:
1. Hold I unchanged while repairing every destination-exclusive J root through individual additions of missing destination labels, then deletions of old-only labels.
2. At the possible shared slot s, expand its support to the actual union of source and destination supports, then contract to its destination.
3. Hold the fully installed destination guard J while repairing every remaining root to Q** through its own union.

At the shared stage define the comparison family D on I union J: source supports at I-exclusive slots, destination supports at J-exclusive slots, union at s. If a palette pair K hits every exclusive support, the old guard forces K to miss its source root at s and the new guard forces it to miss its destination root there. It misses their union too. Thus D supplies an ACTUAL missed root for EVERY pair. When there is no shared slot the unchanged old guard suffices. Current roots in this stage are subsets of their D supports, so each missed-root witness persists. Preparation and final restoration use the unchanged actual old and installed new guards respectively.

Every addition is eligible and retains the old floor-safe support. Deletions begin only after the complete floor-safe destination support is present. Every unfinished root has a missing destination incidence to add or an old-only incidence to remove. The finite phase/slot order and decreasing sum of symmetric differences give a finite schedule reaching exactly Q**. Shared capacities are not cloned, and only one incidence changes per primitive.

The new guard is installed BEFORE the remaining old-guard roots are edited. It renews protection for all subsequent edits even if the full tuple is at level three. This is the inherited reusable handover with NEW actual access supplied by the shared-core exact hub, not a claim of universal arbitrary multiple-overlap transfer.

The preliminary schedule has tau>=3; its upper bound is finite since any k-h+1 labels hit every floor-h support. Apply baseline maximum-layer Theorem A to this ACTUAL finite lower path between exact E* and Q**. Its nonempty-root, original-floor, native-union and fixed-carrier hypotheses hold. It gives a finite path with tau in {3,4}, possibly changing the schedule and using temporary/repeated incidences.

Concatenate the original source exact compaction, converted middle path and reversed full hub permutation. This reaches the SAME specified ORIGINAL labelled exact-four hub Q, including all pad tokens. Its supports already have floor size, so no additional hub compaction is needed.

For arbitrary original exact endpoints A,C, obtain the two COMPLETE paths A->Q and C->Q. Reverse the latter and join at this same actual full exact hub. Reversal preserves native floors and the band and returns every original labelled/noncompact support of C through its saved compaction reverse. Thus A->Q->C reaches the precise original destination. Any finite chain of exact endpoints in this class can reuse Q in the same way; each complete leg restores an exact full tuple and deficits do not accumulate.

Full endpoint permutation has its own eligible next swap whenever a token is misplaced and fixes at least one more destination slot. Exact compaction has eligible deletions and finite excess decrease. The middle has eligible primitive edits and finite symmetric-difference decrease. Maximum-layer conversion has the accepted finite layer-removal construction. Together these supply existence AND termination of the complete repair, not merely a safe supplied prefix or a canonical-form aspiration.

The final band path is distinguished from the lower schedule. No length/efficiency guarantee or original destination-directed universality is inferred. These arguments prove X19A.

## 7. A rigorous bound on this constructor's added supports

On P={x} union U union V of EXACTLY 2h+1 labels, the two cores have h^2 distinct three-covers {x,u,v}. An additional support containing x misses NONE of them and supplies no blocking contribution.

An additional support B avoiding x lies in U union V. Let b=|B intersect U| and c=|B intersect V|. Its original floor gives b+c>=h. It misses precisely (h-b)*(h-c) of those three-covers. Put a=h-b and d=h-c; these are nonnegative integers with a+d<=h. Therefore

a*d<=floor(h^2/4).

This bound concerns the same actual support across all its pair obligations. A family of n added roots can consequently block at most n*floor(h^2/4) distinct triples (overlap can only reduce that union). Exact-four completion requires all h^2 triples blocked. Thus

n>=ceil(h^2/floor(h^2/4)).

For even h this is four, attained by the four rectangular blockers. For odd h>=3, floor(h^2/4)=(h^2-1)/4 and 4<h^2/floor(h^2/4)<=5, so at least five are needed. The constructed six are sufficient; no five-root impossibility or optimality claim is made.

If the ambient palette has other labels and added roots may use them, the b+c>=h inference can fail. The bound is confined to this declared exact palette/support constructor. It is NOT a barrier to another native preparation, a minimum universal root count, or evidence of disconnected exact endpoints.

## 8. Complete original-floor-four/nine-label consequence

Let h=4,k=9. The new hub needs fourteen existing slots. Explicitly set x=9,U={1,2,3,4},V={5,6,7,8}, with halves {1,2}/{3,4} and {5,6}/{7,8}.

Use all five four-subsets of {1,2,3,4,9}, all five four-subsets of {5,6,7,8,9}, and these four blocking supports:

{3,4,7,8}, {3,4,5,6}, {1,2,7,8}, {1,2,5,6}.

Every core three-cover {9,u,v} is missed by the blocker excluding its U and V halves. The supplied minimum four-cover {1,3,5,7} hits every root. The guard is the first core's five roots plus {5,6,7,8}, on six slots. Exact-four feasibility at fourteen is therefore proved directly. Duplicate padding gives feasibility at every r>=14.

By X19A EVERY exact endpoint pair at r>=14 is connected; all original destination incidences are restored. Before this checkpoint, this nine-label/floor-four all-count conclusion was not established. The next small-r branches are inherited, not newly claimed mechanisms:

- r<11: accepted X16C requires r>=L(9,5,3)=11 for exact four, so those carriers are infeasible.
- r=11: accepted X16 gives avoiding-root requirement g=6 and strict-slack complete repair. Equivalently the actual incidence/O1 budget below also works.
- r=12,13: accepted X7G supplies actual three-guards at each exact compact endpoint of size at most N=floor(5r/9), namely6 and7. The actual one-overlap composition applies since r>=2N-1:12>=11 and13>=13. Uniform full exact endpoint permutation, actual O1, upper conversion and reversed exact compaction restore the complete destination.

The branches exhaust all r. They prove X19F: EVERY feasible uniform-original-floor-four/nine-label carrier has complete target-four native repair. Existence at r11,r12,r13 is left undecided. A necessary covering lower bound is not an attainment certificate, and conditional connectivity is not infeasibility.

This is a consequence of ONE general shared-core protection/access mechanism and accepted small-domain composition, not a numerical root-count campaign.

## 9. Scientific gain and correct comparison with previous coverage

Accepted X12D obtains an exact-four hub from disjoint (h+1)-label cores and therefore needs at least2h+2 labels. Here only2h+1 labels are available. Simply overlapping those cores would leave exact level three; the added partition supports supply ALL missing three-cover witnesses while retaining an explicit four-cover. This removes the disjoint-core palette requirement for the declared access theorem. Hub existence AND access from arbitrary exact endpoints are proved separately.

The guard does not depend on the added blockers: it is an actual complete first core plus the other core's private root. Its h+2-slot protection is compatible with actual source incidence. The blockers restore exact entry; the guard plus slot budget supplies safe handover. These are different mathematical roles, not independent resource pools.

For h>=4 even the new narrow-palette threshold is2h+6; for odd h>=5 it is2h+8. The earlier palette-independent X9 threshold is(h+2)*(h+1)-3 and does not supply these smaller thresholds. X7/O1 incidence may already cover some particular counts below or above the new hub threshold; those are not labelled new. The significance is universal arbitrary endpoint access throughout the declared new narrow-palette domain.

At h2, accepted X4 already gives universal target-four repair; at h3, accepted X15 already closes all feasible carriers and X11 supplies a thirteen-slot/seven-label hub smaller than this odd construction. These instances are inherited controls, not new coverage. At k>=2h+2 with the same degree requirement, accepted X12D has a smaller slot cost; only the shared-core narrow-palette gain is claimed. X16 already closes the floor-four/ten-label feasible class and the conditional eleven-root/nine-label branch. X19 adds the COMPLETE nine-label class.

This is mathematical protection derived from existing support relationships. It introduces no physical geometry or fundamental time. The partition into label groups is a combinatorial proof choice, not a newly imposed native geometry or admissibility constraint.

## 10. Remaining obligations, inherited domains and publication limits

Uniform-original-floor-four on all other palettes is NOT universally closed by this packet. Unrestricted mixed-floor, higher-target and nested universality remain open outside accepted classes. Original A11 destination-directed scheduling remains open: endpoint permutations, temporary incidence edits and upper conversion can alter original schedules.

X18's shared-incidence renewal lemma remains accepted with its explicit certificate-derivation obligation. This packet follows the alternative authorized route of creating an exact accessible protection hub; it does not claim universal availability of X18 or X5's hypotheses. X5's same-slot requirement is not invoked or weakened. No arbitrary mixed-floor slot permutation follows from the uniform proof.

Dependencies checked for domain applicability: X12A's exact-input/hub guard access and restoration; X7G's actual incidence guard; actual GUARD_HANDOVER O1; baseline OVERLAPPING_CLIQUE_EXCHANGE M, GENERAL_PARENT_CONNECTIVITY exact compaction/maximum-layer A and conditional child interfaces; X16C and its declared nine-label branch. Frozen source, X15 consolidation, earlier failed constructions and certified baseline remain unchanged. No new external design/classification theorem is needed.

Root paths lift only when the inherited exact-child/fixed-root-clearance interfaces are actually supplied; no unconditional nested closure or negative nested necessity follows. Unit repair is an upper bound, not a positive minimum defect for every endpoint pair.

No numerical enumeration, scientific tests/workflows/run IDs, implementation, benchmark, numbered v16.55 certification or certified integration merge. Separate accepted efficiency baseline/A2 proposal/tiny validation DESIGN stays complete at ea49d2556e4ca4929c0aece68d01e8193ab94b66; runner implementation/fixture execution/benchmarks and measured speedup remain unstarted. Analytical freezing is not numerical preregistration.
