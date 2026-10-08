# C3 capacity-bit observability — author-side audit

Date: 2026-10-07.
Status: AUTHOR-SIDE AUDIT PASSED / INDEPENDENT REVIEW PENDING.

Frozen scope 0b8d59969c33f77410a543b0bd997a501b717b56.
Proof candidate 7b567d4b22dbc968f60ddcaa7a04fced941ba490.

1. Since E4={d,e} union Z and f4=2, source slack sigma4=|Z| exactly.
2. The hypothetical deletion -d(r4) preserves tau=3 even when Z empty; it is forbidden there solely because r4 would drop to size1.
3. Thus a hypothetical native legality bit equals 1[Z nonempty], conditional on a nondestructive legality oracle actually being available.
4. The core projection R excludes |E4| and the legality oracle, so identical R inputs with opposite b refute any R-only computation of b.
5. If an independently derived retained slack exists, thresholding it recovers b. If a legitimate hypothetical legality query exists, it also recovers b. Neither is assumed to be present.
6. The six-edit and eight-edit shortest paths are inherited from independently closed hidden-optimality result, and do not depend on spectator identities.
7. Executing an inadmissible edit is not a legitimate nondestructive observation.
8. The result establishes conditional extractability and a precise interface obstruction, NOT observer access, universal information law, or physics.

Rejecting controls: empty Z versus Z={z}, identical R, tau=3 after hypothetical deletion in both, opposite floor legality.

Broader C3 remains open pending an actual source audit of existing native retained invariants.
