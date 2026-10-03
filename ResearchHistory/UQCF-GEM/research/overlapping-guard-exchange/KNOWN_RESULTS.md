# Accepted connectivity classes and remaining obligations

**Latest universal analytical result (X15):** all exact-four endpoint pairs on every feasible finite carrier with original UNIFORM floor three have complete native {3,4} repair and exact original labelled/noncompact destination restoration. No carrier obligation remains for this root theorem. Original directed, unrestricted mixed-floor and nested questions remain separate/open. Proof and consolidated explanation are independently reviewed; implementation certification is not claimed.

Source baseline: `466aa8a6d55a9b21cbf6bfe8a34dd8e6f5c6946f`, under `ResearchHistory/UQCF-GEM/demos/v16.54-parent-support-connectivity/`. Historical proof headers say candidate; their separate independent review records and final closeout govern acceptance. The original files are unchanged. This ledger summarizes scope, not a new certification of their implementations.

All statements concern fixed palette, labelled slots and positive floors. Unless stated otherwise, the output for two permitted exact-q endpoints is a primitive path with transversal in {q-1,q}.

| Accepted result / source | Required input | Output and boundary |
| --- | --- | --- |
| Targets 1 and 2; GENERAL_PARENT_CONNECTIVITY | Any feasible same-carrier endpoints | Direct expansion/contraction; target 1 stays exact |
| Upper-excursion removal; same source, A | A finite path maintaining tau>=q-1 between exact-q endpoints | Converts to the desired band; does not supply the lower-guard path |
| Arbitrary-arity target 3; same source, D | Exact target 3 | Element-cover buffering plus upper removal; not arbitrary pair-cover connectivity |
| Five-child target 4; same source, F | r=5, exact target 4 | Degree-two cycle buffering or saturated partition exchange |
| Saturated capacity; EXACT_ENDPOINT_CAPACITY, H/I | delta=sum_i(k-a_i)-(q-1)k=0, q>=3 | Classifies full roots plus a partition and connects all such endpoints; positive delta remains separate |
| All floors 2; FLOOR_TWO_CONNECTIVITY, O | a_i=2 for every slot | Graph star edits and renewed symmetrization reach a common form |
| Mixed floors 1/2; SINGLETON_ANCHOR_REDUCTION, Q | Every floor belongs to {1,2} | Anchor/residual-graph reduction; does not cover arbitrary higher floors |
| Enough singleton anchors; same source, P | At least q slots have floor 1 | Other floors may be arbitrary; reaches protected class |
| Renewable singleton anchors; A11_RENEWABLE_SINGLETON_ANCHORS, X2 (separate analytical branch) | q>=4, at least q-2 ORIGINAL floor-one slots | Arbitrary remaining positive floors; finite renewed guard path plus accepted upper removal; temporaries/repeated toggles allowed |
| Residual target-three anchor lift; A11_RESIDUAL_THREE_ANCHOR_LIFT, X3 (separate analytical branch) | q>=4, at least q-3 ORIGINAL floor-one slots | Arbitrary remaining positive floors; common residual carrier plus inherited target-three D, symmetry L and upper removal A; temporaries/repeated toggles allowed |
| Pair-anchor target four; A11_PAIR_ANCHOR_CONNECTIVITY, X4 (separate analytical branch) | q=4, at least one ORIGINAL floor-two slot | Arbitrary remaining positive floors; derived strict slack and direct residual {2,3} path lift to {3,4}; temporaries/repeated toggles allowed |
| Preserved pair-anchor profile; same source, X4H | q>=4, q-4 ORIGINAL floor-one slots plus a DISTINCT floor-two slot | Arbitrary other floors; preserved residual floor-two profile uses X4, then inherited upper removal; no universal target-four premise |
| Conditional triple anchor; A11_TRIPLE_ANCHOR_RENEWAL, X5 (separate analytical branch) | q=4, same original floor-three slot; each endpoint has a supplied compact triple meeting a minimum four-cover, and actual avoiding roots of residual transversal at least two | Direct {3,4} path for arbitrary other positive floors; strict-slack OR saturated residual capacity; three existing reserves renew each saturated owner swap; guard existence not universal |
| Protected roots; PROTECTED_EXCHANGE, J/K | Each endpoint has q pairwise disjoint roots | Connects that class; its existence requires sum of q smallest floors<=k, but accessibility from every endpoint is not proved |
| Safe symmetry exchanges; OVERLAPPING_CLIQUE_EXCHANGE, L/M | Label permutation, or root permutation with destination-compatible floors, at exact q | Connects symmetry-related endpoints, not arbitrary overlap types |
| Contraction clone guard; CONTRACTION_CLONE_GUARD, U/V/W | Slot-compatible prescribed clone; retained-family cover f and contraction cover lambda | Exact formula tau(new)=min(1+f,lambda); eligible clones or a globally terminating sequence are not guaranteed |
| Uniform modules; HYPEREDGE_STAR_RELOCATION, Y | Complete h-uniform cores on a partition, h>=3, q=k-m(h-1)>=3; extra roots contain core roots | Connects endpoints of this type at fixed r,k,h,q; not a universal normal form |
| Cyclic triples; CYCLIC_TRIPLE_CONNECTIVITY, AA | Three nonempty palette parts, all internal triples and directed AAB/BBC/CCA core triples, floor 3, redundant extras, k>=6 | Connects this class at fixed r,k and q=k-3; not all triple systems |
| Disjoint compatible guards; GUARD_BUFFER_CONNECTIVITY, AB | Actual t=q-1 guards on disjoint index sets | Two-phase handover for arbitrary floors; extended to one shared slot by the present candidate |
| Uniform slot bound; same source, AC | Uniform h, r>=2N with N=binomial(h+q-2,h) | Small guards can occupy disjoint existing slots; present candidate improves to 2N-1 |
| Palette room; PALETTE_SLACK_CONNECTIVITY, AE | k>=sum_i a_i | Split shared labels using currently unused labels already in P; does not follow from complementary capacity |
| Finite-support reduction; FINITE_SUPPORT_REDUCTION, AD | Compact endpoint pair, S=sum_i a_i | Preserves connectivity answer on a suitable subpalette of size<=3S+1; finiteness does not imply connectivity |

The exact-endpoint hierarchy supplies |N_A(X)|>=q-|X| and the local capacity inequalities. One-root replacement consumes at most one lower-guard unit, but the completed state need not renew exact redundancy. Complete-module normal forms are genuinely unavailable in some exact higher-floor carriers (MODULE_CAPACITY_OBSTRUCTION); those examples are not disconnection results and the cyclic class has its own successful method.

The present candidate targets a missing link: protection can transfer through one shared root, without requiring disjoint guards or palette room. The unresolved problem is a generally available, renewing exchange when multiple shared slots admit different missed-root sets. An exact characterization of one bridge's failure does not resolve general connectivity.

## A11.X2 extension and current boundary

A11.X2 is independently accepted at candidate 1cd572d2e90ba3880dc5598d260c14e8a92acc5c, receipt INDEPENDENT_A11_ANCHOR_REVIEW.md. It lowers the sufficient arbitrary-other-floor singleton count from q to q-2. It is not merged implementation certification or a change to the integrated baseline sources.

For q=4, two original floor-one slots now suffice for native one-unit connectivity of every exact-four endpoint pair. A11.X1's large carrier is therefore covered as a full native class. The proof supplies renewable protection and unconditional finite progress within this class. It does not guarantee destination-directed incidence monotonicity.

The original q=4/uniform-floor-three diagnostic has zero singleton-capable slots and remains OPEN unless its individual parameter class is already covered elsewhere in this ledger. Fewer than q-2 singleton-capable slots are not declared universally unresolved: previously accepted results still apply. No minimal-anchor necessity or universal root/nested closure is claimed.

## A11.X3 stronger sufficient class

A11.X3 is independently accepted at candidate d2f79a71983a135eb035ef4d4c1289bdf6409814, receipt INDEPENDENT_A11_RESIDUAL_REVIEW.md. It improves the sufficient arbitrary-other-floor count to q-3. For q=4, a SINGLE original floor-one slot suffices for native one-unit connectivity of all exact-four endpoint pairs. X2 remains correct and retains its separate six-move renewable-guard mechanism.

The new ingredient is a common residual carrier: every nonanchor slot with floor <=k-(q-3) can be prepared inside the complementary palette; larger-floor slots necessarily intersect the forced anchors and are redundant. Higher residual levels descend to exact three before the ALREADY accepted target-three theorem is invoked. Dependency applicability was reviewed; no baseline theorem is newly discovered or recertified.

Any remaining exact-four native counterexample, IF one exists, must have zero original floor-one slots. This does not declare every zero-anchor carrier unresolved: all earlier graph, protected, symmetry, palette-room, slot-bound and other sufficient classes remain valid. Original uniform-floor-three diagnostics outside those classes remain OPEN. Universal A11 destination-directed scheduling and general root/nested universality remain OPEN. No minimal or necessary anchor-count threshold is asserted.

## A11.X4: completed pair-anchor native connectivity

For target four, ONE ORIGINAL floor-two slot suffices for native one-unit connectivity of ALL exact-four endpoint pairs, with arbitrary positive floors elsewhere. Together with X3, every carrier containing an original floor one OR two is covered. Any hypothetical remaining native exact-four counterexample must have ALL floors at least three; none is claimed.

Compact and align the pair root T. Actual roots avoiding both pair labels have residual transversal two or three, and their complements cover every outside label. Exact-four endpoint triple coverage forces strict total residual capacity greater than the outside palette size. The inherited element-cover owner construction then transfers protection in a common labelled residual carrier. A separate upper-bound argument proves every residual primitive stays in {2,3}, so the main theorem lifts DIRECTLY to {3,4}, with finite progress and exact labelled restoration.

For q>=4, q-4 original floor-one slots PLUS a distinct original floor-two slot also suffice. This corollary preserves a specific residual floor profile before invoking X4; it assumes no universal target-four theorem. Main dependencies C/L and corollary A/X3 are inherited and domain-checked, not recertified.

A fixed triple anchor does not inherit this one-family preparation: the all-twenty-triples example would prepare to level two, but is itself already covered by the accepted uniform-slot theorem AC. This is a method failure, not disconnection. Renewal of THREE overlapping pair-indexed protection systems with shared capacities remains unresolved. Exclude other accepted classes before identifying an unresolved all-floor-at-least-three domain.

Evidence: A11_PAIR_ANCHOR_SCOPE.md; A11_PAIR_ANCHOR_CONNECTIVITY.md; INDEPENDENT_A11_PAIR_REVIEW.md; A11_PAIR_ANCHOR_CLOSEOUT.md. Candidate 6525e708393c345b01e2004163fcc738f1e4d486, independently ACCEPTED without corrections. Temporaries/repeated toggles are permitted; universal A11 destination-directed scheduling and general root/nested universality remain OPEN. Native lifting retains accepted child interfaces. No numerical campaign, implementation or new certification is assigned.


## A11.X5: conditional triple-anchor renewal without residual slack

At target four, a SAME ORIGINAL floor-three slot suffices for native {3,4} connectivity under an explicit endpoint condition: each endpoint supplies a compact triple inside that root meeting a minimum four-cover, and the other actual roots avoiding that triple have residual transversal at least TWO. This condition is not asserted universally.

Both endpoints prepare to the same labelled residual floor carrier, with actual residual transversal two or three. If residual capacity is strictly larger than the residual palette, inherited element-cover owner transfers apply with their upper band separately checked. If capacity is exactly saturated, exact-four triple coverage forces THREE existing ORIGINAL floor-n slots, n the residual palette size. Temporary attachments of two anchor labels let those roots jointly protect two temporarily ownerless outside labels. A four-incidence owner swap is followed by restoration of all three reserves, so the next swap remains available. The misplaced-owner count strictly decreases; every primitive stays DIRECTLY in {3,4} and every labelled destination support is restored.

This proves renewing protection at saturated residual capacity without creating a slot or label. The actual avoiding-root guard condition remains essential to this theorem's input, not a proved necessary condition for connectivity. Endpoints lacking a supplied qualifying compact triple remain outside X5 unless another accepted class applies. The twenty-triples example fails this guard condition but is already solved by AC, so is not a new unresolved domain.

Evidence: A11_TRIPLE_ANCHOR_SCOPE.md; A11_TRIPLE_ANCHOR_RENEWAL.md; INDEPENDENT_A11_TRIPLE_REVIEW.md; A11_TRIPLE_ANCHOR_CLOSEOUT.md. Candidate 3857dfcc33eccb2c01456a1273426ab9dd94bade. Inherited C/L and X4's residual band argument are domain-checked, not recertified; no universal floor-two theorem is misapplied to the residual carrier. X3/X4's universal target-four class with an original floor one or two remains accepted. A11 universal destination-directed scheduling, remaining floor-three cases outside accepted classes and general root/nested universality remain OPEN. Temporary incidences/repeated toggles are allowed; child-interface conditions govern native lifting. No numerical campaign or implementation certification is assigned.


## A11.X6: sharp X5 target-existence boundary

On the seven-label uniform-floor-three carrier, the X5-qualified exact-four class G_s is nonempty at any chosen labelled slot if and only if r>=13. Exact compaction retains the supplied minimum four-cover and guard; four residual triples plus coupled mixed-triple witness counting force thirteen slots. An explicit thirteen-slot state attains the bound. Therefore ALL G_s are empty at r<=12, allowing every floor-permitted support size. A cyclic (3,2,2) core supplies a feasible exact-four twelve-slot control, already connected within accepted AA. This is an empty-target obstruction to Route A, NOT native disconnection. For six labels exact four requires at least twenty slots; G_s is empty for any r, and the all-twenty-triples control is already solved by AC.

No arbitrary accessibility or new universal repair theorem is proved. At seven labels/r>=13, existence is distinct from reachability; at seven labels/r=12 a replacement mechanism must avoid reliance on X5's all-triple-avoiding family. Other accepted classes remain valid. Larger palettes, A11 destination-directed scheduling and unrestricted native/nested universality remain OPEN. No scientific run or implementation is initiated.

Evidence: A11_X6_SCOPE.md, A11_X6_GUARD_ACCESSIBILITY.md, INDEPENDENT_A11_X6_REVIEW.md and A11_X6_CLOSEOUT.md. Candidate 442fb7b839425a96b2ae248616b944f56f1229a0. This is analytical source freezing and review, not numerical preregistration.

## A11.X7: incidence-derived replacement guards and complete repair

For uniform original floor h on k labels and r labelled slots, exact-q endpoints (q>=3) compact exactly while retaining a supplied minimum cover. A maximum-incidence label belongs to at least ceil(hr/k) compact roots. The ACTUAL family avoiding that single label requires at least q-1 hitting labels; otherwise its smaller cover plus the omitted label would cover the exact-q tuple. Thus every compact endpoint has a guard on at most N=floor(r*(k-h)/k) existing slots.

If 2N<=r, the guards from two endpoints fit on disjoint existing indices after the inherited safe endpoint root permutation. Inherited AB installs the destination guard while preserving the source, then uses the installed guard to finish every other root. Actual next primitives exist and symmetric difference decreases. The preliminary lower path is converted by accepted upper-layer removal to {q-1,q}; reversing endpoint permutation and exact compaction restores the ORIGINAL labelled noncompact destination.

This closes ALL exact-four endpoint pairs at k=7,r=12,h=3, without a cyclic or X5 hypothesis. X6 remains correct: every X5 target is empty there. The replacement is a single-label-avoiding guard of at most six roots, not an all-triple-avoiding guard. The general sufficient criterion also holds whenever 2h>=k. These are analytical theorems, not new implementation certification. AB/M/A remain inherited and domain-checked, not recertified.

Evidence: A11_X7_SCOPE.md, A11_X7_INCIDENCE_GUARD_REPAIR.md, INDEPENDENT_A11_X7_REVIEW.md and A11_X7_CLOSEOUT.md. Candidate 4e0eee45107e54d6059d00b846a666fd0cd6c00d. No numerical campaign, run, workflow, tests or numbered version. A11 original destination-directed scheduling and general native/nested universality remain OPEN; failure of the sufficient slot inequality is not disconnection.

## A11.X8: one-overlap incidence guards complete repair

The accepted incidence-derived actual guard bound N=floor(r*(k-h)/k) now composes with accepted one-shared-slot O1: uniform-original-floor exact-q endpoints (q>=3) have complete native {q-1,q} repair whenever r>=2N-1. Endpoint-sensitive maximum compact degrees d_A+d_C>=r-1 also suffice.

Place the destination guard on existing slots with at most one source overlap by an accepted safe EXACT-endpoint root permutation. Actual guard obligations force every small cover of the exclusive roots to miss BOTH supports at the shared root, protecting their union and every subset visited during the primitive handover. Once the destination guard is fully installed, it protects all remaining root repairs. Each middle primitive has an eligible next edit and decreases symmetric difference. Accepted upper-layer removal and reversed endpoint preparation restore the exact original labelled noncompact destination.

All seven-label/uniform-floor-three exact-four endpoint pairs are therefore connected at r=13,15,17 without X5 or cyclic assumptions. X7's r=12 result remains valid. At seven labels, any remaining universal carrier obligation is among r=14,16,18, before excluding accepted subclasses and endpoint-sensitive degree conditions; old accepted O1 closes every r>=19. No feasibility claim is made for every smaller r.

This is incremental analytical composition, not recertification of X7G/O1/M/A or a new multiple-overlap theorem. Original A11 destination-directed scheduling and general native/nested universality remain OPEN. Failure of a sufficient inequality is inconclusive.

Evidence: A11_X8_SCOPE.md, A11_X8_ONE_OVERLAP_INCIDENCE_REPAIR.md, INDEPENDENT_A11_X8_REVIEW.md and A11_X8_CLOSEOUT.md. Candidate 6c5b2159080486b83fd005d42e0bbd719561f9f2. No numerical campaign, run, tests, workflows, implementation or numbered version.

## A11.X9 — strictly smaller guards derived from exact endpoints

Fresh whole-argument analytical review accepts X9G and the complete repair composition. For uniform original floor h>=2, exact-q endpoints q>=3 have an actual (q-1)-guard of size at most B-1 after exact minimum-cover-retaining compaction, where B=binomial(h+q-2,h). A smallest guard attaining B would be the classical complete equality core; exactness supplies an ACTUAL external root. Replacing two core selections by that existing root yields a smaller guard with explicit witnesses against every forbidden cover.

Combine with X7G using G=min(floor(r*(k-h)/k),B-1). If r>=2G-1, safe full exact endpoint permutation places guards with at most one shared slot. O1 protects every primitive of handover; installed destination protection supports all remaining repairs with eligible strictly decreasing symmetric difference. The supplied lower path can exceed q; accepted A converts it before reversed permutation/compaction restore the original labelled noncompact destination.

Palette-independent r>=2B-3 follows. Uniform floor-three target-four repair is complete for ALL feasible palettes at r>=17, improving the prior nineteen threshold. Seven-label remaining universal carrier obligations are confined to r14,16 before accepted subclass exclusions. No isolated campaign, sharpness, multiple-overlap universality, mixed-floor or original directed/nested closure.

New external dependency is the CLASSICAL uniform Bollobas equality case, explicitly sourced in the proof; no originality claim. Frozen prior sources/certificates unchanged. Scope7664ed65aac533f16f39740483dc5019055f217f, candidate31566452722b73d833250f1132a154883a73d60f. Proof A11_X9_STRICT_GUARD_REPAIR.md, consolidation A11_REPAIR_CONSOLIDATION.md, fresh INDEPENDENT_A11_X9_WHOLE_REVIEW.md, closeout A11_X9_CLOSEOUT.md.

Separately promised evidence-based efficiency baseline / bounded orchestration proposal / tiny end-to-end validation DESIGN are completed on the isolated engineering branch; runner implementation, execution and measured speedup remain NOT STARTED. No numerical jobs, workflows, new version or certified integration merge.

## A11.X10 — localized protection, complete-core compression and exact-hub repair

Accepted revised candidate: 4bc023027488c023bbe4c79983f45c92decbafeb. Initial candidate ead7a528d11cf5f54531986a45ac18d124731ba6 was REVISE for the newly derived universal hub consequence; it is preserved in INDEPENDENT_A11_X10_INITIAL_REVIEW.md. Final fresh whole-argument receipt: INDEPENDENT_A11_X10_WHOLE_REVIEW.md. Proof: A11_X10_PROTECTION_LOCALIZATION.md; closeout: A11_X10_CLOSEOUT.md.

General X10L: when all covers of size at most t-1 exposed by removing selected guard roots have union size at most t=q-1, exact q supplies an ACTUAL root missing that union. Repeated eligible reductions strictly decrease selected cardinality; a terminal pair-local obstruction is only a limitation of that selection rule, not minimum guard size or native disconnection.

X10C: an exact endpoint containing every actual h-subset of a core of size h+t-1 has a t-guard on B-t+1 slots, B=binomial(h+t-1,h). The actual missing-cover root replaces all t core supports containing one (h-1)-set. Every forbidden small cover has a retained-core or replacement-root witness. Under r>=m_A+m_C-1, exact compaction, full uniform endpoint permutation, O1 handover, eligible finite lower progress, A upper conversion and reversed preparation reach the full original labelled/noncompact destination.

A single exact core hub connects every endpoint under the one-sided budget r>=2B-t-1. At h=3,q=4, an explicit fifteen-root seven-label core hub plus one duplicate exists on every feasible sixteen-slot carrier: k<=5 cannot realize exact four, k=6 requires twenty distinct actual triples, and every k>=7 permits embedding. Hub guard<=8 plus arbitrary endpoint guard<=9 therefore gives UNIVERSAL full repair at r>=16 across ALL feasible palettes (r>=17 remains inherited X9). This improves the prior sufficient threshold seventeen; universal r15 is not proved. At seven labels the remaining universal carrier candidate is r14 before accepted subclass exclusions.

This is a stronger derived-guard mechanism and exact-hub composition, not an isolated numerical campaign. Same-slot X5 qualification is unnecessary; arbitrary input endpoints need not contain a core. Universal localization below the budget, necessary multiple-overlap renewal, original directed scheduling, mixed-floor placement and unconditional nested repair remain open. Frozen baseline and X9 sources, certified v16.54 and completed read-only efficiency baseline/design remain unchanged. No runs, tests, workflows, numbered version or integration merge.

## A11.X11 — grouped minimum-cover completion and economical exact hubs

Reviewed final candidate: f51ac417fe18772e1b91b2558ee89635b6a5c765; proof A11_X11_MINIMUM_COVER_HUB.md, SHA256 104a162dd7359137e44351a5df4346bffa0ed4643aa8bc556e6aa46e1c0cc6d7. Fresh whole-argument receipt INDEPENDENT_A11_X11_WHOLE_REVIEW.md; closeout A11_X11_CLOSEOUT.md. Actual initial ACCEPT (fifteen-slot theorem) and strengthened-candidate REVISE (two stale scope statements) remain in INDEPENDENT_A11_X11_INITIAL_REVIEW.md and INDEPENDENT_A11_X11_REVISION_REVIEW.md. No failed scientific run is implied.

X11H manufactures an exact-(t+1) hub by complementing ALL minimum t-covers of a specified tau=t guard. X11P groups those obligations into fewer reserve roots: each group's allowed pool must fit the original floor AND meet a supplied (t+1)-cover of the guard. Those conditions are necessary and sufficient within the fixed-guard/fixed-cover extension class. Constructor slots and native access budget remain separate.

The explicit six triples145,167,246,257,347,356 have tau3 and exactly eleven minimum three-covers. Seven reserves456,236,234,135,134,126,127 exclude them all;1234 is a supplied four-cover. This constructs a thirteen-root exact-four hub with an ACTUAL six-root guard on seven existing labels. Extra labels can remain unused; duplicate a guard root to fit more existing slots. No external design/classification or inserted geometry is used.

Arbitrary exact endpoints receive actual guards<=9 from X9. Six plus nine needs fourteen slots under accepted O1 placement. Exact minimum-cover compaction, full uniform exact-endpoint permutation, actual pair witnesses, eligible finite primitive progress, upper conversion, original hub restoration and exact two-leg composition give UNIVERSAL floor-three target-four repair at r>=14 across EVERY feasible palette. Every original labelled/noncompact destination support is restored. k<=5 is infeasible; k6 requires twenty actual complement triples and r>=20 remains inheritedX9.

The former seven-label fourteen-slot obligation is closed; there is no remaining prior seven-label carrier obligation. Residual coarse bounds can use4<=r<=13,8<=k<=3r-1 before accepted subclass exclusions; not every tuple is feasible. These are consequences of a general exact-cover packing/hub mechanism, not an enumeration checklist. Universalr13 on larger palettes, sharpness, smaller guards/hubs, necessary multiple-overlap renewal, original directed schedules, mixed-floor placement and unconditional nested repair remain open.

Certified v16.54 and all frozen inherited sources are unchanged. Read-only efficiency baseline/design remains complete; runner execution and measured speedup remain unstarted. No scientific enumeration, tests, workflows, numerical campaign, numbered version or integration merge.

## A11.X12 — incidence-selected protection and minimal-guard module access

Reviewed candidate: adaa8f50fa75c90da19f720c4074535f877125fa; proof A11_X12_MODULE_HUB_ACCESS.md, SHA256 c70dce453d84447b7b0021412df1a70130fb13b3d57fb930692ac4f0da4aba12. Fresh whole-argument receipt: INDEPENDENT_A11_X12_WHOLE_REVIEW.md; closeout: A11_X12_CLOSEOUT.md.

An exact compact endpoint has hr incidences. A maximum-degree label of degree d supplies an ACTUAL three-guard on r-d avoiding-root slots. An exact hub with actual m-root guard has complete native access when d>=m-1: uniform full exact-endpoint permutation places its guard with at most one overlap, and O1/M/A plus eligible finite primitive progress restores the entire original labelled/noncompact endpoint. Exact full hub return makes two-leg composition reusable.

General uniform h>=2,target4: a complete h-uniform core on h+1 labels plus two private h-blocks makes an exact-four hub on h+3 slots/3h+1 labels with the MINIMUM three-root guard. Thus ALL endpoints are connected at r>=h+3,k>=3h+1: k<hr forces degree>=2 and actual guard access; k>=hr is accepted palette-room AE. Two disjoint complete h+1 cores yield another exact-four hub on2h+2 slots/labels with m=h+2 guard and derived universal access when ceil(hr/k)>=h+1.

At floor three, these mechanisms plus checked inherited domains give UNIVERSAL full repair at r>=10 across EVERY feasible palette, improving fourteen. ALL feasible k>=10 carriers are covered at EVERY r; k8/r>=9 and k9/r>=10 are covered. Small palettes use actual guards and explicit hub branches rather than X9 equality: k7 incidence/O1 and X11's explicit constructor, k6 actualtwentytriples/ten-root guards, k<=5 infeasible. r4 protectedJ and r5F extend wide-palette closure at small arity.

Remaining possible carriers before accepted subclass exclusions have ONLY eight or nine labels and small r (r>=6, r<=9; at eight labels r<=8). This is the consequence of general guard/module/density mechanisms, not an isolated campaign checklist. A failed degree budget is not disconnection. Sharper actual protection, lower-cost access or genuinely reusable necessary multiple-overlap handovers remain the mathematical obligation.

No new external classification/equality/design dependency; X9's bound is NOT needed in the new proof. Original directed scheduling, mixed-floor placement, unrestricted nested universality and efficiency remain open. Frozen proofs/v16.54 certificate remain unchanged. Read-only efficiency baseline/design stays complete with runner execution unstarted. No runs, tests, workflow, numbered version or integration merge.

## A11.X13 — exhausted-palette protection and exact six-root feasibility

Reviewed candidate: 81cc1d59fb7ae79328cdcb0129f216a57c9a31bf; proof A11_X13_NARROW_PALETTE_PROTECTION.md, SHA256 bbb17c815f8bbce1cb27982452cceb87052f553739ca36f0af2433cbad6bbf84. Fresh whole-argument receipt: INDEPENDENT_A11_X13_WHOLE_REVIEW.md; closeout: A11_X13_CLOSEOUT.md.

X13B: when t disjoint actual h-root supports exhaust the palette, each additional floor-safe root misses at most (1-1/t)^t of the colourful t-covers. Exact transversal at least t+1 therefore requires b>=ceil((t/(t-1))^t) additional roots. At t3, three additional roots cannot complete the actual disjoint guard to exact four. This is a necessary exact-entry construction bound, not disconnection or a sufficient completion theorem. Shared incidences of each actual root are counted together.

At k<3h any actual three-guard needs at least four roots, so exact-four label degree is at most r-4 and compact incidences satisfy hr<=k(r-4). At six floor-three roots, k<=8 is infeasible by this bound. At k9, degree3 would expose three disjoint avoiding triples exhausting the palette; X13B rules out their completion by the other three roots. Thus every label has degree2 and the six compact roots form a loopless cubic multigraph on six vertices. The elementary proved perfect matching supplies a forbidden three-label cover. Hence exact-four endpoints on six floor-three slots exist IF AND ONLY IF k>=10.

Every feasible six-slot exact-four pair therefore has full native {3,4} repair by X12W: explicit exact hub, actual degree-derived source guard, O1 handover, eligible finite edits, upper conversion, full original labelled/noncompact hub return and exact two-leg restoration. The positive construction is inherited X12; no new multiple-overlap availability is claimed.

Remaining possible floor-three exact-four carriers before accepted subclass exclusions have k8,r7..8 or k9,r7..9. These bounds follow from structural protection/completion/feasibility arguments, not isolated campaigns. The empty six-slot/nine-label exact entry class is NOT an unreachable existing target or native endpoint disconnection. Continue sharper actual protection or reusable necessary multiple overlaps with full next-move and restoration obligations.

Fresh whole-argument review accepts the exact source. No external theorem/classification, numerical execution, test, workflow, run ID, implementation, numbered v16.55 certification or integration merge. Certified v16.54 and inherited sources stay frozen. Original directed scheduling, mixed-floor and unrestricted nested questions remain open. Separate accepted efficiency baseline/design remains complete; runner implementation and measured speedup remain unstarted.

## A11.X14 — guard palette requirements and renewable saturated incidence cycles

Reviewed candidate:9abe657a82bff30c05d6a943d379b7c5a2e4663a; proof A11_X14_SATURATED_INCIDENCE_RENEWAL.md, SHA256 107c6b9d8f814def5b8702fba6c7ecfbf0e0ab68ee41194607ab92a7d63dd3b2. Fresh whole-argument receipt INDEPENDENT_A11_X14_WHOLE_REVIEW.md; closeout A11_X14_CLOSEOUT.md.

X14G proves that a four-root three-guard at floor h needs at least ceil(5h/2) actual labels. Two disjoint intersecting root pairs would give a two-cover, so the root intersection graph is a star or triangle. The star requires three disjoint leaves; the triangle requires an isolated root and a three-root union with label multiplicity at most two. Actual avoiding-label guards live on P minus that label. Thus k-1<ceil(5h/2) forces at least five avoiding roots, degree<=r-5 and compact hr<=k(r-5).

X14C gives COMPLETE repair for exact-q endpoints q>=3 with arbitrary positive original floors, when both admit exact compactions of maximum label degree D and r>=(q-2)D+2. Pending row surplus/deficit transfers either have a destination below D or an eligible directed cycle. Rotate a cycle through one temporarily overfull label D+1 and a travelling underfull label, restoring all row sizes/column degrees at completion. It needs NO spare label, column capacity or root. Every forbidden at-most-(q-2)-cover meets at most (q-2)D+1<r actual roots, supplying a missed-root witness. Every primitive reduces destination symmetric difference, next cycles exist by actual flow balance, and the lower structure renews even at level q-1. Inherited upper removal and reversed exact compaction restore every original labelled/noncompact destination support. No permutations or universal mixed-floor claim.

At k8,h3,q4, actual avoiding families need five roots. No exact-four endpoint exists at r<=7. At r8 compact incidences force every label degree exactly3, so X14C's renewable SATURATED cycles connect every pair. Two complete triple cores on disjoint four-label palettes supply an exact-four feasibility control. X12D covers every r>=9. Hence ALL feasible eight-label floor-three exact-four carriers have complete {3,4} repair. This is a general structural guard/renewal mechanism, not an isolated campaign.

Remaining possible original-floor-three target-four carriers before accepted exclusions have ONLY nine labels and r7..9; feasibility of every tuple is not asserted. Original destination-directed universality, necessary arbitrary-guard multiple overlaps and unrestricted nested generality remain open. Failure of the incidence inequality is not disconnection. Temporary larger supports and repeated incidences remain native.

Fresh whole-argument analytical acceptance; no new external graph/design theorem, scientific enumeration, tests, workflow/run, implementation, numbered v16.55 certification or integration merge. Certified v16.54/inherited sources and separate accepted efficiency design remain unchanged; runner implementation and measured speedup remain unstarted.

## A11.X15 — universal floor-three target-four ROOT repair by renewed actual protection

Reviewed candidate:fdfcc64ae0f828d9dcedc2cc41d2bc2a63868e5d; proof A11_X15_UNIVERSAL_FLOOR_THREE_REPAIR.md, SHA256 6907acf000829479ec99fefb43392a36ca7d396665f94e3655493bfd858a22f1; reviewed consolidation A11_REPAIR_CONSOLIDATION.md, SHA256 2fd3615ef1d644a6779c9210595aaa1ea81fa85a93995ca2f68abfe2077fa542. Fresh whole-argument receipt INDEPENDENT_A11_X15_WHOLE_REVIEW.md; closeout A11_X15_CLOSEOUT.md.

X15S proves arbitrary-degree-capacity incidence repair under strict total slack S<Dk. Pending deficits supply a greedy transfer or a full-column directed cycle. A spare label absent from a cycle row buffers that row's source; if it occurs in EVERY cycle row, an ACTUAL incident row of a full cycle column missing the spare label exists OUTSIDE the cycle colours. Borrow that row's incidence, rotate the cycle, restore it. All degrees stay <=D; repeated colours/floors/absent additions/present removals and all buffer restoration are checked. Every completed macro strictly decreases pending differences and renews the next-move conditions. No spare column need miss a cycle row.

X15L levels max degree M to D when S<=Dk and r>=D+(q-3)M+1. Every above-D donor has a below-D recipient and an actual row containing the former but missing the latter. After adding the recipient, every forbidden set containing it still misses a root by D+(q-3)M<r; other sets retain actual old witnesses. Deletion cannot weaken protection. Excess degree decreases at every completed transfer. The arrival can remain at q-1; exact entry is not assumed.

X15N composes those lower paths with strict-slack X15S or saturated X14 LOWER cycles (the latter requires r>=(q-2)D+2), then reverses saved destination leveling. Apply maximum-layer A ONLY to the complete path between original exact-q endpoints, followed by full original labelled/noncompact restoration. Arbitrary positive floors are valid in this explicit sufficient class because original slots are never permuted; no universal mixed-floor theorem follows.

At k9,floor3,target4 every exact endpoint label avoids at least four roots, giving M=r-4. D3 and S3r supply ALL remaining r7,8,9 via M3,4,5: strict slack at r7/r8, saturated renewal at r9. Together with checked accepted X12/X13/X14 branches, EVERY exact-four endpoint pair on EVERY feasible finite carrier with original UNIFORM FLOOR THREE has COMPLETE native repair with3<=tau<=4 and the exact original labelled destination restored. The unit is an upper bound, not a claim every pair requires a positive defect.

This removes X5's conditional guard requirement for the universal native root-repair conclusion by a replacement construction; universal X5 qualification itself is NOT proved. There is no remaining uniform-floor-three target-four root-connectivity carrier obligation. Original A11 stricter destination-directed universality, arbitrary mixed-floor/higher-target universality and unrestricted nested universality remain OPEN. Conditional child lifting retains certified interfaces. No physical/originality/fundamental-time claim.

Fresh whole-argument analytical ACCEPT covers the new proof, renewed structures, all carrier branches and consolidated explanation. Earlier failures and frozen sources remain unchanged. No numerical enumeration, test/workflow/run ID, implementation, benchmark, numbered v16.55 certification or integration merge. Certified v16.54 and accepted separate efficiency design remain unchanged; runner implementation and measured speedup remain unstarted.

## A11.X16 — palette-aware actual guard requirements and mixed-floor repair budgets

Reviewed candidate:fb1625a62c617bc818eac7725131e2ee38b895f4; proof A11_X16_PALETTE_GUARD_BOUNDS.md, SHA256 b5d1eb74b0b7475bd8ba0570d87a091bf60a8c54e5fef25df2f8fad4965cbe81. Fresh whole-argument review INDEPENDENT_A11_X16_WHOLE_REVIEW.md; closeout A11_X16_CLOSEOUT.md.

X16C derives the elementary recursive actual-cover requirement L(v,b,0)=1 and L(v,b,t)=ceil(v/b*L(v-1,b-1,t-1)). Labelwise incidence counting uses the SAME actual blocks across shared obligations; it proves a necessary minimum block count, not existence at equality. Exact-four roots of minimum floor h require r>=L(k,k-h,3). Actual label-avoiding three-guards on k-1 labels require g_C=L(k-1,k-1-h,2), strengthened where applicable by X14's guard palette bounds. This furnishes endpoint degree<=r-g, not a count-only buffer.

X16R supplies COMPLETE mixed-floor {3,4} repair with every original labelled/noncompact support restored when any certified actual avoiding-guard lower bound g gives: (A)r<=2g-2; (B)r=2g-1 and sum floors<(g-1)k; or (C)r>=2g and sum floors<=(g-1)k. It checks X14/X15 domains, actual pair witnesses, eligible leveling/repair moves, renewed capacities, macro progress and full-path upper conversion. Floors remain in original slots; no arbitrary mixed-floor permutation.

At floor4/k9, covering density strengthens the avoiding-guard minimum to6 and exact endpoint count to at least11. Uniform floor4/r11 has strict capacity44<45 and complete repair CONDITIONAL on exact endpoints existing; feasibility is NOT asserted. At floor4/k10, actual g5 excludes r<=8, supplies complete repair at r9 and saturation at r10; X12D covers r>=11. Thus ALL feasible ten-label original-uniform-floor-four exact-four pairs connect. Two disjoint complete4-uniform five-label cores prove feasibility for r>=10; feasibility at r9 stays undecided.

At k9/r8 every original floor profile with minimum3 and sum floors<=27 has complete repair. The actual tuple2349,134,124,123,678,578,568,567 proves a feasible mixed profile(4,3,3,3,3,3,3,3) with supplied minimum cover1256. This is a transparent corollary of accepted renewal plus actual input bounds, not a new independent handover or isolated campaign.

X15's UNIVERSAL original-floor-three target-four ROOT theorem remains accepted/unchanged. Universal mixed-floor/higher-floor/higher-target and unrestricted nested questions remain open outside proved classes, as does original destination-directed scheduling. Covering lower bounds and failed sufficient criteria are not existence/disconnection certificates. No originality/physical/fundamental-time claim.

Fresh analytical ACCEPT; no numerical enumeration, test/workflow/run ID, implementation, benchmark, numbered v16.55 certification or integration merge. Frozen inherited sources, certified v16.54 and separate accepted efficiency design unchanged; runner implementation and measured speedup unstarted.
