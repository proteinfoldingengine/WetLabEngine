# Independent analytical check

**Verdict: accepted, with the fixed-resource and full-output qualifications below.** No algebraic flaw or additional hypothesis was found. This check uses finite-dimensional analytical arguments only; no scientific code, simulation, external-model call, or GitHub write was used. Native bridge **NOT_DERIVED**; the Hilbert benchmark is supplied. No novelty or new numbered-stage claim is supported.

## All-input channel and receiver

Let `T:S -> S tensor R` be the isometry

\[
 T|j\rangle=|j,0\rangle\quad(j=o,p,v),\qquad
 T|u\rangle=|p,1\rangle.
\]

The four output vectors are orthonormal, including the two outputs with source label p. Since the factors W_R and V_E act on disjoint subsystems, the prepared output of U is, up to the stated S,E,R tensor ordering,

\[
 \Phi_U(X)= (TXT^\dagger)_{SR}\otimes\tau'_E,
 \qquad
 \tau'=V_E\tau V_E^\dagger
 =\frac16\begin{pmatrix}2&0&1\\0&2&0\\1&0&2\end{pmatrix}.
\]

This holds for **every source operator X**, not only density matrices or basis populations. Tracing R preserves each retained-retained matrix unit, sends `|u><u|` to `|p><p|`, and removes every cross matrix unit involving u because its receiver labels differ. Thus the source channel is exactly `QXQ+X_uu pi_p`, and the receiver effect is exactly `q(rho)=rho_uu`. There is no missed coherent-source case.

The two bath states have the same uniform charge-basis diagonal and the same strictly positive eigenvalues `1/2, 1/3, 1/6`. The bath spectrum `{0,2,4}` satisfies the predecessor's no-unit-gap assumption.

## Endpoint statistics

The swapped W_R vectors `|u,0>` and `|p,1>` both have source-plus-receiver charge one, so `[K,W_R]=0` globally. Bath diagonals alone determine the endpoint distribution before W_R. Writing `a=Tr(Q rho)` and `b=rho_uu`, the initial and final K distributions both are

\[
 p(0)=p(2)=p(4)=a/3,\qquad
 p(1)=p(3)=p(5)=b/3,\qquad p(6)=0.
\]

This accounts for the entire global spectrum of K. Bath and source off-diagonal entries cannot enter these spectral-projector traces. Consequently the equality is valid for every original source state, including coherent states; it concerns endpoint distributions only. The specified U itself is nonconserving: `|o,e_2,0>` is sent to `|o,e_4,0>`.

## No conserving realization of the same complete prepared channel

Suppose a unitary Z on the **same S,E,R**, with the **same tau and receiver preparation**, commutes with K and reproduces the complete output channel. The o-input alone gives

\[
 Z(\pi_o\otimes\tau\otimes\pi_0)Z^\dagger
   =\pi_o\otimes\tau'\otimes\pi_0.
\]

Both sides have support

\[
 L_o=|o\rangle\otimes E\otimes|0\rangle,
\]

because tau and tau' are full rank. Unitary conjugation maps supports exactly, hence `Z L_o=L_o`. This conclusion follows from equality of mixed outputs and does **not** require identifying individual bath eigenvectors, assuming vectorwise agreement, or permitting pure bath inputs.

The subspace L_o is K-invariant and its restriction of K is exactly the nondegenerate `Q_E=diag(0,2,4)`. Therefore the restriction `D=Z|L_o` is a unitary satisfying `[D,Q_E]=0`, hence diagonal in that basis. The matching equation requires `D tau D†=tau'`, but

\[
 (D\tau D^\dagger)_{0,4}
   =d_0\tau_{0,4}\overline{d_4}=0
   \ne \tau'_{0,4}=1/6.
\]

This is the required contradiction. **Global degeneracies do not provide an escape:** although total-charge eigenspaces contain vectors outside L_o, exact output support forces Z to preserve L_o; within it every charge eigenspace is one-dimensional. Only the nondegeneracy of Q_E on L_o is used here, not any absence of global degeneracy.

## Exact scope of the separation

At these fixed dimensions, charges, preparations, and output labels, the class of complete prepared SER channels satisfying endpoint charge-statistics conservation and exact C strictly contains the subclass admitting a K-commuting unitary realization. W_R belongs to the latter class, while the displayed U supplies an element outside it. This is a channel-level separation, stronger than the predecessor's vectorwise-completion separation, and answers the stated fixed-resource existence question.

After tracing E, however,

\[
 \operatorname{Tr}_E\Phi_U(X)=TXT^\dagger
  =\operatorname{Tr}_E\Phi_{W_R}(X)
\]

for every X. Thus **the entire accessible SR channel**, including its coherences and correlations, already has the conserving realization W_R. There is no new receiver contrast, source effect, native operation, or operational SR separation. Replacing the initial bath state by tau' also makes W_R reproduce the complete output, but changes a stipulated resource. Enlarged baths, different preparations, differently identified bath outputs, other realizations with discarded environments, and a classification of all channel classes are outside the result.

Recommended wording: retain “same complete prepared SER channel with the same fixed resources” wherever asserting nonexistence or strict enlargement. Do not shorten it to an unrestricted claim that the source or SR channel has no conserving realization.
