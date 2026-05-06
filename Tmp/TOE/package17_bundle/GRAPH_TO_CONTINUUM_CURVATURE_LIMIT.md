# GRAPH_TO_CONTINUUM_CURVATURE_LIMIT.md

# Graph-To-Continuum Curvature Limit
## First refinement test for \(R_{\mathrm{graph}}^{(3)}\rightarrow R^{(3)}\)

## Status
**Geometric convergence target. Current proxy not stable enough. Not a proof of continuum curvature.**

`GEOMETRIC_GR_OBLIGATIONS_REFOCUS.md` identified the highest-value next GR seam:

\[
R_{\mathrm{graph}}^{(3)}
\longrightarrow
R^{(3)}.
\]

The ADM/EH action convergence cannot be claimed until the graph curvature proxy has a controlled continuum limit.

This file defines the first focused curvature-limit target and a refinement-style verifier.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Lemma candidate**
- **Theorem candidate**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving GR.

---

# 1. Why this seam matters

The current proxy action has the form:

\[
S_{\mathrm{proxy}}
=
\sum_k
N_k\sqrt{\det h_k}
\left[
R_{\mathrm{graph},k}^{(3)}
+
K_{ab}K^{ab}
-
K^2
\right]\Delta k.
\]

To approach ADM gravity, the spatial curvature term must satisfy:

\[
R_{\mathrm{graph}}^{(3)}
\rightarrow
R^{(3)}.
\]

Without this, the action cannot be honestly identified with:

\[
S_{\mathrm{ADM}}.
\]

---

# 2. Continuum target

For a smooth spatial slice \((\Sigma,h_{ab})\), the continuum scalar curvature is:

\[
R^{(3)}(h).
\]

A graph curvature estimator is acceptable only if, under refinement:

\[
\mathcal G_n\rightarrow \Sigma,
\]

\[
h_{\mathcal G_n}\rightarrow h,
\]

and:

\[
R_{\mathrm{graph},n}^{(3)}
\rightarrow
R^{(3)}
\]

in a controlled sense.

---

# 3. Required convergence modes

## Definition 1
Pointwise convergence:

\[
R_{\mathrm{graph},n}^{(3)}(i)
\rightarrow
R^{(3)}(x_i).
\]

## Definition 2
Integrated convergence:

\[
\sum_i
\sqrt{h_i}
R_{\mathrm{graph},n}^{(3)}(i)
\Delta V_i
\rightarrow
\int_\Sigma
\sqrt{h}R^{(3)}d^3x.
\]

## Definition 3
Action-level convergence:

\[
\sum_k
N_k\sqrt{h_k}
R_{\mathrm{graph},k}^{(3)}
\Delta k
\rightarrow
\int
N\sqrt{h}R^{(3)}dt\,d^3x.
\]

The GR program ultimately needs action-level convergence.

---

# 4. First refinement diagnostic

## Definition 4
Use a known smooth reference geometry.

The verifier uses a sampled unit sphere as a curvature-controlled test surface.

For the unit two-sphere:

\[
R^{(2)}=2.
\]

This is not the full \(3\)-dimensional target, but it is a clean curvature-refinement diagnostic: if the graph curvature estimator cannot stabilize on a known smooth manifold, it cannot support the GR curvature seam.

---

# 5. Verifier implementation

## Status
**Implemented as `graph_to_continuum_curvature_limit_verifier.py`. Execution log captured.**

The verifier:

1. samples points on a unit sphere;
2. builds a \(k\)-nearest-neighbor graph;
3. computes a local curvature signal from neighborhood covariance;
4. performs refinement over increasing sample sizes;
5. measures calibrated curvature stability and coefficient of variation.

## Captured verifier output

```text
Graph-to-continuum curvature limit verifier
==================================================
Route:
unit sphere sampled graph -> curvature proxy -> refinement stability
Diagnostic only; not proof of continuum curvature convergence.

n,h_median,R_est_calibrated,relative_error,coefficient_of_variation
100,0.4582525618,2.06704192,0.03352096014,0.4187500702
200,0.3196813085,2.051256935,0.02562846728,0.4318102635
400,0.2268022303,2.037673402,0.01883670079,0.4158925157
800,0.1607363148,2,0,0.4358697484
stability_class: PROXY_NOT_STABLE
cv_improvement_factor: 0.960723
```

---

# 6. Interpretation

The calibrated median curvature approaches the unit-sphere target after normalization:

\[
R\approx2.
\]

However, the coefficient of variation does **not** improve under refinement:

```text
cv_improvement_factor: 0.960723
stability_class: PROXY_NOT_STABLE
```

This means the current curvature proxy is not stable enough to support the GR seam.

This is a useful negative result.

The proxy can be calibrated to the right scale, but it does not yet show controlled local convergence.

---

# 7. What this establishes

### Established

1. A reference-geometry curvature refinement test exists.
2. The current proxy can be globally calibrated on a unit sphere.
3. The current local curvature signal does not improve enough under refinement.
4. The curvature seam remains open.

### Not established

1. \(R_{\mathrm{graph}}^{(3)}\rightarrow R^{(3)}\).
2. Integrated curvature convergence.
3. Action-level curvature convergence.
4. Robustness under irregular antichain graphs.
5. A coordinate-free intrinsic graph curvature theorem.

---

# 8. Failure conditions triggered

The current proxy triggers this failure condition:

```text
coefficient of variation does not decrease with refinement
```

Therefore the current estimator should not be used as evidence for continuum curvature convergence.

---

# 9. Next derivation target

The next file should be:

```text
CURVATURE_ESTIMATOR_FAILURE_ANALYSIS.md
```

Its job:

- diagnose why the local covariance curvature proxy fails;
- compare candidate graph curvature estimators:
  - Ollivier-Ricci;
  - Forman-Ricci;
  - angle-deficit / triangulated curvature;
  - heat-kernel curvature;
  - spectral/Laplacian curvature;
- select a better estimator for `CURVATURE_REFERENCE_GEOMETRY_TESTS.md`.

---

# Honest status line

> `GRAPH_TO_CONTINUUM_CURVATURE_LIMIT.md` begins the curvature-convergence seam and finds that the current graph curvature proxy is not refinement-stable enough. This is a useful negative result: the GR action-convergence branch requires a stronger intrinsic curvature estimator.

**End of file.**
