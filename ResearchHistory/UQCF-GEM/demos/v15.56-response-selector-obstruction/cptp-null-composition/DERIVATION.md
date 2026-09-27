# Composition of fixed measure-and-prepare channels

Let D_b(z)=Tr(z)b and N(z)=kappa Tr(Az)Y. Here Tr(b)=1, Tr(Y)=0, Tr(Ab)=0 and Tr(AY)=0. Hence D_b^2=D_b, D_bN=ND_b=N^2=0 and Phi_b=D_b+N satisfies Phi_b^2=D_b. With r=1-s,

T_b^n=r^n id+(1-r^n)D_b+n s r^(n-1)N.

This follows by writing id=D_b+(id-D_b) and binomial expansion on the complementary subspace, where N is nilpotent of order two. It holds for arbitrary matrices, not only states. Integer powers compose exactly. The parameter s is a source mixing weight; n is ordered update depth.

Both choices b=I/8 and b=rho0 give CPTP Phi_b because M_±=(I±A)/2 are a POVM and tau_±=b±kappa Y are density matrices. For the anchored choice, the frozen selector ensures lambda_min(rho0)>=.025, while kappa||Y||HS=.01 sqrt(3/8)<.006124, so both prepared states are positive. T_b and every power are CPTP. This argument does not select either channel as fundamental physics.

For the reference rho0, which has zero hidden moments, the composed center and hidden derivative are

rho_n=b+alpha(rho0-b),
Z_n=alpha h+beta kappa Tr(Ah)Y,
alpha=(1-s)^n, beta=n s (1-s)^(n-1).

Only h=XXX/sqrt(8) has Tr(Ah)=sqrt(8); all other probes have zero retained response. Thus the hidden-to-retained Q/E map has rank at most one, not nine. The calibration lift has one-body moments zero and pair moments O0/sqrt(3) on each edge.

## Original channel: output geometry can drift

For b=I/8, a_i(n)=alpha a_i(0) and raw pair moments scale by alpha. Thus
C_n=alpha C0+alpha(1-alpha)a_i(0)a_j(0)^T.

The second term can change O_n. The retained hidden derivative still points along the fixed O0 direction, so its skew is proportional to O_n^T O0-O0^T O_n, which need not vanish. This is a finite-strength prediction to test for the frozen anchor, not a theorem of visibility for every possible anchor. At n=1 it already compares the fixed response with the moved output geometry; visibility there must not be described as first caused by repetition.

## Anchored channel: an exact finite null

For b=rho0, the center remains rho0 at every depth. For the active hidden probe and the signed finite states,

C_n,±=O0 [P0 ± eta beta kappa sqrt(8/3) I].

Provided the bracket remains positive, both polar factors are exactly O0. There is nonzero retained leakage for every finite positive depth in the frozen ladder, while the rotational response and finite polar change vanish. The other hidden probes have zero retained response. This is a fixed physical channel, with no recomputation of the lift after any update.

The anchored channel has zero source field at the reference state itself; its nontrivial response acts on hidden perturbations. Its composition-stable null is confined to the calibrated reference/fiber and does not contradict v15.75's full-dimensional open-state theorem. It supplies an engineered existence example, not a natural source selection or marginal-restriction theorem.
