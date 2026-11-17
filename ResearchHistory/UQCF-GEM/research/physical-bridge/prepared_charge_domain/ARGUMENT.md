# The domain required by the charge-conservation premise

Status: **NEW-assumption analytical diagnostic; native bridge NOT_DERIVED.** This bounded continuation tests one precise weakening of PR147's physical-law premise. It neither changes the frozen PR147 proof nor supplies a native producing operation. The explicit counterexample and completion proof below were derived before the review freeze. No scientific simulation or enumeration was used.

## 1. Question and fixed objects

PR147 proved a fixed receiver response under global additive conservation. Can conservation instead be asserted only on the vectors appearing in the given input preparation?

Retain the source basis `(o,p,u,v)`, `pi_j=|j><j|`, `Q=I_S-pi_u`, and the supplied exact all-input source channel

\[
 C(\rho)=Q\rho Q+\rho_{uu}\pi_p.
\]

The bath E is finite dimensional, with a fixed density matrix tau and Hermitian charge Q_E. R is the **same qubit**, initially `|0_R>`, and `F_R=|1_R><1_R|` is the **same fixed effect**. One source-independent unitary U acts on the full S tensor E tensor R space. Product input preparation is `rho tensor tau tensor pi_0,R`. Its reduced source output is required to equal C(rho) for every rho. Define

\[
 K=\pi_u\otimes I_E\otimes I_R+I_S\otimes Q_E\otimes I_R
       +I_{SE}\otimes F_R,\qquad D=KU-UK.
\]

Assume the same bath spectral exclusion

\[
 \operatorname{spec}(Q_E)\cap(\operatorname{spec}(Q_E)+1)=\varnothing.
\]

Let `A=supp(tau)`, `L=S tensor A tensor |0_R>`, and P_L be the orthogonal projection onto L. Compare three statements:

| Statement | Exact meaning |
|---|---|
| Global conservation | `D=0` on the whole joint space; PR147's premise |
| Prepared-input vector condition | `D P_L=0` |
| Conservation on the charge-generated input space | `D P_Lhat=0`, with Lhat defined in §3 |

The second condition is an **operator/vector** equation on L, stronger than conservation of the mean charge on those inputs. It is not merely a compressed equation `P_L D P_L=0`. No claim is made that an ordinary mean-charge measurement verifies it. Calling it a prepared-input condition does not assert physical ability to prepare arbitrary bath support vectors individually.

The source pair is unchanged:

\[
 \rho^{(0)}=\operatorname{diag}(1,1,2,1)/5,\qquad
 \rho^{(1)}=\operatorname{diag}(1,1,1,2)/5.
\]

The receiver probability is `q(rho)=Tr[(I_SE tensor F_R)U(rho tensor tau tensor pi_0,R)U†]`, and signed contrast is `Delta=q(rho^(0))-q(rho^(1))`.

**Premise ledger.** The Hilbert factorization, normalized encoding, exact C, fixed product preparation, same receiver and owned effect access remain SUPPLIED. The physical charge assignment `pi_u+Q_E+F_R`, spectral exclusion, and every version of the conservation law above remain NEW ASSUMPTIONS. Native total-grade preservation is not any of these joint operator laws. Actual event occurrence remains ACCEPTED INPUT. Algebraic charge powers below do not introduce physical time.

## 2. Explicit counterexample to the prepared-input weakening

**Proposition 1.** The prepared-input vector condition, spectral exclusion, and exact all-input C do not force any receiver response. There is an explicit finite realization satisfying all three with `q(rho)=0` and the complete R state blank for every rho.

### 2.1 Bath and unitary

Choose an orthonormal bath basis `(e_0,e_2,e_4,e_6)` and

\[
 Q_E=\operatorname{diag}(0,2,4,6),\qquad
 a=\sqrt{3/8}\,e_0+\sqrt{5/8}\,e_4,\qquad
 b=\sqrt{5/8}\,e_2+\sqrt{3/8}\,e_6,\qquad \tau=|a\rangle\langle a|.
\]

All bath eigenvalue differences are even integers, so the spectrum has no unit gap. Define orthogonal bath subspaces `A_0=span(e_0,e_4)` and `B_0=span(e_2,e_6)`. These are not the prepared support A: here `A=span(a)`.

In the displayed ordered bases define the isometry `T:A_0 -> B_0` by

\[
 T=\frac14\begin{pmatrix}\sqrt{15}&1\\-1&\sqrt{15}\end{pmatrix}.
\]

It is unitary between these two-dimensional spaces because `T†T=TT†=I`. Define V on S tensor E as the exchange

\[
 V(|u\rangle\otimes x)=|p\rangle\otimes Tx\quad(x\in A_0),\qquad
 V(|p\rangle\otimes y)=|u\rangle\otimes T^\dagger y\quad(y\in B_0),
\]

and let V act as identity on the orthogonal complement of these two source-bath subspaces. Thus `V=V†`, `V²=I`; set `U=V tensor I_R`. This is a specified global unitary, not only an input isometry.

Direct exact multiplication gives `Ta=b`. For retained labels j in `{o,p,v}`, `V|j,a>=|j,a>`, since the retained p input has its bath in A_0, orthogonal to the exchanged p,B_0 subspace. For the erased input, `V|u,a>=|p,b>`. The two bath record vectors a,b are orthogonal. Consequently the reduced source map preserves every retained-retained matrix unit, sends `pi_u` to `pi_p`, and kills every off-diagonal matrix unit involving u. It is exactly C on **all** inputs, including coherent inputs. U acts trivially on R, so the entire receiver remains blank and `Delta=0`.

### 2.2 Exact conservation check on prepared inputs

Let `K_SE=pi_u tensor I_E+I_S tensor Q_E`. Since U acts trivially on R, `D=[K_SE,V] tensor I_R`. On the block from `|u> tensor A_0` to `|p> tensor B_0`, the defect is

\[
 B=Q_E|_{B_0}\,T-T\,(Q_E|_{A_0}+I)
   =\frac14\begin{pmatrix}\sqrt{15}&-3\\-5&\sqrt{15}\end{pmatrix}.
\]

Writing `a=(sqrt(3),sqrt(5))/sqrt(8)` in A_0 gives `Ba=0`. On each retained input `|j,a>`, V fixes both the vector and `K_SE|j,a>`: Q_E sends a into A_0, and V is the identity on every retained-label A_0 subspace. Hence D annihilates `|j,a,0_R>` for every source basis label, including u. By linearity,

\[
 D P_L=0.
\]

Global conservation nevertheless fails. For example `B e_0=(sqrt(15)e_2-5e_6)/4` is nonzero. More informatively, put

\[
 a_\perp=(-\sqrt5\,e_0+\sqrt3\,e_4)/\sqrt8,
 \qquad b_\perp=(-\sqrt3\,e_2+\sqrt5\,e_6)/\sqrt8.
\]

Then `B a_perp=2 b_perp`, so D is nonzero on the unprepared companion direction `|u,a_perp,0_R>`.

The obstruction is that `span(a)` is not Q_E-invariant: a has nonzero components at two distinct eigenvalues. The explicit vector condition `Dx=0` for every x in L cannot be iterated on `Kx` without further information because `Kx` can leave L.

### 2.3 Why this is not physical conservation of the full charge distribution

For source u, the input K distribution has values 1 and 5 with probabilities 3/8 and 5/8. The output has values 2 and 6 with probabilities 5/8 and 3/8. Both have mean 7/2 and second moment 16; their third moments are respectively 157/2 and 86. Thus even these first two scalar checks agree while the charge distributions differ.

The counterexample satisfies the proposed weakened vector condition but violates the original global conservation law. It therefore does **not** refute PR147 or establish a physical violation of conservation. Its sole purpose is to reject the invalid inference from a prepared-input condition to the global selection rule for arbitrary coherent bath preparations.

## 3. A sufficient conservation domain and commuting completion

Let the charge-generated bath space be

\[
 \widehat A=\operatorname{span}\{Q_E^n a':a'\in A,\ n=0,1,2,\ldots\},
 \qquad \widehat L=S\otimes\widehat A\otimes|0_R\rangle.
\]

Finite dimensionality makes this span stabilize. It is the least Q_E-invariant linear subspace containing A, equivalently the span of the spectral projections of vectors in A. Lhat is invariant under K. This is a mathematical space on which a conservation law may be **asserted**; it does not posit new experimentally available input preparations.

**Lemma 2 (finite commuting completion).** If a subspace M of the finite joint Hilbert space is K-invariant and `D P_M=0`, there exists a globally K-commuting unitary U_c that agrees with U on M.

**Proof.** For each eigenvalue kappa of K, set `M_kappa=M intersect ker(K-kappa I)`. Hermiticity and invariance give the orthogonal decomposition `M=direct_sum M_kappa`. For x in M_kappa, `K Ux=U Kx=kappa Ux`; hence U is an isometry from M_kappa into the same full K-eigenspace. Extend this isometry to a unitary on that finite eigenspace by completing orthonormal bases. Taking their orthogonal direct sum over kappa gives U_c. It commutes with K and agrees with U on M. QED.

**Corollary 3.** Under the supplied benchmark and spectral exclusion, the condition `D P_Lhat=0` suffices for `q(rho)=rho_uu` for every rho and `Delta=1/5`.

**Proof.** Apply Lemma 2 with M=Lhat. Original input states have support in L, contained in Lhat, so replacing U by U_c changes none of their joint output states. In particular U_c implements the same exact C on the original preparation tau. PR147's globally conserving theorem now applies and gives the stated effect law. There is no need to assume that C holds with arbitrary replacement bath states from Ahat. QED.

The reduction to PR147 is intentional. This corollary is a completion consequence of the earlier conditional theorem, **not a new physical mechanism or a newly enlarged class of prepared behaviors**.

### 3.1 Invariant support as a sufficient special case

If A itself is Q_E-invariant, then `Ahat=A`, and the prepared-input condition already supplies the corollary's domain. Stationarity `[tau,Q_E]=0` is sufficient for support invariance but is not required. For example, a full-rank coherent tau has the entire bath as its invariant support even though tau need not commute with Q_E. Full rank is also sufficient, not necessary; rank-deficient states supported within an invariant spectral subspace are included.

The actual U may violate conservation outside Lhat. Its action on the original preparations nevertheless has a globally conserving completion, so the observable outcome falls within PR147's admitted class. The corollary makes no claim that U equals U_c off the asserted conservation domain, or that the domain condition is necessary or minimal among all sufficient physical premises.

In Proposition 1, Ahat is exactly A_0. The failed companion direction a_perp lies in Ahat and reveals why the stronger domain check rejects the blind realization. This diagnoses a concrete missing implication rather than changing the source pair, effect, receiver, or bath charge gap.

## 4. Provenance, peer follow-up and disposition

PR147's argument and adjudication are pinned at `70b14bf9303a42da831a22ef22f1473f5d4a396d`; its argument blob remains `b2f47d735e30c7ee8ffd5fc1bf859269626fd4d3`. It explicitly used global blocks before restriction to supp(tau). Its proof is unchanged by the present counterexample.

The inspected `joint_balance_delivery/ATTEMPT.md` at research parent `2ab565c3f5bf10305a96ddeef30901de49959ba5` distinguished a no-bath-contribution first-moment balance on an input isometry from full joint commutation. Its response preserved native restriction deficits without assigning them to a receiver. Neither inspected predecessor states the explicit prepared-vector counterexample above. The completion corollary is elementary finite spectral linear algebra. No archive-wide or literature novelty is claimed.

Grok's Q193/Q194 peer check and the existing scope reply (PR111 comments [6844737841](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6844737841) and [6845069695](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6845069695)) leave PR147 unchanged. The rank inequality and blank-receiver conclusion cover arbitrary bath rank; only the empty-class corollary uses finite full rank. Spectrum `{0,2}` shows that bandwidth below one is unnecessary for no-unit-gap, not that no-unit-gap is unnecessary.

The suggested rank-obstruction citation was verified in the primary paper: Reeb and Wolf, *An improved Landauer principle with finite-size corrections*, New Journal of Physics 16, 103011 (2014), [§3.3, Proposition 5 and following rank remark](https://arxiv.org/pdf/1306.4352), doi:[10.1088/1367-2630/16/10/103011](https://doi.org/10.1088/1367-2630/16/10/103011). Its finite-reservoir rank restriction explains the full-rank part of PR147's obstruction once the receiver is forced blank. Taking the paper's system as S tensor R makes the input rank two and target rank one. Writing a full-rank tau formally as a Gibbs state for `-log(tau)` does not identify that auxiliary Hamiltonian with the proposed Q_E or any native charge. This citation supplies context, not a native mechanism or a proof of Proposition 1.

**What is earned:** a concrete counterexample to a tempting weakening of the added conservation premise, and a sufficient domain on which conservation can instead be asserted. Non-invariance of the prepared support is essential to this particular evasion; no statement that every coherent or rank-deficient bath evades selection is made.

**What remains unearned:** native `pi_u` charge, physical additive conservation, the bath spectrum, and actual same-owner action/access. The charge-generated space and its conservation law are not inherited operations of P1. Native bridge remains NOT_DERIVED; no physical signal, GR claim, empirical result, stage closure, or time parameter is introduced. The next native step still needs a specifically sourced event operation and its typed owner output, not repeated audits of this completed conditional diagnostic.
