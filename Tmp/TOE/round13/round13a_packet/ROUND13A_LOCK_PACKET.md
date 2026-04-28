# Round 13A Lock Packet
## Scaling Relations Moonshot — Gas-Side Pilot

## Status
This packet documents the locked corpus and runnable evaluation used for Round 13A.

## Scope
Round 13A is a **gas-side scaling pilot**.
It is not yet the final full BTFR moonshot because the current locked corpus does not contain a real stellar decomposition layer.

## Locked corpus
- Source basis: strict locked public WALLABY subset carried forward from the Round 12 external track
- No-SPARC-overlap rule preserved
- Same locked galaxies used to generate the Round 13A corpus
- Corpus file: `round13_locked_corpus.csv`

## Current corpus contract
Each radial row contains:
- `galaxy`
- `source`
- `Rad`
- `Vobs`
- `Vgas`
- `Vdisk`
- `Vbul`
- `Mgas_total`
- `Mstar_disk_total`
- `Mstar_bul_total`

### Important note
In this gas-side pilot:
- `Vdisk = 0`
- `Vbul = 0`
- `Mstar_disk_total = 0`
- `Mstar_bul_total = 0`

Therefore:
- RC scoring is meaningful
- RAR scoring is meaningful as a gas-side pilot
- BTFR remains provisional until a stellar layer is added

## Round 13A scoring criteria
Round 13A gas-pilot success criteria:
- positive aggregate RC improvement
- zero catastrophic failures preferred
- RAR scatter improvement relative to baryonic baseline

## Round 13A result
- positive win rate: 0.70
- mean RMSE improvement: +6.557220252625269
- catastrophic failures: 0
- RAR baryonic scatter: 0.18739351289487285
- RAR Bridge scatter: 0.1392224247309576

## Interpretation
Round 13A is counted as a success under gas-pilot criteria.
It demonstrates:
- stable scaffold
- locked corpus execution
- positive RC aggregate behavior
- improved RAR scatter

It does not yet constitute a full BTFR claim.

## Next step
Round 13B / full Round 13 should add a real stellar mass layer and then rerun:
- RC
- BTFR
- RAR
under frozen rules.