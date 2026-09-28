# v15.96 preregistration — overlap holonomy common line

Parent0bb9d708f1a793dc0020000426ede5391b8e76f9; branch research/v15.96-overlap-holonomy-common-line. Freeze before implementation/expected RED. No new sampling, fitting, threshold rescue or historical verdict change.

## Inputs and construction

Pin compatible-holonomy-reduction/gate.py c38eba50e1d99e01026cb956fd308f750b48b9932422ca100966c16a70a5251a; RESULT.json.gz f05a0ebc7d41128d8b2be4fd46161d7827f623d6107da8b3dd2c4585cb95561f; raw JSONee9b13d07c3856357b157fdcf58854957fe56767ee55eeba61266b34ee40e607. Require all_valid and FIXED_SUPPORT_HOLONOMY_REDUCTION_CONFIRMED plus PLANAR_LOOP_RESPONSE_CONFIRMED. Also pin preparation-span-obstruction/gate.py7d65d2525353ec83426694e5375881740031c33d2bb02ea38aec4737ac052ec9 for its exact local preparation definitions.

Use all12 original states in order[13,16,22,25,27,29,37,39,46,50,66,77], pair each with its cyclic successor, and form sigma_k exactly as DERIVATION. No positivity selection or resampling. Extend the frozen source unitaries by tensor I on qubit3: lambda[-1,0,1],u=0.1, unchanged v15.81 weights. Apply both planar and isotropic local preparation channels to all4sites. Total72 state/source/arm cases. No hidden derivative is measured in this gate. Python3.11,numpy2.3.5,sympy1.13.3,mpmath1.3.0.

Retain regions012,013 and edges[01,12,20,13,30]. Record spectator edge23 separately including C and rank. Validate region01 overlap by independent partial traces, and match regional extraction to direct global Pauli extraction. Source acts only01, so spectator marginal must remain unchanged.

## Exact and numerical controls

Use symmetric traceless basis: diag(1,-1,0)/sqrt2, diag(1,1,-2)/sqrt6, and symmetric xy,xz,yz off-diagonal units/sqrt2. Thirteen new exact grouped checks: basis orthonormality; D(Rx90 Rz90)=D(Rx90)D(Rz90); planar Z with cos3/5,sin4/5 and F=diag(1,-1,-1) fix N-I/3 for N=diag(0,0,1); their stacked B rank4; ||FZ-ZF||^2=128/25; quarter-turn Rx90,Rz90 stacked B rank5; conjugation covariance D(GHG^T)=D(G)D(H)D(G)^T for both quarter-turn controls using the first frozen frame (one grouped check); swap S23 is unitary and involutive; exact spectator connected-correlation identity from symbolic Bloch vectors (one grouped check); four quaternion frames each satisfy SO(3), SU(2) and Pauli-adjoint correspondence (four grouped checks). Total13.

Frames are normalized quaternions(w,x,y,z)=(1,2,3,4),(2,-1,3,1),(3,2,-1,2),(1,-2,1,3). U=(wI-i(xX+yY+zZ))/sqrt(norm_squared). Reuse all45 v15.92 exact local-channel/affine checks without editing them. Numerical controls must reproduce B rank4 for the noncommuting shared-line pair and B rank5 for the quarter-turn pair at all thresholds[1e-9,1e-10,1e-11], reference1. Noncommutation alone is not the scientific discriminator.

## Channel and state certificates

Implement four-site postprocessing independently through normalized Pauli coefficients (256basis elements) and through tensor-product POVM/preparation states (plane256outcomes, isotropic1296). Verify both on all256 computational matrix units and every output center. Require POVM completeness/Hermiticity, prepared-state trace/Hermiticity/positivity, outcome probabilities real/nonnegative and summing to1. This is an explicit full-separability certificate, not merely PPT. Store center probabilities for every row.

Compute source and composite Choi matrices from matrix-unit action with d=16: three source and six composite maps. Check CP/TP/Hermiticity. The old d=8 CP wrapper must not be reused without correcting the dimension in this new implementation. Check all12 constructed inputs,36 source centers and72 outputs for density validity. Numerical thresholds: eigenvalues/probabilities>=-1e-12; trace/Hermiticity/TP/POVM/probability/independent reconstruction/marginal/spectator/connected affine residuals<=1e-12. Scalar norms are Frobenius, array reconstruction checks may use maximum entry. Preserve full complex arithmetic.

## Geometry and common-line measurement

For each declared edge store source/output C,singular values,ranks at thresholds[1e-9,1e-10,1e-11] times its source leading singular value. Domain: planar all5edges rank2; isotropic all5edges rank3 with positive full polar determinant. Do not rescue domain exits by completing a different rank or flipping a full-rank polar factor. A row outside its domain has null loop/B fields and gives a scientific NO, not INVALID, if its quantum/algebraic certificates remain valid.

Inside domain, form both based loops. Record R,H1,H2, ordinary commutator norm, group-commutator distance, the full B10x5 matrix, singular values, ranks and kernel dimensions. B thresholds have fixed reference1. Check proper orthogonality and polar reconstruction, D(H)^T D(H)=I, and equality of the two commutator norms at1e-9. For planar cases record the fixed normal tensor N-I/3 residual under both loops; this must be<=1e-9 for validity but no orientation-sign restriction is imposed.

Transform the full output density by tensor U0 U1 U2 U3, independently extract all correlations, recompute polar links/loops/B where the transformed rank domain holds, and compare to endpoint frame covariance. Compare B singular values and loop commutator scalars for invariance. Tolerance1e-9. A transformed domain exit is a scientific NO, with null transformed completion data, not an algebraic INVALID. This changes coordinates of the full output state; do not reapply an unchanged anisotropic channel after rotation.

## Verdicts

Validity: parents/indices/counts,13new and45inherited exact checks, both numerical rank controls, all nine Choi and all state/preparation/POVM/reconstruction/overlap/spectator/affine checks, finite data, applicable geometry/covariance identities within frozen limits. Primary OVERLAP_COMMON_LINE_OBSTRUCTION_CONFIRMED iff valid and all36 isotropic cases and transformed cases lie in domain and B has rank5 at every threshold. Otherwise OVERLAP_COMMON_LINE_OBSTRUCTION_NOT_CONFIRMED. Secondary PLANAR_COMMON_LINE_PRESERVED iff valid and all36 planar cases and transformed cases lie in domain and B rank<=4 at every threshold. Otherwise PLANAR_COMMON_LINE_PRESERVATION_NOT_CONFIRMED. INVALID overrides both. Valid scientific NOs are accepted by tests; do not change thresholds or inputs after measurement.

## Execution and interpretation

Publish prereg/derivation/tests/workflow without gate.py; inspect expected GitHub RED and downloaded artifact; implement only frozen measurement; run CI; inspect actual JSON/logs and verify downloaded artifact/head/source/checksums; publish reproducible evidence. No merge to main. No inference of continuous SO(3) holonomy, causal source response from baseline loops, a complete six-edge atlas, physical source selection or gravity. All scientific NOs remain unchanged.
