# v15.80 — Signed linear source data and physical tangent extensions

Parent 659c078f47f1b6732c310701bd3fd4170787fc43 (v15.79).

## Additional hypotheses, not a universal physical axiom

Consider a real-linear source assignment a -> L_a, where a is one traceless
Hermitian three-qubit source tensor. L_a is complex-linear on arbitrary
operators, Hermiticity preserving, trace annihilating, independent of the
input state, and covariant under independent local SU(2)^3 with a transformed.
Require a differentiable CPTP curve T_{epsilon,a} through the identity channel
for every a and -a, with derivative L_a and epsilon>=0 an ordered source
strength. This is source oddness L_{-a}=-L_a, not negative physical time.
The curves may have higher-order terms; I+epsilon L is NOT required to be CP.
No semigroup, inverse-curve equality, or reversible finite update is assumed.
Higher-order dissipation is not excluded by a first-order classification.

A source law quadratic or otherwise nonlinear in a is outside this class.
Sign-admissibility without linearity does not imply L_{-a}=-L_a. This
assumption is tested explicitly against a physical even-source control below.

## Full global extension before retained projection

The v15.79 retained/hidden block does not determine complete positivity.
Classify full bilinear maps L(a,z) with arbitrary input operator z instead.
At one site the allowed (source,input,output) scalar/vector triples are
000,011,101,110,111. Their tensors are scalar multiplication, identity,
vector from scalar input, dot, and cross, each with multiplicity one.
Products give 5^3=125 tensors. Excluding scalar source support removes eight,
leaving 117. Trace annihilation removes seven independent output-identity
rows, one per nonempty source support, leaving 110.

For fixed source support sizes 1,2,3, the trace-annihilating coefficient
blocks have dimensions 11,17,26 respectively (three,three,one support blocks).
All source directions are tested; no unspecified completion is set to zero
before CP constraints. Completeness follows from the local representation
multiplicities, independently checked by local Lie-algebra kernels.

## Two-sided tangent-cone argument

Use the input-first unnormalized Choi convention J(Phi)=sum_ij Eij tensor
Phi(Eij), omega=vec(I)/sqrt(8), and P=I-|omega><omega|. Since J(id) has
support span(omega), differentiability and CP for epsilon>=0 require
K_a=P J(L_a) P >=0. Applying the same requirement to -a gives -K_a>=0;
therefore K_a=0. This is a necessary first-order condition, not a finite-
Euler-map CP test.

Conversely, if L is Hermiticity preserving and trace annihilating with
P J(L) P=0, the Hermitian Choi matrix has only omega-row/column blocks.
It can be written |I>><A|+|A>><I| for a matrix A, absorbing the omega-diagonal
coefficient into A. It corresponds to L(z)=A z+z A† (up to renaming the
vectorized matrix according to the chosen input-first convention). Trace
annihilation gives A+A†=0, so L=-i[H,z] with H Hermitian. This has an exact
unitary CPTP realization. Thus these are precisely the tangent directions
that can occur with both signs. This is standard quantum-channel tangent
structure, not a new fundamental-law theorem; see the generator framework
of G. Lindblad, Commun. Math. Phys. 48,119–130 (1976),
https://doi.org/10.1007/BF01608499. The finite-dimensional argument above is
self-contained and does not identify source strength with fundamental time.

Covariance and source linearity imply H(a)=sum_{nonempty S} lambda_S a_S/2,
modulo an irrelevant identity. Each support representation occurs once.
Seven coefficients remain. In the canonical unscaled dot/cross basis the
commutator coefficients are sin(k*pi/2), where k is the number of cross
factors: +1 for one cross, -1 for three, zero for even k.
Expected conditional-Choi constraint rank: 110-7=103.

## Projection back to observable response

Project the full seven-dimensional Hamiltonian family to the v15.79
18-dimensional retained/hidden coupling coordinates. Local source supports
have zero retained hidden response. Each two-site source support fixes the
two associated one-cross coefficients together; the three-site support fixes
its three one-body-output coefficients together. The retained image has
four free coefficients, not nine independently chosen one-cross couplings.
No symmetry under permutations of qubits is additionally assumed.
The frozen ensemble can test their Q/E observability; coefficient rank four
is not an edge-geometric dimension and does not select nonzero strengths.

## Physical control outside the source-linearity hypothesis

Fix a=(ZII+XXI)/sqrt(2), a†=a, a²=I and
D_a(z)=a z a-{a²,z}/2=a z a-z. It is quadratic/even in source data:
D_{-a}=D_a, not -D_a. For epsilon=.1,
exp(epsilon D_a)=p id+(1-p)Ad_a, p=(1+exp(-2epsilon))/2,
a CPTP mixture. Its reversed-strength expression has a negative mixture
weight and is not CP. Source sign reversal remains physical and does not
reverse strength. K(D_a) has one eigenvalue 8 and all others zero;
K(-D_a) has eigenvalue -8. Hence it lies outside the two-sided *linear*
tangent class while remaining a physical one-sided source update.

For hidden YYZ/sqrt(8), its retained output is -IZZ/sqrt(8); for XXX/sqrt(8),
it is ZIX/sqrt(8). Across all hidden inputs the retained rank is 12, on edges
(1,2) and (2,0). Both edges have skew rank three; the aggregate Q/E rank is
six at regular reference states. This is an independently frozen control,
not a rescue after a failed gate.

## Boundaries

The hypotheses can narrow physical responses without choosing a physical
source mechanism. All-zero and purely local strengths remain allowed; gravity
is not forced. Nonlinear-source and state-dependent laws remain open, as do
naturality under restriction/composition and changes of admissible worlds.
Earlier null constructions and historical verdicts are unchanged. Genesis Pin
and ordered recoverability remain foundational; geometry remains retained
exhaust. No fundamental time or dark-matter primitive is introduced.
