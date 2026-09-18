# Protein P5 — Authoritative constrained-backbone TPO survival result

**Decision:** `NO_GO_TPO_ENTROPY_INCREMENT`

**Certified scientific head:** `8adfdc161645c32a8ae7f2bcacbdb3fd78b32780`  
**Pre-exposure contract certification:** GitHub Actions run `35294941990` — SUCCESS on `c65e7aa06fe06048dd8d5499539e51c0a5dd3b44`  
**Authoritative measurement:** GitHub Actions run `35295009294` — SUCCESS  
**Artifact:** `10528211747`, `protein-p5-authoritative-measurement`  
**Artifact SHA-256:** `cf64c0ea1e7356c72898b60c76e6910639bf6c70cb35ee041d5ded8951663e6b`

## What was tested

P5 prospectively tested whether the recovered historical torsional-preorganization (TPO) entropy term adds folding-relevant information after the invalid Patch-630 Cartesian representation is replaced by the previously certified covalently constrained `kinematic_pdb` representation.

The gate was frozen before result exposure:

- targets: 1VII and held-out 1CRN;
- seeds: 0..7;
- matched deterministic random phi/psi starts across modes;
- fixed source bond lengths, bond angles and omega;
- phi/psi-only optimization;
- native-blind objective;
- float64 deterministic CPU execution;
- 120 Adam steps at learning rate 0.03;
- gradient-matched torsional controls;
- exact paired sign-flip tests with Holm correction.

Before measurement, P5 was corrected to use the literal recovered Stage-1 entropy definition: histogram bounds `[-3.14159,+3.14159]`, normalization epsilon `1e-8`, and the historical interior-residue phi/psi projection. No outcome had been exposed before that correction.

## Pooled primary result

Mean best corrected Kabsch C-alpha RMSD across the 16 target/seed pairs:

| mode | pooled mean best RMSD (A) |
|---|---:|
| variance | 7.958500 |
| rama | 8.122549 |
| baseline | 8.178262 |
| rama_entropy | 8.229326 |
| entropy | 8.324414 |

The historical fixed-coefficient entropy diagnostic, excluded from the GO/NO-GO family by preregistration, had pooled mean best RMSD `8.192942 A`.

The preregistered candidate `rama_entropy` was therefore not the lowest pooled primary mode.

## Primary matched comparisons

### rama_entropy versus rama

- pooled mean delta, candidate minus control: **+0.106777 A**;
- candidate wins: **3/16**;
- exact two-sided sign-flip p: **0.634765625**;
- Holm-adjusted p: **0.634765625**;
- 1VII mean delta: **+0.203474 A**;
- 1CRN mean delta: **+0.010080 A**.

### rama_entropy versus variance

- pooled mean delta, candidate minus control: **+0.270826 A**;
- candidate wins: **4/16**;
- exact two-sided sign-flip p: **0.103515625**;
- Holm-adjusted p: **0.20703125**;
- 1VII mean delta: **+0.165338 A**;
- 1CRN mean delta: **+0.376314 A**.

Positive deltas are worse for the TPO candidate.

## Target means

For 1VII:

- rama: 7.104692 A;
- variance: 7.142829 A;
- rama_entropy: 7.308166 A;
- entropy: 7.333522 A;
- baseline: 7.442384 A.

For held-out 1CRN:

- variance: 8.774171 A;
- baseline: 8.914140 A;
- rama: 9.140405 A;
- rama_entropy: 9.150485 A;
- entropy: 9.315306 A.

Thus the TPO candidate failed the target-wise direction requirement against both preregistered controls on both proteins.

## Physical and numerical controls

The constrained representation behaved as intended:

- every run satisfied the covalent-geometry drift requirement;
- maximum observed bond-length drift was on the order of `10^-15 A`;
- maximum observed bond-angle drift was on the order of `10^-15 rad`;
- no numerical run failed;
- native geometry was not used in the optimization objective.

Therefore the scientific NO-GO is not caused by failure of the physical-backbone representation.

## Independent verification

The downloaded artifact ZIP SHA-256 exactly matched the GitHub Actions artifact digest.

All six per-file SHA-256 values in `SHA256SUMS.txt` independently matched their archive members.

The pooled means, target-wise deltas, exact 2^16 sign-flip p-values, Holm correction and every acceptance predicate were independently recomputed from `p5_results.csv` and matched the machine-generated acceptance packet.

## Scientific consequence

P5 does **not** support continuing the recovered TPO entropy term as a distinct protein-folding mechanism on the present evidence.

The entropy term did not add value beyond the conventional controls after peptide geometry was made physically valid. On the held-out target it was directionally worse than both the variance control and the baseline, and the combined Rama+entropy candidate was worse than both preregistered controls.

This closes **TPO-entropy-specific continuation** under the frozen P5 protocol.

It does **not** invalidate the kinematic peptide representation, corrected RMSD implementation, provenance work, or the general usefulness of a physically constrained backbone test harness.

## Claim boundary

This is a scoped prospective NO-GO, not a theorem that torsional information can never help protein folding. It says the recovered historical TPO entropy observable did not earn incremental scientific continuation under the preregistered constrained-backbone test.

No post-exposure retuning, seed removal, target rescue, coefficient search or alternate endpoint is authorized as a response to this result.
