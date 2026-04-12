# UQCF-GEM v9 trajectory packet
## Purpose
This packet is the direct trajectory-level artifact check requested for frozen **v9**.

It contains the raw time-series traces for:
- **1UAO** baseline vs frozen v9
- **1L2Y** baseline vs frozen v9

## What is included
- `uqcf_bridge_patch_v9_1uao_traces.csv`
- `uqcf_bridge_patch_v9_1uao_results.csv`
- `uqcf_bridge_patch_v9_1uao_summary.csv`
- `uqcf_bridge_patch_v9_1uao_stats.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_traces.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_results.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_summary.csv`
- `uqcf_bridge_patch_v9_1l2y_confirm_stats.csv`

## What the traces contain
Per checkpoint step, the traces include:
- RMSD
- energy
- bridge observables when present:
  - compat_field
  - dihedral_preserve
  - productive_contact
  - sigma_bridge
  - closure_ready
  - false_closure
  - dir_pen
  - angle_var
  - dihed_smooth
  - soft_contacts
  - density_var
  - rg
  - loop_compat

For baseline rows, bridge observables are empty because no bridge layer is injected.

## What this packet is for
This is meant to answer the artifact question at the trajectory level:

Does frozen v9 show a distinct time-evolution signature relative to baseline,
or are the summary gains only a reporting artifact?

## Important limit
This packet contains the folding trajectories for frozen v9.
It does **not** currently include the raw TSP trajectories.
So it is enough to test the folding-side operator trace, but not yet the TSP-side parallel.

## Suggested artifact checks
1. Compare baseline vs v9 RMSD over step for each target.
2. Check whether sigma_bridge and closure_ready rise in tandem with structural ordering.
3. Check whether gains appear gradually through the trajectory, rather than only at the endpoint.
4. Check whether bridge observables correlate with reduced dir_pen / angle_var in the same runs.
