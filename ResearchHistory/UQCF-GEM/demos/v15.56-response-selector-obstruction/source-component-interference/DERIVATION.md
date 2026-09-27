# v15.81 — Matched source-component interference

Parent f7bf2826e6952dae11ae67d548423911ecf94151 (v15.80).
Freeze P=ZII, Q=XXI, P²=Q²=I and PQ=-QP. No geometry target enters the source.

## Matched physical family

Let D_A(z)=AzA†-{A†A,z}/2. Define
L_lambda=.5(D_P+D_Q)+lambda C, C(z)=.5(PzQ+QzP), -1<=lambda<=1.
The cross anticommutator vanishes because PQ+QP=0. In the specified P,Q
component basis the coefficient matrix is Gamma=.5[[1,lambda],[lambda,1]],
which is positive semidefinite with trace1. All arms have identical diagonal
component rates .5,.5. At lambda=0 the generator is the incoherent sum of
the two individual dissipators. Both components remain active. This matches
diagonal rates, not total superoperator norm or all baseline observables.

Set a_plus=(P+Q)/sqrt(2), a_minus=(P-Q)/sqrt(2), and r_plus/minus=(1±lambda)/2.
Then L_lambda=r_plus D_a_plus+r_minus D_a_minus. These are Hermitian unitary
jumps, so the family is CPTP-admissible for nonnegative ordered strength.
Both source components transform as source data under local SU(2)^3.
The phrase component interference is relative to this frozen source
decomposition. A jump-basis change diagonalizes Gamma without changing the
channel; no basis-independent measure of Lindblad coherence is claimed.
C alone is an algebraic difference, not an admissible source generator.

## Exact hidden response

Each Pauli conjugation preserves Pauli support. Thus D_P and D_Q send every
weight-three hidden tangent back into that hidden sector. Their retained
response is zero, regardless of source activity. Consequently
R L_lambda(h)=lambda R C(h).
The v15.80 witnesses and support transfer apply: C has retained rank12,
with six independent pair outputs on each of edges (1,2) and (2,0).
The source edge (0,1) is null. At a regular polar base point, each affected
edge has Q/E rank3, so the combined rank is6. At a common base point the
whole Q and E maps, not just their norms, scale by lambda. Cross-sign
reversal is physical here because Gamma remains positive.

## Finite ordered updates and composition

Let T_lambda(u)=exp(u L_lambda), where u labels ordered source strength,
not fundamental time. The adjoint involutions of a_plus and a_minus commute:
a_plus a_minus=-PQ and reversed order changes only a phase. For
p_plus/minus=(1+exp(-2 r_plus/minus u))/2, T is a mixture of the unitary
channels I,a_plus,a_minus,a_plus a_minus with weights
p_plus p_minus, (1-p_plus)p_minus, p_plus(1-p_minus),
(1-p_plus)(1-p_minus).
This gives CP, TP and exact composition without numerical ODE integration.
The incoherent finite arm is exp(u*.5(D_P+D_Q)); it is not asserted to be
the arithmetic average of two finite-strength channels.

On hidden tangents, the I and a_plus a_minus conjugations are retained-closed.
The difference of the middle two weights gives
R T_lambda(u)h = b(lambda,u) R C(h),
b(lambda,u)=exp(-u)sinh(lambda u).
Thus the incoherent arm remains retained-closed at every depth. Nonzero
lambda transfers hidden information after finite updates. To test actual
output-base rotational response, evaluate the analytic hidden derivative
T_lambda(u)h at center T_lambda(u)rho, not at the original rho. Q/E still
have ranks6 if that center remains in the regular proper-polar domain.
Their amplitudes need not simply rescale between arms because their centers
differ. No such cross-center amplitude equality is assumed.

## Interpretation

This experiment isolates a term of an explicit physical source family.
It does not derive why quantum/global consistency would select that family,
its source components, or lambda. Matched component activation is not enough
if the cross term changes retained leakage. Neither this mechanism nor its
CPTP realization changes an exterior admissible-world slice merely by acting
on a state. Historical null results, Genesis Pin, and ordered recoverability
remain unchanged. No external alignment, heuristic fitting, fundamental time,
dark-matter primitive or gravity derivation is introduced.
