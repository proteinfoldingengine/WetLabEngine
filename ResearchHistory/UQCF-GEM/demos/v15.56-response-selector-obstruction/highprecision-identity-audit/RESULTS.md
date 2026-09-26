# v15.67 Result — STATE_MISMATCH

Date: 2026-09-26.

Verdict: STATE_MISMATCH.

The first semantic divergence between the float64 and v15.66 80-digit paths occurs before any moment, connected-correlation, Gram, or polar computation.

Frozen candidate 13, eta=1e-4, t=1e-3:
- float state maximum imaginary entry: 0.021549503437634027;
- max absolute float-vs-mpmath state difference: 0.021549503437634027;
- traces agree because the discarded imaginary entries are off-diagonal;
- one-body expectation disagreement: 0.04501706190875484;
- two-body disagreement: 0.10652061275156993;
- connected-correlation disagreement: 0.10673993699504462.

Cause:
v15.66's mpmat converter used only A[i,j].real, discarding the imaginary part of complex Hermitian density matrices, hidden tangents, source tangents, and Pauli-Y observables.

Therefore the O(1) "high precision" mixed response in v15.66 is invalid evidence about the analytic derivative. It was computed on a different, real-projected state/operator problem.

The audit stopped scientifically at STATE_MISMATCH as preregistered. Downstream differences are consequences, not independent findings.

Next:
repair only complex-number transport in the high-precision path, verify frozen-corner identity, then rerun the full v15.66 adjudication without changing amplitudes or numerical verdict thresholds.

Reproducibility:
- branch: research/v15.67-highprecision-identity-audit
- preregistration: fde83e9a1646a829ceb33f07c1aac60587d03e1f
- RED run: 36275861647
- first audit implementation: 3c6130cb1c194270a2ba8d67bbe15c1caa48ba82
- trace-helper-only repair: d92b2e15c17470da30578928938b4c6f3b193437
- successful audit run: 36275968542
