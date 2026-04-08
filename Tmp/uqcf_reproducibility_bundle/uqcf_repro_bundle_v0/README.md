# UQCF Repro Bundle v0

This bundle freezes the first reproducibility spine for the current UQCF-GEM sprint cycle.

## Purpose
Allow an external technical reader to verify three core claims without conversation context:

1. A broad-attractor upstream selector flow exists and converges near the certified closure point.
2. The selector's load-bearing structure can be audited by ablation and refined by lag renormalization.
3. A first locked bridge-to-observable proxy exists with a public falsification grid.

## Folder layout

### 01_baseline_closure
Broad-initial-condition convergence sweep for the upstream relaxation flow.
Expected qualitative outcome:
- all runs converge to the same selected attractor
- final selected state near gamma ~ 0.273, chi ~ 0.401, W ~ 0.431

### 02_selector_audit
Ablation audit of the selector flow.
Expected qualitative outcome:
- full flow performs best
- freezing W is catastrophic away from near-solved initialization
- removing screening worsens the attractor
- removing lag worsens but does not destroy selection

### 03_selector_refinement
Lag-renormalized selector scans.
Expected qualitative outcome:
- screening exponent stays near 1
- improved selector obtained with stronger, mildly sublinear lag
- best narrow refinement lands near gamma ~ 0.2686

### 04_observable_proxy
First locked DESI-facing expansion-response proxy and falsification grid.
Expected qualitative outcome:
- strictly positive F_AP-style response across z = {0.51, 0.71, 0.93, 1.32, 1.48, 2.10, 2.33}
- percent shift rises from about +0.26% to about +0.91%

## Minimal run order for review
1. Read 01_baseline_closure/flow_selection_summary.json
2. Read 02_selector_audit/ablation_summary.json
3. Read 03_selector_refinement/narrow_lag_refine_summary.json
4. Read 04_observable_proxy/sprintB_locked_falsification_grid_summary.json

## Current scope
This is a frozen artifact bundle, not yet a public release package.
It does not include standalone Python entrypoints yet.
It is intended to lock outputs, file structure, and expected values before that next step.
