# Anchored donor release and renewable arbitrary exact permutation

Date:2026-10-10 UTC. Status: analytical checkpoint OPEN; prospective freeze before new scientific execution. Parent1e7cd0938a668fbbcd916e6767e355be0cd1c39e. The analytical construction below was already derived before this freeze, not discovered by a later preregistered computation.

## 1 Objects and exact two-stage release criterion
Finite nonempty original core C on labelled roots R, palette P exactly its active labels, positive original floors f_i<=|C_i| and 3<=tau(C)<=4. Disjoint nonempty hidden palette; Q ranges over ALL original protected completions and is fixed. Allowed operations are one core incidence toggle, optional NOOP. Core access/addresses, source protection and actual committed changes remain supplied.

Fix an occupied reserve r. A two-stage monotone donor release first adds incidences of labels d!=r, without deleting any original donor incidence; then deletes ALL original r incidences. No other operation occurs. Let I_d be ORIGINAL footprints and M the inclusion-maximal nonempty original footprints.

Claim: such a uniformly safe release exists iff there is an assignment phi(d) in M for EVERY d!=r with:
(a) I_d subset phi(d);
(b) for every root i, #{d!=r:i in phi(d)}>=f_i;
(c) at most four of the assigned donor footprints cover all R.
Donor labels are actual distinct existing labels; multiplicities occur by assigning several labels to the same maximal footprint. Empty r is the only removed footprint. This is anchored assignment, unlike unconstrained static kappa.

Necessity: final safe S satisfies original floors,tau(S)<=4 and original-footprint domination by the inherited exact criterion. Non-r footprints contain I_d. Expand each final donor footprint to a maximal original phi(d). Expansion preserves floor satisfaction and expands a current at-most-four cover, proving(a)-(c).

Sufficiency: add d on phi(d) minus I_d for all donors, then remove r on I_r. During additions the original C remains a subcore, giving upper cover<=4; all donor footprints stay inside phi(d), and original floors cannot decrease. During deletions the final S remains a subcore and its donor four-cover persists; floor demands are already satisfied by S. r footprints shrink inside I_r. Every slice is dominated by ORIGINAL footprints, so all original protected hidden Q retain their lower bound. The original fiber is NEVER narrowed or reset.

Release length ell=sum_{d!=r}|phi(d) minus I_d|+|I_r|. This is achieved, not minimal. Any root/donor ordering within completed addition/deletion stages is safe. The final core has r absent and every other donor still active. Conversely criterion failure excludes only THIS two-stage class, not all safe paths.

## 2 Absent label permits arbitrary exact core permutation
Lemma: if a universally safe core S has a globally absent core label r, every permutation pi of P can be realized by safe single toggles, with exact final pi(S) and hidden Q unchanged. pi need NOT fix r.

A whole-footprint rename x->y is valid when y is absent: add y on EVERY x root, then delete x on EVERY x root. Before deletion the old cover remains; afterward replace x in that cover by y. Each partial y footprint lies within the former x footprint, which is itself dominated by an ORIGINAL footprint. Original floors are never reduced, and fixed original lower protection follows domination. Empty source footprints cost zero. At the rename boundary the root supports are an exact core-label relabelling, so their sizes and full hitting number are unchanged.

Decompose pi into disjoint cycles. Process cycles not containing r first. For cycle(x0,...,x{k-1}) meaning pi(xj)=x{j+1 mod k}, rename x{k-1}->r, then x{k-2}->x{k-1},...,x0->x1, then r->x0. Each destination is absent when used, and r returns absent. Last process the cycle containing r, writing it(r,x1,...,x{k-1}): rename x{k-1}->r, x{k-2}->x{k-1},...,x1->x2. The final absent label is x1=pi(r); the initially empty r footprint requires no last rename. Trivial cycles require no edits. Thus arbitrary permutations, including those moving the reserve, are covered.

For each cycle not containing r the cost is2(sum_j|I_xj(S)|+|I_x{k-1}(S)|); the r-containing cycle costs2 sum_{j>=1}|I_xj(S)|. These depend on the chosen cycle order, not an optimality theorem.

## 3 Release, exact exchange, and full restoration
Let L be the certified release path C->S. Apply the absent-label lemma S->pi(S). Follow the REVERSE of pi(L), from pi(S) to pi(C). Every pi(L) slice is safe for the SAME original Q: pi relabels only core labels, fixes hidden labels, preserves root sizes and full hitting number pointwise for every Q. Equivalently its set of core footprints is unchanged as an unlabelled multiset and remains dominated by original footprints.

Endpoint is EXACTLY pi(C), not an unlabelled equivalent: every added donor incidence is undone in its prescribed pi image; all hidden incidences are fixed. Cost2ell plus the rename cost. If pi fixes a donor or reserve its original incidence pattern is fully restored; if it moves it, that pattern is restored under the prescribed exact permutation. No initial spare, extra root, palette growth, floor relaxation, hidden read/write or restricted fiber is supplied.

Renewal: pi(C) is a palette relabelling of C. Relabel the same certificate/path at each macro-source. Source floors are identical and its full hidden fiber is identical, since core permutations fix hidden labels and full tau. Every finite prescribed permutation sequence can reuse the reserve construction without accumulated donor changes. This is a conditional path theorem, not native observer genesis or fairness. The supplied finite script may use a program counter; a phase-free current-core policy is NOT claimed.

## 4 Multi-donor example across distinct maximal footprints
Labels r,a,b,c,d,e; roots({r,a},{r,b},{a,c},{b,d},{e}); all floors saturated(2,2,2,2,1),tau3. Original maximal footprints are I_r={0,1},I_a={0,2},I_b={1,3},{4}. No one footprint contains the whole donor structure. Choose phi(a)=phi(c)={0,2},phi(b)=phi(d)={1,3},phi(e)={4}. Add c at0,add d at1,remove r at0,remove r at1. All original floors hold; a,b,e cover every slice. No single donor can replace both saturated r incidences within a dominated footprint. Yet TWO existing donors free r without a common backbone. Section3 supports arbitrary exact permutations and complete donor restoration.

Rejecting upper control: ten roots T_i={A,p_i},X_i={B,p_i} for i1..3 or{C,p_i} for i4..5; floors1,tau3. Reserve A. Every remaining maximal donor footprint is fixed (B,X1..3;C,X4..5;p_i,{T_i,X_i}). After removing A floors and domination hold but tau5, so anchored release fails. Cover condition cannot be omitted.

## 5 Increment and scope
This strictly generalizes deletion-only extraction and particular saturated single-backbone transfer: exact anchored feasibility for any finite original core in the declared domain, a constructive monotone release, and an arbitrary exact-permutation restoration/renewal interface. It does NOT characterize general connectivity or prove every feasible static reserve is releasable. Inherited safe-region and spare-copy choreography are explicitly reused. Local-progress and antichain controls remain negative.

Broad C3/general C4/native access/source admission/outcome selection/guaranteed progress remain OPEN. No fundamental time, physical force, inserted geometry, dark-matter variable or GR derivation follows.
