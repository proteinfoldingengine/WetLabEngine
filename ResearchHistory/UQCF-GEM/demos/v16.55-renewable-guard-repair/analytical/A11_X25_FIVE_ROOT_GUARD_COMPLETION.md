# A11.X25 — five-triple protection with grouped exact completion

Scope: 6163f3aa0e6d4db75eca3d3a38c07e0fc2940b2c.
Parent analytical publication: 24133ff861c23f324a6c5322a6db7a70d85de08d.
Certified baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent whole-argument analytical review.

## 1. Native setting and exact conclusions

Fix a finite ordered palette P with SEVEN labels, r labelled original slots, and original floors a_i in {3,4}. Let ell be the number of original floor-three slots. Each support is any subset of P of size at least its own original floor. A primitive adds or removes ONE incidence in ONE root. Temporary larger supports, repeated edits and changes to background roots remain permitted. Endpoints have transversal EXACTLY FOUR.

Strings such as123 denote the corresponding sets of existing palette labels, ordered as1,...,7 for the displayed constructions. Relabelling the notation is not a primitive.

**Lemma X25G — minimum-cardinality actual guard on seven labels.** The five actual triples

G=(123,145,246,257,367)

have transversal three. Their COMPLETE minimum three-covers are exactly

123,126,127,156,147,167,
234,246,247,235,256,257,
345,347,356.

No family of at most four supports, each of size at least three on seven labels, has transversal at least three. Thus five is the minimum actual guard cardinality in this declared size/palette setting. This is not an optimal exact-hub theorem.

**Lemma X25Q — two grouped exact-four completions.** On those same seven labels:
- Q15 consists of the five guard triples, THREE triple reserves and SEVEN four-support reserves, fifteen tokens total and EIGHT designated triple tokens;
- Q14 consists of the same five guard triples, FOUR triple reserves and FIVE four-support reserves, fourteen tokens total and NINE designated triple tokens.

Both have exact transversal four, actual five-root three-guard G, and supplied minimum four-cover H=1234. Every forbidden triple is missed by an actual guard or assigned reserve. Tables in Section 3 specify every support and obligation.

**Theorem X25R — complete original mixed-floor repair.** EVERY pair of original exact-four endpoints on the same fixed carrier has finite native repair with 3<=tau<=4 and full original labelled/noncompact destination restoration in either sufficient class:

(A) r>=15 and ell>=8;
(B) r>=14 and ell>=9.

Only seven existing labels and existing slots are used. No input guard shape, X5 qualification or destination monotonicity is assumed. All original floors stay fixed. Earlier classes remain accepted, including X23's ell>=10,r>=13 and every r>=35 on seven labels.

The discovery reduces the actual guard cardinality from the six-root X11/X23 construction to five, while explicitly completing ALL minimum-cover obligations and deriving compatible access from actual capable-slot incidence. This gives new guaranteed mixed carrier classes, not merely a guard example.

## 2. Actual pair witnesses and complete minimum covers

Every two-label set fails to hit G. It must meet root123, so classify by its first available label among1,2,3:
- If it contains1, its other label would have to lie in 246 intersect257 intersect367. The first intersection is{2}, which misses367; the triple intersection is empty.
- If it contains2 but not1, its other label would need to hit BOTH145 and367. Those supports are disjoint.
- If it contains3 but neither1 nor2, its other label would have to lie in 145 intersect246 intersect257. The first intersection is{4}, which misses257.
A pair missing123 already has that root as its witness. In each displayed case an unmet actual support supplies the witness; choose the first unmet support in guard order. This handles every pair, and smaller sets cannot be covers. The triple123 hits all five roots, so tau(G)=3.

Classify every three-label cover K similarly:
- If1,2 are both in K, its third label must be in367: exactly123,126,127.
- If1 belongs to K but2 does not, its two remaining labels lie in{3,4,5,6,7}. They must meet246 via4 or6, meet257 via5 or7, and meet367 via3 or6 or7. Of the four choices crossing{4,6} and{5,7},45 misses367; the other three give147,156,167. No pair containing3 can meet both disjoint sets{4,6},{5,7}.
- If1 is absent and2 present, the other pair must meet145 via4 or5 and367 via3,6 or7. These disjoint sets give exactly234,246,247,235,256,257; roots246 and257 are already met by2.
- If1,2 are absent, K must contain3. Its remaining pair in{4,5,6,7} must meet145 via4 or5,246 via4 or6, and257 via5 or7. The choices are45,47,56, giving345,347,356.

This exhaustive symbolic classification proves the list without running an enumeration. Guard lower witnesses and every minimum-cover case use the SAME actual supports.

For the cardinality boundary, accepted X14G says three supports of minimum size three requiring three labels need nine labels, and four such supports need at least ceil(15/2)=8. Both exceed seven. One or two nonempty roots cannot require three labels. Thus five is necessary and our displayed family attains it. This applies to larger supports too, but says nothing about the minimum total roots needed for an exact-four completion.

## 3. Full allowed pools and exact completion

Use the first THREE reserve groups:

| Assigned guard covers | Union of assigned covers | Actual triple reserve |
| --- | --- | --- |
| 126,127,167 | 1267 | 345 |
| 234,235,345 | 2345 | 167 |
| 156,256 | 1256 | 347 |

Each reserve is the FULL complement of its group's union within P, so it misses every assigned cover. The eight assigned covers are distinct.

The SEVEN remaining minimum guard covers are123,147,246,247,257,347,356. Add their actual four-label complements:

| Assigned guard cover | Actual four-support reserve |
| --- | --- |
| 123 | 4567 |
| 147 | 2356 |
| 246 | 1357 |
| 247 | 1356 |
| 257 | 1346 |
| 347 | 1256 |
| 356 | 1247 |

Together with G these specify Q15 completely: five triple guards, three triple reserves, seven four-support reserves. All fifteen minimum guard covers have an actual missed reserve.

For Q14 retain the first three groups and additionally group147,247, whose union is1247, using its full complement356 as a fourth triple reserve. Retain ONLY the five four-support reserves assigned to123,246,257,347,356 in the second table. Thus Q14 has five triple guards, four triple reserves and five four-support reserves. All fifteen covers again have actual assigned missed reserves; no independent capacity is assigned to overlapping groups.

Every three-set K either fails to cover G and misses an actual guard root, or is on the complete Section 2 list and misses its assigned actual reserve. Thus both full tuples have tau>=4. Smaller sets follow by adding labels to reach size three.

H=1234 hits all five guards and the triple reserves345,167,347,356. Every four-support on seven labels intersects a four-label H because4+4>7. Hence H hits every root in either full tuple and proves tau<=4. Both are EXACT FOUR before access is invoked.

This is the actual X11 completion principle applied to a different smaller guard, with all covers and pools proved directly. We neither rewrite X11 nor assume a pool fits a floor simply because it has sufficient total capacity: actual reserves and H-incidences are supplied. No global optimality of grouping or hub size is claimed.

## 4. Legal full hubs at original slots

For class A select EIGHT distinct original floor-three slots and place Q15's eight triple tokens there. Put its seven four-tokens into any seven other distinct existing slots, possible because r>=15. These tokens fit any original floor3/4.

For class B select NINE distinct original floor-three slots for Q14's nine triple tokens; its five four-tokens fit five other slots, possible because r>=14.

Fix a deterministic initial assignment by original slot order. Fill each further EXISTING slot with a size-four support containing the actual guard support123, for example1234. This fits original floors3/4. The base tuple supplies tau>=4, and H=1234 meets every padding root. Thus the completed FULL labelled hub Q is legal and EXACT FOUR. Its actual five-slot guard remains G.

This specification does not install supports simultaneously at an input. The following access argument supplies all individual native edits. It keeps the full four-tokens intact during permutations; it does not compact them to unequal original floors prematurely.

In X23A's notation h=3,m=5,n=8 or9,b<=4. Every non-designated token has size four and fits every original floor. There are enough capable slots for every designated triple token, not only the guard.

## 5. Actual source preparation and capable outside slots

For arbitrary exact-four source E choose a supplied minimum four-cover H_E. In every original slot retain an a_i-subset meeting H_E and delete excess incidences individually. Deletion cannot lower tau, and retained H_E gives tau<=4; every primitive remains EXACT FOUR. The next excess incidence exists whenever preparation is unfinished, and total excess decreases. Save the full reverse.

Let E* be this exact original-floor compaction. Restricted to original floor-three slots, it has EXACT incidence sum3ell. Thus some actual palette label x satisfies

d_3(x)>=ceil(3ell/7)>=4

in both classes, because ell>=8. These are incidences in slots capable of holding triple tokens. All floor-four roots stay present in the actual source; their incidences are not counted as small-token placement room.

Let I be ALL actual roots of E* avoiding x. They form an actual three-guard: a two-cover of them, together with x, would cover E* with at most three labels. Every palette pair is therefore missed by some actual I root.

The d_3(x)>=4 capable slots containing x are DISTINCT original slots OUTSIDE I. Place four of Q's five guard triple tokens there, and the fifth in any distinct remaining capable slot. Such a slot exists because ell>=n>=8. Its location may be inside I, so the destination guard J has overlap at most ONE with I.

Place the other n-5 designated triple tokens in remaining capable slots; ell>=n guarantees enough. Assign every remaining FULL token to a remaining original slot. Its size four fits every original floor. This extends the injection to a bijection of ALL full hub tokens, including duplicates treated as distinct tokens.

The full permuted hub Q' is consequently legal and exact four. This is the actual X23A compatible-assignment hypothesis, supplied constructively; it is not an arbitrary mixed compact-support permutation. Different sources can choose different x and different assignments, but saved full reverses return them to the SAME fixed labelled Q.

## 6. Native edits, every pair witness and renewed progress

First supply the full permutation Q->Q' using baseline M. Process original slots in decreasing floor order. If a slot is unfinished, its desired token lies in an unfixed slot. Its final fit is already proved. The displaced support meets the current floor, which is at least the other slot's floor, so it fits that slot. Expand the two actual supports to their union, then contract to the legal swapped supports, one incidence at a time.

For a swap, the union tuple has tau>=3: a cover of it hits at least one of the two original supports, and adding a label from the other repairs it to an original four-cover. Every intermediate contains either its original or swapped exact-four endpoint and is contained in the union tuple. Hence every primitive has tau in{3,4}; floors hold at every addition/contraction. Every completed swap fixes another token without moving fixed slots, so a next swap exists until termination. Save the full finite reverse Q'->Q. Unequal ORIGINAL floors remain fixed.

Now build the actual LOWER access E*->Q' by O1:
1. Keep I unchanged while repairing every slot in J minus I to its FULL Q' support, adding missing destination incidences then deleting old-only incidences.
2. If there is a shared slot s, expand E*_s to its union with Q'_s, then contract to Q'_s.
3. Hold fully installed J unchanged while repairing all remaining slots to Q'.

During stage1 every forbidden pair misses an unchanged actual I root. At the shared handover use the comparison family consisting of source-exclusive I supports, destination-exclusive J supports and the shared union. If a pair misses an exclusive support it has that actual witness. If it hits all exclusive supports, both guard inequalities force it to miss BOTH shared endpoint supports, so it misses their union. Current supports on these guarded indices are subsets of their comparison supports throughout the handover, preserving that missed witness. With empty overlap, the old guard itself supplies the comparison. During stage3 the completed actual J guard protects every pair.

This accounts for ALL palette pairs using the SAME actual roots, not separate capacities. It also treats smaller covers. The floor-four background roots can be changed once installed J is available; they are not frozen as a new native rule.

Every addition retains an existing legal support. Every scheduled deletion retains the already complete destination support meeting the same original floor. An unfinished scheduled support has a missing destination incidence or, after all are present, an old-only incidence, supplying its next primitive. Each such edit decreases its scheduled symmetric difference by one. Finite phase/slot lists and finitely many incidence differences yield finite termination at EXACT Q'.

The completed five-root destination guard is installed BEFORE the remaining old protection is modified. It is reusable for finishing the other roots; the construction need not return tau to exact four after every handover. This is actual renewal plus available finite completion, rather than an arbitrary-safe-prefix assertion.

## 7. Upper conversion and original destination restoration

The preliminary access is a finite native lower path with tau>=3; its upper bound can exceed four. Its endpoints E*,Q' are ACTUALLY exact four. The native positive-floor carrier allows arbitrary additions/unions and all roots remain nonempty. Baseline maximum-layer A therefore converts this FULL lower leg to a finite primitive path with tau in{3,4}. It may alter the schedule; no path-length or destination-direction claim is made.

Prepend saved exact source compaction and append saved reverse FULL permutation Q'->Q. This reaches the SAME fixed full labelled exact hub Q. There is no compaction of Q's four-support reserves before the return.

Construct the same complete leg C->Q for the arbitrary original destination C and reverse it. Both legs meet at identical labelled full Q, not merely a symmetry copy or a level-three guard. Reversal is legal in the undirected native incidence graph. Reversed destination compaction restores EVERY original noncompact support and incidence in its original labelled slot.

Thus A->Q->C is finite and stays in{3,4}, proving X25R. The same construction works for any finite chain of exact endpoints in the declared class, without accumulated deficits. X5 and its same-slot qualification are not invoked.

## 8. New guaranteed classes and controls

Class A includes the genuine mixed profile k7,r15 with EIGHT original floor-three slots and SEVEN original floor-four slots. Q15 is an exact feasible control on precisely that profile, with a supplied minimum H. Class B similarly supplies k7,r14 with NINE original floor-three slots and FIVE floor-four slots via Q14. The theorem connects EVERY arbitrary exact pair on these fixed profiles, not just module-shaped inputs.

The prior X23 seven-label sufficient classes require ell>=10,r>=13 or r>=35, so neither control lies there. X22 covers larger palettes and six slots, not these controls. They have no floor1/2 or cover-automatic original floors>=k-2=5; uniform X15/X20 statements do not apply to these mixed profiles. Max-floor wide modules need larger palettes. Existing conditional pair bridges can still cover some pairs; no universal failure of those bridges is claimed.

Both controls fail EVERY choice of X15N whole-carrier degree/slack parameters:
- Q15's profile has S=52 on seven labels. Any original-floor compaction has maximum degree M>=ceil(52/7)=8. X15N would require D<=r-M-1<=6, but S<=Dk would then give52<=42, impossible.
- Q14's profile has S=47, so M>=ceil(47/7)=7. Again D<=14-7-1=6 and47<=42 is impossible.
Even increasing the claimed M only tightens this contradiction. X14C also fails for every degree cap: D>=8 would require r>=18 in the first profile; D>=7 would require r>=16 in the second.

Thus the new proof genuinely supplies complete repair beyond those whole-carrier methods. It derives an actual capable-slot degree and a minimal-cardinality guard, completes its cover obligations at exact four and supplies compatible repeatable access. No total-capacity count alone implies the path.

These are structural sufficient classes, not full feasibility classification or globally optimal root/slot thresholds. A failure to meet either construction is not native disconnection. No numerical case campaign has been run.

## 9. Dependencies and open obligations

Read inherited actual sources at parent24133ff861c23f324a6c5322a6db7a70d85de08d: X23A graded access and full token placement; X11 grouped completion principles; GUARD_HANDOVER O1; X14G's guard palette bounds; X15N's control inequalities. Read baseline GENERAL_PARENT_CONNECTIVITY exact compaction/A and OVERLAPPING_CLIQUE_EXCHANGE M at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f. Domains are checked, not recertified or rewritten. The concrete guard and its COMPLETE cover classification are proved here; no external design catalogue or equality theorem is imported.

Earlier X15/X20/X22/X23/X24 results remain accepted. Remaining mixed3/4 carriers must exclude these new seven-label low-reserve classes in addition to ALL inherited classes. Continue stronger actual guard/grade constraints or genuinely reusable coupled handovers; do not turn residual root counts into isolated campaigns.

Original A11 destination-directed scheduling, unrestricted mixed/higher-target/nested repair and physical interpretation remain open. Child lifting retains inherited exact-child interfaces/fixed-root clearance. Unit repair is an upper bound, not a positive minimum for every pair. Ordered repair and retained recoverability introduce no fundamental time or inserted geometry.

No scientific enumeration, numerical tests, workflow/run IDs, implementation, benchmarks or certified integration merge. Certified v16.54 and separately accepted efficiency design remain unchanged. Efficiency runner execution and measured speedup remain unstarted. Numbered v16.55 remains OPEN: prospective protocol, independent full-domain reconstruction, rejecting controls, inherited execution, reproduction/durable evidence, exact merge review and post-merge audit gates remain unsatisfied.
