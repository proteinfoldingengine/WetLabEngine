# P1 — Authoritative v9 regularizer-reduction result

**Date:** 2026-09-17  
**Branch:** `research/protein-p1-v9-regularizer-reduction`  
**Authoritative measurement head:** `f38cce040c98b78f4300ace06f28c350e4e4c313`  
**GitHub Actions run:** `35288146185` / Protein P1 Acceptance Measurement #2  
**Artifact ID:** `10525307040`  
**Artifact SHA-256:** `424a11c975ec7c7d662d027294f3034a5d42d93e2c2b8d17e416f4373d54a9d2`

## Decision

```text
NO_GO_HIERARCHICAL_ADVANTAGE
```

Under the acceptance rule frozen before result exposure, the prospective P1 experiment does **not** establish a distinct advantage for the live hierarchical v9 gate over simpler information-matched regularizers.

This is a mechanism-discrimination NO-GO. It is not a claim that every geometry-based preconditioning effect is absent.

## Frozen protocol

The authoritative run used:

- historical loader-equivalent 1UAO input, 10 chain-A C-alpha atoms;
- historical loader-equivalent 1L2Y input, 20 chain-A C-alpha atoms;
- seeds 0 through 5;
- seven modes: baseline, angle-only, dihedral-only, soft-contact-only, static-combo, fixed-gate, v9;
- 180 preconditioning steps;
- the same 240-step baseline relaxer after handoff;
- Adam, learning rate 0.05;
- noise scale 0.013 with the frozen decay;
- identical initial states and Gaussian noise schedules across modes for a target/seed pair;
- optimizer reset at handoff;
- deterministic CPU PyTorch execution;
- fixed-gate constants frozen at exactly the recovered source precision: sigma = 0.1956, closure = 0.0393.

The native target geometry was excluded from all energies and gradients and used only for post-hoc evaluation.

## Primary endpoint

Primary metric: `post_best_rmsd`, the best Kabsch C-alpha RMSD reached during the common baseline relaxation.

Pooled means over 12 matched target/seed trials:

| Mode | Mean post-best RMSD |
|---|---:|
| angle_only | 4.3490916491 |
| baseline | 4.3521756132 |
| fixed_gate | 4.3722229997 |
| v9 | 4.3762910366 |
| soft_contact_only | 4.3779221376 |
| dihedral_only | 4.4225071867 |
| static_combo | 4.4401470025 |

v9 was therefore **not** the lowest pooled-mean method. It was 0.024115 Å worse than baseline and 0.027199 Å worse than angle-only on the frozen primary metric.

## Predeclared mechanism comparisons

### v9 versus static-combo

Across the 12 matched pairs:

- mean v9-minus-static delta: **-0.06385597 Å**;
- median delta: **-0.06698537 Å**;
- v9 lower RMSD in **9/12** pairs;
- 1UAO mean delta: **-0.11252014 Å**;
- 1L2Y mean delta: **-0.01519179 Å**;
- exact two-sided paired sign-flip p = **0.119140625**;
- Holm-adjusted p = **0.23828125**.

v9 moved in the favorable direction relative to static-combo on both proteins, but this did not satisfy the frozen statistical gate.

### v9 versus fixed-gate

Across the 12 matched pairs:

- mean v9-minus-fixed delta: **+0.00406804 Å**;
- median delta: **+0.00108600 Å**;
- v9 lower RMSD in **5/12** pairs;
- 1UAO mean delta: **+0.00659780 Å**;
- 1L2Y mean delta: **+0.00153828 Å**;
- exact two-sided paired sign-flip p = **0.60693359375**;
- Holm-adjusted p = **0.60693359375**.

The fixed-gate control was slightly better on average on both targets. The difference is tiny, but that is precisely the point of the reduction test: the data do not require the live state-dependent gate to obtain the observed behavior.

## Frozen gate evaluation

The predeclared GO conditions evaluated as:

```text
v9 lower pooled mean than every control      FAIL
v9 lower than static-combo on 1UAO           PASS
v9 lower than static-combo on 1L2Y           PASS
v9 lower than fixed-gate on 1UAO             FAIL
v9 lower than fixed-gate on 1L2Y             FAIL
v9 vs static Holm p < 0.05                    FAIL
v9 vs fixed Holm p < 0.05                     FAIL
```

Therefore the frozen decision is necessarily:

```text
NO_GO_HIERARCHICAL_ADVANTAGE
```

## Independent verification

After downloading the authoritative GitHub Actions artifact, the result was recomputed independently from `p1_results.csv` rather than trusting `p1_acceptance.json`.

The independent calculation reproduced exactly:

- all pooled means;
- both target-wise paired deltas;
- both 2^12 exact sign-flip p-values;
- Holm correction;
- all seven frozen Boolean acceptance predicates;
- the final NO-GO decision.

Every individual output file also matched the SHA-256 recorded by the workflow.

## Infrastructure history

The first authoritative attempt at head `a371a88362c57a252bb5e89f9502641bef449c46` completed the trajectory calculations but stopped while serializing sparse trace rows because the first trace row lacked an `energy` field. Hashing and artifact upload were skipped, so no authoritative result packet was exposed.

That defect was reproduced by a dedicated RED test and repaired by taking the union of trace CSV fields. No protein input, seed, force/energy term, coefficient, optimizer setting, noise schedule, endpoint, statistical test, or GO/NO-GO criterion was changed. The repaired contract passed 14/14 tests before run #2.

## Scientific interpretation

P1 narrows the earlier v9 interpretation substantially.

What survives:

1. The v9 geometry terms can alter trajectories.
2. The live v9 construction can outperform one deliberately ungated static-combo construction in this compact model.
3. Geometry-based regularization/preconditioning remains a legitimate phenomenon to study.

What P1 does **not** support:

1. that the live `sigma_bridge` / `closure_ready` hierarchy is necessary;
2. that it is superior to a frozen information-matched gate;
3. that v9 is the best-performing regularizer in the prospective matched experiment;
4. that these compact-model results establish a new folding law or protein-specific physical mechanism.

The strongest bounded conclusion is:

> The prospective matched-control experiment does not distinguish the live hierarchical v9 bridge from simpler geometric regularization strongly enough to justify continuing v9-specific mechanism development.

## Program consequence

P1 should now be closed as a scientific NO-GO for **hierarchical-v9-specific advantage**.

Do not spend additional work on:

- v9 coefficient tuning;
- live sigma/closure gate refinements;
- larger v9 parameter searches;
- attempts to rescue a special bridge-state interpretation using these same compact-model mechanics.

The next high-value protein question lies outside this v9 branch: return to the independently recovered older backbone/TPO lineage and test whether its torsional/full-backbone mechanics contain a signal that is not reducible to these compact regularizers.
