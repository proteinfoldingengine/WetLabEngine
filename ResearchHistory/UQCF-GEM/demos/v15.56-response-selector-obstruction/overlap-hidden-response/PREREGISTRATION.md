# v15.97 preregistration — overlap hidden response

Parent c61de02241acac20c02b50a76469ba63224a7b3e; additive branch research/v15.97-overlap-hidden-response. Freeze before implementation and expected RED. No new random seed, state selection, fit, source tuning or historical verdict change.

## Inputs

Pin v15.96 overlap-holonomy-common-line/gate.py SHA256 56feb3fb08c135f060895160aa7fb9955f2c887da5469694c61523aa562a0f52, RESULT.json.gz 1102dd9da14f82cc44d958de15effe9b0553e3b6cf396deb1791f98a88527550 and decompressed result 99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e. Require all_valid and both confirmed verdicts. Read the exact hexadecimal complex input matrices from that result; independently reconstruct all twelve mixtures and require agreement <=1e-15. Candidate order [13,16,22,25,27,29,37,39,46,50,66,77]. Preserve full complex data.

Use both v15.96 preparation arms and five declared edges, source lambda [-1,0,1] and the actual no-source origin u=0. Directions in lexicographic X,Y,Z order: first27 on012 then27 on013, normalized /4. Additional81 exact-weight-four directions /4. No direction selection. Finite hidden amplitude epsilon=1e-4. Positive source ladder a=[1e-3,3e-4,1e-4], with all u in {0,a,2a}. Python3.11,numpy2.3.5,sympy1.13.3,mpmath1.3.0; single BLAS thread. Total72 analytic state/lambda/arm rows.

## Exact and null controls

Eight grouped exact checks: (1) P,Q Hermitian involutions and anticommute; (2) A± Hermitian involutions; (3) derivatives of the four finite source weights at u=0 equal [-(r+ + r-),r+,r-,0] with r±=(1±lambda)/2; (4) expansion of L into incoherent plus lambda cross term on all nine local two-body Paulis; (5) the four-entry one-body cross-leakage table in DERIVATION and zero remaining entries; (6) incoherent local generator has zero one-body projection on all nine; (7) local -i[ZI,.] has zero one-body projection on all nine; (8) spectator Pauli trace zero and trace preservation of both conjugations, establishing the weight-four restriction null. Reuse v15.96's13 exact geometry/frame checks and v15.92's45 preparation checks unchanged.

Numerical controls: hidden Gram matrix identity; zero trace and Hermiticity error; zero one-/two-body moments of all54 probes; zero one-body moments of Lh; zero pair leakage for all81 weight-four probes at all lambda; zero pair leakage for the local Hamiltonian on all54. Retained leakage in cross-loop blocks and baseline hidden response must vanish. Null response matrices for lambda0 have rank0 at all frozen thresholds and norm<=1e-9. These are validity controls, not source-response YES hypotheses.

## Analytic response and covariance

At u=0 extract postprocessed centers and mixed edge derivatives from global matrices. Solve the frozen skew Sylvester equation, form both differentiated loop products and left-trivialized K6x54; form invariant J3x54 from trace derivatives. Store full K,J, singular values, ranks, edge-response ranks and baseline loops. Thresholds for K,J and edge response: [1e-9,1e-10,1e-11], absolute reference1. Store per-loop and per-probe-family ranks. No rank inferred solely from generator activity.

Check Sylvester equations, skewness of delta H H^T, zero cross-loop blocks, and proper polar identities at1e-9. Domain at baseline and every finite stencil: all five planar edges rank2, or all five isotropic edges rank3 with positive full-polar determinant. Edge ranks use thresholds times the leading unprocessed correlation singular value, as v15.96. Domain exits are scientific NOs with null affected response fields, not INVALID when other controls pass.

Use the same four quaternion frames as v15.96, one independent frame per site. Transform global states, probes, source unitaries and postprocessed centers/tangents. For the anisotropic arm, the transformed channel is Ad_U composed with preparation composed with Ad_Udagger; never reapply an unchanged planar map to transformed input. Independently extract and recompute response in the transformed frame. K must transform by blockdiag(G0,G0), J must remain unchanged, and rank lists must match. Covariance tolerance1e-9.

## Independent finite evaluation

For every row and every54 hidden probes, use physical states sigma±epsilon h, the unchanged finite source at u=0,a,2a, and global postprocessing. Recompute polar loops directly. Let F_r(u)=[H_r(sigma+epsilon h,u)-H_r(sigma-epsilon h,u)]/(2epsilon). Estimate mixed derivative [-3F_r(0)+4F_r(a)-F_r(2a)]/(2a), then project its product with H_r(0)^T onto skew coordinates for K. Independently apply the same finite differences to the three scalar invariants for J. Record each ladder error divided by max(1,Frobenius norm of its analytic matrix). At the final frozen step, both errors must be<=1e-4 for numerical validity; no monotonic or asymptotic scaling claim is required. Record baseline hidden finite difference norm and require<=1e-9. Only compare derivatives if baseline and all relevant stencil geometries lie in domain. The smaller steps are not used to rescue a failed final-step criterion.

Check density positivity >=-1e-12, trace/Hermiticity<=1e-12 for all perturbed inputs and every finite source/output stencil, including u=0. Source unitarity<=1e-12; every used weight vector nonnegative within1e-12 and sum within1e-12. Together with exact source unitarity and inherited preparation certificate these certify finite CPTP maps; no d=8 Choi wrapper is used. Check analytic-vs-direct connected mixed correlation extraction<=1e-12 using zero single-body response, and input reconstruction/hidden/null algebra controls as above. All reported numeric data must be finite.

## Frozen adjudication

Validity requires all parent, count, exact, physical, null, derivative-identity, finite-difference and covariance controls. INVALID overrides both verdicts if any fails. Primary OVERLAP_HIDDEN_RESPONSE_CONFIRMED iff valid and all24 coherent isotropic rows have baseline/transformed/stencil domains and K ranks[6,6,6], J ranks[3,3,3]. Otherwise OVERLAP_HIDDEN_RESPONSE_NOT_CONFIRMED. Secondary PLANAR_TWO_LOOP_RESPONSE_CONFIRMED iff valid and all24 coherent planar rows have all domains and K,J ranks[2,2,2]. Otherwise PLANAR_TWO_LOOP_RESPONSE_NOT_CONFIRMED. Incoherent rows are null controls. Tests accept valid scientific NOs. Never modify these thresholds after measurement.

## Publication

Publish this preregistration, derivation, tests and targeted workflow without gate.py. Inspect expected RED logs and downloaded artifact. Implement only this frozen measurement, run CI, inspect actual scientific JSON and exact logs/artifact/checksums. Publish RESULTS.md with exact hashes and interpretation boundaries. No main merge. This gate studies a specified source law at its origin, not admissible-world selection or the necessity of quantum entanglement. It does not resolve fundamental gravity.
