# v15.68 Complex high-precision repair — COMPLETE

Date: 2026-09-26.

## Verdict

\`NUMERICAL_CANCELLATION_CONFIRMED\`.

The v15.67 state-layer defect was repaired by preserving complex matrix entries in the 80-digit path. No scientific state, amplitude, target, polar formula, or adjudication threshold was changed.

## Frozen-corner identity gate

Candidate 13, eta=1e-4, t=1e-3:

- state max-entry difference: **1.3877787807814457e-17**
- one-/two-body moment max difference: **4.85722573273506e-17**
- connected-correlation max difference: **4.85722573273506e-17**
- polar-factor Frobenius difference: **6.920916227142602e-16**

The repaired high-precision path therefore reproduces the float64-defined finite corner before the polar derivative comparison.

## Full 12-state adjudication

All 12 frozen asymmetric states passed the original v15.66 criteria.

Across the ensemble:

- maximum analytic O-frame skew projection: **2.309601941963082e-16**
- float64 raw four-corner numerator tail-floor factor: **1.0544008571333747–1.8027756377319946**
- corrected 80-digit mixed norm at t=3e-5: **1.6574274187172809e-15–2.7859932537090195e-14**
- float64 / 80-digit mixed-norm ratio at t=3e-5: **8.742489587491449e6–1.445192993774026e8**

Thus the float64 estimator's apparent growth at small t is caused by a nearly t-independent ~machine-precision numerator divided by 4 eta t.

The corrected high-precision result is consistent with the analytic v15.61 symmetric-null derivative.

## Impact on earlier stages

Historical verdicts are not rewritten:

- v15.64 remains **SOURCE_VECTOR_FIELD_NULL_FALSIFIED** under its preregistered float64 finite-rank gate.
- v15.65 remains **NULL_DERIVATIVE_ASYMPTOTICS_NOT_CONFIRMED** under its preregistered float64 scaling gate.
- v15.66 remains **ANALYTIC_NUMERIC_DISAGREEMENT** because its high-precision implementation discarded imaginary components.

v15.67 identified why v15.66 was invalid as a high-precision scientific comparison.

v15.68 now establishes that, after complex-transport repair, the high-precision finite estimator is numerically consistent with the analytic null and that the float64 small-step signal is cancellation noise.

## Scientific statement now earned

For the explicit base-point-local source vector field of v15.64, the symmetric-null construction has:

- a genuine hidden coordinate;
- a globally valid Hermitian trace-zero lift;
- locally positive and normalized finite source states;
- nonzero retained correlation leakage;
- zero analytic polar-skew mixed derivative;
- corrected 80-digit finite mixed polar response at only ~1e-15 to 1e-14.

Therefore the earlier float64 nonzero mixed-rank observation is not evidence of a physical rotational response.

This supports the v15.61 classification:

\[
\text{retained hidden leakage alone does not force rotational geometry response;}
\]

the rank-producing object is the **polar-skew observable component** of that leakage.

## Reproducibility

- branch: \`research/v15.68-complex-highprecision-repair\`
- preregistration: \`3be967945138505cfe6bf072e385eb9784dad0eb\`
- RED run: \`36276035006\`
- tested implementation: \`d40ea79f11cb20e431dfb669640e8504967efb46\`
- GREEN run: \`36276091968\`, job \`108499013372\`
- artifact: \`10917198122\`
- artifact ZIP SHA-256: \`e31c84c51ac193355aa5b10ef39ef9dec568b4cccc1494c8a8f82de94ff0fe40\`

## Next scientific bottleneck

The existence counterexample is intentionally base-point-local and non-covariant. The next useful discriminator is not another numerical null test.

The remaining source-law question is whether the symmetric-null mechanism survives stronger admissibility axioms such as:

1. local-frame covariance;
2. source neutrality;
3. composition/consistency across retained atlas charts;
4. positivity beyond a local affine neighborhood.

That is where a physically meaningful source-law classification must now proceed.
