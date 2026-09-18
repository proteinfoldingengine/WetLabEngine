# Protein P7A — Early-backbone controller provenance / active-path gate

**Status:** `ACTIVE_CONTROLLER_CALLING_PATH_NOT_PROVEN_IN_SURVIVING_SNAPSHOT`

## Question

Before prospectively testing the remaining Phase-I observable/controller idea, can the surviving source establish which controller actually drove the strongest historical protein runs?

At the current source snapshot, **no**.

## Frozen source snapshot

Repository: `proteinfoldingengine/UQCF-GEM`  
Commit: `9e8172268b1feadc1fdbecfa6ca61239dccf21d7`

Controller source exists:

- `dag_engine.py` blob `4694cab56217202b8732cd2800f1bc3c60c589dc`;
- `physics_only_controller.py` blob `e576f9a66eada6ba8fa00ad4a99b15ce56757c7e`;
- separate `state_evaluator.py` blob `c444f067b94e32c1a5b3bfeeec90410b320a7901`.

The DAG source implements the Compaction -> LockIn transition based on Betti1 count and persistence, and changes the active force set after transition.

The physics-only source defines direct observable/timescale-driven actions such as contact ramping, hydrophobic boost, Rama relaxation and Rg-window enforcement.

## Snapshot-wide caller scan

Every surviving Python file in the snapshot was scanned for:

- `dag_engine`;
- `DagEngine`;
- `physics_only_controller`;
- `PhysicsOnlyController`;
- `update_and_get_params`;
- `evaluate_step(`.

The only matches were the controller/evaluator definitions themselves.

No surviving runner imports or calls `DagEngine` or `PhysicsOnlyController`.

## Surviving execution path

The snapshot's `Main.py` blob `c6032f6f6affaff0a4071e852dd85bb0e21ca7db` identifies itself as a **minimal, gate-free physics probe**.

It does not instantiate either controller.

The surviving orchestration drivers likewise launch `Main.py`:

- `experimental_suite_driver.py` -> `Main.py`;
- `invariant_calibration_driver.py` -> `Main.py`;
- `sweep_driver.py` -> `Main.py`.

The adjacent `qis_combined_probe.py` is also gate-free.

Therefore the public snapshot proves that the controller code **existed**, but not that it was on the active calling path of the surviving runs.

## Historical record boundary

Contemporaneous Phase-I documentation records topology-triggered phase changes and later milestones. That is useful evidence of historical intent and claimed execution, but it does not replace a source/config/raw-run calling path.

Accordingly:

```text
CONTROLLER SOFTWARE EXISTED:                YES
DAG MECHANIC IS SPECIFIED IN SOURCE:        YES
PHYSICS-ONLY CONTROLLER EXISTS:             YES
SURVIVING RUNNER CALLS DAG:                 NO
SURVIVING RUNNER CALLS PHYSICS-ONLY:        NO
HISTORICAL ACTIVE PATH CERTIFIED:           NO
```

## P7A decision

`ACTIVE_CONTROLLER_CALLING_PATH_NOT_PROVEN_IN_SURVIVING_SNAPSHOT`

This is **not** a NO-GO on the controller idea.

It is a provenance stop: P7B must not be presented as a replay until an earlier active runner/config or raw execution artifact establishes which mechanic was actually used.

## Next forensic target

Search the historical Drive/source archive for an earlier runner or raw log that provides at least one of:

1. an import/instantiation/call of `DagEngine` or the physics-only controller;
2. a force-policy trace showing the controller's emitted active parameters/actions;
3. a phase-transition log tied to exact source/config identity;
4. a historical config plus runner pair sufficient to reproduce the calling path.

If none can be recovered, a later constrained-backbone controller experiment may still be scientifically legitimate, but it must be labeled **new prospective architecture testing**, not recovery of a demonstrated historical mechanism.
