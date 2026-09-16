# HB1 Replay Attempt 001 — Unchanged Historical Launch

Date: 2026-09-16
Branch: `gen3-historical-backbone-reconstruction-v1`
Historical target: `1VII`
Historical patch identifier: `Patch_630_Full_Backbone_1VII`

## Purpose

Test how far the contemporaneous August 5, 2025 Patch-630 source package runs in the current isolated environment without editing the historical source.

## Preflight

- All recovered `.py` files passed `python -m py_compile`.
- All project-local modules imported successfully.
- Direct project-local imports referenced by `main.py` are present in the recovered set.
- No historical physics or objective code was modified.

## Launch result

The unchanged runner successfully:

1. selected the local runtime path,
2. loaded `generic_physics.yaml`,
3. merged the configuration,
4. initialized `Patch_630_Full_Backbone_1VII`, and
5. selected the CPU device.

It then reached the historical external-input boundary and attempted:

`https://files.rcsb.org/download/1VII.pdb`

The current isolated execution environment has no external network access, so DNS resolution failed. The runner then exited through its existing error path with `Could not retrieve protein data. Halting simulation.`

## Interpretation

This is **not a scientific or code-compatibility failure**. It is an environmental input-access failure encountered before model construction, optimization, or force evaluation.

No historical claim is promoted by this attempt. In particular, `phi_RMS = 0.2215` and `RMSD = 10.19 A` remain unreproduced historical values.

## Next step

Recover/pin the exact 1VII PDB input (or the closest authoritative historical PDB bytes available), record its SHA-256 and provenance, and supply it through a separate compatibility adapter or local cache. The historical physics source must remain byte-for-byte unchanged.

After the PDB boundary is cleared, rerun unchanged and stop again at the first new incompatibility or scientific result.
