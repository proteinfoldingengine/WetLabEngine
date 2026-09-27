# v15.78 — Fixed-law covariance without source data

Parent: fdc9c239491d952672457e1ff994fbca7d4b4ed8 (v15.77).

## The extra hypothesis

Let Phi be one fixed linear map on three-qubit operators. Require
Phi Ad_U = Ad_U Phi for every independent local U in SU(2)^3,
without transforming any source parameter. This is stronger than the
source-indexed covariance Phi_{U d}(U z U†)=U Phi_d(z) U† used earlier.
The latter allows a source tensor, reference, generator, or hidden probe to
transform as data; it is not refuted here. No assertion is made that the
stronger hypothesis is a required physical principle.

## Exact obstruction before geometry

Use the 64 Hermitian Pauli tensors e_p=P_p/sqrt(8), including identity.
Local conjugations by X and Z at each of three sites give six commuting
sign actions. Their joint characters distinguish all 64 Pauli tensors:
at one site I,X,Y,Z have characters (+,+),(+,-),(-,-),(-,+).
In the real Pauli transfer matrix L, covariance imposes
(chi_g(p)-chi_g(q)) L_pq=0. Thus L is diagonal.
For the hidden-to-retained block, p has weight 1 or 2 and q has weight 3;
p and q differ. Each of its 36*27=972 entries therefore vanishes.
The diagonal Gram entries of these six constraint equations are positive
integers sum_g(chi_g(p)-chi_g(q))^2. No tolerance or fitted rank is needed.
This excludes retained leakage itself, before any polar-skew calculation.

Independent local rotations also connect X,Y,Z on each occupied site.
Their orbits have fixed support S subset {0,1,2}; dimensions are
1,3,3,3,9,9,9,27. The commutant is scalar on each of eight inequivalent
support sectors. TP sets the identity scalar to 1; unitality follows.
These are linear commutant dimensions, not a claimed characterization of
all CP inequalities. Composition preserves this block structure and closure.

## Independent covariance projection

The orthogonal/Haar projection of any Pauli transfer matrix is diagonal,
with diagonal coefficients averaged over each fixed-support sector.
An independent construction averages Ad_U^{-1} Phi Ad_U successively
at each site over the 24 proper signed axis permutations (local Clifford
adjoint rotations). This finite group has the same commutant as SU(2)^3,
so its orthogonal group average equals the Haar projection on linear maps.
Each summand conjugates a channel by unitaries; the average remains CPTP.
We verify agreement of these two constructions and generic local-rotation
commutators. This is a mathematical symmetry control, not an alignment
procedure on data and not a proposed physical source process.

## Controls inherited from certified work

For each of the same 12 reference states, freeze Y=global_lift(rho),
A=XXX, b=rho+0.02Y, kappa=0.01. Then
Phi_null(z)=Tr(z)b+kappa Tr(Az)Y is the v15.77 active symmetric channel.
It is CPTP via preparations b±kappa Y and effects (I±A)/2.
Its derivative on hidden h has retained leakage but polar-skew null at
its calibration state. Its covariance projection is complete depolarization:
all nonidentity translation and hidden-to-retained entries are off diagonal.

The positive control is Phi_unitary(z)=U z U† with
U=cos(pi/8)I-i sin(pi/8)XXI (the v15.73 generator, finite angle pi/4).
On hidden probes, its retained component is sin(pi/4) times that generator's
commutator response, hence retained rank 12 and Q/E rank 6 at each reference.
Its covariance projection need not be depolarizing, but has zero retained
hidden response. Identity is a third retained-closed control.

Measure X=Phi-id and DX[h]=Phi(h)-h at the original reference rho;
these are source-vector-field tangents, not polar derivatives at Phi(rho).
No finite-output polar regularity is assumed or needed: depolarization has
singular correlations, but the derivative is evaluated at the regular input.
The twirled channel's absence of retained hidden information is exact and
independent of this choice of evaluation point.

## Interpretation boundary

If verified, strict source-free covariance removes the null construction
by also removing the desired hidden-to-retained signal. It does not select
skew-producing laws among leaking sources. Covariant source data remain
legitimate and are the next representation-theoretic issue. Reference-free
must not be conflated with source-data-free. Prior NOs remain unchanged.
This is a finite-dimensional structural obstruction, not new gravity,
source-law selection, or a mechanism changing admissible worlds. Genesis
Pin remains foundational. Ordered source labels do not introduce fundamental
time; geometry remains a retained observable, not an inserted primitive.
