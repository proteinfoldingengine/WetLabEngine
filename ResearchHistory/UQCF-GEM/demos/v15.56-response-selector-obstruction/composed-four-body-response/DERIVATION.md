# v15.98 — composition, four-body exposure and source order

Question: can two individually pair-invisible source actions expose exact-weight-four information, and is exposure distinct from order sensitivity? This follows v15.97's weight-four null without changing it. Time remains ordered recoverability/pruning; u and v are source strengths.

Use the same frozen twelve four-qubit states and the same five-edge atlas. Each of 81 Hermitian probes h=P_a P_b P_c P_d/4 is invisible on every proper region before the source. Copy the existing two-site source to A on01, B on12, and D on23. Each copy uses P=ZI, Q=XX, A±=(P±Q)/sqrt2 and the unchanged v15.81 random-unitary weights. The coherent arm is lambda=+1, with L=Ad_Aplus-Id. AB means A first, B second; AD means A first, D second.

Each single two-site source leaves all retained pairs independent of h. At the two-source origin, the first potentially visible hidden derivative is

Y_AB=L_B L_A h, Y_BA=L_A L_B h.

All lower hidden pair derivatives and all one-body hidden derivatives through this order vanish. Hence the third mixed derivative (two source strengths and one hidden-state coordinate) of connected correlations is the pair moment of Y. The polar/loop chain rule has no Hessian or cross-product terms involving lower hidden derivatives. It equals the ordinary retained polar derivative applied to those moments, after local preparation. The order contrast uses Y_AB-Y_BA at the same baseline; it is a difference of two physical protocols, not itself a CPTP channel.

For overlapping sources, the union of supports is012 and qubit3 is untouched. The first loop on012 remains hidden-null. The second loop can respond through13 and30. Exact local cross leakage XX->ZI, ZX->XI, YY->-IZ, YZ->IY gives an order witness: for h=YYXX/4, the two-body part of Y_AB is -IXIX/4, while that of Y_BA is zero. Other words provide additional directions. The overlap order contrast is bounded by K rank3 and J rank2; on a fixed plane both ranks are at most1. These bounds are not assumed to be saturated.

The disjoint A,D sources commute, but their composition can reduce Pauli support twice. For h=XXXX/4, its retained two-body part after L_D L_A is ZIZI/4, nonzero. Thus exposure of four-body information need not require noncommutation. The geometry gate tests whether the disjoint exposure reaches both loop tangents and their invariant coordinates on this ensemble.

Define K6x81 from axial coordinates of delta H_r H_r^T for the two loops, and J3x81 from derivatives of (tr H1,tr H2,tr(H1 H2)). J avoids counting a pure frame change as an invariant signal. Compare both orders and their difference in the same frame. Edge23 must be reported separately: it is no longer an invariant spectator under sources on12 or23, and no v15.96 spectator-marginal null is inherited.

Finite channel identity: at lambda=1, Phi_u=Id+s(u)L with s(u)=(1-exp(-2u))/2. Since every lower pair restriction vanishes,

R_pair Phi_B(v) Phi_A(u) h = s(u)s(v) R_pair L_B L_A h.

This identity permits a stable finite global-state correlation check without a noisy third finite difference of loop matrices. Separately check the already derived polar/loop Frechet derivative using physical nearby states rho±eta Y. That affine tangent probe is numerical verification, not an additional physical source law.

No source is fitted or selected by this gate. It studies specified compositions on a deterministic inherited ensemble. CPTP composition remains associative; order dependence is noncommutation, not failure of associativity. No continuous SO(3) holonomy, admissible-world change or gravity is inferred. Genesis Pin and previous verdicts remain unchanged.
