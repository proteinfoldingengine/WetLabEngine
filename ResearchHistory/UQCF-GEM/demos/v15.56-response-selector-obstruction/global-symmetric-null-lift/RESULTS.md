# v15.63 Results — COMPLETE

Date: 2026-09-26.

Verdict: GLOBAL_SYMMETRIC_NULL_LIFT_EXISTS.

The v15.62 polar-symmetric retained-observable null is compatible with the full three-qubit global tangent space.

Across all 12 frozen asymmetric states:

- all 18 single-edge targets per state (3 edges x 6 symmetric directions) were feasible;
- the simultaneous three-edge target delta C_e = O_e I/sqrt(3) was feasible;
- one-body derivatives were constrained to zero;
- reconstructed tangents were Hermitian and trace zero to numerical precision.

For the simultaneous system:
- constraint rank = 36;
- global tangent dimension = 63;
- nullity = 27;
- minimum-norm coefficient norm = sqrt(3/8) = 0.612372435695794...;
- relative feasibility residuals were at floating-point roundoff (~1e-16).

For a single-edge system:
- constraint rank = 18;
- nullity = 45;
- minimum-norm coefficient norm for normalized target directions = 1/sqrt(8) = 0.3535533905932738... .

Thus there is no quantum-marginal linear compatibility obstruction at the tangent level. A nonzero globally valid state tangent can change all three retained edge correlations in polar-symmetric directions while producing zero first-order rotational response.

This strengthens v15.61/v15.62: nonzero hidden leakage can be globally compatible yet rotationally invisible.

Still not established: that such a tangent is realizable as D X_rho[h] for a normalized, covariant, positive finite source update. That source-vector-field realization is the next problem.

Reproducibility:
- branch: research/v15.63-global-symmetric-null-lift
- preregistration: 29b4fbcd1645198cfdad1cffd6426bcab67d2670
- RED run: 36274377319
- implementation: 30d2cce92edfc2b0b4a918437c4bcc375349bcee
- interface-only failed runs documented in GitHub history
- corrected tested head: db87958f1a0d39390d26c47c4495d503e75314a3
- GREEN run: 36274604368
