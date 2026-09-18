# Historical UFI / Foldability-Predictor Audit

**Audit date:** 2026-09-17  
**Repository source:** `proteinfoldingengine/UQCF-GEM`  
**Archive destination:** `proteinfoldingengine/WetLabEngine`

## Decision

```text
NO_GO_HISTORICAL_UFI_FOLDABILITY_CLAIM
PRESERVE_ENGINE_SPECIFIC_INITIAL_COMPACTION_CORRELATION
```

The historical Universal Foldability Index (UFI) headline is numerically reproducible from the exact archived 1PGB deep-scan table, but it does not survive source-level scientific audit as evidence for a distinct topology-based foldability predictor.

The strongest bounded surviving observation is that, within the historical engine, initial compaction strongly correlates with the scalar endpoint produced by its deterministic quench.

That observation is not enough to establish a transferable foldability law.

## Exact historical evidence recovered

The original private UQCF-GEM repository still contains the raw 1,000-seed 1PGB table:

`deep_scan_results/1PGB/deep_scan_results_1PGB.csv`

The file first appears in commit:

`919c3a439001ce785992dc6b24850571c5858098`  
date: 2025-08-31T03:46:33Z  
message: `updated to engine`

Exact Git blobs at that generating commit:

- 1PGB CSV: `63680cbde41a230f458651c99effe8305731516c`
- `run_discovery_protocol.py`: `c5e4d4385e3e76b3107fb16b3049d277adc81643`
- `main_engine_wrapper.py`: `2cdeec5d69341f24266b289da5dd68f668b8ef1f`
- `physics_metrics.py`: `087d90e1727b1dbddec33e7e7b6538be89989136`

The later historical UFI validator is:

`validate_ufi_on_1pgb.py`

and its archived blob in the reviewed repository snapshot is:

`77019bfad2cc50230d3e3df532f50c6eec0b5912`.

## Historical UFI formula

The validator uses only two quantities from the 1PGB table:

- `initial_Betti1`
- `initial_Rg`

with:

```text
Betti1 weight       = 1.5
Rg-proximity weight = 1.0
Rg sweet spot       = 8.3 A
```

Both inputs are min-max normalized over the analyzed dataset.

The historical UFI is:

```text
UFI =
1.5 * normalized(initial_Betti1)
+
1.0 * [1 - normalized(abs(initial_Rg - 8.3))]
```

The reported endpoint is `final_RMSD`.

## Numerical reproduction

The exact 1PGB dataset contains:

- 1,000 rows;
- seeds 0 through 999;
- initial Rg range: 5.7453 to 21.0213;
- reported final RMSD range: 8.7035 to 24.1401.

Independent recomputation gives:

| predictor | Pearson r vs historical final_RMSD |
|---|---:|
| historical UFI | **-0.6913947** |
| initial Rg alone | **+0.7547364** |
| abs(initial Rg - 8.3) alone | **+0.7491307** |
| historical `initial_Betti1` alone | **-0.5355636** |

Thus the historical `r approximately -0.69` headline is numerically real.

However, the composite UFI is **weaker than initial Rg alone** on the same dataset.

A deterministic 10-fold out-of-fold normalization check gives UFI `r = -0.6916102`; therefore full-dataset min-max normalization is not the main reason for the correlation.

## Transfer check on 1QYS

The same repository contains an independent 1,000-seed 1QYS deep scan:

`deep_scan_results/1QYS/deep_scan_results_1QYS.csv`.

Using the **frozen 1PGB UFI formula**, including the 8.3-A target, 1PGB weights and 1PGB normalization constants, gives:

| predictor | Pearson r vs historical 1QYS final_RMSD |
|---|---:|
| frozen 1PGB UFI | **-0.6328745** |
| same formula re-normalized on 1QYS | -0.6359342 |
| initial Rg alone | **+0.7385254** |
| abs(initial Rg - 8.3) alone | **+0.7394523** |
| historical `initial_Betti1` alone | -0.4829781 |

The relationship therefore transfers in a bounded sense across these two archived engine datasets.

But again, the UFI composite does **not** beat the simple Rg predictor.

## What historical “Betti1” actually measures

At the exact 1PGB generating commit, `physics_metrics.compute_betti1_count` does not compute persistent homology or a general first Betti number.

It:

1. creates an 8-A contact graph;
2. removes self and adjacent-chain contacts;
3. counts contact edges;
4. returns:

```text
max(0, total_contacts - (N_residues - 1))
```

under an explicit assumption that the graph has one connected component.

This is effectively an **excess-contact-count / compaction proxy**, not an independently calculated topological invariant.

In the archived datasets it is strongly correlated with Rg:

- 1PGB: `corr(initial_Rg, initial_Betti1) = -0.7742155`
- 1QYS: `corr(initial_Rg, initial_Betti1) = -0.6932165`

After controlling for Rg, the partial correlation of the historical Betti-like quantity with the endpoint is:

- 1PGB: **+0.1174455**
- 1QYS: **+0.0596375**

The sign also reverses relative to the raw correlation.

Therefore the historical evidence does not establish meaningful incremental predictive information from topology beyond compaction.

## Load-bearing endpoint defect

The 1PGB table itself was created with the historical RMSD routine that is already independently known to fail rigid-rotation invariance.

At the exact generating commit, `run_discovery_protocol.py` calls:

`main_engine_wrapper.run_deterministic_relaxation(...)`

which computes the endpoint using:

`physics_metrics.compute_rmsd(model.CA_coords, native_ca_coords)`.

The exact historical `compute_rmsd` implementation:

1. centers the coordinate matrices;
2. computes `H = X1_c.T @ X2_c`;
3. performs SVD;
4. constructs `R = Vt.T @ D @ U.T`;
5. applies it as the row-vector transform `X1_c @ R`.

That mixes a column-vector Kabsch rotation expression with row-vector application.

Independent rigid-transform controls already demonstrated that this implementation can report a large nonzero RMSD for a structure changed only by rigid rotation/translation.

Therefore the `final_RMSD` column in the historical 1PGB deep-scan CSV is **not a validated Kabsch RMSD endpoint**.

## Why the archived CSV cannot be repaired directly

The deep-scan path records:

- seed;
- initial Rg;
- initial Betti-like contact count;
- scalar final RMSD.

The wrapper returns only the final scalar RMSD from Stage 2.

The 1,000-row table does not contain the final coordinates required to recompute a correct rigid-alignment RMSD.

Thus a corrected historical outcome cannot be recovered from this CSV alone.

Re-running the same historical engine would not be a clean repair because separate audits already established major physical-backbone and representation defects in that lineage.

## Scientific interpretation

What survives:

1. The archived numerical claim `r approximately -0.69` is reproducible exactly enough to be taken seriously as a historical computation.
2. Initial compactness is strongly associated with the later scalar endpoint generated by the historical deterministic quench.
3. That association is present in both the 1PGB and 1QYS archived tables.

What does **not** survive:

1. UFI outperforms a simple compactness predictor — **false in both audited datasets**.
2. Historical `Betti1` provides strong independent topological information — **not supported**.
3. The endpoint is validated native RMSD — **false for this generating source**.
4. The archived result proves a transferable foldability classifier — **not established**.
5. The result supports a novel protein-folding mechanism — **not established**.

The strongest bounded conclusion is:

> The historical deep-scan engine exhibits a strong relationship between initial compaction and its downstream scalar outcome, but the archived UFI composite does not add predictive value over Rg alone and was evaluated against a defective RMSD implementation.

## Decision path

Do **not** launch a new protein-mechanism gate to rescue historical UFI.

A future foldability-prediction study would need to begin independently with:

- physically valid peptide trajectories;
- corrected geometry-invariant endpoints;
- predictors frozen before outcome exposure;
- simple baselines such as Rg and starting RMSD;
- topology calculated by a defensible method if topology is claimed;
- held-out proteins, not only held-out seeds;
- explicit incremental-value tests against compactness;
- no target-specific sweet-spot tuning on the evaluation protein.

That would constitute a new predictive-science project, not continuation evidence for the historical UQCF-GEM mechanism program.
