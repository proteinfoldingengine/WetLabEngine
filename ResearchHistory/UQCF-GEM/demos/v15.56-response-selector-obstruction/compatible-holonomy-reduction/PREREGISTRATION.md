# v15.95 preregistration — compatible holonomy reduction

Parent22f93cd9483eacca8d09e89e8a1b4aa8aa47a77b; additive branch research/v15.95-compatible-holonomy-reduction. No measurement before expected RED, no new random states, fitted support or source law. Preserve all historical verdicts.

## Frozen parents

Pin oriented-composition-compatibility/gate.py SHA-256 a62df70edfef9f30563d4dd89681508d5c35e577a7d26bb1d59b798e74e634a1; RESULT.json.gz 627e9ac50b1ead13f76036965f020db19c85f5287f669e9a23f1a589118cc04a; raw JSON7c9fc2bf42316e366d059e7b45d2aa8ebdeb11947a5b7593c4808de608a8e6b4. Require all_valid and both ORIENTED_COMPOSITION_OBSTRUCTED and MATCHED_SUPPORT_COMPOSITION_CONFIRMED.

Pin oriented-rank-two-response/gate.py e12b740453761330add8f8d9694befa242e6b5c24bc9c6b49870d648b5c8725c; RESULT.json.gz4c3e4d893c69f1a72a5409f905a1eafa81d4a0295b10439a0643ed21ba1dcc09; raw JSON540f46f32bf8f74ad2c4283870d14f36427b16d0155444546e7113cedd26cd2a. Require all_valid and ORIENTED_RANK_TWO_READOUT_CONFIRMED plus PLANAR_ORIENTED_RESPONSE_CONFIRMED.

Use all36 v15.93 rows: candidates[13,16,22,25,27,29,37,39,46,50,66,77] x lambda[-1,0,1], source u=0.1,27 hidden directions. Read all archived C,dC,V,R,W and E_map. Supports and preparation channel are fixed under hidden perturbation. Use Python3.11,numpy2.3.5,sympy1.13.3,mpmath1.3.0. No new density operators or physical source updates: inherit physicality from pinned parents.

## Thirteen exact checks and independent controls

Use rational planar rotation Z(t), c=(1-t^2)/(1+t^2), s=2t/(1+t^2), F=diag(1,-1,-1), P=diag(1,1,0), J=[[0,-1,0],[1,0,0],[0,0,0]]. Ten grouped checks: both Z and ZF are proper orthogonal; their normal actions are +z and -z; both preserve P; FZF=Z^T; at t=1/2, ||FZ-ZF||_F^2=128/25; the symbolic skew commutator with P has a one-dimensional kernel; two rational planar rotations commute; the three-link derivative with dR_e=R_e*w_e*J gives Omega=(w0+w1+w2)J; the axial response Jacobian in w0,w1,w2 has rank1; unrestricted skew generators produce rank3. Plus three exact inherited rational quaternion-frame checks gives13.

Numerical controls: feed the production loop-tangent function identity links with x,y,z generator derivatives on the first link and zero elsewhere; its axial map must equal I3 (no automatic projection onto the normal). A rational normal-flip/rotation control must have commutator squared norm128/25 and preserve P. These are matrix-algebra controls, not new physical channels.

## Frozen measurement

For every row independently recompute R and W from archived C,dC using v15.93's oriented and Sylvester functions, requiring C rank2 at all [1e-9,1e-10,1e-11] thresholds times its archived edge reference. Compare R,W and edge E_map against archived values at1e-9. Extract P_i=V_i V_i^T from archived support factors; verify each R_ij P_j R_ij^T=P_i, including initial/final support agreement, at1e-9. Record each edge normal action in the inherited planar frame and its rank. Do not repair factors or choose new planes.

Form H=R01 R12 R20 and dH by the full matrix product rule for each hidden direction. Form Omega=H^T dH and K[:,h]=(Omega21,Omega02,Omega10). Also compute Omega by the independently assembled body-tangent conjugation formula. Compare K with the signed-sector specialization sum of the three archived E_map edge blocks. The latter specialization is valid only for the frozen normal-preserving sector; guard that sector rather than assuming it for arbitrary data.

Record H, all Omega, full K3x27, singular values, ranks, norm, ||H-I||, normal-sign scalar tr[(I-P0)H], and plane preservation. Require skewness, [Omega,P0]=0 and P0*K=0 within1e-9. Record K ranks at [1e-9,1e-10,1e-11] times max(1,archived E reference), giving a fixed absolute floor for the null.

For each of the972 row/hidden derivatives, central-difference the loop made from oriented completions of C_e+epsilon*dC_e simultaneously. epsilon=b*min_e(s2_e)/max(1,max_e||dC_e||_F), b=[1e-3,1e-4,1e-5]. Use the top-two support factors for these exactly planar matrix probes. Record all steps/errors normalized by max(1,||dH||_F). Require final-rung error<=1e-6; no monotonic-convergence requirement. These are matrix-space paths, not finite quantum-state updates.

Covariance uses the same three rational quaternion frames as v15.93. Independently recompute R,W from G_i C_ij G_j^T and G_i dC_ij G_j^T, then recompute H,Omega,K. Verify H'=G0 H G0^T, Omega'=G0 Omega G0^T, K'=G0 K, and the transformed P0 confinement, all within1e-9. This is a coordinate check, not a new physical frame family. Compare H to the archived v15.94 compatible triple completion at1e-9.

## Validity and verdicts

Validity: all pins/parent verdicts/indices,36 rows,13 exact checks and both independent numerical controls, finite data; all archived/reconstruction, product-rule, skew, support, normal-sector, covariance and parent-triple residuals<=1e-9. Final finite-difference residual<=1e-6. Every row must retain the frozen rank-two input and normal-preserving sector; an exit invalidates this aggregation experiment because its input assumptions differ from the pinned parent, not a universal physical failure.

Primary FIXED_SUPPORT_HOLONOMY_REDUCTION_CONFIRMED iff valid and all loop K ranks<=1 at all thresholds; otherwise FIXED_SUPPORT_HOLONOMY_REDUCTION_NOT_CONFIRMED. Secondary PLANAR_LOOP_RESPONSE_CONFIRMED iff valid, all24 coherent rows have K rank1 at every threshold and all12 incoherent rows have K rank0 and norm<=1e-12; otherwise PLANAR_LOOP_RESPONSE_NOT_CONFIRMED. INVALID overrides both. Tests accept valid scientific NOs and check verdict separation. No threshold or source change may rescue a negative outcome.

## Execution and boundaries

Publish prereg/derivation/tests/workflow absent gate.py; inspect expected GitHub RED and downloaded artifact. Implement frozen gate, run targeted CI, inspect actual result JSON/logs, download/hash artifacts, verify execution/source/checksum bytes, and publish RESULTS/EVIDENCE and lossless result data. No merge to main. No claim that the full O(2) stabilizer is abelian, no empirical inference of a global gauge group from one triangle, no fixed-support tangent bound for moving supports, no source-law selection, physical recovery, fundamental time or gravity derivation.
