# v15.91 preregistration — separable-output rotational response

Branch research/v15.91-separable-output-rotation from certified parent 5e4c27c47dbfbc922fdfcf903f0f9dd95d139fdd. Freeze all definitions before implementing gate.py. No random samples, optimizer, fit, finite-difference derivative or revised historical gate.

## Inputs

Use the v15.81 source-component-interference code and its helpers. Pin gate.py SHA-256 eb44b9214844384bb5962e973711bfe31dc3d0038877063540e0b238879236be and RESULT.json.gz SHA-256 6ec462e269a8cfd81b8cbd9312a2b613e8c802434b28dd2b38d3cbce4f37217d, decompressed JSON SHA-256 14d1fdac212d7373bddd3f450269a0c39dd0ae0d7937fa9356fe1acc64c646fc. Require all_valid, primary MATCHED_COMPONENT_INTERFERENCE_RESPONSE_CONFIRMED and historical secondary FINITE_COMPONENT_INTERFERENCE_WINDOW_NOT_CONFIRMED. Preserve that NO.

Frozen states: candidates [13,16,22,25,27,29,37,39,46,50,66,77]. All 27 normalized exact-weight-3 hidden Pauli directions. Source P=ZII,Q=XXI as v15.81, lambda=[-1,0,1], u=0.1, hidden finite probes rho +/- eta h with eta=1e-4. This new postprocessing test fixes u=0.1; it does not rerun or rescue the previously failed full finite window through u=0.8.

Attenuations a=[1,1/3,1/6,0]. Cases: 12 states x3 source arms x4 attenuations=144; 108 regular a>0 cases, 36 zero-attenuation controls. Use Python3.11, numpy2.3.5, sympy1.13.3, mpmath1.3.0. Measurements are float64 with complex matrices; exact certificates use SymPy. No small-step cancellation quotient.

## Nineteen new exact checks

For symbolic real a, six effects Pi/3 and six prepared tau from DERIVATION: four matrix-unit channel identities, one POVM sum, six prepared traces, six prepared determinants det(tau)=(1-9a^2)/4. Positivity on a in [0,1/3] follows from trace/determinant and Hermiticity; certify numerically at every EB attenuation. Add two generic symbolic identities for C'=a^2 C and delta C'=a^2 delta C, with independent one-body, pair, and tangent variables. Total 19 checks.

## Measurements and controls

Implement D_a^tensor3 independently via full 64-dimensional normalized Pauli expansion with multiplier a^weight. Construct the 216 product POVM effects/preparations at a=1/3,1/6,0. Check all tensor effects sum to I; all prepared product states are positive normalized; compare measure-and-prepare action to the Pauli channel on all 64 global matrix units, and on all finite centers and source-hidden tangents. Record preparation probabilities and their minimum across centers and +/-eta hidden probes, probability sums, tangent sums, and reconstruction errors. Certify the source and all 12 composite channels CPTP by full Choi diagnostics. Output separability is certified by the explicit decomposition, not a PPT surrogate.

For all states/source arms, compute source center=S(rho), source tangents=S(h), source C,O,P,Q,E. Check the u=0.1 parent norms/singular values/ranks against the archived matching row. For each a>0 compute attenuated center/tangents and independently extract C,O,Q,E. Record matrices Q,E, their singular values, norms, threshold ranks and per-edge ranks. Measure normalized residuals C_a/a^2-C, Q_a/a^2-Q and E_a-E against the corresponding nonzero lambda=+1 reference norm at the same state; the lambda=0 arm uses those same scales, never divides by its own null norm. O residual is absolute Frobenius. Compute one-body/pair moment scaling for center and tangents and the Sylvester residual. Frozen rank thresholds [1e-9,1e-10,1e-11] use a^2 times the lambda=+1 Q leading singular value for Q, and the unattenuated lambda=+1 E leading singular value for E.

Source centers must have proper polar determinant and minimum edge singular value>=1e-4. At a>0 the floor is a^2*1e-4, from the exact scaling law; record the unscaled minimum too. This scale-covariant domain criterion is frozen before measurements. A domain exit is a scientific NO with Q/E null fields, not INVALID or forced reflection correction. Check physicality of all source/output centers and +/-eta tangents. At a=0 require center I/8, all hidden output tangents zero and all connected correlations zero within 1e-12. Record geometry_status=UNDEFINED_ZERO_CORRELATION and Q=E=null; do not invoke polar extraction there.

## Adjudication

Validity requires parent hashes/verdicts/indices, 19 exact checks, finite data, source/composite CPTP, input/source/output physicality, normalized positive preparations, effect completeness and all probability conditions. Choi/state/preparation eigenvalues >=-1e-12; trace/Hermiticity/TP/probability/tangent-sum errors <=1e-12. Matrix-unit and center/tangent reconstruction errors, one/pair scaling residuals <=1e-12. Parent metric matching <=1e-9 relative with denominator max(1, archived norm/leading value). Sylvester residual <=1e-10. Failure of these validity controls gives INVALID.

Primary SEPARABLE_OUTPUT_ROTATIONAL_RESPONSE_CONFIRMED iff valid, all 108 positive-a cases remain in their frozen proper-polar domains, and: C/Q/E scaling relative errors <=1e-9; polar-factor error <=1e-9; lambda=+/-1 Q and E rank6 at all three thresholds with edges (1,2),(2,0) rank3 each and edge(0,1) norm<=1e-10 times the full matching positive-reference scale; lambda=0 Q/E rank0 and relative norms<=1e-10. Baseline positive-arm E norms must exceed 1e-6. Otherwise SEPARABLE_OUTPUT_ROTATIONAL_RESPONSE_NOT_CONFIRMED. This verdict concerns fully separable outputs at a=1/3,1/6, with a=1 as unprocessed reference.

Secondary ZERO_ATTENUATION_POLAR_UNDEFINED_CONFIRMED iff valid and all 36 a=0 cases obey the frozen maximally-mixed/tangent/correlation controls and null geometry fields. Otherwise ZERO_ATTENUATION_POLAR_UNDEFINED_NOT_CONFIRMED. INVALID overrides both. Valid scientific NOs remain NO and are accepted by tests.

## Execution

Publish documents, tests and targeted workflow with implementation absent, inspect GitHub expected RED and downloaded artifact, then implement only this measurement. Inspect GREEN logs, scientific JSON, artifact digest, execution SHA and source bytes. Publish exact results and provenance, retaining every historical verdict and all scope boundaries in DERIVATION. No merge to main.
