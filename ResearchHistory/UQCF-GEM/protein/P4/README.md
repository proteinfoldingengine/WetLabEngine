# Protein P4 — Patch-630 physical-backbone validity gate

**Decision:** `NO_GO_HISTORICAL_PHYSICAL_BACKBONE_INTERPRETATION`

HB1 already established that the August-5 Patch-630 computation numerically reproduces the historical scalar endpoint. P4 asks the more basic question: did that computation evolve a covalently valid peptide backbone such that its phi/psi ordering can be interpreted as physical protein-backbone organization?

The exact recovered source says no.

## Load-bearing source facts

The historical initializer declares N-Cα=1.46 Å, Cα-C=1.53 Å, peptide C-N=1.33 Å, Cα-C-N=2.03 rad and N-Cα-C=1.94 rad. On the exact 36-residue seed-42 initializer:

- all 35 Cα-Cα steps are 3.8 Å to numerical precision;
- all 34 interior N-Cα and Cα-C distances match their declared values;
- **0/35 peptide C(i)-N(i+1) links are within 0.1 Å of the declared 1.33 Å value**;
- the closest peptide C-N link is 2.3873 Å, already 1.0573 Å away;
- peptide C-N links range 2.3873–7.2501 Å, mean 3.5476 Å;
- only 1/35 Cα-C-N angles is within 0.1 rad of the declared 2.03 rad target.

The source assigns `C_N_dist = 1.33` but never reads that variable afterward.

`ProteinModel` registers N, Cα and C as independent trainable arrays. `ForceField.calculate_total_force_loss` does not receive N or C coordinates; `main.py` passes only `ca_coords` plus phi/psi and other scalar/state inputs. No covalent-bond/peptide-bond/bond-length force exists in the recovered force field.

Therefore the historical computation does not enforce the peptide chain whose torsions are being interpreted.

## Claim boundary

This closes only the **historical physical-backbone interpretation**. It does not erase the HB1 numerical reproduction and does not reject prospective torsional/full-backbone work implemented on a covalently constrained or kinematic peptide representation.

## Next gate

`P5 — CONSTRAINED_BACKBONE_SURVIVAL`: move only the bounded surviving candidate mechanics onto a peptide-geometry-preserving representation and test them prospectively against matched conventional controls. Historical Patch-630 performance numbers do not transfer automatically.
