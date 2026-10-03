# A11.X10 — localized missing covers create stronger actual protection

Scope commit: 6a1af2372d4d077eafca899373395c128131179d.
Supplemental scope commit: 370387e13fd4673696d7d523de8546b71d64d934.
Parent publication: fe8085d006e8e8b6c24a5b70613eaf573bf518ed.
Integrated baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Candidate frozen for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. Carrier, result and boundaries

Fix a finite ordered palette P of size k and r labelled root slots. A root E_i is a subset of P meeting its original positive floor. A primitive toggles ONE incidence in ONE root while preserving that floor. Exact endpoints have transversal q. Put t=q-1. An actual t-guard is a subfamily of existing labelled roots with transversal at least t; selecting it changes no support.

Lemma X10L below applies to arbitrary positive floors and q>=3. The quantitative completion statements use UNIFORM original floor h>=2 and q>=4. Put

n=h+t-1, B=binomial(n,h), g=B-t+1.

A COMPLETE CORE at an endpoint means that for some S subset P with |S|=n, the endpoint contains an actual support equal to U for EVERY h-subset U of S. Select one distinct existing slot for each such support. Duplicate supports elsewhere are allowed. Containment of U in a larger root is insufficient.

**Lemma X10C.** Every exact-q endpoint containing this complete core has an actual t-guard on at most g=B-t+1 slots. This improves the X9 universal bound B-1 by t-2 under this openly stated additional hypothesis.

**Theorem X10.** For two exact-q endpoints, select actual endpoint guards of sizes m_A,m_C after exact compaction, using X10C where a complete core is present, X9G or X7G otherwise, or X10L when applicable. If r>=m_A+m_C-1, there is a finite native primitive path with tau in {q-1,q}, restoring EVERY original labelled destination support.

In particular:
- If BOTH endpoints contain a complete core, r>=2B-2t+1 suffices.
- If just ONE endpoint contains a complete core, the other can be ANY exact-q endpoint on the same carrier, and r>=2B-t-1 suffices, using its universal X9G guard.
- Smaller actual or incidence-derived guards can improve either sufficient budget further.

For h=3,q=4, B=10,t=3,g=8: both-core completion needs r>=15; one-core-to-arbitrary-destination completion needs r>=16. These are structural sufficient budgets. A single complete-core exact endpoint can serve as a hub: under the one-sided budget every endpoint connects to that hub, so every pair connects through it. Section 9 proves hub existence on every feasible sixteen-slot floor-three target-four carrier. Consequently the NEW universal floor-three target-four sufficient threshold is r>=16 across ALL feasible palettes, improving X9's seventeen. Universal closure at fifteen and sharpness remain unproved; no carrier campaign is performed.

No same distinguished slot or common label core is required at the two endpoints. Uniform floors license the FULL exact-endpoint permutation used below. X10 does not prove core existence or accessibility everywhere, a universal multiple-overlap handover, or original destination-directed scheduling.

## 2. General localization lemma: exactness supplies one actual replacement

Let E be exact q=t+1 and I an actual t-guard. Choose Q subset I with |Q|>=2 and let F be the roots indexed by I minus Q. Define the COMPLETE family of exposed small covers

D={K subset P : |K|<=t-1 and K meets every root in F},
U=union of all K in D.

The empty root family is hit by every K, including the empty set; use that convention here. We include ALL covers up to t-1, not just private covers chosen for individual removed roots.

**Lemma X10L.** If D is empty, I minus Q remains a t-guard. If D is nonempty and |U|<=t, an actual root E_b misses U, and

I'=(I minus Q) union {b}

is a t-guard of cardinality |I|-|Q|+1<|I|.

Proof. Exact q says that NO set of at most t labels hits the full endpoint. Hence |U|<=t supplies an existing root E_b disjoint from U. This uses exactness, not a new slot, spare capacity or a proposed auxiliary support. Every K in D misses E_b. If a set of at most t-1 labels hit I', it would belong to D and simultaneously hit E_b, a contradiction. Thus tau(I')>=t.

The slot b cannot belong to I minus Q: a K in the nonempty D hits every such root but misses E_b. It MAY belong to Q; being outside all of I is unnecessary. Consequently the claimed cardinality is exact. No incidences are edited, so all original floors and palette restrictions remain satisfied. When D is empty, its definition directly excludes every forbidden small cover of F. This proves the lemma.

At target four, D includes every exposed pair, singleton and empty cover. If their union fits within three labels, exact four supplies a single actual root missing them ALL. Protection is transferred at the level of guard selection; no simultaneous native move is being claimed.

## 3. Repeatable selection and its precisely limited obstruction

At a fixed exact endpoint one may repeat the following finite selection rule. First discard any one selected root whose deletion retains a t-guard. Otherwise inspect pairs Q of selected indices. If D is empty, discard the pair. If D is nonempty and |U|<=t, use X10L to replace the pair by an actual root missing U. Fix the finite supplied index/label orders to choose among eligible options and actual witnesses.

Whenever an eligible option exists its next selection is supplied by the lemma and strictly decreases the integer |I|. Exactness of the FULL endpoint is unchanged between selections because none of them edits a root. Therefore the same exactness argument can be reused. All guard selections stay actual, and the process terminates after finitely many reductions.

If it stops without reaching a desired size, its current guard is inclusion-minimal and EVERY pair Q exposes small covers whose union has at least t+1=q labels. Indeed an empty D or a union of size at most t would supply another eligible move. This is a rigorously characterized obstruction to THIS pair-localization reduction on THIS current selection.

It is NOT a proof that the guard has globally minimum cardinality, that other selections cannot be smaller, that groups larger than two cannot help, that a native path is blocked, or that arbitrary guards reach any proposed target size. No unconditional existence of an eligible pair is asserted. The progress measure is paired with next-selection existence exactly on the stated eligible domain.

## 4. Complete-core compression and all small-cover witnesses

Suppose the actual core roots are all h-subsets of S, |S|=h+t-1. Choose any t-subset H_0 of S. It hits every core root: S minus H_0 has only h-1 labels. Because E is exact t+1, some ACTUAL root F misses H_0. F is not a core root. Put d=F intersect S. Then d subset S minus H_0 and |d|<=h-1.

Choose an (h-1)-subset L of S containing d. There are exactly t core roots containing L, namely L union {x} for x in S minus L. Remove these t slots from the SELECTED guard, retain all other core roots, and add the existing root F. The resulting actual selection has

B-t+1=g

distinct slots. The endpoint itself has not changed.

For every K subset P with |K|<=t-1, we now exhibit an actual missed selected root.

If |K intersect S|<=t-2, W=S minus K has at least h+1 labels. Choose some ell in L, which exists since h>=2. If ell is outside W, any h-subset of W is a retained core root: it lacks ell and hence does not contain L. If ell belongs to W, choose an h-subset of W minus {ell}, possible because |W|-1>=h. Again it is retained. In either case this actual support lies in W and misses K. This handles outside-core labels as well as smaller sets.

Otherwise |K intersect S|=t-1, so |K|<=t-1 forces K to lie wholly in S and have size t-1. Its complementary core h-subset W=S minus K is the unique core support missing K. If W does not contain L it was retained and witnesses the miss. If it does contain L, then K misses L, hence misses d=F intersect S. Since K is wholly in S, it also misses all of F outside S. The actual root F supplies the witness.

Thus every forbidden small cover is excluded; tau of the selected guard is at least t. This proves X10C with legal actual roots and no capacity assumption.

Equivalently, after deleting the t core roots containing L, the exposed small covers are EXACTLY

K_x=S minus (L union {x}), x in S minus L.

Their union is S minus L, of size t (each label lies in another K_x since t>=2). The preceding argument proves completeness of this list, including absence of covers using outside-core labels. Lemma X10L therefore supplies the same compression directly, with U=S minus L and F disjoint from U. This is a fully characterized eligible group reduction, unlike the conditional stopping rule of Section 3.

For h=3,q=4, the omitted roots are the three triples L union {x}, where L is a core pair. The three exposed pairs are the pairs in the other three core labels. Their union has size three. The actual replacement F misses those three labels. Every other palette pair misses a retained core triple. This accounts for ALL pairs, not just total coverage counts or independent fictitious protection systems.

## 5. Exact compaction preserves the structural hypothesis

At any exact-q endpoint choose a minimum hitting set H, |H|=q. For each root retain an h-subset containing some label of H and delete other incidences individually. Existing complete-core roots already have exactly h labels, so they are left unchanged. Each is met by H because H hits the full tuple.

Every primitive deletion retains its original floor. Shrinking cannot decrease tau, and retained H gives tau<=q, so all compaction states are EXACT q. Whenever excess remains, an incidence outside the retained subset supplies an eligible next deletion; total excess decreases. The process is finite and its reverse restores the entire original endpoint.

Thus a complete core in the original endpoint remains in the compact exact endpoint. Apply X10C THERE, selecting its actual missing-H_0 root after compaction. No exact-endpoint lemma is invoked at level t. The proof also works directly before compaction, but the compact preparation permits the inherited uniform guard bounds and placement theorem to be combined.

At each endpoint choose the smallest supplied guard bound:
- g=B-t+1 if a complete core is available;
- B-1 from accepted X9G, for every uniform h>=2,q>=3 exact endpoint;
- N=floor(r*(k-h)/k) from accepted X7G;
- any smaller ACTUAL guard obtained by the eligible X10L selection rule.

X7G's availability is elementary: compact roots contribute hr incidences, so some label has degree at least ceil(hr/k). Its actual avoiding roots occupy at most r-ceil(hr/k)=N slots. A cover of them with at most q-2 labels, plus that label, would hit the full exact-q endpoint with at most q-1 labels. Thus they are a t-guard. We never replace actual availability by a bare bound without its hypotheses.

X9G is accepted at 31566452722b73d833250f1132a154883a73d60f and publication fe8085d006e8e8b6c24a5b70613eaf573bf518ed. Its classical uniform set-pairs equality dependency remains disclosed and unchanged; X10C itself requires NO external equality or near-extremal classification.

## 6. Full exact-endpoint placement, same-slot accounting

Write A*,C* for the compact exact endpoints and I,J_0 for their selected actual t-guards of sizes m_A,m_C. Under r>=m_A+m_C-1, at least m_C-1 slots lie outside I. Assign the destination guard tokens to outside slots first, using at most one slot in I; extend this assignment to a permutation of ALL r destination support tokens. Equal supports can remain distinct tokens.

Uniform ORIGINAL floor h makes the entire resulting tuple C** admissible and exact q. Accepted Lemma M in OVERLAPPING_CLIQUE_EXCHANGE gives a finite primitive band path from C* to C**. Save its reverse. This permutes full exact endpoints, not an unprotected bare t-guard.

For uniform floors every required support-token swap fits both destination slots. Processing unfixed destination slots, the needed token lies in an unfixed slot; swapping fixes that slot without moving a previously fixed one. Fixed-slot count strictly increases until the entire assignment is complete. Each individual swap uses expansions to the two-support union followed by contractions, preserving the band by Lemma M. Thus placement has actual eligible primitives and finite termination.

The resulting guard J has |I intersect J|<=1. Cores, qualifying slots and label triples may differ at the two endpoints. X5's same-slot prerequisite is neither assumed nor omitted: X5 is NOT invoked, and full exact-endpoint M supplies the slot alignment needed by O1 instead. Arbitrary mixed-floor slot permutations are not claimed.

## 7. Primitive handover, renewed progress and every pair

Define D on I union J by the source support on source-exclusive slots, the destination support on destination-exclusive slots, and their union at the shared slot s if present.

If there is no shared slot, D contains the source t-guard. If there is one, any K with |K|<=t-1 hitting all exclusive supports must miss A*_s (source guard) and C**_s (destination guard), and therefore misses their union. Hence tau(D)>=t. This is accepted O1 with its ACTUAL guard and overlap hypotheses established. At q=4 it witnesses every forbidden pair of labels, including core/core, core/outside and outside/outside.

The preliminary LOWER path is:
1. Hold source guard I fixed. For each destination-exclusive slot add missing destination incidences, then delete old-only incidences. I protects every edit.
2. If shared s exists, expand to A*_s union C**_s, then contract to C**_s. On I union J every current support is a subset of its corresponding D support. Any small K missed by a D support is still missed by its current subset, so the lower guard persists.
3. The destination guard J is now fully installed. Hold it fixed and repair every remaining slot by its individual union with its destination support.

Every addition contains the old h-support. Deletions begin only after the complete destination h-support is present and retain it. No palette label or slot is introduced. Each edit toggles exactly one incidence and preserves the original floor.

Within this middle schedule, the sum of all symmetric differences from C** decreases by ONE per primitive. An unfinished root supplies a missing destination incidence; once none is missing, any old-only incidence is an eligible deletion. The fixed phase order plus the respective guard proofs gives existence of each next edit, not merely a potential. There are finitely many incidences, so the schedule terminates at exactly C**.

Renewal is installation of the actual destination guard before the remaining old-guard roots are edited. It can retain tau=t, and supports ALL remaining repairs without further modification. No restoration to exact q after every individual handover is required. X10L's repeatable selections instead occur at the unchanged exact endpoint; these two uses of exactness are explicitly different. We do not claim a universal necessary multiple-overlap transfer.

## 8. Upper conversion and original endpoint restoration

The constructed middle path has tau>=t; it may exceed q. At uniform floor h every k-h+1 labels hit every root, so it has the finite preliminary upper bound k-h+1.

Apply accepted maximum-layer Theorem A in GENERAL_PARENT_CONNECTIVITY to this finite lower path between exact-q endpoints A*,C**. Both endpoints are exact, roots remain nonempty at original floors, and the carrier permits unions and arbitrary temporary incidences. Its finite upper-layer removal produces a native primitive path with tau in {q-1,q}. This conversion need not preserve the preliminary schedule or be efficient.

Concatenate source exact compaction, this converted middle path, reverse the saved full destination permutation, and reverse destination exact compaction. Every join is exact q and every primitive respects the band and original floors. The final tuple is the full ORIGINAL labelled destination C, including all noncompact supports. This proves Theorem X10 and both sufficient budgets.

The root result lifts only under baseline Section 7's accepted exact-child and fixed-root-clearance interfaces. It is not unconditional nested connectivity: a full native path may spend its defect inside a child. No root-level method obstruction is promoted to a nested barrier.

## 9. Existing core hub and universal floor-three target-four completion

**Hub corollary.** On any uniform-floor carrier admitting an exact-q complete-core endpoint E, the one-sided budget r>=2B-t-1 connects ALL exact-q endpoints. Apply Theorem X10 to A,E and E,C separately. The arbitrary endpoint guard is supplied by X9G, and E supplies its smaller core guard each time. Reverse a path if necessary: the primitive graph is undirected and both endpoints are exact. Concatenation joins at exact E; excursions cannot accumulate. Each full composition restores its specified labelled endpoint, so the second path starts at exactly the original hub, not merely a tuple with the same hitting number. No safe-prefix extension or independently assumed accessibility enters: the one-sided theorem CONSTRUCTS access from each endpoint to E.

**Theorem X10U.** Every pair of exact-four endpoints on a fixed finite ordered palette with uniform original floor three and r>=16 existing labelled root slots has a finite native primitive path with tau in {3,4}, restoring the full original labelled destination.

Proof. For r>=17 use accepted X9. At r=16, we explicitly construct a hub on any palette k>=7. Choose seven distinct existing palette labels 1,...,7. Put the ten triples on S={1,2,3,4,5} in ten slots, put {6,7,a} for each a in S in five other slots, and put a duplicate core triple in the last slot. Every root has size three and uses only existing slots and labels.

Any cover of the ten core triples needs at least three core labels: a set with at most two leaves at least three core labels, whose actual triple misses the set. A putative full cover of size at most three must therefore be exactly three core labels. Choose a in S outside that cover. The actual outer root {6,7,a} misses it, proving tau>=4. The four-set {1,2,3,6} hits all core and outer roots and their duplicate, proving tau=4. The hub contains the complete five-label triple core and hence has an actual three-guard on at most eight slots by X10C.

For k>7, the other labels simply occur in no hub support. Unused labels are permitted on the fixed native carrier; they cannot improve a hitting set. No palette is added or removed. The hub is therefore a legal exact-four endpoint on the SAME carrier as arbitrary A,C, irrespective of their incidence patterns or originally larger supports.

For k<=5, any k-2 labels hit every root of size at least three: their complement has size two. Thus tau<=k-2<=3 and exact four is infeasible. At k=6, each three-set K must be missed by an actual root, since exact four means K is not a cover. Its complement has size three, so the floor forces that root to equal P minus K. Different K require the twenty distinct triples, hence at least twenty slots. This elementary accepted X6 argument excludes k=6 at r=16 WITHOUT any enumeration or simulation. Thus every feasible sixteen-slot carrier has k>=7 and admits the constructed hub.

For h=3,q=4, B=10,t=3, the one-sided budget is 2B-t-1=16. Each arbitrary endpoint has a guard of at most nine roots by X9G, and the hub has one of at most eight; their sum is at most seventeen=r+1. Uniform exact-endpoint placement and O1 therefore supply each completed path to/from the hub. Concatenate at the exact labelled hub, then restore the original destination as in Section 8. This proves X10U.

The same construction has fifteen slots before duplication and shows nonvacuity of the two-core r>=15 statement. At k=8 one may keep label 8 unused, or change the a=5 outer support to {6,8,5} so all eight labels occur; the same lower/upper proof holds. For r=15,k=8, N=floor(15*5/8)=9, so X9's universal inequality requires seventeen and does not certify arbitrary endpoints there. X10's two-core statement is conditional at fifteen; it does NOT connect an arbitrary endpoint to that fifteen-slot hub because an arbitrary nine-root guard plus its eight-root guard need sixteen slots for the established O1 placement budget.

The scientific advance is the general actual-guard compression/localization mechanism plus its reusable EXACT-HUB composition. It removes assumed protection at a core endpoint and supplies access to an explicitly available hub from every endpoint under the one-sided budget. The sixteen-slot consequence is analytical universal coverage over every feasible palette and support tuple, not a finite passing-case count or execution campaign. The control is not asserted to be a previously unsolved particular pair; some pairs already satisfy X5 or symmetry criteria.

Other inherited domains remain separate:
- Floors one/two and target three results do not settle this uniform h=3,q=4 statement.
- q disjoint floor-safe witnesses require qh<=k; the control has 12>8.
- Palette-room requires k>=rh; the control has 8<45.
- Five-child target-four applies at r=5, not fifteen/sixteen.
- General floor-three cyclic complementary-triple classes have q=k-3; at k=8 this is five, not four.
- Saturated complementary capacity at q=4 requires r(k-h)=3k; here 75>24, so equality classification cannot be inferred.
- Safe symmetry exchanges connect symmetry-related endpoints; the ONE-SIDED theorem and exact-hub composition permit arbitrary endpoint incidence structure.
- O1 and old guard-buffer criteria already complete paths once suitably small ACTUAL guards are supplied. X10 supplies those guards for its structural class; it does not rebrand O1 as new or re-certify frozen sources.
- X5 still needs an actual triple-avoiding guard at BOTH endpoint entries in the same original floor-three slot. X10's one-sided result does not assume that destination availability and does not silently infer it from any anchor.

The complete-core hypothesis remains strong for endpoint-specific compression. It is NOT imposed on arbitrary input endpoints in X10U: Section 9 supplies a hub on every feasible sixteen-slot carrier and Theorem X10 supplies access. At seven labels, accepted incidence results and X10U leave r=14 as the possible universal carrier obligation before further accepted-class exclusions. For other palettes at r<16, the core hypothesis alone does not guarantee the placement budget or arbitrary access.

The general selection lemma identifies what exactness needs to supply replacement protection: localization of ALL exposed forbidden covers in at most t labels. The core construction proves localization and next-selection existence explicitly, removing a mere assumed small-guard availability at that endpoint. It does not prove this localization for arbitrary near-extremal guards, arbitrary core accessibility below the stated one-sided budget, or universal completion at r<16 for floor three and target four.

## 10. Review and consolidated next obligation

Fresh review must check general localization (all covers, outside-vs-removed slot, exact witness), finite repeatability and correctly limited stopping obstruction; every complete-core small-cover witness; minimum-cover-retaining exact compaction; one-sided bound arithmetic, explicit hub existence on every feasible sixteen-slot palette and full exact-hub composition; full exact destination permutation with uniform floors; O1 primitives, shared witnesses, eligible progress and renewal; maximum-layer applicability; and exact labelled/noncompact restoration.

Inherited dependencies are X9G (including its disclosed classical equality theorem) only for arbitrary-destination bound, X7G optionally, baseline O1/M/A and conditional child interfaces. No new external classification is introduced and frozen inherited sources are unchanged.

Next mathematical direction remains stronger derived actual guards or genuinely reusable necessary multiple-overlap handovers. Specifically, derive localization or another actual replacement criterion for guards NOT containing a complete core, sharpen the hub-access budget, or prove a renewable coupled handover when reducing the overlap to one is impossible. Below sixteen, a convenient hub is not accessible merely because it exists. Pair-localization termination with a large exposed union is only a method limitation, not disconnection or failure of other native repairs.

Original directed scheduling, mixed-floor placement, universal core accessibility outside the proved budget, unrestricted native/nested repair and quantitative efficiency remain open. No claim is made that every endpoint itself contains a complete core. This is ordered-repair/retained-recoverability mathematics, not fundamental time, a physical law, a new implementation certification or an originality assertion. No scientific runs, workflows, tests, numerical campaign, new numbered version or certified integration merge exist for this checkpoint.

