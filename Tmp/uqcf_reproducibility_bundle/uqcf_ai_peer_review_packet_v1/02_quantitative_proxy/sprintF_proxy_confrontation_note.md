# Sprint F — First quantitative proxy confrontation

This note compares the locked bridge proxy to DESI DR2 anisotropic BAO points using

F_AP = D_M / D_H

constructed from the published DESI DR2 mean vector and covariance already present in the workspace.

## What is compared

For each anisotropic BAO redshift with both D_M/r_d and D_H/r_d available, we compute:

1. data-side F_AP(z) = (D_M/r_d)/(D_H/r_d)
2. propagated sigma[F_AP(z)] from the published covariance block
3. baseline proxy F_AP^0(z) from the flat-LCDM reference proxy with Omega_m = 0.30
4. bridge proxy ratio F_AP^bridge(z)/F_AP^0(z)
5. data-side ratio F_AP^data(z)/F_AP^0(z)

The comparison is therefore ratio-based and r_d-independent.

## Proxy score

- n points = 6
- proxy chi2 = 6.831
- proxy reduced chi2 = 1.139
- RMS residual = 2.608% 

## Scope note

This is a first quantitative proxy confrontation, not a full DESI likelihood analysis.
