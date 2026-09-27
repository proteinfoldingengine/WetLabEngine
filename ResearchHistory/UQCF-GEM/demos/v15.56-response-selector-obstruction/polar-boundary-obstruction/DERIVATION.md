# v15.82 — Canonical polar continuation at a physical source boundary

Parent: 8ef3c4388dffcd0b799578600246808e5aa14c2e.
This is a diagnostic of the v15.81 failure, selected after that result;
it is not a new held-out source-law discovery or a rescue of its NO.

## Exact path from the frozen channel

Keep candidate 46, lambda=-1, P=ZII, Q=XXI and A=(P-Q)/sqrt(2).
For ordered source strength u>=0 set q=exp(-2u). Then
rho(q)=(1+q)rho/2+(1-q)A rho A/2.
A is Hermitian unitary. The channel is CPTP and its density lower bound
is at least the original minimum eigenvalue at every q in [0,1].
The strength is an ordered update label, not fundamental time.

The complete complex entries of the selected binary64 matrix are treated
as exact binary rationals. A rho A=(P-Q)rho(P-Q)/2 is then rational too.
Each one-body moment and pair moment is affine in q. Consequently the
connected source-edge matrix C(q) is polynomial of degree at most two,
and det C(q) is a rational polynomial of degree at most six. Exact rational
root isolation can distinguish a genuine simple zero from SVD roundoff.
Identity checks against the original complex channel guard transport.
The exact theorem is about the stored finite-precision input, not an
unavailable infinitely precise preparation.

## Structural obstruction

For nonsingular real C, its unique orthogonal polar factor is
O=C(C^T C)^(-1/2), with det O=sign(det C). Opposite determinant signs
lie in disconnected components of O(3). Thus a determinant sign crossing
precludes any continuous orthogonal extension that agrees with this
canonical factor on both regular sides. An atlas change using continuous
local SU(2) frames induces SO(3) endpoint matrices and preserves the sign;
it cannot remove this obstruction.

At a simple determinant zero with rank(C)=2, the canonical partial
isometry V0 is unique with kernel equal to ker C. The two one-sided full
polar limits agree on the two-dimensional support and differ by sign
on the missing one-dimensional sector. Their difference has singular
values (2,0,0); each differs from V0 by a rank-one term of norm 1.
This permits a support-defined value at the singular slice, but does not
make the full orthogonal link continuous. The finite-gap numerical ladder
checks the approach to this theorem, rather than defining an extrapolated
fit. No reflection-corrected SO(3) observable is substituted.

The singularity may occur on the source edge even though its entire
hidden-to-retained tangent is zero. Check all 27 hidden Pauli directions
against all 15 nonidentity observables supported on that edge exactly.
This separates changing the baseline retained matrix along the source
path from differentiating that state with respect to hidden input data.
No Q/E response is assigned at the singular point.

## Boundary of the conclusion

An obstruction to continuous canonical orthogonal polar transport is not
an obstruction to quantum positivity, CPTP composition, or all conceivable
geometric extraction laws. Partial-isometry/support descriptions may still
be meaningful. This does not select a physical source law or alter an
exterior admissible-world slice. Genesis Pin, ordered recoverability and
historical verdicts remain unchanged. No gravity derivation is claimed.
