# v15.93 preregistration — oriented rank-two response

Exact certified parent: 59b40b60802b70b9cc57c3091e3d6deb9dc04cfb. Additive branch research/v15.93-oriented-rank-two-response. No measurement before expected RED; no random search, fitting or threshold revision.

## Frozen inputs and scope

Pin preparation-span-obstruction/gate.py SHA-256 7d65d2525353ec83426694e5375881740031c33d2bb02ea38aec4737ac052ec9; RESULT.json.gz ea33a8cd3dbbea12bffd13e5af1a5eecd61e235ee7617d056058b95cf4f72a7f; decompressed result bd2749b7f7b1afd836074890bf66f49ba96faa20353615b741fb2bd6cac1b30a. Require both v15.92 confirmed verdicts and all_valid. Reuse its 12 states [13,16,22,25,27,29,37,39,46,50,66,77], all 27 hidden directions, source lambda=[-1,0,1], u=0.1, state probe eta=1e-4 and planar local channel T=diag(1/2,1/2,0), t=0. There are 36 state/source cases, 108 edges, 2916 edge/direction derivatives. No source update composition claim.

Python3.11, numpy2.3.5, sympy1.13.3, mpmath1.3.0. Full-complex float64 state transport; exact symbolic controls. Use the same frozen covariance frames at all states: quaternions (w,x,y,z)=(1,2,3,4),(2,-1,3,1),(3,2,-1,2), normalized analytically by their squared norms in the rotation formula. These are endpoint coordinate checks, not new random states or physical sources.

## Fourteen exact checks

1 rank-two diagonal support completion; 1 symbolic skew Sylvester identity; 1 determinant p1*p2*(p1+p2) of the skew operator; 2 distinct rank-one proper completions; 1 rank-one nonzero skew kernel; 3 rational frame orthogonality/determinant checks; 3 cofactor covariance checks on the rank-two diagonal support (one per edge); 2 symbolic planar angle-derivative identities, one for each determinant sign. Total 14. Positive p1,p2 symbolic assumptions are fixed. Rank-one ambiguity is a positive control for the limitation, not an INVALID outcome.

## Measurement

Recompute the frozen planar output states and all hidden tangents through v15.92's Pauli-transfer implementation. Independently extract connected dC from pair moments minus both one-body derivative terms. Compare centers against the archived v15.92 plane C and independently compare dC against T*dC_source*T^T. Check xy support. Recompute source/composite Choi CP/TP and input/output center and +/-eta probe physicality using inherited diagnostics.

At all thresholds [1e-9,1e-10,1e-11] times each archived unprocessed edge leading singular value, record rank. Rank two at every threshold is the oriented domain. A domain exit is a scientific NOT_CONFIRMED, not a rescued or automatically INVALID result. Only inside that domain calculate support V (middle threshold), R=V+cof(V), P, Q, W, and dR=RW using off-diagonal Sylvester solve. Record all full Q/E maps (9x27), edge and total ranks and norms. Coordinates are (W21,W02,W10), similarly Q. Rank reference for both Q and E is max(1, the corresponding archived v15.92 isotropic map reference); this fixed absolute floor prevents self-normalized noise from appearing active. Record rank agreement Q/E; do not assume agreement solely from the theorem because numerical thresholding has finite resolution.

Check R^TR=I, detR=1, RP=C, P symmetric PSD, support matching R*V^TV=V; independent 2x2 signed planar completion and derivative; Q=PW+WP; skew W; inactive xy-complement and first edge response. Covariance: independently recompute support completion and Sylvester tangent from transformed C'=A_i C A_j^T and dC'=A_i dC A_j^T. Compare R'=A_i R A_j^T, W'=A_j W A_j^T and dR'=A_i dR A_j^T. No extra source transformation is inferred: these are coordinate transformations of the full retained data.

For every edge/direction inside the domain, central-difference R(C+epsilon*dC) with epsilon=b*s2/max(1,norm(dC)), b=[1e-3,1e-4,1e-5], s2 the second singular value of the center. Use the top two singular directions for the support partial isometry of these exactly planar matrix probes. Record every error normalized by max(1,norm(RW)); require the final rung error<=1e-6. Do not require monotone decrease at roundoff. These are matrix-space differentiation probes, not density operators.

## Validity and verdicts

Require pinned parents/indices, finite data, all 14 exact checks, 36 cases, source and composite CP/TP and input/output physicality at inherited eigenvalue tolerance -1e-12 and trace/Hermiticity/TP 1e-12. Center archive, connected-derivative identity and xy support errors <=1e-12. Completion/PSD/support, Sylvester/skew, planar comparison, covariance and inactive-response residuals <=1e-9. Matrix errors use Frobenius norm, relative errors divide by max(1,reference norm); center/derivative support checks may use maximum entry. Final finite-difference relative error <=1e-6. Missing domain rows skip derivative controls and force scientific NO; nonfinite data or failed identity/physicality gives INVALID.

Primary ORIENTED_RANK_TWO_READOUT_CONFIRMED iff valid and every edge lies in the rank-two domain; otherwise ORIENTED_RANK_TWO_READOUT_NOT_CONFIRMED. Secondary PLANAR_ORIENTED_RESPONSE_CONFIRMED iff valid, primary domain passes, all 24 coherent cases have E and Q rank2 at every threshold, and all 12 lambda=0 cases have rank0 for both with norms<=1e-12. Otherwise PLANAR_ORIENTED_RESPONSE_NOT_CONFIRMED. INVALID overrides both. Tests accept valid scientific NOs and test that adjudication cannot convert a negative predicate into a pass.

## Execution

Publish derivation, preregistration, tests and workflow with gate.py absent. Inspect GitHub expected RED logs/artifact. Implement only the frozen measurement, run CI, inspect exact logs and result JSON, download and verify artifact bytes/source/head/checksums, then publish lossless data and exact provenance. No merge to main; no changes to prior gates or verdicts. This establishes a conditional readout, not a source-law selection, a new geometry primitive, or gravity.
