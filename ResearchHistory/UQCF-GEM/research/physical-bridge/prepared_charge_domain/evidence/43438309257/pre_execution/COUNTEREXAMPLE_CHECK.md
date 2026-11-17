# Analytical check: conservation only on the prepared subspace

**Verdict: the proposed counterexample is correct.** The condition
`[K,U] L = {0}` on the prepared subspace is insufficient to imply Theorem A's
receiver law, even with the unchanged exact source channel, the same blank
receiver qubit and effect, independent product preparation, and the no-unit-gap
bath spectrum. The construction below has `q(rho)=0` for every source state.

This is a direct finite-dimensional algebraic check. It does not assert a
physical implementation, a native source correspondence, or a change to the
global-conservation theorem in the frozen `charge_selection/ARGUMENT.md`.

## 1. Data and the exact weakening

Let the source basis be `(o,p,u,v)`, and write

\[
Q=I_S-\pi_u,\qquad
C(X)=QXQ+\langle u|X|u\rangle\pi_p.
\]

The receiver is the same qubit with initial state `pi_0,R` and fixed effect
`F_R=pi_1,R`. Let the bath have orthonormal basis `(e_0,e_2,e_4,e_6)` and charge

\[
Q_E=\operatorname{diag}(0,2,4,6).
\]

Define orthogonal two-dimensional bath subspaces

\[
A=\operatorname{span}(e_0,e_4),\qquad
B=\operatorname{span}(e_2,e_6),
\]

and normalized vectors

\[
a=\frac{\sqrt3\,e_0+\sqrt5\,e_4}{2\sqrt2},\qquad
b=\frac{\sqrt5\,e_2+\sqrt3\,e_6}{2\sqrt2}.
\]

Thus `a` and `b` are orthogonal, and the bath preparation is the pure state
`tau=|a><a|`. The total charge and prepared subspace are

\[
K=\pi_u\otimes I_E\otimes I_R
  +I_S\otimes Q_E\otimes I_R
  +I_{SE}\otimes F_R,
\qquad
L=S\otimes\operatorname{span}(a)\otimes\operatorname{span}(|0_R\rangle).
\]

The weakening being checked is exactly `[K,U]P_L=0`, where `P_L` is the
orthogonal projection onto `L`. It is a vector identity on every vector in
`L`, not merely conservation of an expectation value.

## 2. A global unitary exists explicitly

In the ordered bases `(e_0,e_4)` of `A` and `(e_2,e_6)` of `B`, set

\[
T:A\longrightarrow B,\qquad
T=\frac14\begin{pmatrix}\sqrt{15}&1\\-1&\sqrt{15}\end{pmatrix}.
\]

Direct multiplication gives

\[
T^\dagger T=TT^\dagger=I_2:
\]

the diagonal numerators are `15+1=16`, and the off-diagonal numerators cancel.
Let

\[
H_1=|u\rangle\otimes A,\qquad H_2=|p\rangle\otimes B.
\]

These subspaces are orthogonal. Define `U_SE` on the whole of `S tensor E` by

\[
U_{SE}(|u\rangle x)=|p\rangle Tx\quad(x\in A),
\qquad
U_{SE}(|p\rangle y)=|u\rangle T^\dagger y\quad(y\in B),
\]

and let it be the identity on `(H_1 direct-sum H_2)^perp`. On `H_1 direct-sum
H_2` its block matrix is

\[
\begin{pmatrix}0&T^\dagger\\T&0\end{pmatrix}.
\]

Consequently `U_SE` is self-adjoint, has square equal to the identity, and is a
global unitary. Set `U=U_SE tensor I_R`. This is one fixed source-independent
unitary on the whole joint space; it is not merely an isometry specified on
the occupied input vectors.

The proposed vector identity is exact:

\[
Ta=
\frac{1}{8\sqrt2}
\begin{pmatrix}\sqrt{15}\sqrt3+\sqrt5\\-\sqrt3+\sqrt{15}\sqrt5\end{pmatrix}
=\frac{1}{2\sqrt2}\begin{pmatrix}\sqrt5\\\sqrt3\end{pmatrix}=b.
\]

Here and below the coordinates in the final column are in the ordered basis
of `B`. Since `|p> tensor A` is in the fixed complement, every retained source
label `j` in `{o,p,v}` obeys

\[
U|j,a,0_R\rangle=|j,a,0_R\rangle,
\qquad
U|u,a,0_R\rangle=|p,b,0_R\rangle.
\]

## 3. Exact source channel, including every coherence

For retained labels `j,k` in `{o,p,v}`, the output of the source matrix unit
`|j><k|` after tracing out the bath and receiver is `|j><k|`, since both bath
vectors are `a`. The input matrix unit `|u><u|` gives `|p><p|`, since `b` has
unit norm. Each matrix unit with exactly one index equal to `u` vanishes after
the trace, because its bath overlap is either `<a|b>` or `<b|a>`, both zero.

Thus the reduced map is precisely

\[
\operatorname{Tr}_{ER}
\left[U(X\otimes|a\rangle\langle a|\otimes\pi_{0,R})U^\dagger\right]
=QXQ+X_{uu}\pi_p
\]

for every source operator `X`, hence for every coherent or mixed source
density matrix. The initial state has exactly the required product form.

Because `U` acts as the identity on `R`, the complete receiver output is
`pi_0,R` for every input. In particular,

\[
q(\rho)=0\quad\text{for every }\rho,\qquad\Delta=0.
\]

The proposed Theorem A conclusion already fails on `rho=pi_u`, where its
right-hand side would be one. The counterexample is whole-receiver blindness,
not just blindness of the nominated effect on the two supplied diagonal
inputs.

## 4. The vector commutator vanishes on all of the prepared subspace

Write

\[
Q_A=\operatorname{diag}(0,4),\qquad
Q_B=\operatorname{diag}(2,6),\qquad
K_{SE}=\pi_u\otimes I_E+I_S\otimes Q_E.
\]

Since the receiver factor is untouched,

\[
[K,U]=[K_{SE},U_{SE}]\otimes I_R.
\]

On `H_1`, the commutator maps `|u> x` to `|p> Mx`, with

\[
\begin{aligned}
M&=Q_BT-T(Q_A+I_A)\\
 &=\frac14\begin{pmatrix}\sqrt{15}&-3\\-5&\sqrt{15}\end{pmatrix}.
\end{aligned}
\]

This agrees with the stated defect matrix for the convention `D=[K,U]=KU-UK`.
It annihilates `a` exactly:

\[
Ma=\frac{1}{8\sqrt2}
\begin{pmatrix}\sqrt{15}\sqrt3-3\sqrt5\\-5\sqrt3+\sqrt{15}\sqrt5\end{pmatrix}
=0.
\]

Equivalently, the stronger-looking vector identity in the proposal holds:

\[
T(Q_A+I_A)a=Q_Bb
=\frac{1}{2\sqrt2}\begin{pmatrix}2\sqrt5\\6\sqrt3\end{pmatrix}.
\]

For completeness, on `H_2` the commutator maps `|p> y` to `-|u> M^dagger y`.
The fixed orthogonal complement is invariant under `K_SE`, because `Q_E`
preserves `A` and `B` and the source charge is diagonal in the source basis.
The commutator is therefore zero on that complement. Its full nontrivial
block is

\[
[K_{SE},U_{SE}]\big|_{H_1\oplus H_2}
=\begin{pmatrix}0&-M^\dagger\\M&0\end{pmatrix}.
\]

The prepared retained vectors `|j,a>` all lie in the fixed complement, while
the prepared erased vector `|u,a>` is killed by `M`. Hence

\[
[K,U]|s,a,0_R\rangle=0\quad(s=o,p,u,v).
\]

Linearity proves this for every superposition of source labels and therefore
for every vector in `L`. No replacement of vector commutation by a scalar
expectation condition has occurred.

## 5. Global commutation fails, and spectral exclusion holds

The defect is nonzero. An explicit witness is

\[
[K,U]|u,e_0,0_R\rangle
=\frac14|p\rangle\otimes
 (\sqrt{15}\,e_2-5e_6)\otimes|0_R\rangle\ne0.
\]

Thus the construction does not satisfy the global hypothesis of Theorem A.
There is no conflict with that theorem.

Meanwhile,

\[
\operatorname{spec}(Q_E)=\{0,2,4,6\},\qquad
\operatorname{spec}(Q_E)+1=\{1,3,5,7\},
\]

so the required spectral intersection is empty. All bath eigenvalue
differences are even integers, and none equals one or minus one.

## 6. Why the weakening admits this example

The bath support is not invariant under its charge:

\[
Q_Ea=\frac{4\sqrt5}{2\sqrt2}e_4
\notin\operatorname{span}(a).
\]

Therefore `K L` is not contained in `L`. The local commutator condition does
not supply an operator intertwining identity on the whole bath charge space,
nor does it permit repeated application on `K L`. The two charge components of
the coherent prepared vector cancel in `Ma`, even though the matrix `M` itself
is nonzero. The global proof's eigenvalue-by-eigenvalue block exclusion is
therefore unavailable.

For example, the input `|u,a,0_R>` has total-charge probabilities `3/8` at
charge `1` and `5/8` at charge `5`; its output `|p,b,0_R>` has probabilities
`5/8` at charge `2` and `3/8` at charge `6`. Their charge distributions differ.
This observation is consistent with the exact vector commutator equality on
the prepared subspace: that equality alone does not imply conservation of all
spectral projections or all powers of `K` there when the prepared subspace is
not `K`-invariant.

**Scope of the result.** Replacing global additive conservation solely by
`[K,U]P_L=0` invalidates the asserted forced receiver response. This construction
uses a rank-one coherent, nonstationary bath preparation and says nothing
against a stronger replacement that adds charge invariance of the prepared
support or another sufficient closure condition. The source charge, bath
charge, Hilbert-space implementation, and receiver assignment remain supplied
physical premises; no native derivation or physical realizability is claimed.
