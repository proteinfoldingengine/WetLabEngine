# V498 Formal Retained-Geometry Report

## Title

**Retained-Geometry Law: A Formal Toy Demonstration of Source-Responsive Effective Branch Geometry**

## Executive summary

This report packages the current retained-geometry law into a formal, reproducible proof run.

The retained bridge generated a dynamic effective branch geometry in which:

1. retained-flow stress loads the geometry,
2. available recoverability reserve constrains deformation,
3. the effective metric changes,
4. curvature-like deformation is derived from the metric,
5. localized defects form where source pressure exceeds local recoverability,
6. repair follows recoverability-weighted geodesics,
7. weak graph families improve after adding true restoration costs.

The central result is the field relation:

\[
\frac{\partial g_{\mathrm{eff}}}{\partial t}
=
G_L *
\left[
\frac{T_{\mathrm{retained}}}{C_t - C_{\mathrm{floor}} + \epsilon}
\right]
-
R_{\mathrm{repair}}
-
D_{\mathrm{leakage}}
\]

with:

\[
C_t = M_t R_t L_t + \lambda_0 \eta_{\mathrm{convert}}(t)B_t
\]

and:

\[
K_{\mathrm{eff}} = \mathrm{Curv}(g_{\mathrm{eff}})
\]

The script `v498_retained_geometry_proof.py` runs this law across six graph families and produces validation tables and plots.

---

# 1. Variables

| Symbol | Meaning |
|---|---|
| \(M_t\) | adaptive safety margin |
| \(R_t\) | retained recovery capacity |
| \(L_t\) | retained lineage addressability |
| \(B_t\) | recoverable branch volume |
| \(C_t\) | total recoverability reserve |
| \(\eta_{\mathrm{convert}}\) | conversion efficiency from stored recoverability into branch geometry |
| \(T_{\mathrm{retained}}\) | retained-flow stress / leakage pressure |
| \(g_{\mathrm{eff}}\) | effective recoverability metric |
| \(K_{\mathrm{eff}}\) | curvature-like operator derived from \(g_{\mathrm{eff}}\) |
| \(D_{\mathrm{leakage}}\) | localized defect leakage |
| \(R_{\mathrm{repair}}\) | repair / relaxation term |

---

# 2. Core equations

## 2.1 Total recoverability reserve

\[
C_t = M_tR_tL_t + \lambda_0\eta_{\mathrm{convert}}(t)B_t
\]

where:

\[
\eta_{\mathrm{convert}} =
\frac{
\mathrm{lineage\ integrity}
\cdot
\mathrm{conductance}
\cdot
\mathrm{topology\ redundancy}
}{
1 + \mathrm{stress\ dispersion} + \mathrm{drift\ pressure}
}
\]

Interpretation:

Stored recursive recoverability \(M_tR_tL_t\) converts into accessible recoverable branch volume \(B_t\) through a measurable conversion efficiency.

---

## 2.2 Source-to-metric field equation

\[
\frac{\partial g_{\mathrm{eff}}}{\partial t}
=
G_L *
\left[
\frac{T_{\mathrm{retained}}}{C_t - C_{\mathrm{floor}} + \epsilon}
\right]
-
R_{\mathrm{repair}}
-
D_{\mathrm{leakage}}
\]

Interpretation:

Metric deformation is driven by retained stress divided by available recoverability reserve.

Stress alone is not the driver.  
Stress-over-reserve is the driver.

---

## 2.3 Curvature-like operator

\[
K_{\mathrm{eff}} = \mathrm{Curv}(g_{\mathrm{eff}})
\]

In the proof script, \(K_{\mathrm{eff}}\) is computed from:

- local geodesic divergence,
- local branch-volume contraction,
- effective metric pinch concentration,
- lineage repair smoothing.

The important point is that \(K_{\mathrm{eff}}\) is derived from the metric.  
It is not inserted as an independent target.

---

## 2.4 Defect localization law

\[
D_i \propto
\left[
\frac{T_i}{C_{\mathrm{surplus},i}+\epsilon}
\right]
\Lambda_i
\Pi_i
\]

where:

- \(\Lambda_i\) = lineage discontinuity,
- \(\Pi_i\) = topology pinch / low conductance.

Interpretation:

Defects form where stress-over-reserve concentrates through weak lineage and topological pinch.

---

## 2.5 Repair-cost correction

Earlier graph-family tests showed weaker repair prediction in scale-free and fragmented graphs. The weakness was traced to under-modeled repair cost:

\[
\mathrm{repair\_cost}
=
\mathrm{path\_cost}
+
\mathrm{hub\_saturation\_cost}
+
\mathrm{lineage\_reconnection\_cost}
\]

This preserves the field law while improving repair geodesic prediction.

---

# 3. Evidence chain

The work progressed through the following retained-geometry signal chain:

1. source pressure creates branch deformation,
2. deformation survives admissible metric changes,
3. source-response law appears,
4. nonlinear saturation appears under high stress,
5. regeneration relaxes deformation,
6. lineage controls residual curvature memory,
7. hysteresis and path dependence appear,
8. memory-kernel source equation fits,
9. locality and distance-decay laws hold,
10. effective metric predicts curvature-like response,
11. defects localize via source/reserve ratio,
12. repair follows recoverability-weighted geodesics,
13. law survives multiple graph families,
14. repair weakness is corrected by true restoration cost.

---

# 4. What the Python proof demonstrates

The proof run creates six graph families:

1. lattice,
2. random geometric graph,
3. scale-free graph,
4. small-world graph,
5. tree with loops,
6. fragmented block graph.

For each graph, it computes:

- \(M, R, L, B\),
- \(\eta_{\mathrm{convert}}\),
- \(C_t\),
- \(C_{\mathrm{floor}}\),
- \(C_{\mathrm{surplus}}\),
- retained-flow stress \(T\),
- effective metric loading \(g_{\mathrm{eff}}\),
- metric deformation \(\Delta g_{\mathrm{eff}}\),
- metric-derived curvature \(K_{\mathrm{eff}}\),
- defect scores,
- leakage path scores,
- repair path scores.

It reports:

- source/reserve → metric deformation \(R^2\),
- metric → curvature-like response \(R^2\),
- defect localization AUC,
- leakage path AUC,
- repair path AUC.

It also generates plots for external review.

---

# 5. What is derived vs empirical

## Derived / frozen in V498

- \(C_t = M_tR_tL_t + \lambda_0\eta B_t\)
- \(\eta_{\mathrm{convert}}\) from lineage, conductance, redundancy, stress dispersion, drift pressure
- source/reserve driver \(T/(C-C_{\mathrm{floor}}+\epsilon)\)
- defect law \(D_i \propto (T_i/C_i)\Lambda_i\Pi_i\)
- repair-cost correction with hub saturation and lineage reconnection

## Still empirical / needs formal derivation

- exact branch-space measure,
- exact curvature operator,
- exact memory kernel \(G_L\),
- exact continuum limit,
- rigorous uniqueness of \(M R L\),
- whether this retained geometry maps to any known physical geometry.

---

# 6. Claim boundary

The current claim is:

> The retained bridge produces a dynamic effective branch geometry in which stress-over-recoverability-reserve deforms the metric, curvature-like response is derived from that metric, and defects localize where source/reserve pressure concentrates through weak lineage/topology structure.

This is a formal retained-geometry toy result.

---

# 7. How to run

In Colab:

```python
!pip install networkx scikit-learn pandas matplotlib
!python v498_retained_geometry_proof.py
```

Outputs will be saved in:

```text
v498_outputs/
```

Key files:

- `v498_summary.csv`
- `v498_summary.json`
- `v498_summary_bars.png`
- `aggregate_source_ratio_metric.png`
- `aggregate_metric_curvature.png`
- `geometry_<family>.png`
- `source_ratio_metric_<family>.png`
- `curvature_consistency_<family>.png`
- `defect_law_<family>.png`

---

# 8. One-line summary

Adaptive branch geometry deforms when retained-flow stress exceeds available recoverability reserve, and the resulting effective metric predicts curvature-like contraction, defects, leakage paths, and repair geodesics.
