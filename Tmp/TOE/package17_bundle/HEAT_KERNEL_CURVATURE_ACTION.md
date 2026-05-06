# HEAT_KERNEL_CURVATURE_ACTION.md

# Heat-Kernel Curvature Action
## First-principles route from graph Laplacian heat trace to integrated scalar curvature

## Status
**Principle-guided curvature route. Diagnostic only. Not curvature closure.**

`CURVATURE_ROOT_CAUSE_AND_FIRST_PRINCIPLES_NEXT_STEP.md` identified the root cause of the failed curvature proxy:

```text
the covariance proxy is embedding/extrinsic, not controlled intrinsic scalar curvature.
```

The next route must be guided by first principles, not by fitting graph curvature proxies.

The heat-kernel route is preferred because scalar curvature appears directly in the continuum heat-trace expansion.

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

# 1. Continuum principle

For a compact \(d\)-dimensional Riemannian manifold with Laplace-Beltrami operator \(\Delta\), the heat trace has the small-\(t\) expansion:

\[
\mathrm{Tr}(e^{-t\Delta})
\sim
(4\pi t)^{-d/2}
\left[
\int_\Sigma dV
+
\frac{t}{6}
\int_\Sigma R\,dV
+
O(t^2)
\right].
\]

The integrated scalar curvature appears as the coefficient of \(t\):

\[
\frac{1}{6}\int_\Sigma R\,dV.
\]

This is directly relevant to the ADM/EH action spine because the spatial curvature action term is:

\[
\int_\Sigma \sqrt h\,R^{(3)}\,d^3x.
\]

---

# 2. Graph target

Given a weighted spatial graph \(\mathcal G\), define a graph Laplacian:

\[
L_{\mathcal G}.
\]

The graph heat trace is:

\[
H_{\mathcal G}(t)
=
\mathrm{Tr}(e^{-tL_{\mathcal G}}).
\]

The desired continuum behavior is:

\[
H_{\mathcal G}(t)
\rightarrow
\mathrm{Tr}(e^{-t\Delta_h})
\]

under graph refinement and metric convergence.

If this holds in a controlled scaling window, then the heat-trace coefficients can recover integrated geometric invariants.

---

# 3. Why this is better than covariance curvature

The covariance proxy estimates a local extrinsic bending signal.

The heat-kernel route depends on:

```text
graph metric
graph Laplacian
diffusion across the intrinsic graph
spectral geometry
```

It is therefore closer to intrinsic geometry and action-level curvature.

---

# 4. No-fitting rule

This route must obey:

```text
one fixed graph Laplacian rule
one fixed heat-time window rule
no per-geometry calibration
multiple reference geometries
```

A method that only works after tuning one scale per geometry is not evidence of curvature convergence.

---

# 5. First verifier

## Status
**Implemented as `heat_kernel_curvature_action_verifier.py`. Execution log captured.**

The verifier constructs a symmetric normalized graph Laplacian on reference geometries:

```text
plane
sphere
saddle
perturbed sphere
```

It computes fixed heat-trace features:

\[
H_{\mathcal G}(t)/n
\]

over a fixed dimensionless \(t\)-grid.

It reports:
- heat-trace slope;
- heat-trace area;
- spectral gap;
- geometry separation scores.

This is a diagnostic only. It does not yet extract \(\int R\,dV\).

## Captured verifier output

```text
Heat-kernel curvature action verifier
==================================================
Route:
fixed graph Laplacian heat trace features across reference geometries
No per-geometry calibration. Diagnostic only.

kind,feature,median,std
plane,slope,-0.917477230789951,0.014509996929947543
plane,area,1.1595218262775306,0.0034834138738444632
plane,gap,0.014963417285163406,0.0030355693709027227
plane,h,0.2209635847840517,0.004340161868091656
sphere,slope,-0.9340730217284623,0.004324642481408334
sphere,area,1.155309049241555,0.0011401757914859284
sphere,gap,0.02607403698775306,0.0035652313821566187
sphere,h,0.3614460130868369,0.006358342242609771
saddle,slope,-0.904251787979384,0.010131653759177024
saddle,area,1.1633561313440706,0.003707587743903384
saddle,gap,0.013420215159195212,0.0034293512437695733
saddle,h,0.24265046671064006,0.006955238292595844
perturbed_sphere,slope,-0.9456449078233156,0.009017186608803164
perturbed_sphere,area,1.1525505314406457,0.0016673871882202753
perturbed_sphere,gap,0.02775709984862873,0.0033848113081596694
perturbed_sphere,h,0.37050621948642815,0.0046296045513222195
separation_sphere_plane_area: 0.0018199070526174663
separation_saddle_plane_area: 0.001650670046593504
area_order: {'plane': np.float64(1.1595218262775306), 'sphere': np.float64(1.155309049241555), 'saddle': np.float64(1.1633561313440706), 'perturbed_sphere': np.float64(1.1525505314406457)}
slope_order: {'plane': np.float64(-0.917477230789951), 'sphere': np.float64(-0.9340730217284623), 'saddle': np.float64(-0.904251787979384), 'perturbed_sphere': np.float64(-0.9456449078233156)}
classification: SPECTRAL_DIAGNOSTIC_WEAK
```

---

# 6. Interpretation

The current verifier asks only:

```text
Do fixed spectral heat-trace features distinguish reference geometries without per-geometry calibration?
```

A positive result means:

```text
spectral route is promising
```

not:

```text
scalar curvature recovered
```

The next step after this file is to derive a graph heat-kernel coefficient estimator with a fixed scaling window.

---

# 7. What must eventually be shown

A real curvature-action result requires:

\[
\widehat{\int R\,dV}_{\mathcal G}
\rightarrow
\int R\,dV.
\]

That requires:

1. graph Laplacian convergence;
2. heat-time scaling window;
3. volume normalization;
4. boundary handling;
5. dimension control;
6. reference-geometry validation;
7. refinement convergence.

---

# 8. Failure conditions

This route fails if:

1. heat-trace features cannot distinguish flat and curved references;
2. results require per-geometry calibration;
3. graph Laplacian choice dominates geometry;
4. refinement does not stabilize;
5. no heat-time window isolates the curvature coefficient.

---

# 9. Next derivation target

The next file should be:

```text
HEAT_TRACE_COEFFICIENT_ESTIMATOR.md
```

Purpose:

Define a fixed-window estimator for the curvature coefficient in:

\[
H(t)\sim (4\pi t)^{-d/2}
\left[
V+\frac{t}{6}\int R\,dV+\cdots
\right].
\]

This is the first route toward the integrated curvature action term.

---

# Honest status line

> `HEAT_KERNEL_CURVATURE_ACTION.md` redirects the curvature seam from extrinsic graph proxies to a first-principles spectral route. The heat trace is relevant because its continuum expansion contains \(\int R\,dV\). The current verifier is only diagnostic and does not yet recover scalar curvature.

**End of file.**
