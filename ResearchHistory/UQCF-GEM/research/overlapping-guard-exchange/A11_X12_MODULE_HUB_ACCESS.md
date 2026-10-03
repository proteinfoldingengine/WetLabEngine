# A11.X12 — incidence-selected protection reaches minimal-guard module hubs

Scope commit: 21f0a707fe1d52a335539b53b9bc39e4c2ff0de3.
Parent analytical publication: 731a2a636a49ec89cda3e6e3f290100ce9418f85.
Certified integrated baseline: 466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f.
Candidate frozen for fresh independent WHOLE-ARGUMENT review. Analytical only.

## 1. Native statements and exact result

Fix a finite ordered palette P of k labels, r labelled slots and uniform ORIGINAL floor h>=2. Every root is any subset of P of size at least h. A primitive toggles ONE incidence in ONE root while preserving that floor. Larger intermediate supports, temporary incidences and repeated toggles are permitted. Endpoints have transversal EXACTLY FOUR.

A three-guard is an ACTUAL selected subfamily requiring at least three hitting labels. Selecting roots edits no support. A full exact-four hub Q is a specified admissible tuple on the SAME carrier, not an assumed canonical destination.

**Lemma X12A (incidence-to-hub access).** Suppose a specified exact-four hub fits in r slots and has an actual three-guard on m slots. After exact compaction of an arbitrary endpoint E, let d be a maximum label degree. If d>=m-1, then E has a finite native primitive path to the original full labelled hub with tau in {3,4}. Every endpoint satisfying that inequality therefore connects to every other such endpoint via that exact hub. The uniform sufficient condition is ceil(hr/k)>=m-1.

**Theorem X12W (minimal-guard wide-palette access).** For uniform h>=2, every exact-four endpoint pair is connected with full labelled/noncompact restoration whenever

r>=h+3 and k>=3h+1.

The proof supplies a hub with the MINIMUM possible three-root guard. If k<hr, actual incidence forces the degree needed for access. If k>=hr, accepted palette-room AE supplies the route. No classical equality or design bound is required.

**Theorem X12D (two-core degree access).** For uniform h>=2, the same conclusion holds if

r>=2h+2, k>=2h+2 and ceil(hr/k)>=h+1.

The two-core exact hub has an actual three-guard on h+2 roots. This is a derived sufficient domain, not a claim that all endpoints have that shape.

**Theorem X12U (universal large-r floor-three repair).** For original floor three, every exact-four pair on EVERY feasible finite palette has complete native {3,4} repair when r>=10. This improves X11's all-palette sufficient threshold fourteen.

**Additional floor-three coverage.** All feasible k>=10 carriers are covered at EVERY r, including smaller r via inherited results. At k=8,r>=9, and k=9,r>=10, all exact endpoint pairs are covered. The previously solved seven-label classes remain covered.

The only possible remaining uniform-floor-three exact-four carriers, BEFORE other accepted-class exclusions, have eight or nine labels and at most nine roots; at eight labels at most eight roots. Because r<=5 is inherited or infeasible, the possible small ranges start at r=6. This is a consequence of general protection/access mechanisms, not an instruction for isolated campaigns or proof of disconnection. Universal original directed scheduling, mixed-floor placement and unrestricted nested universality remain OPEN.

## 2. Exact compaction and actual avoiding-root protection

At exact-four endpoint E choose a minimum four-label hitting set H. In each root retain an h-subset containing a label of H. Delete every other incidence individually. Each deletion retains the original floor, cannot lower transversal by monotonicity and retains H as a cover; hence EVERY primitive remains exact four.

Whenever excess remains, a label outside the retained subset is an eligible next deletion. Total excess decreases and the finite process ends at E*. Its reverse restores every original incidence and labelled support. Compact any chosen hub in the same manner and save its reverse. Shrinking its selected guard roots cannot weaken their lower transversal; original slot count is unchanged.

The compact endpoint has hr incidences. Some actual palette label x has degree d>=ceil(hr/k). Let I be ALL its avoiding roots, exactly r-d existing slots. If at most two labels covered I, those labels together with x would cover E* using at most three labels, contradicting exact four. Therefore I is an ACTUAL three-guard.

This degree count does not assert that a deficient label is automatically a safe buffer after arbitrary edits. It supplies a particular actual subfamily at an EXACT endpoint and measures how many existing slots remain for placement. No local coverage count substitutes for the missing-root witness inequality.

An exact-four tuple also has d<=r-3: x plus one label from each avoiding root is a cover of size at most1+r-d. This is consistent with nonempty three-guard availability. None of these exact-endpoint implications is reused at an arbitrary inexact prefix.

## 3. General actual-guard access lemma and full slot alignment

We first state the precise inherited composition with all hypotheses furnished.

Let E,Q be exact-four endpoints on uniform original floor h, with actual three-guards of sizes a,m. If

r>=a+m-1,

complete native {3,4} repair from E to Q is possible. Compact both endpoints exactly as in Section 2; guard roots stay actual and their transversal cannot decrease.

Write I for the compact source guard and J_0 for the compact destination guard. At least m-1 existing slots lie outside I. Place the destination guard tokens there first, using at most ONE slot in I, and extend the assignment to a permutation of ALL r destination support tokens. The resulting tuple Q** is admissible and exact four because every original floor is the same h.

Accepted Lemma M in OVERLAPPING_CLIQUE_EXCHANGE supplies a finite primitive {3,4} path from compact Q* to Q**; save its reverse. This is a full EXACT endpoint permutation, not an edit primitive and not a permutation of an unprotected bare level-three guard. Equal supports can remain distinct tokens.

The eligible swap is supplied explicitly by M: at an unfinished destination slot, its desired token is in an unfixed slot. Uniform floor h makes both supports fit the swapped destinations. Expand each to their union and contract to the swapped supports through individual incidence toggles. Completed swaps fix a destination and move no previously fixed slot, so the number of fixed destinations strictly increases to finite completion.

Write J for the placed guard. Then |I intersect J|<=1. Neither X5's same-slot condition nor a shared module/core pattern is assumed. Arbitrary mixed-floor slot reassignment is not licensed.

## 4. Every pair witness, primitive handover and renewed progress

On I union J define a comparison family D: source support at source-exclusive slots, destination support at destination-exclusive slots, and the union of source/destination supports at the possible shared slot s.

If the guards are disjoint, D contains the source three-guard. If they share s, any set K of at most two labels meeting all exclusive supports must miss the source support at s, or it would hit the source guard. It must likewise miss the destination support at s. Thus it misses their union. Consequently tau(D)>=3.

This is accepted O1 with actual guards and at most one shared index. It covers EVERY palette pair, singleton and empty set, including labels outside a hub's active modules. The roots supplying protection are actual labelled roots, not independent fictitious capacity systems.

The preliminary LOWER path is:
1. Hold I fixed. For each destination-exclusive slot add missing destination incidences, then delete old-only incidences.
2. If s exists, expand its source root to its union with its destination, then contract to that destination. Every support on I union J is a subset of its corresponding D support. Any small set missed by a D support remains missed by its current subset, so the lower guard holds throughout.
3. The full destination guard J is installed. Hold it fixed while repairing ALL remaining roots to Q** through their individual unions.

Every addition retains the old floor-safe root. Deletions start only after the complete destination support is present and retain it. Each primitive is one incidence in one existing slot, using only original palette labels.

At each unfinished scheduled root there is either a missing destination incidence, eligible for addition under the phase's guard, or an old-only incidence, eligible for deletion while retaining the complete destination. The sum of symmetric differences from Q** decreases by one per primitive. There are finitely many incidences and phases, so the supplied next-move rule terminates at the EXACT full Q**.

Renewal is installation of the actual destination guard BEFORE editing the remaining old-guard roots. The full tuple may still be at level three; exact four need not reset after each handover. The installed guard supports all subsequent edits without modification. This is the accepted one-overlap mechanism with newly derived availability, not a universal necessary multiple-overlap theorem.

## 5. Upper removal, exact labelled hub return and repeatability

The preceding schedule keeps tau>=3 and may rise above four. At uniform floor h any k-h+1 labels hit every root, so it has finite preliminary upper bound k-h+1.

Apply accepted maximum-layer Theorem A to this ACTUAL finite lower path between exact-four endpoints E*,Q**. The original carrier has nonempty roots, fixed original floors, arbitrary additions/unions and no new label/slot. The theorem gives a finite primitive path with tau in {3,4}. Its finite layer-removal progress is inherited; no efficiency or preservation of the preliminary schedule is asserted.

Concatenate source exact compaction, converted middle path, reversed full destination permutation and reversed destination exact compaction. All joins are exact four. The endpoint is EXACTLY the original full labelled Q, including larger original supports and duplicate-slot tokens. Thus the general actual-guard lemma restores a precise original tuple, not just its hitting number.

For any two endpoints A,C satisfying access to Q, construct the two COMPLETE paths A->Q and C->Q. Reverse the second and join at the same original exact-four labelled Q. Primitive moves are undirected, so reversal preserves floors and the band. Deficits do not accumulate at an exact join. This reaches every original labelled/noncompact support of C.

The same full hub return allows reuse for any finite chain of exact endpoints in the proved class. Arbitrary safe-prefix completion is not inferred; each leg is a supplied complete construction with available next edits.

For incidence access, a=r-d. The guard-sum condition is

r>=r-d+m-1 iff d>=m-1.

Together with Section 2's actual guard and the completed chain above, this proves X12A. The condition ceil(hr/k)>=m-1 guarantees it for every endpoint, but larger actual degrees can improve a specific pair.

## 6. Minimal three-root guard hub without four disjoint witnesses

Choose h+1 existing labels for a core S, and two other disjoint h-label blocks U,V, all three label sets mutually disjoint. This needs exactly3h+1 labels, available under Theorem X12W.

Use ALL h-subsets of S as roots (h+1 supports), then U and V in two more existing slots. Thus the hub uses h+3 slots. Fill additional existing slots with duplicates of a chosen core root; no new cover obligation is introduced.

The complete core has transversal TWO: any singleton s in S misses the actual support S minus {s}, while any two distinct core labels meet every h-subset because such a support misses only one core label. A label outside S cannot hit any core root. Each block U,V independently requires one hitting label. Disjointness of their palettes proves additivity, so the full hub has transversal2+1+1=4.

Choose two core labels, one label in U and one in V to supply an actual minimum four-cover. All roots have size h and ORIGINAL floor h; extra palette labels can remain unused legally. Every forbidden set with at most three labels fails to meet one of these disjoint module requirements.

Choose ONE core support plus roots U,V as the hub guard. They are three disjoint nonempty supports and require exactly three hitting labels, so m=3. This is the MINIMUM possible number of guard roots: choosing one label per nonempty root always gives a cover, so a subfamily on fewer than three roots cannot require three labels.

The hub's three disjoint GUARD roots do not mean the exact endpoint has four disjoint roots. The core itself requires two labels through overlapping supports. At3h+1<=k<4h, FOUR floor-safe disjoint roots cannot exist anywhere, but this hub and its three-root guard are legal.

If k<hr, compact incidence count forces some label degree at least two: otherwise hr incidences could occupy at most k distinct labels. X12A with m=3 requires exactly d>=2 and supplies complete access from every endpoint to this exact hub. Thus the argument constructs accessibility and does not assume it from the hub's existence.

If k>=hr, inherited palette-room AE applies because sum of the original floors is hr. Its compact label-splitting route raises active-label count to a disjoint tuple using unused labels already in P, then exact global relabeling and maximum-layer conversion supply finite repair between any exact-four endpoints. In particular it connects each endpoint to the given exact hub, or directly connects A,C. The existence/progress/floor arguments remain the frozen AE proof; no palette-room inference is made from complementary capacity.

These two exhaustive alternatives prove Theorem X12W for r>=h+3,k>=3h+1. There is no need for the X9 cardinality/equality bound. Exact incidence either supplies the actual outside-label guard and placement budget or the accepted palette-room mechanism supplies the full path.

For h=3 this yields ALL endpoints at r>=6,k>=10. A concrete previously uncovered universal domain is r=6,k=10: four triples on {1,2,3,4}, plus {5,6,7} and {8,9,10}, form a legal exact-four hub. The four-cover {1,2,5,8} is supplied; one core triple and the two private triples are its three-root guard. Here palette room fails (10<18) and four disjoint floor-three witnesses are impossible (10<12), but all arbitrary exact endpoints acquire complete access by the degree-two guard argument. Earlier module connectivity alone covered only module-shaped endpoints; the new access theorem does not assume that shape in its inputs.

## 7. Two-core hub and larger derived degree requirement

Choose disjoint S,T with |S|=|T|=h+1, requiring2h+2 existing labels. Put ALL h-subsets of each core in2h+2 slots; pad extra existing slots with copies of a core support.

Each complete core requires exactly two labels by the preceding elementary argument. Disjoint palettes give exact hub transversal2+2=4. Two labels in each core supply a minimum four-cover. All supports are exactly h and floor legal; unused other palette labels cannot reduce transversal.

Select all h+1 roots of the first core and ONE root of the second as a guard. The selected family has transversal2+1=3 and occupies m=h+2 slots.

X12A therefore needs d>=m-1=h+1. Compact incidence supplies this for every endpoint when ceil(hr/k)>=h+1. The hub fits under r>=2h+2,k>=2h+2. This proves Theorem X12D, with exact construction/slot count, actual guard, supplied cover and full restoration/access already established.

For h=3 the hub has eight roots on eight labels and a five-root guard. At k=8 or9 and r>=10,

ceil(3r/k)>=ceil(30/9)=4,

so every arbitrary endpoint qualifies. At k=8,r=9, ceil(27/8)=4 also suffices. These are arithmetic consequences of a general shared-guard access criterion, not numerical passing-case evidence.

At k=8,r=8 or k=9,r=9 the derived ceiling can be only three, insufficient for this m=5 placement budget. That says nothing about disconnected endpoints: smaller actual source guards, another exact hub, necessary two-overlap transfer, partial interleaving or other native mechanisms remain possible.

## 8. Universal floor-three target-four repair at ten roots

We now cover EVERY feasible palette when r>=10 without a classical equality/design bound.

If k>=10, Theorem X12W applies because r>=10>=6. The proof works at arbitrary r in this range, using actual incidence or AE.

If k=8 or9, Theorem X12D applies for r>=10, as Section 7 proves. Input endpoints need no cores or disjoint guard pattern.

At k=7:
- For10<=r<=12, compact avoiding-label guards at each endpoint have at most N=floor(4r/7) roots. These N are5,6,6 respectively; each satisfies2N-1<=r. The complete actual-guard lemma of Sections 3-5 connects the endpoints after full uniform placement. This is the accepted X8 incidence/O1 composition, with its actual inequality explicitly supplied.
- For r>=13, the immutable X11 proof supplies its exact thirteen-root hub on seven labels, with six-root actual guard:145,167,246,257,347,356 plus seven reserves456,236,234,135,134,126,127. Its complete eleven-cover classification and four-cover1234 were independently accepted; we use that EXPLICIT constructor, not X11's arbitrary-endpoint X9 bound. Pad by duplicates to r. Compact incidence gives d>=ceil(3r/7)>=6, stronger than the required m-1=5. X12A supplies complete access from every arbitrary endpoint. No input pattern or X5 availability is assumed.

At k=6, exact four requires an actual support complementary to EVERY three-set K: K is not a cover, and a root missing it must equal P minus K because both the complement and original floor have size three. Thus all twenty distinct triples occur as actual roots, and r>=20. With fewer slots the carrier is infeasible, not disconnected.

When r>=20, select all ten triples on any fixed five-label subset as an ACTUAL three-guard at each endpoint. Any two labels leave at least three of those five labels, whose present triple misses the pair; any three core labels hit every core triple. This guard has size ten. Full uniform placement needs10+10-1=19<=r, so Sections 3-5 supply complete repair with original restoration. This direct actual-guard argument requires no equality classification or new classical bound.

For k<=5, exact four is impossible: every k-2 labels hit every root of size at least three, because the complement has at most two labels. If k<3 no root can meet its floor. No numerical infeasibility search is used.

All palettes are exhausted, proving X12U. The small k=7 arithmetic is dependency-domain verification inside a general proof; no labelled case campaign, numerical process or new implementation exists.

## 9. Wide-palette completion at every arity and remaining obligation

For h=3,k>=10,r>=6, Theorem X12W already gives complete all-endpoint repair. With r<4, choosing one label per root shows exact four is infeasible.

At r=4, an exact-four tuple has all four roots pairwise disjoint: if two roots shared a label, that label plus one label from each of the other two roots would be a three-cover. Thus every feasible endpoint is protected, and inherited PROTECTED_EXCHANGE Theorem J connects them with their exact original floors. Feasibility itself requires k>=12. We do not extend J to arbitrary unprotected endpoints.

At r=5, accepted GENERAL_PARENT_CONNECTIVITY Theorem F covers every palette and positive floor vector, including original floor three. Both its strict-capacity and saturated cases are included. It is not assumed that its degree-two lower estimate works at arbitrary arity.

Therefore ALL feasible uniform-floor-three exact-four carriers with k>=10 are closed at EVERY r. Combining Section 7, all k8 carriers at r>=9 and all k9 carriers at r>=10 are also covered. At k=7, the same incidence/O1 inequality holds at6<=r<=9, with N=3,4,4,5 respectively and2N-1<=r. Section 8 supplies all r>=10. The preceding r<=5 inherited/infeasible arguments apply to EVERY palette, not just k>=10. Thus every feasible seven-label carrier is covered without assuming a new seven-label feasibility classification.

Any remaining carrier outside all accepted methods has k=8 or9, with r>=6 and r<=9; for k=8, r<=8. These narrowed domains are structural consequences of minimal actual guards, disjoint module requirements and exact incidence placement. They are NOT a checklist of separate campaigns. Not every parameter tuple is feasible. A failed degree/access budget is only a limitation of this particular handover, not evidence of native disconnection or a full nested barrier.

The next mechanism should derive sharper actual protection or renew necessary multiple overlaps when the current hub's guard cannot fit with at most one shared slot. An exact convenient hub alone does not settle that question. Every pair witness, original shared capacity, next-edit availability, repeated renewal, progress and destination restoration still need proof.

## 10. Consolidation, inherited boundaries and fresh review

X10 showed localization can compress a complete-core guard and an exact hub can connect arbitrary endpoints under a sufficient budget. X11 grouped exact-cover obligations to manufacture a smaller hub. X12 separates two independent costs: construct an exact hub with small guard, then derive an actual input guard using exact incidence. A minimum three-root guard only needs TWO slots outside the input guard; exact incidence supplies those slots whenever private-label palette room is absent. A second core configuration handles narrower palettes with a derived degree-four requirement. This explains the improved scope, rather than attributing it to root-count campaigns.

The hubs belong to previously accepted module families; their INTERNAL connectivity is not newly claimed. The advance is full access from arbitrary incidence types and reuse of the exact hub, not an assumption every endpoint can reach a convenient normal form. Disjoint four-root witnesses, original singleton/pair anchors, X5 triple-avoiding families, clone availability, safe-prefix extension and local certificates alone are not substituted for the proved access inequality.

New theorem domains use no X9 set-pairs equality theorem and no new external classification/design property. X11 is inherited only for its locally proved explicit thirteen-root/seven-label hub; actual input protection comes from incidence. AE, O1, M, A, J and F are applied exactly in their accepted domains. Frozen source and v16.54 certificate remain unchanged.

Root paths lift only under baseline Section 7's accepted exact-child/fixed-root-clearance interfaces; no unrestricted nested theorem is inferred. Original A11 destination-directed scheduling and mixed-floor permutation remain open. The results concern ordered repair and retained recoverability, not fundamental time, physical energy or inserted geometry. No efficiency, sharpness or originality claim is made.

Fresh independent WHOLE-ARGUMENT review must check both module exactness proofs and actual guard sizes, construction versus placement budgets, minimum-cover compaction and degree witness, all pair witnesses/primitive floors, full exact endpoint permutation, supplied next edit and termination, upper conversion, full original hub/destination restoration and exact two-leg join, AE/J/F domain branches, explicit X11-hub dependency, every feasible-palette branch, wide-palette small-arity extension and correctly limited remaining domains.

Immutable dependencies: analytical parent731a2a636a49ec89cda3e6e3f290100ce9418f85 GUARD_HANDOVER O1 and A11_X11_MINIMUM_COVER_HUB; baseline466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f, under ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/, GENERAL_PARENT_CONNECTIVITY A/F/conditionalchildinterfaces, OVERLAPPING_CLIQUE_EXCHANGE M, PALETTE_SLACK_CONNECTIVITY AE and PROTECTED_EXCHANGE J. No re-certification or rewriting of these frozen proofs.

No scientific enumeration, numerical diagnostic, test, workflow, benchmark, numbered implementation version or certified integration merge. Separately promised read-only efficiency baseline/design remains complete; runner implementation/execution and measured speedup are unstarted.
