# Gen3 HB1 — Gate 005 Held-Out 1CRN Transfer Preregistration

Date: 2026-09-16
Target: `1CRN` crambin (46 residues)
Held-out status: no `1CRN` occurrence found in UQCF-GEM or WetLabEngine project history before this gate.

## Purpose

Test whether the Patch-630 topology-conditioned nonlocal constraint-graph effect transfers beyond 1VII without target-specific retuning.

## Source and input rule

Use the recovered Patch-630 historical mechanics unchanged. The official 1CRN SEQRES is used to define the 46-residue sequence and seeded random-coil start. Native coordinates are not part of the force objective; therefore this gate's primary endpoint is angular organization only. Native-structure RMSD will not be used for the gate decision unless a separately pinned 1CRN coordinate fixture is available and verified.

## Seeds

`11, 23, 42, 57, 73, 101, 137, 211`

No seed may be removed because of outcome.

## Conditions

Each seed runs 5,000 steps under five conditions:

1. historical dynamic contacts;
2. contacts OFF;
3. contact graph frozen at first LockIn activation;
4. randomized matched graph preserving the frozen graph's sequence-separation histogram but randomizing pair identity without native information;
5. generic isotropic compaction control calibrated at first LockIn activation to the historical contact-loss scale, then held fixed.

All other mechanics, force constants, optimizer settings, topology thresholds, and learning rates remain unchanged.

## Primary endpoint

`phi_RMS` at historical step 4999 (the pre-update metric logged by the original runner).

Primary paired contrast: frozen graph versus contacts OFF.

Secondary paired contrasts: dynamic vs OFF; randomized vs OFF; generic vs OFF; frozen vs generic; dynamic vs frozen.

## Secondary endpoints

LockIn transition step, final Betti1 count, radius of gyration, gamma_bar, fixed/random graph pair count, and run failures.

## Decision rule

Transfer is supported only if frozen contacts improve phi_RMS over contacts OFF in a clear majority of paired seeds and the aggregate frozen effect is stronger than the generic-compaction control. If this criterion fails, do not promote the mechanism to Gen3 kinematic physics.

## Provenance correction

The previously committed Gate-004 multi-seed table lacks corresponding raw run artifacts in the current workspace and is treated as unverified until independently rerun. This Gate-005 experiment is executed from a new reproducible batch harness calibrated against the reproduced 1VII seed-42 baseline before any 1CRN result is exposed.