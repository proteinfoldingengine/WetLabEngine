# Sixth-edge polar-domain argument

For the ideal historical mixture, the raw two-site Pauli moments on sites 2 and 3 vanish: each mixture term carries the maximally mixed identity on one of those sites. Let u and v denote their one-body Bloch vectors. Then the connected correlation is C23=-u v^T. Local product depolarization multiplies each one-body vector by a, and a diagonal unital preparation with Bloch map Q gives C23=-a² (Qu)(Qv)^T. This has rank at most one for every a.

For an archived binary state, let B be its actual raw 23 moment matrix. The exact expression is C23=a² Q(B-u v^T)Q^T. The audit retains B exactly, computes all minors, and does not replace B by the ideal zero. This distinguishes the ideal theorem from the stored-state result.

A rank-one matrix C=σ x y^T fixes the action of its polar transport on span(y), but does not fix a rotation on the perpendicular two-plane. Proper orientation still leaves a continuous SO(2) freedom. Equivalently, the polar derivative equation PΩ+ΩP=K has a zero coefficient for rotation within the two-dimensional null space of rank-one P. An arbitrary full orthogonal completion therefore introduces information not supplied by C.

The canonical support partial isometry x y^T is well-defined. It is not an invertible full link and does not satisfy the inherited full-link loop/derivative construction. A different observable based on partial transports would require its own definition, domain and covariance analysis. Rejection by this audit does not prove that every possible geometry on the edge is impossible.

The inherited plane solver uses a rank-two domain and the oriented cofactor completion. Its second singular value must exceed 1e-9 of the unprepared source reference, with its third at most 1e-11 of that reference. The inherited isotropic solver requires three singular values above 1e-9 of the same reference and a proper full polar factor. Tiny binary residues are not justification for lowering these gates. No source, state, loop or tolerance is changed in this audit.
