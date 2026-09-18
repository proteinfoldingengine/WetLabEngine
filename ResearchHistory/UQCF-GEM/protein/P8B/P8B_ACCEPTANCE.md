# Protein P8B — Recovered Topology-Gated Controller on a Valid Backbone

**Status:** preregistered before implementation and before prospective native-evaluation result exposure.

## Scientific question

Does the **coordinate-effective mechanism recovered in P8** produce transferable native-blind protein preorganization on the already validated covalently exact P6 peptide backbone, and does its **state-dependent topology gate** add value beyond information-matched nonadaptive schedules using the same force family?

This is the bounded scientific consequence of the P8 reopen. It is not a replay of the old Cartesian engine and it is not a rescue of P6.

## Historical mechanism boundary

P8 established that the recovered Drive snapshots contain a materially different coordinate mechanism from the StableDAGPhysics source reduced by P7.

The coordinate-effective recovered mechanism consists of:

**Compaction**
- Lennard-Jones repulsion;
- C-alpha pseudo-dihedral angular torque;
- C-alpha pseudo-dihedral Ramachandran penalty;
- radius-of-gyration compaction funnel;
- binary hydrophobic-centroid collapse.

**LockIn adds**
- screened electrostatics;
- dynamic current-state contact springs.

The later recovered snapshot also activates a torsional-incoherence penalty and gamma well. P8 source audit showed those terms do not provide a coordinate-gradient path to the backbone. P8B therefore excludes them from the coordinate objective rather than pretending they are backbone forces. A contract test must confirm this reduction.

The recovered folders remain mixed-version historical snapshots. P8B tests the **frozen coordinate-effective mechanism family**, not an exact named Patch-622 or Patch-624 release.

## Exact historical topology observable

P8B preserves the recovered observable exactly.

The historical function named `compute_betti1_count` is not treated as a mathematically exact persistent-homology Betti number. It is a contact-graph loop proxy:

1. compute all C-alpha pair distances;
2. mark contacts with distance `< 8.0 A`;
3. exclude self and immediately adjacent residue pairs;
4. let `E_nonadj` be the remaining undirected contact count;
5. return `max(0, int(E_nonadj - (N - 1)))`.

The historical name `betti1_count` is retained only for source traceability. P8B documentation calls it the **historical Betti1 proxy**.

The recovered history implementation keeps at most 120 proxy values and defines “lifetime” as the **count**, not necessarily the consecutive count, of stored values at or above threshold 8.

The exact recovered state logic is:

- start in `Compaction`;
- after appending the current proxy value, transition once to `LockIn` if:
  - current proxy >= 8, and
  - stored qualifying-count >= 100;
- while in `LockIn`, screened electrostatics and contact springs are active only if:
  - current proxy >= 8, and
  - stored qualifying-count >= 50.

No native structure information enters either gate.

## Representation

P8B reuses the validated P6 target-independent canonical peptide backbone.

- fixed canonical N-Cα-C geometry;
- trans omega;
- phi/psi are the only structural degrees of freedom;
- no target-PDB bond lengths, bond angles, native fragments, native torsions or native local geometry.

The exact P6 target/evaluator objects are reused without substitution.

## Target family and seeds

Targets are frozen to the P6 family:

- `1VII`
- `1L2Y`
- `1UAO`

Seeds are:

`0,1,2,3,4,5`

Every arm for a matched target/seed starts from the exact same P6 deterministic initial phi/psi state.

## Optimizer and budget

P8B is a **representation-transfer test**, not a Cartesian numerical replay.

The historical Cartesian learning rate `0.001` is not dimensionally transferable to torsion parameters. P8B therefore inherits the already validated P6 torsion-space optimizer:

- deterministic CPU float64 PyTorch;
- Adam;
- learning rate `0.02`;
- `2000` optimization steps;
- angle wrapping after every step;
- no native-information early stopping.

The longer budget is frozen before implementation because the recovered gate itself requires up to 100 qualifying history entries before LockIn can first become eligible.

No learning-rate or step-count change is permitted after result exposure.

## Frozen recovered coefficients

The coordinate-effective historical coefficients are used without coefficient search:

- `k_contact_spring_base = 1.5`
- `k_df_funnel = 6000.0`
- `k_phi_torque_base = 1.0`
- `k_lj_repulsion_base = 1.25`
- `k_hydro_base = 0.75`
- `k_electrostatic_base = 1.0`
- `k_rama = 0.05`
- `contact_dist = 8.0 A`
- `DEBYE_LENGTH = 5.0 A`

Residue classes are frozen to the recovered source:

- hydrophobic: `A,V,I,L,M,F,W,Y,C`;
- charges: `D=-1,E=-1,K=+1,R=+1,H=+1`, all others zero.

The recovered pseudo-dihedral functions are evaluated from reconstructed C-alpha coordinates. P8B does not silently replace them with native torsions or a modern Ramachandran library.

## Experimental arms

There are four arms for every target/seed. All four use the same coordinate-effective force expressions and historical coefficients.

### 1. `recovered_state_gate`

Exact recovered controller:

- begins in Compaction;
- uses the historical Betti1 proxy and recovered history-count rules;
- one-way Compaction -> LockIn transition;
- LockIn contact/electrostatics retain the recovered secondary state gate.

This is the candidate.

### 2. `fixed_step99_lockin`

Time-schedule control:

- Compaction for steps `0..98`;
- full coordinate-effective LockIn force set from step `99` onward;
- no topology/proxy gate.

Step 99 is frozen because, if every stored value qualified starting at step 0, the recovered history would contain its 100th qualifying entry before the force evaluation of step 99.

This tests state-dependent switching versus the earliest possible fixed-time switch.

### 3. `static_lockin`

All coordinate-effective LockIn forces are active from step 0.

This tests whether the recovered state gate is better than simply using its complete force family continuously.

### 4. `compaction_only`

The coordinate-effective Compaction force set remains active for all 2000 steps.

This tests whether the recovered LockIn additions provide value beyond the Compaction phase itself.

## Native-information firewall

The optimization objective and controller may not read:

- native coordinates;
- native contacts;
- native RMSD;
- native Rg;
- native torsions;
- native secondary structure;
- target-specific fitted parameters.

Native evaluator coordinates are used only after a trajectory or frozen checkpoint has been generated.

Contract tests must show objective/gradient and controller-transition invariance when native evaluator coordinates are rigidly transformed or replaced.

## Primary endpoint

P8B reuses the P6 primary endpoint unchanged:

**final fixed-budget long-range native-contact precision**

At final step:

1. consider all C-alpha residue pairs with sequence separation >= 4;
2. rank modeled pairs by C-alpha distance;
3. take `K = max(1, floor(N/2))`, capped by eligible pair count;
4. corresponding native evaluator pair is positive if native C-alpha distance `< 8.0 A`;
5. score is native-positive fraction among the K modeled closest pairs.

No best-over-trajectory native endpoint is permitted.

The common starting-state primary precision is also evaluated after trajectory generation and is used only for the frozen improvement condition below.

## Anti-collapse gate

For the `recovered_state_gate` arm, target-wise median final modeled Rg/native evaluator Rg must lie in:

`[0.75, 1.25]`

for every target.

Native Rg remains evaluation-only.

## Primary comparisons

There are 18 matched observations for each candidate-control comparison.

Compare:

1. `recovered_state_gate - fixed_step99_lockin`
2. `recovered_state_gate - static_lockin`
3. `recovered_state_gate - compaction_only`

Higher precision is favorable.

Use exact two-sided paired sign-flip tests over all `2^18` assignments and Holm-adjust the three p-values.

## Controller-use requirement

A GO cannot be earned by trajectories that never exercise the recovered state transition.

Every one of the 18 `recovered_state_gate` trajectories must:

- enter LockIn at least once by the frozen final step; and
- activate the recovered contact/electrostatic LockIn force pair for at least one optimization step.

Failure of this condition is a controller NO-GO even if another phase happens to score well.

## GO rule

Return:

`GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION`

only if **all** conditions are true:

1. `recovered_state_gate` has the highest pooled mean primary precision of all four arms;
2. candidate mean primary precision is greater than each of the three controls on **every target**;
3. Holm-adjusted exact paired p `< 0.05` versus each of the three controls;
4. candidate mean final primary precision is greater than its matched starting-state precision on every target;
5. all 18 candidate trajectories satisfy the controller-use requirement;
6. candidate target-wise median final Rg/native-Rg is within `[0.75,1.25]` for every target;
7. every run preserves canonical bond lengths and bond angles to maximum drift `< 1e-8`;
8. every run passes finite-value/numerical-health checks;
9. native-information firewall tests pass on the exact implementation used for measurement;
10. source/constant hashes and exact historical proxy tests pass.

Otherwise return:

`NO_GO_RECOVERED_TOPOLOGY_GATED_PREORGANIZATION`.

## Secondary diagnostics

Report, but do not allow them to rescue a failed primary gate:

- transition step;
- historical proxy trajectory and qualifying-count trajectory;
- fraction of steps contact/electrostatic LockIn forces are active;
- final corrected Kabsch C-alpha RMSD;
- native-contact recall;
- fixed-checkpoint top-K precision;
- Rg and Rg ratio;
- energy-component trajectories;
- C-alpha pseudo-dihedral dispersion;
- hydrophobic and charged-contact counts;
- maximum covalent drift.

## Claim boundary

A GO would establish only that this frozen recovered topology-gated mechanism, translated onto a valid canonical peptide representation, produces transferable native-topology enrichment beyond its same-force nonadaptive controls under this preregistered benchmark.

It would **not** establish:

- de novo folding in general;
- a new force or physical law;
- that the historical Cartesian runs were physically valid;
- that the mixed folders are exact Patch-622/624 releases;
- superiority to modern folding methods or established force fields.

A NO-GO closes this recovered coordinate-effective controller mechanism under the present translation. It may not be rescued by post-exposure coefficient tuning, threshold changes, target substitution, seed removal, longer runs, alternate endpoints or replacement topology metrics.

## Post-exposure rule

After the first authoritative native-evaluation result is exposed:

- no coefficient search;
- no change to `8/100/50` gate thresholds;
- no step-budget extension;
- no learning-rate change;
- no target substitution;
- no seed removal;
- no favorable checkpoint selection;
- no alternate primary endpoint;
- no true-persistent-homology replacement presented as the same historical mechanism.

Any such change is a new hypothesis and requires a new preregistration.
