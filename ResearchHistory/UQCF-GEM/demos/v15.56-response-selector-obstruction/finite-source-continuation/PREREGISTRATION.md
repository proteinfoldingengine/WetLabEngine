# v16.03 frozen finite-source continuation gate

Parent publication 90ca400855ae45a408ecb42f71be08cfd64f7e16; scientific input is the verified v16.02 run 36440529651 at ccc65c5569e904be3c98ec61e3d231f8e693eb92. PARENT_J.json.gz preserves a lossless extraction of all 144 positive-a native 80-digit forward/reverse J matrices from the verified raw JSON (source SHA256 6b0e8e5a143df5c7ece910e1b3d9fe7204d916ea2cdce7f181ccc1f12ebe9eb9). Extraction raw SHA256 bcc465fcc363106f77e2f856eeaa205721e164889c70d3f7b729f3e2cf4fe745. The complete original remains in artifact 10978763246. This compact extraction avoids duplicating the 87 MB parent JSON in every new checkout. Historical verdicts remain unchanged.

## Frozen ensemble and implementation

All 12 archived candidates [13,16,22,25,27,29,37,39,46,50,66,77], all 81 weight-four probes, overlap/disjoint pairs, both orders, plane/isotropic preparations, a=1 and the exact archived binary floats 1/3 and 1/6. Complete a=0 erasure is a separate undefined-domain control. Both 50 and 80 decimal digits; Python 3.11, numpy 2.3.5, sympy 1.13.3, mpmath 1.3.0; one BLAS thread.

Use actual finite centers for lambda=2^-4,2^-5,2^-6,2^-7,2^-8 with E_X(lambda)=I+lambda L_X. These are mixture parameters. Do not use an origin center or change a failed step. Rebuild global native and transformed sources, states and preparation at each precision using the parent global path. The result consists of 144 positive-a origin rows and 720 fixed finite-step rows (each with both orders, frames and precisions). Shard by the 12 candidates; each shard must evaluate both precisions.

The primary new matrix is T=D^2 F(C0)[Vf-Vr,B] for disjoint pairs. Differentiate the Sylvester equation analytically; do not obtain T by fitting or finite-lambda differences. Include connected-centering derivatives in V. Evaluate both preparations and all a, including the exact disjoint a=1 null. Record all 3x81 arrays, spectra and ranks at inherited absolute thresholds 1e-9,1e-10,1e-11. Evaluate origin J and compare to the archived 16.02 80-digit native arrays.

## Independent checks and arithmetic validity

The differentiated Sylvester implementation must satisfy its equations, mixed-derivative symmetry, and an analytic identity-center example with J mixed derivative (-2,-2,-8) for a shared-edge skew direction. Its first derivative must agree with the inherited readout. Check its Hessian independently by a centered directional difference of the first derivative at C0 plus/minus h V, h=1e-6, whenever both probes are in the frozen domain. Normalize by max(1,norm T); use the inherited affine tolerance 1e-5. An out-of-domain artificial derivative-check stencil is recorded as unavailable, never as a scientific domain exit; the algebraic/symmetry/analytic controls remain mandatory and at least one eligible independent stencil per arm is required for complete certification.

All source manifests and extracted parent hash must match. Source/preparation controls, exact hidden and one-body nulls, analytic solve identities, covariance of global stages/retained inputs/invariant outputs, and exact nulls use 1e-35. The 50/80 comparison uses 1e-30 and identical rank lists/domain decisions. Origin comparison to the parent uses 1e-30 (compare native high-precision arrays, not historical float64). Record absolute residuals, not only relative comparisons. All values must be finite. Preserve frozen edge rank/reference tests (1e-9 supported and 1e-11 planar discarded). No rank repair, threshold change, fitted frame, clipping or normalization of states.

Physicality: check every native finite unprepared/prepared center and rho plus/minus 1e-4 h using inherited float64 density diagnostics at 1e-12. Physical maps are convex combinations of certified unitary conjugations plus inherited CPTP middle/preparation maps; record nonnegative normalized mixture weights. Transformed physicality follows from the independently checked unitary frames. Check a=0 maps the centers to I/16 and annihilates hidden tangents in both frames; leave polar response undefined.

## Scientific decisions

INVALID overrides scientific outcomes if any mandatory arithmetic, source, finite-value, physicality, or covariance control fails. A finite physical center exiting its polar domain is a valid scientific domain obstruction, not a numerical INVALID; record it with null responses. Do not repair it or treat it as a zero matrix.

For each disjoint EB row (48 total), classify T as resolved-active if its leading singular value exceeds 1e-9 at both precisions, numerical-null if its Frobenius norm is <=1e-35 at both precisions, otherwise unresolved. Rank lists and classification must agree across frames and precisions. Primary verdict DISJOINT_CUBIC_RESPONSE_DETECTED if at least one EB row is resolved-active; DISJOINT_CUBIC_NUMERICAL_NULL if all 48 are numerical-null; otherwise DISJOINT_CUBIC_UNRESOLVED. Numerical-null does not mean a proof of exact zero.

Finite continuation verdict: FINITE_GRID_OVERLAP_RESPONSE_CONFIRMED iff all 360 overlap finite-step rows are in domain and the normalized invariant contrast has leading singular value >1e-9; otherwise FINITE_GRID_OVERLAP_RESPONSE_NOT_CONFIRMED. This is a statement about this fixed grid, not the existence theorem's unknown neighborhood. Record disjoint finite contrast independently, including its a=1 exact-null control.

For each valid step publish Delta Jphysical=lambda^2*(Jhat_f-Jhat_r), its /lambda^2 or /lambda^3 normalization, and the residual to the analytically computed leading coefficient. These five residuals are descriptive finite-remainder data: no fitted exponent and no unproved uniform Taylor bound is claimed. The design's missing remainder rule is resolved by separating exact coefficient adjudication from descriptive finite remainders. The independent small directional check has the fixed tolerance above; large-lambda remainder sizes are not an arithmetic failure or an adjustable pass criterion.

## Publication and scope

Publish this preregistration, source manifest, tests and targeted workflow before implementation; inspect expected absent-implementation RED. Tests permit a valid scientific NO. Run the complete fixed ensemble, inspect all shards and exact job logs/artifacts, then publish raw compressed JSON, checksums and RESULTS.md. No merge to main. No gravity derivation, universal source-law selection, fundamental time or external alignment is claimed.
