# UQCF-GEM bridge-to-classical handoff test
## Design
Matched seeds and same initializations were compared under two protocols:

1. `classical_only`
   - baseline relaxer for the full run

2. `bridge_preconditioning`
   - frozen `v9` bridge stage first
   - then the exact same baseline relaxer used in `classical_only`

Targets:
- 1UAO
- 1L2Y

Metrics:
- best RMSD
- angle RMS
- dihedral RMS
- contact recovery

## Purpose
This is the cleanest test of the paper's central interpretation:

Does the bridge create a better starting manifold for classical realization,
or is it only producing a nicer-looking internal trajectory without downstream value?

## Reading guide
Use:
- `uqcf_bridge_to_classical_handoff_summary.csv`
- `uqcf_bridge_to_classical_handoff_stats.csv`

Trajectory-level support:
- `uqcf_bridge_to_classical_handoff_traces.csv`
- RMSD plots for both targets
- sigma_bridge plots during bridge-preconditioning stage
