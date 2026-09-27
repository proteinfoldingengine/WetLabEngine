# v15.76 — CPTP pointwise null under finite composition

Parent certified head: 07170c00ebb63e17e8be5d6d88f0ba1ca8e42dc7.
Branch: research/v15.76-cptp-null-composition.
No v15.76 measurement before clean missing-implementation RED.

## Frozen channels and scope
Load the unchanged 12-state selector and verify indices [13,16,22,25,27,29,37,39,46,50,66,77]. This experiment uses the existing pointwise-null reference candidate 13, denoted rho0. No new random selection. All 27 hidden probes are the historical lexicographic weight-three h=P/sqrt(8). Freeze A=XXX, kappa=.01, s=.1, eta=1e-4, depths n=[1,2,4,8]. Y is v15.71 global_lift(rho0), computed ONCE and held fixed for every input and depth.

Phi_b(z)=Tr(z)b+kappa Tr(Az)Y, T_b(z)=(1-s)z+s Phi_b(z).

Primary channel: b=I/8, exactly the v15.75 pointwise channel. Separate matched control: b=rho0. This changes only the prepared-state center and is a NEW, explicitly labeled channel. Never substitute its verdict for that of the original channel. Both are measure-and-prepare channels with outputs b±kappa Y. The anchored channel fixes rho0: it has zero baseline source field there but a nonzero hidden response. It is an engineered existence control, not a selected physical source law.

Evaluate all 2*4*27=216 channel/depth/hidden cases. Depth one is a finite-strength baseline; if the original null fails there, do not attribute its first failure to multiple-update composition. Depth is an ordered source-update count, not fundamental time.

## Measurement
Repeatedly apply the frozen T_b to rho0 and each h to obtain output center rho_n and hidden derivative Z_n=T_b^n(h). Compute global retained moments of Z_n, connected derivative at rho_n, pre-Sylvester Q and polar E. Archive each 9-by-27 Q/E map and 36-by-27 retained HS coefficient map. Ratios q=||Q||_F/||retained||_F and e=||E||_F/||retained||_F use all hidden columns at a given depth.

The measured object is the hidden derivative of the finite composed channel at its output geometry. It is not DX at the original anchor. Use analytic derivatives; no small-step mixed polar finite-difference rank gate.

## Primary scientific verdict
Require retained norm >1e-6 at every depth to claim either a null or its obstruction. If all q and e <=1e-10 -> FROZEN_CHANNEL_FINITE_NULL_CONFIRMED. If at least one depth has both q and e >=1e-6 -> FROZEN_CHANNEL_FINITE_NULL_OBSTRUCTED. Otherwise -> FROZEN_CHANNEL_FINITE_NULL_UNRESOLVED. Report depth one separately and identify the first tested visible depth. Failed numerical validity -> INVALID. Do not tune the gap between the fixed null and visibility tolerances.

## Separate anchored-channel gate
ANCHOR_FIXED_CPTP_COMPOSITION_NULL_CONFIRMED requires at every depth: retained norm >1e-6; q,e<=1e-10; center displacement from rho0 <=1e-12; and for every input rho0±eta h the undivided polar-factor difference from the original O0 <=1e-10. Otherwise ANCHOR_FIXED_CPTP_COMPOSITION_NULL_NOT_CONFIRMED, provided numerical validity passes; else INVALID.

No requirement is made that the original channel stay null or become visible. Tests accept all valid primary outcomes and both valid secondary outcomes.

## Frozen identities and validity controls
Write alpha=(1-s)^n, beta=n*s*(1-s)^(n-1). Analytic formula for arbitrary matrices:
T_b^n(z)=alpha*z+(1-alpha)*Tr(z)*b+beta*kappa*Tr(Az)*Y.

- Tr(b)=1, Hermiticity and trace-zero Y, Tr(Ab)=Tr(AY)=0 within 1e-12. Y norm agrees with sqrt(3/8) within 1e-12.
- b±kappa Y positive normalized Hermitian: density minimum eigenvalue >=-1e-12, trace/Hermiticity errors <=1e-12. Choi matrices of each Phi_b and each T_b^n use the v15.75 input-first convention. Choi minimum eigenvalue >=-1e-12; Hermiticity and output-partial-trace identity errors <=1e-12.
- Compare recursive T_b^n with closed form on all 64 complex matrix units at all primary depths: max Frobenius error <=1e-12. Verify Phi_b^2(z)=Tr(z)b on those units within 1e-12.
- Verify composition on all 64 matrix units for n,m in [1,2,4]: T_b^n(T_b^m(z)) equals the closed formula for n+m within 1e-12. Sums 3,5,6 are identity checks, not new primary depths. This is composition of a fixed step, not source-strength additivity.
- Independently verify recursive center, global hidden derivatives and retained coefficient map against closed forms within 1e-12. Active XXX retained norm matches beta*kappa*sqrt(8)*||Y|| within 1e-12; other hidden retained columns have norm <=1e-12.
- Inspect each center and rho0±eta h and all their composed outputs: density minimum eigenvalue >=-1e-12; trace/Hermiticity errors <=1e-12. All polar factors used must be proper with positive P and minimum connected-correlation singular value >=1e-4. This frozen floor permits finite correlation contraction; no inherited .015 output floor is imposed.
- Maximum Sylvester residual <=1e-10. Independently verify retained response against the closed-form retained tangent beta*kappa*Tr(Ah)Y and original-center formula C_n=alpha*C0+alpha*(1-alpha)*a_i*a_j^T (original channel), or C_n=C0 (anchored channel), within 1e-12 for correlations and 1e-10 for Q/E.
- Positive skew control: for each output center and edge use dC=O K, K01=1/sqrt(2), K10=-1/sqrt(2), others zero. Require Q norm agrees with 2 within 1e-12 and E norm >1e-6. This ensures the rotation observable has not been disabled.
- Missing coverage, nonfinite data, or failed numerical controls -> INVALID. Unexpected programming defects fail CI and must be fixed separately without changing criteria.

Python 3.11, numpy==2.3.5, OPENBLAS_NUM_THREADS=1. Full matrices, scalar diagnostics, source/channel identities and exact provenance will be archived. Prior verdicts remain unchanged. Neither channel is derived from Genesis Pin, nor is geometry an inserted explanatory primitive: the reference-dependent construction is only a counterexample control. No gravity or admissible-world modification is claimed.
