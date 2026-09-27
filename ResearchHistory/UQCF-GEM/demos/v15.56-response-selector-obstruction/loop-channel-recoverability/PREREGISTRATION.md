# v15.84 preregistration — loop channel and recoverability

Frozen before gate.py exists or new measurement. Parent
782ed08968e19da829e9b041d5af047af94ba588; branch
research/v15.84-loop-channel-recoverability.

## Frozen input and measurement

Use parent support-loop-composition/RESULT.json with SHA-256
bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166.
Require all_valid=true and its crossing CONFIRMED, composition OBSTRUCTED,
core TRIVIAL verdicts. Read L from its full 80-digit strings. Recompute
L^n for n=[1,2,3,4] at 80 digits and verify the stored matrices/spectra.
No new states, source choices, amplitudes, seeds, traversal search or fitting.
This is a diagnostic of candidate46 at the inherited root approximation.

For each power, implement the complex-linear Pauli extension in DERIVATION.md
and build its Choi matrix on all four computational matrix units. Measure
Choi spectrum, output partial trace, input partial trace, Hermiticity,
Bloch-ball contraction, and the rank-two spectral formula. Classify CPTP if
minimum Choi eigenvalue >=-1e-40, NON_CP if <=-1e-8, otherwise UNRESOLVED.
Record the candidate Bell-output minimum eigenvalue separately (J/2).
Do not project negative Choi eigenvalues or rescale the map.

At the frozen fourth power only, if CPTP, construct the singular-axis
measure-and-prepare decomposition, checking every matrix unit. Use weights
s1,s2,1-s1-s2 without adjustment. Then test antipodal states along all three
right singular axes. Measure input/output trace distances, state positivity,
and the optimal binary recovery fidelity (1+D_out)/2. Explicitly implement
the attaining binary measurement and re-preparation to check this value.
The third axis must be treated as the null direction, not an active control.
For the first two axes compute T^+ and its formal unital inverse candidate;
verify exact initial-plane inversion and negative output on the corresponding
pure left-axis state. No claim about an inverse outside that image is assumed.
If power4 is not CPTP, record physical-recovery fields null and a scientific
NO; do not label it an admissible recovery experiment.

## Validity gates (otherwise all scientific verdicts INVALID)

- Parent hash/verdicts exactly match. Recomputed matrices and spectra agree
  with the parent to1e-60 max error. Every power has two singular values
  >=1e-4 and its third <=1e-60. Largest singular value <=1+1e-40.
- Choi Hermiticity, TP/unital partial traces, direct action reconstruction
  from the Choi blocks, and rank-two eigenvalue formula agree to1e-45.
  Complex Pauli-Y and all four matrix units must be preserved.
- Synthetic maps: identity Choi eigenvalues (0,0,0,2), complete
  depolarization (.5,.5,.5,.5), rank-two projection diag(1,1,0)
  (-.5,.5,.5,1.5), and diag(.3,.2,0) (.25,.45,.55,.75), each to1e-45.
  Identity antipodal trace distance1 and depolarized distance0 to1e-45.
- At a CPTP fourth power, measure-and-prepare weights >=-1e-40 and sum1
  to1e-45; construction equals Phi_T on all matrix units within1e-45.
  All input/output/recovered states are Hermitian and trace1 within1e-45,
  minimum eigenvalue >=-1e-40. Formal inverse witness outputs are deliberately
  excluded from the positivity requirement, with their negative spectra
  recorded as evidence. No negative eigenvalue is silently clipped.
- Input trace distances equal1, output distances equal all three singular
  values, and attained recovery fidelities equal (1+D_out)/2 within1e-45.
  Formal initial-plane inversion error <=1e-45.
- All output finite. Unexpected exceptions are implementation failures.

## Scientific gates

Primary predicted pattern: rows n1,n2,n3 NON_CP, row n4 CPTP, and power4
has its valid nonnegative constructive measure-and-prepare decomposition.
YES LATE_CPTP_LOOP_POWER_CONFIRMED;
NO LATE_CPTP_LOOP_POWER_NOT_CONFIRMED.
This is an audit of a prediction from known spectra, not a held-out result.

Recovery: fourth power CPTP with constructive realization; both active
output trace distances in[1e-4,1-1e-4], missing-axis distance<=1e-40, and
both formal-inverse pure-output-axis witnesses have minimum eigenvalue
<=-1e-4. With validity identities, this certifies loss of two-state exact
CPTP recoverability despite algebraic inversion on the active plane.
YES CPTP_LOOP_RECOVERY_OBSTRUCTED;
NO CPTP_LOOP_RECOVERY_OBSTRUCTION_NOT_CONFIRMED.
All valid scientific NOs are accepted by tests. No threshold changes.

## Publication

Publish preregistration, derivation, tests and dedicated workflow with gate.py
absent, verify expected GitHub RED, implement only the frozen diagnostics,
then inspect exact GREEN/failure logs and downloaded artifacts. Verify hashes,
execution SHA and frozen sources; publish full JSON, RESULTS.md and exact
IDs. Preserve old verdicts and source files; no merge to main. Only this
targeted research workflow; final documentation uses [skip ci].
