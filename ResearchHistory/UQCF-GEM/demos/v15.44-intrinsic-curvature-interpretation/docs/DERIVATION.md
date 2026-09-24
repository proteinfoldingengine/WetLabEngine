# Exact curvature-response coefficient derivation

Let the ordered carrier labels be \(\ell_0,\ldots,\ell_{N-1}\), and let
\(f_j\) be the basis field equal to one at \(\ell_j\) and zero elsewhere.
All coefficients here are rational. A centered derivative at vertex \(x\)
has the two rows \(G_x[i,j]=(1_{n_i^+(x)=\ell_j}-1_{n_i^-(x)=\ell_j})/2\),
where \(n_i^\pm(x)\) are the unique neighbors in the positive and negative
directions of local unit axis \(i\). Thus \(q_x(\phi)=G_x\phi\) for every
field \(\phi\), without assigning a geometric meaning to a numeric label.

For an oriented edge \(x\to y\), the gradient average in the frame at
\(x\) is \(\bar q=(G_x+P_{yx}G_y)\phi/2=H\phi\). Writing \(d\) for the
edge direction and \(P_{xy}\) for its constant baseline transport, the
degree-one edge perturbation is \(D(\phi)=P_{xy}B(\phi)\), with coefficient

\[
B_j[a,b]=\frac{1_{x=\ell_j}-1_{y=\ell_j}}2\,1_{a=b}
 +\frac{H[a,j]d[b]-d[a]H[b,j]}2,
\qquad D_j=P_{xy}B_j.
\]

The first summand is a scalar identity matrix and the second is skew. Each
entry is linear in \(\phi\): \(D(\phi)=\sum_j\phi_jD_j\). In particular the
gradient stencil is retained in full, including all neighbors that happen to
contribute to a face edge. No stencil or Laplacian reduction is assumed.

For the inherited oriented four-cycle, write its ordered edges as
\(e_0,\ldots,e_3\) and their baseline factors as \(P_0,\ldots,P_3\).
The full holonomy product is
\((P_3+\epsilon D_3)\cdots(P_0+\epsilon D_0)\).
Selecting exactly one degree-one factor gives the coefficient at label
\(\ell_j\):

\[
K_j=\sum_{s=0}^3 P_3\cdots P_{s+1}\,D_{s,j}\,P_{s-1}\cdots P_0.
\]

The implementation forms all four ordered products explicitly. Its output
has four entries per inherited face, in row-major order, and one column per
ordered label. The independently evaluated oracle computes the inherited
transport and differentiated holonomy for each basis field; equality tests
compare each coefficient on all four actual carriers.

The scalar part cancels on a flat baseline. Indeed, for a fixed slot the
scalar identity term in \(D_s\) contributes
\((\phi(x_s)-\phi(y_s))P_3P_2P_1P_0/2\). Its sum around the closed cycle is
zero because \(y_s=x_{s+1}\) cyclically. Flatness makes the common baseline
product the identity, so these terms vanish entrywise. The skew terms do not
take this telescoping form and remain in the four-product expression; the
implementation does not discard either contribution before forming \(K_j\).

Tuple matrices encode all nonempty row shapes, including \(m\times0\).
An empty tuple cannot distinguish \(0\times n\) widths. The exact matrix
functions therefore accept explicit width arguments for zero-row operands;
shape mismatches raise instead of silently truncating an inner dimension.

## Exact finite rank and projection certificates

For each frozen carrier, row reduction uses exact rational elementary operations
in fixed column order. The certificate retains every row swap, nonzero scaling,
and row addition, the resulting reduced matrix and its pivot columns. The
independent verifier replays these operations on the original operator, checks
the reduced row-echelon conditions, and checks the pivot-column basis spans
every original column. Invertible operations preserve rank. If the pivot set
has size (r), standard free-variable back substitution gives (N-r) vectors
whose selected free coordinates form the identity matrix. Thus they are
independent, annihilated by (A_C), and exhaust its kernel. The verifier
also checks these facts on the original matrix and independently checks image
basis independence. A separate zero-sum intersection is obtained by imposing
the additional row of ones on (A_C), with independent basis checks.

Let (Z) be this complete kernel basis. Its rational Gram matrix (Z^TZ)
is invertible because the columns are independent. For the fixed unweighted
vertex inner product, (P=Z(Z^TZ)^{-1}Z^T) is symmetric, (P^2=P), and
(PZ=Z); moreover (A_CP=0). Hence its image equals the kernel, and each
field splits orthogonally as (P u+(I-P)u). The replay verifier directly
checks these four equalities and the response annihilation; this projection
is an algebraic decomposition, without physical metric normalization.

The algebra above proves linearity and the stated conditional certificate
implications for any carrier satisfying the inherited finite flat-baseline,
oriented-face and centered-gradient assumptions. The numerical ranks,
nullities, particular bases and all archived comparisons are reproducible
finite computations on precisely four frozen carriers, not a theorem about
every periodic size or a continuum. Equality of the independent coefficient
formula with the inherited core is checked on every ordered basis impulse;
linearity then extends that equality to every rational field on each of
these four carriers. The inherited core also checks constant, kernel and
mixed fields directly, with frame, orientation, relabeling and scale controls.

The archived fields are centered, whereas the kernel certification covers
all of \(\mathbb Q^{L^2}\). Exact ratios and pair categories are descriptive
for these known 740 fields and 592 canonical-control pairs. Their generation
and earlier nonzero outcomes were already known; neither a pair difference
nor a pair equality identifies a physical source law. No compact named
differential-operator identity, all-size statement, physical curvature,
source correspondence or foundational uniqueness is asserted.
