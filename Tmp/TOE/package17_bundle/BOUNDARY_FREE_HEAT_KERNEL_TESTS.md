# BOUNDARY_FREE_HEAT_KERNEL_TESTS.md

# Boundary-Free Heat Kernel Tests
## First boundary-free spectral curvature test using flat torus and sphere references

## Status
**Boundary-free diagnostic. Current result weak. Not curvature closure.**

`HEAT_KERNEL_FAILURE_ANALYSIS.md` identified boundary contamination and heat-window instability as major causes of the failed heat coefficient estimator.

This file removes the easiest confounder:

```text
boundary
```

and tests only compact boundaryless geometries:

```text
flat torus
sphere
```

The goal is not to prove curvature convergence. The goal is to check whether a fixed spectral rule gives the expected curvature ordering without per-geometry calibration.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Definition**
- **Observation**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as deriving GR.

---

# 1. Reference targets

## Flat torus

A flat two-torus has:

\[
R=0.
\]

So:

\[
\int R\,dV=0.
\]

## Sphere

A unit two-sphere has:

\[
R=2.
\]

So:

\[
\int R\,dV=8\pi.
\]

Therefore the expected ordering is:

\[
\int R_{\mathrm{sphere}}dV
>
\int R_{\mathrm{flat\ torus}}dV.
\]

---

# 2. First-principles rule

The verifier uses:

```text
intrinsic distances
```

instead of ambient chord distances:

- flat torus: angular product distance;
- sphere: geodesic great-circle distance.

It constructs a graph Laplacian with one fixed rule and estimates the heat coefficient in several fixed \(h^2\)-scaled windows.

The key diagnostic is a plateau-style estimate.

No per-geometry calibration is allowed.

---

# 3. Verifier implementation

## Status
**Implemented as `boundary_free_heat_kernel_tests_verifier.py`. Execution log captured.**

The verifier reports:
- estimated integrated curvature coefficient;
- variance across repetitions;
- heat-window plateau coefficient of variation;
- sphere-vs-torus ordering;
- separation score.

## Captured verifier output

```text
Boundary-free heat-kernel tests verifier
==================================================
Route:
intrinsic distances on flat torus and sphere -> heat coefficient plateau test
No per-geometry calibration.

geometry,intR_coeff_median,intR_coeff_std,window_plateau_cv_median,h_median
flat_torus,-479.08872096067756,7.279410123940157,0.5195571444237038,0.733773190148194
sphere,-462.71443202195746,10.755680347564299,0.521337785407889,0.4086656704737675
sphere_greater_than_flat_torus: True
separation_score: 0.01738610545830482
plateau_stable: True
classification: BOUNDARY_FREE_WEAK
```

---

# 4. Interpretation

The boundary-free test produced the correct ordering:

```text
sphere_greater_than_flat_torus: True
```

but the separation was tiny:

```text
separation_score: 0.0174
classification: BOUNDARY_FREE_WEAK
```

Both coefficients were large and negative:

```text
flat_torus: -479
sphere:     -463
```

That means the estimator is dominated by graph/Laplacian normalization artifacts, not by the scalar curvature coefficient.

Boundary removal helped with plateau stability but did not solve curvature extraction.

---

# 5. What this establishes

### Established

1. Boundary-free geometries can be tested with intrinsic distances.
2. The sphere/torus ordering is weakly correct under this rule.
3. Heat-window plateau stability improved.
4. The coefficient magnitude/sign is still wrong.

### Not established

1. Correct scalar curvature sign.
2. Correct magnitude.
3. Meaningful separation between \(R=0\) and \(R>0\).
4. Heat coefficient convergence.
5. ADM/EH curvature action convergence.

---

# 6. Root cause update

The main remaining issue is likely not boundary.

It is likely:

```text
graph Laplacian normalization / sampling measure / heat coefficient extraction
```

Specifically, the leading graph spectral contribution dominates the \(t\)-coefficient fit, causing large negative offsets for both flat torus and sphere.

---

# 7. Next derivation target

The next file should be:

```text
HEAT_KERNEL_RENORMALIZATION.md
```

Purpose:

Derive a renormalized heat-trace coefficient estimator that subtracts or controls the graph-discretization baseline before interpreting the \(t\)-coefficient as curvature.

The target is not to fit per geometry, but to define a universal baseline correction from the flat reference / graph dimension / sampling density.

---

# Honest status line

> `BOUNDARY_FREE_HEAT_KERNEL_TESTS.md` shows that boundary-free heat-kernel testing improves stability but not curvature extraction. The estimator gives weak ordering but wrong sign/magnitude, indicating that graph Laplacian normalization and baseline renormalization are now the main blockers.

**End of file.**
