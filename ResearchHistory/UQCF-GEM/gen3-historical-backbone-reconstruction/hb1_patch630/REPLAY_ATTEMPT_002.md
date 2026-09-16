# HB1 Replay Attempt 002 — Patch 630 Historical Replay

Date: 2026-09-16
Branch: `gen3-historical-backbone-reconstruction-v1`
Historical target: `1VII` (Villin headpiece)
Historical patch identifier: `Patch_630_Full_Backbone_1VII`

## Result

**REPRODUCED to close numerical agreement.**

The recovered August 5, 2025 Patch-630 source was executed for the configured 5,000 steps with seed 42 and random-coil initialization. Historical physics/objective/source files were not edited. A separate adapter intercepted only the historical network fetch of `1VII.pdb` and supplied a pinned local input projection containing the deposited SEQRES plus the exact N/CA/C coordinate records used by the historical loader.

### Final replay state

- Final RMSD: **10.1913 A**
- Final gamma_bar: **3.0016**
- Final phi_RMS: **0.2226**
- Final Betti1 count: **544**
- Final Betti1 lifetime: **120**
- Final phase: **LockIn**
- Runtime: **21.51 s** on the recorded CPU environment

### Historical contemporaneous report

- RMSD: **10.19 A**
- phi_RMS: **0.2215**
- gamma_bar: approximately **3.0**
- phase behavior: topology-triggered **LockIn**

The RMSD agrees to the reported two-decimal precision. The reproduced phi_RMS differs from the historical reported value by approximately 0.0011 absolute. The qualitative dynamics also agree: RMSD and phi_RMS decline through LockIn, gamma remains capped near 3.0, and the final topology state has persistent Betti1 lifetime.

## Input provenance and limitation

The isolated runtime could not reach RCSB directly. An independently preserved legacy 1VII PDB copy was located in the OpenMM/PDBFixer test corpus (`pdbfixer/tests/data/test.pdb`, commit `5e658a4fb8d2b90d65ca8408c845cbf104ce7099`). It identifies itself as PDB 1VII and contains the Villin headpiece deposited sequence and coordinates. For the replay adapter, only the fields consumed by historical `protein_model.py` were projected into a local PDB input: SEQRES plus N, CA, and C ATOM records for all 36 residues.

Pinned projected-input SHA-256:

`774243f304cb7e0b95b69ea24a7bfbae6d24ab92419b74fc8db8bbfdf4c32200`

This is **not claimed to be the byte-identical full RCSB PDB file used in August 2025**. It is an exact projection of the required sequence/backbone records from an independently preserved 1VII legacy PDB copy. Because the historical loader ignores the other PDB records for the simulation state, this is sufficient for this replay, but a future audit should still compare against an official/versioned 2025 RCSB artifact if recovered.

## Output hashes

- summary log: `4bfc53adf53463d163c7c263331dcdcced655f36047c59a2da8f8adbe51325df`
- diagnostics timeseries CSV: `3b25ff8e3630943319408db96ffbdd31df6204a69b1cf90ef4a0500e0dc17118`
- comprehensive report PNG: `d1e1d35254b87b9a0b9d7bf754d3bab842446fc9b18e181504dd910051a281f8`
- diagnostics report PNG: `42bd79498af5ccaa12156fe22fc7f0680846508342cf699d052118ff291bd5f5`
- replay adapter: `69fdbbc3bdacb557a3e3cb28001284e3c49f6f449a530afa8ca7194480df7a51`

## Scientific interpretation

This replay materially upgrades the Patch-630 evidence. The historical values are no longer narrative-only: the recovered source reproduces essentially the same final RMSD, torsional-order metric, coherence state, and LockIn phase under a separately pinned backbone input.

It does **not** establish that Patch 630 predicts native protein folds, that its mechanism is novel, or that every force term is causally responsible for the result. The next gate is causal ablation.

## Next gate

Run matched ablations from the same seed/input/config:

1. full backbone with historical mechanics (replay baseline),
2. Ramachandran force disabled,
3. topology/DAG phase transition disabled,
4. torsional-incoherence penalty disabled,
5. C-alpha-only or matched reduced-coordinate control where historically well-defined,
6. conventional geometric-regularization control.

No parameter retuning should occur between baseline and ablations unless preregistered as a separate experiment.