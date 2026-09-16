# Gen3 HB1 — Gate 005 Held-Out Transfer: 1CRN

Date: 2026-09-16
Target: `1CRN` (crambin)
Held-out status: no `1CRN` occurrence was found in the project repositories before target selection.
External structure provenance: independently preserved legacy PDB `microsoft/foldingdiff:data/1CRN.pdb` at commit `8be5f8fb9b461011d80522e587fc93bdc04a12d7`.
Sequence used by the historical random-coil engine: `TTCCPSIVARSNFNVCRLPGTPEAICATYTGCIIIPGATCPGDYAN` (46 residues).
Seeds: 11, 23, 42, 57, 73, 101, 137, 211.
Conditions: dynamic contacts, contacts OFF, frozen LockIn graph, randomized matched graph, matched generic compaction.
Steps: 5000 per run.
Completed: 40/40 runs.

## Important execution note

The historical engine initializes a seeded random coil from the target sequence. For this held-out mechanism test, the external PDB establishes target identity/sequence provenance; native coordinates are not supplied to the contact mechanism or optimization objective. No target-specific force retuning was performed.

## Primary endpoint: final phi_RMS

| Seed | Dynamic | OFF | Frozen | Randomized | Generic |
|---:|---:|---:|---:|---:|---:|
| 11 | 0.372220 | 0.374563 | 0.482589 | 0.355263 | 0.536833 |
| 23 | 0.406593 | 0.341664 | 0.408387 | 0.419631 | 0.343015 |
| 42 | 0.743207 | 0.370097 | 0.457048 | 0.618862 | 0.266390 |
| 57 | 0.558057 | 0.435729 | 0.553893 | 0.432817 | 0.465370 |
| 73 | 0.486522 | 0.460700 | 0.478896 | 0.515649 | 0.432957 |
| 101 | 0.611287 | 0.502152 | 0.528554 | 0.540778 | 0.578200 |
| 137 | 0.484857 | 0.563196 | 0.579237 | 0.510270 | 0.495820 |
| 211 | 0.446033 | 0.442837 | 0.445458 | 0.472043 | 0.432721 |

Aggregate final phi_RMS:

- contacts OFF mean: **0.436367**
- generic compaction mean: **0.443913**
- randomized graph mean: **0.483164**
- frozen graph mean: **0.491758**
- dynamic contacts mean: **0.513597**

Paired results:

- frozen minus OFF: mean **+0.055391**; frozen improves in **0/8** seeds.
- dynamic minus OFF: mean **+0.077230**; dynamic improves in **2/8** seeds.
- frozen minus generic: mean **+0.047845**; frozen improves in **2/8** seeds.
- generic minus OFF: mean **+0.007546**; generic improves in **4/8** seeds.

Lower phi_RMS is treated as better angular organization, consistent with the prior gates.

## Gate decision

**NO TRANSFER.**

The Villin/1VII graph-constraint advantage does not generalize to held-out 1CRN under the frozen no-retuning protocol. The strongest preregistered contrast fails in the opposite direction: frozen contacts are worse than contacts OFF in all 8 paired seeds. Dynamic contacts are also worse on average and improve only 2/8 seeds.

Therefore the Patch-630 contact-graph mechanism must **not** be promoted into Gen3 physics on the present evidence. The correct classification is target-specific/insufficiently general rather than a demonstrated general protein-backbone mechanism.

## Scientific interpretation

This negative result is valuable because it narrows what survived the historical reconstruction:

1. The original Patch-630 Villin result is reproducible.
2. Its strong Villin angular-order effect is causally associated with LockIn contact constraints.
3. That effect can persist across Villin seeds.
4. It does **not** transfer to a genuinely held-out small protein without retuning.

Accordingly, no rescue/tuning campaign is justified under this gate. Further work should first audit whether the earlier Villin multi-seed control implementation and metrics are directly comparable to this held-out harness, then decide whether the historical mechanism is worth preserving only as a documented target-specific phenomenon.

## Boundary

This gate tests angular organization, not native-fold accuracy. The batch harness used here does not compute native-coordinate RMSD, so no RMSD claim is made for Gate 005.
