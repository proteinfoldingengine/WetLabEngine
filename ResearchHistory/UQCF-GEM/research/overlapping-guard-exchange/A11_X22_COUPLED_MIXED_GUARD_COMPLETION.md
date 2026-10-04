# A11.X22 — coupled mixed-slot guard placement and weighted completion

Scope: d518fbda367f7a2a12ba6737221734d98b239919.
Parent analytical publication: 6a382d5a344302e524a53f1026a62e6b02f4bc28.
Certified baseline:466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Frozen candidate for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. Statements and original native rules

Fix a finite ordered palette P, k=|P|, r labelled original slots and ORIGINAL floors a_i in{3,4}. Supports may be larger than their floors. Each primitive adds or removes ONE incidence in ONE existing root and retains its own original floor. Temporary incidences, background edits and repeated toggles remain allowed. Endpoint hitting number is EXACT FOUR.

**Theorem X22U (mixed-three/four closure above ten labels).** EVERY exact-four endpoint pair on EVERY original mixed-three/four carrier with k>=11 has a finite native path with tau in{3,4}, restoring EVERY original labelled/noncompact destination support, at ANY root count for which exact endpoints exist.

This removes the residual small-arity restriction from X21's eleven/twelve-label mixed class. It is connectivity, not feasibility of every profile; the defect unit is an upper bound, not a positive minimum for every pair.

**Theorem X22S (six-slot mixed completion).** At r=6, EVERY exact-four pair with original floors in{3,4} has complete native{3,4} repair at EVERY finite palette. Such endpoints necessarily have S=sum a_i<=2k. The necessary budget is derived from actual endpoint constraints, not assumed.

**Lemma X22P (coupled placement of small guard tokens).** Suppose there are at least two original floor-three slots and an exact-four full hub Q has exactly two support tokens of size3, all others of size4. Suppose its actual three-guard consists of those two small tokens and one size4 token. Let E* be an exact original-floor compaction and let x occur in a floor-three support and in at least one other support. Then E* has complete native{3,4} repair to the SAME full labelled Q. The actual avoiding-x guard supplies protection and its complementary occupied slots supply a compatible placement with at most one overlap. No arbitrary mixed compact permutation is assumed.

**Theorem X22D (shared low incidence or private modules).** At r=7 and k11 or12, every exact-four mixed-three/four endpoint can reach a SAME exact full hub by one of two supplied complete constructions. A shared floor-three incidence supplies X22P when at least two such slots exist. Otherwise the exact compact low-floor roots are disjoint private modules; the remaining exact-two obligation supplies a complete alternative repair. The sole floor-three case has its own compatible placement or degree renewal.

**Lemma X22B (weighted completion on actual disjoint roots).** A general necessary inequality for actual disjoint roots is given in Section2. It incorporates unequal block sizes, original root floors and the available OUTSIDE label budget. This extends the exhausted-palette count of accepted X13B; it is an endpoint completion restriction, not native disconnection or an existence theorem at equality.

**Corollary X22L.** At k>=11, complete target-four repair holds whenever each ORIGINAL floor is at most4 OR at least k-2, with arbitrarily many large-floor slots and exact original restoration.

Uniform-floor-three/four universal root closures remain accepted. Unrestricted mixed profiles on seven through ten labels, general higher original floors/targets, original A11 destination-directed universality and unrestricted nested repair remain open outside accepted classes.

## 2. Weighted actual completion with outside labels

Consider ANY family on a fixed palette containing t>=2 ACTUAL pairwise-disjoint nonempty roots U_1,...,U_t. Let n_j=|U_j| and w=k-sum_j n_j, the number of existing palette labels OUTSIDE their union. Other actual roots A_i have original lower bounds a_i. Suppose the full transversal is at least t+1.

There are N=product_j n_j distinct t-label sets choosing one label from each U_j. Every such set hits all the U_j, so exact protection requires it to miss at least one OTHER actual root.

For each other root put c_ij=|A_i intersect U_j|. The number of those t-sets missing A_i is EXACTLY

product_j (n_j-c_ij).

Because at most w of its incidences can lie outside the block union,

sum_j c_ij >= max(0,a_i-w).

Define the finite analytical bound

B(n_1,...,n_t;l)=max { product_j(n_j-c_j) : 0<=c_j<=n_j integers, sum_j c_j>=l }.

If l>sum n_j the root cannot exist. Otherwise completion necessarily satisfies

product_j n_j <= sum_i B(n_1,...,n_t;max(0,a_i-w)).

Indeed the union of the actual missed-choice sets must contain all N choices; its size is at most the sum of their actual sizes, and each size is bounded by B. Shared blocking obligations are counted in the SAME actual supports. This is not a claim the maximizing missed sets can be independently realized or that equality suffices for a construction. A violating inequality proves only endpoint infeasibility under the supplied actual disjoint roots/floors/palette.

No finite scientific computation is executed in defining B; it is a mathematical maximum. An explicit bound is available without enumeration: for equal block sizes h and l<=th, arithmetic-geometric mean gives B<= (h-l/t)^t. This is the elementary counting mechanism inherited from X13B, now accounting for OUTSIDE labels and each root's own floor.

In particular for three disjoint triples and w=1, any additional floor-four support has at least3 incidences in their union. Its missed-choice count is at most

((9-3)/3)^3=8.

There are27 colourful triple choices, so THREE such actual roots cannot block them all: their total missed-choice count is at most24<27. This fact will exclude a six-slot saturated endpoint pattern. It does not exclude another carrier/path or infer disconnection.

## 3. Native exact compaction and avoiding guards

At any original exact-four endpoint E choose a minimum four-label cover H. In each original slot retain a_i labels including a label of H that meets that root. Delete excess incidences one by one.

Every deletion preserves the original floor and retained H; deletion cannot lower hitting number, so every intermediate remains EXACT FOUR. An excess incidence supplies the next deletion whenever unfinished. Finite total excess decreases and the saved reverse restores every original support.

Write E* for the exact floor-size tuple and S=sum a_i for its incidence count. At exact four, any label x of degree d has an actual avoiding-root family requiring at least three hitting labels: adding x to a two-cover of that family would give a full three-cover.

With r=6 this also forces d<=3 because x plus one label from each avoiding root is a cover of size at most7-d. If d=3, the three actual avoiding roots must be pairwise disjoint; an intersection would allow two labels to hit them all. All their labels lie outside x. These exact endpoint facts are not assumed at inexact repair prefixes.

## 4. Six-slot mixed budget is forced, then renewed repair completes

Let f be the number of ORIGINAL floor-four slots at r6. Exact compaction has S=18+f.

We prove that a feasible exact-four compact tuple cannot have S>2k.

For k<=9, degree three is impossible: its three avoiding roots each have size at least3 and would need at least9 labels outside x. Thus all degrees are<=2 and S<=2k. This proves the necessary inequality, and in particular excludes any profile with S>2k in that palette range. At k9 with f0 the inequality is equality; inherited X13 supplies its stronger uniform infeasibility result, which is preserved, not needed for the conditional repair conclusion.

For k10, S>2k means f>=3. Compact incidence then forces some degree-three label x. Its three avoiding roots are disjoint on at most9 labels; if any were floor4 their sizes would total at least10, impossible outside x. Hence all three are floor3, and every floor4 root contains x. There are only three slots containing x, so f<=3. Consequently f=3, the avoiding roots are THREE DISJOINT TRIPLES exhausting P minus{x}, and the other three roots are floor4.

Section2 has w=1 and shows those three actual floor-four roots miss at most24 of27 colourful triples. Some three-label set therefore hits ALL six roots, contradicting exact four. Thus S>2k is impossible at k10.

For k11, S>2k means f>=5 and again forces a degree-three x. Its three disjoint avoiding roots have total size9+g, where g is their number of floor-four slots. Since they lie in10 labels, g<=1. Thus at least f-1>=4 floor-four roots contain x, contradicting d=3. S>2k is impossible.

For k>=12, S<=24<=2k directly. These cases exhaust every palette and prove S<=2k whenever exact endpoints exist.

Now compact both exact endpoints to their original floor sizes. Their maximum degree is at most M3. Use accepted X15N with D2:
D<=M; S<=Dk; r6>=D+M+1=6.
If S=Dk, its additional saturated inequality is r6>=2D+2=6. Thus both strict and saturated cases are legally supplied.

Protected leveling uses an above-two donor, below-two recipient and an actual containing/missing root whenever excess remains. A pair containing the added recipient meets at most D+M=5<6 roots; every other pair retains its old actual witness. Add-before-delete preserves each original floor; excess degree decreases.

The strict degree-class construction restores any borrowed cycle-row or OUTSIDE-row incidence. Saturation uses a single temporarily degree-three label and a travelling hole; every pair hits at most2D+1=5<6 actual roots. Pending surplus/deficit balance supplies the next greedy move or cycle whenever unfinished. Finite macro progress and restoration renew the same structure for subsequent exchanges.

Internal entries can have level three. Invoke only the explicit LOWER constructions there; reverse saved destination leveling and original compaction to join the ORIGINAL exact endpoints, THEN apply maximum-layer A to the full lower path. The result restores every original labelled/noncompact destination at the original mixed floors. This proves X22S for all palettes.

This is a weighted endpoint completion argument coupled to a general accepted renewal lemma, not isolated numerical campaigns at k10/k11.

## 5. Coupled small-token placement supplies actual protection

Prove X22P. Let L be the set of ORIGINAL floor-three slots, |L|>=2. At exact E*, let x belong to some low-floor root and another root. Its actual degree d>=2. Let I be ALL roots avoiding x and O be their complement, so |O|=d>=2 and O contains a low-floor slot.

The target actual guard has TWO size3 tokens and ONE size4 token. Construct its assignment jointly:
- If O contains at least two low-floor slots, put both small guard tokens in two such slots. Put the size4 guard token in any other slot. If no outside slot remains, that third guard token lies in I, so there is only ONE overlap.
- If O contains exactly one low-floor slot j, put one small guard token there. Some other O slot exists and has original floor4; put the size4 guard token there. Put the second small token in any other low-floor slot, which necessarily lies in I. Again the overlap is ONE.

Thus the actual guard can be assigned with |I intersect J|<=1 while EVERY guard token fits its assigned ORIGINAL floor. The two small tokens have used distinct low slots. ALL remaining tokens have size4 and fit every remaining slot, so the assignment extends to a full admissible permutation of Q.

This is a coupled support/slot assignment, not three independent guard capacities. It specifically allows a small token to use the single protected overlap when the outside low-floor capacity is only one.

Baseline M supplies a FULL exact-four path from Q to this permuted Q', processing decreasing original floors with its eligible token-fixing swaps. The final assignment is legal, so every swap fits both floors. Each swap expands to the union and contracts to the new exact supports, preserving tau in{3,4}; fixed slots increase, guaranteeing termination. Save the full reverse to the original labelled Q.

Actual O1 supplies the LOWER route E*->Q'. For every palette pair hitting all source/destination exclusive guard supports, the two actual guard inequalities force it to miss both endpoint supports at the shared slot, hence their union. Otherwise an exclusive root supplies the missed-pair witness. The unchanged source guard protects installation, the comparison family protects the shared union and the installed destination guard protects repair of all remaining roots.

Add missing destination incidences before deleting old-only incidences. Additions retain the original support; deletions retain the complete destination in the same slot. Each is a legal single incidence, every unfinished root supplies the next edit, and scheduled symmetric difference decreases. At the deficient handover boundary the destination guard is already reusable; exact-four resetting is unnecessary.

Apply A only to the finite lower path between exact E*,Q', then append the saved FULL permutation reverse to Q. Prefix the exact source compaction. This restores the same FULL labelled hub. Reversing a second complete endpoint leg restores every original destination support. These supplied next edits/progress/renewal/restoration establish X22P, not just a safe placement.

## 6. Seven-slot exact hub with two private triples

For r7,k11 or12 and at least TWO original low-floor slots, choose two distinguished slots in L ONCE for the fixed carrier. Put private disjoint triples U,V there. Choose an existing five-label core S_0 disjoint from U union V; this uses11 labels. In the other five slots put ALL four-subsets of S_0.

Every size4 token meets its original floor3 or4; the private triples are assigned to original floor3 slots. The core requires two labels, U and V one each, so the full hub Q is EXACT FOUR. Supply two core labels and one from each private triple as a minimum four-cover.

ONE core support and U,V are an actual THREE-root guard: three disjoint supports require three hitting labels. Every palette pair misses one of them, including unused palette labels. The full tuple has exactly two size3 tokens and five size4 tokens, so Section5 applies whenever the input has a shared low-floor incidence.

The hub is legal on the mixed ORIGINAL profile. We do not strengthen the private triples to four or assume the uniform-floor-four target carrier is feasible. This is the narrower mixed alternative to X21's all-token maximum-floor construction.

## 7. No shared low incidence forces a complete private-module alternative

Take an exact floor compaction E* at r7,k11/12 with at least two low-floor slots, and suppose EVERY label in a low-floor support has global degree ONE.

Then all those actual triples are mutually disjoint and disjoint from EVERY high-floor support. For a genuine mixed profile there is at least one floor-four slot, whose support needs4 labels outside their union. With n=|L| low slots we therefore have

3n+4<=k<=12,

so n<=2. Since n>=2, n=2 exactly. This implication is actual structural protection, not a convenient input normal form assumed reachable.

The two private triples each require one hitting label independently. The remaining five high-floor roots lie in their complementary palette R of size k-6. The full tuple is exact four, so this high-root family is EXACT TWO. Its original floors are all4 and its supports are exactly4 in the compaction. In particular |R|>=5; otherwise every four-support on at most4 labels would be identical and have transversal one.

Globally permute EXISTING palette labels to send the two ordered private triples to the fixed U,V of Section6. Extend the mapping to the full palette. Baseline L implements this full exact-four permutation by native transpositions with tau in{3,4}, preserving every original slot/floor. Completed permutations are exact four. Save its reverse. All high roots now lie in the SAME complementary palette R_0=P minus(U union V).

The target Q high family is the five4-subsets of the fixed S_0 subset R_0 and is also EXACT TWO. Connect the actual high family to it through its individual componentwise unions, first performing ALL missing target additions, then ALL old-only deletions.

During all additions the high tuple contains its exact-two source family, so its hitting number is at most TWO. During all deletions it contains its exact-two destination, again at most TWO. Positive original floors give the lower bound ONE throughout. Additions retain old floor4 supports and deletions retain destination floor4 supports. Every incidence is in R_0.

Because U,V remain unchanged and disjoint from every high intermediate, FULL transversal is exactly

2+tau(high family) in{3,4}.

This is a directly bounded path; no premature exact-four theorem is applied to a deficient high intermediate and no upper conversion is needed for this segment. Every missing/excess incidence is an eligible next edit in the stated phase, and finite symmetric difference decreases.

The endpoint is the SAME original labelled Q from Section6. Combine with the saved exact source preparations; the reversed destination leg restores every original full support. The private-module alternative proves complete repair when the shared-low-incidence route is unavailable. No root is removed from the native carrier; the high-family moves operate in their existing slots while the actual private roots supply the other two obligations.

Uniform floor3/floor4 profiles are already closed by X15/X20. The private-case argument applies only to genuine mixed profiles. A uniform low profile cannot be classified by the presence of a nonexistent high root.

## 8. A sole low-floor slot has its own valid mechanism

At r7,k11/12, suppose there is exactly ONE floor-three slot s and six original floor-four slots.

For k12, form a full hub using all five4-subsets of a five-label core, a disjoint private TRIPLE in s and a disjoint private FOUR-support in another slot. It uses5+3+4=12 existing labels. All supports fit their original slots and the full transversal is2+1+1=4. One core support and the two private roots form an actual three-guard. The ONLY size3 token belongs to slot s.

Input exact compaction has S27, so an actual label has degree d>=ceil(27/12)=3. Its actual avoiding-root guard is I. There are at least THREE outside slots. Put the small private token in its fixed original slot s. At least TWO outside slots remain after excluding s, whether s was outside or inside; put the other two size4 guard tokens there. All other size4 tokens fit all remaining slots, so extend to a full legal permutation.

The guard overlaps I in at most the slot s. M/O1/A, eligible next edits, renewed guard and saved reverse FULL hub permutation apply exactly as in Section5. Both endpoint legs reach this SAME full Q and restore the original exact destination. The small token is never illegally moved to a floor-four slot.

For k11, every actual label-avoiding family is a three-guard on at most10 labels. If it had only three roots, they would be pairwise disjoint. Their ORIGINAL floors total at least3+4+4=11 (or12 if s is absent), impossible on10 labels. Hence every avoiding family has at least four roots and every exact endpoint degree is at most r-4=3.

Exact original compactions have M3,S27. Accepted X15N with D3 applies:
r7>=D+M+1=7 and S27<3k33.
The strict-slack incidence renewal supplies actual pair witnesses (at most6<7 roots hit), eligible cycles/restored buffers and finite macro progress. Only the completed original exact endpoint lower path is converted by A, restoring every original labelled/noncompact support. No mixed permutation is used in this branch.

These branches plus Sections6-7 establish X22D for EVERY seven-slot genuine mixed profile on eleven/twelve labels.

## 9. Whole-domain composition and large-root lift

For original a_i in{3,4} and k>=11:
- k>=13, EVERY root count is already accepted X21M.
- k11/12,r>=8 is accepted X21M, including the uniform-three arithmetic exception.
- r7 is X22D for genuine mixed profiles, and accepted X15/X20 for uniform profiles.
- r6 is X22S at every palette.
- r5 is baseline F for arbitrary positive original floors, including saturation.
- r4 exact four forces all four roots pairwise disjoint, so baseline protected J applies at the original mixed floors.
- r<4 cannot admit exact four because one label per nonempty root is a cover.

These branches exhaust EVERY root count and prove X22U. It is not asserted that every branch has feasible endpoints. Existing frozen uniform infeasibility/results are unchanged.

For X22L, retain slots of original floor below k-2. At k>=11 the stated profile makes their floors1..4. Full exactness forces retained exact-four endpoints: a retained cover of at most three can be padded to three and meets every held large root, contradicting full exactness. If the retained family is empty full exact four is impossible.

Retained floor1 invokes accepted X3; floor2 invokes accepted X4; otherwise retained3/4 invokes X22U at ANY retained root count. Accepted X17's positive lift holds the large roots fixed while retained actual witnesses supply every forbidden pair. A retained minimum cover of size3/4 hits every large root, so full and retained hitting numbers agree throughout.

After exact retained restoration, each large root is repaired through its own union with its ORIGINAL destination, with additions before deletions. Its original floor>=k-2 meets every three-label set; retained exact four supplies the lower four bound and its minimum cover supplies the upper four bound. Missing/excess incidence progress terminates at EVERY original support at full exact four.

No high-floor coordinate is natively deleted, no arbitrary mixed floor permutation occurs, and no converse projection or negative obstruction is inferred. X22L has no whole-carrier incidence budget.

## 10. Discovery, review scope and precise limits

This analytical loop has two interacting advances. Weighted completion derives access to accepted renewable degree classes from actual endpoint constraints. Coupled placement uses the actual shared low incidence to decide WHERE small guard supports legally fit; when that incidence is absent, exactness forces isolated modules that themselves carry a complete alternative repair.

Thus absence of the preferred guard-access resource does not end the argument. It can force a different reusable structure. Both constructions supply the next primitive whenever unfinished and restore the exact full destination. The seven-slot dichotomy does not assume a special input core or clone/compaction preservation.

Fresh whole-argument review must check weighted counting's outside budget and shared obligations; all exact-compaction minimum covers; six-slot S<=2k proof including the cube case and X15 saturation; the two small-token placement branches and extension to a legal full M assignment; actual O1 witnesses; private-module forced classification and global L legality; exact-two high union path/full hitting-number sum; the sole-low case; exact endpoint inputs to A; termination, renewed structure and same full labelled Q; whole k>=11 composition and X17 positive lift.

Accepted domains used: baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f GENERAL_PARENT_CONNECTIVITY A/F and exact compaction, OVERLAPPING_CLIQUE_EXCHANGE M/L, PROTECTED_EXCHANGE J; parent6a382d5a344302e524a53f1026a62e6b02f4bc28 GUARD_HANDOVER O1, X13B completion counting, X15 strict/saturated LOWER renewal and leveling, X17 lift, X20 uniform closure and X21 broad mixed closure. Sources/reviews are read for applicability and stay frozen, not rewritten or recertified.

X21's compatibility idea is extended to hubs with TWO small tokens, where arbitrary assignment would be illegal. Whole-argument acceptance covers these stated analytical classes only. General mixed-three/four at k7..10, other mixed/higher-floor/higher-target profiles outside accepted sufficient classes, A11 stricter destination-directed universality and unrestricted nested repair remain OPEN. k<=6 arbitrary positive floors are already covered by X17. Some remaining tuples are already solved by other accepted criteria; this is not a checklist of isolated campaigns or a no-path claim.

Conditional native nested lifting still requires inherited exact-child interfaces and fixed-root clearance. A unit defect upper bound does not establish a positive barrier minimum for every pair. No physical metric/energy/gravity, fundamental time, inserted geometry or originality claim.

No numerical enumeration, scientific test/workflow/run ID, implementation, benchmark, numbered v16.55 certification or integration merge. The corrected user target is v16.55; this loop attempts its mathematical closure but does NOT substitute analytical review for that version's execution/reproduction/merge audit requirements. Certified v16.54 and the separately accepted efficiency design remain unchanged; runner execution/measured speedup remain unstarted.
