# Protein P8A — Authoritative Patch-622/624 source-mechanism certification

**Decision:** `REOPEN_RULE_SATISFIED_DISTINCT_HISTORICAL_MECHANISM_SOURCE_LEVEL`

**Authoritative launch/source head:** `f5966461bc4f1db6f9ab3fba7738bc5cbcb063ac`  
**GitHub Actions push run:** `35357274229` — SUCCESS  
**Job:** `105639581724` — SUCCESS  
**PR confirmation run:** `35357281592` — SUCCESS  
**Artifact:** `10552352159`, `protein-p8-source-certification`  
**Artifact SHA-256:** `529056e02ac32276ccc2b2c4e7be0504796eb22687f89cc3a703900f7a459ba5`  
**Draft PR:** `#32`

## What changed after P7

P7 remains correct for the exact StableDAGPhysics source it certified. P8A establishes that P7 did **not** exhaust the recoverable historical early-DAG lineage.

The newly recovered Patch-622/623 bundle and Patch-624/625-adjacent bundle satisfy the post-P7 reopen rule because their executable mechanism is materially different:

1. `Compaction` is not skipped at step 0.
2. Under the fixed continuously qualifying Betti fixture, Compaction remains active through step 98 and first transitions to `LockIn` at step 99.
3. The recovered fractal-compaction energy has a direct, nonzero coordinate-gradient path.
4. Patch-622/623 `LockIn - Compaction` is exactly:
   - `contact_springs`
   - `screened_electrostatics`
5. Patch-624/625 additionally activates `torsional_incoherence_penalty`.

This directly contradicts applying P7's StableDAGPhysics reduction—step-0 phase skip, non-gradient fractal offset, contact-springs-only late addition—to the entire historical DAG lineage.

## Exact certified mechanics

For the fixed synthetic audit fixture:

- Patch-622/623 fractal coordinate-gradient norm: `2683.2815729997474`
- Patch-622/623 electrostatic coordinate-gradient norm: `0.042666948611742486`
- step 0 active parameters include `k_df_funnel` and exclude contact/electrostatic activation;
- step 99 active parameters add `k_contact_spring_base` and `k_electrostatic_base`.

The Patch-624/625 torsional-incoherence penalty is real in the active DAG force set, but its recovered runner computes `phi_rms` through `.item()`. In the isolated audit the penalty therefore has:

- direct coordinate gradient: **none**
- gamma gradient: `1.5999999046325684`

It must not be described as an additional direct coordinate force.

## Important lifetime nuance

The recovered `MetricsHistory.get_betti1_lifetime()` implementation counts how many retained Betti-history entries meet the threshold. It does **not** require a strictly consecutive run. The certified step-99 trace is therefore the exact result for the preregistered continuously qualifying fixture, not a claim that the source implements a mathematically strict 100-step consecutive lifetime.

## Provenance boundary

The Drive folders are mixed historical snapshots, not clean release archives:

- `GlobularFoldQIS` — Drive folder `1kYk-we-NgI_Fbg_BG8IY1InFXnzEkxRU`
- `StableGlobularQISBest` — Drive folder `1xW0FbrtXCR048VfdS7Hi01QvjTezDljk`

The exact file IDs and SHA-256 hashes are frozen in `P8_RECOVERED_SOURCE_MANIFEST.json`.

Representative source identities:

- Patch-622/623 runner: Drive `1zibfebFh0-iQMkXZyDoBmdjLNYqUsbNG`, SHA-256 `7c461d6cb91531caf71b78c92e90244ba41b87323748e37c507670fb54ef94b3`
- DAG: Drive `1ojCa7wWaqzt9u3etrA8_YLkiVFbxpz8d`, SHA-256 `ee2d2f3148105815e0670b83d7dc62427e4637f732539343943506fe29b9b91e`
- force field: Drive `1D82b07r8qjV923QsLpYP8CF-m1Pr10WP`, SHA-256 `69dde0b4a4de06798963c7bc489b13143cb2c5bf70b500fa1b420347f52230ce`
- Patch-624/625 DAG: Drive `1soTZT-k6-xIw56JZ-e-guxzvT-Uwoo93`, SHA-256 `1eccbcdd4367db5ee63459e631657e634788387208d113eb7713880b2c08b43f`
- Patch-624/625 force field: Drive `1CEi0STjaoBYloTn58FfhMduZkm8rBtLg`, SHA-256 `1aa99c3e681c1c9a8c9e591e2c514e3762ed568b2fc5d2725313aa3b97578935`

No raw historical Patch-622/624 execution log has yet been recovered.

## Scientific consequence

The correct state is now:

```text
P7 StableDAGPhysics source reduction                  VALID
P7 as exhaustive historical-DAG classification       SUPERSEDED
PATCH-622/624 DISTINCT HISTORICAL MECHANISM           SOURCE-CERTIFIED
HISTORICAL FOLDING SUCCESS                            UNVERIFIED
P8B PROSPECTIVE MECHANISM TEST                        AUTHORIZED
```

P8B must be prospectively specified on a physically constrained peptide backbone. It may test whether the recovered mechanism produces useful native-blind preorganization, but it must not restore the invalid unconstrained Cartesian historical representation or inherit a GO from retrospective folding claims.
