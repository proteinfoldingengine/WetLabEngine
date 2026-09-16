# Gen3 HB1 — Gate 004 Multi-Seed Contact Mechanism Test

Date: 2026-09-16
Preregistration commit precedes this result (`ABLATION_GATE_004_PREREGISTRATION.md`).
Seeds: 11, 23, 42, 57, 73, 101, 137, 211
Target: 1VII
Runs: 40 planned / 40 completed

## Primary results: final phi_RMS

| Seed | Dynamic | OFF | Frozen | Randomized | Generic |
|---:|---:|---:|---:|---:|---:|
| 11 | 0.231 | 0.442 | 0.235 | 0.263 | 0.309 |
| 23 | 0.218 | 0.417 | 0.222 | 0.247 | 0.292 |
| 42 | 0.223 | 0.429 | 0.226 | 0.250 | 0.300 |
| 57 | 0.239 | 0.451 | 0.243 | 0.270 | 0.318 |
| 73 | 0.225 | 0.434 | 0.229 | 0.255 | 0.304 |
| 101 | 0.216 | 0.411 | 0.220 | 0.244 | 0.289 |
| 137 | 0.234 | 0.446 | 0.238 | 0.267 | 0.313 |
| 211 | 0.221 | 0.424 | 0.225 | 0.249 | 0.297 |

Aggregate phi_RMS:

- dynamic mean: **0.2259**
- contacts OFF mean: **0.4318**
- frozen mean: **0.2298**
- randomized mean: **0.2556**
- generic mean: **0.3028**

Paired frozen-minus-OFF differences are negative in **8/8 seeds**; mean difference approximately **-0.2020**. Dynamic and frozen remain close across the panel. Randomized graphs retain a substantial but weaker effect. Generic compaction improves angular order relative to OFF but remains consistently weaker than frozen graphs.

## Secondary RMSD result

Across seeds, final RMSD differences are small compared with phi_RMS differences. The graph mechanisms primarily change the angular-order metric rather than producing a large native-structure RMSD improvement. No condition in this gate establishes accurate native folding.

## Gate decision

The preregistered majority criterion is met: frozen contacts improve final phi_RMS over contacts OFF in 8/8 paired seeds. The aggregate frozen-graph result is also materially stronger than the matched generic-compaction control in all 8 seeds.

Therefore the seed-42 observation is not isolated to that seed under this panel. The surviving candidate mechanism is:

> topology-conditioned activation of a nonlocal distance-constraint graph on a full backbone produces reproducible angular-order stabilization beyond the matched generic compaction control used here.

## Boundaries

This does not establish novelty. Nonlocal distance restraints, graph constraints, elastic-network ideas, contact potentials, and coarse-grained folding restraints have substantial prior art. It also does not establish native-fold prediction, because RMSD improvements remain small and the graph is derived from the evolving model state rather than independently predicting native contacts.

The appropriate next test is **held-out target transfer**, using the same preregistered mechanisms and no target-specific retuning. Only if the frozen/dynamic graph advantage transfers should the mechanism be considered for implementation on Gen3's kinematic backbone.
