# Activation to exact exchange: inherited composition

Date: 2026-10-11 UTC. Status: analytical source reconciliation; separate review and publication readback pending. This is a corollary of already closed results, not a new numerical campaign, new native mechanism, or extension to arbitrary intervening repair.

Source snapshot: `1282d628b2639e8a695b2893954f8e00d476644b`. The thirteen immutable source identities and locally checked bytes are recorded in `source_readbacks.json`. The reserve-activation and anchored-release closeouts remain authoritative for their respective scientific campaigns. Historical prospective headers in their result files remain historical.

## The gap being reconciled

Reserve activation produces a uniformly safe path L from the original labelled core C to a core S with an existing label r absent. Its own reversal argument only covers the case in which nothing intervenes. That restriction on reversing L verbatim is correct.

However, sections 2 and 3 of the earlier anchored-release result already provide a stronger interface: any safe core with an absent label permits every prescribed core-palette permutation, and the reverse of the PERMUTED release path restores the preparatory changes in their prescribed images. The permutation/restoration argument does not require the release to have been monotone. The later saturated-handover result explicitly uses the same interface for a nonmonotone release.

Consequently, a statement that exact permutation followed by restoration remains wholly unresolved after activation is too broad. Arbitrary intervening repair remains unresolved. A specified palette permutation is a supported operation, not an arbitrary repair.

## Domain and statement

Retain exactly the reserve-activation domain: finite simple isolate-free pair-root H, source vertex-cover number three or four, positive original multiplicities, saturated subgraph G, fixed positive original floors, the original active core palette P, and disjoint hidden palettes. Every original protected hidden completion Q stays fixed. Choose the declared eligible donor set I, original cover C_anchor of size at most four, actual original anchors, and donor identities. The source core is denoted C; C_anchor is a set of types, not the core.

If the activation criterion |Z(R*)| > |R*| holds, choose any certified activation-and-release path L:C -> S ending with r absent. For EVERY prescribed permutation pi of P, there is a finite sequence of single core-incidence toggles from C to exactly pi(C), fixing Q, preserving every original floor and the protected full-system band for EVERY original Q. Preparatory modifications are removed in their prescribed pi images. The permutation may move r and may move the originally selected anchor identities. No label or root is added.

This implication is sufficient for exact exchange in the full native safe region; the activation criterion is exact only for its previously declared release template. Failure of that criterion does not prove that a specified permutation is unreachable by another route. Identity permutations and some nontrivial permutations may need no released reserve at all. No necessity, arbitrary-repair, shortest-path, phase-free-controller, sensing, enforcement or actual-progress claim is made.

## Why whole-footprint renaming is safe

At a uniformly safe core T, let y be an absent core label and x be an occupied one. Add y at every root in the current footprint of x; only after the copy is complete, delete x at every such root. The endpoint renames x to y and makes x absent.

During additions, the former at-most-four cover remains. During deletions, replace x in that cover by the now complete y whenever x was used by the cover. This uses at most four labels, even if x was an anchor. Floors first increase and then return to their former values. Both partial and full copied footprints are subsets of the former x footprint and hence are contained in an ORIGINAL source footprint. All other footprints are unchanged. The inherited universal-safety criterion therefore protects the same original hidden completions, without rebasing to a narrower hidden fiber. There are exactly twice the size of the copied footprint actual edits. An empty footprint needs no operation.

The core palette is disjoint from hidden labels. Thus a core-absent label is absent in the full state, and a core permutation extends to a full-palette permutation that fixes every hidden label. This disjointness is essential to the argument.

## Constructing the permutation and restoration

Use r as the empty slot. For each nontrivial cycle (x0,...,x{k-1}) of pi not containing r, first rename x{k-1} to r, then x{k-2} to x{k-1}, through x0 to x1, and finally r to x0. The empty slot returns to r. Process the cycle containing r last. Writing it (r,x1,...,x{k-1}), rename x{k-1} to r, then x{k-2} to x{k-1}, through x1 to x2. The final empty slot is pi(r)=x1. Fixed points require no renames. This is exactly the inherited absent-label construction and reaches pi(S), including when pi moves r.

Now follow reverse(pi(L)), not reverse(L). For each intermediate core T of L and each fixed Q, pi(T)+Q is isomorphic to T+Q under a label permutation that fixes Q. Root sizes and full hitting number are unchanged. Its footprint multiset is also unchanged, so original-footprint domination is preserved. Hence every permuted slice is safe for the SAME original Q. Every edit remains a single syntactically valid toggle after relabelling and reversal.

The complete path is

    C --L--> S --rename(pi)--> pi(S) --reverse(pi(L))--> pi(C).

The last equality is exact in labelled incidences. If pi fixes a helper, that helper returns to its original footprint; if pi moves it, the source footprint is restored under its prescribed image. "Restoration" does not mean returning all labels to C while also performing a nontrivial exchange. The intended exact endpoint is pi(C), with no additional preparatory residue.

If L has ell actual edits and the inherited rename script has b actual edits, the achieved total is 2 ell + b. This is a construction cost, not a lower bound or optimum. Activation's equal-star zero-edit bookkeeping transfers contribute no actual edits.

For a finite prescribed sequence of permutations, relabel the release certificate at each completed source. Each source is a core-palette permutation of C with identical root sizes, original footprint multiset and original hidden-completion protection. The same argument applies repeatedly. There is no accumulated preparatory residue. An external finite script is supplied; a native schedule, successful resolution, or guaranteed completion is not derived.

## Worked symbolic examples on the accepted chain

Use the already accepted H=K4,3 source with donor types 0,1,2,3, receiver types 4,5,6, all multiplicities one, and G={04,14,15,25,26,36}. Let M_v denote the original star of v, and use label v for its sole original label. The accepted 18-edit L transfers 0->4, 1->5, 2->6, then releases label 3. At S, labels 0,1,2 occupy M4,M5,M6, label 3 is empty, and labels 4,5,6 retain their original stars.

For pi=(0 3), rename the four-incidence footprint of label 0 into absent label 3: four additions followed by four deletions. Then reverse pi(L). The achieved total is 18+8+18=44 edits. The exact endpoint has label 3 on original M0 and label 0 on original M3; labels 1,2,4,5,6 return to their original footprints. The actual anchors 4,5,6 stay unchanged throughout this particular construction. This exchanges a former donor with the released label while restoring the other activation donors.

For pi=(4 5), use the cycle through absent label 3: rename 5->3, 4->5, and 3->4. Each copied receiver star has four incidences, so this middle script has 24 edits and the total is 60. Reverse pi(L) then reaches the exact exchange of original labels 4 and 5, with all other source footprints restored. The initially chosen anchors 4 and 5 are not fixed during this route; the inherited at-most-four cover argument supplies protection through each rename. Fixed-anchor protection of the activation subpath must not be misreported as fixed anchors for every composed exchange.

These are hand-derived applications of established constructions and degree counts. No new simulation, enumerated universe, test result or optimality result is asserted for them. The prior 485 scientific tests do not become tests of these newly written examples by citation.

## Physical meaning and next boundary

The composition clarifies one precise meaning of usable relational freedom: cooperative activation can supply an internal vacant label, that label can mediate a prescribed rearrangement, and preparatory support changes can be removed without changing the original protections. A temporary vacancy need not be consumed as permanent damage to the preparation.

The result still concerns permitted routes under supplied core observations, source promises, addressing and committed-edit semantics. It does not identify energy, momentum, mass, a force, physical duration or an arrow of time. Its inverse construction is consistent with reversibility. It does not supply a law selecting one of these permitted responses.

The two full endpoints C+Q and pi(C)+Q are label-isomorphic. Consequently every observable invariant under these core-label permutations has the same endpoint value. The exact labelled task has supplied reference identities, but this corollary does not establish a physically distinguishable response relative to an independently derived record or reference system. Such a coupling must be earned separately. This is not a claim that all labels in the broader program are physically meaningless or necessarily gauge.

The inspected native-origin sources continue to require justified native input, carrier/initial correlation, action connection and accessible retained output. Fixed-family preparation and core-write autonomy already close the tempting same-interface shortcuts; they should not be rerun as new discoveries. No native acquisition mechanism is constructed by this reconciliation. Native enforcement, successor selection and progress remain separate open obligations. Broad C3/C4-C6 remain OPEN; Path A remains active and Path B closed.

## Evidence classification

This note reconciles the scope of existing accepted theorems. Its review and publication checks will be recorded separately; they are not a new Gemini mathematical campaign, a new finite scientific verification, or a reopening of prior closeouts. The unchanged raw prior reviews remain evidence of their original scopes only.
