# Protein P8B — Measurement Implementation Contract

**Frozen before prospective native-evaluation exposure.**

This file defines implementation/output details that do not alter the scientific GO/NO-GO rule in `P8B_ACCEPTANCE.md`.

## Run matrix

Exactly 72 trajectories:

```text
3 targets × 6 seeds × 4 arms = 72
```

Each matched target/seed uses identical initial P6 torsions in every arm.

## Optimization timing

A trajectory contains exactly 2000 optimizer updates indexed `0..1999`.

For each optimizer index:

1. reconstruct the canonical P6 backbone from current phi/psi;
2. compute the historical Betti1 proxy from modeled C-alpha coordinates;
3. for `recovered_state_gate`, append the current proxy to history and update the recovered controller;
4. select the frozen coordinate force set;
5. calculate loss;
6. backpropagate;
7. Adam step at learning rate 0.02;
8. wrap phi/psi to the circular range;
9. perform numerical/covalent-health checks.

The fixed-time control first uses LockIn forces at optimizer index 99.

## Native-evaluation boundary

Optimization and controller execution receive no native coordinates.

Native-derived values are computed only after the trajectory states have already been generated.

The stored evaluator is allowed only for:

- starting-state top-K native-contact precision;
- fixed-checkpoint diagnostic precision;
- final primary precision;
- final Rg/native-Rg;
- corrected Kabsch C-alpha RMSD;
- native-contact recall or other explicitly secondary diagnostics.

## Frozen checkpoints

The diagnostic checkpoints are numbers of completed optimizer updates:

```text
0, 99, 100, 500, 1000, 2000
```

Checkpoint 0 is the common starting state. Checkpoint diagnostics cannot replace the final-step primary endpoint.

## Required outputs

The authoritative measurement must produce:

- `p8b_results.csv`
- `p8b_controller_traces.csv`
- `p8b_checkpoint_traces.csv`
- `p8b_summary.csv`
- `p8b_primary_comparisons.csv`
- `p8b_acceptance.json`
- `p8b_run_manifest.json`
- `SHA256SUMS.txt`

## Result rows

Each final trajectory row records at minimum:

- target;
- seed;
- mode;
- starting-state primary precision;
- final primary precision;
- final Rg/native-Rg;
- final corrected C-alpha RMSD;
- maximum bond-length drift;
- maximum bond-angle drift;
- numerical-health status;
- final optimizer step;
- whether LockIn was ever entered;
- LockIn transition step;
- number/fraction of steps with contact/electrostatic LockIn forces active.

## Controller trace

For the candidate arm, every optimization index records:

- historical Betti1 proxy;
- qualifying-history count;
- phase;
- transition flag;
- LockIn contact/electrostatic activation flag.

This trace is mechanistic evidence, not a native-derived endpoint.

## Adjudication

The adjudicator consumes only the frozen final result rows for the primary decision.

It must:

1. verify all 72 unique target/seed/mode rows are present;
2. compute pooled and target-wise means;
3. compute the three matched candidate-control precision comparisons;
4. apply exact two-sided paired sign-flip tests over 18 pairs per comparison;
5. apply Holm correction across all three comparisons;
6. apply the starting-state improvement, controller-use, Rg, geometry, numerical-health, firewall and source-integrity gates;
7. return exactly one of:
   - `GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION`
   - `NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION`.

No checkpoint or secondary metric can rescue a failed primary decision.
