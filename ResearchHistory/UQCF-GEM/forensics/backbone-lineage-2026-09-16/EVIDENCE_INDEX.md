# Evidence Index — Early Protein-Backbone Lineage

This file maps each important forensic claim to the exact source that supports it. It is intended to be machine-readable by inspection even though it is Markdown.

Authority classes:

- **A** — raw/executed artifact
- **B** — exact executable source / Git provenance
- **C** — contemporaneous historical narrative
- **D** — later forensic interpretation

## Claim index

| Claim | Source | Exact identity | Authority | Status / caveat |
|---|---|---|---:|---|
| Phase-I had a Compaction -> LockIn controller | `UQCF-GEM/dag_engine.py` | commit `9e8172268b1feadc1fdbecfa6ca61239dccf21d7`; blob `4694cab56217202b8732cd2800f1bc3c60c589dc` | B | Source-proven |
| Phase transition depended on Betti1 count and persistence duration | same `dag_engine.py` | same blob | B | Source-proven |
| Compaction and LockIn activated different force sets | same `dag_engine.py` | same blob | B | Source-proven |
| An alternate physics-only observable controller existed | `physics_only_controller.py` | blob `e576f9a66eada6ba8fa00ad4a99b15ce56757c7e` | B | Source-proven; exact run usage must be established per experiment |
| Physics-only controller estimated intrinsic timescales/slopes | `physics_only_controller.py`; `online_metrics_utils.py` | blobs `e576...`, `b9aabb...` | B | Source-proven |
| Patch 630 used independent learnable N, CA and C coordinates | `protein_model.py` | blob `6bc1a564cff022cf533ad2b8de2c03a1aee21afe` | B | Source-proven |
| Patch-630 protein model survived into recovered QIS | PharmaApp `QISEngine/protein_model.py` | same blob `6bc1a564...` | B | Exact blob identity |
| Historical QIS probe calculated true phi/psi from N/CA/C | UQCF-GEM `Main.py` / recovered QIS Main | blob `c6032f6f6affaff0a4071e852dd85bb0e21ca7db` | B | Source-proven |
| Historical QIS force field contained directional H-bond physics | `force_field.py` pre-removal | blob `5b5728f61a0572f9118f03b257eecf333342a51a` | B | Source-proven |
| Historical QIS force field contained Debye-Huckel electrostatics | same | same blob | B | Source-proven |
| Historical QIS force field contained Ramachandran, contacts and torsion terms | same | same blob | B | Source-proven |
| Historical QIS added phi/psi entropy regularization | same | same blob | B | Source-proven |
| Historical QIS added neighbor torsional coherence | same | same blob | B | Source-proven |
| Historical QIS added a differentiable soft-topology/cycle term | same | same blob | B | Source-proven |
| QIS terms were annealed by a schedule in the combined probe | `Main.py` | blob `c6032...` | B | Source-proven |
| The combined probe was gate-free relative to Phase-I DAG | `Main.py` header/architecture | blob `c6032...` | B/D | Source says minimal gate-free probe; inference concerns architectural comparison |
| QIS mechanics were later deliberately removed | commit `RemoveQISEngine` | `1dea70ca8864f80a909ee8a23d379608692e80b6` | B | Git-diff proven |
| TPO metrics measured 2-D phi/psi entropy | `torsional_metrics.py` | commit `b11552a...`; blob `0aee35076a59805aa4f99897d7c662b943051ebe` | B | Source-proven |
| TPO metrics measured periodic distance to alpha/beta basins | same | same blob | B | Source-proven |
| A differentiable torsion-entropy penalty entered Stage-1 discovery | `stage1_discovery_engine.py` | commit `d019fe0...`; blob `c580a15c75e68816e1143d2a28f4485174cf4925` | B | Source-proven |
| The TPO discovery engine still optimized full N/CA/C coordinates | `stage1_discovery_engine.py` + ProteinModel | commit `d019fe0...` | B | Source-proven |
| Historical Phase-I record claimed molten-globule behavior in 1UBQ | Drive `Scientific summary` | file `14V4iV-f3kSyVDmU6v-mC3-nwxOGAeD3MbMEEKWRO19w`; revision `ANLCKQlBBZCzRwj0aVR-7xWfBsSfh3_Ef05F2t8TUFBsIvVJ8aZ1ODJNoylBMPKprF5an-oRTI1zEk0GeBdCmA` | C | Historical claim; raw run not pinned here |
| Historical Phase-I record claimed stable molten globules in 1UBQ + 1VII | same | same | C | Historical claim; raw logs need recovery |
| Historical Phase-I record claimed Top7/1QYS generalization | same | same | C | Historical claim; raw run needs recovery |
| Historical record says CA-only phi≈psi degeneracy motivated Patch 630 | same + `PhysicsBasedStructureEmergence` | Drive IDs `14V4...` and `13nz...` | C/B | Narrative aligns with representational change in source |
| Patch-630 historical record reports phi-RMS 0.2215 | Drive `PhysicsBasedStructureEmergence` | file `13nzDwcZktYPZwsRzd6YcfektGA_4-c1-tNiTTgpmnpI`; revision `ANLCKQlKj93Lj6GAkKMEl4S6xOpf6FGqg-4k5gWpBn4f5SwxzSHKkbu_WSZgzwsMaZH2Hbc1qN2wsns801aGmA` | C | Raw run not pinned here |
| Patch-630 historical record reports RMSD 10.19 A | same | same | C | Raw run not pinned here |
| Patch-630 historical record reports disappearance of phi≈psi diagonal | same | same | C | Plausible and representation-consistent; raw plot/run still needed |
| 1VII Seed 965 described as TPO Index 0.69 | Drive `TheTheoryOfTheBeginning` | file `1KGakmnwTW_gXvtuBa8Rk4kIcICcLHt4Lx4Jw1qU3KAg`; revision `ANLCKQkcw9BndAai6OST0712jVaY96Swe9XuxUDeLasfSZJyiRVNzPesgV13N3pQ7_1HD6DrMVAHsc_wm8EaDg` | C | Raw candidate table/config not yet pinned |
| 1VII Seed 965 prediction described as RMSD 6.5-8.5 A | same | same | C | Historical preregistration claim; exact timestamped prediction artifact should be recovered |
| 1VII Seed 965 result described as RMSD 8.90 A | same | same | C | Raw run not yet pinned |
| 1VII Seed 965 result described as Rg 7.27 A | same | same | C | Raw run not yet pinned |
| Production QIS is a distinct executed lineage | PharmaApp `QISEngine/PROVENANCE.json` | blob `5affdaa095d3b2c084e7710220d06bff781967b6` | B | Provenance record explicitly distinguishes probe and production |
| Accepted production QIS source commit is `1e88c1b...` | same provenance | source commit `1e88c1b5778e98eb2f5c1b0c0f019ba0801e1c38` | B | Recovery authority |
| Production QIS used CA-only structure representation | recovered `qis_engine_production.py` | blob `2cb51ffc7b2edacee0e867a16a511b30847adbae` | B | Source-proven |
| Production QIS used fragment-bridge proposals | same + campaign stdout | engine blob `2cb51...`; stdout blob `ba779...` | A/B | Source + executed artifact |
| Production QIS used torsion-tweak proposals | same + campaign stdout | same | A/B | Source + executed artifact |
| Production QIS used jitter proposals | same + campaign stdout | same | A/B | Source + executed artifact |
| Production QIS computed Betti persistence features and information score | engine blob `2cb51...` | same | B | Source-proven |
| Production QIS objective explicitly used native RMSD | engine blob `2cb51...` | same | B | Source-proven |
| Production QIS used simulated-annealing/Metropolis acceptance | engine blob `2cb51...` | same | B | Source-proven |
| Production QIS did not preserve full Patch-630 N/CA/C mechanics | compare blobs `6bc1...` vs `2cb51...` | source comparison | B/D | Strong source-based forensic conclusion |
| 1UAO seed-3 QIS OFF ended at RMSD 3.982 A, Rg 3.395 A | Drive raw summary | file `1cQoWOAMIqSnQ8VgNRGcCZ7Aroz7-DY4j` | A | Raw summary pinned |
| 1UAO seed-3 QIS ON ended at RMSD 3.982 A, Rg 3.395 A | Drive raw summary | file `1cNVH5SCRnAwdraWI7ekZbIgQcdQtmt-p` | A | Raw summary pinned |
| QIS cannot be credited for that specific 1UAO final state | paired raw summaries | above two Drive files | A/D | Identical reported outcome with QIS ON and OFF |

## Negative and cautionary evidence

### 1UAO control

The strongest directly pinned falsification control in this package is the 1UAO seed-3 pair:

```text
QIS OFF -> RMSD 3.982 A, Rg 3.395 A
QIS ON  -> RMSD 3.982 A, Rg 3.395 A
```

This blocks any statement that the observed 3.982-A result in this paired experiment demonstrates a QIS effect.

### Historical confidence language

Several Drive documents use phrases such as “validated,” “breakthrough,” “first-principles,” or “predictive theory.” Those phrases are preserved as historical context only. The current forensic standard requires raw artifact recovery and controlled reproduction.

### Seed-number collisions

Do not identify a run by seed number alone. `965` occurs in later deep-scan tables for proteins other than 1VII. Always include protein and campaign provenance.

## Raw-artifact recovery queue

The following claims are important enough to prioritize but are **not** promoted to Class A in this package:

1. Patch-630 raw run producing phi-RMS `0.2215` and RMSD `10.19 A`.
2. 1VII Seed-965 candidate-selection/TPO record.
3. 1VII Seed-965 preregistration artifact.
4. 1VII Seed-965 Phase-B timeseries/trajectory supporting `8.90 A / 7.27 A`.
5. Phase-I 1UBQ and 1VII molten-globule logs.
6. Top7/1QYS Patch-627 generalization run.
7. Exact evidence identifying which historical controller path was active in each early successful run.

## Machine-handoff questions

A future AI should answer these in order before extending the system:

1. Can the Patch-630 numerical result be reproduced from an exact source/config pair?
2. Can the 1VII Golden-Coil result be recovered as raw data and reproduced?
3. Does TPO predict Phase-B outcome after controlling for Rg and topology?
4. Does the observable-driven Phase-I controller improve outcomes over a static force field?
5. Do QIS combined-probe terms add anything after full-backbone geometry and TPO are controlled?
6. Are any observed advantages larger than simple conventional geometric regularization baselines?
7. Only then: is there a scientifically novel mechanism worth further development?
