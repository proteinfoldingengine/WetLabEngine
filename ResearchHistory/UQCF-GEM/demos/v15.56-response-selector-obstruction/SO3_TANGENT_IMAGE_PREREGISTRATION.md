# SO(3) tangent-image theorem gate

Frozen before implementation.

For the closed-form mixed loop response K at a base holonomy H in SO(3), test two logically separate statements.

1. Tangency theorem.
Because every edge polar factor O_e lies in SO(3), the loop H is in SO(3). Differentiating H^T H = I implies H^T K is skew-symmetric for every mixed hidden/source direction after the lower-order mixed product rule is included. Therefore image(Ktilde) is contained in H so(3), giving rank at most 3.

The implementation must verify the closed-form identity numerically on all 243 basis columns and all 11 fixtures, with max symmetric-part residual <= 1e-10 relative to column norm.

2. Surjectivity gate.
Project each response column to the three independent coordinates of Omega = H^T K in so(3). Compute the 3 x 243 projected operator rank at relative threshold 1e-10. Require rank 3 on all 11 fixtures to certify that the response fills the complete tangent space rather than a smaller subspace.

Controls:
- reconstruct the original 9-entry response matrix from H Omega with relative error <= 1e-10;
- projected rank invariant under deterministic orthogonal basis changes in hidden/source input spaces;
- no finite-difference response columns and no fitted parameters.

Verdicts:
SO3_TANGENT_IMAGE_SURJECTIVE if tangency and projected rank 3 hold on all fixtures.
SO3_TANGENT_IMAGE_NONSURJECTIVE if tangency holds but any projected rank is below 3.
SO3_TANGENCY_FAILS if tangency fails.
INVALID if controls fail.

Claim boundary: this establishes the exact geometric codomain of the already-derived finite response map. It does not select a microscopic hidden completion or source and does not establish physical gravity.
