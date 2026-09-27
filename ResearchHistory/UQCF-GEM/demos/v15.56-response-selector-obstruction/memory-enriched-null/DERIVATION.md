# v15.71 Derivation before implementation

Let rho be a full-rank three-qubit state with each connected-correlation polar decomposition C_e=O_e P_e, det(O_e)=+1, P_e>0. Work on this open regular domain. Full-support h is fixed source data, Hermitian, HS-unit, and traceless on every proper marginal. Write

    Y(rho) = (1/(8 sqrt(3))) sum_e,ab (O_e)_ab Pauli_e,ab.
    m_h(rho) = Tr(h rho).
    X_h(rho) = m_h(rho) Y(rho).

The first expression is the historical minimum-HS-norm lift: one-body coefficients zero, fixed two-body targets O_e/sqrt(3), unconstrained weight-three coefficients zero. Restricting to edge e gives

    y_e(rho_e) = (1/(4 sqrt(3))) sum_ab (O_e(rho_e))_ab sigma_a tensor sigma_b.

Other edge terms vanish under that partial trace. All endpoint partial traces vanish.

## Hidden derivative and origin

Y depends only on proper marginals, so DY[h]=0. Therefore

    DX_h[rho](z) = Tr(h z)Y(rho) + m_h(rho) DY[rho](z),
    DX_h[rho](h) = Y(rho).

This is one differentiable field on the regular state domain, not a collection of fields zeroed at their own reference points. At a hidden-free base rho0, m_h(rho0)=0. Along pure-hidden offsets with the same marginals, it agrees with the historical affine field. For all 27 sources simultaneously, hidden-free means all weight-three coefficients vanish. It does not agree with the old zero-centered field at an arbitrary base with m_h(rho0) nonzero.

## Exact local source flow and composition

Y has weight two, so Tr(hY)=0 and every m_h is conserved under all these sources. Along Y, one-body derivatives vanish and dC_e=O_e/sqrt(3); the polar Sylvester equation gives dO_e=0, hence DY[Y]=0. Thus X_h is constant along its own local integral curve:

    T_s^h(rho) = rho+s m_h(rho)Y(rho).

This is the exact local flow as long as density positivity and positive-polar regularity persist. Source parameters are ordered repair labels, not fundamental time. All X_h are scalar multiples of the same Y with mutually conserved coefficients, so their brackets vanish. Re-evaluated sequential updates agree with combined increments; no fixed reference point is needed. A scalar c changes C_e to O_e(P_e+c I/sqrt(3)), leaving rotations unchanged while that last factor stays positive.

## Enriched restriction

Define the retained source-state object as (rho_R,m_h), carrying m_h through restriction. The regional source vector is (m_h y_R(rho_R),0). Then

    enriched_Res_e T_s^h(rho) = regional_T_s(enriched_Res_e(rho)).

For two sources carry both memories. The edge-to-node restriction has zero state source component and unchanged memory; overlapping edges agree. This does not contradict the marginal-only obstruction: m_h is extra global information, not a function of rho_e. If the memory is deleted, the prior unequal-output/equal-input witness remains.

## Why the complete old Jacobian need not integrate

The historical rank-one assignment N_rho[z]=Y(rho)Tr(hz) specifies zero visible derivatives. If it were the full Jacobian of a C2 field, its derivative would obey symmetry of mixed derivatives. For any pure weight-two v,

    D_v N[h] - D_h N[v] = DY[v].

Whenever this is nonzero the full assignment cannot be integrated unchanged on an open neighborhood. Each edge polar differential has three rotational degrees of freedom; the complete weight-two input domain covers all 27 pair-correlation components and the edge lifts are independent, predicting rank nine for this curl map on the regular stratum.

The completed field X_h=m_h Y adds exactly m_h DY[z] to the full Jacobian. Its hidden derivative remains the desired Y; its mixed derivatives agree. A nonzero curl for N is therefore consistent with existence of X_h. This separates preserving a measured hidden-sector derivative from preserving every derivative of a reference-centered construction.

## Scientific limits

The existence proof is conditional on granting the memory and using the already engineered Y. All source fields are pointwise collinear with Y; 27 source labels do not mean 27 independent flow directions. Curl rank nine is a derivative-space rank, not the dimension of these flows. Under a local frame change both rho and the explicit source h must transform. The construction cannot supply a physical source-to-consistency law, select a skew sector, or establish gravity. It addresses restriction and base-point consistency on this regular domain only; extension through singular strata and tensor-product composition remain open.
