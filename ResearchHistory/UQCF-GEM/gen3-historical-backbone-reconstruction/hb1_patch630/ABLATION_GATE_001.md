# Gen3 HB1 — Patch 630 Causal Ablation Gate 001

Date: 2026-09-16
Branch: `gen3-historical-backbone-reconstruction-v1`
Baseline replay record: `REPLAY_ATTEMPT_002.md`
Target: `1VII` Villin headpiece
Seed: 42
Steps: 5000
Input projection SHA-256: `774243f304cb7e0b95b69ea24a7bfbae6d24ab92419b74fc8db8bbfdf4c32200`

## Experimental rule

All runs use the same recovered Patch-630 source, pinned 1VII backbone input, random seed, optimizer, step count, learning rates, and force constants except for the single preregistered ablation named for that run. The historical source remains preserved separately; ablations are executed only in quarantined run copies/adapters.

## Results

| Run | Final RMSD (A) | Final phi_RMS | gamma_bar | Betti1 | lifetime | final phase |
|---|---:|---:|---:|---:|---:|---|
| Historical replay baseline | 10.1913 | 0.2226 | 3.0016 | 544 | 120 | LockIn |
| Ramachandran disabled (`k_rama=0`) | 10.1913 | 0.2226 | 3.0016 | 544 | 120 | LockIn |
| Torsional-incoherence penalty disabled (`k_torsion_penalty=0`) | 10.1913 | 0.2226 | 3.0016 | 544 | 120 | LockIn |
| DAG Compaction->LockIn transition suppressed | 10.2661 | 0.4286 | 3.0016 | 546 | 120 | Compaction |

## Direct causal findings

### Ramachandran term

Disabling `k_rama` produces the same final summary as baseline. Inspection of the baseline diagnostics shows `ramachandran_potential_loss == 0` for all 5000 steps. Therefore the recovered Patch-630 replay's reproduced `phi_RMS ~= 0.2226` cannot be attributed to an active Ramachandran loss in this run.

### Torsional-incoherence penalty

Disabling `k_torsion_penalty` also produces the same final summary as baseline. Baseline diagnostics show `torsional_incoherence_penalty_loss == 0` for all 5000 steps. Therefore this penalty likewise did not cause the reproduced torsional-order result in the replay.

### DAG / topology-triggered LockIn

The baseline switches from `Compaction` to `LockIn` at step 99. Suppressing that transition changes final `phi_RMS` from 0.2226 to 0.4286 (about 92.5% higher) while changing final RMSD only from 10.1913 A to 10.2661 A (about +0.0748 A).

This means the LockIn transition materially improves the backbone angular-order metric while having only a small effect on this run's final C-alpha RMSD.

## Which mechanics actually switch on at LockIn?

The baseline diagnostics show that the force components newly becoming nonzero at step 99 are:

- `contact_springs_loss` — nonzero from step 99 through 4999
- `screened_electrostatics_loss` — nonzero from step 99 through 4999

By contrast:

- `ramachandran_potential_loss` remains zero for all steps
- `torsional_incoherence_penalty_loss` remains zero for all steps
- angular torque, fractal compaction, hydrophobic collapse, and Lennard-Jones repulsion were already active before LockIn

Therefore the current evidence narrows the LockIn effect primarily to the mechanics added at transition, especially contact springs and/or screened electrostatics, or to their interaction with the pre-existing force set.

## Important interpretation boundary

This gate does not show that contact springs or electrostatics individually cause the improvement. It only shows that suppressing the phase transition removes their LockIn activation and weakens angular ordering. Individual ablations are required next.

It also does not establish native-fold prediction or novelty. Final RMSD remains approximately 10 A in both baseline and DAG-off runs. The scientifically interesting result at this stage is reproducible backbone angular organization and a measurable causal contribution from the LockIn phase.

## Next gate

Run matched LockIn-component ablations, one at a time:

1. contact springs disabled while preserving the normal DAG transition;
2. screened electrostatics disabled while preserving the normal DAG transition;
3. both disabled as an interaction control;
4. compare trajectory divergence beginning at step 99, especially phi_RMS, RMSD, Betti1, Rg/compaction proxies, and individual loss terms.

No retuning should occur between these runs.
