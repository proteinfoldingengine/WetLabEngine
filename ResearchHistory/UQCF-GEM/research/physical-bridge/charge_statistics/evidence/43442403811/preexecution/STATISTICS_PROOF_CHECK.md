# Fixed-preparation charge statistics: direct proof and scope check

**Status: analytical check of a NEW-assumption diagnostic. Native bridge NOT_DERIVED.**

This note checks the proposed replacement of actual global unitary commutation by conservation of the outcome distribution of the same additive charge, at the fixed product preparation. It uses only finite-dimensional linear algebra. No numerical/scientific execution, new API/model call, GitHub write, native census, or literature/novelty claim is part of this check.

Inspected local inputs:

- `charge_selection_work/package/ResearchHistory/UQCF-GEM/research/physical-bridge/charge_selection/ARGUMENT.md` (PR147).
- `prepared_charge_work/package/ResearchHistory/UQCF-GEM/research/physical-bridge/prepared_charge_domain/ARGUMENT.md` (PR148).

## 1. Fixed objects and exact statements

The source basis is `(o,p,u,v)`, with `pi_j=|j><j|` and `Q=I_S-pi_u`. The required reduced source channel is

\[
C(\rho)=Q\rho Q+\rho_{uu}\pi_p
\]

for **every source density matrix**, including coherent inputs. E is finite dimensional, `tau` is any fixed density matrix on E, R is the same initially blank qubit, and `F_R=pi_1,R` is the same fixed receiver effect. There is a single source-independent unitary U on S tensor E tensor R. Write

\[
\begin{aligned}
T_\tau(\rho)&=U(\rho\otimes\tau\otimes\pi_{0,R})U^\dagger,\\
J&=I_{SE}\otimes F_R,\\
q(\rho)&=\operatorname{Tr}[J T_\tau(\rho)],\\
K&=\pi_u\otimes I_E\otimes I_R
  +I_S\otimes Q_E\otimes I_R
  +I_{SE}\otimes F_R.
\end{aligned}
\]

Set `Lambda=spec(Q_E)` and assume

\[
\Lambda\cap(\Lambda+1)=\varnothing.
\tag{G}
\]

For a set B of real outcomes, let `P_B(K)` be its spectral projector and define the initial and final probabilities

\[
\begin{aligned}
p_{\mathrm{in}}(B\mid\rho)
 &=\operatorname{Tr}[P_B(K)(\rho\otimes\tau\otimes\pi_{0,R})],\\
p_{\mathrm{out}}(B\mid\rho)
 &=\operatorname{Tr}[P_B(K)T_\tau(\rho)].
\end{aligned}
\]

Full-distribution conservation for an input means equality of these probabilities for every B, equivalently for every individual eigenvalue of the finite observable K. It refers to separate initial and final K distributions. No two-time projective-measurement protocol, measurement back-action, or joint input/output distribution is being assumed.

The two source states and their difference remain

\[
\rho^{(0)}=\operatorname{diag}(1,1,2,1)/5,
\quad
\rho^{(1)}=\operatorname{diag}(1,1,1,2)/5,
\quad
\rho^{(0)}-\rho^{(1)}=(\pi_u-\pi_v)/5.
\]

The target effect law is `q(rho)=rho_uu`; its signed contrast is `Delta=1/5`.

## 2. Spectral event: what is true globally and on the two relevant supports

Choose the single coarse event

\[
\Gamma=\Lambda+1,\qquad P=P_\Gamma(K).
\]

The source/receiver charge is 0 on `Q tensor |0_R>`, 1 on `pi_u tensor |0_R>` and `Q tensor |1_R>`, and 2 on `pi_u tensor |1_R>`. The corresponding bath-shifted charge spectra are Lambda, Lambda+1, and Lambda+2.

Condition (G) says that Gamma is disjoint from Lambda. It also says Gamma is disjoint from Lambda+2: an equality `lambda+1=mu+2` would imply `lambda=mu+1`, contradicting (G). **There is no requirement that Lambda and Lambda+2 be disjoint.** They may overlap; for example, Lambda can be `{0,2}`.

Consequently the exact global projector is

\[
\boxed{
P=\pi_u\otimes I_E\otimes\pi_{0,R}
   +Q\otimes I_E\otimes\pi_{1,R}.
}
\tag{1}
\]

This is the sum of two orthogonal source/receiver blocks. It is **not** globally `pi_u tensor I_ER`, and it is **not** globally J. In particular its value on the source-u/receiver-one block is zero, whereas J has value one there. No factorization of individual K eigenspaces, or separation of Lambda from Lambda+2, is needed.

Let `B_0=I_SE tensor pi_0,R` project onto the initially blank-R subspace, and let `O=Q tensor I_ER` project onto the possible output source subspace. Equation (1) gives the two distinct restriction identities

\[
B_0PB_0=\pi_u\otimes I_E\otimes\pi_{0,R},
\qquad
OPO=Q\otimes I_E\otimes\pi_{1,R}=OJO.
\tag{2}
\]

These support-specific identities are the entire spectral selection step. In particular, the coarse event does not require tau to commute with Q_E or to have Q_E-invariant support.

## 3. Why exact C puts the complete positive output in Q

For every source density matrix rho,

\[
\operatorname{Tr}[(\pi_u\otimes I_{ER})T_\tau(\rho)]
=\operatorname{Tr}[\pi_u C(\rho)]=0.
\]

For any positive operator X and orthogonal projection A, `Tr(AX)=0` implies `AX=XA=0`. Indeed,

\[
0=\operatorname{Tr}(X^{1/2}AX^{1/2})
  =\lVert AX^{1/2}\rVert_{\mathrm{HS}}^2,
\]

so `AX^(1/2)=0`, and the claimed support statement follows. Applying this to the joint output shows

\[
T_\tau(\rho)=O T_\tau(\rho) O.
\tag{3}
\]

The conclusion concerns the **complete** joint output, including its off-diagonal blocks. It would be invalid to infer it from a zero signed contribution without positivity; here the state is positive and the traced quantity is a projection probability.

For later basis arguments, diagonalize the actual preparation as

\[
\tau=\sum_{i=1}^{k}t_i|e_i\rangle\langle e_i|,
\qquad t_i>0.
\]

The vectors e_i need not be charge eigenvectors. Exact C maps each retained basis input pi_a, `a in {o,p,v}`, to the pure source state pi_a, and maps pi_u to pi_p. Positivity of each occupied summand therefore gives

\[
\begin{aligned}
U|a,e_i,0_R\rangle&=|a\rangle\otimes|\eta_{a,i}\rangle_{ER}
&& (a=o,p,v),\\
U|u,e_i,0_R\rangle&=|p\rangle\otimes|\zeta_i\rangle_{ER}.
\end{aligned}
\tag{4}
\]

All these ancillary vectors have norm one. Thus mixed or coherent tau causes no cancellation loophole in the support arguments.

## 4. Exact equivalence of the one-event law and the existing effect law

On the initial state, the first identity in (2) gives

\[
p_{\mathrm{in}}(\Gamma\mid\rho)=\rho_{uu}.
\tag{5}
\]

On the output, (2) and (3) give

\[
p_{\mathrm{out}}(\Gamma\mid\rho)=q(\rho).
\tag{6}
\]

Hence, **for each individual source input rho**,

\[
\boxed{
p_{\mathrm{out}}(\Gamma\mid\rho)
=p_{\mathrm{in}}(\Gamma\mid\rho)
\quad\Longleftrightarrow\quad
q(\rho)=\rho_{uu}.
}
\tag{7}
\]

In particular, conservation of this single coarse-event probability for every source rho is **equivalent**, under the fixed benchmark and (G), to the sharp-writer effect law. It is not an independent mechanism that explains that law from less specific physical information. Full-distribution conservation is stronger and is a sufficient premise because it includes this event.

For clarity about mixed preparations, the source effect is

\[
M=T_\tau^*(J),\qquad 0\leq M\leq I_S,
\qquad q(\rho)=\operatorname{Tr}(M\rho).
\tag{8}
\]

Thus the all-input conclusion is exactly `M=pi_u`. If tau is purified into a passive reference Z and `V_tau:S -> S tensor E tensor R tensor Z` is the resulting input isometry, it reads

\[
V_\tau^\dagger(J\otimes I_Z)V_\tau=\pi_u.
\]

Since J is a projection, this is equivalent to

\[
(J\otimes I_Z)V_\tau=V_\tau\pi_u.
\]

For example, the first equation makes the squared norm of `(J tensor I_Z)V_tau Q` zero and the squared norm of `(I-J tensor I_Z)V_tau pi_u` zero, proving the second equation. This is a precise mixed-state formulation of the already existing sharp-writer identity. It does not identify a new native operation.

The effect law does not specify the whole receiver density matrix for a general coherent source input. In particular, source p/u coherence can contribute receiver off-diagonal terms.

## 5. Basis distribution checks suffice: positivity closes the coherence gap

Assume full K-distribution conservation for the four source basis inputs pi_o, pi_p, pi_u, pi_v, always with the same fixed tau and blank R. In fact only their Gamma-event equalities are needed for this step. Equations (5)-(6) imply

\[
M_{oo}=M_{pp}=M_{vv}=0,\qquad M_{uu}=1.
\]

Every positive matrix satisfies `|M_ab|^2 <= M_aa M_bb`. All off-diagonal entries therefore vanish because every off-diagonal pair contains at least one retained index with zero diagonal. Hence

\[
M=\pi_u,\qquad q(\rho)=\rho_{uu}\quad\hbox{for all source rho}.
\tag{9}
\]

This is an endpoint-positivity argument. An arbitrary Hermitian operator identity cannot normally be inferred from agreement on basis populations alone. Here the 0/1 values and `0<=M<=I` make that inference valid. No charge diagonality of tau is used.

Full-distribution conservation for **all** source states trivially implies the four basis checks. Under the present exact-source/no-gap hypotheses, the converse also holds, although it is not needed for the target effect theorem:

1. The coarse part of the basis checks has just forced (9).
2. Combining the saturated receiver probabilities with (4) shows, for each occupied i, that the output from a retained a lies in `|a> tensor E tensor |0_R>`, whereas the output from u lies in `|p> tensor E tensor |1_R>`.
3. Each spectral projector of K preserves every fixed source-label/receiver-bit block. These four distinct output blocks have zero off-diagonal matrix elements for every spectral projector of K.
4. Consequently the final K distribution depends only on the source input's diagonal entries. The initial K distribution also depends only on those entries. Equality for the four basis inputs extends by linearity to every source rho.

Explicitly, write the occupied output vectors as xi_s,i. For distinct source labels s,t and any eigenvalue kappa,

\[
\operatorname{Tr}\!\left[P_{\{\kappa\}}(K)
 U(|s\rangle\langle t|\otimes\tau\otimes\pi_{0,R})U^\dagger\right]
=\sum_i t_i\langle\xi_{t,i}|P_{\{\kappa\}}(K)|\xi_{s,i}\rangle
=0.
\]

This establishes the stated extension without mistakenly treating a difference of two general effects as positive.

## 6. The unchanged source-pair contrast requires only u and v

For the requested fixed contrast, the direct proof is shorter. Conservation of the Gamma event on pi_u and pi_v gives

\[
q(\pi_u)=1,\qquad q(\pi_v)=0.
\]

Linearity and the fixed source difference then give

\[
\boxed{
\Delta=q(\rho^{(0)})-q(\rho^{(1)})
=\frac{q(\pi_u)-q(\pi_v)}5=\frac15.
}
\tag{10}
\]

Thus full-distribution checks on u and v are sufficient for the fixed contrast; their single coarse-event checks already suffice. No o or p distribution check enters (10), and no new receiver, effect, source pair, or bath preparation is introduced.

### Optional stronger consequence of the exact all-input source channel

The supplied **all-input** C actually makes the two selected basis checks stronger than needed just for the contrast. This is separate from the short proof above and should not be confused with a general claim about arbitrary channels.

Exact preservation of a retained matrix unit `|a><b|` in (4) gives

\[
\sum_i t_i\langle\eta_{b,i}|\eta_{a,i}\rangle=1.
\]

Consequently

\[
\sum_i t_i\lVert\eta_{a,i}-\eta_{b,i}\rVert^2=0,
\]

so `eta_a,i=eta_b,i` for every occupied i and every retained a,b. The complete ancillary output is therefore the same on all retained source basis inputs. This is the elementary no-information-without-disturbance consequence of exact identity on the retained subspace.

In particular, `q(pi_o)=q(pi_p)=q(pi_v)`. The two Gamma checks on u and v therefore imply all four effect diagonals and hence (9). Likewise, if the full K distributions are conserved on u and v, all retained basis distributions equal the v distribution: the source charge is zero for each retained label and their ancillary output states are common. The all-input distribution extension in section 5 then applies.

Under the entire fixed benchmark and (G), one may therefore record the exact implications

\[
\begin{aligned}
\text{full distributions for all source rho}
&\Longleftrightarrow\text{full distributions for all four basis inputs}\\
&\Longleftrightarrow\text{full distributions for u and v},\\[2mm]
\text{Gamma-event conservation for all source rho}
&\Longleftrightarrow\text{Gamma-event conservation for all four basis inputs}\\
&\Longleftrightarrow\text{Gamma-event conservation for u and v}\\
&\Longleftrightarrow M=\pi_u.
\end{aligned}
\tag{11}
\]

The first line of (11) implies the second group. The reverse implication is false in general, as shown next. No claim is made that two checks are a necessary or universally minimal empirical verification scheme.

## 7. Strictness and non-equivalence controls

Let W_R be the standard global writer from PR147, acting trivially on E and swapping `|u,0_R>` with `|p,1_R>` while fixing the other source/receiver basis states. It implements C exactly for every tau and commutes with the present additive K for every Q_E.

### 7.1 The effect/event law does not imply full-distribution conservation

Take a two-dimensional bath with orthonormal charge eigenvectors e_0,e_2,

\[
Q_E=0|e_0\rangle\langle e_0|+2|e_2\rangle\langle e_2|,
\quad\tau=|e_0\rangle\langle e_0|.
\]

Let X_E swap e_0 and e_2 and define `U=X_E W_R` with identities implicit. The spectrum `{0,2}` satisfies (G). Applying a bath-only unitary after W_R changes neither the exact reduced source channel nor the receiver effect, so `q(rho)=rho_uu` for every rho. The Gamma event is therefore conserved for every rho.

Nevertheless, source v has initial total charge 0 with probability one and final total charge 2 with probability one. Source u similarly changes from charge 1 to charge 3. Full-distribution conservation fails. This proves that, in the admitted benchmark class, full-distribution conservation is a **strictly stronger sufficient condition** than the single-event/effect law.

The example deliberately has `Lambda intersect (Lambda+2)={2}`. It also confirms that this overlap does not spoil the coarse-event proof.

### 7.2 Full-distribution conservation at fixed tau does not imply actual global commutation

Keep the same bath, charge, X_E, W_R, and `U=X_E W_R`, but now choose the full-rank state `tau=I_E/2`. Since `X_E tau X_E^dagger=tau` and W_R acts trivially on E, every prepared output density matrix equals the output density matrix of W_R alone. Thus U implements C and conserves the full K distribution for every source rho at the specified tau.

The actual U nevertheless changes the charge of the joint vector `|v,e_0,0_R>`:

\[
U|v,e_0,0_R\rangle=|v,e_2,0_R\rangle,
\qquad
(KU-UK)|v,e_0,0_R\rangle=2|v,e_2,0_R\rangle\ne0.
\]

Therefore `[U,K] != 0`. The discrepancy occurs on the occupied support, not merely on an unused receiver-one subspace. Here `supp(tau)=E` is charge-invariant, so the same example also violates the prepared-vector condition and PR148's charge-generated-domain condition for the actual U.

This is possible because the new premise fixes the **mixed preparation tau**. Varying rho does not allow arbitrary independent bath inputs or resolve the charge permutation of its occupied components. The prepared joint output densities happen to have the commuting realization W_R, but that does not make the specified U commute or satisfy a vector intertwining condition. No general claim about existence or nonexistence of other commuting completions is needed.

Actual global commutation is sufficient: it gives `U^dagger P_B(K)U=P_B(K)` for every B and therefore conserves the distribution for every joint input state. The converse above fails because the proposed premise tests only `rho tensor tau tensor pi_0,R`.

### 7.3 Relation to PR148's failed prepared-vector weakening

PR148's explicit blind example has `Lambda={0,2,4,6}`. For source u its input distribution is on `{1,5}` and its output distribution is on `{2,6}`. With `Gamma={1,3,5,7}`, the input coarse-event probability is one and the output probability is zero. It therefore fails the present statistical condition immediately, despite satisfying `(KU-UK)P_L=0`.

Together with section 7.2, this shows that conservation of all prepared-source charge distributions and the bare prepared-input vector condition are **incomparable** in this benchmark class. The former is not a reformulation of the latter.

PR148's stronger condition on its K-invariant charge-generated space remains sufficient for the distribution law: its commuting completion agrees with U on every actually occupied input vector, so it preserves their complete output densities and their K distributions. That implication is a consequence of the already proved completion lemma, not a new mechanism.

## 8. What is sufficient, what is equivalent, and what is still supplied

| Statement or proposed inference | Checked status under exact C, fixed product preparation, and (G) |
|---|---|
| Global `[U,K]=0` implies fixed-preparation full-distribution conservation | Sufficient; not equivalent for the actual U |
| PR148's charge-generated-domain vector law implies fixed-preparation full-distribution conservation | Sufficient, by its commuting completion |
| Bare prepared-input vector law implies distribution conservation | False; PR148's blind example refutes it |
| Distribution conservation implies the bare prepared-input vector law | False; section 7.2 refutes it even with full-rank tau |
| Full-distribution conservation implies `q(rho)=rho_uu` | Sufficient; strictly stronger than the effect law |
| Conservation of the single event `Gamma=Lambda+1` for every rho | Exactly equivalent to the sharp-writer effect law |
| Four source-basis event checks imply the all-input effect law | Valid by positivity and endpoint probabilities |
| u/v event checks imply the requested fixed contrast | Valid directly by linearity |
| u/v checks imply the corresponding all-input law | Also valid here, using exact coherence preservation on the retained subspace; not a general basis-testing principle |

The quantum factorization, normalized encoding, exact all-input C, independent product preparation, one chosen U, initially blank same qubit R, and same owned accessible effect F_R remain **SUPPLIED**. The source charge pi_u, physical bath charge Q_E, receiver-charge/effect identification, additive K, spectral exclusion (G), and whichever statistical conservation premise is asserted remain **NEW**. Treating a distribution law as testable would additionally require the relevant preparation and measurement access; this note does not derive or assert that access.

The direct one-event identity exposes the evidentiary limit. Full-distribution conservation supplies a sufficient physical restriction. Its useful selected-event content is already the writer effect identity on the admitted input/output supports. It must not be presented as native derivation, a new delivery mechanism, a weakest physical axiom, a new conservation theorem, empirical evidence, or an archive-wide novelty result.

The candidate is a bounded diagnostic of a different stated conservation premise. It neither revises PR147's globally conserving theorem nor rescues PR148's bare prepared-vector condition. Native bridge remains **NOT_DERIVED**: no native producing event, same-owner physical action/access, detector response, physical energy identification, GR law, fundamental time, stage closure, or exhaustive native census has been established.
