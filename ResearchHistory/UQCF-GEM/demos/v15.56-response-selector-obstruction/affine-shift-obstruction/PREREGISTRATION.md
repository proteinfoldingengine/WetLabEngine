# v15.85 preregistration — affine-shift obstruction

Frozen before gate.py exists or new measurement. Parent
b35525fd01bea949cacd6b2f65939c57a2911682; branch
research/v15.85-affine-shift-obstruction.

## Frozen inputs and diagnostics

Pin loop-channel-recoverability/RESULT.json SHA-256
2b51d58a3d5b93c494904a179942feb3e574b8bcec53dbe80c6a6cf5b5ced9f4
and support-loop-composition/RESULT.json SHA-256
bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166.
Require both all_valid and their published verdicts. Use the stored loop L,
recompute powers n=[1,2,3,4] at 80 digits, and retain their full complex
qubit extension. No new state, source, seed, amplitude fitting or depth search.
This is a diagnostic of the inherited candidate46/root approximation.

Implement DERIVATION.md. Verify the spin-flip Choi identity exactly using
symbolic Pauli matrices on all13 affine coefficient matrices (one constant,
nine T components, three shift components). For actual loop powers verify
unital Choi identities, spectra and the three shift derivatives independently
by constructing the affine map on all four complex matrix units. Recover
minimum-eigenvalue rank-one Choi witnesses for n1,n2,n3; record their two
marginals, negative expectation and three shift coefficients.

At n4 take the null left singular vector u3 and freeze
 tau=[-1,-.5,0,.5,1], t=tau*u3.
Record the full Choi spectra, exact line-bound formula, positivity
classification, and spin-flip/averaging checks. Classification: CPTP if
minimum eigenvalue>=-1e-40, NON_CP if<=-1e-8, otherwise UNRESOLVED.
No full-region feasibility claim from this line sampling.

For CPTP rows tau=-.5,0,.5, test the same three antipodal right-singular-axis
pairs as v15.84. Record input/output trace distances and the mean pure-target
overlap attained by the corresponding binary measurement-and-preparation
recovery. If a stipulated row is not CPTP, record recovery null and a valid
scientific NO, not physical recovery evidence.

## Validity (otherwise verdicts INVALID)

- Pinned hashes and inherited verdicts match. Recomputed loop powers agree
  with stored matrices and v15.84 Choi spectra within1e-60 max error.
- All13 symbolic coefficient identities hold exactly, S^dagger S=I exactly.
  Real source-state geometry is unchanged; complex Pauli-Y is preserved.
- Actual unital spin-flip invariance, affine shift derivative identity,
  Choi Hermiticity/TP, and opposite-shift averaging residuals <=1e-45.
  Include both output unitality offset and nonunital action on I.
- Negative-witness normalization, eigenvector reconstruction and both
  marginal-I/2 residuals <=1e-45. Witness imaginary expectation residuals
  <=1e-45. Scientific negativity and shift-coefficient tests are below.
- n4 rank-two guard: s2>=1e-4, s3<=1e-60. Its null-axis shift Choi spectra
  match the analytic formula within1e-45. Record raw tau-bound radicand;
  it must be nonnegative to1e-45. Clipping is allowed only within that
  roundoff tolerance for its square root, never to repair a Choi spectrum.
- Positive nonunital synthetic control: amplitude damping gamma=1/2 with
  T=diag(1/sqrt2,1/sqrt2,1/2), t=(0,0,1/2). Affine and Kraus Choi matrices
  agree within1e-45; eigenvalues (0,0,.5,1.5) within1e-45, and its opposite
  shift is CPTP too. For T=0, t=(0,.5,0), spectrum(.25,.25,.75,.75);
  for t=(0,1.5,0), spectrum(-.25,-.25,1.25,1.25), within1e-45.
  The latter is a deliberate NON_CP control, not INVALID.
- For admissible recovery rows, all input/output/recovered states are
  normalized/Hermitian within1e-45, minimum eigenvalue>=-1e-40. Input trace
  distances equal1, output distances equal corresponding singular values,
  and attained mean overlap equals (1+D_out)/2 within1e-45.
- Every output finite. Unexpected programming exceptions are CI defects.

## Scientific gates

Universal obstruction: every n1,n2,n3 witness expectation<=-1e-8, each
shift coefficient has absolute value<=1e-45, and the exact coefficient
identity holds. YES AFFINE_SHIFT_RESCUE_OBSTRUCTED;
NO AFFINE_SHIFT_RESCUE_OBSTRUCTION_NOT_CONFIRMED.
Universality follows from the exact theorem, not approximate zero coefficients
multiplied by arbitrarily large shifts.

Nonunital recovery extension: n4 controls tau=-.5,0,.5 all CPTP, tau=-1,+1
NON_CP; recovery data valid on the three admissible rows. Both active output
trace distances in[1e-4,1-1e-4], kernel distance<=1e-40. With exact shift
cancellation, YES NONUNITAL_RECOVERY_OBSTRUCTION_CONFIRMED;
otherwise NO NONUNITAL_RECOVERY_OBSTRUCTION_NOT_CONFIRMED.
All valid scientific NOs are accepted by tests. Thresholds and shifts are
immutable after measurement. No change to historical verdicts.

## Workflow

Publish preregistration, derivation, tests and targeted workflow with gate.py
absent; inspect expected GitHub RED. Implement only the frozen diagnostics,
run CI, inspect exact logs and downloaded artifacts, verify hashes and
execution SHA, review interpretation and publish lossless JSON and RESULTS.md.
Only this research workflow; no merge to main. Documentation uses [skip ci].
