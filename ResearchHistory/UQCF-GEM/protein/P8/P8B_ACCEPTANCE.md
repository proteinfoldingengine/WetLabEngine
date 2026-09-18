# Protein P8B — Source-faithful constrained-controller gate

**Status:** preregistered before implementation and before any P8B protein outcome exposure.

## Scientific question

P8A source-certified a recovered Patch-622/623 controller that is materially different from the StableDAGPhysics mechanism reduced by P7.

P8B asks the smallest prospective question that can determine whether that recovered controller has scientific value:

> When the recovered coordinate-active Patch-622/623 mechanism is placed on a covalently exact peptide backbone, does its adaptive topology timing produce useful native-blind structural preorganization beyond matched versions of the same force set with the timing removed or altered?

This is not a historical replay. The old unconstrained Cartesian C-alpha representation is not restored.

## Claim boundary

A P8B GO would establish only that the recovered controller/timing mechanism produces a reproducible preorganization signal on a physically constrained 1VII benchmark under this frozen protocol.

A GO would **not** establish:

- general de novo protein folding;
- historical Patch-622/624 result validity;
- transfer to other proteins;
- novelty over established protein-folding methods;
- superiority to modern force fields;
- a new physical law.

A GO authorizes only P8C held-out transfer testing.

A NO-GO closes the direct source-faithful constrained-transplant line. There will be no coefficient rescue on this benchmark.

## Why 1VII

P8B uses **1VII** only.

Reasons fixed before measurement:

1. 1VII is explicitly part of the historical Patch-624-era claim lineage.
2. Its exact evaluator is already pinned in the validated P5/P6 archive.
3. At 36 residues it is large enough for the recovered absolute Betti threshold of 8 to be meaningfully reachable without rescaling the historical gate.
4. Restricting P8B to one historically adjacent target keeps the reopen bounded and inexpensive.

Exact evaluator:

- repository path: `ResearchHistory/UQCF-GEM/protein/P5/inputs/1VII.pdb`
- Git blob: `dc55a7f18ce79b6db592240bdb7dcee96a4c1b8b`
- sequence: `MLSDEDFKAVFGMTRSAFANLPLWKQQNLKKEKGLF`
- native coordinates are evaluation-only.

1L2Y and 1UAO are reserved for P8C and may not be consulted to tune P8B.

## Representation

Use the already validated P6 canonical peptide kinematics:

- fixed target-independent N-Cα-C covalent geometry;
- trans omega = 180 degrees;
- only phi/psi torsions are optimized;
- maximum allowed bond-length and bond-angle reconstruction drift: `1e-8`.

The P8B implementation must reuse the frozen P6 kinematic constants and reconstruction equations byte-for-byte or by a mechanically verified vendor copy.

The initial conformation is generated from the P6 deterministic native-blind torsion initializer, not from target geometry and not from the historical unconstrained Cartesian random walk.

## Recovered coordinate mechanism

P8B uses the exact Patch-622/623 recovered coordinate-force semantics and coefficients frozen by P8A.

### Compaction force set

- C-alpha Lennard-Jones repulsion
- C-alpha pseudo-dihedral angular torque
- C-alpha pseudo-dihedral Ramachandran potential
- fractal compaction funnel `k_df * Rg`
- hydrophobic centroid-collapse term

### LockIn additions

- current-state contact springs
- screened electrostatics

### Frozen coefficients

- `k_contact_spring_base = 1.5`
- `k_df_funnel = 6000.0`
- `k_phi_torque_base = 1.0`
- `k_lj_repulsion_base = 1.25`
- `k_hydro_base = 0.75`
- `k_electrostatic_base = 1.0`
- `k_rama = 0.05`
- `contact_dist = 8.0 A`
- `DEBYE_LENGTH = 5.0 A`
- historical hydrophobic-residue set and formal residue-charge table from the recovered source.

Pseudo-dihedrals, Betti proxy, contact-pair selection, and electrostatic masking must preserve the recovered source semantics.

No native structure, native contacts, native Rg, native torsions, or native secondary structure may enter the force calculation, DAG, optimizer, force scaling, or stopping rule.

## Gamma channel

The recovered Patch-622/623 gamma variable may be retained for source fidelity with:

- initial gamma = 1.0;
- gamma learning rate = 0.1;
- gamma target = 3.0;
- `k_gamma_surge = 2.0`.

P8A established that the Patch-624 torsional penalty acts through gamma while `phi_rms` is detached to a scalar, and no gamma value feeds the coordinate-force path or Betti DAG.

Therefore Patch-624's torsional penalty is excluded from P8B's **coordinate-mechanism** question. It may not be presented as a distinct folding-coordinate mechanism.

## Exact recovered topology semantics

Use the recovered history semantics exactly:

- Betti threshold: `8`
- DAG transition lifetime: `100`
- force activation lifetime: `50`
- history lifetime means the **count of qualifying entries in the retained history**, not a strict consecutive streak;
- history is updated before DAG evaluation;
- once the DAG reaches LockIn it does not transition back.

No threshold may be rescaled for chain length after outcome exposure.

## Experimental arms

For every seed, all four arms start from identical phi/psi torsions.

### 1. `dynamic_622`

Exact recovered two-level controller:

- starts in Compaction;
- DAG transitions to LockIn when the recovered Betti/lifetime rule is met;
- contact springs and screened electrostatics are applied only when the recovered force gate is active.

### 2. `compaction_only`

Exact Compaction force set for the entire trajectory.

- DAG transition disabled;
- no contact springs;
- no screened electrostatics.

This tests whether any signal is merely the recovered fractal/compaction force set.

### 3. `force_gate_only`

The DAG phase is treated as LockIn from step 0, but the recovered ForceField Betti gate is preserved.

Thus contact/electrostatic additions may activate after the configured force lifetime of 50 qualifying history entries rather than waiting for the 100-entry DAG transition.

This tests whether the second 100-entry DAG layer adds value beyond the lower-level topology gate.

### 4. `all_lockin_from_start`

The exact LockIn coordinate force set is active from step 0 and the topology gate is bypassed for contact/electrostatic additions.

No coefficient changes are allowed.

This tests whether adaptive timing adds value beyond simply exposing the same final force set for the whole trajectory.

## Seeds and optimization

Seeds: `42,43,44,45,46,47,48,49`.

For every arm/seed:

- CPU float64 PyTorch;
- deterministic algorithms;
- identical initial torsions across arms;
- optimizer: Adam;
- torsion learning rate: `0.001`;
- gamma learning rate: `0.1` if gamma is retained;
- fixed budget: `2000` optimization steps;
- angle wrapping after each torsion update;
- no native-informed early stopping;
- no seed removal.

The 2000-step budget and 0.001 primary optimizer learning rate are taken directly from the recovered Patch-622/623 configuration rather than tuned on P8B outcomes.

## Primary endpoint

Use the already validated P6 fixed-budget long-range native-contact precision at final step 2000:

1. consider all C-alpha pairs with sequence separation >= 4;
2. rank pairs by modeled C-alpha distance;
3. take `K = max(1, floor(N/2))` closest eligible pairs;
4. native contact = corresponding evaluator C-alpha distance < 8.0 A;
5. score = native-contact fraction among those K pairs.

For 1VII, `N=36` and therefore `K=18`.

No best-over-trajectory native metric may be used for the decision.

## Anti-collapse gate

For `dynamic_622`, the median final C-alpha Rg/native-Rg across the eight seeds must lie in:

`[0.75, 1.25]`.

Native Rg is evaluation-only.

## Primary comparisons and statistics

Three matched paired comparisons across the eight seeds:

1. `dynamic_622 - compaction_only`
2. `dynamic_622 - force_gate_only`
3. `dynamic_622 - all_lockin_from_start`

Higher primary precision is better.

Use exact two-sided paired sign-flip tests over all `2^8` assignments. Apply Holm correction across the three primary comparisons.

## GO rule

Return:

`GO_PATCH622_CONTROLLER_SIGNAL_ON_PHYSICALLY_CONSTRAINED_1VII`

only if **all** conditions are true:

1. `dynamic_622` has the highest mean final primary precision of the four arms;
2. mean paired primary delta is positive against each of the three controls;
3. Holm-adjusted exact paired p < 0.05 for each of the three comparisons;
4. median final dynamic Rg/native-Rg is in `[0.75,1.25]`;
5. every trajectory preserves canonical covalent geometry below `1e-8` maximum bond-length and bond-angle drift;
6. every trajectory completes with finite coordinates, gradients, and energies;
7. the native-information firewall passes on the exact implementation used for measurement.

Otherwise return:

`NO_GO_PATCH622_CONTROLLER_SIGNAL_ON_PHYSICALLY_CONSTRAINED_1VII`.

## Required secondary diagnostics

These are reported but cannot rescue a failed GO:

- final corrected Kabsch C-alpha RMSD;
- native-contact recall;
- Rg and Rg ratio at checkpoints;
- exact Compaction -> LockIn transition step for every dynamic seed;
- Betti count and recovered history-count trace;
- contact-spring/electrostatic activation trace;
- force-component energies;
- maximum torsion gradient norm;
- minimum nonadjacent C-alpha distance;
- final pseudo-dihedral dispersion.

Checkpoints: `0, 50, 100, 250, 500, 1000, 2000`.

## P8C authorization

Only a P8B GO authorizes P8C.

P8C must freeze the exact P8B implementation and coefficients and test transfer without rescaling on at least the already-pinned 1L2Y and 1UAO evaluators. P8B itself is not a generalization claim.

## Post-exposure rule

After the first authoritative P8B structural result is exposed:

- no coefficient tuning;
- no learning-rate change;
- no Betti-threshold or lifetime rescaling;
- no seed removal;
- no endpoint replacement;
- no checkpoint rescue;
- no alternate 1VII structure;
- no force reinterpretation.

A P8B NO-GO ends this direct recovered-controller line on the present scientific case.
