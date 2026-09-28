# v15.91 — fully separable outputs retain the rotational-response signal

The frozen gate returned **SEPARABLE_OUTPUT_ROTATIONAL_RESPONSE_CONFIRMED** and **ZERO_ATTENUATION_POLAR_UNDEFINED_CONFIRMED**, with `all_valid: true`. All three tests, 19 exact symbolic checks and 144 state/source/attenuation cases passed. No implementation repair or criterion change was needed.

The earned conclusion is specific: **the retained polar rotational response does not, by itself, witness surviving output entanglement**. The same coherent hidden-to-rotation maps can occur after a CPTP update whose outputs are fully separable among the three sites and disentangled from any external reference.

## Exact mechanism

Postcompose the frozen v15.81 source channel with independent isotropic depolarization on each qubit,

    D_a(z)=a z+(1-a)Tr(z)I/2.

For any normalized state and trace-zero tangent, one-body moments scale by a and two-body moments by a^2. Connected correlations and their complete derivatives therefore scale together:

    C_a=a^2 C, delta C_a=a^2 delta C.

On the regular polar domain, this implies O_a=O, P_a=a^2 P, Q_a=a^2 Q and E_a=E. The invariant E follows from the skew Sylvester equation. It does not follow from renormalizing measured response matrices after the fact: the code independently extracts E from each attenuated state and tangent. [DERIVATION.md](DERIVATION.md) gives the argument.

For 0<=a<=1/3, the local channel has six effects E_(k,s)=(I+s sigma_k)/6 and preparations tau_(k,s)=(I+3a s sigma_k)/2. Tensoring this representation gives 216 positive product preparations with nonnegative normalized weights. Thus every output of the three-site channel is fully separable. Measure-and-prepare structure also proves entanglement breaking across the total-output/reference partition. These are constructive separability certificates, not inferences from a numerical PPT test.

The depolarizing postprocessing D_a^tensor3 commutes with independent local unitary frames. This is not a claim that the full composite with fixed source tensors commutes with every frame change. Pauli coordinates provide one implementation of the isotropic postprocessing; they do not select a physical preferred frame or insert an alignment mechanism.

## Frozen scientific outcomes

All 12 asymmetric states and all 27 exact-weight-three hidden tangents were retained. Source arms lambda=-1,0,+1 used the already specified v15.81 component law at ordered strength u=0.1. Attenuations were a=1,1/3,1/6,0.

All 108 positive-attenuation cases remained in the preregistered proper-polar domain. The 72 coherent cases had Q and E rank 6 at all three frozen relative thresholds. This includes **48 coherent cases with certified fully separable outputs**, at a=1/3 and a=1/6. Each responsive edge, (1,2) and (2,0), retained rank 3; source edge (0,1) remained null. All 36 positive-attenuation incoherent cases retained Q/E rank 0.

| Attenuation a | Fully separable output certificate | Coherent Q norm | Coherent E norm range | Minimum edge singular value |
|---|---|---:|---:|---:|
| 1 | Not asserted by this certificate | 1.025413710 | 4.537666617–7.005278868 | 0.0189437680 |
| 1/3 | Yes | 0.113934857 | 4.537666617–7.005278868 | 0.00210486311 |
| 1/6 | Yes | 0.0284837142 | 4.537666617–7.005278868 | 0.000526215778 |
| 0 | Yes | Geometry undefined | Geometry undefined | Numerical zero |

Q and raw correlations shrink by factors of 9 and 36 while E is invariant. Largest relative C scaling error was 1.242e-14, Q scaling error 7.888e-15, and E invariance error 1.578e-14; largest absolute polar-factor discrepancy was 2.281e-14 (rounded upward). These are far below the frozen 1e-9 geometry tolerances.

All 36 complete-depolarization cases produced I/8, zero hidden output tangents and zero connected correlations within a maximum residual of 1.571e-16. Their status is `UNDEFINED_ZERO_CORRELATION`; Q/E and their maps are null fields. No polar routine was called at a=0. The limiting loss of a defined polar geometry is not reported as rotational rank zero.

## Independent validity evidence

The 19 exact checks cover four single-site matrix-unit measure-and-prepare identities, effect completeness, six prepared traces, six prepared determinants, and connected-correlation/tangent scaling. Positivity for 0<=a<=1/3 follows analytically from the prepared spectra. The numerical implementation independently compared the 216-term construction against the full 64-dimensional Pauli channel on every global matrix unit, center and source tangent.

Maximum matrix-unit reconstruction error was 1.666e-16; center/tangent reconstruction error was 1.666e-16. Minimum preparation probability across all source centers and finite hidden probes was 0.0026013646. Probability normalization error was at most 3.331e-16, and imaginary probability residual at most 4.377e-19. The full source channels and all 12 composite channels passed CPTP checks.

All original inputs and source/output finite probes passed positivity, trace and Hermiticity controls. Minimum original input eigenvalue was 0.0383162; minimum across the source/output controls was 0.0418252. The most negative composite Choi eigenvalue, -1.797e-15, and prepared-product eigenvalue, -1.813e-16, were roundoff inside the frozen -1e-12 allowance. Maximum Sylvester residual was 7.003e-16. Parent metrics matched within 2.367e-15 and all archived rank labels matched.

## What this does and does not establish

Output entanglement is unnecessary for this particular rotational-response observable. A nonzero E can survive through a channel with an explicit classical measurement-record/product-preparation description of its output. This strengthens the need to distinguish the geometry statistic from a witness of quantum resources.

The source can still require global/nonlocal access: composing its adjoint with the product POVM need not give local measurement effects. The result does not establish that every intermediate state is separable, that the original quantum consistency mechanism is classical, or that quantum source selection is unnecessary. It also does not claim that the unprocessed a=1 states were entangled; that was not measured or needed.

Correlation amplitudes and Q are reduced even though polar E is unchanged. Consequently this is not a claim of unchanged measurement sensitivity, sample complexity or detectability at fixed noise. For arbitrarily small positive a the analytic invariance holds on a nonsingular domain, but conditioning deteriorates and a=0 has undefined geometry.

The composite family D_a^tensor3 composed with S_(lambda,u) is CPTP. For a<1 it is not identity-anchored at u=0 and has no claimed source-strength semigroup law. This test supplies a postprocessing counterexample to output-entanglement necessity; it does not replace the original source-vector-field problem or select a source-to-admissible-world law.

The v15.81 historical verdict **FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED** remains unchanged, including its candidate-46 orientation exit at u=0.8. This gate chose u=0.1 before implementation for a different question. It neither changes that old window nor repairs its NO by excluding the failed endpoint.

Entanglement-breaking qubit channels and measure-and-prepare structure are established theory; see [Ruskai (2003)](https://arxiv.org/abs/quant-ph/0302032). No novelty or priority claim is made for those ingredients. The program-specific result is their certified application to the native polar-skew response. No gravity law is derived. Genesis Pin, time as pruning/ordered recoverability, and geometry as retained exhaust remain intact; no foundational fit, external alignment trick, or dark-matter primitive was introduced.

## Exact provenance and reproduction

- Branch: `research/v15.91-separable-output-rotation`.
- Certified parent: `5e4c27c47dbfbc922fdfcf903f0f9dd95d139fdd`.
- Preregistration/tests: `54e9dfc47143407028fb77465fe00ac01559a400`.
- Expected RED: [run 36360938558](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36360938558), job `108737869563`, artifact `10945457367`. Setup passed; the explicit absent-implementation assertion failed.
- RED ZIP SHA-256: `1c47bfa957684bced7e1ef28438f0bb7247a886bc807895810409a1f5de2f5a2`.
- Tested implementation: `8ee6415db853196e5ea0867c2ec13dafa5d37f6d`.
- GREEN: [run 36361210766](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36361210766), job `108738641813`, [artifact 10945577420](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36361210766/artifacts/10945577420).
- GREEN ZIP SHA-256: `1fa8578b3a08d1f7b346a044ee85c0e4e36f32cae0624aa632e366fc3a260a24`.
- Full result JSON SHA-256: `9c848c70134adbb62e70c988dc35001834bccf3c78a0539b294e6ce60167bca9`.
- Lossless [RESULT.json.gz](RESULT.json.gz) SHA-256: `1e38de1e7e1474e4d14546f722c3ab5013bf347fb02f72ab91bb43115a6da984`.
- Compressed result Git blob: `c9320f49d517a9ba9e8ca8f267a6c56a9d1f5de5` (291,139 bytes).

Exact job logs and both downloaded artifacts were inspected. ZIP digests, execution heads, frozen documents/tests and implementation bytes were verified, as were all GREEN SHA256SUMS entries. The scientific JSON extracted from the log matched the artifact byte-for-byte after removing GitHub timestamp/BOM chunk headers. This log-transport normalization did not alter the artifact or any scientific value. The lossless gzip and its Git blob were independently checked. [SUMMARY.json](SUMMARY.json) is derived from the full result; [EVIDENCE.json](EVIDENCE.json) records provenance. TEST_LOG.txt and SHA256SUMS are copied from the artifact.

Use the pinned dependencies in the workflow and run from this folder at the tested commit:

```sh
OPENBLAS_NUM_THREADS=1 python -m unittest -v test_gate
OPENBLAS_NUM_THREADS=1 python gate.py > result.json
```

At the documentation head, decompress the published result:

```sh
gzip -dc RESULT.json.gz > certified-result.json
sha256sum certified-result.json
```

The documentation commit is additive and changes no tested scientific code. Nothing was merged to main.
