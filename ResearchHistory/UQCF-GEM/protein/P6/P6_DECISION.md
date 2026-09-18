# Protein P6 — Corrected scientific continuation decision

**Assessment date:** 2026-09-17  
**Program status:** `NO_GO_TESTED_MECHANISMS_BROADER_EARLY_BACKBONE_LINE_OPEN`  
**Retention status:** `GO_RETAIN_KINEMATIC_BACKBONE_AND_VALIDATION_INFRASTRUCTURE`

## Corrected decision

P6 closes the specific historical mechanisms that have actually been subjected to certified falsification. It does **not** close every distinct mechanism in the earlier backbone program.

The correct conclusion is:

> The v9 hierarchy, Patch-630 physical-backbone interpretation, Patch-630 contact-graph generalization, and recovered TPO-entropy mechanism have not earned further mechanism-specific development. The earlier Phase-I observable-driven controller architecture remains a distinct, incompletely tested scientific line.

The prior P6 wording was too broad because it treated failure of those tested mechanisms as if it exhausted the earlier Phase-I topology/DAG controller.

## Mechanisms now closed on present evidence

### v9 live hierarchy

P1: `NO_GO_HIERARCHICAL_ADVANTAGE`.

The live state-dependent hierarchy was not required to obtain the observed compact-model behavior and did not beat the simpler frozen/information-matched controls under the preregistered gate.

### Patch-630 physical interpretation

P4: `NO_GO_HISTORICAL_PHYSICAL_BACKBONE_INTERPRETATION`.

The recovered representation did not preserve peptide C-N connectivity and had no covalent enforcement capable of repairing it. Its reproduced low phi dispersion therefore remains a numerical result, not evidence of physical peptide-backbone organization.

### Patch-630 contact-graph transfer

Held-out 1CRN Gate 005: `NO TRANSFER`.

The frozen Villin contact graph was worse than contacts OFF in 8/8 held-out matched seeds. The dynamic contact condition was also worse on average.

### TPO as an independent predictor

The certified 1QYS audit found no independent torsional-preorganization signal after controlling for initial geometry/topology:

- adjusted torsion entropy rho = +0.02387, p = 0.45086;
- adjusted torsion basin-distance rho = +0.00471, p = 0.88184.

### TPO entropy on a physically valid backbone

P5: `NO_GO_TPO_ENTROPY_INCREMENT`.

On the certified kinematic peptide backbone, the preregistered Rama+entropy candidate was worse than both Rama and simple torsion-variance controls on both 1VII and held-out 1CRN. Covalent and numerical controls passed, so the negative result is not an artifact of broken peptide geometry.

## What remains scientifically open

The forensic reconstruction shows a mechanically distinct earlier Phase-I architecture:

```text
structure observables
    -> controller state/action
    -> physical-force policy
    -> new structure
    -> new observables
```

The strongest surviving source-level candidates are:

1. **topology/DAG phase control** — state-driven Compaction -> LockIn switching based on Betti1 threshold and persistence;
2. **observable-driven force activation** — topology changes which physical terms are active rather than merely being logged;
3. **adjacent physics-only feedback controller** — online Rg, phi dispersion, coherence and Betti-lifetime behavior can emit force-policy actions such as contact ramps, hydrophobic boosts, Rama relaxation and Rg-window enforcement.

These mechanics are not equivalent to TPO entropy and are not equivalent to the later CA-only QIS production solver.

They have **not yet received the same prospective constrained-backbone survival test as P5**.

## Important execution uncertainty

The surviving source proves that the Phase-I DAG/controller mechanics existed. It does not yet prove which exact controller path was active in each strongest historical protein result.

That calling-path question must be resolved before a prospective mechanism test.

The adjacent `physics_only_controller.py` must not be silently treated as historically active merely because it exists in the same source snapshot.

## Evidence deliberately excluded from promotion

### Gate 004

The historical 1VII multi-seed table remains excluded from acceptance-grade evidence because a later preregistration records the corresponding raw artifacts as absent/unverified.

### Seed 965

The historical 1VII Seed-965 TPO narrative remains Class C until its raw candidate table, exact preregistration artifact, Phase-B trajectory and summary log are recovered and pinned.

Those claims cannot override P5 and do not certify a separate Phase-I controller effect.

## What P6 therefore authorizes

P6 authorizes **one more bounded mechanism-discrimination program** directed only at the genuinely distinct Phase-I observable/controller line.

It does **not** authorize:

- v9 coefficient tuning;
- Patch-630 contact-graph rescue;
- TPO entropy variants;
- Seed-965 rescue by parameter search;
- broad custom-force expansion;
- combining all historical features into a synthetic engine and calling it a replay.

## Next gate

`P7 — EARLY_BACKBONE_CONTROLLER_SURVIVAL`

P7 should proceed in two stages.

### P7A — controller provenance / active-path gate

Before running science:

1. identify the exact Phase-I controller source and configuration for the strongest historical cases;
2. determine whether DAG phase switching, the physics-only controller, or another path was actually invoked;
3. freeze source/config/calling-path provenance;
4. stop rather than guess if active-path provenance cannot be established.

### P7B — physically constrained survival test

Only for a controller mechanic that passes P7A:

1. transplant the controller's **meaning**, not its broken Cartesian representation, onto the certified kinematic peptide backbone;
2. preserve the same native-blind force/controller inputs;
3. compare dynamic observable-driven switching against matched static and schedule controls;
4. use matched seeds and at least one held-out protein;
5. freeze the endpoint/statistics before exposure;
6. prohibit target-specific rescue or post-exposure retuning.

A GO would establish only that the controller architecture contributes reproducible information beyond matched static scheduling under the tested constrained protocol. Novelty would remain a separate question.

A NO-GO would justify closing the remaining historical mechanism line.

## Current program ledger

```text
HISTORICAL NUMERICAL WORK:              PRESERVE
KINEMATIC / VALIDATION TOOLING:         RETAIN

V9-SPECIFIC MECHANISM:                  NO-GO
PATCH-630 PHYSICAL INTERPRETATION:      NO-GO
PATCH-630 CONTACT-GRAPH TRANSFER:        NO-GO
TPO INDEPENDENT PREDICTOR CLAIM:        NOT SUPPORTED
TPO CONSTRAINED-BACKBONE INCREMENT:     NO-GO

PHASE-I OBSERVABLE/DAG CONTROLLER:       OPEN — NOT YET PROSPECTIVELY TESTED
PHYSICS-ONLY FEEDBACK CONTROLLER:        OPEN SOURCE CANDIDATE; ACTIVE PATH UNPROVEN
BROADER EARLY-BACKBONE LINE:             OPEN PENDING P7
```

## Decision boundary

The scientifically efficient next action is **not** another rescue of a failed mechanism.

It is a final bounded test of the genuinely distinct early observable/controller architecture. If that surviving mechanism also fails physical representation and held-out discrimination, the historical custom protein-mechanism program can then be closed on substantially stronger grounds.
