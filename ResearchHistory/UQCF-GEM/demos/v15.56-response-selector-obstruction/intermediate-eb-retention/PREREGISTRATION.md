# v15.99 preregistration — intermediate EB retention

Parent3a3655a5c5bd263b8986a651b9c9ef23bda0c306; branch research/v15.99-intermediate-eb-retention. Freeze before implementation/RED. No new sampling, fit, threshold tuning or historical verdict change.

## Frozen data and protocols

Pin composed-four-body-response/gate.py SHA256 ddc0e59aee1db514e77728dd7788d43545f03cde40cb7a19b221e2e8b1733239, RESULT.json.gz20a117760c6f5a9ecac86e45c871411ab3ed64c59f48c42d79641202b6656c6d, raw044fa85ad44c2edf5e1d8e0fa4c2410f44498d5edc2456c99633706b4c251b0e. Require all_valid and both v15.98 confirmed verdicts. Read exact input hex from v15.96 rawJSON99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e, with code56feb3fb08c135f060895160aa7fb9955f2c887da5469694c61523aa562a0f52. Same12 indices[13,16,22,25,27,29,37,39,46,50,66,77], all81 Pauli weight-four probes normalized /4.

Use unchanged coherent lambda=+1 sources A01,B12,D23, both orders for source pairs overlap(A,B) and disjoint(A,D), followed by unchanged planar/isotropic preparation. Insert M_a=D_a tensor4 BETWEEN the sources, a in[1,1/3,1/6,0]. a=1 is the exact parent reproduction; a=1/3 and1/6 are EB cuts; a=0 is complete erasure. Total192 rows:144 positive-a rows and48 erasure controls. Python3.11,numpy2.3.5,sympy1.13.3,mpmath1.3.0, one BLAS thread.

## Exact and channel certificates

Eight new grouped exact checks: (1) six-outcome local measure-and-prepare equals D_a on all four computational matrix units symbolically in a; (2) complete positive effects and positive normalized prepared states at a=1/3,1/6,0; (3) connected-correlation baseline scaling a²; (4) only intermediate Pauli weight3 contributes to the final pair restriction, all other weights contribute zero for all81 probes/pairs/orders; (5) retained mixed derivative scales a³ symbolically; (6) all lower hidden pair and one-body restrictions vanish through the mixed order; (7) a=0 maps every traceless Pauli word to zero and the identity to itself; (8) disjoint retained mixed order contrast vanishes symbolically. Reuse all74 v15.98 and inherited exact checks unchanged, without treating old uninvolved-spectator or full-source-commutation statements as properties of the new inserted protocols.

Implement M_a independently by four-qubit normalized Pauli weights a^weight. For each EB a, compare with explicit tensor-product1296-outcome POVM/preparation action on all256 matrix units, tolerance1e-12. Require effect completeness/Hermiticity, PSD, prepared-state trace/Hermiticity/PSD with1e-12 tolerance. For each unique(state,a,first source) with a=1/3,1/6,0, independently reconstruct the finite intermediate center after source strength0.1 from these outcomes; store all1296 probabilities, require real/nonnegative within1e-12, sum1 within1e-12, reconstruction<=1e-12. There are108 such center records. Exact positivity of the prepared states plus this linear map certificate proves full separability of the intermediate states for any input, not just those centers.

Check normalized hidden basis, individual retained nulls, mixed one-body nulls and source unitarity/weight normalization at1e-12. Compare numeric pair derivatives to the symbolic a³ law at1e-12 maximum entry; audit intermediate weight3 contribution and store its norms. Record full global ordered tangent/contrast norms separately. Record all six pair-leakage ranks/norms, labeling23 outside the geometry atlas.

## Response gate

Recompute every positive-a baseline and mixed derivative from global matrices. The baseline before final preparation is M_a(rho); the derivative is L_second M_a L_first h. Use the frozen polar/Sylvester/loop extraction for K6x81 and J3x81. No reuse of parent response as the measured response. Parent matrices provide independently certified predicted values aK98,aJ98.

Absolute rank thresholds[1e-9,1e-10,1e-11], reference1. Baseline and affine-check domain: planar five edges rank2; isotropic five edges rank3 with proper full polar determinant. Edge reference is the leading unprocessed M_a(rho) correlation singular value. Never flip a full-rank determinant or complete another rank. For positive-a domain exits, null affected response fields and give a scientific NO if other checks pass.

For each positive-a row and both orders/contrast, require rank lists equal the matching v15.98 parent and normalized matrix residuals norm(K-aK98)/max(1,norm(aK98)) and similarly J <=1e-9 for the primary scientific YES. A mismatch here is a scientific NO, not numerical INVALID by itself. Store actual native K,J, singular values and ranks; transformed ranks and covariance residuals; scaling residuals; baseline loops.

Validity controls: proper polar identities, derivative Sylvester/skew identities, baseline polar/loop invariance, linear contrast identity, overlap first-loop null and disjoint retained order-contrast null <=1e-9. Require the disjoint contrast ranks0. Do not require full global disjoint contrast zero after insertion.

Covariance: same four quaternion frames as v15.98; transform states, h, source unitaries and the final preparation channel correctly. M_a commutes with independent local unitary frame changes. Independently recompute both ordered responses and contrast; K transforms by blockdiag(G0,G0), J invariant, absolute residual<=1e-9, rank lists match.

## Finite and physical checks

For every row/order use hidden states rho±epsilon h, epsilon=1e-4, finite strengths u=v=0.1, with the middle channel inserted. Compare the final connected correlation difference divided by 2epsilon s(0.1)^2 to the analytic mixed derivative. Relative Frobenius error with denominator max(1,norm analytic array)<=1e-7. This checks finite retained action, not finite-strength polar ranks.

For a>0 independently check the loop derivative on global affine states M_a(rho)±eta Y_a, eta=1e-6, followed by final preparation. Central differences of loop matrices and invariant scalars must match native K,J within1e-5 normalized Frobenius error. Affine domain exits are scientific NOs, skipping undefined comparisons. The affine probes are derivative diagnostics, not new source laws.

Check density positivity>=-1e-12, trace/Hermiticity<=1e-12 for hidden inputs, each finite stage (after first source, middle, second source, final preparation) and affine input/output states. All data finite. a=0: require baseline M_0(rho)=I16/16, all final centers and source-stencil outputs equal I16/16 within1e-12, all pair correlations and mixed tangents <=1e-12, correlation rank0, and null/undefined polar response fields. Do not manufacture rank-zero K/J at erasure.

## Frozen verdicts

Validity includes pinned parent/counts, exact/quantum/algebra/null/frame/finite agreement checks within stated limits. INVALID overrides both verdicts if validity fails. Primary INTERMEDIATE_EB_RESPONSE_SCALING_CONFIRMED iff valid and all144 positive-a rows have all applicable domains, unchanged response rank lists and all K,J scaling residuals<=1e-9 for both orders/contrast. Otherwise INTERMEDIATE_EB_RESPONSE_SCALING_NOT_CONFIRMED.

Secondary COMPLETE_INTERMEDIATE_ERASURE_POLAR_UNDEFINED_CONFIRMED iff valid and all48 zero-a rows satisfy the erasure criteria with undefined response fields. Otherwise COMPLETE_INTERMEDIATE_ERASURE_NOT_CONFIRMED. Expected erasure-domain loss does not count as a positive-a scientific failure. Tests accept valid scientific NOs. No post-measurement tuning.

## Execution

Publish preregistration/derivation/tests/workflow without implementation; inspect expected RED log and downloaded archive. Implement frozen measurement, run targeted CI, inspect actual verdicts in a compact job-log summary and complete artifact JSON, verify manifest hashes against logs and downloaded files. Publish results with exact provenance. No main merge. No claim of intermediate reference entanglement, fully classical sources, finite-strength rotational ranks, unique physical law, continuous holonomy or gravity.
