# Protein P9 — Authoritative Retained-Coherence Transfer Result

**Decision:** `NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL`

**Scientific preregistration head:** `8f4e320b291d6fba7c43cd716e4af3f348ef27d4`  
**Authoritative measured head:** `234ab6f8357000f75c322803992a05cbbe528a02`  
**GitHub Actions run:** `35385155331` — SUCCESS  
**Job:** `105730229017`  
**Artifact:** `10563980479`, `protein-p9-authoritative-measurement`  
**Artifact SHA-256:** `0267103d8ad7e7884912183bb1525d45eed48862e6e0778ece922b743884f804`

The downloaded artifact independently hashes to the GitHub artifact digest, and every member listed in `SHA256SUMS.txt` independently verifies.

## Question tested

P9A was the final novelty-focused continuation gate for the protein/WetLabEngine program.

It tested whether the frozen v9 retained bridge/coherence history — prior `sigma_bridge` and `closure_ready` means and slopes — carries **transferable predictive information about subsequent structural progress** beyond:

- current optimization step;
- current energy;
- current `sigma_bridge`;
- current `closure_ready`;
- current radius of gyration;
- immediate prior energy change;
- immediate prior Rg change.

The test deliberately did not ask whether protein dynamics can be non-Markovian in general. That has substantial prior art. It asked whether this program's retained coherence state contains a distinct transferable signal beyond simpler current-state and ordinary-history descriptions.

The primary design trained on one protein and tested on the other, in both directions.

## Source and firewall checks

All frozen source identities passed:

- 1UAO traces: `95bf84ad9d19ee84533190787889bb1d1420c330`
- 1UAO results: `2768ccbad6c694282a689bba799d14d65c0bb0d7`
- 1L2Y traces: `819e8cecda27ba4248b64288de88d672c7b705bc`
- 1L2Y results: `aa3565a2a597ef93ba81d3d9d078cf452f29edbb`

Instance cardinalities were exactly frozen:

- 1UAO: 24
- 1L2Y: 40

The native-information firewall passed. Replacing all RMSD values leaves every predictor matrix unchanged.

## 1UAO -> 1L2Y transfer

Ordinary-history control M1:

- RMSE: `0.2518526869`
- Pearson correlation: `0.8519943085`

Retained-coherence candidate M2:

- RMSE: `0.2452414162`
- Pearson correlation: `0.8553844134`
- absolute RMSE improvement: `0.0066112707`
- relative RMSE improvement: **2.625%**
- permutation p: **0.4637681159**

The retained history moves slightly in the favorable direction, but it is far below the preregistered 10% transfer threshold and is fully compatible with the permutation null.

## 1L2Y -> 1UAO transfer

Ordinary-history control M1:

- RMSE: `0.0973889004`
- Pearson correlation: `0.6956623014`

Retained-coherence candidate M2:

- RMSE: `0.1028613036`
- Pearson correlation: `0.6872517584`
- absolute RMSE change: `-0.0054724032`
- relative RMSE change: **-5.619%**
- permutation p: **0.4877561219**

The retained-coherence features make held-out prediction worse in the reverse transfer direction.

## Frozen acceptance result

P9A required, in both transfer directions:

1. at least 10% lower M2 RMSE than M1;
2. positive retained-history improvement;
3. permutation p < 0.05;
4. M2 correlation greater than M1;
5. source/cardinality integrity;
6. native-information firewall.

Only the integrity/firewall conditions pass universally.

Therefore the frozen decision is necessarily:

```text
NO_GO_RETAINED_COHERENCE_TRANSFER_SIGNAL
```

## Scientific interpretation

The archived v9 retained coherence history does not show a transferable signal beyond the preregistered instantaneous and ordinary-history controls.

This result is stronger than merely failing an arbitrary significance threshold:

- one transfer direction shows only a 2.6% gain with permutation p ~ 0.46;
- the reverse direction becomes 5.6% worse;
- correlation also declines in the reverse direction.

There is therefore no evidence in this frozen test that accumulated `sigma_bridge` / `closure_ready` history defines a useful transferable state variable.

## Relation to earlier results

This does not erase earlier bounded observations:

- v9 and other geometric regularizers can alter trajectories;
- P6 contains a pooled real-sequence signal versus generic collapse;
- recovered historical source contains mechanisms that P7 originally reduced too aggressively;
- P8B's torsional representation transfer remains open to the calibration criticism documented after its result.

However, none of those bounded observations now supplies a sufficiently distinct, potentially novel protein mechanism for continued development.

P9A was chosen specifically because broad ideas such as folding funnels, topology/order parameters, local preorganization, and generic non-Markovian history already have substantial prior art. The retained-coherence/state-completeness hypothesis was the final archive-supported candidate that could have distinguished this program scientifically.

It did not survive held-out transfer.

## Decision consequence

P9B — matched-present-state / divergent-history prospective folding intervention — is **not authorized**.

Do not respond to this result by:

- adding more retained bridge observables;
- changing history windows;
- tuning ridge alpha;
- changing checkpoints or labels;
- selecting favorable seeds;
- recalibrating P8B merely to keep the program open;
- recombining failed components without a new independent scientific reason.

The current protein custom-mechanism research line should be closed and preserved as an audited archive.

A future reopening requires materially new evidence independent of this result, not another rescue of the existing stack.
