# Protein P6 — Native-Blind Physical Preorganization Gate

**Status:** preregistered before implementation and before prospective result exposure.

## Scientific question

Can a covalently exact, torsion-space peptide backbone driven only by transparent conventional native-blind physics generate **sequence-specific native-topology enrichment beyond generic polymer collapse** across unrelated small proteins?

P6 is a new benchmark. It is **not** a rescue of P1/v9, Patch-630, or the P5 TPO entropy term. Their frozen NO-GO decisions remain unchanged.

## Claim boundary

A P6 GO would establish only that this minimal native-blind physical model produces transferable sequence-specific preorganization beyond its matched nulls under the frozen protocol.

It would **not** establish:

- de novo protein folding in general;
- a new force or physical law;
- superiority to established all-atom or coarse-grained force fields;
- novelty relative to the protein-folding literature;
- resurrection of v9, Patch-630, or TPO entropy.

## Frozen target family

Primary target set:

1. **1VII** — Villin headpiece, 36 residues; alpha-rich historical target.
2. **1L2Y** — Trp-cage, 20 residues; compact fast-folding miniprotein.
3. **1UAO** — chignolin, 10 residues; beta-hairpin miniprotein.

1VII must use the already pinned P5 source artifact.

1L2Y and 1UAO must use the exact historical full-PDB objects already bound in the P1 provenance record:

- 1L2Y full PDB SHA-256: `5d1bbb545a312dfff1ae1e64b6d8addecb2f561ddc4011aeb5bee9d1dfcd4438`
- 1UAO full PDB SHA-256: `e827fae677f8e96d1320688694b3db96bcc73050f81c6f842efc2e0ce9937e1e`

No fresh PDB substitution is permitted after implementation begins. If either exact historical full-PDB object cannot be recovered, P6 stops at the input-binding gate and must be explicitly redesigned before any result exposure.

1CRN is excluded from the primary family because its disulfide topology would make a minimal non-disulfide model an avoidable confound.

## Representation

P6 uses an **idealized canonical peptide geometry**, not target-PDB bond lengths, bond angles, omega torsions, native fragments, or native local geometry.

The target PDB contributes only:

- amino-acid sequence / residue identity;
- post-hoc native evaluation coordinates.

The initial peptide frame is fixed and target-independent.

Only phi/psi torsions are optimized.

Canonical covalent constants and any proline-specific handling must be committed and tested before prospective measurement.

## Native-information firewall

The optimization objective may not consume:

- native coordinates;
- native contact maps;
- native RMSD;
- native radius of gyration;
- native phi/psi;
- native secondary structure;
- native fragments;
- target-PDB bond lengths or bond angles;
- any target-specific parameter fitted using the native structure.

Native information is evaluation-only after each trajectory has been generated.

A contract test must demonstrate objective/gradient invariance when the stored native evaluator coordinates are rigidly shifted or replaced.

## Common physical scaffold

Every arm receives the same:

1. exact canonical covalent geometry through the torsion-space kinematic representation;
2. excluded-volume sterics;
3. a residue-independent local Ramachandran prior;
4. a native-blind directional backbone hydrogen-bond term built only from reconstructed backbone/virtual peptide atoms.

These terms are identical across all experimental arms.

## Sequence-dependent physical terms

The real-sequence arm adds only transparent, conventional native-blind residue interactions:

1. residue-class hydrophobic attraction derived from a frozen published/standard residue classification or frozen hydrophobicity scale;
2. screened Debye-Huckel electrostatics from residue formal/acid-base charge rules at the frozen pH and ionic strength.

No pair parameter may depend on native proximity.

The exact constants, residue classes, pH, ionic strength, dielectric treatment, cutoffs, and switching functions are frozen before measurement.

## Experimental arms

For every target/seed, all arms begin from exactly the same deterministic random phi/psi state.

### 1. `physical_real_sequence`

Common scaffold + sequence-dependent hydrophobic and electrostatic terms using the real amino-acid order.

### 2. `physical_shuffled_sequence`

Identical physics, but amino-acid order is replaced by one deterministic composition-preserving shuffle frozen per target before any outcome is exposed.

The shuffle must:

- preserve exact residue composition;
- differ from the real sequence;
- be reused for every seed of that target;
- be committed in the source manifest before measurement.

### 3. `generic_collapse`

Common scaffold + a sequence-independent nonlocal attraction.

For each matched target/seed, its **initial torsional gradient L2 norm** is scaled once to equal the initial gradient norm contributed by the real-sequence nonlocal hydrophobic/electrostatic terms. The scale is then frozen for the trajectory.

This control tests whether any apparent improvement is merely generic compaction at comparable initial force scale.

## Seeds and optimization

Seeds: `0,1,2,3,4,5`.

For each target/seed:

- deterministic CPU float64 PyTorch;
- identical initial phi/psi for all three arms;
- fixed optimizer and learning rate;
- fixed step budget;
- no early stopping using native information;
- no target-specific hyperparameters;
- no seed removal after exposure.

The implementation commit must freeze optimizer, learning rate, and step count before the authoritative measurement workflow is enabled.

## Primary endpoint

### Fixed-budget long-range native-contact precision

At the final frozen optimization step:

1. consider all C-alpha residue pairs with sequence separation >= 4;
2. rank those pairs by modeled C-alpha distance;
3. take the closest `K = max(1, floor(N/2))` pairs;
4. define a native contact as a corresponding native-evaluator C-alpha distance < 8.0 A;
5. primary score = fraction of those K predicted pairs that are native contacts.

This top-K precision fixes the number of predicted contacts and prevents gross over-collapse from earning a high score merely by putting almost every residue pair inside a contact cutoff.

No best-over-trajectory native metric is used as the primary endpoint.

## Anti-collapse sanity gate

For the real-sequence arm, the final C-alpha radius of gyration divided by native-evaluator radius of gyration must have target-wise median in the interval:

`[0.75, 1.25]`

for each of 1VII, 1L2Y, and 1UAO.

Native Rg is evaluation-only and never affects the trajectory.

## Secondary endpoints

Reported but unable to rescue a failed primary gate:

- final corrected Kabsch C-alpha RMSD;
- native-contact recall;
- top-K precision at fixed intermediate checkpoints;
- final Rg and Rg ratio;
- native torsion circular RMSE;
- hydrogen-bond count;
- hydrophobic-contact count;
- energy-component trajectories;
- maximum covalent length/angle drift;
- numerical-health status.

## Statistics

There are 18 matched target/seed observations.

Primary paired comparisons:

1. `physical_real_sequence - generic_collapse` precision;
2. `physical_real_sequence - physical_shuffled_sequence` precision.

Because higher precision is better, favorable deltas are positive.

Use exact two-sided paired sign-flip tests over all `2^18` sign assignments and Holm-adjust the two p-values.

## GO rule

Return:

`GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION`

only if **all** conditions are true:

1. `physical_real_sequence` has the highest pooled mean primary precision of all three arms;
2. real-sequence mean primary precision is greater than generic-collapse mean on **each** of 1VII, 1L2Y, and 1UAO;
3. real-sequence mean primary precision is greater than shuffled-sequence mean on **each** target;
4. Holm-adjusted exact paired p < 0.05 versus generic collapse;
5. Holm-adjusted exact paired p < 0.05 versus shuffled sequence;
6. real-sequence target-wise median final Rg/native-Rg lies in `[0.75,1.25]` for every target;
7. every run preserves canonical covalent geometry to maximum bond-length and bond-angle drift < `1e-8` in float64 reconstruction;
8. every run passes finite-value/numerical-health checks;
9. the native-information firewall tests pass on the exact implementation used for measurement.

Otherwise return:

`NO_GO_SEQUENCE_SPECIFIC_PHYSICAL_PREORGANIZATION`.

## Post-exposure rule

After the first authoritative result is exposed:

- no coefficient search;
- no target substitution;
- no seed removal;
- no alternate primary metric;
- no endpoint rescue;
- no target-specific physics;
- no sequence-shuffle replacement.

A NO-GO closes this minimal P6 model.

A GO authorizes only a new external-validation gate against additional held-out proteins and established baselines; it does not by itself justify a broad custom folding engine.
