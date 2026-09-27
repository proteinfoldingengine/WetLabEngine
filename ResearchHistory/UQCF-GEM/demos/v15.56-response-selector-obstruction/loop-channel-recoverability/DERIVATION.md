# v15.84 — Conditional quantum-channel interpretation of a retained loop

Parent 782ed08968e19da829e9b041d5af047af94ba588 certifies v15.83's rank-two
loop L, its raw powers and attenuation. This is a diagnostic of that
already-selected witness, not a held-out source-law experiment.

## A specified operational interpretation, not an assumed law

A node is a qubit with its inherited Pauli frame. For a real 3x3 matrix T,
the unique complex-linear unital trace-preserving extension with that
Bloch action is
Phi_T(z) = [Tr(z) I + sum_ij T_ij Tr(sigma_j z) sigma_i]/2.

This defines a candidate map, not a proof of physical implementability.
The unital choice and identification of geometric transport with a Bloch
map are explicit interpretation assumptions. They are not derived from
global consistency, and Phi_T is not the original three-qubit source
channel. A local frame change conjugates the loop at its node, so positivity
and complete positivity of this extension are frame invariant.

Use T=L^n without fitting, scaling, noise admixture or repolarization.
Since ||T||_2<=1, the Bloch ball maps into itself: the candidate map is
positive on single-qubit states. Complete positivity is stronger. Compute
the unnormalized input-first Choi matrix
J_T=sum_ab |a><b| tensor Phi_T(|a><b|), Tr(J_T)=2.
J_T/2 is the candidate map's output on half a normalized maximally entangled
pair. A negative eigenvalue directly disproves complete positivity.

## Rank-two channel criterion and constructive sufficiency

For rank-two T with singular values s1>=s2>=0, proper input/output rotations
can bring it to diag(s1,s2,0). The null singular direction permits the SVD
sign choices to be proper rotations without altering T. Direct Pauli
expansion of the Choi matrix gives eigenvalues
(1-s1-s2)/2, (1-s1+s2)/2, (1+s1-s2)/2, (1+s1+s2)/2.
Thus complete positivity requires s1+s2<=1.

Conversely, write T=sum_{a=1,2} s_a u_a v_a^T. Measure the two outcomes
along the unit Bloch axis v_a and prepare the corresponding signed pure
state along u_a. This map has Bloch matrix u_a v_a^T. Mixing those two
measure-and-prepare channels with weights s1,s2 and the completely
depolarizing channel with weight 1-s1-s2 realizes Phi_T whenever that last
weight is nonnegative. This is an explicit CPTP realization. It is also
entanglement breaking: on any joint input each measurement outcome
produces a product of a prepared qubit state and a conditional ancilla
state, so the final sum is separable. No external separability test or
fitted alignment is required. Singular axes are a decomposition of the
same operator, not a replacement observable.

v15.83's published spectra already predict non-CP powers 1,2,3 and a CPTP
power 4. The new measurement tests the explicit Choi and constructive
channel calculations, not an unanticipated spectral discovery. A physical
four-traversal block would not make the preceding elementary maps CP or
establish a CP-divisible family.

## What attenuation means if the channel interpretation passes

For the antipodal input states rho_±=(I±v_a.sigma)/2, their input trace
distance is one and output trace distance is s_a. A CPTP recovery cannot
restore both states exactly if s_a<1: positive trace-preserving maps
contract trace norm on Hermitian differences, by the Jordan decomposition
and triangle inequality. This obstruction applies even though T remains
linearly invertible between its two-dimensional initial and final images.

For these equally likely orthogonal input labels, the optimal mean fidelity
of a recovery is (1+s_a)/2. An optimal binary measurement on the outputs
followed by preparing the guessed input attains this bound. The upper bound
is the binary discrimination bound: any recovery followed by measurement
in the original orthogonal basis is another output-state discriminator.
This is a two-state witness, not an optimization over arbitrary ensembles.

The Moore-Penrose inverse T^+=sum_a v_a u_a^T/s_a recovers the initial-plane
Bloch vectors exactly. Its zero-extension unital candidate map sends a
pure output-axis state u_a to Bloch length 1/s_a>1, a nonpositive matrix.
This supplies a concrete distinction between algebraic inversion and
physically admissible recovery. The kernel-axis antipodal states map to
the same state; complete loss is confined to that input direction, not
claimed for all information.

## Boundaries

All operational conclusions are conditional on the explicit Bloch-map
interpretation. Finding a CPTP realization is a mathematical existence
result, not a physical source-law selection. Geometric links need not be
quantum channels, so non-CP links do not falsify the geometry itself.
Spatial traversal count is not fundamental time. Historical verdicts,
Genesis Pin, ordered recoverability and the distinction between a source
acting on states and changing admissible worlds remain unchanged. No
external alignment, heuristic fit, dark-matter primitive or gravity claim.
