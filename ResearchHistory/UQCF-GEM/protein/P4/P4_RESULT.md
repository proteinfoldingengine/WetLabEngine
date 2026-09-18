# Protein P4 — Authoritative Patch-630 physical-backbone validity result

**Decision:** `NO_GO_HISTORICAL_PHYSICAL_BACKBONE_INTERPRETATION`

**Certified scientific head:** `cd14868c6bb7865a4d6c13c0579a07b72581d60c`  
**GitHub Actions:** run `35292391335`, run #14 — SUCCESS  
**Artifact:** `10526897177`, `protein-p4-patch630-geometry-source-gate`  
**Artifact SHA-256:** `5ef741f80df8ad64d764a2db19177f7998d1c7199e38e10c35fde8ad676e6187`

## What was tested

P4 did not rerun or reinterpret the historical performance endpoint. HB1 already reproduced that numerical endpoint. P4 instead audited the exact recovered August-5 Patch-630 source and its seed-42 initializer against the geometry the source itself declares.

The source declares N-Cα = 1.46 Å, Cα-C = 1.53 Å and peptide C-N = 1.33 Å.

The certified audit finds:

- 34/34 interior N-Cα distances satisfy the declared N-Cα geometry;
- 34/34 interior Cα-C distances satisfy the declared Cα-C geometry;
- **0/35 peptide C(i)-N(i+1) distances are within 0.1 Å of 1.33 Å**;
- the closest peptide C-N link is 2.3873 Å;
- peptide C-N distances span 2.3873–7.2501 Å, mean 3.5476 Å;
- only 1/35 Cα-C-N(next) angles is within 0.1 rad of the source's declared 2.03-rad angle.

The source assigns `C_N_dist = 1.33`, but the variable is never consumed after declaration.

## Why optimization cannot repair the contract

The recovered `ProteinModel` treats N, Cα and C coordinates as independent trainable coordinate arrays. But the recovered force-field entry point does not receive N or C coordinate arrays. `main.py` passes Cα as the force coordinates and uses N/C only to calculate φ/ψ observables.

No explicit covalent-bond, peptide-bond or bond-length enforcement function exists in the recovered force field.

Thus Patch 630 did not represent an evolving covalently connected peptide backbone whose φ/ψ values could automatically be interpreted as physical protein torsions.

## What remains true

HB1's historical numerical reproduction remains valid as a computation:

- historical RMSD endpoint reproduced at approximately 10.1913 Å;
- historical `phi_rms` field reproduced at approximately 0.2226;
- the historical full N/Cα/C coordinate path was genuinely executed.

P4 changes the scientific interpretation, not those numerical facts.

## Scientific consequence

The historical low φ dispersion cannot be promoted as evidence of physically valid backbone organization. The original Patch-630 representation fails the physical geometry prerequisite before novelty or folding performance is considered.

This is therefore a **NO-GO for the historical representation**, not a NO-GO for the broader idea that torsional/full-backbone mechanics might matter.

## Next gate — P5

`P5 — CONSTRAINED_BACKBONE_SURVIVAL`

Any surviving historical idea must now be tested prospectively on a representation that preserves peptide covalent geometry by construction. Historical Patch-630 scores do not transfer to P5.

P5 should use:

- fixed/kinematic peptide geometry;
- native-blind optimization;
- corrected Kabsch RMSD only as post-hoc evaluation;
- matched random starts/seeds;
- conventional torsion/geometry controls;
- at least one held-out protein;
- no target-specific rescue or retuning after exposure.

If the effect disappears under a valid peptide representation or reduces to ordinary geometric regularization, the backbone-mechanism line becomes a scientific NO-GO.
