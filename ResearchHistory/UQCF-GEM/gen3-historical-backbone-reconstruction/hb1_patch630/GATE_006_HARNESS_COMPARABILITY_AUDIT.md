# Gen3 HB1 — Gate 006 Harness Comparability Audit

Date: 2026-09-16
Purpose: determine whether the positive 1VII Gate-004 result and negative held-out 1CRN Gate-005 result are directly comparable before closing the historical contact-graph mechanism.

## Audit question

Could the apparent target dependence be an artifact of different experimental harnesses rather than protein identity/sequence?

## Dimensions checked

| Dimension | 1VII Gate 004 | 1CRN Gate 005 | Comparable? |
|---|---|---|---|
| Historical engine lineage | recovered Patch-630 full N-CA-C | same recovered Patch-630 full N-CA-C | yes |
| Initialization | seeded random coil | seeded random coil | yes |
| Seeds | 11,23,42,57,73,101,137,211 | same | yes |
| Steps | 5000 | 5000 | yes |
| Optimizer / learning rates | historical frozen settings | same | yes |
| Topology/DAG trigger | historical trigger retained | same | yes |
| Contact cutoff | 7.5 A | same | yes |
| Minimum sequence separation | >=3 | same | yes |
| Conditions | dynamic/OFF/frozen/randomized/generic | same five | yes |
| Primary endpoint | final phi_RMS | final phi_RMS | yes |
| Native contacts supplied | no | no | yes |
| Native coordinates in objective | no for contact mechanism | no | yes for mechanism test |
| Target-specific retuning | none within panel | none | yes |
| Sequence | 1VII, 36 aa | 1CRN, 46 aa | intentionally different |
| Native-coordinate RMSD reporting | available in earlier 1VII replay context | not computed in Gate 005 batch | no, but not relevant to primary endpoint |

## Important implementation distinction

Gate 005 deliberately uses the target sequence to generate the historical random coil and does not feed native 1CRN coordinates into the contact mechanism or optimization objective. The external PDB is used to establish target identity and sequence provenance. This matches the mechanistic question being tested: whether the same topology/contact policy improves angular organization on a different sequence without native-contact information.

The primary comparison does not depend on native RMSD. Both gates use final `phi_RMS` as the endpoint, and the five post-LockIn mechanisms are defined identically.

## Audit conclusion

**COMPARABLE FOR THE PRIMARY MECHANISTIC CLAIM.**

No harness difference identified here can explain the sign reversal in the preregistered primary contrast:

- 1VII Gate 004: frozen graph improves phi_RMS versus contacts OFF in 8/8 seeds, mean difference about -0.202.
- 1CRN Gate 005: frozen graph worsens phi_RMS versus contacts OFF in 8/8 seeds, mean difference +0.05539.

The lack of native-coordinate RMSD in Gate 005 prevents a cross-target native-fold accuracy comparison, but it does not invalidate the angular-order transfer test. The observed reversal should therefore be treated as target/sequence dependence under the tested historical mechanics, not as a known harness artifact.

## Scientific disposition

The historical Patch-630 result should be preserved as:

1. a reproducible 1VII/Villin phenomenon;
2. a causally narrowed effect associated primarily with topology-triggered nonlocal contact constraints;
3. robust across the tested Villin seeds;
4. **not general across the first held-out protein tested without retuning**.

The contact-graph mechanism should not be promoted into Gen3 active physics and should not receive a target-specific rescue campaign on the present evidence.

## What remains scientifically worth preserving

This gate closes only the proposed **general contact-graph mechanism**. It does not erase the broader historical findings that motivated this reconstruction: full-backbone N-CA-C representation, true phi/psi measurement, TPO/torsional-preorganization observables, and the methodological lesson that backbone organization must be separated from native-fold accuracy.

Those elements may still be useful as measurement/control infrastructure in Gen3, but any new scientific hypothesis should begin from a fresh preregistered question rather than treating the Villin contact result as established general physics.
