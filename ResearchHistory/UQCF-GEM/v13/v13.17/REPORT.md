# UQCF-GEM v13.17 — Recoverability-to-QMAR Geometric Error Propagation Gate

**Date:** 2026-09-12

## Adjudication

v13.16's state-level recoverability error now propagates into explicit retained-geometric error bars.

On a conditioned stratum with local qubit eigenvalue floor `mu>0` and pair-correlation singular floor `gamma>0`, separator CMI gives certified `O(sqrt(CMI))` errors in the BKM metric, polar transport, linear nonmetricity defect, and loop holonomy.

## Exact qubit BKM bound

For `rho=(I+r.sigma)/2`,

`K(r)=a(r)I+[b(r)-a(r)]nn^T`,
`a(r)=r/atanh(r)`,
`b(r)=1-r^2`.

If `lambda_min(rho)>=mu`, then `|r|<=1-2mu` and `lambda_min(K)>=4mu(1-mu)`.

With `c(r)=[b(r)-a(r)]/r^2`, define

`L_K(mu)=sup [sqrt(3)|a'|+r^2|c'|+2r|c|]`.

Then

`||Delta K||_F <= 2 L_K(mu) T`.

Fresh random bound ratio: `0.614324180527`.

Evaluated constants: `[{'mu': 0.02, 'Rmax': 0.96, 'K_eigen_floor_kappa': 0.0784, 'BKM_Frobenius_Lipschitz_LK': 7.239763950504676}, {'mu': 0.05, 'Rmax': 0.9, 'K_eigen_floor_kappa': 0.19, 'BKM_Frobenius_Lipschitz_LK': 4.187606081395928}, {'mu': 0.1, 'Rmax': 0.8, 'K_eigen_floor_kappa': 0.36000000000000004, 'BKM_Frobenius_Lipschitz_LK': 2.7843614132664447}, {'mu': 0.15, 'Rmax': 0.7, 'K_eigen_floor_kappa': 0.51, 'BKM_Frobenius_Lipschitz_LK': 2.13280397781791}, {'mu': 0.2, 'Rmax': 0.6, 'K_eigen_floor_kappa': 0.6400000000000001, 'BKM_Frobenius_Lipschitz_LK': 1.6936027879202387}]`.

## Polar bound

Trace-distance contractivity gives

`||Delta C_ij||_F <= 18 T`.

The polar perturbation theorem gives

`||Delta O_ij||_F <= 2||Delta C||_F/[sigma_min(C)+sigma_min(C')]`.

If both singular floors are at least `gamma`,

`||Delta O||_F <= (18/gamma)T`.

Fresh random bound ratio: `0.873814729205`.

## Nonmetricity and holonomy

For `M_ij=K_j-O^T K_i O`,

`||Delta M_ij||_F <= [4L_K(mu)+36/gamma]T`.

For an m-edge loop,

`||Delta H||_F <= (18m/gamma)T`.

Fresh holonomy-product bound ratio: `0.991646513868`.

Using recoverability

`T <= sqrt(1-exp[-I(A:C|B)])`

turns all of these into explicit `O(sqrt(CMI))` geometric-locality bounds.

## Conditioning boundary

The theorem is deliberately restricted to a regular stratum.

As `mu->0`, support/rank-change destroys uniform BKM regularity.

As `gamma->0`, polar transport becomes ill-conditioned or nonunique.

Those are structural singular boundaries, not fit parameters.

## Source-trajectory boundary

A one-slice CMI bound does not certify a whole arbitrary ETL/PGRL source trajectory.

The v13.16 parity-hidden family with a non-clique source shows strong CMI amplification, reaching a maximum amplification factor of `32535.894` in the executed controls.

Therefore a finite source trajectory is certified only if CMI and the two conditioning floors remain uniformly controlled along the path.

Under

`I_s<=I_*`, `mu_s>=mu_*`, `gamma_s>=gamma_*`

the same geometric bounds hold at every source value.

What remains open is an infinitesimal QMAR-jet theorem: static recoverability alone does not control derivatives of the recovery/hidden-completion map.

## Status

- recoverability -> BKM geometry: **CLOSED CONDITIONAL**
- recoverability -> polar connection: **CLOSED CONDITIONAL**
- recoverability -> nonmetricity: **CLOSED CONDITIONAL**
- recoverability -> holonomy: **CLOSED CONDITIONAL**
- scaling: **O(sqrt(CMI))**
- finite source trajectory: **CERTIFIED WITH UNIFORM CMI + CONDITIONING**
- infinitesimal QMAR jet locality: **OPEN**
- Pillar 3: **OPEN**

No broad scientific breakthrough is declared.

This is a **major certified approximate geometric-locality theorem**.

## Next — v13.18

### Source-Conditioned Recoverability / QMAR Jet Locality Gate

Test whether source-conditioned recovery controls `dot K`, `dot O`, `dot M`, and `dot H`, rather than only finite state slices.

If this requires genuinely new tangent-level hidden-completion data, freeze approximate locality at the finite-trajectory level.
