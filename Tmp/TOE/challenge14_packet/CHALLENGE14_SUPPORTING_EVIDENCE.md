# Challenge 14 Supporting Evidence

## Aggregate Summary
- n = 171
- n_exception_flagged = 0
- positive_improvement_rate = 0.9415204678362573
- mean_hybrid_improvement = 15.33268559946402
- catastrophic_failures = 0

### BTFR
- observed scatter RMSE = 0.10993146042311981
- bridge scatter RMSE = 0.10310158244409962

### RAR
- baryonic scatter RMSE = 0.3901826147286833
- bridge scatter RMSE = 0.18175595069131176

## Top 20 galaxies by improvement
| galaxy | distance_mpc | n_points | stellar_fraction_proxy | improvement_13a_local | selected_model | exception_flag | hybrid_improvement | vflat_obs | vflat_bridge | m_baryon | catastrophic_failure |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---|
| UGC02487 | 69.10 | 17 | 0.983178 | 71.219661 | 13A_default | False | 71.219661 | 331.00 | 280.012575 | 1144418.1530 | False |
| NGC2841 | 14.10 | 50 | 0.959144 | 56.325178 | 13A_default | False | 56.325178 | 283.00 | 233.941498 | 2784859.4167 | False |
| UGC12506 | 100.60 | 31 | 0.873063 | 51.248323 | 13A_default | False | 51.248323 | 233.00 | 202.208572 | 732462.8298 | False |
| NGC5985 | 39.70 | 33 | 0.981887 | 49.642844 | 13A_default | False | 49.642844 | 291.50 | 263.439181 | 1415060.6738 | False |
| NGC6674 | 51.20 | 15 | 0.955433 | 44.745535 | 13A_default | False | 44.745535 | 242.00 | 204.362005 | 507313.7356 | False |
| UGC02885 | 80.60 | 19 | 0.936456 | 43.027248 | 13A_default | False | 43.027248 | 298.00 | 261.509661 | 1042031.3600 | False |
| UGC00128 | 64.50 | 22 | 0.642539 | 42.323608 | 13A_default | False | 42.323608 | 130.00 | 102.830153 | 69693.5946 | False |
| F563-1 | 48.90 | 17 | 0.555138 | 37.205105 | 13A_default | False | 37.205105 | 111.25 | 86.392247 | 21438.0225 | False |
| F563-V2 | 59.70 | 10 | 0.654886 | 33.195791 | 13A_default | False | 33.195791 | 118.00 | 95.848274 | 18272.6678 | False |
| UGC07399 | 8.43 | 10 | 0.759518 | 33.118971 | 13A_default | False | 33.118971 | 103.00 | 81.150956 | 15706.6101 | False |
| F568-V1 | 80.60 | 15 | 0.832657 | 32.327111 | 13A_default | False | 32.327111 | 112.00 | 90.341031 | 29080.5433 | False |
| UGC06786 | 29.30 | 45 | 0.988276 | 31.957272 | 13A_default | False | 31.957272 | 226.50 | 194.672168 | 1518623.7195 | False |
| ESO563-G021 | 60.80 | 30 | 0.975491 | 31.545679 | 13A_default | False | 31.545679 | 313.00 | 282.274561 | 1569546.3719 | False |
| NGC3992 | 23.70 | 9 | 0.962827 | 31.203264 | 13A_default | False | 31.203264 | 241.00 | 215.231435 | 392637.4020 | False |
| NGC1003 | 11.40 | 36 | 0.775356 | 31.192506 | 13A_default | False | 31.192506 | 110.00 | 86.807600 | 123746.1537 | False |
| NGC0289 | 20.80 | 28 | 0.883784 | 29.982897 | 13A_default | False | 29.982897 | 168.00 | 142.849876 | 597863.6205 | False |
| F568-1 | 90.70 | 12 | 0.746117 | 28.818108 | 13A_default | False | 28.818108 | 131.50 | 107.169974 | 28281.1049 | False |
| UGC01230 | 53.70 | 11 | 0.682665 | 28.422090 | 13A_default | False | 28.422090 | 104.00 | 87.814187 | 30536.6197 | False |
| NGC6015 | 17.00 | 44 | 0.910337 | 28.046810 | 13A_default | False | 28.046810 | 157.00 | 131.935715 | 557131.0863 | False |
| NGC2915 | 4.06 | 30 | 0.780581 | 26.571311 | 13A_default | False | 26.571311 | 82.20 | 62.582426 | 32108.0125 | False |

## Worst 10 audited cases
| galaxy | hybrid_improvement | vflat_obs | vflat_bridge |
|---|---:|---:|---:|
| UGC11557 | 0.0 | 83.05 | 94.864122 |
| UGC06628 | 0.0 | 42.30 | 54.167290 |
| UGC02455 | 0.0 | 53.10 | 74.640327 |
| NGC5005 | 0.0 | 264.50 | 297.285282 |
| NGC4085 | 0.0 | 133.00 | 151.791784 |
| NGC4389 | 0.0 | 95.90 | 143.578684 |
| F574-2 | 0.0 | 36.00 | 41.778417 |
| CamB | 0.0 | 16.80 | 17.405795 |
| NGC4051 | 0.0 | 154.00 | 184.858182 |
| NGC3953 | 0.0 | 223.00 | 236.271306 |

## Failure-audit interpretation
The “worst” cases are not destructive failures.

In all ten audited bottom cases:
- improvement = 0.0
- actual_add = 0.0
- no catastrophic behavior
- no negative degradation

This means the scaffold is not breaking. It is remaining inactive in a bounded way.
