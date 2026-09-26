# v15.64 Result — FALSIFIED AS PREREGISTERED

Date: 2026-09-26.

Verdict: SOURCE_VECTOR_FIELD_NULL_FALSIFIED.

This is a scientific failure of the preregistered finite-strength null criterion, not an infrastructure failure.

What passed:
- the frozen XXX hidden tangent has zero proper retained marginals;
- the v15.63 global symmetric-null lift exists;
- the explicit local vector field satisfies D X_rho[h] = Y_rho analytically/by construction;
- finite affine source updates remained normalized and positive at the frozen amplitudes.

What failed:
- the direct four-corner mixed polar-rotation response did not remain effective-rank zero under the frozen finite source amplitudes and parent-scaled rank thresholds.

Interpretation:
v15.61 is a derivative theorem at source amplitude t=0. The affine state update is linear in t, but the polar-rotation observable is nonlinear. Even when the first mixed derivative is exactly in the polar-symmetric null, a centered finite-t estimator generically contains higher-order polar terms (leading even-source correction O(t^2) for the centered derivative). The v15.64 preregistration deliberately required the finite estimator itself to be numerically rank zero at t up to 1e-3. That stronger statement is not implied by v15.61 and is falsified here.

No threshold or amplitude is changed after the result.

Therefore:
- v15.61–v15.63 remain local derivative/tangent results;
- v15.64 does NOT earn a finite-strength source-law null;
- hidden access plus global tangent compatibility plus local positivity is insufficient to guarantee a finite-amplitude null of the nonlinear polar observable.

The next legitimate test is not to rerun v15.64 with smaller amplitudes and call it a pass. It is to preregister an asymptotic scaling test of the residual versus t. The derivative theorem predicts the centered mixed-rotation residue should vanish toward zero with the appropriate even-power scaling as t -> 0. That is a different claim and must be tested separately.

Reproducibility:
- branch: research/v15.64-source-vector-field-null
- preregistration: c1ed5dae252cd0235b04fde8964a6c19575c7a4b
- RED run: 36274709255
- tested implementation: fa07205e2aa79fb1126f56258b285e5f7368b0e7
- GREEN/falsification run: 36274816043
- failed evidence artifact: 10916916220
- artifact SHA-256: b55f8d05dc8c3f64e6d45b45a6cc0ba7b9da4577e8316e8bf18cc411a51fbc19
