# Protein P6 — Scientific continuation decision

**Assessment date:** 2026-09-17  
**Program decision:** `NO_GO_CONTINUE_HISTORICAL_CUSTOM_PROTEIN_MECHANISM_DEVELOPMENT`  
**Retention decision:** `GO_RETAIN_KINEMATIC_BACKBONE_AND_VALIDATION_INFRASTRUCTURE`

## Decision question

After reconstructing, auditing, reducing and prospectively retesting the original protein-backbone/TPO work, is there enough surviving evidence of a distinct, physically valid and transferable mechanism to justify continued custom-engine development?

**No, on the present evidence.**

This is a cost-benefit and scientific-evidence decision about the historical mechanism line. It is not a theorem that custom protein physics can never be useful.

## Evidence chain

### 1. v9 did not earn mechanism-specific continuation

P1 returned:

`NO_GO_HIERARCHICAL_ADVANTAGE`.

The live v9 hierarchy was not the best pooled method, was slightly worse than the frozen gate on both targets, and failed both preregistered significance comparisons. The result supports geometry-based regularization as a phenomenon but not the live v9 gate as a distinct mechanism.

### 2. The Patch-630 contact-graph effect did not transfer

The first held-out 1CRN gate completed 40/40 runs without target-specific retuning.

The primary final-phi-RMS means were:

- contacts OFF: 0.436367;
- generic compaction: 0.443913;
- randomized graph: 0.483164;
- frozen graph: 0.491758;
- dynamic contacts: 0.513597.

The frozen graph was worse than contacts OFF in **8/8** matched seeds.

Verdict:

`NO TRANSFER`.

This blocks promotion of the Villin contact-graph effect as a general protein-backbone mechanism.

### 3. Historical TPO was not an independent predictor in the recovered 1QYS population

The certified HB2 audit used 1000 rows.

Raw torsional correlations with final RMSD were small. After residualizing against initial radius of gyration and Betti1:

- torsion entropy: rho = **+0.02387**, p = **0.45086**;
- torsion basin-distance metric: rho = **+0.00471**, p = **0.88184**.

The adjusted evidence does not support an independent TPO signal beyond the stronger initial geometry/topology variables in that recovered dataset.

### 4. Patch 630 was not a physically connected peptide backbone

P4 returned:

`NO_GO_HISTORICAL_PHYSICAL_BACKBONE_INTERPRETATION`.

The exact recovered source declares a 1.33-A peptide C-N distance, but the seed-42 initializer produced:

- 0/35 peptide C-N links within 0.1 A of 1.33 A;
- minimum peptide C-N distance 2.3873 A;
- mean peptide C-N distance 3.5476 A;
- maximum 7.2501 A.

The historical objective had no covalent N/CA/C enforcement capable of repairing that representation.

Therefore the reproduced historical phi-dispersion collapse remains a valid computation but cannot be promoted as physical peptide-backbone organization.

### 5. The TPO idea did not survive a valid constrained backbone

P5 replaced the invalid representation with the certified kinematic peptide backbone, froze source bond lengths/angles/omega, optimized only phi/psi, used native-blind objectives, matched starts and force scales, and included held-out 1CRN.

P5 returned:

`NO_GO_TPO_ENTROPY_INCREMENT`.

Pooled mean best C-alpha RMSD:

| mode | mean best RMSD (A) |
|---|---:|
| variance | 7.958500 |
| rama | 8.122549 |
| baseline | 8.178262 |
| rama_entropy | 8.229326 |
| entropy | 8.324414 |

The preregistered Rama+entropy candidate was worse than both controls on **both** targets:

- versus Rama: +0.203474 A on 1VII, +0.010080 A on 1CRN;
- versus variance: +0.165338 A on 1VII, +0.376314 A on 1CRN.

Neither Holm-adjusted comparison approached the frozen p<0.05 requirement.

All covalent-geometry and numerical-health controls passed, so the negative result is not explained by backbone failure.

## Evidence deliberately not used to rescue the program

### Gate 004

The historical 1VII multi-seed table is not used as acceptance evidence because the later preregistration explicitly records its raw run artifacts as absent/unverified.

The held-out 1CRN failure is independently sufficient to block promotion of the contact-graph mechanism.

### Seed 965

The historical narrative records:

- 1VII Seed 965 TPO Index 0.69;
- predicted final RMSD 6.5-8.5 A;
- reported final RMSD 8.90 A;
- reported final Rg 7.27 A.

The forensic evidence index classifies these as authority **C** because the raw candidate table, exact timestamped preregistration artifact, Phase-B trajectory and summary log were not recovered/pinned.

Those claims remain historically interesting, but they are not allowed to override the prospective P5 result.

Recovery of the raw Seed-965 packet would still be valuable for historical reconstruction. By itself it would not justify a rescue campaign unless it exposed a genuinely different mechanism that P5 did not test.

## Overall adjudication

The original backbone work **did contain real executable ideas worth auditing**:

- full N/CA/C representation;
- true phi/psi measurement;
- topology-triggered contact logic;
- torsional-organization observables;
- target-blind seeded experiments;
- a useful instinct to separate initial-state foldability from downstream relaxation.

That historical value is now documented.

But the load-bearing mechanism claims did not survive the sequence of falsifiers:

1. hierarchy reduction;
2. held-out transfer;
3. geometry/topology adjustment;
4. physical peptide-integrity audit;
5. prospective constrained-backbone comparison against ordinary controls.

There is therefore no current scientific basis for further spending on historical-engine-specific coefficient tuning, contact-graph rescue, TPO entropy variants, v9 gate refinements, or broad custom force-field expansion.

## What should be retained

Keep and maintain:

- the certified `kinematic_pdb` representation;
- canonical residue identity handling;
- corrected Kabsch RMSD;
- native-blind matched-seed measurement harnesses;
- provenance/source manifests;
- exact RED/GREEN and CI certification patterns;
- recovered historical source and evidence ledgers;
- negative results and raw artifacts.

These are useful research infrastructure even though the historical mechanism line is closed.

## Reopen rule

Do **not** reopen the historical mechanism line because a new coefficient, seed or target looks promising.

A scientifically legitimate restart requires at least one of:

1. recovery of new raw historical evidence that exposes a materially different, previously untested mechanism;
2. a new independently motivated physical hypothesis with a preregistered held-out consequence;
3. external evidence that identifies a specific missing mechanism not represented in the frozen controls.

Any restart must begin as a new hypothesis branch, not as post-hoc tuning of Patch 630, TPO, v9, or the failed contact graph.

## Final program verdict

```text
HISTORICAL NUMERICAL WORK:          PRESERVE
KINEMATIC / VALIDATION TOOLING:     RETAIN
V9-SPECIFIC MECHANISM:              NO-GO
PATCH-630 PHYSICAL INTERPRETATION:  NO-GO
PATCH-630 CONTACT-GRAPH TRANSFER:    NO-GO
TPO INDEPENDENT PREDICTOR CLAIM:    NOT SUPPORTED
TPO CONSTRAINED-BACKBONE INCREMENT: NO-GO
OPEN-ENDED HISTORICAL ENGINE WORK:  NO-GO
```

The scientifically efficient next action is preservation and closeout, not another rescue experiment.
