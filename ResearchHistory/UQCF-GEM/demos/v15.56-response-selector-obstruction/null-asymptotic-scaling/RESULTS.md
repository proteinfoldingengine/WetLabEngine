# v15.65 Result — NOT CONFIRMED

Date: 2026-09-26.

Verdict: NULL_DERIVATIVE_ASYMPTOTICS_NOT_CONFIRMED.

The preregistered O(t^2) collapse did not occur. On the measured ladder the centered mixed-rotation norm generally increased as t decreased, with fitted slopes near -1 rather than +2. The smallest-amplitude residual was roughly 12x–36x larger than the largest-amplitude residual in the shown states.

This does not support the proposed finite-nonlinearity explanation of v15.64.

The observed ~t^-1 behavior is consistent with a t-independent floating-point/cancellation numerator being divided by the 4 eta t denominator once the true analytic signal is below numerical precision. That interpretation is diagnostic, not a rescue of the preregistered claim.

Consequences:
1. v15.64 remains FALSIFIED.
2. v15.65 is a separate NO.
3. The finite-difference polar estimator at eta=1e-4 and t<=1e-3 is numerically incapable of resolving the derivative-null asymptotics.
4. The analytic v15.61 factorization and exact retained-layer/global-lift constructions are not falsified by this numerical-floor behavior, but the finite source-vector realization has not been certified.

The next defensible step is numerical-method adjudication, not another smaller-t run: compute the mixed derivative analytically through the polar/Sylvester derivative or use higher precision, and separately characterize the floating cancellation floor. Thresholds must be frozen from precision/error analysis before any new scientific verdict.

Reproducibility:
- branch: research/v15.65-null-asymptotic-scaling
- preregistration: 208d4201b5d13a87154b65a73f8abc1456336964
- RED run: 36274949577
- tested implementation: ba08188a3ca36b67bb7adb28770764966ba36510
- GREEN run: 36274987681
