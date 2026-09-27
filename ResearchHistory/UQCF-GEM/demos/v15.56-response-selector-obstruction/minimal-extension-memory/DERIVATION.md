# v15.71 Derivation before measurement

## 1. The lost information is a 27-dimensional fiber

For three qubits, the HS-normalized nonidentity Pauli strings split by support weight. The exact-weight-three sector H3 has dimension 3^3=27.

Every h in H3 has zero one- and two-body partial traces, so H3 lies in the common kernel of the three edge restrictions. Conversely, in the 63-dimensional traceless Pauli basis, the coefficients not visible in any one- or two-body marginal are exactly the 27 weight-three coefficients.

Thus the strict marginal descent obstruction of v15.70 is a lost-fiber-coordinate problem.

## 2. Canonical memory and sufficiency

Let {h_a} be the orthonormal H3 basis and z=sigma-rho. Define

    m_a(z)=<h_a,z>_HS.

For an arbitrary source vector s=sum_a s_a h_a, the historical fixed-base response operator is

    N_s z = |Y><s| z = Y sum_a s_a m_a(z).

After restriction,

    R_e N_s z = (s·m(z)) R_e Y.

Therefore an enriched regional object carrying the ordinary marginal plus m(z) has enough information to reproduce the complete 27-label linear family.

The retained response itself does not require the global Y. v15.70 derived

    R_e Y = (1/4) sum_ab (O_e/sqrt(3))_ab sigma_a⊗sigma_b,

which is computable from the retained two-qubit state through its own polar factor O_e.

## 3. Linear-memory minimality

Suppose a linear memory map L:H3->R^k is sufficient for every source functional <s,z>, s in H3. Then whenever Lz=0, every source pairing must vanish:

    <s,z>=0 for all s in H3.

Taking s=z gives ||z||^2=0. Hence ker L={0}, so L is injective and

    k >= dim H3 = 27.

Thus the 27-coordinate memory is minimal among linear memories that must support the full source-label space. This does not say 27 coordinates are required after one source label has already been fixed; in that restricted problem one scalar pairing is enough.

## 4. Why the rebased null should integrate

The v15.63 derivative matrices A1 and Ap are actually base-independent: they are expectation derivatives of fixed Pauli observables. The minimum-norm lift Y(rho) therefore depends on rho only through the three proper polar rotations O_e(rho).

The lift has zero one-body derivative and

    delta C_e = O_e I/sqrt(3).

For a finite displacement rho_c=rho+cY(rho), connected correlations change exactly linearly:

    C_e(c)=C_e(0)+c O_e I/sqrt(3)
          =O_e(P_e+c I/sqrt(3)).

As long as the positive factor remains positive, the proper polar rotation O_e is unchanged. Since A1 and Ap are fixed and the target O_e I/sqrt(3) is unchanged, the independently recomputed minimum-norm lift must also remain unchanged:

    Y(rho_c)=Y(rho).

Because Y contains only weight-two Pauli coefficients,

    <h_a,Y>=0

for every hidden-memory coordinate. The extension memory is therefore conserved along this ordered repair family.

Consequently rebasing predicts exact additivity and order independence inside the regular positive-polar neighborhood:

    (rho + aY) + bY = rho + (a+b)Y.

The measurement is an implementation/stratum check of these exact identities, not a fitted discovery.

## 5. Scientific boundary

This construction adds explicit source/extension memory. That is exactly the missing object v15.70 says marginal state data cannot replace.

The result can show that such memory is mathematically sufficient and that the null sector survives rebasing. It cannot explain why a fundamental theory should carry these 27 coordinates, how they are selected dynamically, or whether a different higher-incidence source object is required.
