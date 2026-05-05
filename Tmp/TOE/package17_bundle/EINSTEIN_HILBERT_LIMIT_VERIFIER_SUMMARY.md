# EINSTEIN_HILBERT_LIMIT_VERIFIER_SUMMARY.md

# Verifier Summary
## Discrete curvature-density action convergence

## Status
**Executed structural verifier. Not a full Einstein-Hilbert proof.**

Verifier file:

```text
einstein_hilbert_limit_verifier.py
```

Execution log:

```text
einstein_hilbert_limit_verifier_run.log
```

## Captured output

```text
Einstein-Hilbert limit verifier
==================================================
Controlled 2D conformal metric:
g_ij = exp(2 phi) delta_ij
EH-like density sqrt(g) R = -2 Laplacian(phi)
Also testing absolute curvature and R^2 convergence diagnostics.

Refinement test:
abs_rel_err_n24: 0.04182948800486294
R2_rel_err_n24: 0.0819092699429803
abs_rel_err_n32: 0.02372177815344278
R2_rel_err_n32: 0.046880833548126485
abs_rel_err_n48: 0.010604669080448383
R2_rel_err_n48: 0.021096879154595353
abs_rel_err_n64: 0.005977318990046603
R2_rel_err_n64: 0.011918909637783467
abs_rel_err_n96: 0.0026604645387316187
R2_rel_err_n96: 0.00531385100591137
abs_rel_err_n128: 0.0014972756952113002
R2_rel_err_n128: 0.0029923095559142594
abs_rel_err_n192: 0.000665698648422814
R2_rel_err_n192: 0.0013309541421699757

Sweep results:
PASS: 32.0
SOFT_FAIL: 68.0
HARD_FAIL: 0.0
abs_rel_error_median: 0.16094912435528386
R2_rel_error_median: 0.31714743261194456
abs_rel_error_max: 136.1921922995654
R2_rel_error_max: 19415.407858336555
```

## Interpretation

The verifier tests discrete curvature-density convergence in a controlled 2D conformal metric.

Because the raw 2D periodic Einstein-Hilbert-like integral is topological / boundary-sensitive, the verifier also tracks:

\[
\int\sqrt{g}|R|,
\]

and:

\[
\int\sqrt{g}R^2.
\]

The refinement test shows convergence in smooth noiseless settings.

The noisy/under-resolved sweep mostly soft-fails, which is an important warning: action convergence requires controlled curvature resolution.

This does not prove:
- 4D Lorentzian Einstein-Hilbert convergence,
- Regge or causal-set action convergence,
- Newton constant normalization,
- boundary terms,
- or field equations.

**End of summary.**
