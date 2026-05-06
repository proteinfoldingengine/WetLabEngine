# RENORMALIZED_HEAT_KERNEL_CONVERGENCE_CAMPAIGN_VERIFIER_SUMMARY.md

# Verifier Summary
## Renormalized heat-kernel convergence campaign

## Status
**Executed convergence campaign diagnostic. Not curvature proof.**

Verifier file:

```text
renormalized_heat_kernel_convergence_campaign_verifier.py
```

Execution log:

```text
renormalized_heat_kernel_convergence_campaign_verifier_run.log
```

## Captured output

```text
Renormalized heat-kernel convergence campaign verifier
==================================================
Route:
fixed flat-baseline residual heat coefficient across refinement ladder
No per-geometry calibration.

n,h_median,flat_baseline_raw,sphere_raw_median,sphere_residual_median,sphere_residual_std,flat_residual_std,flat_window_cv,sphere_window_cv,residual_separation_z
60,0.7757960938871017,-243.33284431895373,-225.27935174707983,18.053492571873903,5.183120231753891,5.533720290772406,0.4984634018268752,0.521458870737542,1.6845909514025725
90,0.6538535307637955,-365.04282497083943,-357.00703972883724,8.035785242002191,9.508254767713602,6.33598320051037,0.5147000595095625,0.5092017042995984,0.5071739807315226
120,0.5858965120954753,-497.5474753982587,-463.7057727481736,33.8417026500851,17.95451367826028,3.887813736945229,0.5095980130636666,0.5276242766354742,1.5493633991826663
180,0.4628031803042234,-706.93935293054,-705.5335949906953,1.4057579398447047,27.598253520343775,11.071702769215516,0.5225808511036026,0.5237487393869896,0.03635271602890889
240,0.40787755370122514,-970.6284668685373,-972.4283902276634,-1.799923359126069,14.310269332545287,11.576732892539827,0.5179264651168933,0.5142236191082694,0.06953000364722925
positive_residual_all_refinements: False
window_cv_ok_all: True
separation_ratio_last_vs_first: 0.041274116775528225
residual_vs_h_log_slope: 4.233874194728276
classification: CONVERGENCE_CAMPAIGN_WEAK
```

## Interpretation

The verifier evaluates the flat-baseline residual heat coefficient across a refinement ladder.

This tests whether the positive sphere residual persists with increasing graph density.

**End of summary.**
