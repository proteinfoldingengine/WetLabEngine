# Protein P7A — Early-backbone controller provenance / active-path gate

**Current status:** `DAG_ACTIVE_CALLING_PATH_RECOVERED_SOURCE_LEVEL`  
**Raw Patch-622/624 execution log:** not recovered  
**Physics-only controller active path:** not established

## Supersession note

The first P7A pass inspected only the surviving public Git snapshot and correctly found no live controller caller there. Historical Google Drive recovery has now located multiple earlier source bundles in which the DAG is explicitly on the execution path. This report supersedes the earlier public-snapshot-only stop while preserving it as a provenance fact about the later Git snapshot.

## Primary recovered controller authority — StableDAGPhysics

Historical Drive parent:

- folder: `StableDAGPhysics`
- Drive ID: `1alYQEh5KnVcZa3CBcRIuRb-OV3NmhT8D`
- created: 2025-08-03

The folder preserves a coherent ten-file source bundle. All ten Python files compile.

| File | Drive ID | SHA-256 |
|---|---|---|
| main.py | `1QwVl_edsXIKMRyV-apbROE7eykPRjpJ3` | `71500484969c5e67db0f106f1417be57274c9a5eb71e886df98e55a4b918c6be` |
| dag_engine.py | `1R_DEUaADHyENA4DQO-NqvutEHlL_NdMJ` | `32dd940a4d81d1b718f040cb9944e13586792928fbc869260b8120e0fb69d92d` |
| force_field.py | `1TmTA8WR_GtGuMAsyI6ecZvdloHkUdVKM` | `2d13e3b00dada665724a41ce3a9acc1eb69f2389cbdf465bd9eefa53936ba44e` |
| physics_metrics.py | `1kpaDHStaawxOJo71_e9f7VnkgG8dCUM4` | `fc5df19386b8db3dad73cf0574b13062138e0f4e2175583da46d23e27923826d` |
| protein_model.py | `15Ds1ghA22bpZFSEcsmDkjFzoZYK0RT-T` | `f4fbf4f66d97ffd864e0c42d20934d4a599570c9e0319938b4694e7cae1e93bf` |
| physics_constants.py | `1GTLnE1USuKgn696CTODLagW3j_c69lCo` | `1a5aa4ecea48e755f190e797d5c625053dde1dd8627bb52ebf9d088634c858ee` |
| fractal_dimension_utils.py | `1aQBkvbT5DqVhevSYDqjMbIOl0K03SBuv` | `06641d4dff2b86ba1093e2e626130cbab0dfe1691e007dbf5d43e0d795025fca` |
| physics_purity_auditor.py | `1jkvhCBhdXTrt7QYaAuoiaOX34I7-zg-J` | `c35895598f48e6757b0f155e02e3d2f4c53f69c36dd8936b1d2eaa468f406764` |
| metrics_history.py | `1GPNszRRXslwj7YsGTMg1HHYfBaWcJMMZ` | `74fcf97044ddb3217a240277f5fdce0f4ce60d884683e65e8a83b15a6312792e` |
| chart_utils.py | `1K2bii5FC25nIZPQ9faS44owmLaeu6spA` | `d1dbcec0a144a0ef330ba92d42bf27c95d8a2910c8098e938b89de62f4086b18` |

The runner identifies itself as `Patch 602.4`, target 1UBQ, seed 42, 2000 steps.

## Active calling path — established

The recovered `main.py`:

1. imports `DagEngine, DAG_SCHEMA, _dag_force_mapping`;
2. instantiates `DagEngine(DAG_SCHEMA, GLOBAL_CONSTANTS, _dag_force_mapping)`;
3. calculates state observables each step;
4. calls `dag_engine.update_phase(metrics_for_physics, step)`;
5. copies `dag_engine.active_params`;
6. passes those active parameters directly into `ForceField.calculate_total_force_loss(...)`;
7. logs the current phase and whether contact/entropy terms are active.

This is not dead controller source. The DAG sits on the coordinate-update path.

## Recovered three-stage DAG

### Phase 0 — Initial_Relaxation

Active:

- angular torque locking;
- Lennard-Jones repulsion;
- gamma surge.

Exit is state-driven from coherence/torsional dynamics or thermodynamic stall.

### Phase 1 — Coherence_Growth_and_Compaction

Adds:

- fractal compaction funnel;
- entropy pulse.

The transition logic uses topological stability, torsional flatness and entropy curvature.

### Phase 2 — Contact_Lock_In

Adds:

- contact springs.

The final-state criterion combines coherence, Betti stability, fractal dimension and thermodynamic freeze-out.

Thus the historically distinctive mechanism is broader than the Patch-630 contact graph alone:

```text
state observables
 -> phase transition
 -> change active force family
 -> new structure
 -> new observables
```

## Native-blindness of the recovered force/controller path

The runner calculates native-aligned RMSD for diagnostics. However:

- `dag_engine.py` contains no RMSD/native reference;
- `force_field.py` contains no RMSD/native reference;
- native coordinates are not passed into either module;
- the diagnostic `NATIVE_CONTACT_DISTANCE_THRESHOLD` is only a scalar threshold used to report current-state contact density, not a native contact map.

Therefore the recovered DAG/force path is native-blind even though RMSD is logged.

## Source caveats relevant to P7B

P7B must preserve these facts rather than silently fixing them:

1. the historical state is C-alpha only and its phi/psi are pseudo-dihedrals; this representation is not acceptable for the prospective physical test;
2. the historical fractal-dimension term receives a detached scalar Df value, so that term does not by itself create a coordinate gradient in this source;
3. gamma is a separate optimized scalar and participates in phase/control logic;
4. the entropy pulse, angular torque, LJ term and contact springs do have coordinate-gradient paths;
5. contact springs use a current-state contact graph, not a native contact map.

A prospective constrained-backbone port must test the controller architecture without falsely claiming that representation repair was part of the historical run.

## Additional historical corroboration

### FoldSuccess — July 24

Drive `MainSimulation` ID `10Wmc2UjuXBWGsasDay9CNnlvm2rZszqQzwFh5mS4Pew` explicitly imports and instantiates a DAG and logs current phase. Its matching DAG source is preserved in the same folder. This establishes an earlier DAG-wired lineage.

### StableFold Patch 505 — July 31

Drive folder `1fEoE4ew0CYC5KSf9Bq62cGV0sikyFMtu` preserves a complete, compilable source bundle with a DAG-wired `Main.py`.

The contemporaneous `StableFold` document reports decreasing RMSD, improving Df/contact behavior, increasing Betti1 and states that the DAG was intact. That is Class-C contemporaneous execution evidence; the referenced raw trajectory/report files have not been recovered.

### Phase-I scientific summary — August 5

Drive document `14V4iV-f3kSyVDmU6v-mC3-nwxOGAeD3MbMEEKWRO19w` records Patch 622.2 as a topology-triggered DAG phase change with evidence described as a “DAG log,” and Patch 624.x as stable molten-globule behavior with logs.

The underlying Patch-622/624 DAG log has not yet been recovered, so those outcome claims remain historical rather than Class-A evidence.

## Patch606 archive anomaly

Drive folder `StablePatch606LogsRMSD` contains a later DAG/force bundle, but its archived `main.py` materializes byte-identically to its `force_field.py` in the recovered copy and contains force-field code rather than the expected runner. P7A therefore does not use that file as calling-path authority.

This archival defect is preserved rather than repaired by inference.

## Physics-only controller boundary

The later `physics_only_controller.py` remains a separate source candidate. P7A has not recovered a historical runner that invokes it. It must not be folded into the recovered DAG mechanism.

## P7A adjudication

```text
DAG SOFTWARE EXISTED:                         YES
DAG ACTIVE RUNNER RECOVERED:                  YES
DAG ACTIVE PARAMS FEED FORCE LOSS:            YES
RECOVERED DAG/FORCE PATH NATIVE-BLIND:        YES
CONTEMPORANEOUS EXECUTION NARRATIVE:           YES
EXACT PATCH-622/624 RAW DAG LOG RECOVERED:     NO
PHYSICS-ONLY CONTROLLER ACTIVE PATH:           NOT PROVEN
```

**P7A result:** `DAG_ACTIVE_CALLING_PATH_RECOVERED_SOURCE_LEVEL`

## Consequence

P7B is scientifically legitimate as a **prospective survival test of the recovered historical DAG architecture** on the certified kinematic peptide representation.

P7B must not be described as reproducing the exact Patch-622/624 result unless the raw run/config/log is later recovered.

The prospective test must isolate whether state-responsive multi-force switching contributes information beyond matched static/nonadaptive controls. It must not reopen v9, TPO entropy, or the already-failed Patch-630 contact graph as standalone rescue mechanisms.
