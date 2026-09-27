# v15.83 — Surviving support and loop composition

Parent b7e472378b907c7ff95a44cd8611d11c7fdaa2f5 certifies the v15.82 crossing.
This is a diagnostic of the same selected witness, not a held-out test.
Use its frozen exact complex input and isolated root. No source family,
state, edge, frame, or earlier verdict is changed.

## The existing triangle supplies composition

C_ij maps the Bloch frame at j to the frame at i. At the crossing, let V
be the rank-two canonical partial isometry of C_01. The other two links
O_12 and O_20 remain regular orthogonal polar factors. The original triangle
therefore supplies a based loop L=V O_12 O_20, mapping node 0 to itself.
It is a rank-two partial isometry with initial projector P=L^T L and final
projector Q=L L^T. These are native support data, not externally selected
planes. Under local frame changes L transforms by conjugation at node 0;
all spectra, norms and dimensions below are invariant.

For the regular loops L_minus and L_plus at strengths u*±delta,
L_minus P and L_plus P tend to the same L as delta tends to zero: the
one-dimensional sign jump is killed by restriction to P. This continuity
is earned by discarding that sector. It does not extend the full orthogonal
observable, so v15.81 and v15.82 remain unchanged.

## Partial isometries need not close under composition

P and Q need not agree. Applying the same spatial loop twice gives L^2.
This composition remains a well-defined associative linear map, but may
attenuate some directions instead of acting as a partial isometry.
Let c^2=tr[(I-P)(I-Q)], the squared overlap of the one-dimensional kernel
normals. Then the singular values of L^2 are (1,c,0). In particular,

||[(L^2)^T L^2]^2-(L^2)^T L^2||_F
= c^2(1-c^2) = ||[P,Q]||_F^2/2.

This follows by sandwiching the two plane projectors; their principal
angles consist of zero and arccos(c). A product of partial isometries is
not assumed to be another partial isometry. Composition here means path
traversal at a fixed ordered slice, not further quantum source updates.
No repolarization or normalization is inserted between traversals.

## Maximal lossless core

For n traversals define
G_n=I-(L^n)^T L^n=sum_{k=0}^{n-1}(L^k)^T(I-P)L^k.
Each summand is positive semidefinite. Thus ker G_n is exactly the set of
inputs that lose no norm at any of the first n traversals, not merely the
range of L^n. In three dimensions Cayley-Hamilton makes the constraints
for k>=3 consequences of those for k=0,1,2. Hence ker G_3 is the maximal
invariant lossless subspace for arbitrarily many traversals.

If G_3 is positive definite, this core is trivial and ||L^3||_2<1.
Consequently ||L^(3m)||_2 <= ||L^3||_2^m. This does not mean L^3=0 or that
all finite-amplitude information disappears after three traversals; it
means every nonzero input has incurred some loss by then.

## Interpretation boundary

The question is whether a support-defined crossing also gives lossless
composition around the inherited loop. An obstruction would identify
support compatibility as an additional condition for isometric transport.
It would not invalidate quantum positivity, associative linear composition,
all support-based geometry, or the source's demonstrated rotational response.
No change to admissible worlds, fundamental time, external alignment,
heuristic fit, dark-matter primitive or gravity derivation is introduced.
Genesis Pin and ordered recoverability remain foundational.
