# v15.74 — Open-state Hamiltonian null theorem

## Statement
Fix a three-qubit Hermitian H, independent of rho. Let h run through all 27 full-support Pauli tangents. On any nonempty full-dimensional open set of full-rank density matrices with invertible positive-polar retained correlations on all three edges, suppose the polar rotational derivative from Y_h=-i[H,h] vanishes for every rho and every h. Then H is a sum of one-body terms and a scalar identity. Conversely these terms always have zero retained hidden response.

This theorem concerns state-independent unitary generators and this retained observable. It does not classify arbitrary operational source laws.

## Proof
Write a_i for the one-body Bloch vectors. For fixed H,h, let u_i be one-body moments of Y_h and V_ij its raw pair moments. These quantities are independent of rho. The connected-correlation variation is

D_ij(a)=V_ij-u_i a_j^T-a_i u_j^T.

In a full-rank physical neighborhood, all Pauli moment coordinates can be varied independently by sufficiently small amounts. The coordinate change from raw pairs to connected C_ij=raw_pair-a_i a_j^T is invertible locally. For invertible positive-polar C_ij=O_ij P_ij, O_ij can vary over an open neighborhood of SO(3) independently of a_i and with P_ij held fixed. Small such changes remain within the assumed physical open set.

For fixed a, D_ij does not depend on O_ij. Null rotation is equivalent to O^T D-D^T O=0 because the positive Sylvester operator is invertible. If this holds for an open set of O, put S=O0^T D, which is symmetric, and vary O=O0 exp(tK) for arbitrary skew K. Differentiating the symmetry equation at zero gives KS+SK=0 for every skew K. Diagonalizing S gives lambda_i+lambda_j=0 for each pair i!=j. In dimension three these equations force all eigenvalues to zero. Thus D=0.

Therefore V_ij-u_i a_j^T-a_i u_j^T=0 throughout an open box of independently varying Bloch vectors. Differentiate with respect to a_j while holding a_i fixed: u_i x^T=0 for every x, so u_i=0. Similarly u_j=0; then V_ij=0. Across all edges, every retained one-body and pair moment of [H,h] vanishes for every full-support h.

To identify H, use the adjoint identity Tr(O Y_h)=i Tr(h[H,O])=i Tr(H[O,h]). For each weight-three Pauli coefficient of H, choose a one-body observable O and full-support h differing on precisely O's site so [O,h] is a nonzero multiple of that weight-three Pauli. Orthogonality then forces that coefficient to vanish. For each weight-two Pauli coefficient of H, choose a pair observable O and full-support h that match on one shared site, differ on the other, and leave the third site untouched by O; [O,h] is a nonzero multiple of the desired weight-two Pauli. Such choices exist for every target. Thus all weight-two and weight-three coefficients vanish. Weight-one commutators with full-support h remain full support; their retained moments vanish, proving the converse. QED.

No analytic continuation to a zero-Bloch point is needed. The full-dimensional openness assumption is essential: at zero Bloch vectors, every weight-three generator has zero connected-correlation derivative despite nonzero one-body leakage for suitable h.

## Finite-state classification
At a fixed state the map is linear in the 63 real nonidentity H coefficients. The 243 output rows enumerate 27 hidden probes and nine edge skew coordinates. Source coefficients are shared across those probes. Stacking frozen states tests whether a SINGLE interacting generator can remain null at all of them. A rank-54 interacting stack excludes every nonzero interacting coefficient combination at the stated numerical thresholds. It does not select a preferred generator or show that every source must be interacting.

Weight-two-only injectivity can also be proved at any one positive-polar state. For an edge, fix the omitted hidden index and let Z range through arbitrary 3x3 hidden matrices on the edge. The retained response has form A Z+Z B, with A,B skew matrices encoding the two crossing pair couplings (signs absorbed into A,B). Set W=O^T Z and A'=O^T A O. Polar-null for all Z requires skew(A'W+WB)=0 for all W. W=I gives B=-A'. Choosing all skew W then requires [A',W]=0 for every skew W, forcing A'=0 and B=0 in so(3). Repeating over the omitted index and edges kills every pair coupling. Hence the 27 weight-two coefficient columns have rank 27. The full interacting stack test additionally excludes cancellations involving weight-three terms.

## Exceptional-state fixture
For epsilon=.04, rho0=(I+epsilon sum_{edges,a} sigma_i^a sigma_j^a)/8 is positive since the perturbation operator norm is at most 9 epsilon=.36<1. It is normalized and has a_i=0, C_ij=epsilon I. Weight-three H with full-support h produces weight-one or weight-three Y, never weight two; hence D_ij=0 here even when one-body leakage is nonzero. This is a deliberate control against claiming that a single-state rotational null implies a local generator.

The second control adds beta X on qubit 1, beta=.02, in the numerator. H=XXX/2 and h=YXX/sqrt(8) give Y=ZII/sqrt(8), so D_01=-sqrt(8) beta e_z e_x^T. Consequently ||Q_01||_HS=4 beta=.08 and ||W_01||_HS=.08/(2*.04)=1. The other edges have zero response. Its density remains positive by the same norm bound, now .38<1.
