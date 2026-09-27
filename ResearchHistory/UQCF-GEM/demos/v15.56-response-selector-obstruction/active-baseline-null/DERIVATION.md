# Nonzero baseline action does not force rotation

For each reference rho in the existing positive ensemble, let Y be the frozen global lift with pair moments O_e/sqrt(3) and zero one-body/hidden moments. Its HS norm is sqrt(3/8). Set b=rho+deltaY, delta=.02. The measure-and-prepare channel with outputs b±kappaY, kappa=.01, is CPTP: the selector guarantees lambda_min(rho)>=.025, while (delta+kappa)||Y||HS=.03 sqrt(3/8)<.018372. Thus the prepared states have strictly positive lower bound before measurement.

The source field at its reference is X(rho)=Phi_b(rho)-rho=deltaY, a nonzero global and retained action. The reference is not fixed. Because Tr(A rho)=Tr(A Y)=0, the v15.76 algebra still applies: Phi_b²=D_b and
T_b^n=alpha id+(1-alpha)D_b+beta N,
where N(z)=kappa Tr(Az)Y, alpha=(1-s)^n and beta=n s(1-s)^(n-1).

The output center is rho+(1-alpha)deltaY. Its one-body moments are unchanged, so its connected pair matrices are
C_e(n)=O_e[P_e+(1-alpha)delta/sqrt(3) I].
For the active normalized XXX hidden probe, finite signed inputs produce
C_e(n,±)=O_e[P_e+((1-alpha)delta ± eta beta kappa sqrt(8))/sqrt(3) I].
Whenever the bracket is positive, all these polar factors are exactly O_e. The center moves and hidden leakage remains nonzero, but rotation does not respond. The other hidden probes remain fully hidden. This disproves the necessity of a fixed reference center for a calibrated composition-stable null, without asserting a baseline rotational action.

For the comparison, define Z=(sqrt(3)/8)sum_ab(O_01 K)_ab sigma_0^a sigma_1^b with K skew and HS norm one. Pauli orthogonality gives ||Z||HS=sqrt(3/8), matching Y. Its only pair moment is sqrt(3)O_01 K. The equal-norm baseline deltaZ therefore has Q norm 2sqrt(3)delta at the reference, while deltaY has Q=0. The prepared states rho+deltaZ±kappaY satisfy the same triangle-norm positivity bound. This comparison tests whether an equally active skew baseline changes the fixed leakage's observability after finite updates; it is not used to fit a favorable channel.

Every reference supplies distinct source data (rho,Y,Z). Once supplied, each source is a fixed affine CPTP map, and its powers compose. The ensemble is a family of independently calibrated laws, not one universally null law across a full-dimensional state neighborhood. Thus the construction remains consistent with v15.75. Calibration dependence and the selection of a physical source remain unresolved. Update count is ordered source depth, not fundamental time.
