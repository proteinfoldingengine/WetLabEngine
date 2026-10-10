# Shared-root slack handover: first reserve beyond every anchored release

Date: 2026-10-10 UTC. Status: OPEN analytical checkpoint; prospective proof/scope freeze before new execution. Parent: 84d16d4aed09ff52f02080b567adbcf958cb103e.

## Family and original promises
Fix q>=2. Existing labels are b,x_0,...,x_{q-1},e (N=q+2). Labelled roots are P_i={b,x_i} for 0<=i<q, shared root R={x_0,...,x_{q-1}}, and T={e}. Original floors are 2 on every P_i, h on R, and 1 on T, where 1<=h<=q. All labels are initially active. Core tau is exactly3: b,x_0,e cover; T forces e and no one core label hits all P_i and R. Hidden labels are disjoint and ALL original protected completions Q are fixed. Every such full source has tau3 because core tau3 bounds it above.

Original maximal footprints are B={all P_i}, X_i={P_i,R}, E={T}. For q>=2 these are pairwise incomparable and exhaust every active footprint. Every original label has its own maximal footprint. No hidden incidences, labels, roots or floors are added or relaxed. Supplied core access, addresses, finite script and actual committed toggles remain assumptions.

## Theorem 1: every anchored monotone release fails
For any prescribed reserve, each remaining donor's anchored maximal container is forced to be its own original footprint. No original non-reserve donor can be expanded. Removing x_i violates floor2 at P_i; removing b violates floor2 at every P_i; removing e violates floor1 at T. Thus EVERY anchored two-stage release certificate fails for EVERY h in1..q, including sources with reachable spare capacity below. This refutes general necessity of anchored release for safe reserve reachability, not the earlier theorem's exactness within its declared class.

## Theorem 2: exact static capacity and sharp slack boundary
In a maximal-footprint multiplicity assignment let t copies occupy B, u_i copies occupy X_i and v copies occupy E. The constraints are t+u_i>=2, sum_i u_i>=h, v>=1, plus an actual at-most-four cover. Minimum active-label capacity is
kappa=min(q+2,h+3).
If t=0, each u_i>=2, so capacity>=2q+1. If t=1, each u_i>=1, so capacity>=q+2. If t>=2, capacity>=h+3. The source attains q+2; two B copies, h X copies and one E copy attain h+3 when this is smaller, with an actual three-cover. Expansion to maximal original footprints preserves floors and a current four-cover, so the inherited exact safe-region/static-capacity theorem makes this a lower bound on EVERY universally safe core, not merely maximal vertices.

Consequently an absent label is statically possible iff h<=q-2, equivalently the original shared-root slack q-h is at least2. This condition is also sufficient for actual safe reachability by Theorem3. With h=q-1, safe first progress exists (delete one x_p at R), but kappa=N: no safe state can omit a label. With h=q, all floors are saturated, every deletion violates a floor and every addition violates original-footprint domination; the source has no safe first changing toggle. Optional NOOPs do not supply a route.

## Theorem 3: four-edit nonmonotone first release, uniformly optimal
For h<=q-2, choose distinct pivot p and reserve r among the x labels. Choose a third spoke s distinct from both; it exists because q>=3. Execute:
1. delete x_p at R;
2. add x_p at P_r;
3. delete x_r at P_r;
4. delete x_r at R.
The final x_r footprint is empty. The pivot changes its containing original maximal footprint: after step1 it is {P_p}, and after step2 {P_p,P_r} lies within B. This route necessarily deletes an ORIGINAL non-reserve donor incidence before freeing the reserve, so it is outside the anchored monotone class.

R decreases from q to q-1 to q-2, which meets h. P_r grows2->3->2; every other original floor remains met. The pivot remains inside X_p before deletion and B afterward; the reserve shrinks inside X_r. All other footprints are fixed. The actual labels b,x_s,e cover EVERY slice. Original-footprint domination supplies lower protection for ALL ORIGINAL fixed hidden completions, while this persistent three-cover supplies upper protection. Full tau is exactly3 at every slice. No hidden read, current-fiber restriction or spare-label assumption is used.

Four is the minimum number of actual committed incidence changes to create ANY FIRST absent label in a positive member of this family, even allowing arbitrary uniformly safe paths. If e is first absent, some other label must enter T earlier; the only original container including T is E, so that label must first become empty before it can enter T, contradiction. To make b absent requires deleting its q original P incidences and at least q replacement incidences to meet floor2, hence at least2q>=6 in a positive member. To make x_i absent requires its two original incidences removed and at least one other-label addition at its tight P_i. A three-edit route would therefore consist only of those two removals plus that addition. The donor would still have its original maximal footprint; adding outside it is forbidden. A separate preparatory donor deletion is necessary, giving at least4, attained above. NOOPs do not reduce committed-change cost. This is a first-vacancy optimality result, not a general permutation-path or batch optimum.

Once one x label is absent, whole-footprint rename of any prescribed occupied label into that empty destination leaves the prescribed label absent, safely. Thus ANY prescribed label, including b or e, is reachable absent iff h<=q-2, though four is not claimed optimal for those prescribed labels.

## Theorem 4: unbounded transferable capacity, exact restoration and renewal
Choose a pivot p and a nonempty subset J of other x labels of size m<=q-h-1. Delete x_p at R once. For each r in J, add x_p at P_r, delete x_r at P_r and delete x_r at R. The pivot footprint is a subset of B, each reserve shrinks inside X_r, and a surviving x_s not in J or {p} yields the same unchanged three-cover b,x_s,e. All original floors and hidden completions remain protected, with exact full tau3. Cost is1+3m achieved, not claimed globally minimal.

Taking m=q-h-1 leaves exactly h+3 active labels and reaches the exact STATIC minimum kappa. At fixed h, the accessible surplus q-h-1 grows without bound. One existing shared root carries the transferable slack; no replicated roots, fresh labels or relaxed demands are introduced.

For any safe release L:C->S (single or batch), apply the inherited absent-label rename choreography S->pi(S), then reverse pi(L) to obtain EXACTLY pi(C). This restores every preparatory incidence in its prescribed image, fixes every hidden incidence and renews under relabelling for any finite prescribed permutation sequence. It covers permutations moving the released label. Cost is2|L| plus rename cost; no global optimality or phase-free controller is derived.

## Increment and limits
This is an explicit reusable NONMONOTONE positive family with strict static spare capacity despite failure of ALL anchored certificates. It is not only a finite connectivity decision procedure. The original floors at private roots remain saturated; usable slack is supplied at the shared root. The positive source is NOT fully saturated. The fully saturated member is obstructed. This does not settle general saturated reserve reachability or universal mixed-floor connectivity. A persistent three-cover is used in this family; arbitrary upper-cover handovers are not newly derived.

The prior five-by-five diagnostic checked only globally saturated and one-slack floor modes. Its absence of hard cases did not include the mixed floor vector here: the smallest positive q=3,h=1 has floors(2,2,2,1,1), two units of slack at R only. This distinction is disclosed, not treated as a contradiction or post-hoc theorem discovery. The analytical result above was derived BEFORE this freeze and is tested prospectively below.

## Prospective exact verification contract
- Primary family: q=2..7, EVERY h=1..q, EVERY ordered distinct pivot/reserve pair. Independently reconstruct the entire typed identity set, original source/floors/footprints, all-original one-hidden-label masks, anchored failures for EVERY label, positive four-edit route and exact endpoints, one-slack last-edit floor rejection, fully saturated every-first-toggle rejection.
- Independently enumerate ALL nonnegative original maximal-type multiplicity vectors with total<=N for q=2..7. Reconstruct complete admissible-vector identity digests and canonical minimum witnesses for every h; compare exact static capacities, not only a supplied lower-bound formula. Reject omitted source/route/multiplicity identities and altered floors/operations.
- Batch: EVERY positive q,h, EVERY pivot, EVERY nonempty subset J of other spokes with |J|<=q-h-1. Verify exact cost, original floors, domination, a persistent actual cover, original-hidden safety, endpoints and optimal active-label count at maximal J. Deduplicate hidden checks by exact (q,current-core) identity while retaining per-case route identities; report both explicitly.
- Independent breadth-first reconstruction of the COMPLETE raw safe-toggle layers through depth4 for (q,h)=(3,1),(4,1),(4,2), checking no first vacancy before4 and actual first vacancies at4. Both implementations enumerate from source; omission of a layer state must reject. Four-edit optimality for arbitrary q remains proof-based.
- Smallest positive q=3,h=1: ALL120 permutations of the full five-label palette using pivot0/reserve1 release, exact reverse-conjugated restoration, plus three renewed two-permutation sequences. Arbitrary palettes/permutation sequences rely on proof and inherited interface.
- Native rejecting control: adding pivot to reserve private root BEFORE deleting it at R is dominated by no original footprint. For q=3,h=1, hidden mask20 (P_2 and T) gives original fulltau3 but candidate fulltau2. Other controls must retain sharp positive-floor/saturation/anchoring boundaries. Do not represent a failed script as general path impossibility without the static lower bound.
- Preserve genuine local RED, independent implementations, relevant inherited175 tests, prospective freeze, original ZIPs/full logs/raw reviews, separate mathematical and publication reviews, author reconciliation and immutable readback. No result is accepted solely because CI succeeds.

Broad C3/general C4/native observer/access/source/outcome/progress remain OPEN. No numbered-stage/full-stack or physical derivation.
