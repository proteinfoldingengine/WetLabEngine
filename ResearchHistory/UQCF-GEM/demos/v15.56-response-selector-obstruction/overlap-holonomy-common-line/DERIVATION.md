# Overlapping retained triangles and a common-line discriminator

One triangle cannot empirically establish an irreducible multi-loop structure. Construct a four-qubit state from consecutive members of the frozen12-state ensemble:

sigma_k = [rho_k(012) tensor I_3/2 + S23 (rho_next(012) tensor I_3/2) S23^dagger]/2,

where next is cyclic and S23 swaps the last two qubits. This is a positive normalized convex mixture, not cloning or a fitted four-qubit ensemble. Retain regions012 and013 with overlap01. Their five edges are01,12,20,13,30. Region marginals and their common01 marginal must agree with the global state. The sixth edge23 is measured and reported but is not in the declared union of these two regions.

The inherited source acts only on01. Before local preparation, the spectator pair has

C23 = -r_(2,k) r_(2,next)^T / 4,

hence rank at most one. Its quantum marginal is unchanged by this source. This is an explicit five-edge overlapping-region atlas, not a complete six-edge nonsingular atlas.

Apply the same local measure-and-prepare channel at all four sites: either planar T=diag(1/2,1/2,0), or isotropic T=I/3. Both yield fully separable four-qubit output states. They differ in preparation affine span, not in the availability of entanglement in the output. Connected correlations obey C'_ij=T C_ij T^T. Use the v15.93 proper completion on rank-two planar edges and the proper full polar factor on rank-three isotropic edges; domain failures remain visible.

At base0, define H1=R01 R12 R20 and H2=R01 R13 R30. They transform by simultaneous conjugation under local coordinate changes. Noncommutation alone does not exclude the embedded O(2) stabilizer: a normal flip and a planar rotation can fail to commute while preserving a common line.

Let S_a be an orthonormal basis of real symmetric traceless3x3 matrices (dimension5), and define D(H)_ab=tr(S_a H S_b H^T). Stack B=[D(H1)-I; D(H2)-I], a10x5 real matrix. A common invariant line with projector N gives the nonzero kernel element N-I/3. Conversely a nonzero symmetric traceless matrix fixed by both conjugations has an isolated one-dimensional eigenspace in three dimensions, which both rotations preserve. Therefore:

rank(B)=5 iff the two loops have no common invariant real line.

This criterion includes unoriented lines and discrete normal flips. Its singular values are invariant under simultaneous SO(3) conjugation. It distinguishes a shared parallel-line restriction without choosing or fitting a comparison axis.

The planar channel supplies a common normal and predicts rank(B)<=4. Full-span preparation need not preserve that normal; rank(B)=5 on every frozen isotropic case is the preregistered numerical hypothesis, not a universal sufficiency theorem. Such a result would not establish continuous SO(3) holonomy: finite irreducible rotation groups can also have no invariant line. The exact quarter-turn control is itself an example.

This measures loop structure at each source setting, not the derivative of loop structure with respect to a source. In particular lambda=0 is not a required loop-geometry null. All new states are deterministic constructions from existing states, not a new held-out ensemble. Geometry is still extracted from correlations; the declared incidence of retained regions is a measurement protocol, not an explanatory geometry primitive.
