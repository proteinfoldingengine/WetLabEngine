# v15.79 — Covariant source representations and observable couplings

Parent: 7f68c941f699ccbebec5b15834bfdb032807950f (v15.78).
The new question restores transforming source data, rather than imposing
invariance on a fixed channel without source data.

## Precisely restricted class

Let a be one traceless Hermitian three-qubit source tensor (63 real raw Pauli
coordinates), h an exact-weight-three hidden tangent (27 HS-normalized Pauli
coordinates), and B(a,h) a weight-one/two retained output tangent (36
HS-normalized coordinates). Classify real bilinear maps B, with coefficients
independent of the state, satisfying
B(Ad_U a,Ad_U h)=Ad_U B(a,h) for all independent local SU(2)^3 frames.
This is a response-level class: it is not an assertion that all such maps
are derivatives of positive, trace-preserving physical source operations.
It excludes state-dependent coefficients, extra source tensors, higher local
spin source representations, and nonlinear dependence on the source.
The source and hidden inputs need not have the same units; raw source Pauli
and normalized tangent bases fix the convention without fitting amplitudes.

## Completeness by local representations

Each nonempty source support S carries a product of local spin-one vector
representations on S and scalars elsewhere. The hidden input carries a vector
at all three sites. A retained target support T has size one or two.
At a site absent from S, the hidden vector can only remain a vector. At a
site in S, 1 tensor 1 decomposes into spins 0,1,2 once each. Retained qubit
operators admit only spin 0 or 1. Therefore an intertwiner exists iff
S union T={0,1,2}, and its multiplicity is one. Its local factors are:

- preserve the hidden vector where the source is scalar;
- dot product where source and hidden vectors produce a scalar;
- cross product where they produce a vector.

The independent local multiplicities multiply; distinct source/target support
pairs are orthogonal. Counts by source weight are 3,9,6: total 18.
The identity-source sector has no retained intertwiner, reproducing the
source-free obstruction. Lie-algebra constraints determine these local
multiplicities independently of explicitly constructed delta/epsilon tensors;
SU(2)^3 acts through the connected proper-rotation group.

Use unnormalized delta/epsilon tensors with epsilon_123=+1 and
(a cross h)_r=epsilon_{r a h} a_a h_h. An intertwiner with k cross factors
has squared Frobenius norm 27*2^k. No basis rescaling is chosen from data.

## Algebraic and physical checks

For raw source P_a and normalized hidden h, the retained part of
-i[P_a/2,h] is the sum of the nine one-cross intertwiners, all coefficient +1.
This has an ordinary CPTP unitary realization. At fixed angle theta=pi/4,
U=cos(theta/2)I-i sin(theta/2)P_a; the retained part of U h U† equals
sin(theta) times the commutator response.

The retained part of the traceless Jordan benchmark
J(a,h)={a,h}/2-Tr(a h)I/8 is the sum of six zero-cross tensors with coefficient
+1 and three two-cross tensors with coefficient -1. This is only an
algebraic benchmark, not a claim of a positive channel or admissible physical
source generator. The identity trace subtraction has no retained component.

## Observability and its limits

For each reference state, use the certified map F_rho from an arbitrary
retained tangent to Q (and its invertible polar Sylvester transform E).
The 18-column coupling-observation matrix has rows indexed by source basis,
hidden basis, edge, and skew component. Stack all 12 frozen states, without
adapting any coupling coefficient to any state. Test for a common coefficient
kernel. This is coefficient identifiability across many experiments, not
an 18-dimensional edge geometry: each individual retained rotational tangent
still has at most nine edge components.

The v15.75 open-state theorem already implies that a state-independent
retained response cannot be rotationally null on an open state set unless
it vanishes. The new result sought here is the explicit source-representation
classification and its finite-ensemble observability, not a second novelty
claim for that general theorem. We do not infer an open-set theorem from
finite samples.

Use the already certified v15.74 zero-Bloch fixture, not a positivity-unsafe
subtraction from a generic state. Its connected pair matrices are .04 I.
One-body output tangents are rotationally invisible because all baseline
one-body vectors vanish. The expected kernel comprises six one-body-output
intertwiners; the twelve pair-output intertwiners remain observable.
This control prevents confusing ensemble-wide injectivity with visibility
of every coupling at every state, source value, or hidden probe.

## Boundaries

A positive classification admits couplings; it does not select their strengths,
choose a physical source law, establish restriction/composition naturality,
or alter admissible-world consistency. Earlier calibrated symmetric-null
examples and historical verdicts remain intact. Geometry is retained exhaust,
not an inserted primitive. Genesis Pin is unchanged; ordered recoverability
updates introduce no fundamental time. No gravity derivation is claimed.
