# P1 — v9 regularizer-reduction acceptance contract

Status: **FROZEN BEFORE PROSPECTIVE MEASUREMENT**

Base scientific provenance: P0 verified head `6a2362287305a93e4fa63f308dfc19caaf8c1835`.

## Question

Does the live hierarchical v9 gate produce a reproducible advantage over information-matched simpler regularizers once the previously special bridge interpretation is removed?

This is a mechanism-discrimination test, not a claim that the compact folding model is a physical force field.

## Frozen inputs

Only the inputs bound in `INPUT_MANIFEST.json` are eligible.

- 1UAO: exact chain-A C-alpha records consumed from the recovered historical v9 PDB payload.
- 1L2Y: exact chain-A C-alpha records consumed from the recovered historical v9 confirmation PDB payload.
- Fresh PDB downloads are forbidden for this acceptance run.
- Target/native geometry may be used only for post-hoc evaluation metrics. It must not enter any energy or gradient.

## Frozen modes

The seven modes are:

1. `baseline`
2. `angle_only`
3. `dihedral_only`
4. `soft_contact_only`
5. `static_combo`
6. `fixed_gate`
7. `v9`

`static_combo` uses the same v9 ingredients and coefficients with the two live compression gates held fully open: sigma=1 and closure=1.

`fixed_gate` uses the same v9 ingredients with the historical fixed-gate constants recovered before P1:

- sigma = 0.1955639719963073
- closure = 0.0393431633710861

The fixed values may not be refit on 1UAO or 1L2Y.

## Frozen execution protocol

- seeds: 0, 1, 2, 3, 4, 5
- preconditioning stage: 180 steps in the selected mode
- common relaxer: 240 steps in `baseline`
- optimizer: Adam
- learning rate: 0.05
- noise scale: 0.013 with the historical linear decay
- optimizer state is reset at the 180-step handoff for every mode, including baseline
- every mode receives the exact same initial coordinates for a target/seed
- every mode receives the exact same pre-stage and post-stage Gaussian noise tensors for a target/seed
- CPU execution is the authoritative environment

This common-random-number design makes the mode definition the intended causal difference.

## Primary metric

`post_best_rmsd`: the lowest Kabsch C-alpha RMSD observed from the start of the common 240-step baseline relaxation through its final step.

Secondary metrics are final RMSD, pre-stage end RMSD, angle RMS, dihedral RMS, and native-contact recovery. These are descriptive and cannot rescue a failed primary gate.

## Exact primary statistical test

For each comparator, form 12 matched differences:

`post_best_rmsd(v9) - post_best_rmsd(control)`

across 2 targets x 6 seeds.

For the two mechanism-matched comparators (`static_combo`, `fixed_gate`), compute an exact two-sided paired sign-flip test over all 2^12 sign assignments. Apply Holm correction across these two primary comparisons.

## GO / NO-GO rule

P1 is **GO_HIERARCHICAL_V9** only if all of the following are true:

1. v9 has a lower pooled mean `post_best_rmsd` than every non-v9 mode.
2. v9 has a lower target-wise mean `post_best_rmsd` than `static_combo` on both 1UAO and 1L2Y.
3. v9 has a lower target-wise mean `post_best_rmsd` than `fixed_gate` on both 1UAO and 1L2Y.
4. The Holm-adjusted exact paired sign-flip p-value is < 0.05 for v9 versus `static_combo`.
5. The Holm-adjusted exact paired sign-flip p-value is < 0.05 for v9 versus `fixed_gate`.

If any condition fails, the result is **NO_GO_HIERARCHICAL_ADVANTAGE**.

A NO-GO does not mean the geometric regularizers are useless. It means this experiment did not establish a distinct scientific advantage for the live hierarchical gate over simpler information-matched alternatives.

## Exposure rule

The acceptance contract, implementation, source identity, and input hashes are frozen before the first prospective result is read. After exposure:

- no coefficient tuning,
- no seed replacement,
- no target substitution,
- no gate refitting,
- no metric substitution.

A rerun is permitted only for an infrastructure failure and must use the exact same code SHA and inputs.
