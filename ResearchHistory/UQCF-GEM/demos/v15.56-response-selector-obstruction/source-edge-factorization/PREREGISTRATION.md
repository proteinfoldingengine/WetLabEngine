# Source-to-edge factorization gate

Date: 2026-09-26. Parent: ec33024e0343193f6a5d0c7ed62d8512701dd541.

## Approved scope

Execute the next bounded task in ../origin-rank-adjudication-36268823853/README.md. Preserve the original experiment and artifact. Retain its exact 11 fixture parameter triples, 27 weight-three Pauli hidden directions, nine one-body Pauli source directions, and normalized exponential tilt. No fitting, new source law, geometry input, or result-based state selection. The 243 columns are a tensorized bilinear map, not 243 independently physical states.

An additive gate is used rather than overwriting historical code or results. The branch research/v15.56-source-edge-factorization starts at the exact parent above and avoids triggering the two historical all-push workflows on the parent branch. No merge to main is authorized or performed here.

## Outputs and identities

For every fixture save raw NPZ arrays: base state, edge rotations O, mixed edge responses M, hidden first derivatives O_eta, source first derivatives O_s, the 9 x 243 edge-coordinate map E, 3 x 9 loop map L, independently assembled 9 x 243 full loop response K, visible and invisible edge maps, and deterministic finite-difference probe outputs. Use Hilbert-Schmidt orthonormal skew generators (01),(02),(12), with upper entry +1/sqrt(2) and lower entry -1/sqrt(2). Edge coordinates are those of skew(M_e O_e^T). Edge order is (0,1),(1,2),(2,0); columns are hidden-major/source-minor in the unchanged response_quotient_rank bases.

Verify K via the unmodified R.K_for independently of E and L (shared analytic ingredients, not an independent derivation). Also compare three predetermined dense hidden/source combinations against direct four-corner differences of G.geom(G.tilt(r+eta*h,s,p)). Probe coefficients use seed 20260927; normalize h and p separately by operator norm. Steps are 2e-4 and 1e-4, with Richardson value (4 K_small-K_large)/3. These are perturbation parameters, not time.

Save all singular spectra, matrix norms, state eigenvalues, edge singular values and determinants, polar Sylvester conditioning, non-skew parent-relative norms, hidden first-derivative norms, factorization residuals, and basis-spectrum residuals. Decompose E with Pi=L.T L/3 and I-Pi. Save fractions of squared Frobenius norm in the two pieces; these are coordinate-norm diagnostics, not physical probabilities.

## Frozen numerical policy

Algebra/reconstruction relative error limit: 1e-10, with denominator max(parent Frobenius norm,1e-15). Orthogonal basis-spectrum limit: 1e-8. Base fixtures must satisfy the historical E.base_ok criteria and positive-determinant regular polar branch. State/edge thresholds are unchanged (.03 and .02); comparisons to already-frozen boundary values may allow 1e-14 absolute roundoff, recorded explicitly. Orthogonality and Gram/projector identities: 1e-10 absolute Frobenius error. Hidden first derivatives and identity-source response: 1e-10 absolute Frobenius limit. Independent finite-difference probes: error <=1e-5*max(1,||K_analytic||_F); record both steps and their change, without selecting the better one.

Effective rank uses tau=max(1e-10,100*eps*max(A.shape))*s_parent, where s_parent is the largest singular value of the parent matrix. For an ordinary map its own largest singular value is the parent scale; for non-skew residuals the unprojected edge map supplies the scale. Also report ranks at relative cuts 1e-9 and 1e-11, retaining the same floating-point floor. These are numerical resolution criteria, not a rigorous bound on all analytic-evaluation error. Do not alter them after seeing this run. Nonfinite entries, wrong dimensions, incomplete or duplicate fixtures/columns, provenance mismatch, failed conditioning or algebra/control checks, and artifact corruption invalidate the gate. A rank outcome different from 9->3 is a valid scientific alternative when controls pass, not a reason to change thresholds. Threshold-sensitive rank is reported as unresolved, not rounded toward the expected answer.

## Fail-closed execution and tests

First publish and run RED tests before adding implementation. Tests must cover: roundoff-only residual classified relative to its parent; a genuinely nonzero residual retained; nonfinite input; wrong column count; false controls; missing/duplicate fixture; corrupted NPZ; complete export and reread; invalid CLI including python -O; pipeline failure propagation. Use explicit errors/return codes rather than assertions for production validation. JSON must reject nonfinite values. Artifact file names and expected array shapes are fixed. The verifier recomputes diagnostics from NPZ, checks byte digests, and does not trust only a cached controls_pass flag.

After GREEN, run the existing demo directory's complete unittest discovery separately from the new gate tests. Preserve tests, logs, source snapshot, raw matrices, JSON report, environment/source hashes, and actual head SHA as Actions artifacts. Use explicit bash with pipefail; missing artifact output is an error. No invalid record may produce a successful CLI exit.

## Completion boundary

Completion means implementation, RED/GREEN evidence, full 11 x 243 measurement, artifact verification, documented outcome and limitations. The loop rank-three cap is already explained; this task measures E and its split, not gravity, universality, source uniqueness, or a universal rank-nine theorem. Alternative source-law and non-axial fixture controls remain a later task. Self-review is required; a separate independent reviewer is not available in this session.

## Numerical references

NumPy rank documentation: https://numpy.org/doc/2.3/reference/generated/numpy.linalg.matrix_rank.html (SVD error versus error already present in a matrix).
GitHub shell behavior: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsshell (explicit bash and pipefail).
