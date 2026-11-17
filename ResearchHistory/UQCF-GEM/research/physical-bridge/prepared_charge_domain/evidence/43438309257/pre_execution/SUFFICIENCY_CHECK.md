# Prepared-domain charge conservation: sufficient theorem and provenance boundary

Status: **conditional analytical self-check; native bridge NOT_DERIVED.**

This note proves a restricted-domain corollary of the existing charge-selection argument. It does not propose a native mechanism, infer a physical conservation law, certify a new research stage, or claim a weakest physical premise. The charge assignments, spectral exclusion, quantum correspondence, preparation/access assumptions and any asserted domain of conservation remain **SUPPLIED/NEW**. No scientific or numerical execution, new model review, GitHub mutation, or broad source census was performed.

## 1. Exact setting and result

Keep the four-dimensional source with basis `(o,p,u,v)`,

\[
 Q=I_S-\pi_u,\qquad
 C(\rho)=Q\rho Q+\rho_{uu}\pi_p.
\]

The bath E is finite-dimensional, with a fixed density matrix \(\tau\) and Hermitian charge \(Q_E\). Write

\[
 A=\operatorname{supp}\tau,\qquad P_A=\text{orthogonal projection onto }A.
\]

The same receiver R is a qubit, initially \(|0_R\rangle\), with the same fixed effect and charge

\[
 F_R=|1_R\rangle\langle1_R|.
\]

Let U be one source-independent unitary on \(S\otimes E\otimes R\), and define, with tensor identities understood,

\[
 K=\pi_u+Q_E+F_R,\qquad J_R=I_{SE}\otimes F_R,
\]

\[
 L=S\otimes A\otimes|0_R\rangle,\qquad
 P_L=I_S\otimes P_A\otimes\pi_{0,R}.
\]

Retain the exact all-input implementation assumption

\[
 \operatorname{Tr}_{ER}\!\left[U(\rho\otimes\tau\otimes\pi_{0,R})U^\dagger\right]
 =C(\rho)
 \quad\text{for every source density matrix }\rho,
 \tag{1}
\]

and the existing no-unit-gap condition

\[
 \operatorname{spec}(Q_E)\cap\bigl(\operatorname{spec}(Q_E)+1\bigr)=\varnothing.
 \tag{2}
\]

Replace global commutation by the actual vector identity

\[
 (KU-UK)P_L=0.
 \tag{3}
\]

**Invariant-support theorem.** If, in addition,

\[
 Q_E A\subseteq A,
 \quad\text{equivalently in this finite Hermitian setting}\quad
 [Q_E,P_A]=0,
 \tag{4}
\]

then the receiver effect pulled back to S for the specified preparation is

\[
 M_\tau=\pi_u,\qquad
 q(\rho)=\operatorname{Tr}[M_\tau\rho]=\rho_{uu}.
 \tag{5}
\]

Thus the original fixed pair has signed contrast \(\Delta=1/5\). More strongly, on the entire prepared vector subspace,

\[
 J_R U P_L=U(\pi_u\otimes I_{ER})P_L.
 \tag{6}
\]

The stronger relation implies the same receiver probability for any bath density matrix supported in A. That is a mathematical consequence about this fixed U, not a new premise asserting that such alternative bath preparations are physically available.

## 2. Full direct proof

### 2.1 Exact pure system outputs control every vector in the occupied support

For a retained label \(a\in\{o,p,v\}\), (1) gives source output \(\pi_a\); for input u it gives source output \(\pi_p\). Set \(f(a)=a\) and \(f(u)=p\).

Diagonalize \(\tau\), only for this support argument:

\[
 \tau=\sum_{i=1}^{k}t_i|e_i\rangle\langle e_i|,
 \qquad t_i>0,
 \qquad \operatorname{span}\{e_i\}=A.
\]

For any source basis label t, let

\[
 |\Psi_{t,i}\rangle=U|t,e_i,0_R\rangle.
\]

The probability of finding the output system outside \(|f(t)\rangle\) is zero. Consequently,

\[
 0=\sum_i t_i\left\|
 \bigl((I_S-\pi_{f(t)})\otimes I_{ER}\bigr)|\Psi_{t,i}\rangle
 \right\|^2.
\]

Every summand is nonnegative and every \(t_i\) is strictly positive. Each summand therefore vanishes. By linearity,

\[
 U\bigl(|t\rangle\otimes A\otimes|0_R\rangle\bigr)
 \subseteq |f(t)\rangle\otimes E\otimes R.
 \tag{7}
\]

This conclusion holds for all vectors in A even when they are not eigenvectors of \(\tau\). It uses no cancellation between a bath mixture's components and no assumption that those vectors are independently preparable.

### 2.2 The restricted conservation law is an intertwiner because L is invariant

Equation (4), together with \(F_R|0_R\rangle=0\), implies \(K L\subseteq L\). Since K is Hermitian, L is reducing and \([K,P_L]=0\).

Identify L with \(S\otimes A\) through the blank-receiver inclusion, and set

\[
 W\psi=U(\psi\otimes|0_R\rangle),\qquad
 K_L=\pi_u\otimes I_A+I_S\otimes Q_E|_A.
\]

Equation (3) now says exactly

\[
 KW=WK_L.
 \tag{8}
\]

The argument requires K to preserve the **input** domain L. It does not assume that U preserves L; input u must in fact acquire receiver value 1.

### 2.3 Diagonalize charge on A, not the bath density matrix

Because A is invariant, choose an orthonormal basis \(g_\alpha\) of A satisfying

\[
 Q_Eg_\alpha=\lambda_\alpha g_\alpha.
\]

This basis need not diagonalize \(\tau\). Equation (7) nevertheless applies to it.

For a retained a, write

\[
 U|a,g_\alpha,0_R\rangle
 =|a\rangle\otimes
   \bigl(|b_0\rangle\otimes|0_R\rangle
        +|b_1\rangle\otimes|1_R\rangle\bigr).
\]

The input is a K eigenvector of eigenvalue \(\lambda_\alpha\). Equations (3)/(8) make the output an eigenvector with the same eigenvalue, so

\[
 (Q_E-\lambda_\alpha)b_0=0,
 \qquad
 (Q_E-(\lambda_\alpha-1))b_1=0.
\]

Since \(\lambda_\alpha\in\operatorname{spec}(Q_E)\), (2) forbids \(\lambda_\alpha-1\) from being a bath eigenvalue. Hence \(b_1=0\): the receiver stays blank on each retained input and every bath vector in A.

For input u, (7) instead permits only system p. Write

\[
 U|u,g_\alpha,0_R\rangle
 =|p\rangle\otimes
   \bigl(|c_0\rangle\otimes|0_R\rangle
        +|c_1\rangle\otimes|1_R\rangle\bigr).
\]

The initial total-charge eigenvalue is \(\lambda_\alpha+1\), giving

\[
 (Q_E-(\lambda_\alpha+1))c_0=0,
 \qquad
 (Q_E-\lambda_\alpha)c_1=0.
\]

Equation (2) forbids the first bath eigenvalue, so \(c_0=0\). Unitarity preserves the vector norm; thus the receiver is certainly 1 on input u. Linearity over the source labels and the charge eigenbasis of A proves (6).

### 2.4 All coherent source inputs are covered

For completeness, the fixed ancillary state and U define a receiver POVM effect \(M_\tau\) on S satisfying \(0\le M_\tau\le I_S\). The preceding steps yield

\[
 (M_\tau)_{aa}=0\quad(a=o,p,v),\qquad
 (M_\tau)_{uu}=1.
\]

Positivity gives \(|(M_\tau)_{ij}|^2\le (M_\tau)_{ii}(M_\tau)_{jj}\). Every off-diagonal entry has at least one retained index and therefore vanishes. Hence \(M_\tau=\pi_u\), proving (5) on coherent as well as diagonal inputs. Equivalently, (6) directly gives \(W^\dagger J_RW=\pi_u\otimes I_A\). QED.

No quiet-reference law, vanishing bath-charge change, prescribed charge allocation, or receiver expectation balance was inserted into this proof. The quiet receiver on retained inputs is derived. Indeed the proof also yields, on \(S\otimes A\),

\[
 (I_S\otimes Q_E\otimes I_R)W=W(I_S\otimes Q_E|_A),
\]

so preservation of the bath charge is itself a consequence in this admitted class. Preservation of the complete bath state is neither assumed nor implied.

## 3. Globally conserving completion: the operational scope of the weakening

The following finite-dimensional fact is independent of the channel C and the bath-gap assumption.

**Completion lemma.** Let H be finite-dimensional, K Hermitian, D a K-invariant subspace, and U unitary on H. If \((KU-UK)P_D=0\), there is a unitary V on H such that

\[
 [K,V]=0,\qquad VP_D=UP_D.
 \tag{9}
\]

**Proof.** Decompose H into total-charge eigenspaces \(H=\bigoplus_\kappa H_\kappa\). Hermiticity and invariance give

\[
 D=\bigoplus_\kappa D_\kappa,\qquad D_\kappa=D\cap H_\kappa.
\]

For \(x\in D_\kappa\), restricted conservation gives \(KUx=UKx=\kappa Ux\). Thus U maps \(D_\kappa\) isometrically into \(H_\kappa\). Extend that isometry to a unitary \(V_\kappa\) on \(H_\kappa\) by completing orthonormal bases in its domain and range. The finite dimensions of the two complements agree. Then \(V=\bigoplus_\kappa V_\kappa\) has both properties in (9). QED.

Conversely, if such a V agrees with U on an invariant D, then \((KU-UK)P_D=0\): U and V agree both on x and on Kx for x in D.

Applying the lemma to D=L shows that the invariant-support theorem is also a direct corollary of PR147's global theorem. The completion V implements exactly the same prepared operation as U because all original preparations are supported in L. It inherits exact C on the original \(\tau\), and the original theorem applies.

This is a strict relaxation of what is asserted about the **actual unitary on unprepared vectors**: U itself need not globally commute with K. It is not an enlargement of the class of operations observed from this invariant prepared domain. Every such prepared operation has a globally conserving realization. The completion is a mathematical existence statement, not an additional enactment or control operation.

## 4. Non-invariant bath support: conservation on its invariant hull is sufficient

For arbitrary \(A=\operatorname{supp}\tau\), define its least \(Q_E\)-invariant subspace

\[
 \widehat A=\operatorname{span}\{Q_E^n a:a\in A,\ n\ge0\},
 \qquad
 \widehat L=S\otimes\widehat A\otimes|0_R\rangle.
 \tag{10}
\]

Finite dimensionality makes this a finite span; Hermiticity makes \(\widehat A\) reducing. The adjective “least” here concerns only an ordinary invariant-subspace construction, not a claim of a weakest physical conservation premise.

**Invariant-hull corollary.** Keep (1), (2), the same U, the same \(\tau\), and the same receiver. Without assuming A itself invariant, the stronger domain-of-law condition

\[
 (KU-UK)P_{\widehat L}=0
 \tag{11}
\]

still implies \(M_\tau=\pi_u\) and \(\Delta=1/5\).

**Proof.** The subspace \(\widehat L\) is K-invariant. The completion lemma supplies a globally commuting V with \(VP_{\widehat L}=UP_{\widehat L}\). Since \(L\subseteq\widehat L\), V and U agree on every vector supporting \(\rho\otimes\tau\otimes\pi_{0,R}\). Their resulting full output states, and therefore their source channels and receiver effects for this preparation, are identical. V thus satisfies exactly the original all-input source condition (1) for the original \(\tau\), plus global conservation and (2). PR147 Theorem A gives \(M_\tau^V=\pi_u\); equality of the prepared outputs gives \(M_\tau^U=\pi_u\). QED.

There is **no assumption that C is implemented for alternative bath states supported throughout \(\widehat A\)**. In particular, the pure-output support argument in Section 2.1 must not be extended from A to \(\widehat A\) just because the latter is an algebraic hull. The completion proof deliberately avoids that invalid inference. Nor does (11) assert that the hull vectors can physically be prepared. It enlarges the vector domain on which the **NEW conservation law is stipulated**, not the operational preparation repertoire.

If conservation is stated only on the original non-invariant L, then Kx can lie outside L for x in L. The identity \(KUx=UKx\) consequently involves U on unprepared vectors. It no longer says that \(U|_L\) intertwines two self-adjoint restrictions, and the completion proof above does not apply. Neither the invariant-support theorem nor the hull corollary licenses silently replacing (11) by conservation only on L in that case. A failure or counterexample at a hull direction is a diagnostic of precisely this missing domain of law.

## 5. Input and operational assumption audit

| Issue | Exact status in the proof |
|---|---|
| Stationarity \([Q_E,\tau]=0\) | Not assumed. It implies support invariance, but support invariance does not imply stationarity. |
| Full rank of \(\tau\) | Not assumed. Full rank makes A=E and its invariance automatic, including for nonstationary \(\tau\). |
| Rank-one bath | An invariant one-dimensional support is a charge eigenspace, so in this special case support invariance does force stationarity. |
| Coherence in \(\tau\) | Allowed. The proof diagonalizes \(\tau\) for positivity and later diagonalizes \(Q_E|_A\); these may be different bases. |
| Physical preparation of bath eigenvectors | Not needed. The support statements follow mathematically from the single specified mixed bath preparation. |
| Exact source action | The supplied all-input C is retained. For the effect-only proof, its four pure basis-output statements already suffice. Knowing C only on the two fixed mixed benchmark inputs would not establish those statements. |
| Fixed preparation and implementation | One product ancillary preparation and one source-independent U are essential supplied benchmark conditions. Input-dependent dynamics or source-bath correlations are not introduced. |
| Complete receiver state | The result fixes F_R probabilities and basis-input flags. It does not assert that the whole receiver state depends only on \(\rho_{uu}\); p/u coherence can survive off-diagonally. |
| Meaning of conservation | Equation (3) is a vector identity, not merely a compressed first-moment identity or equality of expectations on the two benchmark preparations. |
| Finite bath | Used in the simple eigenspace proof and completion lemma; no infinite-dimensional or unbounded-observable extension is claimed. |
| Native provenance | Neither support invariance, hull-domain conservation, physical \(Q_S=\pi_u\), the bath restriction, nor owned access to F_R follows from native total-grade accounting. |

For a concrete nonstationary, rank-deficient example admitted by the sufficient theorem, take

\[
 Q_E=\operatorname{diag}(0,2,4),\qquad
 \tau=\begin{pmatrix}1/2&1/4&0\\1/4&1/2&0\\0&0&0\end{pmatrix}.
\]

The support is the span of the first two charge eigenvectors, hence invariant. The two positive eigenvalues of \(\tau\) are \(3/4\) and \(1/4\), while \([Q_E,\tau]\ne0\). There is no unit bath gap. The original receiver writer \(W_R\), acting trivially on E, satisfies global conservation and hence every restricted condition above, and implements exact C. Thus nonstationarity is compatible with a nonempty admitted class.

## 6. Narrow comparison with the specified previous work

Only the embedded earlier `joint_balance_delivery/ATTEMPT.md` and `REVIEW_RESPONSE.md`, the supplied PR147 argument and its local adjudication/review text, and PR147's current metadata/discussion were inspected for this comparison. No wider archive novelty search is implied.

### 6.1 Verified identities and live PR scope

| Inspected source | Verified identity / scope |
|---|---|
| Embedded earlier ATTEMPT in `charge_selection_work/sources.json` | Git blob `460adf6765933130ca718e850992cdce92320ae7`; SHA-256 `4c5f69f2e5c85791f7f5ca38f6170ef0d24d35ab5963f49b0152ea8179d33b64`; bytes and both identities recomputed from embedded UTF-8 content. |
| Embedded earlier REVIEW_RESPONSE in the same file | Git blob `e26e6a39a1b33e74c896141694d4453d3cd9f49b`; SHA-256 `bb4f91fc17f2c99b95ac15ebe788e92759f97c1985c5f2374752f4f1fd2031da`; bytes and both identities recomputed. |
| Supplied PR147 ARGUMENT.md | Git blob `b2f47d735e30c7ee8ffd5fc1bf859269626fd4d3`; SHA-256 `571cbbbab58e60c8f981290bdc51f80d06a79ee6dbbd98d91c07f54c64686a72`; blob recomputation matches PR147's declared argument freeze. |
| [PR147](https://github.com/proteinfoldingengine/WetLabEngine/pull/147), read 2026-11-13 UTC | Head `70b14bf9303a42da831a22ef22f1473f5d4a396d`; body states global commutation. The fetched merged discussion timeline contained no comments. |

The two embedded earlier documents were pinned in `sources.json` at research parent `2ab565c3f5bf10305a96ddeef30901de49959ba5`. Their own original chronology is preserved in their content; no new chronology is inferred from the later embedding.

### 6.2 What was already resolved, and what this note actually adds

The earlier ATTEMPT §§4–5 already proved that, for a nonzero source charge difference d, the **no-environment all-input first-moment balance**

\[
 W^\dagger(Q_S+dJ_R)W=Q_S
\]

is equivalent, in that supplied benchmark, to

\[
 W^\dagger J_RW=\pi_u
 \quad\Longleftrightarrow\quad
 J_RW=W\pi_u.
\]

Its §7 also exposed environmental absorption when E contributes to the total balance. The REVIEW_RESPONSE §§2–3 retained those results and explained why a native source restriction deficit does not allocate charge to the named receiver. Neither inspected earlier document formulated the condition \([K,U]P_L=0\), the invariant-support repair, or the invariant-hull condition (11). The sharp writer conclusion itself is emphatically not new.

PR147 proved global-commutator charge selection with no unit bath gap for arbitrary \(\tau\), explicitly including non-invariant support. Its argument and recorded review use a global bath-block identity before restricting to occupied bath support. The inspected texts do not formulate the exact prepared-vector condition or the hull-domain refinement above.

The precise narrow result here is therefore: **the invariant-support/hull-domain formulations are not expressly resolved in those inspected texts, but their positive conclusion is already a completion corollary of PR147.** They identify the domain on which conservation must be asserted for that completion argument. They do not provide a new physical mechanism, an enlarged operational class on an invariant domain, a repaired native correspondence, or a universal minimality result. Any separate non-invariant-support counterexample addresses the false shortcut of shrinking the conservation domain without preserving the relevant charge-orbit directions; it does not negate PR147's global theorem.

Native bridge status remains **NOT_DERIVED**.

## 7. Check of the final assembled argument before freeze

The assembled `prepared_charge_work/package/ResearchHistory/UQCF-GEM/research/physical-bridge/prepared_charge_domain/ARGUMENT.md` was read after the proof above, specifically its fixed-premise statement, finite commuting-completion lemma, hull corollary, invariant-support special case, and provenance/disposition. No blocking mathematical or scope error was found in those assigned sections.

Its Lemma 2 correctly invokes Hermiticity and invariance to decompose the asserted conservation domain by total-charge eigenspaces. Its Corollary 3 transfers the original product-preparation outputs from U to its globally conserving completion; it therefore needs exact C only for the original \(\tau\). Its explicit rejection of replacement-bath channel and preparation assumptions is correct. Its identification of the positive result as a completion corollary of PR147, rather than a new mechanism or an enlarged class of prepared behavior, is supported by the proof here. The source/provenance claims remain appropriately conditional and narrow.

This final check concerns the completion/domain proof and its framing. The explicit non-invariant-support counterexample was assigned to the parent analysis, and the additional peer-comment/literature details in the assembled argument were not independently re-sourced by this subtask.
