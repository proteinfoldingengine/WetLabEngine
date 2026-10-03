# A11.X20 — small-guard three-cover modules and universal floor-four target-four repair

Scope: bd6acc85eda58f04d7782f70c5296d16a1d450a6.
Parent analytical publication: 4b1232a5465d82d9847f3eddabc669fcafd37e5a.
Certified baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen universal analytical candidate for fresh independent WHOLE-ARGUMENT review.

## 1. Exact statements and native rules

Fix a finite ordered palette P of k labels, r labelled original root slots and an ORIGINAL uniform positive floor h. A support is any subset of P of size at least h. Each primitive adds or deletes ONE incidence in ONE existing root, preserving its original floor. Temporary larger supports, repeated edits and background edits remain allowed. Exact endpoint target is FOUR.

**Theorem X20U (universal original-floor-four root repair).** For h=4, EVERY exact-four endpoint pair on EVERY feasible finite carrier has a finite native path with tau in {3,4}, restoring EVERY original labelled/noncompact destination support. No carrier obligation remains for this declared uniform-floor-four,target-four ROOT problem.

This is connectivity whenever exact endpoints exist, not a feasibility classification for every carrier. It is a defect upper bound of one; it does not assert that every pair requires a positive defect.

The new construction is a small-guard exact-three module plus a private root. Its complete eight-slot exact-four hub has a FOUR-slot actual three-guard. This improves the available protection/placement ratio for eleven/twelve-label floor-four carriers and completes the universal composition with accepted results.

**Lemma X20H (general eight-slot module hub and access).** Let h>=2 and t=ceil(h/4). If r>=8, k>=7t+h and ceil(hr/k)>=3, EVERY exact-four endpoint pair on the original uniform-floor-h carrier has complete native{3,4} repair through an explicit SAME labelled exact-four hub, restoring the original full destination. Seven disjoint existing t-label blocks carry the displayed module, and one disjoint h-label support carries its private obligation. The actual three-guard occupies four slots. The larger hub supports of size4t>=h are compacted exactly before compatible full endpoint permutation, with their saved reverses restored.

At h4,t1, this gives arbitrary endpoint access for k=11 or12 and r>=8.

**Lemma X20S (six-slot uniform repair).** For EVERY uniform original floor h>=1, EVERY six-slot exact-four endpoint pair has complete native{3,4} repair. A carrier with k<3h cannot admit such endpoints. At k>=3h the proof supplies the hypotheses of accepted X15N. No complete feasibility classification at k=3h is claimed.

**Corollary X20L (cover-automatic mixed extension).** Every exact-four endpoint pair has complete repair when each ORIGINAL floor is FOUR or at least k-2. For k>=7 the retained nonautomatic slots have original uniform floor4 and Theorem X20U applies after X17's exact retained-endpoint proof. For k<=6 all such floors are cover-automatic and exact-four endpoints are impossible. Arbitrarily many high-floor slots are allowed; no whole-carrier floor-sum budget is needed.

This does NOT establish arbitrary mixtures of original floors3 and4, unrestricted higher floors/targets, original destination-directed universality or unrestricted nested repair.

## 2. The explicit module: exact three from actual pair avoidance

On seven abstract label indices 1..7 display these seven triples:

L1=123, L2=145, L3=167, L4=246, L5=257, L6=347, L7=356.

The actual four-supports on U={1,...,7} are their complements:

R1=4567, R2=2367, R3=2345, R4=1357, R5=1346, R6=1256, R7=1247.

No external design or classification theorem is assumed. Pair coverage by the triples follows directly from this table, listing the other-label pairs on triples containing each index:

| Index | Other-label pairs |
| --- | --- |
| 1 | 23,45,67 |
| 2 | 13,46,57 |
| 3 | 12,47,56 |
| 4 | 15,26,37 |
| 5 | 14,27,36 |
| 6 | 17,24,35 |
| 7 | 16,25,34 |

Each row partitions the six other indices. Every pair of indices therefore belongs to one displayed triple. For EVERY two-label set K in U, choose that actual triple L_j containing it; the actual root R_j=U minus L_j misses K. Smaller sets can be padded to two labels. Thus the module has transversal at least THREE.

The actual three-label set {1,2,4} hits every R_j: if it missed one, it would be contained in the three-label L_j, hence equal L_j, but124 is not among the displayed triples. Therefore the complete module has transversal EXACTLY THREE.

The first three actual roots R1,R2,R3 have empty common intersection: R1 intersect R2={6,7}, disjoint from R3. No single label hits all three. The actual pair {2,6} hits all three, so this subfamily has transversal EXACTLY TWO. This smaller protecting part is the useful feature. The full exact-three module has seven roots, but its contribution to the hub's three-guard needs only THREE of them.

These are properties of the displayed finite supports, proved by explicit incidences. Familiarity of the triple pattern is not a new geometrical axiom, an originality claim or an external certified dependency.

## 3. Native label blocks, legal floors and an exact-four hub

For general h>=2, put t=ceil(h/4). Choose seven mutually disjoint EXISTING t-label blocks B1,...,B7 and an EXISTING disjoint h-label set V. This needs exactly7t+h labels, supplied by the hypothesis. Extra labels of P may remain unused.

For j=1,...,7 define the actual support

A_j=union of B_l over indices l in R_j.

Each support has size4t>=h and is legal at its ORIGINAL floor h. Put V in the eighth original slot. All later existing slots, if any, duplicate a selected module support. No root or label is added along a path; this is a specified completed hub Q on the original carrier.

A hitting set for these seven module supports projects to the set of block indices it meets. Conversely a set of block indices hitting all R_j supplies a hitting set of the actual supports by selecting one existing representative label from each chosen block. Thus the module hitting number is exactly THREE. This proves a property of THIS fixed explicit hub, not a general claim that cloning preserves paths or protection.

Representatives b1 in B1,b2 in B2,b4 in B4 form a supplied minimum module three-cover. Since V is disjoint from every module root, a representative v in V adds one necessary obligation. The full hub has transversal EXACTLY FOUR with supplied minimum cover H_Q={b1,b2,b4,v}. Duplicate padding adds no new obligation.

The first three module roots still have empty common intersection and are covered by a representative from B2 and one from B6. Together with the private root V they form an ACTUAL three-guard on exactly FOUR existing slots: two labels are necessary for that submodule and another for V. No independent copies of protection or capacities are assigned.

For every palette pair K an actual missed guard root exists:
- If K uses fewer than two labels in the module palette, its at-most-one module label cannot hit all first three roots; some actual one misses K, including any other label outside that palette.
- If K uses two module labels, K misses the actual disjoint private root V.
Smaller sets likewise have a missed root. This accounts for labels in unused blocks, the private root and outside the selected hub palette.

The supports4t may exceed their original floor h. Choose in each hub root an h-subset retaining a label of H_Q and compact through single deletions. A subset of this size exists because the root meets H_Q and has size>=h. Every primitive retains h and the four-cover; deletion cannot lower tau, so it remains EXACT four. Shrinking guard roots cannot weaken their lower transversal, so the chosen FOUR-slot guard persists with tau>=3. Save the reverse to restore EVERY incidence of the original hub, including its larger module supports and pad tokens. At h4 all module supports already have size4 and no compaction is needed.

No simultaneous block edit is treated as a primitive. The later repair operates on individual incidences in original roots; temporary states need not keep labels in blocks or preserve the displayed module shape.

## 4. Actual source guard, placement, all pair safety and full hub restoration

At an arbitrary original exact-four INPUT E, retain in each support an h-subset meeting a supplied minimum four-cover H_E. Delete excess incidences singly. Every deletion is exact four and floor-safe, an eligible deletion exists whenever excess remains, and finite excess decreases. Save its reverse.

The resulting exact compact tuple E* has hr ACTUAL incidences. Its maximum label degree d satisfies d>=ceil(hr/k)>=3. The ACTUAL roots avoiding that label form a three-guard: a two-cover of them, together with the omitted label, would hit the complete exact E* with three labels. This guard occupies r-d existing slots.

The compact exact hub has a FOUR-slot actual guard. At least d>=3 original slots lie outside the source guard. Place three hub-guard tokens there, placing the fourth in one source-guard slot only if needed; extend to a permutation of ALL hub support tokens. Uniform ORIGINAL floor h and compact size h justify every support's destination compatibility.

Accepted full EXACT endpoint-permutation Lemma M implements that permutation through floor-safe primitive swaps in{3,4}. It does not permute an unprotected level-three guard or license arbitrary mixed-floor reassignment. Its token-fixing rule supplies a swap whenever the assignment is unfinished, fixes a destination slot, and moves no fixed slot. Save the complete permutation path's reverse.

Let J be the placed hub guard and I the actual source guard, with |I intersect J|<=1. Accepted O1 provides the LOWER schedule: repair destination-exclusive J slots while I remains fixed; process the possible shared slot through its actual union; then hold the fully installed J guard while repairing every remaining root to the permuted hub.

During the shared-slot stage the comparison family consists of unchanged source-exclusive roots, completed destination-exclusive roots and the actual shared union. Any palette pair hitting all exclusive roots must miss both shared endpoint supports by the two actual guard inequalities. It consequently misses their union. Current comparison-stage roots are subsets of those supports, so the missed-root witness persists. The unchanged old guard protects preparation, and the fully installed new guard protects final restoration. EVERY forbidden pair has an ACTUAL existing root witness in the same carrier throughout.

At each unfinished root, a missing destination incidence can be added; after the complete destination is present, an old-only incidence can be deleted. Additions preserve the source floor-safe support and deletions preserve the complete destination. Each changes ONE incidence, uses only P and reduces the scheduled symmetric difference. Finite root/phase order and eligible-next-edit existence prove termination. Installation renews protection before remaining old-guard roots are edited; exact-four restoration is not needed at the level-three handover boundary.

This actual finite schedule maintains tau>=3 but may exceed four. Baseline maximum-layer Theorem A converts it between the exact compact endpoints to a finite{3,4} path, preserving original floors and carrier. The converted path may change the schedule or use temporary/repeated edits; no directed or length property is inferred.

Append reversed full hub permutation and reversed exact hub compaction. This reaches the SAME original labelled/noncompact hub Q. For original exact endpoints E,C, construct both COMPLETE paths E->Q and C->Q, reverse the latter and join at this exact full Q. The reverse includes destination compaction restoration and returns EVERY original labelled/noncompact support of C. Complete exact joins allow repeated use without accumulated deficit.

These are the actual hypotheses and construction of accepted X12A with m=4. Exactness, guard existence and slot budget are separately supplied here; hub existence alone is not taken as access. This proves X20H.

For h4,k11/12,r>=8, t1 and7t+h=11. Further4r>=32>2k, so ceil(4r/k)>=3. The new eight-slot hub is therefore accessible from EVERY exact endpoint on both palette classes at all such root counts.

## 5. Six-slot uniform exact-four repair at every floor

At any exact-four tuple with r=6, every label degree is at most THREE. If a label occurs in d roots, that label plus one existing label from each of the6-d avoiding roots would hit all roots in at most7-d labels. Exact four gives4<=7-d, hence d<=3. This endpoint bound is not reused at inexact prefixes.

If d=3, the three actual avoiding roots must require three hitting labels. Three nonempty roots can require three only when pairwise disjoint: a label shared by two, plus any label of the third, would be a two-cover. Their original floors h therefore require at least3h distinct labels, all outside the degree-three label. Thus k>=3h+1.

Consequently if k<3h, degree three is impossible and all degrees are at most two. Exact compaction would have6h incidences but at most2k<6h, contradiction. Such carriers are infeasible. No no-path inference is made from a failed construction.

For every potentially feasible k>=3h, compact both endpoints exactly. Their max degree is at most M=3; put D=2 and S=6h. Accepted X15N's conditions are

D<=M,
S<=Dk,
r=6>=D+M+1=6.

When S=Dk, necessarily k=3h, and the additional saturated condition is r=6>=2D+2=6. Thus both strict and saturated cases are supplied. This is a transparent consequence of accepted X15N, not a new incidence handover.

For clarity, X15's protected leveling uses actual above-two donors and below-two recipients and an actual row containing the donor but not the recipient whenever excess remains. A pair containing the newly added recipient hits at most D+M=5<6 roots; every other pair retains an old missed-root witness. Deletion cannot lower tau. Finite excess decrease yields a degree-two entry, which may be exact three rather than four.

Strict-slack repair uses an existing spare column and restores any cycle-row or outside-row buffer. Saturated repair uses one temporarily overfull column, and every pair hits at most2D+1=5<6 roots. Completed cycles restore the reusable degree/balance structure. The pending graph supplies the next greedy move or cycle whenever differences remain; finite macro progress terminates. Saved destination leveling and exact-compaction reverses restore the original exact endpoint.

Only the full lower path between ORIGINAL exact endpoints is passed to maximum-layer A. Inexact internal entries are not supplied to an exact-endpoint theorem. No original floor, palette or slot is changed. This establishes X20S for all original uniform h, with full labelled/noncompact restoration.

Feasibility at k=3h is NOT decided by this argument; for example accepted X13 excludes the original h3 six-slot/nine-label case, while even-floor examples can be feasible. X20S supplies connectivity whenever exact inputs exist.

## 6. Seven-slot floor-four eleven/twelve-label access to renewal

Let h4,r7 and k11 or12. At exact four, every label-avoiding family is an actual three-guard on at most k-1<=11 labels. A three-root three-guard would require three disjoint original-floor-four supports, hence12 labels. Fewer than three roots cannot require three labels. Therefore every avoiding family has at least FOUR actual roots and every endpoint degree is at most7-4=3.

Exact compact endpoints have S=28 and M=3. Use accepted X15N with D=3. Its protected-leveling inequality is

r7>=D+M+1=7,

and S28<3k for both k11 and12. No saturated condition is needed. The explicit strict-slack buffer/cycle construction maintains degree<=3, so each pair hits at most6<7 actual roots. Every next transfer/cycle is supplied, buffers are restored, finite pending progress terminates, upper conversion and saved reverse compactions restore original destinations.

This is an actual derived endpoint protection bound and inherited renewal consequence, not a separately launched campaign or claim that an exact-level-three arbitrary prefix can finish.

## 7. Universal floor-four carrier composition

For ORIGINAL h4 and exact target four, every root has size at least4. Exact feasibility implies k>=7, because any k-3 labels hit every root, giving tau<=k-3. It also implies r>=4, since one existing label per nonempty root gives a cover.

The following branches exhaust EVERY finite k,r with possible exact endpoints:

| Palette | Root counts | Complete argument |
| --- | --- | --- |
| k<=6 | all | Exact four infeasible |
| k7 or8 | every feasible r | Accepted X7H:2h=8>=k |
| k9 | every feasible r | Accepted X19F, complete nine-label class |
| k10 | every feasible r | Accepted X16, complete ten-label class |
| k11 or12 | r4 | Exact four forces four pairwise-disjoint roots; accepted protected J |
| k11 or12 | r5 | Accepted five-root F, arbitrary positive floors |
| k11 or12 | r6 | X20S; k11 infeasible, k12 conditional saturated repair |
| k11 or12 | r7 | Section6's actual degree-three strict repair |
| k11 or12 | r>=8 | New X20H eight-slot/four-guard access |
| k>=13 | r4 | Protected J |
| k>=13 | r5 | Accepted five-root F |
| k>=13 | r6 | X20S |
| k>=13 | r>=7 | Accepted X12W:h4,r>=h+3=7,k>=3h+1=13 |

All rows with r<4 are infeasible. At r4, any intersection between two roots would supply one label hitting both and one each for the other two, giving a three-cover; hence every feasible exact-four tuple has four disjoint actual supports and satisfies J. For k11/12 such supports would need16 labels and are infeasible, but the theorem application remains correctly conditional. F is the accepted complete five-root theorem, including its saturated case, with SAME original positive floors. No uniform extra assumption is inserted.

X7's half-palette guard derivation and compatible disjoint placement apply for k7/8; possible feasibility exclusions are not needed to infer repair. X19's full nine-label composition preserves its undecided feasibility at r11..13. X16's ten-label result preserves its undecided feasibility at r9. Neither uncertainty is a remaining CONNECTIVITY obligation.

At k>=13,r>=7, X12W constructs a complete h+1-label core and two disjoint private h-roots, with an actual three-root guard. Its exact compact incidence supplies degree>=2 when palette room is absent; if k>=hr, accepted AE applies at the ORIGINAL floor sum. All hub access/permutation/O1 and palette-room hypotheses are supplied by that accepted theorem. It does not merely prove internal connectivity of module-shaped endpoints.

Every positive branch restores exactly the ORIGINAL labelled/noncompact destination and stays within the SAME native band{3,4}. Hence the branches prove UNIVERSAL X20U. There is no remaining uniform-original-floor-four,target-four ROOT carrier case, no finite passing-case extrapolation and no external alignment.

## 8. Explicit mixed corollary through actual exact projection

Suppose each ORIGINAL floor a_i is4 or at least k-2. Selected high-floor slots meet every three-label set by their complement-size bound. At a full exact-four endpoint, the actual retained nonautomatic family must itself be EXACT four: a retained cover of at most three labels could be padded to three on P and would hit every selected high-floor root, contradicting full exactness. This is accepted X17's sufficient projection fact, not a converse safe-path projection claim.

For k>=7, retained floors below k-2 are all original FOUR, so X20U supplies complete retained{3,4} repair. Enact it directly in the corresponding EXISTING full slots while holding large roots fixed. A retained minimum cover of size three or four hits every large root; conversely full covers hit the retained family. Full and retained hitting numbers therefore agree throughout this supplied path. Every forbidden pair has an ACTUAL retained missed-root witness.

Once the retained original destination is restored at exact four, repair each selected large root through its own union with its original destination, by individual additions followed by deletions. The retained exact family supplies the lower four bound and its minimum four-cover hits every legal large support, giving full exact four throughout. Each original floor is preserved; missing/excess incidences supply next moves and decreasing symmetric difference. All original noncompact labelled supports are restored.

For k<=6, floors>=4 are automatically at least k-2. Every root then meets every three-set, so full exact four is impossible. This is infeasibility, not disconnection. If the retained family is empty at any k, X17 likewise excludes exact endpoints rather than treating an empty auxiliary carrier as a disconnected class.

Thus X20L covers arbitrarily many original large-floor coordinates around the uniform-four active family without a whole-carrier incidence budget. It does NOT license arbitrary mixed-floor root permutations, floor weakening or universal native safety projection. Original floor-three/four mixtures remain outside this new corollary unless another accepted result independently applies.

## 9. Consolidated scientific explanation: create, transfer, renew, restore

The new module separates exactness from the size of a protecting subfamily. A full seven-root module requires THREE labels, but three of its existing supports already require TWO. Appending one private root creates full exact FOUR while the smaller subfamily supplies a FOUR-root three-guard. The guarding structure costs fewer slots than using the whole exact module as protection.

Exact input consistency supplies the other side of the handover: a sufficiently frequent actual label leaves an actual label-avoiding three-guard and enough outside slots to install the new one. The new hub's guard size reduces this access requirement to degree THREE. Eleven/twelve-label floor-four compact incidence supplies it for every r>=8, with no input module shape assumed.

Actual comparison witnesses protect each individual edit; a decreasing potential is accompanied by an eligible next edit. Full installation renews protection before old guards are modified, even at level three. Maximum-layer conversion controls the upper band only after a real finite lower connection exists. Saved exact preparations, full compatible permutations and exact hub joins restore every original destination, including noncompact incidences.

Smaller arity uses the SAME accepted incidence renewal explanation: exact endpoint constraints force degrees small enough, protected leveling creates a reusable degree class, strict slack restores buffers, and saturation carries a travelling hole with one temporary overfull column. These structural forms compose with X19's shared-core blockers and previously accepted wide-palette/half-palette methods; they do not form a checklist of independent campaigns.

X15's universal original-floor-three result remains unchanged. X20 establishes the next uniform floor's complete root repair, and X17 gives a declared additional mixed extension. X5's particular same-slot avoiding-triple guard is not universally manufactured; complete repair is supplied by replacement mechanisms. Local safe moves, renewal and guaranteed complete restoration remain distinct obligations and are all furnished here.

## 10. Remaining questions, inherited scope and publication boundary

Original A11 destination-directed universality stays OPEN: endpoint permutation, temporary buffers, compaction/restoration and upper conversion can alter the original incidence schedule. Arbitrary original mixtures of floors3 and4, general original floors>=5, higher target and unrestricted nested universality remain open outside accepted classes.

Root repair lifts only when the actual inherited six-clause child interfaces/fixed-root clearance are supplied. A universal uniform-floor root theorem is not proof that all nested children satisfy those interfaces, and a root-only obstruction is not native nested necessity.

Actual dependency domains checked here: X12A/X12W, X7H, X19F, X16 ten-label composition, X15N and its actual strict/saturated lower constructions, X17 sufficient projection/lift; O1; certified baseline GENERAL_PARENT_CONNECTIVITY A/F/exact compaction and conditional child interfaces, OVERLAPPING_CLIQUE_EXCHANGE M PROTECTED_EXCHANGE J, and PALETTE_SLACK_CONNECTIVITY AE as used in X12. Frozen mathematical sources and previous reviewed consolidations are not rewritten or recertified. The displayed module is verified by its own incidence table, with no new external design theorem.

No native floor is weakened or reassigned, no slot or label is added, and block structure is not imposed on intermediate states. This is ordered repair/retained recoverability and a unit upper bound, not fundamental time, physical energy, metric, gravity or an originality claim.

No numerical enumeration, scientific tests/workflows/run IDs, implementation, benchmark, numbered v16.55 certification or certified integration merge. Certified v16.54 remains466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. Separate accepted efficiency baseline/A2 proposal/tiny validation DESIGN stays complete at ea49d2556e4ca4929c0aece68d01e8193ab94b66; runner implementation/fixture execution/measured speedup remain unstarted. Any later implementation certification retains prospective full-domain/reproduction/inherited execution/actual-merge audit gates.

Fresh independent WHOLE-ARGUMENT review must check the full universal composition and consolidated explanation, not merely the small hub. Analytical freezing discloses known reasoning and is not prospective numerical preregistration.
