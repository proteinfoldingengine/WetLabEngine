# Prepared mixed-channel equality versus vectorwise conserving completion

Status: **conditional analytical diagnostic; native bridge NOT_DERIVED.** This note checks the specified counterexample and the linear-algebra claims reported from Grok Q196. It introduces no native physical law, novelty claim, or numerical result. The Q196 statements were supplied in the task summary; the original Q196 exchange was not independently retrieved.

The local inputs inspected were PR147's `charge_selection/ARGUMENT.md` and PR148's `prepared_charge_domain/ARGUMENT.md`. All checks below are exact algebra; no numerical or scientific program was executed and no external API/model or GitHub call was made.

## 1. A full mixed-preparation channel can hide a nonconserving dilation

Keep the source basis `(o,p,u,v)`, the exact channel

\[
C(\rho)=Q\rho Q+\rho_{uu}\pi_p,\qquad Q=I_S-\pi_u,
\]

the same blank receiver qubit, and the same effect `F_R=pi_1,R`. Choose a bath qubit with

\[
Q_E=\operatorname{diag}(0,2),\qquad \tau=I_E/2,
\qquad X_E=|e_0\rangle\langle e_2|+|e_2\rangle\langle e_0|.
\]

The bath spectrum `{0,2}` has no difference equal to one. This is a particular allowed mixed bath in PR147's finite arbitrary-bath-state class; no statement about the same construction with an arbitrary replacement bath state is needed.

Let `W_R` be the global unitary on S,R that exchanges `|u,0_R>` and `|p,1_R>` and fixes all other S,R basis vectors. The exchanged vectors both have S,R charge one, hence

\[
[W_R,\pi_u+F_R]=0.
\]

Use identities on omitted factors and define the single, source-independent global unitary

\[
U=W_R X_E=X_E W_R,
\qquad K=\pi_u+Q_E+F_R.
\]

The equality of the factors follows because they act on disjoint S,R and E factors. Although `[W_R,K]=0`, the product U need not commute with K.

### 1.1 Exact equality of the whole SER output for every source input

For every source operator rho, including every coherent density matrix,

\[
\begin{aligned}
U(\rho\otimes\tau\otimes\pi_{0,R})U^\dagger
&=W_R(\rho\otimes X_E\tau X_E^\dagger\otimes\pi_{0,R})W_R^\dagger\\
&=W_R(\rho\otimes\tau\otimes\pi_{0,R})W_R^\dagger,
\end{aligned}
\]

because `X_E tau X_E†=tau`. This is equality of the entire prepared-input output state, before taking any partial trace or charge measurement.

In particular define the source-to-SR isometry

\[
J|a\rangle=|a,0_R\rangle\quad(a=o,p,v),\qquad
J|u\rangle=|p,1_R\rangle.
\]

Up to the written ordering of tensor factors, the common full output is
`J rho J† tensor tau`. On retained-retained matrix units the reduced source output is unchanged; `pi_u` becomes `pi_p`; and every matrix unit with exactly one u index vanishes after tracing R. Thus both global unitaries implement the exact C on all 16 source matrix units. Their fixed receiver effect obeys

\[
q(\rho)=\rho_{uu},\qquad
q(\rho^{(0)})-q(\rho^{(1)})=1/5.
\]

This is not merely a check on the supplied diagonal pair.

### 1.2 Full total-charge statistics are preserved

Let `P_lambda` be any spectral projector of K and let
`omega_rho=rho tensor tau tensor pi_0,R`. Since the U output equals the W_R output and W_R commutes with K,

\[
\operatorname{Tr}(P_\lambda U\omega_\rho U^\dagger)
=\operatorname{Tr}(P_\lambda W_R\omega_\rho W_R^\dagger)
=\operatorname{Tr}(P_\lambda\omega_\rho).
\]

Hence the whole K distribution, every moment, and the expectation of every function of K are preserved on every original source preparation. This conclusion does not require rho to commute with `pi_u`.

### 1.3 Global conservation and vectorwise commuting completion both fail

The occupied preparation space is

\[
L=S\otimes E\otimes|0_R\rangle.
\]

It is **K-invariant**. It is not U-invariant, since the u input is sent to receiver state 1. These two kinds of invariance must not be conflated.

For the vector `x=|o,e_0,0_R>` in L,

\[
Kx=0,\qquad Ux=|o,e_2,0_R>,\qquad KUx=2Ux.
\]

Consequently `[K,U]x=2Ux` is nonzero. There cannot exist a K-commuting unitary `U_c` agreeing with U vectorwise on L: commutation would imply

\[
KU_cx=U_cKx=0,
\]

whereas vector agreement would give `KU_cx=KUx=2Ux`.

The example distinguishes two precise requirements:

| Requirement | Result |
|---|---|
| A conserving unitary has the same complete output on every original mixed preparation | Yes: W_R itself does |
| A conserving unitary agrees with the specified U on every vector in L | No |

There is therefore **no channel-level nonexistence claim**. The failure belongs to a particular dilation's vector action. Fixed full-rank bath support does not mean the experiment supplies every bath pure state: varying rho spans the input-operator family `B(S) tensor span{tau} tensor pi_0,R`, not all operators supported on L. Here the bath flip permutes equally weighted bath components, leaving the mixed state unchanged while changing their individual charge values.

This example also does not refute receiver selection: it has exactly the selected response `q(rho)=rho_uu`. Its counterexample target is the inference from prepared mixed-state statistics, or even equality of the complete prepared channel, to vectorwise conserving completion of the specified U.

## 2. Exact criterion for a vectorwise commuting completion

Let H be finite dimensional, let K be Hermitian with r distinct eigenvalues, let L be an arbitrary subspace, and let U be unitary. The following are equivalent:

1. A unitary `U_c` exists with `[U_c,K]=0` and `U_c x=Ux` for every x in L.
2. For every x,y in L and every spectral projector `P_lambda` of K,
   `⟨x,P_lambda y⟩=⟨Ux,P_lambda Uy⟩`.
3. For every x,y in L,

   \[
   \langle x,K^n y\rangle=\langle Ux,K^n Uy\rangle
   \quad(n=0,1,\ldots,r-1).
   \]

4. The same moment identities hold for every integer `n>=0`.

The n=0 identity is automatic because U is unitary. Using `0,...,dim(H)-1` is a valid but possibly redundant finite bound.

**Necessity.** A K-commuting unitary commutes with every spectral projector and every polynomial in K. Replacing its action by U on x,y in L gives the stated identities.

**Moments versus projectors.** Every spectral projector is a polynomial in K of degree at most `r-1`, by interpolation on the distinct eigenvalues. Conversely powers of K are linear combinations of its spectral projectors. This proves the equivalence of the projector and moment conditions without assuming L invariant.

**Sufficiency.** Within the K-eigenspace `H_lambda`, set

\[
M_\lambda=P_\lambda L,\qquad N_\lambda=P_\lambda U L.
\]

Define a linear map on projected vectors by

\[
T_\lambda(P_\lambda x)=P_\lambda Ux\quad(x\in L).
\]

The projector Gram identity gives

\[
\langle P_\lambda x,P_\lambda y\rangle
=\langle P_\lambda Ux,P_\lambda Uy\rangle.
\]

It follows both that this assignment is well defined and that it is an isometry from `M_lambda` onto `N_lambda`. Their dimensions therefore agree. Complete orthonormal bases inside `H_lambda` to extend `T_lambda` to a unitary `V_lambda` of that whole eigenspace. Then `U_c=direct_sum_lambda V_lambda` commutes with K, and for x in L,

\[
U_cx=\sum_\lambda V_\lambda P_\lambda x
=\sum_\lambda P_\lambda Ux=Ux.
\]

This proves the criterion. In particular the criterion uses `P_lambda L`; for a non-invariant L those spaces need not equal `L intersect H_lambda`.

Equality of each charge distribution for every pure vector x in L also suffices, since polarization recovers the cross-vector Gram identities. Equality only for the fixed mixed-bath preparation family is a different condition, as §1 shows.

## 3. The precise status of `D P_L=0`

Set `D=KU-UK`.

### 3.1 If L is K-invariant, it is equivalent to completion

PR148 Lemma 2 proves sufficiency: decompose invariant L into its intersections with the K eigenspaces and extend each restricted isometry within its eigenspace.

Necessity holds as well. If `U_c` commutes with K and agrees with U on L, then for x in L, both x and Kx lie in L, so

\[
KUx=KU_cx=U_cKx=UKx.
\]

Thus for a K-invariant L,

\[
DP_L=0
\quad\Longleftrightarrow\quad
\text{a vectorwise K-commuting unitary completion exists}.
\]

This equivalence applies to the full-rank-bath L in §1, where both properties fail.

### 3.2 For arbitrary subspaces it is neither necessary nor sufficient

This statement must allow **non-K-invariant** L; it is false as a blanket claim restricted to invariant L.

For non-necessity, take an abstract two-dimensional example with

\[
K=\operatorname{diag}(0,1),\quad U=X,\quad
L=\operatorname{span}\{(|0\rangle+|1\rangle)/\sqrt2\}.
\]

The identity unitary is a K-commuting completion of U on L, because X fixes its spanning vector. Nevertheless

\[
[K,X](|0\rangle+|1\rangle)/\sqrt2
=(|1\rangle-|0\rangle)/\sqrt2\ne0.
\]

This is a generic linear-algebra example, not an additional implementation of the source benchmark.

For non-sufficiency within the source benchmark, PR148 Proposition 1 gives `DP_L=0`, but its prepared u vector has input K distribution
`(1,5)` with probabilities `(3/8,5/8)` and output distribution
`(2,6)` with probabilities `(5/8,3/8)`. Their third moments are `157/2` and `86`, respectively. They violate the completion criterion; no conserving unitary agrees vectorwise with that U on its prepared space.

The matching first and second moments are expected: whenever `DP_L=0`, for x,y in L,

\[
\langle Ux,KUy\rangle=\langle x,Ky\rangle,
\qquad
\langle Ux,K^2Uy\rangle
=\langle KUx,KUy\rangle
=\langle x,K^2y\rangle.
\]

Without invariance there is no general right to iterate the commutator condition on Kx. These first two identities therefore do not establish the all-moment criterion.

## 4. PR148 norm and source-label precision

PR148 uses `U=V_SE tensor I_R`. In the ordered exchange subspaces
`|u> tensor A_0` and `|p> tensor B_0`, its SE defect has block form

\[
D_{SE}=[K_{SE},V]
=\begin{pmatrix}0&-B^\dagger\\ B&0\end{pmatrix},
\qquad
B=\frac14\begin{pmatrix}\sqrt{15}&-3\\-5&\sqrt{15}\end{pmatrix}.
\]

It is zero on the orthogonal complement. With the unit vectors defined in PR148,

\[
B a=0,\qquad B a_\perp=2b_\perp,
\qquad B=2|b_\perp\rangle\langle a_\perp|.
\]

Thus B has one nonzero singular value, 2; `D_SE` has two nonzero singular values, both 2. Tensoring with the two-dimensional receiver identity duplicates those values. For the actual full SER defect,

\[
\boxed{\|D\|_{\mathrm{op}}=2,\qquad
\|D\|_{\mathrm{F}}=\sqrt{\operatorname{Tr}(D^\dagger D)}=4.}
\]

For comparison, `||D_SE||_F=2 sqrt(2)`. Consequently a report of “norm 4” is correct for the full SER **Frobenius/Hilbert–Schmidt norm**, but not for its operator norm. A norm convention must be stated.

Using only three source labels `{u,p,j}`, where j represents one of `{o,v}`, removes zero defect blocks and leaves both displayed norms unchanged. The four-label benchmark has 16 source matrix units; a three-label calculation checks only 9. The remaining seven are nevertheless settled by the explicit algebra, without rerunning a numerical check:

\[
|a\rangle\longmapsto|a\rangle\otimes a_E\quad(a=o,p,v),
\qquad
|u\rangle\longmapsto|p\rangle\otimes b_E,
\qquad\langle a_E,b_E\rangle=0.
\]

All nine retained-retained matrix units are preserved, the u diagonal becomes `pi_p`, and all six u/retained off-diagonal units vanish. V fixes the full bath spaces of the spectator labels o and v, so there is no special untested action attached to the omitted label. This is an analytic extension to the original four-label model; a record that checked 9 matrix units should not be described as a numerical check of all 16.

## 5. Findings and limits

- The proposed mixed-bath construction is valid, source-independent, has no bath unit gap, and gives exact equality of the full prepared output for all coherent source inputs.
- It preserves every original prepared total-charge distribution while failing both global commutation and vectorwise conserving completion on its K-invariant preparation support.
- It still has a conserving realization of the same prepared channel, namely W_R, and still gives the selected receiver signal.
- The all-moment/spectral-projector Gram criterion is exact in finite dimension. Its input vectors range over L; fixed mixed-preparation statistics do not supply that quantifier.
- The “neither necessary nor sufficient” characterization of `DP_L=0` needs arbitrary, potentially non-invariant L. On an invariant L the condition is necessary and sufficient for vectorwise completion.
- PR148's full defect has Frobenius norm 4 and operator norm 2, unchanged by restoring the fourth source label. Its exact isometry formula settles the full 16-unit channel check.

The physical source charge, additive charge observable, chosen bath spectrum/state, receiver ownership, and every asserted conservation premise remain supplied or newly assumed physical structure. None of these algebraic distinctions derives a native event operation or repairs the native physical bridge. No archive-wide or literature novelty is asserted.
