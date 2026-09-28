# Local normal-sign orbit and its spectral boundary

C and N transform as G C Hᵀ and G N Hᵀ under independent endpoint rotations. Unitary changes of qubit Pauli frames induce proper SO(3) rotations. The larger O(3) group would also admit reflections; it is not silently used as the physical gauge here.

For P=CC⁺ and a normal N=(I−P)N(I−Q), J=2P−I is orthogonal, JC=C and JN=−N. Its eigenvalues are +1 on the rank-r column support and −1 on the (3−r)-dimensional complement. Thus det J=(−1)^(3−r).

At r=1, J is a proper rotation. Taking G=J,H=I supplies a covariantly constructed sign-flip witness without a basis choice. Every SO(3)×SO(3)-invariant function of the local pair (C,N) consequently agrees on N and −N. This says nothing about the full set of neighboring edges, tangential derivatives or source channels, which are additional data.

At r=2, J is improper. If N has rank one and is nonzero, its initial/final support is the one-dimensional null complement. In support coordinates det(C+tN)=t alpha with alpha≠0. Determinant is invariant under proper independent endpoint rotations, so the two signs cannot be SO-equivalent. They remain O-equivalent via J. The invariant can be computed without selecting coordinates: alpha=cof(C):N.

For a rank-one C and rank-two N, det(C+tN)=t² beta. It is sign-even, consistently with the proper sign flip. For rank-one C and rank-one N, the pencil has rank at most two and its determinant vanishes. Norm(N)² is invariant and sign-even in every case; positive amplitude scaling between orders therefore remains distinguishable even where the isolated normal sign is gauge.

For the actual quadratic physical path, the first determinant coefficient is cof(C):V. Normal projection gives the same contraction because at rank two the cofactor lies entirely in the null-to-null component; at rank one the cofactor is zero. The first coefficient is thus λ alpha. At rank one, the second coefficient uses one active C direction and two normal directions, yielding λ² beta; a single W column cannot combine with two proportional C columns to give a nonzero determinant. The executable audit checks these statements against the actual V,W coefficients, not by declaring the normal pencil to be a physical density path.

Spectral qualification is essential. |alpha|≤||cof(C)||F ||N||F. At rank two, ||cof(C)||F=σ1σ2, so

`|alpha|/(||C||F² ||N||F) ≤ σ1σ2/(σ1²+σ2²)`.

This tends to zero as σ2/σ1→0. An exact orientation-sensitive witness can therefore depend on tiny stored rank-two residues. No rank truncation or sensitivity normalization can promote it to a robust physical signal. The mathematical rank classification is exact; experimental resolution and physical interpretation remain separate questions.

No external reference frame, source selector or geometry law is introduced. To retain a sign that is gauge for the local pair, a later network observable must use additional intrinsic relational data. It must test whether those data actually couple to the response rather than assuming that closing a loop preserves it. Time is pruning / ordered recoverability update.
