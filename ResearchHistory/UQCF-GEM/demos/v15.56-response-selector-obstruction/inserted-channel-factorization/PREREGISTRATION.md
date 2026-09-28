# v16.04 factorization audit — frozen protocol

Parent publication: a451398b307f89a380736186f387cf61f80718c1. Parent scientific head: 850dc3538f04ce9efcb3e974fa04992bcb1cb150. Analytic head: 49004539e99983d75fe748b18f4d1c968c6a85e8. User approved execution on 2026-09-28. No new state, source, preparation, alignment, threshold or fit is introduced.

## Ensemble and construction

All 12 candidates: 13,16,22,25,27,29,37,39,46,50,66,77. All 81 weight-four hidden probes. Disjoint A,D sources only; both plane/isotropic arms; archived binary a=1,1/3,1/6; native and transformed frames; 50 and 80 decimal digits. There are 72 state/attenuation/preparation configurations per precision, each evaluated in both frames. No finite-lambda sweep or overlapping-source rerun is needed for this coefficient audit.

Lift each frozen two-site generator into the global Pauli basis by explicit index replacement, independently of the parent grouped application routine. For every nonzero transfer entry (output i,input j), form [X,M] by multiplying by a^weight(j)-a^weight(i). Never truncate small coefficients. Record each weight-block operator Frobenius norm and its state-action norm. Weight-preserving blocks must vanish.

Compute k_D and k_A on each state from these blocks and compare them with direct X(M rho)-M(X rho). Prepare Q k_X. Independently form the connected differential, retaining both one-body-product terms, and compare it with the parent retained-differential routine. Compute T_D and T_A with the frozen analytic polar Hessian; T=T_D-T_A. Compare T against the archived parent cubic matrix in the same frame and precision, and against a fresh direct-protocol center-direction Hessian contraction. The Hessian evaluator is intentionally inherited: independence is in the global commutator and connected-direction construction, not a second polar solver.

Reconstruct both forward and reverse hidden tangents and verify their pair equality, complete one-body null and inherited lower-pair null. Use a fixed affine tangent readout DF(C0) on each independently reconstructed hidden tangent; their response difference must vanish. Zero is not inserted as a control output. At a=1 both source commutators and the summed cubic response must vanish.

## Controls, norms, and decisions

Use absolute Frobenius norms throughout. Within-precision residuals <=1e-35: lifted versus direct source application; block versus direct commutator; connected differential; native/transformed global stages and invariant responses; hidden-tangent equality/nulls; affine contrast; polar/Sylvester arithmetic identities; parent cubic comparison; direct-protocol cubic comparison; source contribution sum. Cross-precision matrix discrepancies <=1e-30. No normalization or tolerance tuning after results.

Keep rank thresholds 1e-9,1e-10,1e-11 and every inherited relative spectral-domain check. Check ranks and classifications of T_D,T_A,T in both frames and precisions. Null or unresolved individual contributions are valid outcomes, not failures. Domain errors, mismatches, nonfinite values, corrupted parent provenance, or failed identity controls produce INVALID; a domain error is not a numerical zero. a=0 is excluded because its polar geometry is undefined.

Parent compressed raw files and inherited source files are SHA256-pinned in SOURCE_MANIFEST.json. Require parent version 16.03, all_valid true, exact execution head, candidate identity and complete unique 24-row structure (all pair/arm/a/precision combinations). Do not infer validity from CI green alone.

On valid input, FACTORIZATION_CONFIRMED requires every parent/direct coefficient comparison to pass. FACTORIZATION_NOT_CONFIRMED is representable but any failed identity/validity control overrides to INVALID. The audit does not label a mismatch new physics.

Archive T_D,T_A,T matrices, ranks/spectra/classifications, global and retained direction norms, block norms, edge domain diagnostics, residual maxima, hashes, execution head and logs. Cancellation ratio is ||T_D-T_A||/(||T_D||+||T_A||), descriptive only and null when the denominator is zero.

## Execution

Commit this protocol, manifest, workflow and regression tests before implementation. Observe absent-implementation RED and skipped measurement, then implement and run GREEN controls followed by the full 12-job matrix. The controls also execute the nine parent tests. Inspect exact logs and artifacts. Publish the complete report and raw results on the research branch. No merge to main or unrelated wet-lab execution.

Time remains pruning / ordered recoverability update. The experiment audits a specified mechanism; it does not derive gravity or select a universal source law.
