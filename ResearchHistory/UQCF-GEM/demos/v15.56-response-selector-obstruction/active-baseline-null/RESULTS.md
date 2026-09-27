# v15.77 — Active retained motion still need not produce rotation

Primary verdict: **ACTIVE_RETAINED_BASELINE_COMPOSITION_NULL_CONFIRMED**.

Comparison verdict: **EQUAL_NORM_SKEW_BASELINE_VISIBLE_CONFIRMED**.

The primary null no longer requires a fixed reference center. All twelve separately calibrated active-symmetric channels have nonzero retained baseline action, move their reference states under finite updates, and retain hidden-information leakage, yet their polar rotations remain unchanged through depths 1, 2, 4 and 8. An equal-norm skew baseline produces visible hidden rotational response on every tested reference/depth.

This closes the fixed-point-center limitation of v15.76. It does not remove frozen-reference calibration, and it does not establish a source with nonzero baseline polar action that remains null: the primary baseline acts inside the polar-symmetric sector.

## Frozen results

The experiment evaluated 3,888 finite probe cases and 144 channel/depth rows: 48 fixed controls, 48 active-symmetric cases and 48 equal-norm active-skew cases.

| Quantity | Active symmetric | Equal-norm active skew |
| --- | --- | --- |
| Baseline global/retained norm | approximately 0.0122474487139159 | approximately 0.0122474487139159 |
| Center displacement range | 0.001224744871391584 to 0.006975323636418492 | 0.0012247448713915848 to 0.006975323636418433 |
| Hidden retained norm range | 0.0017320508075688767 to 0.006627476255221528 | same range |
| Maximum Q / retained ratio | 2.220730924145371e-13 | 0.47458695698410064 |
| Maximum E / retained ratio | 1.5098727351433976e-12 | 3.882968148473746 |
| Minimum Q / retained ratio | 8.224662507848095e-16 | 0.03429998082474481 |
| Minimum E / retained ratio | 3.432222581923232e-15 | 0.09148983120466204 |

The active-symmetric ratios stay below the frozen 1e-10 null threshold. Its maximum finite endpoint polar shift from the original reference is 5.863050957829448e-15. The skew comparison exceeds both frozen 1e-6 visibility thresholds on all 48 cases. Its maximum baseline norm mismatch is covered by the 3.2959746043559335e-17 norm-control error, so the contrast is not an amplitude fit.

The fixed-point control also remained null throughout all twelve calibrations and four depths. Its maximum E / retained ratio was 1.5398297718026581e-12.

## Why the center can move without rotation

The new source uses b=rho+deltaY with delta=.02, while retaining the frozen hidden coupling kappa=.01. Its reference vector field is deltaY, not zero. The center after n fixed updates is

rho_n=rho+(1-alpha)deltaY, alpha=(1-s)^n.

Because Y has zero one-body moments and retained pair moments O/sqrt(3), the connected correlations become

C_n=O[P+(1-alpha)delta/sqrt(3) I].

The hidden probe adds another scalar symmetric shift to the positive factor. Thus the state and positive polar factor P move, while O remains fixed. This is rotational invisibility, not absence of all retained observable change or a claim that every notion of geometry is unchanged.

The comparison replaces Y in the baseline displacement by Z of the same HS norm, with one edge's pair derivative sqrt(3)OK. Its baseline Q norm is exactly 2sqrt(3)delta; the measured error against that value was 6.938893903907228e-17. It moves the output polar factor, making the fixed hidden leakage direction visible. This comparison demonstrates the polar-skew distinction for these channels; it is not a universal theorem that all baseline rotational activity forces hidden visibility.

## Numerical and physical validity

All validity gates passed. Every prepared state, finite probe, Phi channel and tested composed channel passed positivity, normalization and trace-preservation checks. The source data were frozen once per reference, with no recalibration during updates.

- Minimum prepared-state eigenvalue: 0.02975064114325797.
- Minimum finite probe eigenvalue: 0.0350990887448251.
- Minimum Choi eigenvalue: 0.0029750641143257415.
- Maximum Choi TP error: 1.2609709600486848e-15.
- Minimum connected-correlation singular value: 0.020860418697313383.
- Recursive versus closed-form power error: 3.6239275968435467e-16.
- Composition identity error: 4.531513127874894e-16.
- Correlation formula error: 2.0408083536618157e-16.
- Independent Q/E formula errors: 3.8460629861821554e-16 and 2.667068294191058e-15.
- Maximum Sylvester residual: 1.5580545255622203e-16.
- Positive-skew observable control Q norm error: 2.6645352591003757e-15; minimum E norm: 5.074483305942512.

No small-step mixed polar finite-difference rank was used. The tiny null residuals are well below frozen tolerances and consistent with the exact polar-factor identity.

## Interpretation boundaries

Nonzero retained baseline action, nonzero hidden leakage, affinity, complete positivity, global state validity and fixed-channel composition remain insufficient to force a pointwise rotational response. The example survives with a moving center. The main source's baseline polar action still vanishes, and all channels remain deliberately calibrated to reference data.

The twelve reference states define twelve distinct source calibrations. This is not one fixed affine law remaining null over an open neighborhood and does not contradict v15.75. Neither does it prove marginal-only naturality or select the physical source-to-consistency law. The original v15.76 b=I/8 negative verdict remains unchanged; adding deltaY defines a new channel, preregistered before this measurement.

The next structural issue is the dependence on calibrated reference data, not whether the retained state can move. These engineered existence results do not derive an interaction from Genesis Pin, gravity, or a change in admissible worlds. Update depth remains ordered source composition, not fundamental time. No heuristic fit, dark-matter primitive, or external alignment is introduced as an explanation.

## Exact execution evidence

Parent certified head: `45cbd56c4833dce1757735fcd175275a0c19780b`.

Preregistration, derivation and tests: `e95206d53feded6674ad0e2cd5601423e5374bd3`.
[Expected RED run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36325844404): job `108638336504`, artifact `10933967573`, SHA-256 `1bee393ebecf2be6565fbb8789b2e675eba359a106c6779be6325f07f966e768`. Setup succeeded, and the sole error was the intended missing-implementation assertion. Downloaded archive digest, execution SHA and frozen source bytes verified.

Tested implementation: `52ae95ec2fe94e89f81b05b16a3ee27828998c7f`.
[GREEN run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36326092787): job `108639023159`, artifact `10933423662`, SHA-256 `3a8028a276252af794431aa43d39c03493bcd6214f7b8e65a9377dc232b461eb`. All three tests passed. The standalone result explicitly records both scientific verdicts above and all_valid=true. Exact job logs were retrieved and inspected. The downloaded artifact digest, execution SHA, source byte identities and all SHA256SUMS entries were verified. Independent read-only review checked the proof and implementation before publication. No implementation repair, state reselection or criterion change occurred.

Raw result SHA-256: `c070efc3cd24a9ff8f7446af33308dd0a4282f0e99f27cc969e62a944b0b826d`.

RESULT.json.gz preserves the exact CI result, including reference lifts, Choi spectra, full Q/E and retained maps, composition diagnostics and finite-domain checks. SUMMARY.json is a readable reduction. EVIDENCE.json records the compressed digest and Git blob; TEST_LOG.txt and SHA256SUMS preserve validation. Decompress with `gzip -dc RESULT.json.gz > result.json` and verify the raw digest.

Reproduce at the tested SHA with Python3.11, numpy2.3.5, OPENBLAS_NUM_THREADS=1 and `.github/workflows/uqcf-active-baseline-null.yml`. Documentation is an additive later commit, identified by its containing Git commit without circular self-hashing. No merge to main.
