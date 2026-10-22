# Protein P9 — Transferable Coherence / Handoff-State Falsifier

**Status:** preregistered before P9 implementation and before any P9 native-evaluation outcome is exposed.

## Why this is the final protein question

P1, P5, P6 and P8B remain valid scoped NO-GOs. P9 does not reopen their frozen implementations.

The only surviving question with enough scientific value to justify another protein experiment is whether the frozen v9 multiscale coherence compression can serve as a **native-blind handoff-state / future-realizability coordinate** on a physically valid peptide backbone.

This is deliberately narrower than claiming a new folding force or a new law of coherence.

Prior art already establishes:
- energy landscapes/funnels and structural reaction coordinates;
- local and nonlocal folding order;
- committor-based reaction coordinates;
- non-Markovian/memory effects after coarse-graining;
- history-augmented state models.

Therefore P9 can earn continuation only if the **specific frozen v9 hierarchical compression** transfers to the valid-backbone setting and predicts downstream ordinary relaxation better than simpler flattened versions using the same information.

If it does not, the WetLabEngine protein program should close on the present evidence.

## Candidate quantity

P9 does not use v9 as an optimization force.

At each sampled C-alpha conformation, compute the exact P1/v9 native-blind observables:

- local: `dir_pen`, `angle_var`, `dihed_smooth`;
- mesoscopic: `soft_contacts`, `density_var`, compactness;
- nonlocal: `loop_compat`.

Define, with the frozen v9 coefficients,

```
R_micro = exp(-(0.60*dir_pen + 0.20*angle_var + 0.26*dihed_smooth))
C_meso  = sigmoid(1.8*(soft_contacts-0.40) - 0.42*density_var + 0.8*compactness)

flat_primary   = 0.36*R_micro + 0.24*C_meso + 0.40*loop_compat
flat_secondary = 0.32*R_micro + 0.20*C_meso + 0.48*loop_compat

sigma_bridge  = sigmoid(6*(flat_primary - 0.45))
closure_ready = sigma_bridge * flat_secondary
```

`closure_ready` is the candidate score.

The two flattened scores are the primary information-matched controls. They contain the same three compressed ingredients but remove the hierarchical gating/product.

## Representation and targets

Use the validated P6 target-independent canonical N-Cα-C peptide geometry:
- fixed canonical bond lengths and bond angles;
- trans omega;
- phi/psi structural degrees of freedom;
- deterministic CPU float64 PyTorch.

Targets:
- 1VII
- 1L2Y
- 1UAO
- 1CRN

1CRN is loaded from the already pinned P5 input and adapted to the P6 canonical representation. Its native coordinates are evaluation-only.

Seeds: `0..5`.

## Native-blind state generator

For every target/seed:
- initialize with the frozen P6 deterministic torsion initializer;
- evolve with the P6 `physical_real_sequence` objective only;
- Adam learning rate `0.02`;
- generate through 200 optimizer steps;
- snapshot completed steps `50, 100, 150, 200`.

The v9 candidate score is diagnostic only and may not change the generator.

## Common downstream handoff

From each frozen checkpoint:
- clone the phi/psi state;
- reset optimizer state;
- use the same P6 `physical_real_sequence` objective;
- Adam learning rate `0.02`;
- run 100 additional steps;
- no v9 force, no topology gate, no native-information early stopping.

This asks whether the current native-blind coherence score identifies states that are better starting points for ordinary downstream relaxation.

## Primary outcome

For each checkpoint state, record the **best corrected Kabsch C-alpha RMSD** reached during the common 100-step handoff.

For ranking, define:

`future_quality = -best_handoff_ca_rmsd_A`

so larger is better.

RMSD is evaluation-only and may not enter generation, scoring or handoff dynamics.

## Primary analysis

For every target/checkpoint group there are six matched seed states.

For each score:
- `closure_ready` candidate;
- `flat_primary` control;
- `flat_secondary` control;

compute Spearman rank correlation with `future_quality` across the six seeds.

This yields 16 group correlations per score (4 targets x 4 checkpoints).

Primary comparisons:
1. candidate minus `flat_primary`;
2. candidate minus `flat_secondary`.

Use exact two-sided paired sign-flip tests over the 16 group-level correlation differences and Holm-adjust the two p-values.

## GO rule

Return `GO_TRANSFERABLE_COHERENCE_HANDOFF_COORDINATE` only if all are true:

1. mean candidate group Spearman correlation is at least `0.35`;
2. candidate mean correlation exceeds both flattened controls;
3. candidate mean correlation is positive for every target when averaged across its four checkpoints;
4. candidate-minus-control mean correlation is positive for every target for both controls;
5. both Holm-adjusted exact paired p-values are < `0.05`;
6. all generator and handoff runs preserve canonical covalent geometry to max drift < `1e-8`;
7. all runs are numerically healthy;
8. native-information firewall passes;
9. the implemented v9 score reproduces the frozen P1 formulas to tolerance `1e-12`.

Otherwise return `NO_GO_TRANSFERABLE_COHERENCE_HANDOFF_COORDINATE`.

## Secondary diagnostics

Report but do not allow them to rescue a failed primary gate:
- final and best handoff top-K native-contact precision;
- contact recall;
- Rg/native-Rg;
- per-target and per-checkpoint correlations for all raw v9 observables;
- P6 energy components at checkpoint and handoff endpoint;
- candidate score distributions;
- ranking ties;
- initial-to-handoff RMSD change.

## Interpretation boundary

A GO would establish only that the frozen v9 hierarchical multiscale compression is a compact transferable predictor of downstream handoff quality on this benchmark, beyond two simpler flattened same-information controls.

It would not establish:
- a new fundamental force;
- a new folding law;
- solved de novo folding;
- that protein dynamics require an ontologically new memory state;
- superiority to modern folding methods;
- novelty over the full reaction-coordinate literature.

A NO-GO closes the remaining v9/coherence-specific protein continuation path on the present evidence. Do not rescue it by changing coefficients, score formulas, targets, seeds, checkpoints, handoff budget, primary endpoint or GO thresholds after exposure.
