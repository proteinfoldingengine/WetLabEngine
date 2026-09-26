# Rank-three response image decomposition gate

Frozen after the SO(3)-tangent interpretation failed and before inspecting response-image decompositions.

For each of the same 11 base states, use the already certified 9 by 243 closed-form response matrix A. Let H be the base loop holonomy. Left-translate every response column by H^T:
M = H^T K.

Decompose M orthogonally under the Frobenius inner product into:
1. scalar trace sector: (tr M / 3) I, dimension 1;
2. skew sector: (M-M^T)/2, dimension 3;
3. symmetric-traceless sector: (M+M^T)/2 - (tr M/3) I, dimension 5.

No sector is privileged in advance.

For each fixture:
- compute the rank-three output image using the left singular vectors of A;
- project the image projector onto the three orthogonal sectors;
- report exact numerical dimensions/intersection ranks and total Frobenius energy fractions by sector;
- test whether the image is invariant under any sector projector by measuring principal-angle leakage;
- compute the rank of the response after each sector projection.

Controls:
- sector pieces reconstruct every column to relative error <=1e-12;
- sector projectors are mutually orthogonal/idempotent to <=1e-12;
- results invariant under deterministic orthogonal changes of the 243-dimensional input basis;
- no fitted parameters and no finite-difference response columns.

Adjudication:
PURE_SKEW if the full rank-three image lies in skew sector.
PURE_SYMMETRIC_TRACELESS if it lies in symmetric-traceless sector.
MIXED_INVARIANT_DECOMPOSITION if image splits into invariant nonzero pieces across at least two sectors.
IRREDUCIBLY_MIXED_IMAGE if rank remains three but no nontrivial sector projector preserves the image.
INVALID if controls fail.

This gate identifies the structural content of the observed rank-three response image. It does not assign physical gravity meaning to any sector.
