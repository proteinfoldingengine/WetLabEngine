# A11.X26 — high-grade guard access and weighted exact completion

Scope: 185a6d902a7da8b935f81b429de5e7064ecf4e6d.
Parent analytical publication: 3e3a677c431f7a2bfbb02599062016b215120b52.
Certified baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent whole-argument analytical review.

## 1. Native rules and exact statements

Fix a finite ordered palette P of k labels and r labelled original slots. Each support is any subset of P meeting its ORIGINAL positive floor. A primitive adds or removes ONE incidence in ONE existing root. Larger temporary supports, repeated changes and background edits remain native. Endpoints have transversal EXACTLY FOUR.

**X26A — two-grade access with the guard in the high grade.** Suppose original floors have two values h<b<=k, with ell floor-h slots and f floor-b slots. A specified full legal exact-four hub Q has n support tokens of size h, EVERY other token of size b, and an ACTUAL m-root three-guard among its size-b tokens. If

ell>=n, f>=m,

and an exact original-floor source compaction has an actual label occurring in at least m-1 ORIGINAL floor-b slots, the original source has complete native{3,4} repair to the SAME full labelled Q. Two sources meeting this condition connect with every original labelled/noncompact destination restored. The endpoint-independent sufficient condition is

ceil(b*f/k)>=m-1.

This is incidence in the HIGH slots, not a whole-carrier budget or an assumption that the small tokens themselves carry the guard. n may be zero. The full assignment must fit every original slot; no arbitrary mixed compact permutation is used.

**X26Q — weighted exact-seven-label modules.** On seven labels, for EVERY integer t with0<=t<=7 there is an explicit exact-four hub Q_t consisting of
- t triple tokens;
- 35-4t four-support tokens, INCLUDING an unchanged seven-root four-support three-guard;
- 35-3t tokens total.

H=1234 is a supplied minimum four-cover. Every three-set misses an actual support. Each selected triple token replaces FOUR four-support completion tokens using their SAME avoidance obligations. The construction below is symbolic and uses no scientific enumeration.

**X26R — complete seven-label mixed repair from high incidence.** For original floors3/4 let ell count floor-three slots and f=r-ell count floor-four slots. Set t=min(ell,7). If

f>=9 and r>=35-3t,

EVERY original exact-four endpoint pair has complete native repair with3<=tau<=4 and full original labelled/noncompact destination restoration.

**X26E — feasibility forces access when ell<=6.** On seven labels with original floors3/4 and ell<=6, exact-four endpoints exist IF AND ONLY IF

r>=35-3ell.

On EVERY such feasible carrier all exact-four pairs have complete native{3,4} repair. The statement holds for every ordering of the original floors. Uniform ell0 is inherited in connectivity from X20; genuine mixtures ell1..6 are the new guaranteed classes.

For ell7, Q7 supplies feasibility for every r>=14, while X26R supplies complete repair for every r>=16. No conclusion for the smaller access cases is inferred. These statements are not universal mixed-floor, directed or unrestricted nested repair.

## 2. Exact source compaction and legal guard placement

For X26A choose a minimum four-cover H_E of the arbitrary original exact source E. In every original slot retain an a_i-subset meeting H_E, then delete every excess incidence individually. Retaining H_E ensures tau<=4; deletion cannot lower tau. All preparation primitives remain EXACT FOUR and meet the unchanged floors. Whenever unfinished an excess incidence is eligible; total excess strictly decreases. Save the full reverse.

In the exact compaction E*, the ORIGINAL high slots have incidence sum exactly b*f. Thus some actual label has high-slot degree at least ceil(b*f/k). For a label x meeting the actual degree hypothesis let I be ALL actual roots avoiding x. They form an actual three-guard: a cover of at most two labels for I, with x appended, would cover E* with at most three.

Every high slot containing x is OUTSIDE I. Place m-1 of the hub's HIGH guard tokens in these distinct outside high slots. Since f>=m, put the last guard token in a distinct remaining high slot; it causes at most ONE overlap with I. Call the placed guard indices J.

No low slot was used by this guard placement. Put all n small tokens into distinct ORIGINAL low slots, possible because ell>=n. Every remaining token has size b and fits EVERY remaining original floor h or b. Hence this injection extends to a bijection of ALL full Q tokens, with repeated supports treated as distinct tokens.

The full permuted Q' is legal at the original floor vector and is EXACT FOUR. The assignment proves its compatibility; we do not first compact its large tokens to smaller mixed floors. The actual source guard I includes low and high roots as they exist, while the destination guard J lies wholly in high slots. They are not independently invented witness systems.

## 3. Full native permutation, handover, renewal and restoration

Supply Q->Q' by baseline M's decreasing-floor token procedure. For an unfinished slot the desired token is in an unfixed slot and fits its final destination. The displaced token has size at least the current floor, which is at least the other slot's floor, so it fits there too. Expand the two supports to their union, then contract to swapped supports, using individual incidences.

A cover of that union tuple can be repaired to a cover of the original exact-four tuple by adding at most one label. Hence the union has tau>=3. Each half of the swap contains its corresponding exact-four endpoint, giving tau<=4, and is contained in the union, giving tau>=3. Floor legality follows from the two legal endpoints. Every completed swap fixes another token without moving fixed slots, proving an eligible next swap and finite termination. Save the full reverse Q'->Q.

Construct actual LOWER access E*->Q' by O1:
1. Hold I fixed and repair every slot in J minus I to its FULL destination support, adding missing destination incidences before deleting old-only ones.
2. At the possible single shared slot, expand to the union of its source and destination supports, then contract to the destination support.
3. Hold the completed actual J guard fixed and repair every remaining root to its full Q' support.

Every forbidden pair has an actual missed root at each stage. Initially an unchanged I root supplies it. During a shared handover the comparison consists of source-exclusive supports, destination-exclusive supports and the shared union. A pair either misses an exclusive support, or hits every exclusive support. In the latter case the two ACTUAL guard inequalities force it to miss BOTH shared endpoint supports, and therefore their union. Current guarded supports are subsets of these comparison supports throughout the handover, preserving the witness. If overlap is empty, unchanged source protection suffices. Final repair uses the installed J guard. Smaller sets follow by padding to pairs, possible since exact four requires at least four labels.

All pair types and all actual root grades are accounted for by the SAME supports. Counting incidence in high slots only identifies legal outside locations; it does not assign separate capacities to different pairs. The installed destination guard renews protection BEFORE the remaining old guard roots are changed.

Every addition retains a legal current support; each deletion retains its already complete destination support at that ORIGINAL floor. Every unfinished scheduled root supplies a missing incidence, or after all destination incidences are present an old-only incidence. Each scheduled edit decreases its symmetric difference by one. Finite phase lists and finite incidence differences give finite completion at ACTUAL exact Q'. The preliminary lower path can rise above four.

Apply baseline maximum-layer A ONLY to this complete lower leg between the exact-four endpoints E*,Q', on the original union-closed positive-floor carrier. It gives a finite path in{3,4}; no schedule or efficiency preservation is asserted. Prepend source exact compaction and append saved reverse FULL Q'->Q permutation. This reaches the SAME fixed labelled full Q.

For arbitrary original endpoints A,C build both complete legs to Q, reverse C's leg and join at identical full exact Q. The incidence graph is undirected, so reversal is legal. Saved reversed destination compaction restores EVERY original noncompact support and label incidence in its ORIGINAL slot. Complete paths can be repeated between any finite chain of inputs in the class. Exact reset is at the joins; intermediate renewal need not restore exact four after every handover. This proves X26A.

## 4. The actual seven-root high guard

On P={1,...,7} use the accepted displayed triples

L1=123,L2=145,L3=167,L4=246,L5=257,L6=347,L7=356.

Their complements are

R1=4567,R2=2367,R3=2345,R4=1357,R5=1346,R6=1256,R7=1247.

The pair table is
1:(23,45,67);2:(13,46,57);3:(12,47,56);4:(15,26,37);
5:(14,27,36);6:(17,24,35);7:(16,25,34).

Each row partitions the other six labels, so every pair lies in exactly one L_j. Consequently for EVERY pair K some actual R_j misses K. The supplied triple124 hits every R_j because124 is not a listed L triple. Thus all seven R_j form an actual EXACT-three guard of four-supports. This is accepted X20's displayed guard, not a newly imposed geometry.

Two L triples intersect in at most one label by unique pair coverage. They cannot be disjoint: a point in one would need three distinct other triples to pair it with the three points of the other, giving degree at least four rather than the displayed degree three. Hence distinct L triples intersect in exactly one, and distinct R complements intersect in exactly two.

No L_i is contained in an R_j, since that would mean disjoint L_i,L_j (or, when i=j, disjointness from itself). Each R_j has exactly FOUR triple-subsets; these are non-L triples and cannot occur in another R because two R intersect in only two labels. Thus the seven groups

B_j={K subset R_j:|K|=3}

are pairwise disjoint, each of size four, and together account for all twenty-eight non-L triples among the thirty-five triples on P. These facts follow from the specified actual incidences, not an executed search.

## 5. Weighted grouped completion with all triple witnesses

Start with the thirty-five four-supports P minus K indexed by ALL triples K of P. Every triple misses its complementary support, so this family has tau>=4. Every four-set meets every four-support on seven labels, giving exact four.

For t in0..7 select the first t groups B1,...,B_t. Remove their four complementary four-support tokens for each selected j, replacing them with the single triple token L_j. Specify Q_t directly:
- low tokens L1,...,L_t;
- high tokens P minus K for EVERY triple K not in the union of the selected B_j.

The B_j are disjoint, so exactly4t high tokens are replaced and total counts are t+(35-4t)=35-3t. Every original high guard root R_i remains: it is indexed by K=L_i, and no L_i belongs to any B_j.

For EVERY triple K:
- if K belongs to a selected B_j, K subset R_j and the actual replacement root L_j=P minus R_j misses it;
- otherwise the actual retained root P minus K misses it.

All thirty-five triple obligations are covered by actual existing supports, with the SAME single L_j carrying the four obligations in its selected group. This is replacement of protection/completion using shared incidences, not four independently assigned reserves.

H=1234 hits every listed L_j, by their displayed incidences. It also hits every retained four-support since4+4>7. Thus tau(Q_t)=4 with supplied minimum H. Its actual seven-root high guard remains unchanged. This proves X26Q.

The construction is a finite symbolic support formula, not a numerical campaign. Every support lies in the original palette. Its tokens are later realized at existing slots and reached by individual primitives; replacement in this completed specification is not a simultaneous native edit.

## 6. Legal full hub and high-grade access

For original floors3/4 set t=min(ell,7). Place Q_t's t triple tokens at t distinct original low slots and its 35-4t four-tokens at other distinct existing slots. This is possible whenever r>=35-3t: there are at least that many total slots and at least t low slots. Four-tokens fit every other original floor, including unused low slots.

Every further existing slot receives a duplicate R1 of size four. The base supplies the lower exact-four bound and H meets every padding root, so the full labelled Q is EXACT FOUR. No token is compacted to an unequal floor before permutation.

For X26A take h3,b4,n=t,m7. The hypothesis f>=9 implies both f>=m and

ceil(4f/7)>=ceil(36/7)=6=m-1.

At every exact source compaction an actual label therefore occurs in SIX high slots outside its ALL-root avoiding guard. The seventh high guard token goes into another high slot. All small completion tokens fit untouched low slots, and the remaining four-tokens fit every remaining slot. This supplies full compatible access and complete restoration by Sections 2–3, proving X26R.

The count is on the right grade: many low incidences are not used as high-slot capacity, and high roots remain present in the actual avoiding family whenever they miss x. Whole-carrier degree/slack budgets are unnecessary.

## 7. Feasibility forces both completion room and access

At exact four, every triple must miss an ACTUAL root. A size-at-least-three root on seven labels has a complement containing at most binomial(4,3)=4 triples. A size-at-least-four root has at most binomial(3,3)=1. Thus the SAME actual roots supply the necessary weighted count

35 <= 4ell+f = r+3ell.

This is X24W's individual-floor complementary count, applied before any execution. Necessary capacity does not alone imply existence or repair.

If ell<=6, it gives

r>=35-3ell, f=r-ell>=35-4ell>=11.

Consequently t=ell, hub realization room is supplied, and f>=9 supplies high-grade access. X26R connects every exact endpoint pair. The separate high-incidence hypothesis is forced by exact feasibility.

Conversely, for every fixed ordered floor profile with ell<=6 and r>=35-3ell, Q_ell fits it: ell triple tokens occupy ALL original low slots, its 35-4ell four-tokens occupy that many high slots, and remaining high slots receive duplicate four-support padding. H is supplied and every triple misses an actual root. Thus exact-four endpoints exist. This proves the stated IF AND ONLY IF feasibility and universal repair on this declared subdomain.

At ell0 the all-four-support uniform case overlaps inherited X20; its construction/control is not a new uniform connectivity claim. For ell1..6, the argument gives new complete genuine mixed classes, rather than isolated root-count campaigns.

At ell7 Q7 has seven triple tokens and seven four-tokens, total fourteen. It proves feasibility at r14 and after duplicate high padding at every larger r. X26R additionally applies when f=r-7>=9, namely r>=16. This proof does not assert unavailable access at r14/15 is disconnection. Other classes or mechanisms can address those obligations.

## 8. Method-limit control and precise discovery

The equality instance ell6,r17 has Q6 with six triples and eleven four-supports, exact four and H1234. Its original floor sum is

S=6*3+11*4=62.

Every exact original-floor compaction on this carrier has maximum degree M>=ceil(62/7)=9. X15N's condition r>=D+M+1 would force D<=7, while S<=7D would require62<=49. Thus NO X15N parameter choice can apply, even if a larger M is proposed. X14C also fails: any degree cap D>=9 requires r>=2D+2>=20, exceeding17.

The carrier is genuinely mixed, has no original floor1/2 or cover-automatic floor>=5, lies below the earlier r>=35 guarantee, and has fewer than X25's eight/nine required low slots or X23's ten. X22's larger-palette/six-slot domains do not cover it. Older conditional bridges may apply to individual pairs; their blanket failure is not claimed.

The advance replaces four separate exactness obligations by one actual low support while keeping the large-support guard available in its own original grade. Incidence in that high grade supplies outside locations, full assignment preserves scarce low slots, and O1 renews actual protection before remaining old roots change. This supplies guaranteed full repair beyond whole-carrier cap methods.

Only the declared two-grade access and seven-label mixed subdomain are proved. No optimal total hub count beyond the stated feasibility subdomain, no universal mixed/higher-target theorem, no arbitrary safe-prefix completion or cloning-path claim is inferred.

## 9. Dependencies, review and remaining closure

Applicable accepted sources read at parent3e3a677c431f7a2bfbb02599062016b215120b52: X20's actual seven-root complement guard; X23's displayed pair/intersection identities and full graded assignment method; X24W weighted complementary capacity; GUARD_HANDOVER O1. Baseline M and exact compaction/maximum-layer A are read at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, demos/v16.54-parent-support-connectivity/OVERLAPPING_CLIQUE_EXCHANGE.md and GENERAL_PARENT_CONNECTIVITY.md. X15N/X14C domains are checked only for the control. All frozen sources remain unchanged.

All earlier X15/X20/X22/X23/X24/X25 closures remain accepted. Residual seven-label mixed questions must now exclude ell<=6 and ell7,r>=16, in addition to ALL previous sufficient classes. This is a structural domain reduction, not a campaign checklist.

Original A11 destination-directed scheduling, remaining mixed/higher-target/unrestricted nested repair and physical interpretation stay open. Conditional lifting retains inherited exact-child interfaces and fixed-root clearance. Ordered repair/retained recoverability introduces no fundamental time or geometry. Unit repair is an upper bound, not a positive minimum for every endpoint pair.

No scientific enumeration, numerical tests/workflows/run IDs, implementation, benchmark or certified integration merge. Certified v16.54 and accepted efficiency design unchanged; runner execution and measured speedup unstarted. Numbered v16.55 remains OPEN: prospective scope/protocol, independent full-domain reconstruction, substantive rejecting controls, inherited replay/logs, reproduced durable evidence, exact merge review and post-merge audit gates are not replaced by analytical acceptance.
