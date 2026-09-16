# Gen3 HB1 — Patch 630 Historical Source Recovery

Status: **source package recovered; raw historical run outputs not found; reproduction not yet executed.**

This directory freezes the contemporaneous August 5, 2025 source package associated with the historical UQCF-GEM Patch 630 full-backbone result. It is quarantined historical evidence. Nothing in this directory is active Gen3 production physics.

## What is recovered

The recovered runner identifies itself as `Patch 630: Full Backbone Angular Physics`, targets `1VII`, defines the patch identifier `Patch_630_Full_Backbone_1VII`, loads N/CA/C coordinates, optimizes the full backbone, computes true backbone angular metrics, and writes diagnostics/plots. The accompanying YAML specifies a 5,000-step, seed-42, random-coil run and retains Patch-629 Ramachandran/gating parameters.

The recovered core source files are copied byte-for-byte from the Drive artifacts available on 2026-09-16. Their Drive IDs, timestamps, byte counts, and SHA-256 digests are recorded in `SOURCE_MANIFEST.json`.

## Important provenance boundary

The historical August 5 report states final `phi_RMS = 0.2215` and `RMSD = 10.19 A`, with a non-degenerate Ramachandran distribution and topology-triggered LockIn. Those numbers are **not promoted to reproduced results** here. Exact Drive searches for the runner-derived output names returned no results:

- `forces_log_Patch_630_Full_Backbone_1VII.txt`
- `diagnostics_timeseries_Patch_630_Full_Backbone_1VII.csv`
- `plots/Patch_630_Full_Backbone_1VII/`

Absence from search is not proof that the outputs never existed or were deleted; it means they have not been recovered.

## HB1 next experimental step

1. Freeze a runnable environment for this exact source package.
2. Identify any remaining imports needed by `main.py` (`chart_utils`, `metrics_history`, and related utilities) from the same August 5 folder/revision.
3. Attempt an **unaltered replay** first. Compatibility changes, if required, must live in an adapter layer and be separately hashed.
4. Record Python, PyTorch, NumPy, SciPy, package versions, CPU/GPU, PDB retrieval content hash, random seed, and output hashes.
5. Compare reproduction metrics to the historical narrative only after the run finishes.
6. Then run causal ablations: full-backbone vs C-alpha-only; Rama on/off; DAG/topology gate on/off; torsional penalty on/off; matched conventional geometric regularizer.

## Scientific rule

The purpose of HB1 is **not** to rescue the historical claim. It is to determine whether the observed backbone-ordering behavior reproduces and, if it does, which mechanics cause it.
