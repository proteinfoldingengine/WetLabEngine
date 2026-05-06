# HEAT_KERNEL_FAILURE_ANALYSIS_VERIFIER_SUMMARY.md

# Verifier Summary
## Heat-kernel coefficient failure diagnostics

## Status
**Executed failure analysis. Current estimator not accepted.**

Verifier file:

```text
heat_kernel_failure_analysis_verifier.py
```

Execution log:

```text
heat_kernel_failure_analysis_verifier_run.log
```

## Captured output

```text
Heat kernel failure analysis verifier
==================================================
Route:
test sign/magnitude sensitivity to boundary, Laplacian normalization, and heat window

config,geometry,intR_coeff_median,intR_coeff_std,A0_median,h_median
unnormalized_h2,plane_patch,11.479272489175688,13.547442416638715,3.8837980386268987,0.2159581502178231
unnormalized_h2,flat_torus,-59.11856826723677,14.76996322285992,32.62481089142009,0.6518172197934764
unnormalized_h2,sphere,-37.36064240114522,12.097962827834472,10.649902285661035,0.3692840017936622
unnormalized_h2,saddle_patch,14.436937344072813,16.795927130165964,5.20243584354693,0.24979279803870558
unnormalized_smaller_window,plane_patch,-209.63739987352358,49.80288907426748,5.207197772521502,0.2159581502178231
unnormalized_smaller_window,flat_torus,-396.2687846608115,44.204804570969465,47.892917281256636,0.6518172197934764
unnormalized_smaller_window,sphere,-341.9455771301492,76.30875031155318,15.222678626718869,0.3692840017936622
unnormalized_smaller_window,saddle_patch,-171.94270876307655,31.13376581359482,6.948629946900895,0.24979279803870558
normalized_dimensionless,plane_patch,-38.06610186324306,6.298288257957372,680.5471393381041,0.2159581502178231
normalized_dimensionless,flat_torus,-95.78868687797404,13.27727288671167,686.4553818136785,0.6518172197934764
normalized_dimensionless,sphere,-78.23597158021606,22.68001801211965,684.2562261863367,0.3692840017936622
normalized_dimensionless,saddle_patch,-42.7389355360906,19.086564058703857,681.1266767523218,0.24979279803870558

diagnosis:
if flat_torus differs strongly from plane_patch, boundary/embedding/graph construction matters
if signs flip across windows/configs, coefficient sign is not stable
if normalized config suppresses separation, scale information is erased
```

## Interpretation

The verifier tests sensitivity to boundary, heat-window, and Laplacian normalization.

The goal is to diagnose why the heat coefficient responds to geometry but gives unreliable signs/magnitudes.

**End of summary.**
