# v16.02 — Full-ensemble global precision certification

Parent documentation head bc6bdbcf244261e3579b6300535e6e4c543f62d9; branch research/v16.02-full-ensemble-precision. This is a new certification, not a revision of v15.99 INVALID, v16.00 FROZEN_INPUT_RANK_RESIDUAL_PERSISTS, or v16.01's eight-case scope.

## Frozen ensemble and arithmetic

Use all twelve archived v15.96 states (indices 13,16,22,25,27,29,37,39,46,50,66,77), all 81 original weight-four probe columns, overlap/disjoint source pairs, both orders and contrast, planar/isotropic final preparations, and binary attenuation values 1, 1/3, 1/6, 0. Exactly 192 rows: 144 positive-a and 48 erasure rows. No sampling, source-law change, normalization, input repair, rank projection, threshold adjustment, or fitted alignment.

Pin all inherited Python and compressed-result dependencies with SOURCE_MANIFEST.json before implementation. Explicitly require v16.01 raw result SHA256 8308d457346e42755697228c4877db2b28eeedb93f6f3c9a16d551aa4449b7ba, valid recovery verdict; v15.99 raw 8107f3f6ac83b08ba9ff9490d56518a10ca823f9bd92a290adf418cc79d9ebbb, historical INVALID; v15.96 raw 99d55b90eee2f05fa979401aaedcfb05af71e35f958efeef1b30ed43affb1d9e. Python 3.11, numpy 2.3.5, sympy 1.13.3, mpmath 1.3.0; one BLAS thread.

Use v16.01's full 256-dimensional global Pauli operator path at both 50 and 80 decimal digits. Preserve exact binary real and imaginary density entries and attenuation values. Independently build transformed local sources and preparation operators at each precision. Planar preparation is the existing I,X,Y mixture with weights 1/2,1/4,1/4. Isotropic preparation is the equivalent I,X,Y,Z mixture with weights 1/2,1/6,1/6,1/6 (Bloch factor 1/3). Derive its transfer from these operators, including their transformed counterparts. Do not transform a previously calculated retained answer to manufacture measured covariance.

## Response and domain

Recompute baseline C, source C, and centered mixed dC globally for every row/order/frame. Use the unchanged oriented rank-two polar/Sylvester algorithm for planar edges. For isotropic edges use the full polar factor U V^T, requiring rank three and positive determinant; never flip it. Reference is the leading unprepared source-C singular value. The original relative domain thresholds and absolute K/J rank thresholds remain 1e-9,1e-10,1e-11. Positive-a domain exit is a scientific NO with undefined response fields, not a manufactured rank-zero response.

Native/transformed K and J must have identical rank lists; absolute covariance residual <=1e-35 at both precisions. Compare each measured native response to a times the pinned v15.98 response at all thresholds; normalized Frobenius scaling residual <=1e-9. Record actual K/J arrays, singular spectra, ranks, loops and edge diagnostics in both frames and precisions. Compare baseline loops/polars with v15.98 <=1e-9. Require contrast linearity, overlap first-loop null, and disjoint retained contrast (including rank zero) <=1e-9. Do not demand global inserted disjoint protocols commute.

## Unchanged physical and finite controls

Rerun v15.99's unmodified measurement to freshly execute its eight exact plus 74 inherited checks, explicit 1296-outcome map certificate on all 256 matrix units, 108 finite intermediate centers, finite channel/affine probes, density checks, hidden nulls, scaling identities and complete-erasure checks. Preserve that execution's own INVALID verdict if its old rank-covariance check still fails. Its numerical rank-covariance boolean is replaced only in this new gate by the independent high-precision full-ensemble comparison, not waived in the historical gate. All other original controls, counts and tolerances must pass. Archive this complete fresh execution separately.

Additionally compare freshly computed finite-channel connected differences and affine-loop finite differences directly against this gate's native high-precision dC and K/J for every positive row and both orders. Keep epsilon=1e-4, source strengths=0.1, eta=1e-6, finite-channel tolerance 1e-7 and affine K/J tolerance 1e-5, with original max(1,norm target) normalization. Preserve physicality and domain checks of these identical stencils from the unmodified rerun. Undefined positive-a affine domains cause scientific NO; undefined comparisons are skipped.

At a=0 independently form the global erased baseline and all source/preparation tangents in both frames and precisions, require their original <=1e-12 zero/identity bounds, and leave every polar response field null. The unchanged finite-channel erasure controls must also pass for all 48 rows.

## Validity and decision

Require v16.01 local channel certificates, complex basis reconstruction, exact state binary roundtrip, solver positive/skew/symmetric-null/rank-one controls and witness controls, all <=1e-35; add a full-rank solver and negative-determinant rejection control. Record global stage and retained covariance independently, each <=1e-35. Compare 50/80-digit global stages, retained tensors, and responses <=1e-30; require identical rank lists and domain status. Nonfinite values, failed prerequisites, failed physical/finite/algebra controls or covariance cause INVALID, overriding both verdicts.

Primary FULL_ENSEMBLE_EB_RESPONSE_SCALING_CONFIRMED iff valid and every positive row has all applicable domains, parent rank lists and scaling within the original bounds; otherwise FULL_ENSEMBLE_EB_RESPONSE_SCALING_NOT_CONFIRMED. Secondary FULL_ENSEMBLE_ERASURE_POLAR_UNDEFINED_CONFIRMED iff valid and all erasure controls pass with undefined polar responses; otherwise FULL_ENSEMBLE_ERASURE_NOT_CONFIRMED. Tests must allow a valid scientific NO. No rescue tuning after measurement.

Publish preregistration, tests and workflow before implementation; inspect expected absent-implementation RED. Then implement, inspect exact CI logs and downloaded artifacts/JSON, verify source/result hashes, and publish RESULTS.md. No merge to main. This remains conditional on the specified source and preparation laws; no universal law selection, surviving reference entanglement, fully classical process, or gravity derivation is claimed. Time is pruning / ordered recoverability update; geometry is extracted from retained relations.
