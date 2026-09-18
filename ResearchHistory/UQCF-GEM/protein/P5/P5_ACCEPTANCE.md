# Protein P5 — Constrained-Backbone TPO Survival Gate

**Status:** preregistered before prospective measurement.

## Question

Does the historical torsional-preorganization (TPO) entropy signal add reproducible folding-relevant information after the invalid Patch-630 Cartesian representation is replaced by a covalently constrained peptide-backbone representation?

This is **not** a Patch-630 replay. P4 closed the historical representation as physically invalid. P5 is prospective.

## Frozen representation

Use the previously certified PharmaApp Gate-9B `kinematic_pdb` representation:

- source PDB N/Cα/C bond lengths are fixed;
- source PDB backbone bond angles are fixed;
- source peptide ω torsions are fixed;
- only φ/ψ are optimized;
- reconstruction is differentiable;
- PDB native coordinates are evaluation references only after matched randomized φ/ψ starts are generated.

The source PDB supplies local covalent geometry and target identity. Native coordinates, native contacts and native φ/ψ do **not** enter any optimization energy.

## Targets

1. **1VII** Villin headpiece, 36 residues — historical target.
2. **1CRN** crambin, 46 residues — held-out transfer target already used as the first negative Patch-630 transfer discriminator.

Pinned source artifacts are committed before measurement.

## Matched initial states

Seeds: `0,1,2,3,4,5,6,7`.

For each target/seed:

- extract fixed source covalent geometry;
- keep source ω values fixed;
- set movable φ[1:] and ψ to the same deterministic Uniform(-π,π) draw for every mode;
- use identical initial state across all modes;
- use float64 CPU deterministic PyTorch.

No seed is removed because of outcome.

## Common native-blind base energy

Every mode receives the same:

- excluded-volume Cα repulsion;
- the controlled Gen3 dynamic Cα contact term (`k_contact=0.05`, 8 Å cutoff, sequence separation >=3);
- standard screened Debye-Hückel electrostatics at pH 7.0, ionic strength 0.15 M and scale 1.0.

No native contact map, native RMSD, native torsion target or native-derived force is permitted.

## Torsional terms

Historical TPO entropy is the recovered differentiable 18x18 soft φ/ψ histogram Shannon entropy used by `stage1_discovery_engine.py`.

The conventional Ramachandran control is periodic squared distance to the nearer of canonical alpha and beta basin centers.

A simple torsion-variance control measures circular dispersion of φ and ψ and contains no residue identity or native target.

### Gradient matching

To avoid deciding the test by arbitrary energy units, every non-baseline torsional regularizer is scaled **once at the initial matched state** so its torsional-gradient L2 norm equals 0.5 times the common-base torsional-gradient norm for that target/seed. If the common-base norm is below 1e-8, use target norm 1.0.

For the combined Rama+TPO mode, construct the equally weighted sum of individually normalized Rama and entropy terms and rescale the combined initial torsional gradient to the same target norm.

The scale is frozen for the full trajectory. No live renormalization is allowed.

## Modes

1. `baseline` — common base only.
2. `rama` — common base + gradient-matched Ramachandran prior.
3. `variance` — common base + gradient-matched simple torsion-dispersion control.
4. `entropy` — common base + gradient-matched historical TPO entropy.
5. `rama_entropy` — common base + equal-information Rama/TPO combination, total initial torsional-gradient matched to the same target norm.

Secondary diagnostic only:

6. `entropy_historical_0p02` — common base + the recovered Stage-1 entropy coefficient `k_torsion_entropy=0.02`. This arm is reported for historical scale context but is excluded from every GO/NO-GO condition and multiplicity family because its force scale is not information-matched.

## Optimization

- optimizer: Adam;
- learning rate: 0.03 rad;
- steps: 120;
- φ/ψ wrapped to [-π,π] after each update;
- no early stopping based on native metrics;
- no coefficient/seed/target changes after result exposure.

## Evaluation

Native geometry is used only post hoc.

### Primary endpoint

`best_ca_rmsd_A`: minimum corrected Kabsch Cα RMSD observed from initial state through step 120.

### Secondary endpoints

- final Cα RMSD;
- best/final native-contact recovery;
- final native φ/ψ circular RMSE;
- final Rg;
- maximum bond-length drift;
- maximum bond-angle drift;
- optimizer/finite-state health.

Secondary endpoints cannot rescue a failed primary gate.

## Statistics

For each primary comparison, use the 16 matched target/seed differences:

`rama_entropy best RMSD - control best RMSD`.

Primary comparisons:

1. `rama_entropy` versus `rama`;
2. `rama_entropy` versus `variance`.

Compute exact two-sided paired sign-flip p-values over all 2^16 sign assignments and Holm-adjust across the two comparisons.

## GO rule

Return `GO_TPO_ENTROPY_SURVIVES_CONSTRAINED_BACKBONE` only if **all** are true:

1. `rama_entropy` has the lowest pooled mean best Cα RMSD of all five modes;
2. `rama_entropy` has lower mean best RMSD than `rama` on **both** 1VII and 1CRN;
3. `rama_entropy` has lower mean best RMSD than `variance` on **both** 1VII and 1CRN;
4. Holm-adjusted exact paired p < 0.05 versus `rama`;
5. Holm-adjusted exact paired p < 0.05 versus `variance`;
6. every run preserves the source covalent manifold to maximum bond-length and bond-angle drift < 1e-8 in float64 reconstruction;
7. no run fails numerical-health checks.

Otherwise return:

`NO_GO_TPO_ENTROPY_INCREMENT`.

## Interpretation boundary

A GO would show only that the recovered TPO entropy observable adds a reproducible effect beyond the specified conventional controls under this constrained protocol. It would **not** by itself establish novelty, general protein folding, or a new physical law.

A NO-GO closes TPO-entropy-specific continuation on the present scientific case. The kinematic representation and measurement infrastructure may still be retained independently.
