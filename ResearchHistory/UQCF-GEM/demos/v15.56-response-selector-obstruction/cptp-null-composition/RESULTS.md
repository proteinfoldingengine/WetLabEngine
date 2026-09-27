# v15.76 — Finite composition separates drift from a stable null

Original v15.75 channel verdict: **FROZEN_CHANNEL_FINITE_NULL_OBSTRUCTED**.

Separate reference-preserving control verdict: **ANCHOR_FIXED_CPTP_COMPOSITION_NULL_CONFIRMED**.

The original channel loses its pointwise rotational null after one finite update. The separately preregistered anchored channel preserves nonzero retained leakage with null rotation through depths 1, 2, 4 and 8. All numerical validity controls passed. The anchored result does not replace or rescue the original channel's negative verdict.

## Original channel: visible already at depth one

The original channel keeps the v15.75 source data fixed: b=I/8, A=XXX, kappa=.01 and the same Y_ref from candidate 13. Each update has source weight s=.1. The measured object is the hidden derivative of the composed channel, evaluated at its output center.

| Depth | Retained norm | Q / retained | E / retained |
| --- | --- | --- | --- |
| 1 | 0.0017320508075688772 | 0.003799397117330254 | 0.025481888315037976 |
| 2 | 0.003117691453623979 | 0.007221083722887538 | 0.053831762222981645 |
| 4 | 0.005050660154870846 | 0.013077042928938283 | 0.1204306211099029 |
| 8 | 0.006627476255221526 | 0.021673529358144757 | 0.3045023848319299 |

Both ratios exceed the frozen 1e-6 visibility threshold at every tested depth. The first tested visible depth is **one**, so the initial failure is finite-strength loss of the null, not a failure first introduced by repetition. At depth one Q norm is 6.58074884534673e-6 and E norm is 4.413592523444146e-5. The finite hidden endpoint polar displacement from its output center is 4.413602248197679e-9, separate from the much larger baseline polar drift of 0.002014934908603451.

The exact retained-correlation formula explains the drift:

C_n=alpha C0+alpha(1-alpha)a_i a_j^T, alpha=(1-s)^n.

The original channel moves the center toward I/8. Its fixed symmetric leakage direction is calibrated to O0, while the output polar factor changes. The complete predicted Q/E response agrees with direct recursive global-channel evaluation within 2.021674357339068e-15, so the visible response is resolved far above numerical residuals. The v15.75 infinitesimal null remains correct; it is a different derivative at a different base point.

## Anchored control: nonzero leakage survives null composition

The matched control changes only the prepared-state center to b=rho0. It is a distinct, globally CPTP measure-and-prepare channel; it was frozen before measurement. Its Y_ref is never recomputed after an update.

It produces the same retained norms in the table above. Across all four depths:

- Maximum Q / retained ratio: 2.2204538443951063e-13.
- Maximum E / retained ratio: 9.868564018281536e-13.
- Maximum center displacement from rho0: 1.3877787807814457e-17.
- Maximum undivided finite endpoint polar displacement from O0: 1.5920046067240293e-15.

These meet the frozen 1e-10 null and finite-polar tolerances with nonzero retained leakage. The analytic formula is

C_n,±=O0 [P0 ± eta beta kappa sqrt(8/3) I], beta=n s (1-s)^(n-1).

The shifted positive polar factor remains positive on every tested probe; O0 is unchanged. This establishes a physical affine channel whose calibrated pointwise null survives the tested finite compositions. The general formula gives the same conclusion whenever the bracket remains positive, without choosing new amplitudes after measurement.

The anchored source has **zero baseline source field at rho0**. Its nontrivial response acts on hidden perturbations. This limitation is part of the construction, not evidence that an active baseline source was tested. It remains calibrated to an explicit reference state and does not establish reference-independent naturality or open-neighborhood nullity.

## Validity and composition checks

All 216 channel/depth/hidden cases passed. The recursive update and closed formula were checked on all 64 complex matrix units. Composition T^n(T^m) was checked for n,m in [1,2,4], including sum depths 3,5,6 as identity controls. This is integer composition of one fixed channel, not additivity of source strength or arbitrary mixing of distinct source laws.

- Phi squared versus replacement channel error: 6.589603847638368e-17.
- Recursive versus closed-form power error: 3.3594539675478776e-16.
- Composition identity error: 3.3594539675478776e-16.
- Retained coefficient formula error: 8.328048306208544e-17.
- Correlation formula error: 2.431168653522475e-16.
- Maximum Sylvester residual: 5.1800756783721856e-20.
- Positive-skew control Q norm error: 2.220446049250313e-15; smallest control E norm: 5.709657331899219.
- Minimum prepared-state eigenvalue: 0.045892049687911274.
- Minimum Choi eigenvalue across both Phi channels and all tested powers: 0.004589204968791062.
- Largest Choi trace-preservation error: 9.155135651400898e-16.
- Minimum finite probe density eigenvalue: 0.04863614328712127.
- Minimum correlation singular value: 0.013987311967654613, above the preregistered 1e-4 finite-output floor.

The original and anchored channels have hidden-to-retained response rank at most one: only XXX can produce retained leakage. The other 26 hidden columns have retained norm at roundoff. This experiment does not increase the dimensionality of retained rotational geometry.

## What this rules out

Complete positivity, affinity, global state validity and repeated composition of a fixed source do not by themselves force a calibrated pointwise leakage direction into the polar-skew sector. Fixing the reference center gives a counterexample. Meanwhile the unmodified original channel's finite null is obstructed and remains recorded as such.

This does not contradict v15.75: the anchored construction is confined to its calibrated reference/fiber, not a full-dimensional open set of states for one fixed law. It also does not establish marginal-only restriction naturality. The next structural bottleneck is dependence on calibrated reference data and the source-selection axiom; composition alone does not settle either.

Both channels are engineered existence controls, not interactions derived from Genesis Pin or recoverability. Ordered source-update depth is not fundamental time. No geometry-dependent construction is being offered as a foundational explanation, and no gravity, dark-matter primitive, external alignment, or change of admissible worlds is claimed. Every historical verdict remains unchanged.

## Exact execution and reproduction

Parent certified head: `07170c00ebb63e17e8be5d6d88f0ba1ca8e42dc7`.

Preregistration, derivation and tests: `6b7f01f17703f50c6af51c1299f04f20a2a58875`.
[Expected RED run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36324772428): job `108635291465`, artifact `10934030429`, SHA-256 `e2bf833a4d4b97494f5e6dfc2ef22963b828488f1b8083d7443455a8ed02aa93`. Setup succeeded; the only failure was the intended missing-implementation assertion. Downloaded archive digest, execution head and frozen file bytes verified.

Tested implementation: `a9a20a6b0771a8101a24ad8de563a8f951945d57`.
[GREEN run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36325015990): job `108636002610`, artifact `10933487379`, SHA-256 `9d3fe59a67a735b04436a85e939ab54ec66160e037041a90901a94a27476425c`. All three tests passed, while the standalone result explicitly recorded the original channel's negative scientific verdict and the control's positive verdict. Green denotes a valid completed adjudication, not a scientific pass for the original channel. Exact logs were retrieved and inspected. Downloaded artifact hash, execution SHA, source byte identities and every SHA256SUMS entry verified. Independent read-only review checked the derivation and code before publication. No implementation repair or threshold change was needed.

Raw result SHA-256: `e6115cad4f550bd3bb213b8d84b01bfa924840cf68ad72caf007fd0ac36d065a`.

RESULT.json.gz preserves the exact CI result, including all response maps, retained maps, centers, Choi spectra and reference lift. SUMMARY.json is a readable reduction. EVIDENCE.json records compressed digest and Git blob; TEST_LOG.txt and SHA256SUMS preserve validation. Decompress with `gzip -dc RESULT.json.gz > result.json` and verify the raw digest.

Reproduce at the tested SHA using Python 3.11, numpy==2.3.5, OPENBLAS_NUM_THREADS=1 and `.github/workflows/uqcf-cptp-null-composition.yml`. Documentation is an additive later commit, identified by its containing Git commit without circular self-hashing. No merge to main.
