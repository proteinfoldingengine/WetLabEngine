# AI Reproduction and Extension Guide

**For:** future AI agents, human reviewers, and code-audit workflows  
**Companion files:** `README.md`, `SOURCE_MANIFEST.json`, `EVIDENCE_INDEX.md`

This guide is designed to prevent three common reconstruction failures:

1. treating historical prose as execution evidence;
2. combining mechanics from different eras into a synthetic engine and calling it historical;
3. confusing software existence, execution, reproducibility, physical validity, and novelty.

## 1. Required evidence order

Use this priority order when adjudicating a claim:

```text
raw run artifact / frozen output
    > executable source at exact commit/blob
    > configuration tied to that source/run
    > contemporaneous narrative document
    > later interpretation
```

When sources disagree, preserve the disagreement explicitly.

## 2. Clone and inspect exact history

Primary historical repository:

```bash
git clone https://github.com/proteinfoldingengine/UQCF-GEM.git
cd UQCF-GEM
```

Do not start on current `main` and assume it is the historical engine. Always inspect exact refs.

### Initial surviving multi-lineage snapshot

```bash
git show --stat 9e8172268b1feadc1fdbecfa6ca61239dccf21d7
git ls-tree -r 9e8172268b1feadc1fdbecfa6ca61239dccf21d7
```

Expected historically important paths include:

```text
dag_engine.py
physics_only_controller.py
protein_model.py
force_field.py
qis_combined_probe.py
Main.py
metrics_history.py
online_metrics_utils.py
```

### Destructive QIS transition

```bash
git show --stat 1dea70ca8864f80a909ee8a23d379608692e80b6
git show 1dea70ca8864f80a909ee8a23d379608692e80b6 -- dag_engine.py force_field.py diagnostics_registry.py
```

Confirm that the commit message is `RemoveQISEngine` and that QIS scheduling/terms and DAG material are removed.

## 3. Verify blob identity, not just filenames

A filename can survive while mechanics change. Use blob identity.

### Patch 630

```bash
git rev-parse 9e8172268b1feadc1fdbecfa6ca61239dccf21d7:protein_model.py
```

Expected:

```text
6bc1a564cff022cf533ad2b8de2c03a1aee21afe
```

The recovered PharmaApp QIS copy must resolve to the same blob if the direct-continuity claim is to hold.

### Phase-I DAG

```bash
git rev-parse 9e8172268b1feadc1fdbecfa6ca61239dccf21d7:dag_engine.py
```

Expected:

```text
4694cab56217202b8732cd2800f1bc3c60c589dc
```

### Physics-only controller

Expected blob:

```text
e576f9a66eada6ba8fa00ad4a99b15ce56757c7e
```

### Pre-removal QIS force field

Expected blob:

```text
5b5728f61a0572f9118f03b257eecf333342a51a
```

## 4. Reconstruct the mechanics statically before running anything

Create a table with one row per mechanic and one column per source state. At minimum verify:

- state representation: CA-only vs N/CA/C;
- learnable coordinate tensors;
- phi/psi calculation path;
- steric term;
- electrostatics;
- H-bond term;
- Ramachandran term;
- contact term;
- hydrophobic term;
- fractal/Rg compaction term;
- gamma/coherence term;
- torsion penalty;
- Betti1 measurement;
- topology as measurement vs topology as controller input;
- controller/phase transitions;
- optimizer type;
- whether native RMSD affects the objective;
- proposal moves and acceptance law.

Do not infer feature presence from a YAML key alone. Locate the executable call path.

## 5. Phase-I controller reproduction

At commit `9e817...`, inspect `dag_engine.py`.

Verify two named phases:

```text
Compaction
LockIn
```

Verify that the transition depends jointly on:

```text
betti1_count
betti1_lifetime
```

and that the active force set differs before and after transition.

Then inspect `physics_only_controller.py` separately. Do **not** merge it with the DAG and claim a historical combined controller unless a calling path proves both were active together.

For every historical run under review, answer:

```text
Which controller object was instantiated?
Which function was called each step?
Which action/parameter dictionary reached ForceField?
Which config values set the thresholds?
```

If any answer is missing, classify controller execution as unresolved.

## 6. Patch-630 representation reproduction

At the source-authority snapshot, inspect `protein_model.py` and verify:

```text
self.N_coords  = nn.Parameter(...)
self.CA_coords = nn.Parameter(...)
self.C_coords  = nn.Parameter(...)
```

Then locate the phi/psi implementation used by the runner and establish the chain:

```text
N/CA/C coordinates
    -> compute_true_phi_psi
    -> phi/psi tensors
    -> Ramachandran / torsional terms
    -> gradient
    -> optimizer step on N/CA/C
```

The important reproducibility question is not merely whether phi/psi are calculated. They must influence a differentiable loss if the claim is “angular physics drove the structure.”

### Patch-630 historical result recovery

High-priority raw result to locate:

```text
phi_RMS = 0.2215
RMSD = 10.19 A
```

The contemporaneous Google Doc records these numbers, but this package intentionally does not certify them until the raw run/config/trajectory is found.

Recovery procedure:

1. Search Drive and repository history for filenames mentioning `630`, the target protein, `phi_rms`, Ramachandran, and `10.19`.
2. Recover the exact config.
3. Recover the summary log and full timeseries.
4. Recover the trajectory/PDB frames if available.
5. Hash every artifact.
6. Confirm that the source revision used for the run contains the same Patch-630 representation.
7. Re-run without changing parameters.
8. Only then promote the result from Class C to Class A/reproduced.

## 7. TPO reproduction

### Static milestone A — metrics

Checkout:

```text
b11552a6c932b20f028ece5e5ff806862077bfde
```

Verify `torsional_metrics.py` blob:

```text
0aee35076a59805aa4f99897d7c662b943051ebe
```

Confirm:

- 2-D phi/psi histogram entropy;
- periodic angular-distance handling;
- alpha and beta basin centers.

### Static milestone B — optimization

Checkout:

```text
d019fe0fef858a4b73d3baaf3406df0447142cbe
```

Verify `stage1_discovery_engine.py` blob:

```text
c580a15c75e68816e1143d2a28f4485174cf4925
```

Confirm the differentiable soft histogram and weighted torsion-entropy term are added to the optimization potential.

### Seed identity rule

Never query or merge a “Seed 965” result without protein and campaign identity. Use at least:

```text
protein_id
campaign / phase
source commit or artifact set
seed
```

The 1VII Golden-Coil narrative and rows labeled seed 965 in later 1QYS/1PGB tables are not interchangeable.

### 1VII Golden-Coil artifact recovery target

Historical Google Doc claim:

```text
protein: 1VII
seed: 965
TPO index: 0.69
predicted final RMSD: 6.5-8.5 A
reported final RMSD: 8.90 A
predicted final Rg: 9.0-10.0 A
reported final Rg: 7.27 A
```

Required promotion evidence:

- candidate-selection table containing 1VII seed 965;
- TPO metrics used for selection;
- timestamped/pre-run prediction artifact;
- Phase-B config;
- raw timeseries;
- trajectory;
- final summary;
- exact source commit.

Without these, retain the result as historically recorded, not independently reproduced.

## 8. QIS combined-probe reproduction

Use source snapshot:

```text
9e8172268b1feadc1fdbecfa6ca61239dccf21d7
```

Verify:

- Patch-630 full-backbone blob is present;
- `Main.py` computes true phi/psi;
- the force field includes the classical terms;
- QIS entropy/coherence/topology blocks are active only when enabled;
- the per-step QIS scale is supplied through `dynamic_params`;
- the runner is “gate-free” relative to the earlier DAG controller.

The combined probe and Phase-I DAG should be treated as separate execution architectures unless a specific run proves integration.

## 9. Reproduce the 1UAO QIS-causality control first

Before making any positive QIS claim, recover these Drive artifacts:

```text
QIS OFF
file id: 1cQoWOAMIqSnQ8VgNRGcCZ7Aroz7-DY4j
final RMSD: 3.982 A
final Rg: 3.395 A

QIS ON
file id: 1cNVH5SCRnAwdraWI7ekZbIgQcdQtmt-p
final RMSD: 3.982 A
final Rg: 3.395 A
```

The summaries are identical at reported precision.

Minimum causal interpretation:

```text
QIS was not necessary to obtain the reported final state in this paired test.
```

Do not upgrade that to:

```text
QIS never matters
```

or:

```text
the initial state universally determines folding
```

without broader controlled evidence.

## 10. Executed production-QIS reproduction

Use the recovered PharmaApp provenance file first. It defines the source authority and warns that a later conflicting `qis_engine_production.py` became a jitter-only placeholder and is not the accepted execution authority.

Accepted source authority:

```text
commit: 1e88c1b5778e98eb2f5c1b0c0f019ba0801e1c38
engine blob: 2cb51ffc7b2edacee0e867a16a511b30847adbae
campaign driver blob: b7e7afa665ad2f29b6287403dfae9478f7e945ca
```

Corroborating run:

```text
artifact commit: 4d61823a0ce4dcc71f596893514b29d151fed435
stdout blob: ba779a7e54d9ee0167f8ab6c664d04050384e4d5
```

Verify that the run records:

```text
fragment_bridge
torsion_tweak
jitter
```

Then verify source mechanics:

- CA-only input/output;
- OpenMM harmonic CA bonds;
- generic weak nonbonded term;
- zero charges in the recovered source;
- FI feature calculation;
- RMSD calculation to native coordinates;
- early `J = RMSD` behavior;
- later `J = alpha*RMSD - beta*FI_z` behavior;
- Metropolis acceptance;
- cooling/reheating and checkpoint archive.

This is enough to classify the production system as a stochastic structural-search engine with information/topology scoring.

## 11. Rules for a “maximum-capability historical engine” reconstruction

A maximum-capability reconstruction is allowed only as a **new forensic experiment**.

Do not say:

```text
This was the original engine.
```

Say:

```text
This reconstruction combines historically attested components that may not have coexisted in one executed revision.
```

Before combining two components, record:

```text
component A source commit/blob
component B source commit/blob
proof they coexisted, if any
interface incompatibilities
behavioral changes required to combine them
```

Any adaptation needed to make old components work together is new code and must be separately versioned.

## 12. Recommended extension experiment

The next scientifically useful extension is **not** a large rescue campaign. It is a bounded ablation of the preserved backbone hypothesis.

Suggested design:

```text
A. full-backbone representation only
B. A + static classical backbone terms
C. B + Phase-I observable-driven controller
D. B + TPO entropy term
E. B + QIS combined-probe terms
```

Use the same initial states and same evaluation metrics for all arms.

Primary questions:

1. Does full N/CA/C representation alone explain most angular ordering?
2. Does the Phase-I controller improve ordering beyond a static force set?
3. Does TPO regularization predict later foldability better than Rg/topology alone?
4. Do QIS terms add anything after representation and TPO are controlled?

Do not use native RMSD to select parameters if native-RMSD generalization is an outcome under test.

## 13. Baseline comparisons required before novelty claims

At minimum compare any recovered effect against:

- simple bond/angle geometry regularization;
- Ramachandran basin regularization;
- a static weighted classical force field;
- random or matched-seed controls;
- an Rg-only compaction objective;
- topology-only ranking;
- TPO-only ranking.

A custom implementation is not itself novel. Novelty requires an effect or mechanism that is distinguishable from known regularization/optimization behavior.

## 14. Evidence promotion ladder

Use the following labels in future reports:

```text
SOURCE_PRESENT
SOURCE_WIRED
EXECUTION_ARTIFACT_FOUND
RUN_REPRODUCED
ABLATION_SUPPORTS_CAUSAL_ROLE
CROSS_TARGET_GENERALIZATION_SUPPORTED
EXTERNAL_BASELINE_ADVANTAGE_SUPPORTED
NOVELTY_REVIEW_PENDING
```

Never skip directly from `SOURCE_PRESENT` to `VALIDATED_PHYSICS`.

## 15. Stop rules

Stop a branch when:

- the exact historical run cannot be tied to source/config/data;
- a positive result disappears under matched-seed controls;
- a claimed QIS effect is reproduced with QIS disabled;
- a supposed new mechanism reduces to a conventional regularizer with no measurable advantage;
- a reconstruction requires extensive new code that dominates the historical component being tested.

Preserve the negative result and move to the next bounded question.
