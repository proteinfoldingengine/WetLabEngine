# Protein P7 — Source reduction of the recovered early DAG

**Gate:** P7B eligibility  
**Status before execution:** source-audit only; no prospective folding result exposed.

## Question

After recovering a real historical DAG calling path, does the strongest native-blind pre-Patch-630 controller still contain a genuinely distinct adaptive multi-force mechanism worth a new constrained-backbone campaign?

## Recovered source authority

Primary bundle: Drive `StableDAGPhysics`, created 2025-08-03.

The exact source is vendored under `recovered_stable_dag/` and hash-bound by `p7_source_reduction.py`.

The runner is Patch 602.4 and is native-blind in its force/controller path.

## Mechanical reduction

The recovered source has three named phases:

1. `Initial_Relaxation`
2. `Coherence_Growth_and_Compaction`
3. `Contact_Lock_In`

However, the actual control flow changes the interpretation.

### Phase 0 is skipped at step 0

The main loop initializes the derivative histories such that at the first step:

- `d2S_dt2 = 0`;
- `dgamma_dt = 0`;
- `dphi_rms_dt = 0`.

The source's `detect_thermodynamic_stall` therefore returns true immediately.

Because `dag_engine.update_phase(...)` is called **before** the active parameters are copied and before the force loss is evaluated, the DAG advances to `Coherence_Growth_and_Compaction` at step 0. The `Initial_Relaxation` force set governs zero optimizer steps.

### The fractal funnel is not a coordinate force in this source

`apply_fractal_compaction_funnel(coords, ...)` never loads the `coords` argument. It consumes a detached scalar Df value from `metrics` and returns an energy offset.

Therefore its activation does not create a coordinate gradient.

This is a source fact, not a judgment about whether a differentiable fractal potential could be designed.

### The only later adaptive coordinate-force addition is contact springs

After the step-0 transition, phase 1 has:

- gamma surge;
- angular torque;
- Lennard-Jones repulsion;
- fractal energy offset;
- entropy pulse.

Phase 2 contains the same set plus:

- contact springs.

Thus the remaining state-responsive force switch in the recovered native-blind controller is a gate controlling when current-state contact springs are added.

## Relation to already-tested Patch-630 mechanics

The exact Patch-630 line also gates current-state contact springs during LockIn.

That later mechanism has already been causally reduced:

- Rama term inactive in the reproduced historical run;
- torsional penalty inactive;
- electrostatics negligible;
- contact springs account for essentially all of the LockIn angular-order effect.

The first held-out 1CRN test then returned `NO TRANSFER`; frozen contacts were worse than contacts OFF in 8/8 paired seeds, and dynamic contacts were worse on average.

The contact formula is not byte-identical between Patch 602.4 and Patch 630, and the gate condition differs. But the remaining adaptive mechanism class is the same scientific question: **state-triggered activation of a current-contact collapse restraint**.

## Other historical controller candidates

### Patch 505.1

A complete contemporaneous source bundle is preserved, but it is not an admissible native-blind authority for P7B:

- its DAG schema contains gates using `rmsd` and `contact_match`;
- it includes `native_contact_forces`;
- the preserved `Main.py` supplies only a subset of the later DAG metrics and contains explicitly omitted force-method sections.

It is useful lineage evidence, not a clean physics-only candidate.

### Patch 606

The historical folder contains a DAG and force field, but the archived `main.py` materializes byte-identically to `force_field.py` and contains force-field source rather than a runner. The active path cannot be reconstructed by guessing.

### Physics-only controller

No historical caller has been recovered. It remains source-only.

## P7B eligibility decision

If the executable audit confirms the reduction above, a new P7B folding campaign would no longer test a distinct early multi-force controller. It would test whether another contact-activation gate can rescue a mechanism class that already failed held-out transfer.

That is outside the corrected P6 authorization and would be post-hoc rescue rather than efficient mechanism discrimination.

The preregistered source-audit verdict is therefore:

`NO_DISTINCT_MULTIFORCE_ADAPTIVE_CONTROLLER_AFTER_SOURCE_REDUCTION`

if and only if the exact-source checks all pass.

No protein-performance result is required to adjudicate this source-level eligibility gate.
