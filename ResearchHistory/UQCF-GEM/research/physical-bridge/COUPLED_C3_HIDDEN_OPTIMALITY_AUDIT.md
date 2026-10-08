# C3 hidden-spectator optimality — author-side audit

Date: 2026-10-07.
Status: AUTHOR-SIDE ARGUMENT AUDIT PASSED; independent review pending.

Frozen scope c2383f36b4c099f8bb27582639b55c2cb59c94a2.
Proof candidate f1531c690ba36662c5a016cd7f2a0cd6ab084275.

Checks:
1. For all hidden Z, source and target have triangle hitting number2 plus disjoint fourth root, so tau=3.
2. The original eight-edit path remains floor2-legal and tau=3 for every Z because spectators persist only on r4 and are disjoint from triangle and w.
3. For nonempty Z, deleting d first leaves r4={e} union Z of size>=2, and the six endpoint-differing toggles give tau=3 at all seven states and exact C(Z).
4. Six mandatory endpoint-differing toggles make the nonempty-Z path shortest.
5. Empty-Z independently closed theorem gives minimum eight edits with forced first +w(r4).
6. R projects away all spectator data including root size and the Boolean Z-nonempty flag; R is identical for empty/nonempty Z, but their optimal first events cannot agree.
7. A uniform eight-edit legal policy exists from R; therefore the negative theorem is about optimality, not legality.
8. One extra bit b=1[Z nonempty] selects a shortest legal policy without revealing spectator identities.
9. No claim is made that b is derivable from an observer field, global W/C, or other already retained physical variables.

Rejecting controls:
- Treating nonempty-Z path as legal at Z empty fails floor2 on its first deletion.
- Treating eight-edit w path as optimal at nonempty Z fails against explicit six-edit route.
- Including full root sizes in R would distinguish the fibers and defeat the stated impossibility, so the retained projection is deliberately declared.
- Allowing spectators on triangle roots or permitting Z to change is outside the scope.

C3 general retained host-selection remains open.
