# Rank-stratum obstruction for canonical support polar transport

Let C be a real matrix of rank r, C+ its Moore-Penrose inverse, P=C C+ its column-support projector and Q=C+ C its row-support projector. For a proposed derivative V, put N=(I-P)V(I-Q), and k=rank(N). These definitions are basis independent. Under C↦G C H^T and V↦G V H^T with orthogonal G,H, N↦G N H^T.

Choose orthonormal support/null coordinates only for the proof. The baseline has blocks diag(A,0), with A invertible r×r. Any differentiable curve with C(t)=C+tV+o(t) has an invertible upper-left block near zero. Its Schur complement is tN+o(t): the product of the off-diagonal blocks contributes O(t²). For nonzero t sufficiently near zero, at least k singular values of the rescaled Schur complement remain positive. Hence rank(C(t))≥r+k. This argument does not choose physical frame axes or an orthogonal completion.

Define U(C) to be the canonical polar partial isometry, equal to zero on ker(C). Its nonzero singular values are all one and ||U(C)||_F²=r. If a nearby matrix has rank r'≥r+k, the von Neumann trace inequality gives Re tr(U(C)^* U(C(t)))≤r. Therefore

    ||U(C(t))-U(C)||_F² ≥ r'+r-2r = r'-r ≥ k.

A nonzero exact N forces a finite discontinuity, even if its magnitude is small. This is a local asymptotic theorem; the size of the neighborhood can depend on the smallest supported singular value and the normal magnitude. It supplies no finite-step scale or numerical robustness claim for tiny binary residues.

If N=0, the direction is tangent to the rank-r manifold and is compatible with some constant-rank matrix curve. It does not certify the actual source path. In particular, the straight pencil C+tV may gain rank at order t² while a curved path with the same derivative keeps rank fixed. Example: C=diag(1,0), V=[[0,1],[1,0]]. The pencil has determinant -t², but [1,t]^T[1,t] has constant rank one and the same baseline and derivative. This audit cannot infer a forced obstruction from pencil rank alone.

The inherited D direction is a connected differential of a prepared commutator contrast. It is a difference of ordered-channel derivatives. A difference direction is not automatically the derivative of an admissible physical source path. The theorem applies conditionally to any differentiable matrix path whose own derivative equals that D direction; it does not establish such a physical path exists, nor that either individual ordered-channel path has that derivative.

The conclusion concerns canonical zero-on-kernel support polar transport. It does not cover arbitrary full orthogonal completions, and it does not prohibit every scalar observable that might remain smooth despite transport discontinuity. No replacement geometry is introduced here. Time is pruning / ordered recoverability update.
