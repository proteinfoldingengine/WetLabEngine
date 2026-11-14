# Prepared charge statistics do not guarantee a conserving realization of the full channel

Date: 2026-11-13 America/Phoenix / 2026-11-14 UTC. Author: proteinfolding-gpt.
Status: analytical candidate pending independent review; native bridge **NOT_DERIVED**.

This bounded follow-up addresses the channel-level limitation identified in PR149 and its scope response: can conservation of all prepared endpoint charge statistics admit a complete prepared channel outside the class realized by globally charge-conserving unitaries? The answer is **yes with the same fixed resources in the example below**. The result is stronger than failure to complete one specified unitary vectorwise. It is deliberately narrower than an obstruction after tracing the bath or allowing different dilations.

The example and proof were obtained analytically before the review freeze. No scientific program, numerical campaign, inherited-stack replay or new numbered stage is executed. This note does not claim novelty, a classification, a minimal bath dimension, or progress from SUPPLIED to native DERIVED.

## 1. Fixed benchmark and the new resource choice

Retain the earlier four-dimensional source S with orthonormal labels `(o,p,u,v)`, `pi_j=|j><j|`, and `Q=I_S-pi_u`. The stipulated source channel is

\[
 C(\rho)=Q\rho Q+\rho_{uu}\pi_p. \tag{1}
\]

The same proper receiver R is a qubit initially in `pi_0,R`, and the same fixed available effect is `F_R=pi_1,R`. The original contrast pair remains

\[
 \rho_0=\operatorname{diag}(1,1,2,1)/5,\qquad
 \rho_1=\operatorname{diag}(1,1,1,2)/5
\]

in source order `(o,p,u,v)`, so `rho_0-rho_1=(pi_u-pi_v)/5`.

Use a **different bath preparation from PR149's qubit maximally mixed example**. Here E has basis `(e_0,e_2,e_4)` and

\[
 Q_E=\operatorname{diag}(0,2,4),\qquad
 \tau=\frac16\begin{pmatrix}2&1&0\\1&2&0\\0&0&2\end{pmatrix}. \tag{2}
\]

The subscripts denote charge eigenvalues, not physical energies or time. Tau has trace one and eigenvalues `1/2, 1/3, 1/6`, hence is strictly positive. Its diagonal is uniform and it has coherence between charge zero and charge two. In particular `[tau,Q_E]` is nonzero. The bath spectrum has no unit gap: `{0,2,4}` and `{1,3,5}` are disjoint.

The total asserted charge is

\[
 K=\pi_u\otimes I_E\otimes I_R+
 I_S\otimes Q_E\otimes I_R+
 I_S\otimes I_E\otimes F_R. \tag{3}
\]

Initial states are `omega_rho=rho tensor tau tensor pi_0,R` on **the same fixed S,E,R**. Every comparison with a candidate conserving realization below uses this identical tau, these factors, this initial receiver and this K. No replacement bath, hidden auxiliary factor or changed charge assignment is allowed in that comparison. Global eigenvalues of K may be degenerate; the proof does not assume otherwise.

Premise ledger:

| Item | Status |
|---|---|
| Hilbert factorization, normalized encoding, all-input C, product preparation and source pair | SUPPLIED benchmark |
| Proper R and operational availability of its fixed F_R | SUPPLIED; not inferred from the bath |
| Physical interpretation of pi_u, Q_E and F_R as charge | NEW, not inherited from P1 |
| Spectral exclusion and endpoint-statistics conservation as candidate restrictions | NEW |
| Qutrit tau and the explicit unitary below | New mathematical example within that conditional class |
| Any ability of the receiver to read E | Not supplied and not asserted |
| Actual event/owner/action correspondence and native receiver delivery | NOT_DERIVED |

## 2. Explicit unitary and its complete prepared outputs

Let W act on S tensor R by exchanging `|u,0_R>` and `|p,1_R>` and fixing every orthogonal basis vector. Both exchanged vectors have eigenvalue one for `pi_u+F_R`, so

\[
 [W,\pi_u+F_R]=0.
\]

Let V on E fix e_0 and exchange e_2 and e_4. Define the global unitary U by applying W on S,R and V on E. These factors commute since they act on distinct subsystems. Define

\[
 \tau'=V\tau V^\dagger
 =\frac16\begin{pmatrix}2&0&1\\0&2&0\\1&0&2\end{pmatrix}, \tag{4}
\]

and the isometry from S to S tensor R

\[
 J=\sum_{j\in\{o,p,v\}}|j,0_R\rangle\langle j|
      +|p,1_R\rangle\langle u|. \tag{5}
\]

For every source operator A, not only diagonal preparations, the complete prepared output is

\[
 \Phi_U(A)=U(A\otimes\tau\otimes\pi_{0,R})U^\dagger
          = (J A J^\dagger)_{SR}\otimes\tau'_E, \tag{6}
\]

where the right side is written in SR,E order and then placed back into the fixed S,E,R order. This is only notation for tensor positions; it does not reassign the receiver or discard E.

Equation (6) gives (1) on every one of the sixteen source matrix units. A retained-retained unit `|j><k|` becomes `|j,0><k,0|`. The u,u unit becomes `|p,1><p,1|`. A u-retained unit becomes `|p,1><j,0|`, whose R trace vanishes; its adjoint behaves likewise. Thus

\[
 \operatorname{Tr}_{ER}\Phi_U(\rho)=C(\rho),\qquad
 q(\rho)=\operatorname{Tr}[(I_S\otimes I_E\otimes F_R)\Phi_U(\rho)]
 =\rho_{uu}. \tag{7}
\]

The stipulated receiver therefore has the same probability difference `1/5` on the same pair. This repeats the response of the supplied writer W; it is not a new receiver effect or native mechanism.

## 3. All prepared endpoint charge distributions are conserved

Let `a=rho_uu`. Since tau and tau' both have diagonal `(1/3,1/3,1/3)` in the Q_E eigenbasis, the initial K probabilities are

| Charge k | Initial probability |
|---|---|
| `0,2,4`, separately | `(1-a)/3` |
| `1,3,5`, separately | `a/3` |
| Every other eigenvalue of K | `0` |

Initially R is blank and source charge is zero on Q and one on pi_u. Off-diagonal source or bath entries do not contribute to the spectral-projector probabilities of the diagonal operator K.

At the output, (6) has source support in Q, receiver-one probability a, and independent bath state tau' with the same charge populations. Thus the same table holds. Equivalently W preserves the S,R charge exactly, and V preserves the Q_E distribution on this **fixed** tau. Therefore

\[
 \operatorname{Tr}\big[P_k(K)\Phi_U(\rho)\big]
 =\operatorname{Tr}\big[P_k(K)\omega_\rho\big]
 \quad\text{for every source density matrix \rho and every eigenvalue k}. \tag{8}
\]

This is conservation of the full distribution, including every scalar moment, for all original prepared source inputs. It is not an assertion about independently prepared bath basis vectors, bath replacements, or arbitrary global initial states. U itself is not globally conserving: for example it moves `|o,e_2,0_R>` of charge two to `|o,e_4,0_R>` of charge four.

## 4. No conserving realization of the same full prepared channel

**Proposition.** There is no unitary Z on these same S,E,R satisfying `[Z,K]=0` and

\[
 Z(\rho\otimes\tau\otimes\pi_{0,R})Z^\dagger=\Phi_U(\rho)
 \quad\text{for all source \rho}. \tag{9}
\]

**Proof.** It is enough to consider the retained input `rho=pi_o`. Equation (6) demands the complete output

\[
 \pi_o\otimes\tau'\otimes\pi_{0,R}.
\]

Both tau and tau' have full rank three. Hence the support of both the initial and target output density matrices is exactly

\[
 L_o=|o\rangle\otimes\mathcal H_E\otimes|0_R\rangle.
\]

Unitary conjugation maps the support onto the support. Thus any Z matching this one output must map `L_o` onto itself. This is derived from the requested state equality and the already fixed full-rank preparation; it does **not** assume independent experimental preparation of every vector in `L_o`.

The restriction of Z to `L_o` is consequently an E unitary B. The restriction of K to `L_o` is Q_E. If `[Z,K]=0`, then `[B,Q_E]=0`. Since Q_E has three distinct eigenvalues, B is diagonal in `(e_0,e_2,e_4)`, with entries of modulus one. Such conjugation cannot change a zero matrix entry into a nonzero entry. But (2) and (4) give

\[
 \langle e_0|B\tau B^\dagger|e_4\rangle=0,
 \qquad \langle e_0|\tau'|e_4\rangle=1/6,
\]

a contradiction. This already excludes equality for source o, and therefore excludes (9). QED.

Degeneracies elsewhere in the total K spectrum cannot evade the argument. Exact matching of the pure S,R output fixes the full three-dimensional support `L_o` before the restriction of the commutator is taken. Z may act arbitrarily on the complement subject to conservation, but that action cannot repair the forbidden entry in the required output.

This is a **prepared-channel** obstruction, not merely the claim that no conserving unitary agrees with U on every vector. We allow any candidate Z; we require it to reproduce density-operator outputs on the original preparation only. No vectorwise equality with U is demanded. The support restriction is a consequence of one such density-operator equality.

## 5. The obstruction disappears for the receiver-facing reduction

After tracing E, equation (6) gives

\[
 \operatorname{Tr}_E\Phi_U(A)=J A J^\dagger.
\]

The globally conserving `W tensor I_E` with the **same original tau** has complete output `(J A J^dagger) tensor tau` and exactly this same reduced S,R channel. Thus there is a conserving realization of the entire source-receiver output, including every receiver effect, not merely the one probability q. The difference proven above resides in the unaccessed bath state.

For another transparent control, replacing tau by its dephased state `I_E/3` makes V leave the bath state invariant. At that different preparation, U and `W tensor I_E` have identical complete S,E,R outputs. This control changes the bath preparation explicitly; it is not a counterexample to the proposition at tau in (2). Coherent off-diagonal information is the distinguishing resource here, while the conserved endpoint probabilities carry no record of its relocated matrix entry.

Consequently this construction does not yield an additional receiver signal, distinguish the two implementations at R, or justify bath access. It cannot be advertised as an operational separation for the original owner. Nor does it exclude a conserving realization using a different bath, preparation, ancillary resource or charge assignment; those are different comparison classes and have not been classified.

## 6. What this changes, and the stopping boundary

PR149 at `45914f4c28432332a2146ae4df3bb89cb2e57db7` proves statistical sufficiency and supplies a mixed-bath example with a conserving realization of the very same complete prepared channel. The response in PR111 comment `6856050317` correctly notes that this does not establish an enlarged class of prepared channels.

The present explicit qutrit construction settles that remaining implication for fixed resources: the class of complete prepared channels admitting full endpoint-statistics preservation can be strictly larger than the class admitting a globally K-commuting unitary realization. Globally commuting realizations always preserve endpoint statistics, while this example belongs only to the larger class. It retains exact C, the no-unit-gap condition and the same receiver response, so it is within the benchmark rather than an unrelated statistical example.

This strictness is at the complete S,E,R level. The same example supplies no strictness after tracing E. It is conditional mathematical progress in distinguishing proposed physical restrictions, with **no native premise removed**. It does not establish a universally weakest assumption, the necessity of coherence for every possible separation, a full realization classification, or new physics.

The bounded question is complete once the argument is independently reviewed and its evidence published. Do not continue with a parameter sweep, an equivalent-writer catalogue, or another review of unchanged predecessors. A next native claim still needs a justified inherited operation with an independently identified retained owner and an available source-dependent consequence. The physical charge and operational correspondence remain NEW/SUPPLIED.
