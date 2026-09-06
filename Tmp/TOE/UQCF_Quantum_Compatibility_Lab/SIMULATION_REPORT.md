# Numerical reproduction report

## Scope

Fresh matrix calculations for the supplied UQCF–GEM v9.167–v9.171 matched-arrangement model. This is not an independent proof of every theorem in that sequence, a new physical law, or an experimental result.

## Results from this run

| Check | Result |
|---|---:|
| Distinct target parameters | 171 |
| Primal–dual comparisons | 342 |
| Maximum A/B distance difference | 1.110223024625e-16 |
| Maximum primal–dual discrepancy | 5.164271787983e-15 |
| Fixed parameter | 21/41 |
| Distance at fixed parameter | 0.012373971022 |
| Exact A map rank / real affine nullity | 310 / 315 |
| Exact B map rank / real affine nullity | 314 / 311 |
| Hidden samples per arrangement | 144 |
| Maximum pair-entry drift in hidden samples | 6.938893903907e-18 |
| Maximum pure-extension recovery error | 2.886579864025e-15 |
| Local-unitary covariance error | 1.463577947914e-16 |

The smallest retained singular values in the numerical kernel calculation exceed 0.135, while discarded singular values are approximately 1e-15. Both numerical dimensions agree with the exact field-arithmetic calculation.

## Operational example within arrangement A

The selected collective yes/no measurement has probabilities 0.480269472133 and 0.465533202124 for two distinct hidden completions. Their difference is 0.014736270010. The corresponding global trace distance is 0.014736270010; agreement error is 4.510e-17. Both pair-state trace distances are below 4e-18. The measurement is a diagnostic constructed to distinguish these states; it is not an independently derived source operation.

## Interpretation

Within each arrangement, genuine global quantum distinctions remain possible while both specified pair marginals stay fixed. Across the arrangements, the scalar compatibility distances agree while the full hidden optimum families have different affine dimensions. The 3D meshes are sampled affine sections, not topological models of the entire high-dimensional families.

The parameter scan and closed display paths are prescribed illustrations of admissible static states. They do not determine physical evolution, holonomy, gravity, or source-induced deformation of admissibility.

## Formula checks

The code builds positive T and computes sigma = Tr_B2 T = Tr_B1 T, then compares

    D(rho,sigma) = (1/2) sum |eig(rho-sigma)|

to

    Tr(W rho) - (1/2) lambda_max(W_AB1 + W_AB2).

It checks 0 <= W <= I, normalization, positivity, equal marginals, local marginals and covariance. Hidden state samples also undergo a second full-matrix partial-trace check independent of their cached coefficient marginal map. A normalized amplitude W_pur with W_pur W_pur* = T is constructed for every sampled hidden state.
