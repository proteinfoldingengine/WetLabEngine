# v15.77 — Active retained baseline with composition-stable null

Parent: 45cbd56c4833dce1757735fcd175275a0c19780b.
Branch: research/v15.77-active-baseline-null.
No v15.77 measurement before missing-implementation RED.

## Question and frozen family
Does the v15.76 null require the source to fix its reference state? Use all twelve unchanged reference candidates [13,16,22,25,27,29,37,39,46,50,66,77]. For each reference rho, compute Y=global_lift(rho) ONCE. Each reference defines a separate fixed channel family: do not describe the twelve calibrations as one fixed law across an open state set. Use A=XXX, kappa=.01, delta=.02, s=.1, eta=1e-4, depths [1,2,4,8], all 27 historical normalized hidden Pauli probes. No new seeds or state selection.

Phi_b(z)=Tr(z)b+kappa Tr(Az)Y; T_b=(1-s)id+sPhi_b.

Three separately frozen prepared-state centers:
- fixed: b=rho (v15.76 fixed-point control).
- active_symmetric: b=rho+delta Y (primary new channel).
- active_skew: b=rho+delta Z (equal-HS-norm positive comparison).

Define K01=1/sqrt(2), K10=-1/sqrt(2), all other K entries zero. Z=(sqrt(3)/8) sum_ab (O_edge01 K)_ab sigma_0^a sigma_1^b, using the reference polar factor and only edge (0,1). Both Y and Z have norm sqrt(3/8), zero one-body and hidden moments. Their reference baseline source fields are delta Y and delta Z, equally nonzero in retained HS norm. Only the skew control has nonzero baseline polar action. These are engineered counterexamples/controls, not source laws derived from recoverability.

Freeze all source data per reference before updates. Run 12*3*4*27=3888 finite channel/depth/probe cases; 144 channel/depth rows. The original b=I/8 channel and its v15.76 negative verdict are not changed or rerun as a rescue.

## Measurements and scientific gates
At each depth recursively obtain center rho_n=T_b^n(rho), hidden tangents T_b^n(h), retained coefficient matrix in the v15.75 36-element HS basis, and analytic Q/E hidden-response maps at the output center. No small-step mixed polar finite differences. Let q=||Q||/||retained|| and e=||E||/||retained||.

Primary confirmation requires, for every active_symmetric reference/depth: reference baseline field norm and retained baseline norm >1e-6, center displacement >1e-6, hidden retained norm >1e-6, q,e<=1e-10, and undivided polar-factor shift from original O for both signs of every finite hidden probe <=1e-10. Verdict ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_CONFIRMED or ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_NOT_CONFIRMED if valid.

Secondary comparison confirmation requires for every active_skew reference/depth: hidden retained norm >1e-6 and both q,e>=1e-6. Verdict EQUAL_NORM_SKEW_BASELINE_VISIBLE_CONFIRMED or EQUAL_NORM_SKEW_BASELINE_VISIBLE_NOT_CONFIRMED if valid. This is a scientific comparison, not a condition silently included in numerical validity. A valid negative in either gate must be preserved.

Failure of frozen numerical validity means INVALID for both verdicts. Tests accept both valid outcomes of each gate.

## Exact predictions and validity controls
With alpha=(1-s)^n, beta=n s (1-s)^(n-1), T_b^n(z)=alpha z+(1-alpha)Tr(z)b+beta kappa Tr(Az)Y. Only the XXX hidden probe leaks, with retained norm beta*kappa*sqrt(8)*||Y||. Its baseline action is independent of hidden probe amplitude.

For active_symmetric: center rho+(1-alpha)deltaY; connected correlations O[P+(1-alpha)delta/sqrt(3) I]. Finite active hidden probes add ±eta beta kappa sqrt(8/3) I to the positive factor. For active_skew, center correlations on edge01 are C0+(1-alpha)delta sqrt(3) O0 K, and other edges stay C0. One-body vectors do not move in any arm.

Numerical validity thresholds, frozen in advance:
- Reference indices and 144/3888 row/case coverage exact; no nonfinite outputs.
- Y and Z trace/Hermiticity errors, one-body/hidden moment norms <=1e-12; both HS norms agree with sqrt(3/8) within 1e-12. Tr(A rho), Tr(A b), Tr(A Y) <=1e-12. Y/Z retained pair moments agree with O/sqrt(3) on all edges and sqrt(3)OK only on edge01, respectively, within norm 1e-12.
- Actual reference field Phi_b(rho)-rho agrees with b-rho within norm 1e-12. Retained/global baseline norms equal delta sqrt(3/8) for both active arms within 1e-12. For baseline polar extraction, fixed and active_symmetric Q/E norms <=1e-10; active_skew Q norm equals 2 sqrt(3) delta within 1e-12 and E norm >1e-6.
- Prepared states b±kappaY: positive normalized Hermitian, eigenvalue >=-1e-12, trace/Hermiticity errors <=1e-12. Choi of every Phi_b and T_b^n: minimum eigenvalue >=-1e-12, Hermiticity and output partial trace errors <=1e-12 (v15.75 convention). Full Choi spectra archived.
- Phi_b^2=D_b, recursive versus closed powers on all 64 complex matrix units, and composition T^n(T^m) versus closed T^(n+m) for n,m in [1,2,4], each max Frobenius error <=1e-12.
- Recursive centers, hidden tangents, retained coefficient matrices and active leakage norms versus closed forms <=1e-12. Other hidden retained columns norm <=1e-12. Correlation formulas above within 1e-12; independent closed-form Q/E predictions within 1e-10. Sylvester residual <=1e-10.
- Every center, input rho±eta h and composed output: density eigenvalue >=-1e-12, trace/Hermiticity error <=1e-12; every polar matrix used positive-proper, minimum correlation singular value >=1e-4 (same finite-output floor as v15.76).
- fixed arm control at all references/depths: center displacement <=1e-12, retained norm >1e-6, q,e<=1e-10, undivided finite endpoint polar shift from reference <=1e-10.
- Independent positive-skew observable control at every output edge: dC=O K must give Q norm 2 within 1e-12 and E norm >1e-6.

Unexpected programming errors fail CI and receive implementation-only fixes. No criterion, amplitude, reference or source law changes after the result. Python3.11, numpy2.3.5, OPENBLAS_NUM_THREADS=1.

Nonzero retained baseline action is not nonzero baseline rotation. The primary construction intentionally remains inside the calibrated polar-symmetric sector. No open-state robustness, marginal-only naturality, source selection, gravity, new matter primitive, external alignment or fundamental time is inferred. Genesis Pin and historical verdicts remain intact.
