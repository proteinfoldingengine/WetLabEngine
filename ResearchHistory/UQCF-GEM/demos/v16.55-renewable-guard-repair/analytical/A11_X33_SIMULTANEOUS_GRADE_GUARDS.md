# A11.X33 — simultaneous original-grade guards remove excess restrictions

Scope:fd8356f7803ae6007ba97fd4c91a993ba6d7247c.
Analytical parent:de679e8d1694d50d0001b75fe2e0f2f5bb0f31a9.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent whole-argument review. Analytical only.

## 1. Exact theorem and native carrier

Fix an ordered palette P of k labels and labelled ORIGINAL slots with positive floors a_i<=k. Partition the slots by their distinct original floors: grade j has n_j>0 slots, common floor h_j and complementary capacity c_j=k-h_j. Primitive moves add/remove ONE incidence in ONE root, retaining that slot's original floor. Arbitrary larger supports, temporary/repeated and background edits remain permitted.

Define the carrier-only integer bound

b_j=floor(n_j*c_j/(floor(n_j/2)+1)).

**X33G — simultaneous actual guard availability.** At EVERY exact-q endpoint, q>=3, if sum_j b_j<k, there is a deterministically selected label x such that the ACTUAL roots avoiding x form a (q-1)-guard occupying at most floor(n_j/2) slots in EVERY original floor grade simultaneously. This holds after legal exact compaction; the analogous count is no larger before compaction.

**X33R — complete mixed-grade native repair.** Under the same inequality, EVERY pair of exact-q endpoints has finite native{q-1,q} repair restoring EVERY original labelled, possibly noncompact destination support. Guard alignment permutes full tokens ONLY within equal ORIGINAL floor grades. There is no arbitrary mixed-floor permutation.

**X33C — grade-capacity sufficient bound.** Let J+ be the nonempty grades with c_j>0, m=|J+|. The simpler bound

k>=2*sum_(j in J+) c_j-m+1

implies X33R. Grades with c_j0 contribute b_j0 and need no reserve.

**X33T — unrestricted two-grade target-four class at larger palettes.** For EVERY k>=13 and ANY counts of original floors k-4/k-3 (either grade may be absent), EVERY feasible exact-four endpoint pair has full native3/4 repair. No oddness, exact saturation, triple-excess, grade balance, source redundancy or X32 placement inequality is assumed.

Feasibility at every profile is NOT asserted. Bound failure is NOT native disconnection. These are root theorems with inherited conditional child-interface lifting, not universal nested or destination-directed theorems.

## 2. Exact preparation and an actual avoiding-label guard

For each original endpoint E choose a minimum hitting set H_E of size q. In every root choose an a_i-subset meeting H_E, and delete excess incidences individually. Every deletion retains its original floor; deletion cannot lower tau, and retained H_E keeps tau<=q. Thus preparation remains EXACT q. Any unfinished root supplies an excess incidence; total excess strictly decreases. Save the full reverse to restore the original noncompact supports.

At compact E*, for a label x and grade j define

g_j(x)=|{i in grade j:x not in E*_i}|.

The SAME actual incidences give sum_(x in P)g_j(x)=n_j*c_j.

For EVERY label x, the actual family I_x of ALL roots avoiding x requires at least q-1 hitting labels. Otherwise a hitting set K of size<=q-2 for that family, together with x, would hit ALL original roots with at most q-1 labels, contradicting exact q. In particular I_x cannot be empty. Full-palette roots contribute nothing to I_x. No hypothetical witness roots or independent capacities are used.

For every K subset P of size<=q-2, this guard therefore supplies an ACTUAL root indexed in I_x disjoint from K. Select the first such index for an explicit witness. This includes K containing x; x cannot help hit a root avoiding it. At q4 this treats EVERY pair, and smaller sets as well.

## 3. Simultaneous grade selection: eligible label and strict bound

A label is bad for grade j when g_j(x)>floor(n_j/2). Each bad label contributes at least floor(n_j/2)+1 to that grade's total n_j*c_j. Hence there are at most b_j bad labels in the SAME palette.

The union of bad label sets has size at most sum_j b_j<k. Consequently at least one existing label is good in EVERY grade simultaneously. Select the first such label in palette order. Evaluating all k actual grade counts and scanning the finite palette furnishes an eligible choice; it does not infer existence from unrelated degree maxima in different grades.

For that x, I_x is the actual (q-1)-guard from Section2 and has at most floor(n_j/2) members in every grade. Derive this separately at compact A* and C*, obtaining actual source and destination guard index sets I and U. Their omitted labels may differ. No same-anchor/same-slot premise is needed.

For c_j>0,

n_j*c_j/(floor(n_j/2)+1)<2c_j,

because floor(n_j/2)+1>n_j/2. Since 2c_j is integer, b_j<=2c_j-1. For c_j0, b_j0. Thus sum_j b_j<=2sum_(J+)c_j-m, proving X33C. If J+ is empty all supports are full palette and exact q>=3 is infeasible, so that vacuous case creates no claimed guard.

This is a derived simultaneous witness bound, not a randomized test, supplied safe prefix or count of successful carriers.

## 4. Compatible FULL destination placement with disjoint guards

In grade j, the source guard uses |I_j|<=floor(n_j/2) slots and the destination guard has |U_j|<=floor(n_j/2) FULL support tokens. Therefore

n_j-|I_j|>=ceil(n_j/2)>=|U_j|.

Choose the first |U_j| slots outside I_j, giving J_j. Map the actual destination guard tokens U_j bijectively to J_j, then map ALL remaining actual destination tokens of that SAME grade bijectively to its remaining slots. Use original index order for finite choices and distinguish equal supports as existing tokens. Apply this independently to every grade. J=union J_j is DISJOINT from I, and EVERY destination token receives a slot.

Call the full permuted destination C'. Every compact grade token has size h_j and every destination slot in that grade has ORIGINAL floor h_j. Thus the complete assignment is floor-compatible. No token crosses grades. It preserves the family of full supports and therefore tau(C')=q. The actual guard on J has the same support family as the original destination guard on U, so its transversal is>=q-1.

Baseline M realizes C* to C' by finite native band-safe swaps. More explicitly, in each grade take the first misplaced destination slot, locate its desired token in an unfixed slot of that grade and swap them through their support union by ONE-incidence additions and deletions. Both exchanged full supports fit BOTH original floors. Each completed swap fixes another slot without moving previously fixed tokens; finite token misplacement decreases. Every completed tuple is an exact-q permutation; intermediate swap states lie in{q-1,q}. Save the full reverse C' to C*.

This accounts for shared floor capacities and ALL full tokens. A guard-only assignment with unplaced or floor-incompatible completion is not used. Original floor values are never permuted.

## 5. Renew protection, supply every primitive, terminate and restore

Construct the complete preliminary LOWER path A* to C':
- Hold source guard I fixed while repairing every J root to its actual C'_i.
- Once all J roots equal C', hold this installed destination guard fixed while repairing EVERY remaining root, including I, to C'.

In each root add missing destination labels in palette order, then delete old-only labels. Additions preserve the old original floor. Every deletion retains the FULL destination support meeting that slot's ORIGINAL floor. All labels are in the existing palette. Every unfinished root has a missing destination incidence, or, after additions finish, an old-only incidence. Thus the next legal primitive exists.

For every palette set K with |K|<=q-2, phase1 keeps an actual source guard witness in I disjoint from K unchanged, because I and J are disjoint. Phase2 keeps an installed actual destination guard witness in J unchanged. This checks ALL forbidden covers in the SAME current roots; pair systems are not treated as separate capacities.

The total symmetric difference from the full C' strictly decreases by one at each preliminary primitive. Both finite phase lists terminate; every root is exactly C'_i at the end. Protection is renewed BEFORE any source-guard root changes, and the installed destination guard protects the entire remaining sequence. It need not reset to exact q at the phase boundary.

The preliminary path may rise above q but maintains tau>=q-1. Apply baseline maximum-layer A ONLY to this complete finite lower path between actual exact-q endpoints A*,C'. Positive original floors and native union/addition closure satisfy its domain. It yields a finite band path with the SAME full labelled endpoints. No preliminary schedule or efficiency bound is asserted for the converted path.

Finally concatenate original A's exact preparation, the converted A* to C' path, saved M reverse C' to C*, and saved exact preparation reverse C* to ORIGINAL C. All joins are actual exact-q tuples, all pieces stay in{q-1,q}, and EVERY original labelled/noncompact destination incidence is restored. This proves X33R.

At every subsequent exact endpoint in the same carrier, the same grade totals derive another simultaneous good label. Compatible guard placement, eligible primitives and strictly decreasing progress are available again. This is guaranteed complete reusable repair, not one safe local exchange or completion of arbitrary safe inexact prefixes.

## 6. Two complementary capacities and nonvacuous strict extension

For original grades k-4/k-3, the positive capacities are4 and3. If both grades are present, b_low<=7 and b_high<=5, so sum b<=12<k whenever k>=13. If one grade is absent its bound is only7 or5 and the same conclusion holds. This proves X33T, including EVEN k. Triple-capacity/excess counting is not needed.

A nonvacuous infinite class beyond X31/X32's derived excess bounds comes from the accepted self-contained X29 constructor. For EVERY m>=4,k=2^m-1, it gives

ell0=k(k-1)(k-3)/24, f0=k(k-1)/6

with floors k-4/k-3, unique triple coverage and actual minimum four-cover H={e1,e2,e3,e1+e2}. For any integer d>=0 specify d additional ORIGINAL high-floor slots with duplicates of a selected existing high support. This defines a NEW FIXED carrier BEFORE any repair. Existing roots force tau>=4; all duplicate supports already meet H, so tau<=4. No native slot is added and no cloning-path equivalence is asserted.

X33T connects ALL exact endpoints on every such profile ell=ell0,f=f0+d, for arbitrarily large d. Taking d=k yields delta=d and epsilon=3d, so epsilon+3delta=6k>k-3. X32R's positive-redundancy hypothesis FAILS, and X31R's stricter epsilon+5delta bound also fails. This is an infinite extension of those sufficient structural domains. Individual endpoints might still satisfy older conditional bridges; their blanket failure is not asserted.

For the first m4 control, k15,ell105,f50,r155,floors11/12,S1755 and compact max degree M>=ceil(1755/15)=117. X14 whole-cap repair at q4 would need r>=2M+2>=236>155. X15N would require D<=r-M-1=37 and S<=15D<=555, impossible. Original grades are genuinely mixed, both floors exceed4, neither is automatic>=k-2, and palette-room k>=S fails. No general optimal guard count or all-profile feasibility classification is claimed.

The same construction with d0 overlaps older saturation results; that overlap is disclosed. The new theorem applies independently of constructor shape, number of duplicates, saturation, parity or repeated support patterns.

## 7. Consolidated discovery and inherited domains

X7 derived a small guard from a single UNIFORM incidence average. X23 supplied compatible access for a specified graded exact hub. X31/X32 derived LOW pair redundancy and installed patches in an odd two-grade excess class. X33 instead uses the SAME palette's simultaneous grade counts to derive an actual avoiding-label guard that fits into at most half of EVERY grade. Consequently TWO exact endpoint guards can be made disjoint with a FULL legal original-grade assignment, and protection can be completely renewed without any excess restriction.

The new statement removes uniform-floor dependence of the X7 alignment within the stated multi-grade count domain, and removes oddness/excess/redundancy/counting restrictions entirely for the k>=13 complementary4/3 target-four class. It does not solve every arbitrary mixed floor vector. sum b<k is sufficient; if it fails, the union estimate may be loose and a good label or another repair mechanism may still exist.

Read at analytical parentde679e8d1694d50d0001b75fe2e0f2f5bb0f31a9: live status/obligation, X7 full incidence guard proof, X23 graded access, X31/X32 complete arguments and their limitations. Baseline GUARD_BUFFER_CONNECTIVITY AB, OVERLAPPING_CLIQUE_EXCHANGE M and GENERAL_PARENT_CONNECTIVITY A at466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f apply only in the explicitly supplied actual guard, full assignment and exact-ended lower-path domains. X29's self-contained constructor supplies feasibility/H; X14/X15 cap domains are checked for the stated control. No frozen source is rewritten, recertified or treated as a new discovery.

Fresh independent WHOLE-ARGUMENT review must verify grade union count/rounding/strictness, c0 and absent grades, actual avoiding-label guard, independent source/destination label choices, full per-grade assignment and finite M reversal, shared capacities and ALL forbidden covers, eligible ONE-incidence moves/floors/palette/progress/renewal, actual exact ends before A, original noncompact labelled restoration, arbitrary d fixed-carrier feasibility and novelty, and inherited theorem domains.

Original A11 destination-directed scheduling, unrestricted remaining mixed/higher-target/nested and physical universality stay OPEN. Conditional child lifting retains exact-child/fixed-root-clearance interfaces. Ordered repair/retained recoverability; no fundamental time or imposed geometry. Unit repair is an upper bound, not a positive minimum at every endpoint pair.

Analytical packet only; no scientific enumeration/numerical test/workflow/run ID, implementation/benchmark or integration merge. A concrete separate v16.55 prospective protocol is an APPROVAL_PENDING proposal, not an executed campaign or certification. v16.55 remains OPEN until execution/reconstruction/rejecting-control/inherited replay/reproduction/exact review/actual merge/post-merge gates pass. Certified v16.54 and accepted efficiency baseline/design unchanged; runner execution/measured speedup unstarted.
