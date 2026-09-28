# v15.92 — local preparation span obstructs regular polar geometry

Parent: eef0d852b2e696675d938244a8ef1ff5d648a24e. v15.91 showed that fully separable outputs can retain the native rank-six rotational response. This gate asks which local preparation structure is still necessary for a full three-axis polar geometry.

## Affine rank theorem

For independent local qubit channels r_i -> T_i r_i+t_i, the two-body moment matrix and connected correlation transform as

    M'_ij=T_i M_ij T_j^T+(T_i r_i)t_j^T+t_i(T_j r_j)^T+t_i t_j^T,
    C'_ij=M'_ij-r'_i r'_j^T=T_i C_ij T_j^T.

Translations cancel exactly. Therefore rank(C'_ij)<=min(rank T_i,rank C_ij,rank T_j). For square 3x3 matrices with nonsingular original C, C' is nonsingular iff both endpoint T matrices are nonsingular. This does not by itself ensure proper orientation: det C'=det T_i det C det T_j, and the sign must still be checked.

More generally, if a fully separable output is expressed using fixed local preparation families with Bloch vectors v_(i,alpha), then

    C_ij=sum_alpha p_alpha (v_(i,alpha)-mean_i)(v_(j,alpha)-mean_j)^T.

Thus its rank is bounded by each local family's affine span dimension. For a local measure-and-prepare channel, range(T_i) lies in that affine span. Full three-dimensional span is necessary for full-rank C but is not sufficient for any arbitrary input or source to produce a response.

A mutually commuting qubit preparation family has collinear Bloch vectors and affine dimension at most one. A noncommuting family can still be planar, with affine dimension two. Therefore noncommutativity alone is insufficient for a regular three-axis polar factor. The claim concerns a fixed family of possible preparations, not the trivial fact that an individual reduced density matrix commutes with itself.

## Four explicit entanglement-breaking channels

Let Pi_(k,s)=(I+s sigma_k)/2. The channels are frozen as follows:

| Arm | Effects | Prepared states | T | t | Preparation affine dimension |
|---|---|---|---|---|---:|
| isotropic | Pi/3 for X,Y,Z and both signs | corresponding Pi | diag(1/3,1/3,1/3) | 0 | 3 |
| plane | Pi/2 for X,Y and both signs | corresponding Pi | diag(1/2,1/2,0) | 0 | 2 |
| line | Pi for Z and both signs | corresponding Pi | diag(0,0,1) | 0 | 1 |
| point | I | (I+Y/2)/2 | 0 | (0,1/2,0) | 0 |

Every arm is measure-and-prepare. Applying its product over the three sites after the same v15.81 source produces fully separable outputs, also disentangled from any external reference. The point arm is a complex, nonunital translation control. Its nonzero local mean does not produce connected correlations.

The isotropic and plane preparation families are noncommuting; line and point families commute. The six-state and four-state decompositions have squared maximum commutator Frobenius norm 1/2. Tensor preparations have respectively 216,64,8,1 outcomes.

This is a controlled local readout comparison, not a new physical source-selection axiom. The plane and line axes are explicit channel data; no external rotation is used to align or rescue a response. Rank and affine dimension are invariant under local frame rotations.

## Singular geometry is not zero response

A rank-deficient C has a canonical support polar partial isometry V. A unique full orthogonal polar factor and the previously used regular Sylvester tangent are unavailable there. The gate records V, its initial/final projectors and rank; it leaves full O,Q,E undefined. It does not label the singular arms as rotational rank zero and does not claim every lower-dimensional notion of transport or geometry is impossible. The prior v15.82/v15.83 support-polar work remains valid.

The expected distinction is: output entanglement is unnecessary, but sufficient local correlation dimension is necessary for this regular three-axis readout. A noncommuting planar preparation family shows why merely requiring noncommutativity would still be too weak.

The source-composite channels are not claimed to form an identity-anchored flow or semigroup. The underlying global source can remain nonlocal. No physical source law, admissible-world update, or gravity law is selected. Genesis Pin, ordered recoverability, historical verdicts, and geometry as exhaust remain intact; no foundational fitting, external alignment mechanism, or dark-matter primitive is added. Measure-and-prepare ingredients are established theory (Ruskai 2003, https://arxiv.org/abs/quant-ph/0302032); no priority claim is made.
