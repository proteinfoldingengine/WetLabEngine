# Input Contract — Round 12 Frozen Runner

## Required input format
The frozen runner expects one CSV per galaxy.

## Required columns
- `Rad` : radius in kpc
- `Vobs` : observed rotation velocity in km/s
- `Vgas` : gas contribution in km/s
- `Vdisk` : stellar disk contribution in km/s
- `Vbul` : bulge contribution in km/s

## Optional columns
- `errV` : observational uncertainty in km/s
- `galaxy` : galaxy identifier

## Units
- Radius: kpc
- Velocities: km/s

## Assumptions
- Rows are ordered by increasing radius
- Missing values are allowed only outside the scored region
- Negative gas entries may appear and are preserved in the baryonic construction rule via signed `Vgas^2`

## Output per galaxy
The runner must emit:
- `galaxy`
- `n_points_used`
- `rmse_baryonic`
- `rmse_bridge`
- `improvement`
- `positive_improvement`
- `catastrophic_failure`
- `notes`

## Output aggregate
The scorer must emit:
- number of galaxies
- positive improvement rate
- mean RMSE improvement
- catastrophic failure count
- per-galaxy table
