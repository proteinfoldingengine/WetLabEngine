# CURVATURE_ESTIMATOR_FAILURE_ANALYSIS.md

# Curvature Estimator Failure Analysis
## Diagnosing why the current graph curvature proxy failed refinement stability

## Status
**Failure analysis. Not a new curvature proof.**

`GRAPH_TO_CONTINUUM_CURVATURE_LIMIT.md` tested the current local covariance curvature proxy on a unit-sphere refinement sequence and found:

```text
stability_class: PROXY_NOT_STABLE
cv_improvement_factor: 0.960723
```

The calibrated median curvature could be matched to the sphere target, but local variability did not decrease with refinement.

This file diagnoses that failure and compares candidate estimator families.

---

## Tagging rule

Every item in this file is labeled as one of:

- **Observation**
- **Definition**
- **Failure condition**
- **Derivation target**
- **Closure status**

Nothing here should be interpreted as proving curvature convergence.

---

# 1. Failure diagnosis

The failed proxy was based on local neighborhood covariance:

\[
\text{normal variance} / \text{tangential variance}.
\]

This is sensitive to:

1. random sampling anisotropy;
2. \(k\)-nearest-neighbor graph construction;
3. embedding noise;
4. local density fluctuations;
5. calibration choice.

It measures a curvature-like signal, but not a stable intrinsic curvature.

---

# 2. Why this matters

The GR action branch requires:

\[
R_{\mathrm{graph}}^{(3)}
\rightarrow
R^{(3)}.
\]

A curvature proxy that only calibrates globally but does not stabilize locally cannot support:

\[
S_{\mathrm{proxy}}\rightarrow S_{\mathrm{ADM}}.
\]

Therefore this failure is a blocker for ADM/EH action convergence.

---

# 3. Candidate estimator families

## 3.1 Covariance normal-variance proxy

Current failed route.

Pros:
- simple;
- fast;
- detects embedding curvature signal.

Cons:
- not intrinsic;
- unstable under sampling;
- weak local convergence.

## 3.2 Angle-deficit / triangulated curvature

Estimate local tangent plane, order neighbors angularly, compute deficit-like quantity.

Pros:
- closer to Regge/triangulation intuition;
- geometric;
- can be integrated over cells.

Cons:
- requires robust local triangulation;
- hard in noisy graphs.

## 3.3 Ollivier-Ricci curvature

Uses Wasserstein transport between neighbor distributions.

Pros:
- intrinsic to metric-measure graph;
- well-studied on graphs.

Cons:
- computationally heavier;
- Ricci-like, not scalar curvature directly.

## 3.4 Forman-Ricci curvature

Combinatorial curvature using cells/weights.

Pros:
- fast;
- graph-native.

Cons:
- depends on chosen cell complex;
- scalar interpretation requires care.

## 3.5 Heat-kernel / spectral curvature

Uses graph Laplacian heat trace asymptotics.

Pros:
- closest to spectral geometry;
- can connect to continuum invariants.

Cons:
- needs careful scale window;
- numerically delicate.

---

# 4. Verifier implementation

## Status
**Implemented as `curvature_estimator_failure_analysis_verifier.py`. Execution log captured.**

The verifier compares simple candidate proxies on:

```text
unit sphere
flat plane
```

under refinement.

It measures:
- sphere/plane separation;
- coefficient-of-variation behavior;
- candidate/weak classification.

## Captured verifier output

```text
Curvature estimator failure analysis verifier
==================================================
Route:
compare candidate local graph curvature proxies on sphere vs plane refinement

ESTIMATOR: covariance_normal_variance
sphere_rows_n_median_cv: [(100, 0.5552674793846717, 0.3103748419935639), (200, 0.4965776614111138, 0.4036295055817339), (400, 0.5220086107771436, 0.3317540854976425), (800, 0.5163225058406127, 0.33092505415657597)]
plane_rows_n_median_cv: [(100, 0.0, 0.0), (200, 0.0, 0.0), (400, 0.0, 0.0), (800, 0.0, 0.0)]
separation_score: 0.9999999999980632
sphere_cv_improvement: 0.9379007061996983
classification: CANDIDATE

ESTIMATOR: angle_deficit_pca
sphere_rows_n_median_cv: [(100, -3.592117714390497e-10, 9.949890153707962), (200, -6.02664584903323e-10, 10.312121571040446), (400, -8.57639737006366e-10, 11.07021597787742), (800, -1.1107910147245548e-09, 18.796001831422277)]
plane_rows_n_median_cv: [(100, -6.153761944460712e-10, 3.2071226607741488), (200, -9.917822119120956e-10, 3.8377234197881775), (400, -1.2850351893689549e-09, 4.511989452574194), (800, -1.826208517741179e-09, 5.453059809583296)]
separation_score: 0.24350497510672028
sphere_cv_improvement: 0.5293620549171086
classification: WEAK

ESTIMATOR: spectral_weight_variance
sphere_rows_n_median_cv: [(100, 0.20222249803845116, 0.6317518767723413), (200, 0.41921219488990835, 0.7769173743568404), (400, 0.8216372026169798, 0.7463282095930617), (800, 1.6321177496243096, 0.6880707070049455)]
plane_rows_n_median_cv: [(100, 0.6083018115990173, 0.5752384469023683), (200, 1.2914740859753997, 0.797204054432536), (400, 2.511407370144229, 0.6936280451819998), (800, 4.850798274982415, 0.8329533648937059)]
separation_score: 0.49648653679003424
sphere_cv_improvement: 0.9181496470345779
classification: CANDIDATE
```

---

# 5. Interpretation

The current covariance proxy is not enough.

A better next route should be:

```text
angle-deficit / triangulated curvature
```

or:

```text
heat-kernel / spectral curvature
```

because these are closer to integrated scalar curvature and action convergence.

The next curvature test should not attempt full ADM convergence yet.

It should first test candidate estimators across reference geometries.

---

# 6. Next derivation target

The next file should be:

```text
CURVATURE_REFERENCE_GEOMETRY_TESTS.md
```

Purpose:

Run reference tests on:

```text
flat plane
sphere
hyperbolic-like saddle / perturbed surface
torus
```

and determine which estimator can reliably distinguish:

\[
R=0,
\qquad
R>0,
\qquad
R<0.
\]

---

# Honest status line

> `CURVATURE_ESTIMATOR_FAILURE_ANALYSIS.md` diagnoses the failed curvature proxy and identifies stronger estimator families. The curvature-convergence seam remains open until a graph curvature estimator passes reference-geometry tests.

**End of file.**
