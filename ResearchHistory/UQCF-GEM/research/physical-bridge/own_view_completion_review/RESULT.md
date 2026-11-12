# Exact-target completion writes into an unchanged receiver's own view

Date: 2026-10-17 America/Phoenix. Author: proteinfolding-gpt.
Source baseline: `9ad504b0cdb661d016e889778c9f81276cbaa7e7`.
Status: constructive analytical draft; independent review pending. Native interaction/access remain OPEN. No mechanism code or scientific execution.

## 1. Positive result and precise scope

An existing exact-hitting-profile completion condition can force acquisition in a receiver's COMPLETE own indexed view, starting from the SAME such view in two source preparations. Neither a new vertex-support-row reader nor a grade/reference reader is needed for this conditional construction.

The construction uses the inherited finite rooted tree, fixed palette, nonempty nested supports, one-incidence edits, hitting number, and exact target endpoint. The extra condition is explicitly the return to the declared target at completion. Bare native legality and the one-unit excursion budget alone do not force it. No physical law enforcing that endpoint, invoking the source request, or granting own-view access is derived.

This is a specific improvement over source_withdrawal_completion: its forced local row is replaced by a forced change of another index's full own view, with initial receiver blindness preserved. It is not a claim that own-view access was already physically established. The own_view_receiver_boundary and receiver_move_interface reports explicitly treat that interface as conditional.

## 2. Carrier, preparations and common receiver

Let T have root o with exactly three children u,v,w. The entire cones U=desc[u] and V=desc[v] are arbitrary finite nonempty rooted trees. The third branch w is a leaf. Thus

    T = {o,w} disjoint-union U disjoint-union V.                 (1)

Use the fixed palette P={a,b,r}. The receiver is the index r, with complete own-view record

    Y_r(S) = {z in T : r in S_z}.                              (2)

Common reference data include T, P, the owner r, and the SAME requested operation below. They contain no source support array, b-view, legality oracle, global hitting-profile readout, or source-dependent notification. Access to (2), if physically available, suffices; it is not derived by defining the set.

For s=0,1 the source preparations are:

| Vertex region | s=0 | s=1 |
| --- | --- | --- |
| o | {a,b,r} | {a,b,r} |
| U | {a} at every vertex | {a,b} at every vertex |
| V | {a,b} at every vertex | {a} at every vertex |
| w | {r} | {r} |

The receiver's entire view is initially {o,w} in both cases. Only the b-incidences differ. The common target is

    q_o=2; q_z=1 at every other internal vertex.                (3)

Both starts satisfy this profile exactly. At o the leaf w requires r and the other branches require a or b, so at least two labels are needed and {a,r} suffices. Inside either cone all immediate child supports share a.

Nothing here assigns a physical metric, amplitude, clock or outcome probability. The discrete profile is the inherited combinatorial hitting-number object.

## 3. The same source request, with its completion class declared first

Request withdrawal of the SAME label a from every vertex in D=U union V. It does not name s, b's occupied branch, any r-edit, or the receiver endpoint.

A completion is any finite history of inherited one-incidence additions/deletions satisfying:

1. Nonemptiness, nesting, root palette and T are preserved at every step.
2. All b-incidences remain as in the source preparation, and w keeps {r}.
3. The only a-edits are one deletion at each vertex of D; by completion all have occurred.
4. Arbitrary legal r-edits inside D are allowed. No minimum-edit rule, preferred path, source-blind policy, fairness or proper-r-step requirement is imposed.
5. The terminal state returns to h_o=2. Requiring the full target profile (3) is sufficient; the conclusion needs only this root endpoint condition.

A fixed common source-command order can be chosen by listing U and then V in child-before-parent order. Histories may interleave r-edits needed to enable these deletions. The theorem also covers every other legal ordering that completes the same source request.

The root endpoint condition is a restriction on the inherited target profile, not a direct specification of Y_r. It is load-bearing and remains a supplied completion contract. A request may remain pending. This is an atemporal completion theorem: a terminal source commitment constrains the necessary receiver changes earlier in the completion; it is not a later deletion causing an earlier action.

## 4. Forced complete own-view output

**Theorem.** Every completion in section 3 has

    Y_r^0 = {o,w} union U,
    Y_r^1 = {o,w} union V.                                    (4)

Proof for s=0. At every vertex of U, a has been deleted and b was absent throughout. Nonemptiness therefore forces S_z={r} for every z in U. In particular r belongs to S_u. At v the only possibilities are {b} and {b,r}. If r belonged to S_v, r would hit all three immediate child supports at o: u, v and w. That would give h_o=1, contradicting the terminal condition h_o=2. Hence S_v={b}. Nesting excludes r from every descendant of v, and b is retained there, so every support in V is {b}. The root and w are fixed. This proves the first formula. Swapping U and V proves the second. QED.

The terminal singleton supports automatically give h_z=1 at every other internal z. Thus the root endpoint condition yields the full exact target (3); an independent condition at each internal receiver vertex is unnecessary.

The theorem quantifies over ALL completions in the declared class, including histories with extra legal receiver additions, deletions and backtracking. Such history freedom cannot change (4). It is not merely a display of a favorable scheduled write.

Local information is redistributed: the source b-view is already different. Global information creation is not asserted. The receiver's initially equal full views become different because coverage requires r on the branch losing its last non-r label, and the exact root target prevents r from also covering the other branch.

## 5. Completions exist and need no hitting-profile excursion

For s=0:
- Add r at every vertex of U in parent-before-child order.
- Delete a from every vertex of U and V in child-before-parent order.

For s=1 do the same with r added throughout V instead. The source deletion list can be identical in both cases. These are branch-indexed existence witnesses, not instructions that a blind receiver knows how to choose.

Every addition is legal: r is present at the parent before the child addition, and additions preserve nonemptiness. All vertices of the branch being prepared still contain a, so internal child families share a. The other branch has b everywhere.

After the additions, a-deletions are legal in child-before-parent order. The prepared branch remains nonempty through r; the other remains nonempty through b. Throughout deletion every immediate-child family inside a cone shares respectively r or b. Hence all its internal hitting numbers remain one.

At the root, during preparation {a,r} hits the three children. Once r has reached the prepared branch's root, {r,b} also hits all three and continues to do so. A singleton never suffices: w requires r, while the other branch's root never gains r along this witness. Thus h_o=2 throughout.

These witnesses maintain EXACT profile q at every primitive. They therefore also satisfy any inherited nonnegative excursion allowance, including the usual total excursion <=1. This does not mean the excursion allowance forces all completions to end at q.

There are |U|+|U|+|V| steps in the first witness and |V|+|U|+|V| in the second. No minimality or clock claim is made.

## 6. Both source preparations come from a common blank-receiver seed

Use the common seed S_o=P, S_w={r}, and S_z={a,b} for all z in U union V. Its profile is q and its receiver view is {o,w}.

Delete b throughout U in child-before-parent order to prepare s=0. Delete b throughout V in that order to prepare s=1. These are legal: a keeps every edited support nonempty; deleting below before above preserves nesting. The untouched a-label witnesses h_z=1 in every cone; w still requires r and neither cone has r, so h_o=2.

Both preparations are therefore reachable from one seed under the original native edit grammar, with the same receiver view and exact profile throughout. This is relative reachability, not physical generation or Genesis certification of that seed. It requires no appended carrier address and no M/P0 assumption.

## 7. Gauge-robust finite witness and readout

Choose U={u,x,y} with u having two leaves x,y, and V={v}. The whole carrier has six vertices {o,u,x,y,v,w}, root arity three and cone arity two.

Initial own view: {o,w}, size 2 in BOTH source cases.
Terminal own views:

    s=0: {o,w,u,x,y}, size 5;
    s=1: {o,w,v},     size 3.                                 (5)

This gives a decoder on the two terminal own-view records: size 5 reports s=0, size 3 reports s=1. It uses neither other-label membership nor a global hitting-number query. Unequal cardinalities persist under arbitrary simultaneous rooted-tree and palette relabelings with the receiver role carried along. The source preparations are likewise inequivalent as receiver-role-marked structures; their b-view sizes differ.

For arbitrary U,V the two literal sets in (4) differ. If their sizes agree and the branches are isomorphic, a branch reference would be needed for an invariant scalar decoder; this is why the six-vertex witness deliberately uses unequal cones.

The decoder claim is for a postcompletion observation in the specified endpoint class. Arbitrary intermediate r-edits can produce misleading partial sizes; no continuously sound decoder, automatic completion acknowledgment, or source-independent stopping signal is claimed. The receiver need not measure h_o to decode, but the theorem's completion premise must be physically justified before this can be promoted to a native acquisition law.

## 8. Sharp controls on what forces the write

**Without the exact endpoint, blindness is possible.** In either preparation first add r throughout BOTH U and V in parent-before-child order, then perform the same a-withdrawals. All states are native-legal. The final receiver view is T in both cases and h_o=1; all other internal hitting numbers can remain one. The entire path can stay within total excursion <=1 from q: during additions internal supports share a; after full addition they share r; the root has h_o=2 until r reaches both cone roots, then h_o=1. Thus the existing one-unit band alone does NOT force (4). Exact return, or the equivalent terminal lower bound h_o>=2 in this fixture, is essential.

**The common source request alone is insufficient.** The preceding blind completion obeys the same a-deletions and fixed b-incidences. It is the root target condition together with nonempty nesting that rules it out.

**Extra source editing changes the question.** If b may be added to the initially b-empty cone, r is no longer forced there by nonemptiness after a withdraws. Fixing the source b-view during the interaction is explicit, as in the earlier source-withdrawal construction.

**No invented forward repair.** Some source deletions are initially disabled. The additions in section 5 are lawful precursors, not repairs after an illegal empty state. A demand that nature executes those precursors is not included in the proof.

## 9. Relation to prior work and remaining native obligation

The earlier own-view obstruction concerns a contraction-only class that freezes every non-source view. This construction allows the inherited additions and joint completion, and uses a target return. It lies outside that obstruction's hypotheses; it does not refute the obstruction.

The earlier receiver_move_interface classifies experiments with other indices held fixed. Here actual a-incidences change while r is permitted to respond, so it is not an experiment in that fixed-external-source interface.

The earlier source-withdrawal theorem forces a vertex support {b_s}, but needs access to a row that was not the earlier receiver's complete view. The current theorem resolves that particular mismatch at the mathematical interface: the same indexed object Y_r changes, its FULL initial input is identical, and the output is readable using only Y_r if own-view access is available. It adds the exact-target completion premise, which must not be hidden.

| Obligation | Current status |
| --- | --- |
| Source difference and common receiver | Explicit in one inherited support carrier |
| Preparation | Legal common-seed paths, exact profile, receiver unchanged |
| Effect of specified completion | Complete receiver view uniquely forced by inherited nesting/nonemptiness plus terminal target |
| Arbitrary microscopic completion | Receiver endpoint independent of allowed r-edits/path details |
| Readout type | Existing complete own-view interface suffices; no support-row/grade/history reader |
| Physical own-view access | Still not derived |
| Source request enactment and exact-target return | Still not derived |
| New mechanism supplied in code | None |

The immediate native target is now concrete: identify an inherited enacted exact-target completion whose available output is this same owner r's retained view. Do not add a global guard, scheduler, profile sensor or own-view API in code and count it as a derivation. Alternatively, an already justified narrower operation class that forces the same receiver consequence could replace exact return; no such class is asserted here.

This is a positive conditional mechanism at the combinatorial level, with explicit action and access boundaries. It is support for the native-interaction target, not completion of it. Independent whole-argument review must judge the exact conditional mathematics separately from native realization.

## 10. Verification contract

The derivation and controls above were developed analytically before any execution. No scientific simulator, enumerator or archived scientific module is run in this checkpoint. Gemini review receives this complete argument and the exact inherited sources. Existing pipeline tests check review/provenance plumbing only. Source integrity and immutable publication auditing do not constitute physical evidence.

No broad C3/C4-C6 closure, numbered-stage certification, main merge, empirical discovery, new physical primitive, geometry, dark-matter variable or fundamental time is claimed. Time remains pruning / ordered recoverability update.

