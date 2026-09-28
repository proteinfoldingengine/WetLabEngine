# v16.00 preregistration — precision readout audit

Parent 64a294845b36877d08c0ef90c87bdec1e1800e58, branch research/v16.00-precision-readout-audit. This separately adjudicates the eight v15.99 rank-covariance failures. Its historical INVALID verdict is immutable. No new source law, fitting, fundamental time, or geometric primitive is introduced.

## Frozen evidence and cases

Pin v15.99 gate.py SHA256 ba44a36fbef8923baf0b2c274fadc1dcc6b65c4f6bff848ff6c8ce0f6d32a56c, gzip84865667bf0a1987d919450eddf41751feb27ace640c99815592ebb65122eac9, raw8107f3f6ac83b08ba9ff9490d56518a10ca823f9bd92a290adf418cc79d9ebbb. Require its all_valid=false and both verdicts INVALID, with scaling_predicate=true and erasure_predicate=true. Pin v15.96 input raw99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e.

Exactly eight response comparisons, all with the planar final preparation and all81 hidden weight-four directions: candidate66, overlap pair, reverse and contrast, each at a=1,1/3,1/6; candidate77, disjoint pair, forward and reverse at a=1/6. The same four quaternion frames, coherent sources, normalization and original absolute rank thresholds [1e-9,1e-10,1e-11] remain fixed. Expected native K/J ranks are1/1 for the six candidate66 comparisons and2/2 for the two candidate77 comparisons.

Python3.11,numpy2.3.5,sympy1.13.3,mpmath1.3.0, single BLAS thread. No random sampling. Precision ladder exactly50 and80 decimal digits.

## Input identity and float64 reproduction

Recompute the declared native/transformed C, source-C and mixed connected derivative dC from the unchanged v15.99 functions, source units, frames, and complex hex density matrices. Do not call the entire192-row gate. Repeat both nested source orders as needed for contrast. Match archived native full K/J and transformed singular spectra within absolute Frobenius1e-9, and require exact archived rank lists at every threshold. This is a validity prerequisite; failure gives INVALID, not a substituted ensemble.

Archive all native/transformed retained input arrays with float.hex, plus their canonical JSON hash. Decode binary float values through integer ratios into mpmath; no decimal-string approximation and no dropped imaginary component. Require exact float roundtrip for state and retained arrays, original density trace/Hermiticity<=1e-12 and eigenvalue>=-1e-12. A synthetic complex converter test must preserve its imaginary entries exactly.

## Two readout arms

FROZEN_INPUT: at each precision independently evaluate native and transformed rounded arrays. No input projection, clipping or alignment. Follow the inherited oriented two-support-vector completion: if C=U S Vt, take V=U[:,:2]Vt[:2,:] and R=V+cof(V). Keep P=sym(R^T C), including a tiny signed third eigenvalue. This is the inherited numerical extension for nominally rank-two inputs, not an assertion that rounded C has exact rank2.

Solve the skew Sylvester equation by an independent3x3 linear solve in the fixed axial skew basis, rather than the inherited eigendecomposition algorithm. Compute both loop derivatives, left-trivialized K6x81 and invariant J3x81 independently. Use high-precision SVD to report singular values and apply the original three thresholds. No rank truncation of K/J.

EXACT_FRAME_CONTROL: take the same native binary-decoded C, source-C and dC, transport each edge with the exact rational SO(3) matrices prescribed by the four frozen quaternions, and independently evaluate the readout. This control tests the readout under exact prescribed tensor transport. It is not a fresh global quantum/source recomputation, not an externally fitted alignment, and cannot certify the entire v15.99 gate.

## Validity and controls

Require input pinning/counts/reproduction above. For every input edge, retain the original planar numerical domain: second singular value exceeds1e-9 times the leading source-C singular value and third singular value is at most1e-11 times that reference. Record all domain spectra. A domain failure is INVALID for this numerical adjudication.

At both precisions require proper-R orthogonality/determinant, reconstruction R P=C, P symmetry, skewness, Sylvester identities and loop derivative skewness residuals<=1e-35. Archive the third C singular value, discarded-support norm and signed minimum P eigenvalue separately as input-rounding diagnostics; do not impose1e-35 PSD or exact-rank-two conditions on rounded inputs.

Require all three skew positive controls C=diag(2,1,0), dC=B_i C to return W=B_i within1e-35, with rotational response rank3 at all original thresholds. Symmetric dC controls must return zero W within1e-35. Rank-one C=diag(1,0,0) must be rejected. These controls prevent a solver that forces the null result by suppressing valid skew directions.

EXACT_FRAME_CONTROL must agree with blockdiag(G0,G0)K_native and J_native within absolute Frobenius1e-35; rank lists must equal the expected native lists. At50 and80 digits, all FROZEN_INPUT and EXACT_FRAME_CONTROL K/J matrices must agree across precision within absolute Frobenius1e-30, with identical rank lists. All data finite. Violations of any validity prerequisite give INVALID.

## Frozen verdicts

READOUT_ARITHMETIC_NOISE_CONFIRMED iff valid and every FROZEN_INPUT native/transformed rank list at both precisions equals its expected archived native list, and their covariance residuals<=1e-9. This means the eight threshold crossings depend on readout evaluation; it does not isolate a particular NumPy operation or eliminate all upstream input rounding.

FROZEN_INPUT_RANK_RESIDUAL_PERSISTS iff valid and that recovery predicate fails. Report exactly which cases, spectra and thresholds persist, without treating this as a physical source-law obstruction. INVALID overrides both outcomes when prerequisites fail. Tests accept either valid scientific verdict and enforce INVALID precedence. Do not relax thresholds after measurement.

## Execution and boundary

Publish this document, derivation and tests before scientific implementation; inspect expected absent-implementation RED and downloaded artifact. Implement only this audit, inspect exact job logs and full artifact even after failure, publish results with hashes/IDs. No main merge. No blanket reclassification of v15.99, no new144-row certification, no physical-law selection or gravity claim. Genesis Pin and ordered recoverability framing remain unchanged.
