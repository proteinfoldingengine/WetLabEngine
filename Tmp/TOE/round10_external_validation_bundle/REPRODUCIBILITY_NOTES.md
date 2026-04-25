# Reproducibility Notes

## Script Categories
1. External rotation-curve reconstruction from THINGS `mom0/mom1/mom2`
2. Gas proxy extraction from cumulative `mom0`
3. Disk proxy extraction from SINGS / IRAC1
4. Frozen Bridge evaluation on progressively externalized pilot tables

## Best Geometry Values Found

### DDO154
- `PA = 135 deg`
- `incl = 66 deg`
- `vsys = 380.559 km/s`

### NGC 2403
- `xc = 1020`
- `yc = 1021`
- `PA = 42.8 deg`
- `incl = 62.3 deg`
- `vsys = 107.0 km/s`

### NGC 3198
- `xc = 541`
- `yc = 542`
- `PA = 15 deg`
- `incl = 50 deg`
- `vsys = 595.0 km/s`

## Methodological Rule
Geometry refinement is upstream of Bridge:
- bad geometry -> no fair Bridge verdict
- good geometry -> meaningful Bridge comparison
