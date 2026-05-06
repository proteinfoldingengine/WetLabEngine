# CURVATURE_ROOT_CAUSE_AND_FIRST_PRINCIPLES_NEXT_STEP.md

# Curvature Root Cause and First-Principles Next Step
## Why the current curvature proxy is not enough, and how to proceed without fitting

## Status
**Root-cause analysis and principle-constrained next step. Not a new curvature proof.**

The recent curvature tests produced an important result:

```text
The graph curvature proxy can separate curved from flat reference data,
but it does not show controlled local convergence.
```

That means we should not keep tuning proxies until one looks good.

The next step must be guided by first principles.

---

# 1. Root cause

The current curvature proxy is based on local embedding statistics:

```text
normal variance / tangential variance
```

or related local covariance signals.

This detects **extrinsic curvature-like bending** of an embedded point cloud.

But GR requires **intrinsic scalar curvature** of the spatial metric:

\[
R^{(3)}(h).
\]

Those are not the same object.

## Root cause statement

> The failed proxy is measuring an embedding-dependent curvature signal, not a controlled intrinsic curvature scalar.

That is why it can separate a sphere from a plane, but still fail as a GR curvature estimator.

---

# 2. The key distinction

## Extrinsic curvature-like signal

Depends on how the graph is embedded in an ambient space:

\[
X_i\in\mathbb R^m.
\]

Examples:

```text
normal variance
PCA curvature
surface bending
local covariance anisotropy
```

These may be useful diagnostics, but they are not sufficient for GR.

## Intrinsic curvature

Depends only on the metric structure inside the space:

\[
(\Sigma,h_{ab}).
\]

GR needs:

\[
R^{(3)}(h),
\]

not:

```text
how the point cloud bends in an embedding
```

Therefore, the next estimator must be graph-intrinsic or metric-intrinsic.

---

# 3. Why calibration is dangerous

The failed test could calibrate the median sphere curvature to:

\[
R=2.
\]

But calibration is not convergence.

A fitted global scale can make one geometry look right while still failing on:

```text
flat space
negative curvature
variable curvature
different sampling densities
different graph constructions
different dimensions
```

So the rule is:

```text
No estimator is accepted because it can be calibrated on one geometry.
```

It must pass multiple reference geometries with one fixed rule.

---

# 4. First-principles requirements for the next curvature estimator

The next estimator must satisfy these requirements.

## Requirement 1: intrinsic dependence

The estimator should depend on:

```text
graph distances
edge weights
local volumes
graph Laplacian / heat kernel
cell complex structure
```

not primarily on ambient embedding curvature.

## Requirement 2: correct flat limit

For flat reference geometry:

\[
R=0.
\]

The estimator must approach zero without geometry-specific tuning.

## Requirement 3: sign sensitivity

It must distinguish:

\[
R>0,\qquad R=0,\qquad R<0.
\]

A proxy that only measures “curved vs not curved” is insufficient.

## Requirement 4: refinement stability

As graph density increases:

```text
variance should decrease
median / integrated curvature should stabilize
```

## Requirement 5: integrated action relevance

Eventually we need:

\[
\sum_i \sqrt{h_i}R_i\Delta V_i
\rightarrow
\int_\Sigma \sqrt h R\,d^3x.
\]

So the estimator must support an integrated curvature quantity, not only local scores.

---

# 5. Best first-principles candidate families

## Candidate A: heat-kernel / spectral curvature

This is the strongest first-principles route.

Reason:

The heat kernel encodes intrinsic geometry.

For a smooth \(d\)-dimensional manifold:

\[
\mathrm{Tr}(e^{-t\Delta})
\sim
(4\pi t)^{-d/2}
\left[
\mathrm{Vol}
+
\frac{t}{6}
\int R\,dV
+
O(t^2)
\right].
\]

The scalar curvature appears in the heat-trace expansion.

This is directly tied to intrinsic geometry.

### Why this is preferred

It targets the **integrated scalar curvature** needed by the action:

\[
\int \sqrt h R.
\]

That is closer to ADM/EH convergence than local embedding curvature.

---

## Candidate B: Regge / angle-deficit curvature

If the graph can be converted into a triangulation or cell complex, then curvature can be represented by deficit angles.

Regge calculus approximates GR by assigning curvature to lower-dimensional hinges.

### Why this is strong

It has a known relationship to discrete gravity.

### Why it is harder

It requires a robust simplicial complex:

```text
triangles / tetrahedra / hinges / volumes
```

A raw \(k\)-NN graph is not enough.

---

## Candidate C: Ollivier/Forman Ricci

These are graph-native Ricci-type curvatures.

### Pros

```text
intrinsic to weighted graph
well-studied
no ambient embedding required
```

### Cons

They are Ricci-like edge curvatures, not directly scalar curvature.

They may still be useful, but require an additional trace/integration rule.

---

# 6. Principle-based decision

The next step should not be:

```text
try five estimators and keep the best-looking one
```

The next step should be:

```text
choose the estimator family with the strongest theoretical path to ∫R√h
```

That points to:

```text
heat-kernel / spectral curvature
```

as the next primary route.

Regge curvature should be the second route if we can build a reliable cell complex.

---

# 7. Next file

The next file should be:

```text
HEAT_KERNEL_CURVATURE_ACTION.md
```

Purpose:

Derive the graph spectral/heat-kernel route to integrated scalar curvature:

\[
\mathrm{Tr}(e^{-tL_{\mathcal G}})
\longrightarrow
\int_\Sigma \sqrt h R.
\]

This directly attacks the action-level curvature term.

---

# 8. What the next verifier should do

The verifier should not fit to one target.

It should test:

```text
one fixed estimator rule
one fixed time-window selection rule
multiple reference geometries
no per-geometry calibration
```

Minimum reference geometries:

```text
flat torus / plane patch: R ≈ 0
sphere: R > 0
hyperbolic-like surface / saddle proxy: R < 0 or negative curvature signal
perturbed sphere: variable positive curvature
```

The output should classify:

```text
PASS: correct sign/order across geometries without per-geometry fitting
SOFT_FAIL: separates some cases but unstable
HARD_FAIL: requires per-geometry calibration or wrong sign
```

---

# 9. Stop rules

Stop and reject an estimator if:

1. it requires calibration separately for each geometry;
2. it cannot distinguish flat from curved;
3. it cannot detect sign or integrated curvature ordering;
4. refinement increases instability;
5. it depends mainly on ambient embedding.

---

# 10. Safe claim after this analysis

Safe:

```text
The current covariance curvature proxy is an extrinsic diagnostic, not a controlled intrinsic scalar curvature estimator.
```

Safe:

```text
The next first-principles route is heat-kernel / spectral curvature because scalar curvature appears in the heat-trace expansion.
```

Unsafe:

```text
Graph curvature convergence has been shown.
```

Unsafe:

```text
The current graph curvature proxy supports ADM/EH action convergence.
```

---

# 11. Report-out language

```text
Milestone: curvature seam sharpened.

The current graph curvature proxy detects curved-vs-flat structure, but root cause is clear: it is mostly extrinsic/embedding-based, not a controlled intrinsic scalar curvature.

So we stop fitting proxies.

Next move is first-principles: heat-kernel / spectral curvature, because ∫R√h appears directly in the heat-trace expansion.

No per-geometry calibration. Multiple reference geometries. Falsify first.
```

---

# Honest final status

> `CURVATURE_ROOT_CAUSE_AND_FIRST_PRINCIPLES_NEXT_STEP.md` identifies the root cause of the failed curvature proxy: it measures an embedding-dependent curvature signal rather than intrinsic scalar curvature. The next principled route is heat-kernel/spectral curvature because it connects directly to the integrated scalar curvature term required by the ADM/EH action spine.

**End of file.**
