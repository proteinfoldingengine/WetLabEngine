# Charge statistics, receiver response, and vector completion

Status: **NEW-assumption analytical diagnostic; native bridge NOT_DERIVED.** This note answers the next bounded question after PR148 and integrates Grok's Q196 completion criterion. The results and explicit controls below were derived analytically before the review freeze. They do not provide a new native operation, physical conservation law, detector, empirical signal, or numbered-stage certification.

## 1. Fixed benchmark and three different conservation claims

Keep the source basis `(o,p,u,v)`, projectors `pi_j=|j><j|`, `Q=I_S-pi_u`, and exact all-input channel

\[
 C(\rho)=Q\rho Q+\rho_{uu}\pi_p.
\]

The finite bath E has a fixed, arbitrary density matrix tau and Hermitian charge Q_E. The same receiver R is a qubit, initially `|0_R>`, with the same fixed effect/charge `F_R=|1_R><1_R|`. One source-independent global unitary U acts on S tensor E tensor R, starting from

\[
 \omega_\rho=\rho\otimes\tau\otimes\pi_{0,R},\qquad
 K=\pi_u+Q_E+F_R,
\]

with tensor identities implicit in K. Tracing the output over E,R must give C(rho) for every source input. Let `Lambda=spec(Q_E)` and retain

\[
 \Lambda\cap(\Lambda+1)=\varnothing.
\]

Define `q(rho)=Tr[(I_SE tensor F_R)U omega_rho U†]`. The unchanged pair is `rho^(0)=diag(1,1,2,1)/5`, `rho^(1)=diag(1,1,1,2)/5`, so its signed contrast is `(q(pi_u)-q(pi_v))/5` by linearity.

| Claim | Meaning |
|---|---|
| Global conservation of the specified unitary | `[K,U]=0` |
| Prepared charge-statistics conservation | `Tr[P_kappa(K) U omega_rho U†]=Tr[P_kappa(K) omega_rho]` for every K outcome kappa and every original source rho, at the fixed tau |
| Vectorwise conserving completion | Some unitary U_c commutes with K and agrees with U on every vector of `L=S tensor supp(tau) tensor |0_R>` |

The second claim concerns endpoint probability distributions. It does not prescribe a sequential measurement, a two-time measurement protocol, microscopic transitions, or new physical preparations. The third claim specifies individual vectors, a stronger identification than equality of the mixed prepared output channel. None implies uniqueness of a unitary.

**Premise ledger.** Hilbert factorization, normalized encoding, exact C, product preparation and same-owner effect access remain SUPPLIED. The physical singleton charge pi_u, Q_E, F_R as charge, bath exclusion, and any conservation statement remain NEW. Native preserved total grade is not identified with pi_u or K. Actual event occurrence remains ACCEPTED INPUT. No physical-time coordinate or energy interpretation is introduced.

## 2. The charge-sector event and the response guarantee

Put `Gamma=Lambda+1`, and let `P_Gamma(K)` be the spectral projector of K onto all its eigenvalues in Gamma. The exclusion implies that Gamma is disjoint from both Lambda and Lambda+2. The latter follows because `lambda+1=mu+2` would give a forbidden unit difference between lambda and mu. Possible overlap of Lambda with Lambda+2 is harmless.

Consequently, on the **full joint Hilbert space**,

\[
 P_\Gamma(K)=\pi_u\otimes I_E\otimes\pi_{0,R}
                 +Q\otimes I_E\otimes F_R.                 \tag{1}
\]

Indeed the S,R charge is 0, 1 or 2; precisely its charge-one sector has total charge in Gamma. Equation (1) is not globally equal to pi_u or F_R separately.

On the initial blank-receiver states, (1) gives

\[
 \operatorname{Tr}[P_\Gamma(K)\omega_\rho]=\rho_{uu}.       \tag{2}
\]

Every output source marginal C(rho) is supported in Q. Positivity of the joint output therefore confines that full state to `Q tensor E tensor R`: a zero expectation of the complementary source projection makes its support lie in the projection's kernel. On this output subspace, (1) restricts to `I_Q tensor I_E tensor F_R`. Hence

\[
 \operatorname{Tr}[P_\Gamma(K)U\omega_\rho U^\dagger]=q(\rho). \tag{3}
\]

**Proposition 1 (statistical sufficiency).** Prepared conservation of the full K distribution implies `q(rho)=rho_uu` for every rho and contrast 1/5 for the fixed pair. This holds for arbitrary coherent or mixed tau and source rho.

**Proof.** Sum the conserved K-outcome probabilities over Gamma and apply (2)-(3). QED.

**Exact equivalence, not a new mechanism.** Conservation of just the single coarse event Gamma for all original source inputs is **equivalent** to the already-known sharp-writer effect law `q(rho)=rho_uu`, within this supplied exact-C/no-gap benchmark. This is a different expression of the required output law, not an independent native explanation of it. Full-distribution conservation is a stronger sufficient physical assumption; it is not identified with native grade preservation.

### 2.1 Sufficient basis checks and what they do not assume

It suffices for Proposition 1 that the full distributions (or the Gamma probabilities) match on the four source basis inputs. Those checks give receiver-effect diagonal entries 0 on retained labels and 1 on u. For the induced POVM effect `0<=M<=I`, positivity `|M_ij|²<=M_ii M_jj` removes all off-diagonal entries, so `M=pi_u` and the conclusion extends to coherent inputs. This is a sufficient check set, not a minimality claim or an assertion that such input preparations are physically available.

For only the fixed-pair contrast, the direct calculation already needs just the u and v checks: they give q(pi_u)=1 and q(pi_v)=0. No full recovery of the source or its observable algebra is required. These are mathematical sufficiency statements under the all-input benchmark, not a proposed experimental protocol or an additional requirement on native access.

## 3. The vectorwise completion criterion supplied by Q196

Grok's Q196 proposed an exact criterion for agreement with a conserving unitary. The following spectral-projector proof gives a finite version and makes its scope explicit.

**Theorem 2.** Let K be Hermitian on a finite-dimensional H, with r distinct eigenvalues, let L be any subspace, and let U be unitary. A K-commuting unitary U_c satisfying `U_c|_L=U|_L` exists if and only if

\[
 \langle x,P_\kappa(K)y\rangle
   =\langle Ux,P_\kappa(K)Uy\rangle
 \quad\text{for all }x,y\in L\text{ and every }\kappa.     \tag{4}
\]

Equivalently it suffices and is necessary that

\[
 \langle x,K^n y\rangle=\langle Ux,K^n Uy\rangle,
 \qquad n=0,\ldots,r-1,\quad x,y\in L.                    \tag{5}
\]

These conditions are also equivalent to the same identities for all n>=0. The n=0 equality is automatic by unitarity.

**Proof.** Necessity follows because a commuting unitary preserves every spectral projector. For sufficiency, fix kappa and define

\[
 T_\kappa(P_\kappa x)=P_\kappa Ux\quad(x\in L).
\]

Equation (4) is equality of the Gram forms of these projected vectors. It makes T_kappa well defined and isometric from `P_kappa L` onto `P_kappa U L`. Complete orthonormal bases to extend it to a unitary of the whole finite eigenspace of K. The orthogonal sum of these extensions commutes with K and maps each x in L to `sum_kappa P_kappa Ux=Ux`. Finally, each spectral projector is a polynomial in K of degree at most r-1 by interpolation on the distinct eigenvalues; powers of K are linear combinations of the projectors. This proves the moment equivalences. QED.

For non-invariant L, the projected space `P_kappa L` need not equal `L intersect ker(K-kappa I)`. Substituting the latter would invalidate the general proof.

Equality of the K distribution for **every pure vector in L** implies (4) by polarization. That is not generally what varying rho at one fixed mixed bath tau supplies. The original mixed preparation family spans `B(S) tensor span{tau} tensor pi_0,R`, not all operators supported on L.

If tau is pure, every pure vector in L is a source vector tensored with its fixed bath and blank receiver. Prepared distribution conservation for all source inputs then is equivalent to vectorwise completion. For a mixed tau, that equivalence can fail, as the next section demonstrates.

### 3.1 Relation to the earlier commutator conditions

Write D=KU-UK. For **K-invariant** L, vectorwise completion is equivalent to `D P_L=0`: sufficiency is PR148's finite commuting-completion lemma, and necessity holds because U and U_c agree both on x and on Kx in L.

For arbitrary, possibly non-invariant L, `D P_L=0` is neither necessary nor sufficient in general. Non-sufficiency is PR148's counterexample: the third moment changes, so Theorem 2 also proves that no conserving unitary agrees on its prepared vectors. For non-necessity, the elementary example `K=diag(0,1)`, `U=X`, `L=span((|0>+|1>)/sqrt2)` has identity as a conserving completion but nonzero `[K,U]` on L. This last example is a linear-algebra control, not a new source-benchmark realization.

PR148's charge-generated-hull condition `D P_Lhat=0` remains a sufficient condition. The exact criterion (4) instead asks whether **some** extension agrees on L; it does not require the specified U to have the conserving action on unprepared hull vectors. No globally weakest physical-premise claim is made.

## 4. Mixed preparation: identical complete outputs without vectorwise completion

Choose a bath qubit with basis `(e_0,e_2)` and

\[
 Q_E=\operatorname{diag}(0,2),\qquad \tau=I_E/2,\qquad
 X_E e_0=e_2,\quad X_E e_2=e_0.
\]

The bath spectrum has no unit gap. Let W_R be the global source-receiver unitary exchanging `|u,0_R>` and `|p,1_R>` while fixing all other S,R basis vectors. Both exchanged vectors have source-plus-receiver charge one; thus W_R commutes with K when extended by identity on E.

Set `U=W_R X_E`, with the factors acting on disjoint S,R and E systems. For every source operator rho,

\[
 U\omega_\rho U^\dagger
 =W_R(\rho\otimes X_E\tau X_E^\dagger\otimes\pi_{0,R})W_R^\dagger
 =W_R\omega_\rho W_R^\dagger.                             \tag{6}
\]

This is equality of the **entire SER output**, before any partial trace. It holds for coherent as well as diagonal source inputs. The W_R construction preserves every retained-retained source matrix unit, maps pi_u to pi_p, and erases off-diagonal source units involving u after tracing R. Hence U implements all of C and has `q(rho)=rho_uu`. Equation (6) and `[K,W_R]=0` show that every total-charge outcome probability is conserved for all original rho.

Yet the specified U does not commute with K. On `x=|o,e_0,0_R>` one has `Kx=0` while `Ux=|o,e_2,0_R>` has total charge 2. Thus `D x=2Ux`. Since tau has full rank,

\[
 L=S\otimes E\otimes|0_R\rangle
\]

contains x and is K-invariant (it is not U-invariant). A commuting unitary U_c agreeing with U on L would send this charge-zero x to the same charge-two Ux, which is impossible.

The distinction is therefore exact:

| Requirement for this fixed mixed preparation | Verdict |
|---|---|
| Full K distributions conserved for every source rho | Yes |
| Same complete prepared SER output as a conserving realization | Yes, explicitly W_R |
| Specified U globally commutes with K | No |
| Some conserving unitary agrees vectorwise with that U on all of L | No |
| Required fixed receiver response | Yes, exactly rho_uu |

There is **no channel-level nonexistence claim**. W_R itself supplies the conserving realization of the same full prepared channel. Fixed full-rank support does not make every bath pure state an independently available input. The bath flip permutes equally weighted components; their individual charge changes are invisible in the stipulated mixed output, while their vector actions differ.

### 4.1 The writer law does not imply full charge-statistics conservation

For a rejecting control, keep the same charges and the same U=W_R X_E but replace the supplied bath preparation by `tau=|e_0><e_0|`. The source channel and receiver law are still exact because X_E acts only on E. For the retained input o, total charge changes from the certain value 0 to the certain value 2, so full K statistics are not conserved. This is a separate explicitly identified preparation, not a counterexample at the mixed tau of (6).

It shows why the implication “full prepared statistics conservation => writer law” is not an equivalence. The equivalence in §2 concerns only the coarse event Gamma. Promoting that equivalent event equation into an independently derived physical mechanism would merely rename the target.

## 5. Peer precision, provenance and stopping scope

The exact Q196 text is preserved in PEER_CONTEXT.json, attributed to comment [6855309114](https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6855309114). Its vector-completion criterion is sustained by Theorem 2. Two reported details need explicit interpretation:

- For PR148's full SER defect, the **operator norm is 2** and the **Frobenius norm is 4**. Its nonzero SE block is `[[0,-B†],[B,0]]`, with `B=2|b_perp><a_perp|`; it has two singular values 2. Tensoring with I_R duplicates them to four singular values 2. Q196's unqualified value 4 should be labeled Frobenius, not operator norm.
- Q196 reports a three-label `{u,p,j}` check of nine matrix units. The original four-label source has sixteen. Algebraically the omitted retained label is fixed with the same bath vector, so all retained cross units are preserved and the u cross units vanish; no numerical rerun is needed. The restricted numerical count should not be described as a full sixteen-unit replay.

The claim “D P_L is neither necessary nor sufficient” is for arbitrary subspaces that may be non-invariant; for invariant L the equivalence in §3.1 applies. Q196's numerical hashes were abbreviated, so this note does not claim to have downloaded or reproduced its local posthoc programs. Its analytical statements were checked directly.

PR147 ARGUMENT.md remains pinned at `70b14bf9303a42da831a22ef22f1473f5d4a396d`, blob `b2f47d735e30c7ee8ffd5fc1bf859269626fd4d3`. PR148 ARGUMENT.md remains pinned at `f3e0642d14375a2a7e60ee42f19183ea1fa706a0`, blob `19745d887370870ae6cc138b3e441a845361f902`. Their proofs are unchanged. The new mixed-preparation example answers Q196's explicitly unexamined distinction between vector agreement and channel-level equality; it does not classify all conserving realizations of arbitrary channels. The spectral-Gram criterion is credited to Q196 and elementary finite spectral linear algebra, with no novelty claim.

**Earned:** a direct sufficient statistical condition for the same receiver response, an exact statement that its coarse-event part is the existing writer law, and a concrete separation between prepared channel equality and the stronger vectorwise unitary requirement.

**Unearned:** native source charge, physical charge-statistics conservation, bath spectral exclusion, actual owner action and effect access. No additional native correspondence is removed. This bounded statistical-versus-unitary diagnostic is complete once reviewed; it should not initiate a catalogue of equivalent conservation predicates. The native task remains a specifically sourced event operation and its typed same-owner retained consequence. Native bridge NOT_DERIVED; physical result not claimed.
