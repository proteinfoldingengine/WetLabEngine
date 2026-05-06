# CURVATURE_ESTIMATOR_FAILURE_ANALYSIS_VERIFIER_SUMMARY.md

# Verifier Summary
## Curvature estimator failure analysis

## Status
**Executed estimator comparison. Not curvature proof.**

Verifier file:

```text
curvature_estimator_failure_analysis_verifier.py
```

Execution log:

```text
curvature_estimator_failure_analysis_verifier_run.log
```

## Captured output

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

## Interpretation

The verifier compares candidate local graph curvature proxies on sphere and plane reference geometries.

This is used to choose the next estimator for controlled reference-geometry tests.

**End of summary.**
