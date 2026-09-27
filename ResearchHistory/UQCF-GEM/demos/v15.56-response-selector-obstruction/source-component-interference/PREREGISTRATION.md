# v15.81 preregistration — matched component interference

Frozen before gate.py exists and before new scientific measurement.
Parent f7bf2826e6952dae11ae67d548423911ecf94151.
Branch research/v15.81-source-component-interference.

## Inputs and measurement

Implement DERIVATION.md. Freeze P=ZII,Q=XXI; lambdas[-1,-.5,0,.5,1];
base source strength .1; retained-order depths[1,2,4,8], u=.1*depth;
hidden perturbation eta=1e-4 used only for positivity controls, never finite
response differences. All27 normalized hidden Paulis and the inherited12
states with indices[13,16,22,25,27,29,37,39,46,50,66,77]. No reselection,
random seed, fitting, or amplitude adjustment. 60 generator geometry rows,
240 finite-output rows. Trace and Choi conventions inherited unchanged.

Use exact mixture channels and independently exponentiate the real symmetric
64x64 generator PTM by eigendecomposition. Test composition on all64 matrix
units for n,m in[1,2,4] (including sums not in the measurement ladder).
Compare analytic generator and finite retained maps with the cross term C.
For finite geometry use center T_lambda(u)rho and hidden derivative T_lambda(u)h.

All rank thresholds are [1e-9,1e-10,1e-11]. Reference scales for generator
retained/Q/E ranks are the leading singular values of C's corresponding maps
at the same original state. Finite retained/Q/E ranks use b(1,u) times the
leading singular values of C's maps at that finite center. The lambda=0 arm
must never use its own roundoff singular value as a reference. For affected
edge ranks use that edge's positive C-map scale. Source-edge nulls use the
full map scale.

## Validity gates (failure overrides verdicts as INVALID)

- Exact selector; inherited M.domain valid at the12 original references.
- P,Q and a_plus/minus Hermiticity/unitarity, PQ+QP=0, and adjoint-channel
  commutation residuals <=1e-12. Gamma eigenvalues >=-1e-12, trace1 and
  fixed diagonal(.5,.5) within1e-12 for all5 arms.
- Direct generator decomposition into component+cross and a_plus/minus
  dissipators agrees on all64 matrix units within1e-12 max entry error.
  Generator Choi Hermiticity/trace-annihilation <=1e-12. PTM imaginary and
  symmetry residues <=1e-12. Matched conditional-Choi trace equals8 within1e-11.
- Component hidden activity counts exactly18(P),12(Q), active norms2 within
  1e-12, retained leakage of each component <=1e-12. Cross-control retained
  rank12 and Q/E rank6 at all original states, each affected edge rank3,
  source-edge Q/E norm <=1e-12 times full positive-control map norm.
- Every finite mixture weight >=-1e-12 and sum1 within1e-12. Every finite
  Choi min eigenvalue >=-1e-12, Hermiticity/TP error <=1e-12. All exact
  channel/eigendecomposition and composition checks <=1e-12 max entry error.
  Full original input and finite output states rho±eta h, center±eta T(h)
  are positive to -1e-12, normalized and Hermitian within1e-12.
- Analytic retained generator/finite reconstruction errors <=1e-12 maximum
  entry. At every regular evaluated base, Sylvester residual <=1e-10 and
  Q/E from actual outputs agree with geometry from reconstructed retained
  cross outputs <=1e-10 max entry. This is not a finite-difference test.
- Every recorded number finite. Undefined finite geometry is recorded null
  as stipulated below; it does not trigger INVALID. Unexpected programming
  exceptions fail CI and require implementation-only repair.

## Primary generator gate

For all12 states and all5 lambdas: lambda=0 retained/Q/E ranks0 and norms
<=1e-12 times their positive-control norms; every nonzero lambda has retained
rank12 and Q/E rank6 at all thresholds. Full Q/E maps equal lambda times
C's maps within relative error1e-10 using C's Frobenius norm. This isolates
the interference term at a common base with matched diagonal component rates.
YES: MATCHED_COMPONENT_INTERFERENCE_RESPONSE_CONFIRMED.
NO: MATCHED_COMPONENT_INTERFERENCE_RESPONSE_NOT_CONFIRMED.

## Separate finite-window gate, with scientific domain exits preserved

For every one of240 cases, the finite center's three connected matrices must
have proper polar orientation and minimum singular value >=1e-4. Precheck
this explicitly. A violation is a secondary scientific NO, NOT INVALID;
record candidate/lambda/depth, spectra and polar determinants, and null Q/E
fields. Do not call a proper-polar-only helper on a failing center.

At all regular centers, lambda=0 retained/Q/E ranks0 and norms <=1e-12
of the finite positive-control norms; nonzero lambdas have retained rank12
and Q/E rank6, each affected edge rank3 and source-edge norm <=1e-12 of
full positive-control norm. All three rank thresholds must agree.
YES: FINITE_COMPONENT_INTERFERENCE_WINDOW_CONFIRMED.
NO: FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED.
No strength/depth changes after observing any domain exit or rank failure.
A primary YES and secondary NO is a valid scientific outcome.

## Publication

Publish preregistration, derivation, tests and workflow with gate.py absent;
inspect exact expected GitHub RED. Then implement the frozen measurement,
run CI, inspect exact logs and downloaded artifacts, verify hashes and
execution commit, and publish lossless JSON plus results with exact IDs/SHAs.
Tests accept valid scientific NOs. Never equate green CI with a scientific
YES. Historical files remain untouched; no merge to main.
