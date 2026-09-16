# Gen3 HB1 — Gate 004 Multi-Seed Preregistration

Date: 2026-09-16
Target: 1VII Villin headpiece
Purpose: test whether the Gate-003 graph-constraint effect survives across seeds without seed selection.

## Frozen design before runs

Seeds: **11, 23, 42, 57, 73, 101, 137, 211**.

Each seed will run the same five conditions for 5,000 steps:

1. historical dynamic contacts;
2. contacts OFF;
3. frozen contact graph captured at LockIn;
4. randomized matched graph (contact count and sequence-separation distribution matched, pair identity randomized without native information);
5. matched generic compaction regularizer.

All conditions retain the pinned 1VII input, full N-CA-C historical representation, optimizer, learning rates, force constants, topology trigger, and all non-contact mechanics. No seed will be removed because of outcome. Failed runs will remain in the denominator and be reported separately.

## Primary endpoint

Final `phi_RMS` at step 5000.

Primary contrast: frozen graph vs contacts OFF.

Secondary contrasts: dynamic vs contacts OFF; randomized vs contacts OFF; generic compaction vs contacts OFF; frozen vs generic compaction; dynamic vs frozen.

## Secondary endpoints

Final C-alpha RMSD, LockIn transition step, Betti1 count/lifetime, and trajectory-level phi_RMS difference after LockIn.

## Analysis rule

Report every seed, mean/median, paired per-seed differences, and dispersion. Do not select the best seed or tune parameters after seeing results. This gate is exploratory-mechanistic, not a native-fold accuracy claim.

## Decision rule

Advance the graph-constraint hypothesis to a held-out protein only if frozen contacts improve phi_RMS over contacts OFF in a clear majority of paired seeds and the aggregate effect is not explained equally well by the matched generic-compaction control. Otherwise classify the Patch-630 effect as seed-specific or generic regularization and do not promote it into Gen3 physics.
