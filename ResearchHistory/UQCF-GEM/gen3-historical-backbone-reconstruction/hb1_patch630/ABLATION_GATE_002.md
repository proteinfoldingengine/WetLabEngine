# Gen3 HB1 — Patch 630 LockIn Component Ablation Gate 002

Date: 2026-09-16
Branch: `gen3-historical-backbone-reconstruction-v1`
Target: `1VII` Villin headpiece
Seed: 42
Steps: 5000
Baseline: reproduced Patch 630 run

## Experimental rule

Same pinned 1VII input, seed, 5000 steps, optimizer, historical source, and all force parameters as the reproduced baseline. The normal topology/DAG transition is preserved. Only the named LockIn-added mechanism is disabled in each quarantined run copy.

## Results

| Run | Final RMSD (A) | Final phi_RMS | gamma_bar | Betti1 | lifetime | phase |
|---|---:|---:|---:|---:|---:|---|
| Baseline | 10.1913 | 0.2226 | 3.0016 | 544 | 120 | LockIn |
| Contact springs OFF | 10.2674 | 0.4290 | 3.0016 | 546 | 120 | LockIn |
| Screened electrostatics OFF | 10.1900 | 0.2225 | 3.0016 | 544 | 120 | LockIn |
| Contacts + electrostatics OFF | 10.2661 | 0.4286 | 3.0016 | 546 | 120 | LockIn |
| Prior DAG/LockIn OFF control | 10.2661 | 0.4286 | 3.0016 | 546 | 120 | Compaction |

## Causal result

The angular-ordering improvement attributed broadly to the LockIn phase in Gate 001 is almost entirely attributable to **contact springs** in this replay.

Disabling contact springs while retaining the DAG transition reproduces essentially the same weakened state as suppressing LockIn altogether: phi_RMS rises from 0.2226 to about 0.429 and RMSD rises by about 0.076 A. Disabling both contacts and electrostatics yields the same final metrics as the prior DAG-off control to the displayed precision.

By contrast, disabling screened electrostatics alone leaves the trajectory/final state essentially unchanged: RMSD 10.1900 A and phi_RMS 0.2225 versus baseline 10.1913 A and 0.2226. Thus screened electrostatics is not a material driver of the reproduced Patch-630 angular-ordering effect under this target/seed/config.

## Mechanistic interpretation

For this reproduced 1VII run:

1. Ramachandran potential is inactive (Gate 001).
2. Torsional-incoherence penalty is inactive (Gate 001).
3. The topology/DAG controller matters because it activates LockIn at step 99.
4. Of the two newly active LockIn terms, contact springs carry essentially all of the measurable angular-ordering effect.
5. Screened electrostatics contributes negligibly at the final-state level tested here.

This sharply narrows the historical result. The engine is not demonstrating a causal Ramachandran or explicit torsional regularizer effect in this run. Instead, the strong phi_RMS improvement emerges when topology-triggered contact constraints are activated on the full N–CA–C coordinate model.

## Scientific caution

The contact term is not yet established as a novel protein-physics mechanism. The historical implementation forms springs from contacts that are already below the configured distance cutoff at each step and penalizes squared contact distances. This may act as an adaptive geometric compaction/constraint mechanism rather than sequence-specific native-contact physics. The result therefore requires conventional controls before any novelty claim.

## Next gate

Test whether the contact-spring effect contains information beyond generic geometric regularization:

1. replace historical contact springs with a matched generic distance/compaction regularizer;
2. freeze the contact set at the LockIn transition versus recomputing it dynamically;
3. randomize contact-pair identity while matching contact count/sequence-separation distribution;
4. repeat baseline/contact-off controls across multiple seeds;
5. only after those controls, transfer the surviving mechanism to Gen3 kinematic backbone coordinates.

No native-contact information or parameter retuning should be introduced.