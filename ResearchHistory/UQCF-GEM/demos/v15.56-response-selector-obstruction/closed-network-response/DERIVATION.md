# Closed-network derivative and its normal attribution

Let Cij map the real Pauli-coordinate space at j to that at i, with Cji=Cijᵀ. For a simple cycle gamma=(i0,...,iL−1), define I_gamma=tr(C_i0i1 ... C_iL−1i0). These connected correlations are not declared unitary transport links.

Under independent orthogonal local frames Cij→Gi Cij Gjᵀ, neighboring frames cancel and the cycle product transforms by conjugation at its root. Its trace is invariant under O(3)^4, hence also the physical SO(3)^4 frame group. The choice of root is immaterial by cyclicity; reversal transposes the product and preserves the trace. The seven cycles are exactly the four triangles and three unoriented four-cycles of K4.

For a physical path C_e(s)=C_e+sV_e+O(s²), differentiate the trace by inserting V at each edge once and summing. This has no inverse, polar factor, division by a gap, or discontinuous normalization. Its full derivative is a polynomial in the baseline matrices and linear in the derivative matrices.

If local frames also depend smoothly on s, their skew generators add Ki Cij−Cij Kj to V. These terms telescope around the loop into a root commutator [K_root, product], whose trace is zero. Normal projection of these extra edge terms also vanishes: (I−P)(Ki C−C Kj)(I−Q)=0. Consequently the normal contribution as well as the full derivative is intrinsic within the fixed baseline rank stratum.

Let G_gamma be the Frobenius gradient of I_gamma with respect to C23. For a forward occurrence of edge23, G is the transpose of the complementary open-chain product; for a reversed occurrence it is that product. It is zero for cycles omitting edge23. Given P=CC⁺ and Q=C⁺C and the archived N=(I−P)V_plus(I−Q), define H=(I−P)G(I−Q). Then

    <G, lambda N>_F = lambda <H,N>_F,
    |lambda <H,N>_F| <= |lambda| ||H||_F ||N||_F.

The sixth-edge derivative decomposes into lambda N and its tangent remainder; all other edge contributions are separately summed. A nonzero normal contribution can cancel against the remainder. Therefore normal-contribution and full-observable results are reported independently, including zero-coherence and source-reversal coefficients.

Continuity of the full observable does not establish robustness of a rank-dependent decomposition across a rank change. P, Q and N are conditioned on the exact archived rank; no tiny singular direction is truncated or inflated, and the 16.13 rank-two orientation caveat persists. The polynomial response obeys a finite product bound: |dI| <= sum_e ||V_e||_F product_(f≠e)||C_f||_F. A nonzero exact rational derivative alone is not a robust physical effect.

The derivative parameter s is channel strength, not fundamental time. The inserted source is a specified CPTP model; gauge invariance does not derive sourcehood, a metric, a connection, curvature or gravity.
