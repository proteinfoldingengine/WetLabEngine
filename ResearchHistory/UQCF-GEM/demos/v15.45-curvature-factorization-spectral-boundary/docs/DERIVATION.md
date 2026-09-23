# v15.45 Task 3: exact finite kernel and parity boundary

## Scope and provenance

This is the mathematical Task-3 result, not final v15.45 certification. Tasks
4–7, conditioning, evidence-dependency and physical source correspondence remain
outside this task. Pillar 3 remains OPEN. No physical metric, physical curvature,
gravity, stress-energy, Einstein equations, continuum limit, foundational
uniqueness or scientific breakthrough is claimed.

The scientific predecessor is `bb79da3fd78065cf4fc5543eb2d3c3ae58fa2a01`;
its Task-2 development run is `35921297708`. The immutable original v15.44
certified head is `9085e4fa0bec3dbd700f759a8a9629b230d226ff`.

**Exposure correction:** the L6/L8 exploratory ranks and extra null modes were
reported before the v15.45 design freeze. They are predeclared verification
controls, not blinded holdouts or first observations. The original design is
preserved; its phrase “before looking at results” cannot erase that exposure.

Even-period objects below are formula-extension fixtures. The v15.44 archive
contains only L5/L7, and its parser is NOT changed to admit new carriers. The
algebraic domain of a theorem is not a new physical admissibility rule.

## 1. From the frozen transport to the compact operator

Let X and Y translate scalar fields by one vertex in the two positive square
directions on Z_L × Z_L. The centered differences are

    Gx = (X - X^-1)/2,    Gy = (Y - Y^-1)/2.

For the consistently counterclockwise face (east, north, west, south), the
coefficient of J=[[0,-1],[1,0]] in the first-order loop holonomy is

    chi = [(1+X)(1-Y) Gy + (1+Y)(1-X) Gx] phi / 4.

This follows by inserting the endpoint averages in the four oriented edge
skew terms. The scalar identity terms telescope around the closed loop. Using

    (1-T)(T-T^-1) = (1+T)(2-T-T^-1)

for T=X,Y, and XY=YX, gives the exact identity

    A phi = chi = (1+X)(1+Y) Delta phi / 8 = M Delta phi / 2,
    Delta = 4I-X-X^-1-Y-Y^-1,
    M = (I+X)(I+Y)/4,
    K_f = (A phi)_f J.

The factor 1/8 is frozen; nothing is tuned. Opposite face orientations reverse
the sign. The full matrix codomain contains (0,-chi,chi,0), so its embedding is
injective and has the same kernel as A. Changes of row order, column labels and
allowed frames are invertible presentations, not additional field constraints.

The code `scalar_operator` constructs this rational stencil directly. The
integration tests independently reconstruct a periodic chart from the actual
carrier direction classes rather than assuming integer labels are coordinates.
They compare full matrices with the archived operator AND the unmodified
v15.44 coefficient constructor, not just summaries or ranks.

## 2. Exact Fourier kernel theorem

For the algebraic periodic operator above, let L be any integer at least 3.
A Fourier character has X-eigenvalue z=exp(2 pi i k/L) and Y-eigenvalue
w=exp(2 pi i l/L). The two cyclic shifts commute and have a complete joint
Fourier basis. On that character the multiplier is

    a(k,l) = (1+z)(1+w)(4-z-z^-1-w-w^-1)/8.

The final factor equals

    4 sin²(pi k/L) + 4 sin²(pi l/L),

which is nonnegative and zero exactly at (k,l)=(0,0). The other factors vanish
exactly at z=-1 or w=-1. Such roots exist only when L is even. Therefore:

    ker A = span of the constant mode,
            together with all k=L/2 or l=L/2 modes when L is even.

For odd L: nullity=1; rank=L²-1; centered nullity=0.

For even L: the two Nyquist lines contain L+L-1=2L-1 modes, with their
checkerboard intersection counted once. The constant is separate. Thus
nullity=2L; rank=L²-2L; centered nullity=2L-1.

These are exact algebraic dimensions, not singular-value threshold decisions.
Since A has rational coefficients, its rational, real and complex ranks agree:
a nonzero minor remains nonzero under extension of the coefficient field.
The Fourier argument therefore determines the dimension of the rational kernel
as well. This theorem concerns the stated square operator, not arbitrary
networks, physically realized carrier selection, or a continuum.

## 3. Explicit rational basis and completeness

For odd L the basis is the all-ones vector.

For even L use that constant plus

    v_b(x,y)=(-1)^x 1[y=b],    b=0,...,L-1,
    w_a(x,y)=(-1)^y 1[x=a],    a=0,...,L-2.

Every strip is centered and annihilated by A: its alternating coordinate
makes I+X or I+Y vanish, and these operators commute with Delta. The omitted
last w strip is redundant because the two families have the common checkerboard
vector. To verify independence, suppose a linear combination of the strips
vanishes. On x=L-1 all included w_a vanish, forcing every v_b coefficient
to vanish; the remaining w_a coefficients then vanish. The constant is
independent of the centered strips by its nonzero sum.

There are 2L basis vectors including the constant, so the spectral dimension
proves completeness. The finite code also independently computes rank by exact
rational elimination, checks every basis vector is annihilated, checks basis
rank, and checks rank+nullity=L². Corrupt ranks, missing basis vectors,
dependent vectors and false injectivity flags are rejected.

## 4. Finite certificates and archive binding

`docs/TASK3_SPECTRAL.json.gz` losslessly stores the exact formula certificates, including full
integer kernel bases, integer zero-mode indices and rational-operator hashes.

| Period | Rank | Kernel dimension | Centered kernel dimension |
|---|---:|---:|---:|
| 5 | 24 | 1 | 0 |
| 6 | 24 | 12 | 11 |
| 7 | 48 | 1 | 0 |
| 8 | 48 | 16 | 15 |

The integration tests check all four actual archived L5/L7 carriers, their
full matrices and v15.44 rank/kernel certificates. Separately, L6/L8 formula
fixtures are checked against both unchanged `compact_operator` and unchanged
v15.44 `derive_operator`, on every matrix entry and every rational kernel vector.
The archive and even-fixture receipts are printed separately in GitHub Actions.
The full Task-2 presentation test is not replaced by these identity-frame checks.

The predecessor compact formula is pinned at blob
`32da787647f886e942b5719115625212601f950e`; the v15.44 results at
`f40002f415515832741a21e4885b7b2f9d7f337e`; the frozen v15.44 coefficient
constructor at `ce72e488e17fba63a37cff46d07c64e42ffa14df`.

## 5. Interpretation and next dependency

The odd-grid injectivity result survives with its correct scope. Universal
centered injectivity over both odd and even periodic sizes is false for this
frozen operator: the even grids have entire families of nonconstant invisible
inputs, not merely a removable constant offset. This is not repaired by deleting
modes, adding a regulator, changing M, or selecting odd sizes after exposure.

Exact finite injectivity is also not a conditioning or stable-refinement theorem.
That distinction belongs to Task 4, together with the dependency audit of the
592 input/output comparisons. No source-correspondence verdict is emitted here.

## Reproduction

From this demo directory with CPython 3.13.5:

    python -m unittest -v test_spectral
    python -m unittest -v test_factorization test_spectral test_spectral_archives

The second command needs the original repository archives. Execution receipts
and the separate full-development regression status are recorded on PR #56.
