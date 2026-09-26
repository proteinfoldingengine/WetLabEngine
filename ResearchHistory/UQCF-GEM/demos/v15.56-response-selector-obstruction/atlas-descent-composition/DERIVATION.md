# v15.70 Derivation before measurement

## 1. Descent is stronger than gluing

Let R be a partial trace. If R X(sigma)=x(R sigma), with fixed source data and differentiable x, then R DX_sigma[h]=Dx_{R sigma}[R h]. A hidden h in ker R therefore has zero retained response. This uses derivative linearity, not an extra neutrality assumption about a nonlinear label-to-lift assignment.

For the historical fixed-base field, put ell_h(z)=Tr(h z)/Tr(h^2), X(sigma)=ell_h(sigma-rho)Y and T_s(sigma)=sigma+s X(sigma). Since ell_h(h)=1,

    R T_s(rho+eta h)-R T_s(rho-eta h)=2 eta s RY.

Both input marginals are R rho. A nonzero RHS proves no single-valued regional map on marginal state alone can reproduce the update, even if differentiability is dropped. Holding all source labels fixed makes this a fiber witness, not a comparison of different sources.

The pair derivatives nevertheless glue on overlaps: Tr_i R_ij Y=Tr_j R_ij Y=0. Such consistent retained output data do not imply a marginal-only source assignment.

## 2. Exact lift and norms

Pauli strings divided by sqrt(8) are an orthonormal real basis for global traceless Hermitian tangents. The 36 constraints separately fix 9 weight-one and 27 weight-two coefficients. Minimum norm sets all 27 free weight-three coefficients to zero. For edge e with unit-Frobenius target D_e=O_e/sqrt(3),

    R_e Y = (1/4) sum_ab (D_e)_ab sigma_a tensor sigma_b.

Hence ||R_e Y||_HS=1/2, ||Y||_HS=sqrt(3/8), and all endpoint restrictions vanish. All full-support h_a are orthogonal to Y. These exact identities are predictions for independent partial-trace and matrix calculations.

## 3. Composition at one base point

For unit hidden h_a define N_a z=Y <h_a,z>. Then

    N_a N_b z=Y <h_a,Y><h_b,z>=0.
    (I+s N_a)(I+u N_b)=I+s N_a+u N_b.

Thus every pair commutes; each fixed-base one-parameter family is locally additive in its source parameter. This is stronger than testing two random frames but weaker than a base-point-independent source law. The family is nilpotent on the complete tangent space, not only on the selected perturbation.

For inputs rho+z with z entirely weight three, each retained connected correlation along the composed update is C_e+c O_e/sqrt(3)=O_e(P_e+c I/sqrt(3)). One-body moments are unchanged. While the last factor is positive, the polar rotation is exactly unchanged. Composition does not inevitably generate skew in this family.

Neither setting every local field to zero at its own moving center nor identifying N_{h+k} with N_h+N_k is justified. We do neither. The reference rho is fixed, and composition sums operators with their source amplitudes.

## 4. Scientific implication conditional on validation

An obstruction here rules out marginal-only naturality for this null family, while the theorem rules it out for any nonzero hidden leakage. It does not privilege rotational leakage. A confirmed fixed-base composition result would show that composition alone, in this precise sense, does not remove null freedom. Enriched source data and rebasing/integrability remain separate questions.
