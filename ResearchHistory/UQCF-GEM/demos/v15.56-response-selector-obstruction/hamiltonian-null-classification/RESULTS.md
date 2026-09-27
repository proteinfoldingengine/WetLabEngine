# v15.74 — Fixed Hamiltonian cancellation classification

Verdict: **HAMILTONIAN_NULL_KERNEL_LOCAL_ONLY_CONFIRMED**.

Within the fixed, state-independent Hamiltonian class, no nonzero interacting coefficient combination remained rotationally null across all hidden probes on the frozen ensemble. Each of the twelve states independently gave full interacting coefficient rank 54; stacking them preserved rank 54. The only nine null coefficients were the one-body generators. A scalar identity, excluded from the 63-column basis, would add one trivial null direction.

This is a rank in **Hamiltonian coefficient space**, not a claim of 54-dimensional retained rotational geometry. For one state the map has 243 rows (27 hidden probes times nine retained edge skew coordinates), with the same Hamiltonian coefficients shared across every probe. The retained edge rotation space for each probe remains nine-dimensional. v15.73's source/probe product-space rank and this source-classification rank answer different questions.

## Frozen scientific results

| Map | Rank at all three thresholds | Nullity |
| --- | --- | --- |
| Each state's full 63-column Q and E maps | 54 | 9 |
| Each state's two-body-only coefficient map | 27 | 0 |
| Each state's three-body-only coefficient map | 27 | 0 |
| Twelve-state stack, 54 interacting columns | 54 | 0 |
| Twelve-state stack, all 63 columns | 54 | 9 |
| Exceptional zero-Bloch control, all 63 columns | 27 | 36 |

The preregistration required full interacting rank only for the stack; per-state ranks were frozen diagnostics without an assumed outcome. All twelve individually reached rank 54. Their smallest interacting Q singular values ranged from 0.1894889574318586 to 0.6058052913100002. This supports the observed individual-state classification without upgrading it to a theorem about every state: the exceptional control explicitly disproves that unrestricted claim.

For the stacked maps:

- Q: smallest interacting singular value 2.1249800393093543; largest full-map singular value 46.930964884425855.
- E: smallest interacting singular value 10.323013804972906; largest full-map singular value 245.54298299286592.
- Q null-projector distance from the local coordinate projector: 8.561022125758971e-15.
- E null-projector distance: 7.963799826513878e-15.

All three relative rank cutoffs (1e-9, 1e-10, 1e-11) agreed. The retained moment operator B independently had rank 54, and the interacting null diagnostics contained zero-dimensional kernels for both Q and E.

## Exceptional control and numerical validity

At the preregistered zero-Bloch state, every weight-three Hamiltonian source column had exactly zero Q/E, despite the full-rank weight-three one-body leakage map. Its 36-dimensional null space comprised the nine local and 27 weight-three directions, as predicted. This preserves the earlier lesson that nonzero retained leakage need not be rotationally visible at a particular state.

Adding the frozen Bloch perturbation made the explicit XXX/YXX source/probe control visible: Q norm 0.07999999999999999 against .08, E norm 0.9999999999999992 against 1. This checks the one-body subtraction in connected correlations, rather than relying solely on generic rank output.

All numerical controls passed:

- Direct versus adjoint commutator moment disagreement, imaginary moments, tangent trace and Hermiticity errors: exactly zero.
- Local retained, Q and E columns: exactly zero.
- Centered source derivative versus sinc identity: 1.8207437135502e-17.
- Unitarity residual: 6.280369834735101e-16.
- Coherent source assembly discrepancy: Q 4.440892098500626e-16; E 2.6645352591003757e-15.
- Maximum Sylvester residual: 1.4802072481531892e-14.
- Minimum density eigenvalue: 0.038338205425993845.
- Minimum retained correlation singular value: 0.02086104354176698.

## Analytic result and interpretation

DERIVATION.md, frozen before measurement, proves that a fixed Hermitian generator which is rotationally null for every hidden tangent throughout a nonempty full-dimensional open set of regular physical states must contain only one-body terms plus identity. The proof varies the polar frames and Bloch vectors independently within a physical neighborhood. A constant retained tangent cannot remain polar-symmetric throughout that neighborhood unless all its retained moments vanish. Pauli commutator identities then eliminate interacting generator coefficients. Independent review checked the derivation and implementation before the measurement was published.

The finite ensemble confirms that the twelve specified states already witness the corresponding Hamiltonian classification. The analytic theorem and finite numerical evidence remain distinct. Full-dimensional openness, state independence of H, all 27 hidden probes and regular positive-polar correlations are essential assumptions. No assertion is made for a restricted state manifold, a single special state, general dissipative source law, or arbitrary state-dependent generator.

The symmetric-null freedom is therefore removed by open-state robustness within this fixed Hamiltonian class. It is not removed by covariance, local positivity, or leakage alone. This selects no particular interaction, does not derive an interaction from Genesis Pin, and does not establish gravity or a source-induced change in admissible worlds. Source parameters remain ordered update labels; no fundamental time, external alignment, heuristic fit, or dark-matter primitive is introduced. Earlier counterexamples and historical verdicts remain intact.

The next bottleneck is whether the same robustness criterion extends to the wider class of affine operational source laws, including dissipative channels, and what it can constrain without selecting the physical source by hand.

## Exact execution and reproduction

Parent certified head: `71c4ece38c4d973884f15cebe104f895f0893671`.

Preregistration and absent-implementation tests: `7dbf286390b6f8e3944fe14e33cfc24cfa317c0c`.
[Expected RED run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36295653365): job `108553890001`, artifact `10922889653`, SHA-256 `a07aed47e2450a29d7ab0dd940c001af0060481f4ad82d89cbbf749785b133e0`. Setup succeeded; the sole error was the intended missing-implementation assertion. Downloaded archive, execution head and frozen source bytes verified.

Tested implementation: `33b9c0bf2476d3ef98c02437dcd96c29aff839cf`.
[GREEN run](https://github.com/proteinfoldingengine/WetLabEngine/actions/runs/36295841740): job `108554407443`, artifact `10923444636`, SHA-256 `668b4aef314d2fd0c87355af91e7f708e64dd8753ac50abd7e1bdaaf5c67c62d`. Four tests passed. The standalone result explicitly reports the scientific verdict and all_valid=true. Exact job log retrieved and inspected. Downloaded artifact hash, execution SHA, source byte identities and every SHA256SUMS entry verified. No intermediate implementation failure or criterion change occurred.

Raw result SHA-256: `fbcd985ef45fb06da82302a6995ad0866e156139f66f1c6d3df3de73a432206e`.
RESULT.json.gz SHA-256: `e5edd0e44e9c8dc0f60f40fb72420dc30b4a4a59e98db136a0679d45292c9f30`.
Git blob: `e25f30f2e40c4b03fdd69e1c4f8ff4fa3be6f584`.

RESULT.json.gz preserves the exact CI result, including the full retained operator B, all per-state Q/E maps, spectra, null-projectors and kernel diagnostics. Stack the stored maps in candidate order to reconstruct the stacked matrices. SUMMARY.json provides a readable reduction; EVIDENCE.json, TEST_LOG.txt and SHA256SUMS preserve execution metadata. Decompress with `gzip -dc RESULT.json.gz > result.json` and verify the raw digest.

Reproduce at the tested SHA using Python 3.11, numpy==2.3.5 and OPENBLAS_NUM_THREADS=1, following `.github/workflows/uqcf-hamiltonian-null-classification.yml`. Documentation is published in an additive later commit; the containing Git commit identifies that documentation head without circular self-hashing. No merge to main.
