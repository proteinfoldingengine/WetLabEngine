# Independent adversarial review — auxiliary permutation theorem

Date: 2026-10-07.
Review provenance:
- External AI model: spark-2
- Job: 01a117ed-cd22-7520-b6d1-c6423766f657
- Thread: 01a117ed-cd5c-776b-967a-f349a433e468
- Status: completed
- Reviewer verdict: ACCEPTED
- Both immutable GitHub files were retrieved: Both specified immutable GitHub blob pages were successfully retrieved and reviewed.

Immutable sources:
- Scope commit 51bb75d3ca71f35c62b480eee21e6f9afcdd6fbb
- Proof commit dcec4d02f79539c4b4ba0e5eb827917149040e77

## Independent assessment

ACCEPTED within the exact frozen singleton-permutation scope. The proof is a constructive sufficient theorem, not a universal repair theorem; the n=4 endpoint-only swap correctly prevents any claim that the auxiliary is always necessary.

## Mathematical checks

Cycle orientation and 2-cycle boundary: For a cycle (i_1,...,i_l) with sigma(i_j)=i_(j+1) and i_(l+1)=i_1, the target of root i_j is {a_(i_(j+1))}. The schedule processes j=l,l-1,...,2, then closes root i_1, so its direction agrees with the target definition rather than its inverse. The construction remains valid for a 2-cycle: the single middle iteration first moves a_(i_1) into i_2 and frees a_(i_2), after which the buffered i_1 is closed. No step relies on l being at least 3.

Nonemptiness: Every addition is made before the corresponding old-label deletion. The buffered root retains w after its old singleton label is deleted; each middle root retains its newly added target label after its old label is deleted; the final deletion of w occurs only after the final target label has been added.

Pairwise disjointness: Initially all singleton supports are disjoint. w is globally absent when added. Every subsequently added endpoint label is the one globally freed by the immediately preceding deletion, so it is absent from every other root. Roots outside the active cycle use labels from disjoint permutation cycles and remain unchanged.

Hitting number: Under the file's hitting-set definition of tau, n nonempty pairwise-disjoint supports require at least one distinct hitting label per root, while selecting one label from each root gives a hitting set of size n. Thus tau=n at every primitive state, including the transient two-element states.

Protected band: For n=3, tau=3; for n=4, tau=4. Therefore every intermediate state satisfies the full protected band 3<=tau<=4 and all floors remain 1.

Count: If m roots move and c nontrivial cycles are present, the schedule has L=sum 2(l+1)=2m+2c edits.

Buffer reuse: At cycle close, every root in the cycle is at its exact target singleton and w is absent. The same w can therefore be used for the next disjoint cycle; at most one root-label incidence involving w exists at any time.

n=3 endpoint-only obstruction: Consequently no endpoint-only primitive first move is protected for any nonidentity permutation at n=3. A protected repair must first add an off-endpoint incidence.

n=3 restricted optimality: For a single nontrivial n=3 cycle of length l, the 2l source/target-differing incidences each have odd endpoint parity and therefore must each be toggled at least once. The first move must be off-endpoint, and all off-endpoint incidences are absent at the target, so at least two off-endpoint toggles are required in total. The construction uses exactly two, giving the lower bound 2l+2 and matching it.

n=4 rejecting control: Every root remains nonempty, every edit is endpoint-only, and the band is preserved. Thus w is sufficient for all instances in the theorem but is not necessary for every n=4 instance; any claim of universal n=4 necessity would be false.

## Adversarial counterexample attempts

- Reverse the cycle orientation: Fails as a counterexample: the schedule's use of a_(i_(j+1)) exactly matches C_(i_j)={a_sigma(i_j)}.
- The l=2 boundary case: Fails as a counterexample: the single middle iteration has the required free label and leaves both roots nonempty and disjoint.
- A cycle adjacent to fixed points or another cycle: Fails as a counterexample: permutation cycles use disjoint label sets; after a cycle closes, w is absent and its labels remain disjoint from the unprocessed cycle.
- A transient addition causing a shared label: Fails for the proposed schedule: each transient addition uses a globally absent label, so no sharing occurs.
- Endpoint-only repair at n=3: The attempted path is blocked at the first primitive event by either floor failure on deletion or tau<=2 on addition.
- Endpoint-only repair at n=4: This is not a counterexample to the theorem; it is a counterexample to a stronger necessity claim, supplied explicitly by the two-root swap path above.

## Proof correction status

Substantive fix required: false
The invariant, cycle indexing, cleanup, reuse, count, n=3 obstruction, and n=4 rejecting control are mathematically sound within the frozen scope.

Recommended reporting precision:
- When saying one label works for any number of cycles, explicitly append 'within the n in {3,4} protected-band theorem'; beyond that, call it only the combinatorial extension because tau=n may exceed 4.
- Keep the 2l+2 optimality statement explicitly tied to a single nontrivial n=3 cycle and the sequential one-incidence toggle model, and do not generalize it to n=4.
- State the hitting-set definition of tau in the theorem statement itself if this result is intended to stand alone.

## Strict boundaries

- tau must mean the minimum cardinality of a label hitting set for the root supports, and supports must be ordinary sets of labels; the tau=n argument depends on that definition.
- Edits are sequential primitive toggles, not simultaneous operations, and every scheduled add is of an absent incidence while every scheduled delete is of a present incidence.
- w is globally absent at the source and target and remains reserved/available for the schedule. The construction does not require a fresh label per cycle.
- The exact theorem is limited to singleton source roots, a permutation target on the same distinct labels, floor 1, n in {3,4}, and disjoint permutation cycles. Fixed points are intentionally left untouched.
- The construction also works combinatorially for larger n, preserving tau=n, but n>4 lies outside the stated protected band with upper bound 4.
- There is no claim for overlapping initial supports, higher floors, arbitrary directed dependency graphs, coupled non-permutation targets, simultaneous edits, physical particles/forces/geometry/energy, or a universal auxiliary bound.

## Governance

This file preserves the independent external mathematical verdict. It is NOT the separate publication/reporting consistency review, final closeout, numerical certification, or physical validation. No further generalization is promoted by this review.
