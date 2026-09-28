# v15.92 preregistration — preparation-span obstruction

Branch research/v15.92-preparation-span-obstruction from exact certified parent eef0d852b2e696675d938244a8ef1ff5d648a24e. Freeze before implementation; no random states, fit, optimizer or finite-difference measurement.

## Inputs

Pin separable-output-rotation/gate.py SHA-256 fb3f26902f624c1a22008c015c4ea8216241eb4c99d89dddbf422f7481afc32d; RESULT.json.gz SHA-256 1e38de1e7e1474e4d14546f722c3ab5013bf347fb02f72ab91bb43115a6da984; decompressed JSON SHA-256 9c848c70134adbb62e70c988dc35001834bccf3c78a0539b294e6ce60167bca9. Require both v15.91 confirmed verdicts and all_valid. Reuse its V81 source and helpers, all 12 states [13,16,22,25,27,29,37,39,46,50,66,77], all 27 hidden directions, lambda=[-1,0,1], u=0.1, eta=1e-4. Preserve all prior scientific NOs, including the v15.81 u=0.8 orientation exit.

Use the four exact channel arms in DERIVATION: isotropic, plane, line, point. Apply the same arm independently to all three sites after the source. There are 144 state/source/arm cases: 36 isotropic controls and 108 potentially singular cases. Python3.11, numpy2.3.5, sympy1.13.3, mpmath1.3.0. Float64 full-complex numerical arithmetic; symbolic exact certificates.

## Forty-five exact checks

For each of four arms: four 2x2 matrix-unit measure-and-prepare versus affine-map identities (16 total); one effect-completeness identity; one grouped prepared trace-one check; one grouped prepared PSD check using exact principal minors/Hermiticity; one prepared Bloch affine-span rank check (3,2,1,0); one maximum squared commutator Frobenius norm check (1/2,1/2,0,0). These five grouped checks per arm add 20. Finally verify all nine entries of the general two-endpoint affine connected-correlation identity in DERIVATION. Total 45 checks. No test may infer separability solely from PPT.

## Independent measurements

Implement the product channel through its full 4x4 affine Pauli transfer matrix R=[[1,0],[t,T]], tensor it three times in the inherited normalized 64-Pauli basis. Independently build its 216/64/8/1 product effects/preparations. Check all 64 global matrix units, every source center and every source-hidden tangent against measure-and-prepare reconstruction. Record probability minima for centers and +/-eta probes, normalization/tangent sums, preparation physicality, full source and 12 composite Choi checks. Record output-center/probe physicality. The preparations and effective probabilities constructively certify separability.

For every edge compare directly extracted C' with T C T^T, including the nonunital point arm. Record the source/output one-body moments and check affine transformation; store C, C', singular values, and ranks at relative thresholds [1e-9,1e-10,1e-11] times the original unprocessed edge's leading singular value. Compute the canonical support partial isometry V using the middle threshold (1e-10); record rank, V, initial/final projectors, their idempotence residuals and the reconstruction error C'-V(V^T C'). These support objects do not define a full orthogonal extension.

Only isotropic rows may call the regular polar/Q/E helper, and only if all edges have rank3 at all thresholds, proper polar determinant, and minimum singular value>=1e-4/9. Compare full Q/E matrices and polar factors to their archived v15.91 a=1/3 row; stored parent C provides the polar-factor comparator. Matching errors are normalized by max(1,parent norm). Record E ranks using the archived reference and thresholds. If an isotropic domain check fails, leave regular fields null and record a scientific NO.

For plane/line/point arms never call the full-polar derivative helper. Record geometry_status=SINGULAR_PREPARATION_SPAN if all edge ranks are respectively <=2,<=1,0 at all thresholds; otherwise SPAN_BOUND_VIOLATION. O,Q,E remain null. The point arm must additionally have all C' norms<=1e-12 despite its nonzero local mean. Do not label these cases as rotational rank zero.

## Validity and verdicts

Validity: pinned inputs/verdicts/indices, all 45 exact checks, finite data; all source and 12 composite channels CPTP; all input/source/output states and preparations physical. Choi/state/preparation/effect minimum eigenvalues and probabilities >=-1e-12; trace/Hermiticity/TP/completeness/probability sums/tangent sums/imaginary probabilities <=1e-12. Matrix-unit, center/tangent reconstruction and affine one-body checks <=1e-12. Connected-correlation identity residual <=1e-12; support projector/reconstruction residual <=1e-10; Sylvester residual <=1e-10. Where isotropic regular fields exist, archived Q/E/polar matching <=1e-9. A failed validity condition gives INVALID, never a rescued scientific pass.

Primary PREPARATION_SPAN_GEOMETRY_OBSTRUCTION_CONFIRMED iff valid and all 108 singular-arm rows obey their rank bounds and null regular-geometry fields, all point correlations meet the zero condition, and all 36 isotropic controls remain regular with E rank6 for lambda=+/-1 and rank0 for lambda=0 at all thresholds. Otherwise PREPARATION_SPAN_GEOMETRY_OBSTRUCTION_NOT_CONFIRMED.

Secondary NONCOMMUTING_PREPARATIONS_INSUFFICIENT_CONFIRMED iff valid, the planar preparations have affine dimension2 and nonzero maximum squared commutator norm >=0.1, and all 36 planar cases have rank<=2 and undefined full O/Q/E. Otherwise NONCOMMUTING_PREPARATIONS_INSUFFICIENT_NOT_CONFIRMED. INVALID overrides both. Valid scientific NOs remain NO and are accepted by tests.

## Execution

Publish preregistration, derivation, tests and workflow with gate.py absent; verify GitHub expected RED and artifact. Implement only this gate, run targeted CI, inspect exact logs/result JSON and downloaded artifact/hash/source bytes. Publish lossless results and exact provenance. Preserve prior verdicts and do not merge to main.
