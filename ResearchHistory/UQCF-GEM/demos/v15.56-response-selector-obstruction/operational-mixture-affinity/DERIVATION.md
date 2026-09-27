# v15.72 Derivation before measurement

## Affinity as an operational discriminator

A fixed linear quantum map E obeys E(p a+(1-p)b)=p E(a)+(1-p)E(b). Thus an unconditioned CPTP operation cannot distinguish two descriptions of the same input density matrix by how they were prepared. This is direct algebra from linearity, not an assumption that every possible higher-incidence source law must be a CPTP state map.

For T_s(rho)=rho+s X_h(rho), the defect is exactly s times the vector-field Jensen defect J. A single valid nonzero witness rules out equality with a fixed affine map on any domain containing those states. It does not require testing complete positivity. Conversely, affinity alone cannot establish complete positivity.

## Why the scalar memory does not remove the issue

The v15.71 memory m_h=Tr(h rho) is linear in rho, but its field is the product m_h(rho)Y(rho). Hidden and visible data can be correlated across preparations. Retaining only their averages does not retain that correlation.

At a hidden-free base and equal mixture weight, the two endpoints are a=rho+eta h+delta v and b=rho-eta h-delta v. Their mean is rho, m_h(a)=eta, m_h(b)=-eta, and Y is independent of hidden perturbations. Therefore

    J = (eta/2)[Y(rho+delta v)-Y(rho-delta v)]
      = eta delta DY_rho[v] + O(eta delta^3).

For general weight p, the leading coefficient is 4p(1-p)eta delta. This normalization is fixed analytically, not fitted. The unequal-weight pooled base depends on v; only the equal-weight response matrix is a common-base tangent comparison.

The full v15.71 hidden derivative Y varies with visible state. A fixed affine vector field has state-independent derivative A[h]. Thus no fixed affine generator can reproduce this entire hidden-derivative assignment on an open neighborhood where DY[v] is nonzero. This is consistent with the earlier Jacobian-curl result.

## Why rotationally null branches may have a skew preparation discrepancy

Each individual source path has C_e -> O_e(P_e+c I/sqrt(3)), so its own polar rotation is fixed while positivity holds. However the *difference between two preparation procedures* has retained tangent proportional to DY[v]. At an equal-mixture base,

    D C_e[Y] = O_e/sqrt(3),
    D C_e[DY[v]] = D O_e[v]/sqrt(3).

For weight-two v the endpoint derivatives are zero. Write D O_e[v]=O_e W_e[v], W_e skew. Then the discrepancy's pre-Sylvester polar-skew projection tends to 2 W_e[v]/sqrt(3). Weight-two variations span all pair-correlation directions, predicting rank nine across the three edges. This is a preparation-procedure discrepancy, not a new source-law response or independent flow dimension.

At finite delta the normalized discrepancy only approaches this differential. The gate measures its rank and checks the equal-mixture tangent approximation at a frozen tolerance; it does not assume the numerical outcome.

## Interpretation boundaries

A conditional branch E_b(rho)/Tr(E_b(rho)) need not be affine. A controller supplied with preparation labels or state estimates also has additional inputs. An operational account of either requires explicit records, success weights and update rules; calling the nonlinear candidate CPTP would not supply them. This experiment does not rule out all conditioned or feedback mechanisms, and does not derive one.

The null-family existence statement survives. Its interpretation as a fixed unconditioned quantum operation is what this gate tests. Historical scientific verdicts and the framework's no-fundamental-time boundary remain unchanged.
