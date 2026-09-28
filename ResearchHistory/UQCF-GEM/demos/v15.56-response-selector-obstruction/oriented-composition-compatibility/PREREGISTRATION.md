# v15.94 preregistration — oriented composition compatibility

Exact parent aee440c43996f9a14cc4973473aa403ed9eeb01e; branch research/v15.94-oriented-composition-compatibility. Freeze before implementation and expected RED. No new state, fitted plane, random frame, source law or amplitude sweep.

## Pinned inputs

oriented-rank-two-response/gate.py SHA-256 e12b740453761330add8f8d9694befa242e6b5c24bc9c6b49870d648b5c8725c; RESULT.json.gz 4c3e4d893c69f1a72a5409f905a1eafa81d4a0295b10439a0643ed21ba1dcc09; decompressed JSON 540f46f32bf8f74ad2c4283870d14f36427b16d0155444546e7113cedd26cd2a. Require both v15.93 confirmed verdicts and all_valid. Read all 36 archived rows (12 states x lambda=-1,0,1), all three archived support factors V. Do not repolarize these factors before raw multiplication. Compare their independently computed completions to archived R.

support-loop-composition/RESULT.json SHA-256 bb2299a633e857beeabce7b05208b9c924d88b3bbceb1f033f772657457c7166. Require all_valid and its three certified verdicts: SUPPORT_RESTRICTED_CROSSING_CONFIRMED, SUPPORT_LOOP_COMPOSITION_OBSTRUCTED, LOSSLESS_LOOP_CORE_TRIVIAL. Read its archived loop L as float64 from the 80-digit decimal strings; do not recompute the root or modify/repolarize L before forming L*L. Validate partial-isometry residuals after conversion and compare L*L to its archived second power. This is a float64 diagnostic of that stored native witness, not a new high-precision root certification or held-out population.

Use Python3.11, numpy2.3.5, sympy1.13.3, mpmath1.3.0. Relative rank thresholds [1e-9,1e-10,1e-11] have fixed unit reference1. All matrix discrepancies are Frobenius norms unless explicitly scalar.

## Exact and numerical controls

Twelve exact checks: three inherited rational quaternion frames have R^TR=I and detR=1; canonical P and Q are plane projectors (one grouped check); QP=U*diag(c,1,0); (QP)^T QP=diag(c^2,1,0); V=UP is a rank-two partial isometry; V+cof(V)=U; ||U-I||_F^2=4(1-c); ||P-Q||_F^2=2(1-c^2); t=0 is the matched completion control; t=1 has rank-one product and two distinct proper completions. Domain 0<t<1 is stated analytically. Total12.

Three numerical rational fixtures: (A,B)=(P,P), (Q,P) with U_y=[[3/5,0,4/5],[0,1,0],[-4/5,0,3/5]], and (Q0,P) with U_y=[[0,0,1],[0,1,0],[-1,0,0]]. Expected c=1,3/5,0; product ranks2,2,1; squared discrepancies0,8/5,undefined. Rank-one completion routine must reject, not assign an SVD-dependent extension.

## Frozen measurements

For every v15.93 row, measure three cyclic pairs: (V01,V12), (V12,V20), (V20,V01), giving108 native matched-pair cases. Measure the one based triple V01*V12*V20 for each row, giving36 compatible paths. Also measure the single v15.83 pair (L,L). Store all factor matrices, raw products, support projectors, spectra/ranks, normal-overlap squared, c, F(AB), F(A)F(B), Frobenius discrepancy and predicted squared discrepancy, plus projector gap and partial-isometry defects. Both factors must have rank2 at all thresholds and A^T A A^T A-A^T A residual<=1e-9 (and similarly B); no silent factor repair.

For rank2 products, compute F only after raw multiplication using its top-two support singular vectors and cofactor. Verify R^TR=I, detR=1, support matching, R^T X symmetric PSD and R(R^T X)=X at tolerance1e-9. Compare product singular values to (1,c,0); compare squared discrepancy to4(1-c) and projector gap squared to2(1-c^2), all at1e-9. Record c^2 before and after scalar roundoff bounding: allow clip to[0,1] only if original lies in[-1e-12,1+1e-12]; outside that range is INVALID. No eigenvalue clipping or product normalization.

For each compatible triple record raw associativity residual and F(V01 V12 V20) versus F(V01)F(V12)F(V20), with all ranks. Triple rank exits are scientific NOs; do not invent full rotations there.

Covariance: use v15.93's exact rational quaternion frames once at each node. For cyclic pair i<-j<-k, transform A'=G_i A G_j^T, B'=G_j B G_k^T and independently recompute its diagnostic. Compare product and completion by endpoint transformation, and scalar discrepancy/projector gap/c^2 by invariance. For L use node0 conjugation for both factors; for the based triple use node0 conjugation. Tolerance1e-9. This changes coordinates only, not support compatibility. Store worst covariance residuals.

## Verdicts and failure classification

Validity requires all pins/verdicts, all36 parent rows and candidate indices [13,16,22,25,27,29,37,39,46,50,66,77] for each lambda, all12 exact checks and3 fixtures, finite data, factor validity, archived R agreement<=1e-9, native squared-loop agreement<=1e-9, raw associativity<=1e-9, all completion/formula/covariance checks<=1e-9. Physical-state and channel certificates are inherited through immutable parents; this gate creates no new density operators or source channels.

Primary ORIENTED_COMPOSITION_OBSTRUCTED iff valid and the native (L,L) product has rank2 at all thresholds and measured completion discrepancy>=1e-6. Otherwise ORIENTED_COMPOSITION_OBSTRUCTION_NOT_CONFIRMED. Secondary MATCHED_SUPPORT_COMPOSITION_CONFIRMED iff valid and all108 planar pairs plus36 triples remain rank2 at all thresholds, all planar pair support gaps<=1e-9, and every pair/triple completion discrepancy<=1e-9. Otherwise MATCHED_SUPPORT_COMPOSITION_NOT_CONFIRMED. INVALID overrides both. Valid scientific NOs must be accepted by tests. An unexpected product rank exit is a scientific NO; a violated algebraic identity or nonphysical archived input certification is INVALID. The rank-one synthetic control is expected and has null completion fields.

## Execution

Publish preregistration, derivation, tests and workflow with gate.py absent; inspect expected GitHub RED and downloaded artifact. Implement only this measurement, run targeted CI, inspect exact scientific JSON/log, verify downloaded source/head/checksum bytes, then publish results with exact provenance. No merge to main or revision of historical verdicts. This tests conditional geometric readout composition, not CPTP/source-update composition, source-law selection, physical recovery or gravity.
