# v15.82 preregistration — polar boundary obstruction

Frozen before gate.py exists or any new measurement. Parent
8ef3c4388dffcd0b799578600246808e5aa14c2e; branch
research/v15.82-polar-boundary-obstruction.

## Frozen inputs and scope

Diagnostic witness: inherited selector candidate 46 out of the unchanged
12 indices [13,16,22,25,27,29,37,39,46,50,66,77]. Source lambda=-1,
P=ZII,Q=XXI, edge(0,1). No random seed or new ensemble selection.
Use the exact rational complex binary64 input and channel in DERIVATION.md.
Record all real/imaginary input entries as float.hex strings. No rounding,
normalization, symmetrization or dropping imaginary entries.

Form all nine exact C(q) polynomials and exact determinant. Isolate roots
in q in [1/5,9/20], including multiplicities, to rational interval width
<=1e-60. This fixed interval contains the earlier u=.4 to .8 sign change.
If exactly one simple root is found, use the midpoint of its isolating
interval and u*=-log(q*)/2. Evaluate at 80 decimal digits. Record any other
root count as a scientific NO without selecting a preferred root.

Evaluate the root and sides u* +/- delta for delta=[1e-3,1e-5,1e-7].
These are diagnostics around an isolated zero, not new permitted depths
for v15.81. No threshold tuning, fitting or extrapolation. Original
identity/control strengths are u=[0,.1,.2,.4,.8].

## Validity (otherwise INVALID)

- Inherited selector exactly matches all 12 indices, and original domain
  remains valid. Complex rational input roundtrip error <=1e-16.
- Exact A^2=I; channel is the explicit convex mixture on the full interval.
  Input/output Hermiticity and trace errors <=1e-12; eigenvalues >=-1e-12.
- Exact C(q) and independent original v15.81 channel/correlation extraction
  agree to <=1e-12 max entry at all five control strengths. Complex matrix
  channel transport also agrees to <=1e-12. Exact polynomial degree <=6.
- Positive synthetic control diag(1/5,1/10,q-1/3) has exactly one simple
  isolated root at 1/3; one-sided canonical polar difference has singular
  values (2,0,0) to 1e-40. Negative control
  diag(1/5,1/10,1/20+q) has no root in [1/5,9/20].
- For every nonsingular high-precision polar evaluation, orthogonality and
  reconstruction residuals <=1e-50. At the root, reconstruct C from its two
  retained singular terms with error <=1e-45 if a rank-two test is asserted.
- All numeric output finite; exact rationals and high-precision values
  serialized as strings. Geometry at the root is partial-isometry data,
  never a Q/E measurement. Unexpected code exceptions are CI defects.

## Scientific gate

All of the following are required for POLAR_CONTINUATION_OBSTRUCTION_CONFIRMED:
1. Exactly one simple determinant root in the fixed q interval; u* in
   (.4,.8). |d det C / dq| >=1e-8 at the root, minimum singular value
   <=1e-45, next singular value >=1e-4 (rank exactly two at this precision).
2. At every paired delta the before factor has determinant +1 and the
   after factor -1 within 1e-40. At delta=1e-7, singular values of their
   difference are within 1e-4 of (2,0,0); Frobenius distances from each
   factor to the root partial isometry are within 1e-4 of 1.
3. The original minimum density eigenvalue is >=.01, as are the root and
   all six side states. The mixture proof supplies the full-interval
   lower bound; sampled checks independently guard implementation.
4. All 27 raw hidden Paulis have identically zero restriction under this
   channel to the 15 source-edge nonidentity observables, coefficient by
   coefficient in q. Normalizing them cannot change these exact zeros.

Otherwise, for valid execution: POLAR_CONTINUATION_OBSTRUCTION_NOT_CONFIRMED.
Tests must allow a scientifically valid NO. Neither outcome revises v15.81
FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED.

## Publication and verification

Publish derivation, this preregistration, tests and workflow with gate.py
absent. Verify expected RED in GitHub Actions, then implement the frozen
measurement. Inspect GREEN or failure logs and downloaded result artifact,
verify execution SHA and hashes, and publish RESULTS.md plus lossless JSON.
Only the targeted research workflow is authorized; no protein/wet-lab
suite and no merge to main. Final documentation commits use [skip ci].
