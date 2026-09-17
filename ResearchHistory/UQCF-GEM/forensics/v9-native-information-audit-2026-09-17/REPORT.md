# Protein P0 — Frozen v9 Native-Information / Source-Provenance Audit

**Audit date:** 2026-09-17  
**Audit base:** `f596583615a823a33170588dcbf998bf13f10453`  
**Branch:** `research/protein-p0-v9-native-information-audit`  
**Primary status:** `CANONICAL_V9_GENERATOR_PROVENANCE_UNRESOLVED`

## Executive finding

P0 now has two distinct provenance results that must not be conflated.

1. The exact April 2026 generator that produced the canonical frozen-v9 packet is still not present in the audited Git repository history and has not been bound to an immutable historical source snapshot.
2. A later executable file, `uqcf_bridge_to_classical_handoff_repro.py`, was recovered from the ChatGPT Library and source-audited. It implements the documented v9 bridge observables, coefficients and handoff protocol, and its energy/gradient path is native-geometry blind at fixed chain length.

Therefore the old broad statement `EXECUTABLE_V9_SOURCE_NOT_PINNED` is superseded by the narrower result:

```text
CANONICAL_V9_GENERATOR_PROVENANCE_UNRESOLVED
```

while the recovered implementation receives the separate result:

```text
V9_REPRODUCTION_SOURCE_RECOVERED_AND_AUDITED
```

The empirical v9 packet remains `PRESERVED_BOUNDED`.

## Historical repository provenance

The canonical v9 update packet first appears at:

```text
commit  8269075e2e66c4fc335c38074900488f20b4cf8c
message v9 protein folding
date    2026-04-12T05:17:31Z
parent  8ed8a291bdb4ee4b9f3b86bd5243d8e0cc35502a
tree    28d28b6259e62c0528877074ac96df3a5ec1af2c
```

That commit adds the v9 memo and two summary CSVs, not executable generator source. The recursive Git tree at the exact packet state was complete (`truncated:false`) and did not contain an executable v9 protein generator. The immediate follow-on `4feac2650ceca1b439adb74381849f1e61862d4e` adds telemetry/results but no generator. The closeout commit `e2bc578b5e486d99881aed948b036653a1d7c4a0` preserves equations and pseudocode but not the function definitions used by the original run.

Current/default-branch search, connected GitHub-wide symbol search, selected historical branches, releases and connected Drive did not recover the exact April generator. This remains an archive-relative provenance boundary, not evidence that the source never existed.

## Recovered executable reproduction

Recovered Library object:

```text
name       uqcf_bridge_to_classical_handoff_repro.py
file id    file_00000000ec7c71f590699bcfde9fcb4b
version    1
bytes      20403
sha256     697d773a8dec951dafbac9132a04da22e342dee52c2b70d62732c4be16778e51
```

The file identifies itself as a "UQCF-GEM bridge-to-classical handoff reproduction script" and as a compact auditable reproduction of the bridge-layer result. That wording is why this audit does not silently relabel it as the original April generator.

Python compilation and AST parsing pass.

## Source-level native-information audit

### Energy path

`baseline_energy(X, ctx)` uses current-conformation bond geometry, steric repulsion and radius of gyration. Its only `ctx` dependency is chain length `N`.

`bridge_observables(X, ctx)` constructs the v9 quantities from the current conformation plus index pairs derived from `N`:

- `dir_pen`
- `angle_var`
- `dihed_smooth`
- `R_micro`
- `soft_contacts`
- `density_var`
- `rg` / compactness
- `C_meso`
- `loop_compat`
- `sigma_bridge`
- `closure_ready`
- `false_closure`
- `compat_field`
- `dihedral_preserve`
- `productive_contact`

It does not read `ctx.target`, target angles, target dihedrals or native-contact identities.

`bridge_v9_energy` reproduces the documented v9 coefficient structure and does not directly read any target field.

Source adjudication for the recovered reproduction:

```text
native coordinates in energy/gradient path       NO
native RMSD in energy/gradient path              NO
native contact map in energy/gradient path       NO
native target angles/dihedrals in energy path    NO
target identity in energy path                   NO
target-derived chain length N                    YES
current candidate geometry X                     YES
```

### Independent substitution control

A direct dynamic control held candidate conformation `X` and `N=12` fixed while replacing the native target with an unrelated same-length geometry.

Result:

```text
energy 1                 37.74882507324219
energy 2                 37.74882507324219
energy exact equal       YES
energy abs difference    0.0
gradient exact equal     YES
gradient max abs diff    0.0
```

At the same time, native-relative evaluation quantities such as angle RMS, dihedral RMS and native-contact count changed. The control therefore discriminates the mechanism path from the evaluation path rather than merely failing to perturb the program.

Result:

```text
REPRODUCED_V9_ENERGY_AND_GRADIENT_NATIVE_GEOMETRY_INVARIANT_AT_FIXED_N
```

## Where native structure is used

`FoldContext` stores the native target, target angles, target dihedrals and a native-contact set. These are used for evaluation/reporting.

During optimization, RMSD to `ctx.target` is evaluated at trace points and is used to retain a `best_X` for reported summary metrics. It does not enter the energy, gradient or state update.

For the bridge-to-classical handoff, the state passed from v9 preconditioning to the classical relaxer is the final `bridge_end`, not the native-RMSD-selected best-v9 state. Therefore native RMSD does not select the handoff state.

The distinction is:

```text
reproduced dynamics / gradient: native-geometry blind at fixed N
native-relative scoring:        explicitly uses the native target
```

That is acceptable for an evaluation harness, but it must be stated when interpreting "best RMSD" results.

## Reproducibility defect found

The recovered script seeds Python `random` and NumPy for each displayed seed, but it does not call `torch.manual_seed(seed)` even though it uses `torch.randn` in initialization and `torch.randn_like` during optimization.

Thus the displayed seed does not fully determine a fresh-process run. This is a reproducibility defect, not evidence of native leakage.

A new frozen reproduction lineage must explicitly control the PyTorch RNG before any new P1 measurement is treated as authoritative.

## Historical regularizer-reduction evidence

The Library also contains a historical `uqcf_v9_control_matrix` packet comparing:

- baseline
- v9
- angle-only
- dihedral-only
- soft-contact-only
- `static_combo`, which uses the ingredients without `sigma_bridge` / closure compression.

Its stated question is whether frozen v9 can outperform simpler controls without the compressed multiscale bridge state. Results and traces are preserved. However, the generating Python/source has not yet been recovered, so this packet is historical evidence only; it is not yet a source-certified P1 gate.

## Current adjudication

```text
v9 empirical packet                         PRESERVED_BOUNDED
exact April generator in Git history        NOT RECOVERED
canonical generator provenance              UNRESOLVED
reproduction executable                     RECOVERED + HASHED
reproduction energy native leakage          NOT FOUND / SOURCE-CERTIFIED NEGATIVE
reproduction evaluation native dependence   YES
reproduction full RNG determinism            FAILS CURRENTLY
historical control-matrix packet             FOUND
historical control-matrix source             NOT FOUND
historical P1 gate                           NOT CERTIFIED
```

The machine-readable source audit is `REPRO_SOURCE_AUDIT.json`.

## Next scientific move

Do not discard v9, and do not rerun broad protein development.

The next work should proceed on two tracks:

1. continue provenance recovery for an original v9/control-matrix generator if one exists;
2. separately freeze the recovered reproduction as a **new explicitly identified lineage**, repair only the RNG determinism defect, and then run a preregistered P1 reduction test against angle-only, dihedral-only, soft-contact-only and static-combination controls.

That P1 result would test the recovered v9 mechanism on its own merits. It must not be retroactively presented as proof that the unrecovered April generator was identical.
