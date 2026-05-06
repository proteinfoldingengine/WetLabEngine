# HEAT_KERNEL_CURVATURE_ACTION_VERIFIER_SUMMARY.md

# Verifier Summary
## Heat-kernel route to integrated scalar curvature

## Status
**Executed spectral diagnostic. Not curvature closure.**

Verifier file:

```text
heat_kernel_curvature_action_verifier.py
```

Execution log:

```text
heat_kernel_curvature_action_verifier_run.log
```

## Captured output

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

## Interpretation

The verifier computes fixed graph heat-trace features across multiple reference geometries with no per-geometry calibration.

This tests whether the spectral route is promising before attempting heat-trace coefficient extraction.

**End of summary.**
