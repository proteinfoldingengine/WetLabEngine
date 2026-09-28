# v16.04 — Inserted-channel factorization of the cubic response

Status: analytic result completed; numerical audit not implemented or run. This is not a new ensemble measurement.

Parent: [v16.03 final report](../finite-source-continuation/RESULTS.md), publication commit a451398b307f89a380736186f387cf61f80718c1. The measured 48 active EB cubic cases remain the v16.03 result.

## Question and answer

Does the disjoint-source cubic coefficient require an additional order-sensitive source law?

Within the frozen model, no additional term is required: the entire cubic coefficient factors through the source–middle-channel commutators, the connected-correlation differential and the chosen readout Hessian. This is already implied by the v16.03 derivation; the contribution here is to expose the factorization and its null controls explicitly. It neither selects the source law nor excludes other physical models.

## Assumptions and notation

Retain the v16.03 states, hidden probes, preparations Q, disjoint generators A=L_A and D=L_D, and inserted channel M=M_a. Composition acts right to left. Write [X,Y]=XY-YX. Disjoint support gives [A,D]=0. The physical source maps are E_X(lambda)=I+lambda X with the inherited admissible mixture interval.

C maps a state to the five connected correlation matrices. F maps these matrices to the three loop invariants. Work only on the inherited smooth polar domain, including the fixed planar support. Let z0=Q M rho and C0=C(z0). The hidden tangent B_a is common to both orders by the inherited exact retained certificate, and is independent of lambda. All identities below are conditional on that certificate and domain.

## Exact protocol identity

Define

K_a = [D,M_a] - [A,M_a] = [D-A,M_a],

R_a = D[M_a,A] - A[M_a,D].

Expanding the two finite protocols gives exactly

E_D(lambda) M_a E_A(lambda) - E_A(lambda) M_a E_D(lambda)
= lambda K_a + lambda^2 R_a.

The quadratic identity uses [A,D]=0. There are no higher protocol powers because each source map is affine in lambda. Connected correlations and F are nonlinear, so their expansions need not terminate.

Both sources commuting with M_a is sufficient for equality of the complete protocols at every admissible lambda. K_a=0 alone does not imply R_a=0, so a cubic null does not establish a full finite-protocol null.

## Cubic factorization

Differentiating the connected centers gives

V_f - V_r = DC(z0)[Q K_a rho].

From the exact v16.03 hidden-response identity,

Delta Jphysical(lambda)
= lambda^2 (DF(C_f(lambda))-DF(C_r(lambda)))[B_a]
= lambda^3 T_a + O(lambda^4),

with the complete coefficient

T_a = D^2F(C0)[DC(z0)[Q [D-A,M_a] rho], B_a].

For each edge ij the connected differential is

DC_ij(z0)[x] = d<sigma_i sigma_j>[x]
- d<sigma_i>[x] <sigma_j>[z0]
- <sigma_i>[z0] d<sigma_j>[x].

Dropping the one-body-product terms changes the proposed coefficient and is not an admissible simplification.

By bilinearity, T_a=T_D,a-T_A,a, where

T_X,a = D^2F(C0)[DC(z0)[Q [X,M_a] rho], B_a].

These two summands are a diagnostic decomposition; they are not separately new physical protocols or separately measured effects.

## Weight-sector mechanism

Let Pi_w project onto Pauli strings of weight w. The frozen product depolarizing channel is M_a=sum_w a^w Pi_w. Therefore

Pi_v K_a Pi_u = (a^u-a^v) Pi_v(D-A)Pi_u.

Only transitions between different Pauli weights contribute. The identity sector has no couplings here: the generators are unital and trace-annihilating. Thus u,v range from 1 to 4 for nonzero blocks, and every polynomial a^u-a^v is divisible by a(1-a). Consequently K_a=a(1-a) Ktilde_a for a polynomial superoperator Ktilde_a.

This statement concerns the global commutator. It is not a universal scaling law for T_a: C0, the connected differential, B_a and the polar Hessian also depend on a. In particular, do not infer continuity or a zero polar response at a=0 from the polynomial factor. Complete erasure has undefined polar geometry.

## Necessary conditions and null controls

A nonzero T_a requires each of the following to survive the preceding map:

1. K_a rho is nonzero.
2. DC(z0)[Q K_a rho] is nonzero.
3. Its contraction with B_a under the readout Hessian is nonzero.

The converses do not hold. Nonzero commutators can cancel, a state or preparation can suppress their retained image, and the Hessian can annihilate a nonzero pair of directions.

At a=1, M_a=I, K_a=R_a=0, and the entire disjoint order contrast vanishes. This agrees with the published identity-middle control.

A fixed affine readout F_lin(C)=F(C0)+DF(C0)[C-C0] has zero Hessian. Its hidden-response contrast is exactly zero for this common-B model, at every admissible finite lambda. This is an algebraic readout diagnostic, not a replacement physical geometry.

## What this resolves

The observed v16.03 cubic response is compatible with ordinary associative channel composition plus a nonlinear geometric readout. For this coefficient there is no residual term outside the factorization above. A future numerical mismatch is an implementation, assumption or domain problem to investigate; it is not by itself evidence for new physics.

This does not establish necessity of the chosen operations, universal coupling, gravity, or a source law selected by global compatibility. Time remains pruning / ordered recoverability update. Historical INVALID outcomes remain unchanged.

## Verification and next step

The published v16.03 derivation and v15.99 exact weight-sector implementation were inspected. A dependency-free symbolic word check verified the quadratic factorization modulo [D,A]=0; all 16 nonidentity weight pairs were checked for zeros at a=0 and a=1. This is algebraic bookkeeping, not an independent proof-assistant certificate or a new scientific run.

The next numerical audit is specified in [NEXT_MEASUREMENT.md](NEXT_MEASUREMENT.md). Its purpose is to audit the implementation and localize the mechanism, not to rediscover the identity or claim new measured nonvanishing.
