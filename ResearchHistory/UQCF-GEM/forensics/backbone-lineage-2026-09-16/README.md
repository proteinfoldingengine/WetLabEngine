# Early Protein-Backbone Engine Forensic Reconstruction

**Date:** 2026-09-16  
**Scope:** UQCF-GEM early protein-folding lineage  
**Primary question:** What mechanics actually existed across the Phase-I topology/DAG engine, Patch 630 full-backbone engine, torsional-preorganization (TPO) program, the early QIS combined probe, and the later executed QIS production engine?

This directory is a provenance-first forensic record for humans and AI systems. It is intentionally more conservative than the contemporaneous project narratives. Executable source, Git history, raw run artifacts, and frozen metrics outrank retrospective prose.

## Executive finding

The historical lineage is **not** a simple monotonic version chain in which QIS inherited every earlier protein-physics feature.

The evidence supports a branched lineage:

```text
Phase-I topology / DAG physics
    -> observable-driven force activation
    -> Compaction -> LockIn transition
    -> Betti1 persistence, coherence, torsional disorder, Rg and other observables

Patch 630
    -> full N-CA-C backbone state
    -> independent learnable N, CA and C coordinates
    -> true phi/psi geometry
    -> physically meaningful Ramachandran-space calculations

TPO / Goldilocks-coil program
    -> global geometry alone found insufficient
    -> torsional entropy / basin distance added as local-order observables
    -> differentiable torsion-entropy term added to discovery engine
    -> initial-state foldability became a central hypothesis

                        +--------------------------+
                        |                          |
                        v                          v
              QIS combined probe          later QIS production
              full backbone retained      C-alpha search engine
              + QIS entropy/coherence     + topology/information score
              + soft topology term        + fragment/torsion/jitter moves
              + annealed QIS scale        + OpenMM relaxation
                                         + native-RMSD-guided acceptance
```

The strongest preserved **protein-physics lineage** is therefore the combination of the Phase-I observable-driven architecture, Patch 630 full-backbone representation, and the TPO/local-order work. The later executed QIS production engine is related, but mechanically different: it is best described as an information-guided stochastic structural-search system rather than a complete successor to the earlier backbone engine.

This conclusion does **not** certify a novel folding law or establish predictive protein folding. It identifies what software and experiments actually existed, what was later lost or disconnected, and which historical results merit bounded re-evaluation.

---

## Evidence authority classes

Every claim in this package should be read using these classes.

| Class | Meaning |
|---|---|
| **A — executed / raw artifact** | A raw run log, campaign output, or other artifact directly records execution. |
| **B — executable source / Git provenance** | Source and exact Git/blob identity establish that mechanics existed and were wired or callable, but do not by themselves prove a claimed scientific outcome. |
| **C — contemporaneous scientific record** | A Google Doc or historical report records what the project believed at the time. Useful for reconstructing intent and claimed results, but subordinate to code and raw artifacts. |
| **D — later forensic interpretation** | A present reconstruction that combines A/B/C evidence. Must not be promoted to experimental fact without reproducing the underlying run. |

A future AI must never convert a Class C claim into Class A evidence merely because the wording in the historical document is confident.

---

## Git provenance caveat

The surviving public UQCF-GEM repository does not preserve a clean one-commit-per-milestone chronology for the earliest stages. The initial surviving repository snapshot, commit:

`9e8172268b1feadc1fdbecfa6ca61239dccf21d7`

contains multiple historical components together, including:

- `dag_engine.py`
- `physics_only_controller.py`
- `protein_model.py` labeled Patch 630
- `force_field.py`
- `qis_combined_probe.py`
- `Main.py`
- metrics/history/calibration code

Therefore this record calls Phase-I, Patch 630, and the QIS combined probe **code-state milestones**, not independent Git commits, unless a later source explicitly supplies a distinct commit.

A later destructive transition is unambiguous:

`1dea70ca8864f80a909ee8a23d379608692e80b6` — `RemoveQISEngine`

That change explicitly removed QIS scheduling, QIS entropy/coherence/topology terms, QIS diagnostics, and the earlier DAG implementation from the then-current UQCF-GEM path.

---

# Forensic feature matrix

Legend: **Y** = present/wired in identified code state; **M** = measured/diagnostic rather than a force; **P** = present in adjacent source but not established as the active main path; **N** = absent from the identified executed production implementation; **?** = exact execution remains to be recovered.

| Mechanic | Phase-I topology/DAG | Patch 630 | TPO / Goldilocks | QIS combined probe | Executed QIS production |
|---|---:|---:|---:|---:|---:|
| C-alpha geometry | Y | Y | Y | Y | Y |
| Independent N / CA / C coordinates | P/Y as lineage evolves | **Y** | **Y** | **Y** | **N** |
| True phi/psi calculation | P/Y | **Y** | **Y** | **Y** | **N** |
| Ramachandran potential | **Y** in force policy | **Y-capable** | **Y-capable** | **Y** | **N** |
| LJ/steric repulsion | **Y** | Y | Y | Y | simplified OpenMM nonbonded |
| Directional backbone H-bond term | historical physics path | Y-capable | Y-capable | **Y** | **N** |
| Screened electrostatics | LockIn | Y-capable | Y-capable | **Y** | **N** (production particles zero-charge) |
| Hydrophobic-collapse control | **Y** | not representation-specific | available in earlier path | not central | **N** |
| Fractal compaction funnel | **Y** | not representation-specific | historical/discovery lineage | not central | **N** |
| Angular torque locking | **Y** | geometry makes it meaningful | superseded/supplemented by torsional terms | not central | **N** |
| Gamma/coherence well | **Y** | not representation-specific | historical | QIS uses a different coherence term | **N** |
| Contact springs | LockIn | available | available | **Y** | **N** equivalent |
| Torsional-incoherence penalty | LockIn | possible | evolves into explicit TPO terms | QIS neighbor-coherence term | only a CA-coordinate torsion proposal move |
| Betti1/topology measurement | **Y** | M | M | M + soft topology loss | **Y** as FI features |
| Topology changes active physical force set | **Y** | not intrinsic | N | N in combined probe | **N** |
| Dynamic Compaction -> LockIn phases | **Y** | not intrinsic | N | gate-free probe | **N** |
| Intrinsic-timescale feedback | **Y** in `physics_only_controller.py` | not intrinsic | N | N | N |
| Torsion entropy observable | not original focus | possible | **Y** | QIS entropy differs | N true-backbone TPO |
| Torsion entropy as differentiable loss | N | possible | **Y** | QIS entropy loss | N |
| Native RMSD in optimization objective | not the defining controller law | diagnostic in probe-style runs | used to assess candidates | diagnostic | **Y, explicitly** |
| Stochastic fragment-bridge move | N | N | N | N | **Y** |
| Stochastic CA torsion-tweak move | N | N | N | N | **Y** |
| Simulated-annealing / Metropolis acceptance | N | N | N | N | **Y** |
| OpenMM relax/checkpoint loop | N | N | N | N | **Y** |

---

# Milestone 1 — Phase-I topology/DAG engine

## Exact surviving source

Repository: `proteinfoldingengine/UQCF-GEM`  
Source authority snapshot: `9e8172268b1feadc1fdbecfa6ca61239dccf21d7`

Key blobs:

- `dag_engine.py` — `4694cab56217202b8732cd2800f1bc3c60c589dc`
- `physics_only_controller.py` — `e576f9a66eada6ba8fa00ad4a99b15ce56757c7e`
- `metrics_history.py` — `fe3f02f7f4d7aad97027fa9258ab8eab3d5469ea`
- `online_metrics_utils.py` — `b9aabbfb7a9f683296d519cdd09ec56075927e02`

## DAG law

`dag_engine.py` identifies itself as Patch 624.1. Its phase schema contains:

### P0 — Compaction

- Lennard-Jones repulsion
- angular torque locking
- gamma/coherence well
- Ramachandran potential
- fractal compaction funnel
- hydrophobic collapse

### P1 — LockIn

The P0 set plus:

- screened electrostatics
- contact springs
- torsional incoherence penalty

The transition is state-driven. The code checks both a Betti1 threshold and persistence duration. In symbolic form:

```text
if Betti1 >= betti_threshold
and Betti1_lifetime >= dag_transition_lifetime:
    Compaction -> LockIn
```

The default values visible in the source are `betti_threshold = 8` and `dag_transition_lifetime = 100` unless overridden by configuration.

This is an important architectural distinction: physical observables are not merely logged; they can change which forces are active.

## Physics-only controller

The adjacent `physics_only_controller.py` goes further and removes named phases. It estimates online autocorrelation times and smoothed slopes for observables including:

- Rg
- phi RMS
- gamma coherence
- Betti1 lifetime

It can emit actions including:

- `RAMP_CONTACTS`
- `CAP_CONTACTS_WEAK`
- `BOOST_HYDROPHOBIC`
- `RELAX_RAMA`
- `ENFORCE_RG_WINDOW`

This is evidence for a second observable-driven control architecture. It should **not** be assumed to have been active in every historical run without locating the calling path/config for that run.

## Scientific interpretation

The distinctive idea in this stage is:

```text
structure observables
    -> controller state/action
    -> physical-force policy
    -> new structure
    -> new observables
```

This feedback architecture is not preserved in the later executed QIS production solver.

---

# Milestone 2 — Patch 630 full-backbone angular physics

## Exact surviving source

`protein_model.py` blob:

`6bc1a564cff022cf533ad2b8de2c03a1aee21afe`

The same blob is preserved in the recovered PharmaApp `QISEngine/protein_model.py`, establishing direct source continuity for this component.

The file labels itself:

`Patch 630: Full Backbone Angular Physics`

## State representation

`ProteinModel` makes the three backbone atom coordinate arrays independent learnable PyTorch parameters:

```text
N_coords
CA_coords
C_coords
```

This is materially different from a CA-only trace. It makes local backbone geometry capable of defining actual peptide-like dihedrals instead of trying to infer two torsions from a single reduced trace.

The random-coil initializer first generates a CA walk at approximately 3.8 A spacing and then places N and C around CA using idealized geometry.

## True torsional geometry

The QIS-era runner built on Patch 630 calls `compute_true_phi_psi(n_t, ca_t, c_t)` each iteration, measures phi RMS, and passes phi/psi to the force field.

This is the key representational upgrade:

```text
C_(i-1), N_i, CA_i, C_i       -> phi_i
N_i, CA_i, C_i, N_(i+1)       -> psi_i
```

## Contemporaneous evidence

Google Doc `PhysicsBasedStructureEmergence`:

- Drive ID: `13nzDwcZktYPZwsRzd6YcfektGA_4-c1-tNiTTgpmnpI`
- revision at forensic read: `ANLCKQlKj93Lj6GAkKMEl4S6xOpf6FGqg-4k5gWpBn4f5SwxzSHKkbu_WSZgzwsMaZH2Hbc1qN2wsns801aGmA`

records the historical Patch-630 interpretation:

- prior CA-only phi-RMS plateau about 1.63
- reported final phi-RMS `0.2215`
- reported final RMSD `10.19 A`
- loss of the previous phi≈psi diagonal degeneracy
- a Ramachandran cluster interpreted as alpha-helical organization

**Authority:** Class C until the exact raw run/trajectory producing those numbers is recovered and pinned. The source code proves the representation and possible mechanism; it does not independently prove those numerical outcomes.

---

# Milestone 3 — TPO / Goldilocks-coil discovery

## Why the name is TPO, not “Seed 965 engine”

The scientifically meaningful milestone is the shift to **torsional pre-organization (TPO)** as a measurable local-order variable. Seed numbers are experiment-specific and can collide across proteins or campaigns.

## Exact Git milestones

### Torsional metrics introduced

Commit:

`b11552a6c932b20f028ece5e5ff806862077bfde` — 2025-08-31

Key blob:

- `torsional_metrics.py` — `0aee35076a59805aa4f99897d7c662b943051ebe`

The module measures:

1. 2-D phi/psi histogram entropy
2. RMS angular distance to canonical Ramachandran basin centers

The preserved basin centers include an alpha-helical center near `(-60, -45)` degrees and beta-sheet center near `(-135, 135)` degrees.

### Torsional entropy made an optimization term

Commit:

`d019fe0fef858a4b73d3baaf3406df0447142cbe`

Key blob:

- `stage1_discovery_engine.py` — `c580a15c75e68816e1143d2a28f4485174cf4925`

This engine creates a differentiable soft 2-D phi/psi histogram and adds a weighted torsion-entropy penalty to the total potential. It also supports an Rg funnel:

```text
E_total = E_classical
        + k_torsion_entropy * S(phi,psi)
        + k_rg_pull * (Rg - Rg_target)^2
```

It optimizes the N/CA/C `ProteinModel` with Adam.

## Historical Golden-Coil record

Google Doc `TheTheoryOfTheBeginning`:

- Drive ID: `1KGakmnwTW_gXvtuBa8Rk4kIcICcLHt4Lx4Jw1qU3KAg`
- revision at forensic read: `ANLCKQkcw9BndAai6OST0712jVaY96Swe9XuxUDeLasfSZJyiRVNzPesgV13N3pQ7_1HD6DrMVAHsc_wm8EaDg`

records a 1VII experiment in which:

- Seed 965 was selected with composite TPO Index `0.69`
- a pre-run final-RMSD prediction of `6.5-8.5 A` was recorded
- a pre-run final-Rg prediction of `9.0-10.0 A` was recorded
- the document reports actual final RMSD `8.90 A`
- the document reports actual final Rg `7.27 A`
- the narrative says RMSD and Rg fell during the same Phase-B classical relaxation that left earlier brittle coils trapped

**Authority:** Class C in this package. The document is strong historical evidence of what was claimed and that the prediction was described as preregistered, but the exact seed-965 raw trajectory/config/log has not yet been pinned here. Future work should locate and hash those artifacts before treating `8.90 A / 7.27 A` as a reconstructed Class-A result.

## Important seed-number warning

Current UQCF-GEM deep-scan tables also contain rows named seed 965 for proteins such as 1QYS and 1PGB. Those rows are **not automatically the 1VII Golden-Coil experiment** described above. Never join historical datasets by seed number alone. Required identity key:

```text
(protein / campaign / source commit or artifact set / seed)
```

---

# Milestone 4a — QIS historical combined probe

## Authority

Pre-removal source snapshot:

`9e8172268b1feadc1fdbecfa6ca61239dccf21d7`

The recovered PharmaApp provenance classifies this as:

`HISTORICAL_COMBINED_PROBE_PRE_REMOVE_QIS`

Important blobs include:

- `Main.py` — `c6032f6f6affaff0a4071e852dd85bb0e21ca7db`
- `qis_combined_probe.py` — `d02644917a788d7033d433a5acfa92b5b8476951`
- `force_field.py` — `5b5728f61a0572f9118f03b257eecf333342a51a`
- `protein_model.py` — `6bc1a564cff022cf533ad2b8de2c03a1aee21afe`

## Mechanics

The probe retains the Patch-630 full backbone and the classical terms present in its force field, including implementations for:

- steric repulsion
- screened electrostatics
- directional backbone H-bond energy
- Ramachandran potential
- contact springs
- torsion penalty

It then adds optional annealed QIS terms:

### QIS entropy

A phi/psi distribution entropy term.

### QIS coherence

Neighbor smoothness in wrapped phi/psi differences.

### QIS soft topology

A differentiable contact-graph cycle-surplus proxy.

### Schedule

The runner applies a configurable QIS scale over the simulation (`cosine`, `linear`, or fallback schedule form).

## What this means

The historical combined probe is a **real descendant of Patch 630** because the full-backbone blob is retained and exercised. It is not, however, equivalent to the earlier DAG controller because `Main.py` describes itself as a minimal, gate-free probe and does not use topology to switch the complete Phase-I force policy.

---

# Milestone 4b — executed QIS production engine

This must be kept separate from the combined probe.

## Recovery authority

The recovered `QISEngine/PROVENANCE.json` identifies:

- source commit: `1e88c1b5778e98eb2f5c1b0c0f019ba0801e1c38`
- source path: `qis_engine_production.py`
- recovered blob: `2cb51ffc7b2edacee0e867a16a511b30847adbae`
- campaign driver blob: `b7e7afa665ad2f29b6287403dfae9478f7e945ca`
- corroborating run artifact commit: `4d61823a0ce4dcc71f596893514b29d151fed435`
- corroborating stdout blob: `ba779a7e54d9ee0167f8ab6c664d04050384e4d5`

The corroborating run records move classes:

- `fragment_bridge`
- `torsion_tweak`
- `jitter`

This is Class A/B evidence of an executed production lineage.

## Representation

The production solver parses and writes **CA coordinates only**.

It constructs a simplified OpenMM system with:

- particles placed on CA positions
- harmonic bonds between adjacent residues around 0.38 nm
- a weak generic nonbonded term
- zero particle charge in the recovered implementation

This is not Patch-630 full-backbone dynamics.

## QIS feature score

The production solver computes features including:

- Betti1 counts at persistence thresholds
- Betti1 lifetime p90
- Betti1 lifetime mean
- a pair-distance entropy/stability feature `S_min`
- Rg

A fixed weighted standardized score `FI_raw` is formed from those features.

## Objective and acceptance

The recovered solver explicitly computes native RMSD. Early iterations use:

```text
J = RMSD
```

and later iterations use a mixed objective of the form:

```text
J = alpha * RMSD - beta * FI_z
```

Candidate structures are generated by stochastic move proposals, relaxed in OpenMM, and accepted/rejected with a simulated-annealing / Metropolis rule.

Therefore production QIS is better classified as:

```text
CA structural search
+ information/topology scoring
+ stochastic proposals
+ OpenMM relaxations
+ native-RMSD-guided selection
```

not as a complete continuation of the Phase-I/Patch-630 protein-physics dynamics.

---

# Strongest falsification control currently pinned

The Drive archive contains a direct QIS-on / QIS-off pair for `1UAO`, seed 3.

## QIS OFF

File ID: `1cQoWOAMIqSnQ8VgNRGcCZ7Aroz7-DY4j`  
Title: `summary_log_T2_QIS_OFF_s3.txt`

Raw summary:

```text
Patch: T2_QIS_OFF_s3
PDB: 1UAO
Steps: 1200
Final RMSD: 3.982 A
Final Rg: 3.395 A
```

## QIS ON

File ID: `1cNVH5SCRnAwdraWI7ekZbIgQcdQtmt-p`  
Title: `summary_log_T2_QIS_ON_s3.txt`

Raw summary:

```text
Patch: T2_QIS_ON_s3
PDB: 1UAO
Steps: 1200
Final RMSD: 3.982 A
Final Rg: 3.395 A
```

These results are identical at the reported precision. They are direct evidence against attributing the 3.982-A outcome to the QIS terms in that experiment.

The scientifically useful interpretation is narrower: the run suggests the initial geometry and/or classical relaxation path were sufficient to produce that result under this harness. It does **not** establish that the initial state alone universally determines folding.

---

# Contemporaneous Phase-I source record

Google Doc `Scientific summary`:

- Drive ID: `14V4iV-f3kSyVDmU6v-mC3-nwxOGAeD3MbMEEKWRO19w`
- revision at forensic read: `ANLCKQlBBZCzRwj0aVR-7xWfBsSfh3_Ef05F2t8TUFBsIvVJ8aZ1ODJNoylBMPKprF5an-oRTI1zEk0GeBdCmA`

records the following historical milestone claims:

- Patch 510.1: molten-globule behavior in 1UBQ
- Patch 622.2: topology-triggered phase change
- Patch 622.4: bounded coherence well
- Patch 623.0: torsional-incoherence penalty
- Patch 624.x: stable molten-globule behavior in 1UBQ and 1VII
- Patch 625: extended-runtime plateau behavior
- Patch 627: generalization to Top7 / 1QYS
- Patch 629: CA-only phi≈psi degeneracy exposed
- Patch 630: full-backbone angular physics activated

This document is particularly valuable for reconstructing historical intent and patch numbering, but its phrases such as “first-principles folding validated” are **not adopted as current conclusions**. Each numerical or scientific claim must be independently tied to raw artifacts before promotion to Class A.

---

# Mechanics that did not carry intact into executed production QIS

The following earlier capabilities are not present in equivalent form in the recovered executed production QIS solver:

1. topology-triggered Compaction -> LockIn force switching
2. intrinsic-timescale observable feedback controller
3. independent learnable N/CA/C coordinates
4. true N-CA-C phi/psi dynamics
5. directional backbone H-bond physics
6. full Ramachandran potential acting on true backbone angles
7. hydrophobic-collapse control from the Phase-I policy
8. fractal compaction funnel from the Phase-I policy
9. angular torque locking
10. gamma/coherence well
11. screened residue electrostatics in the earlier force-field form
12. the earlier torsional-preorganization measurement/penalty pipeline as a full-backbone local-order mechanism

Conversely, production QIS adds capabilities not present in the same form in the early engine:

1. fragment-bridge proposal moves
2. stochastic CA torsion moves
3. coordinate jitter proposals
4. simulated-annealing / Metropolis acceptance
5. OpenMM short/long relaxation checkpoints
6. fixed FI feature scoring
7. native-RMSD-directed objective
8. archive/stall/reheat logic

---

# Current scientific interpretation

The historical work supports several different levels of conclusion.

## Supported by code provenance

- A topology/observable-driven controller existed.
- A full N/CA/C learnable backbone implementation existed.
- True phi/psi calculations were used by the Patch-630/QIS-probe lineage.
- TPO metrics and a differentiable torsion-entropy term existed.
- The QIS combined probe retained the full-backbone representation and added annealed entropy/coherence/topology losses.
- The executed production QIS engine was mechanically different and CA-based.

## Supported by raw pinned control artifacts

- In the identified 1UAO seed-3 control, QIS ON and QIS OFF both ended at 3.982-A RMSD and 3.395-A Rg.
- Therefore that outcome cannot be attributed to QIS terms from those summaries.

## Historically claimed, requiring raw-artifact recovery

- stable molten-globule emergence across 1UBQ / 1VII / Top7
- Patch-630 phi-RMS `0.2215`
- Patch-630 10.19-A Villin result
- 1VII Seed-965 TPO Index `0.69`
- preregistered Seed-965 prediction and reported `8.90-A / 7.27-A` outcome

These are high-priority recovery targets, not current certified results.

---

# What should be preserved

For scientific salvage and future bounded testing, preserve at minimum:

- Phase-I DAG/controller source and exact blobs
- Patch-630 `ProteinModel` and its true-phi/psi metrics path
- the pre-removal force field and QIS probe source
- TPO metric code and the torsion-entropy discovery engine
- exact historical configs associated with validated or claimed runs
- raw trajectories, summary logs and time-series for 1UBQ, 1VII, Top7/1QYS, Villin/Patch630 and 1UAO controls
- production QIS provenance and executed campaign logs as a separate lineage
- negative/falsification records, especially QIS ON/OFF controls

Do **not** collapse these sources into a synthetic “ultimate historical engine” and then claim that engine previously ran. A combined reconstruction would be a new experiment and must be labeled as such.

---

# Recommended bounded continuation

A scientifically disciplined continuation is a forensic-reproduction program, not open-ended feature development.

1. Recover exact raw artifacts for the highest-value historical claims.
2. Hash and freeze the source/config/data tuple for each claimed run.
3. Re-run only enough cases to establish whether the historical behavior reproduces.
4. Separate representation effects from force/controller effects using ablations.
5. Compare TPO/backbone-ordering metrics against simple geometric regularizers and standard structural baselines.
6. Only after reproduction ask whether any effect is novel or scientifically useful.

The broad PharmaApp/QIS rescue-engine program should not be treated as evidence for the earlier backbone-physics program. The two must remain analytically separate.

---

# AI usage rules

An AI extending this work must:

1. Read `SOURCE_MANIFEST.json` before making lineage claims.
2. Use `EVIDENCE_INDEX.md` to locate the authority behind each factual statement.
3. Follow `AI_REPRODUCTION_GUIDE.md` before changing or combining historical mechanics.
4. Cite repository, commit and blob whenever discussing source identity.
5. Cite Drive file ID and revision ID when relying on a historical Google Doc.
6. Never treat a narrative document as proof that code executed.
7. Never infer protein identity from seed number alone.
8. Never attribute an outcome to QIS without an appropriate control.
9. Keep “software existed,” “software executed,” “result reproduced,” “physical mechanism validated,” and “scientific novelty established” as separate propositions.
10. Preserve failed controls. They are part of the scientific result.

See also:

- `SOURCE_MANIFEST.json`
- `EVIDENCE_INDEX.md`
- `AI_REPRODUCTION_GUIDE.md`
