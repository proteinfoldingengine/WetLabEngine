# v16.01 preregistration — global input precision

Parent be25cd28806bea11de0b57da1a342b03c57cf28a; branch research/v16.01-global-input-precision. Freeze before implementation. Preserve v15.99 INVALID and v16.00 FROZEN_INPUT_RANK_RESIDUAL_PERSISTS regardless of this outcome.

## Frozen problem

Pin precision-readout-audit/gate.py SHA2567eeead6262372ac6e57fc1a39d90775bd883227c017285997079c8fd70261fab, gzipccebbb43faf27b7c5d8825e9b53571067ca40011c575618119f059550effa4a2, raw7d2fcc55c51474f12ac596ca5321d6a8e22265560066d64ded61e945ffd0fd24. Require valid negative verdict and all eight cases unrecovered. Pin v15.96 input raw99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e.

Exactly the same eight comparisons: candidate66 overlapping pair reverse/contrast at a=1,1/3,1/6; candidate77 disjoint pair forward/reverse at a=1/6. All81 weight-four probes with the original column labels. Precision50 and80 decimal digits; unchanged rank thresholds1e-9,1e-10,1e-11. Expected K/J ranks1/1 for66 and2/2 for77.

Use the exact binary values of archived density entries, including imaginary components, without normalization or clipping. Decode each archived binary attenuation value exactly; do not replace it with a fitted or adjusted amplitude. Reconstruct the specified algebraic source and quaternion frame matrices at the working precision, rather than promoting already-rounded float64 matrices. Python3.11, numpy2.3.5, sympy1.13.3, mpmath1.3.0; one BLAS thread; no new sampling.

## Global calculation

Represent the complete four-qubit operator by all256 coefficients in the orthonormal basis B_w=P_w/4. Extract coefficients from the complex16x16 density matrix and verify reconstruction. This is a full global operator representation, not a retained-region approximation.

Derive local SU(2) frame superoperators from explicit quaternion unitaries. Rotate every probe to Gamma h, preserving its original column label. Independently derive native and transformed two-site source transfer matrices from AP=(Z tensor I+X tensor X)/sqrt(2) and AP'=(U_i tensor U_j)AP(U_i tensor U_j)^dagger. The coherent generator is Ad_AP-I. Do not obtain a transformed source response by rotating a previously computed retained answer.

Apply the intermediate product depolarizing map to the full coefficient vector with factor a^weight. Apply the planar preparation independently at every site: mixture (1/2)Ad_I+(1/4)Ad_X+(1/4)Ad_Y, with rotated X,Y operators in the transformed protocol. These are mixture weights; the Kraus amplitudes are I/sqrt(2),X/2,Y/2. Derive the local transfer matrices from these explicit complex operators.

Build both ordered global derivative chains when needed for contrast. Extract one- and two-body moments as4 times their normalized Pauli coefficients, form connected C and dC including centering, then use the unchanged v16.00 high-precision readout. No repaired inputs, rank projection of responses, or fitted frame alignment.

## Validity controls

Exact state binary roundtrip; original input trace/Hermiticity<=1e-12 and minimum eigenvalue>=-1e-12. Do not impose an arithmetic-level trace-one condition on the unmodified binary input. Require basis reconstruction, imaginary residuals of Hermitian Pauli coefficients/transfer matrices, local unitarity, transfer-matrix reconstruction on every local Pauli basis element, trace-preservation/generator trace-zero, and frame SO(3) identities<=1e-35 at both precisions. Real coefficient conversion is allowed only after checking its imaginary residual; never discard density imaginary entries.

Validate the global embedding with the frozen witnesses YYXX/4 through A then B (pair restriction -a^3 IXIX/4) and XXXX/4 through A then D (pair restriction a^3 ZIZI/4), at every positive a used. Require witness errors, individual hidden pair nulls and lower/mixed one-body nulls<=1e-35. Reuse both v16.00 solver-control suites unchanged (three active skew directions, symmetric nulls, rank-one rejection).

Native fresh retained C/source-C/dC must agree with the archived v16.00 native binary arrays within absolute Frobenius1e-12, and fresh native K/J with the archived80-digit native readout within1e-9. These are identity controls, not a changed rank threshold. Require the inherited planar readout domain and arithmetic identities<=1e-35, finite data, and50/80-digit convergence of global stage vectors, retained tensors and K/J<=1e-30 with identical rank lists. Invalid prerequisites give INVALID.

Local channel validity follows from the explicit positive mixture/depolarizing weights, unitary controls and trace-preservation. Global tangents are not density matrices and are not required to be positive.

## Recovery measurement

Independently record covariance residuals at the global input, first-source, intermediate-channel, second-source and final-preparation stages, including baseline state stages. Compare with Gamma acting on the native full coefficient vector. Record retained C/source-C/dC covariance under the prescribed rational SO(3) frames and K covariance under blockdiag(G0,G0), with J invariant. No response is replaced by its covariant prediction.

GLOBAL_INPUT_PRECISION_RECOVERY_CONFIRMED iff valid and every declared stage/tensor/response covariance residual<=1e-35 at both precisions, with both native and transformed K/J rank lists equal to the expected native lists at all original thresholds. Otherwise, if valid, GLOBAL_INPUT_PRECISION_RECOVERY_NOT_CONFIRMED. INVALID overrides either. Tests accept a valid scientific NO. No post-measurement threshold or amplitude adjustment.

Archive full freshly formed retained inputs and K/J at both precisions, stage residual summaries, convergence and identity controls, and exact provenance. Verify expected absent-implementation RED before implementation; inspect actual scientific JSON, logs and downloaded artifacts even after failure. Publish RESULTS.md; no main merge.

This adjudicates only the eight failures, not all144 v15.99 positive-a rows. Recovery would resolve their numerical consistency but would not isolate one faulty upstream operation, select a physical source law, or derive gravity. Genesis Pin, ordered recoverability and geometry extracted from retained relations remain unchanged.
