# Corrected mixed-orthogonality quotient theorem gate

Frozen after the rank-three image decomposition returned PURE_SKEW on all 11 fixtures.

Let H(eta,s) be an orthogonal loop holonomy. At the base point define:
He = partial_eta H, Hs = partial_s H, Hes = partial_eta partial_s H.

Differentiating H^T H = I twice gives the exact mixed identity:
H^T Hes + Hes^T H + He^T Hs + Hs^T He = 0.

Therefore the raw mixed derivative need not be tangent by itself. Its symmetric left-translated component is fixed by lower-order cross terms:
sym(H^T Hes) = -1/2 (He^T Hs + Hs^T He).

Define the corrected mixed response
Q = H^T Hes + 1/2 (He^T Hs + Hs^T He).
The theorem predicts Q is exactly skew-symmetric.

For the hidden/source response quotient, construct Q for all 27 x 9 basis pairs using closed-form first and mixed derivatives only.

Tests on all 11 fixtures:
- exact mixed orthogonality residual <= 1e-10 relative;
- corrected Q symmetric residual <= 1e-10 relative;
- 3 x 243 skew-coordinate map has rank exactly 3;
- reconstruction Hes = H [Q - 1/2(He^T Hs + Hs^T He)] <=1e-10 relative;
- no finite-difference response columns and no fitted parameters.

Then compare the corrected skew-coordinate image with the previously observed PURE_SKEW rank-three image by projector principal-angle residual <=1e-10.

Verdicts:
CORRECTED_SKEW_QUOTIENT_THEOREM_VERIFIED
CORRECTED_SKEW_QUOTIENT_NONSURJECTIVE
MIXED_ORTHOGONALITY_IDENTITY_FAILS
INVALID

Claim boundary: this is a finite retained-holonomy response theorem. It does not derive the Genesis selector, physical spacetime, or gravity.
