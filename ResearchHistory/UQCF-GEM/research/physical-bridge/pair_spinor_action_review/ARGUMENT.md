# Frozen pair-spinor action and graph-obstruction argument

Status: review candidate; no native-bridge claim.

Source commit: `1a18308a026c06882b428fbe201b4634c34dfd8f`.

Thread evidence:
- T-363-work: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6697680165
- T-364-dot: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6698008056
- T-365 Grok verification: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6698192101

## Scope and premises

1. Actual atemporal measurement/pruning occurrence is accepted empirical input.
2. The active joint sector, protected grading, and carrier (P=gnt) are supplied historical architecture. A nonzero coupling is not derived here.
3. The real-vector operation
   [
   K(P)=\begin{pmatrix}0&P\\-P^T&0\end{pmatrix}
   ]
   and the graph relation
   [
   [K_{AB}(P),K_{BC}(Q)]=K_{AC}(PQ)
   ]
   are conditional source constructions, not identifications with the actual P1 event.
4. The Pauli-bilinear (H(P)=\sum_{ij}P_{ij}\sigma_i\otimes\sigma_j) is an already declared historical operation. Selecting its unitary as the actual event, identifying either tensor factor with the native retained owner, choosing its orbit parameter, and supplying preparations are not derived here.
5. No tensor split, copy gate, READS graph, instrument, reader, probability law, or owner query is introduced.

## Claim A: the direct marginal-vector reading is not a state action

Take
[
\rho_{CS}=\operatorname{diag}(33,3,3,1)/40.
]
Both marginal Bloch vectors are (c=s=(4/5)e_z). The connected (zz) correlation is
[
\langle Z_CZ_S\rangle-\langle Z_C\rangle\langle Z_S\rangle
=7/10-16/25=3/50.
]
Choose (t=e_ze_z^T), (n=1), (g=1/2), hence (P=(1/2)e_ze_z^T). At orbit parameter (lambda=\pi/2), the corresponding (z)-plane rotation angle is (	heta=\pi/4), so
[
c'_z=\cos\theta,c_z+\sin\theta,s_z=4\sqrt2/5,qquad s'_z=0.
]
The putative receiver marginal
[
\rho'_C=(I+c'_zZ)/2
]
has eigenvalue ((1-4\sqrt2/5)/2<0). Therefore (e^{\lambda K(P)}) cannot act on the entire two-qubit state domain by directly treating its two real endpoint vectors as the two marginal Bloch vectors. This does not refute the abstract orthogonal action or a differently represented/restricted action.

## Claim B: an isolated-pair admissible quantum lift exists

For (L(a)v=a\times v), write
[
X=\begin{pmatrix}L(a)&P\\-P^T&L(b)\end{pmatrix}.
]
Define
[
J(X)=-\frac{i}{2}\left[
(a\cdot\sigma)\otimes I+I\otimes(b\cdot\sigma)+H(P)
\right].
]
Let
[
A_i=-i\sigma_i\otimes I/2,quad
B_j=-iI\otimes\sigma_j/2,quad
T_{ij}=-i\sigma_i\otimes\sigma_j/2.
]
Pauli multiplication yields
[
[A_i,A_k]=\epsilon_{ikm}A_m,quad
[B_j,B_l]=\epsilon_{jln}B_n,quad [A_i,B_j]=0,
]
[
[A_i,T_{kl}]=\epsilon_{ikm}T_{ml},qquad
[B_j,T_{kl}]=\epsilon_{jln}T_{kn},
]
[
[T_{ij},T_{kl}]
=\delta_{jl}\epsilon_{ikm}A_m+\delta_{ik}\epsilon_{jln}B_n.
]
These are the brackets of the corresponding block-skew matrices. Hence
[
J([X,Y])=[J(X),J(Y)].
]
The 15 independent generators span (mathfrak{su}(4)), giving the spinor realization of (mathfrak{so}(6)).

Consequently
[
V_P(\lambda)=\exp[-i\lambda H(P)/2],qquad
\Phi_{P,\lambda}(\rho)=V_P(\lambda)\rho V_P(\lambda)^\dagger
]
preserves positivity, trace, and spectrum on the complete two-qubit state domain. Effects transform as (E\mapsto V_P^\dagger E V_P).

This does not implement (e^{\lambda K(P)}) on the pair of marginal Bloch vectors. In Claim A's diagonal example with (P=(1/2)E_{zz}), the generator is proportional to (ZZ) and the unitary leaves the diagonal state unchanged. The two representations must not be conflated.

## Claim C: the obvious edgewise graph extension fails exactly

Try the same pair lift on overlapping edges of (A\otimes B\otimes C). Choose nonzero (p,q), (P=pE_{zz}), and (Q=qE_{zz}). The edge generators are
[
J_{AB}(P)=-ipZ_AZ_B/2,qquad
J_{BC}(Q)=-iqZ_BZ_C/2.
]
They commute:
[
[J_{AB}(P),J_{BC}(Q)]=0.
]
But the conditional real-vector graph algebra requires
[
[K_{AB}(P),K_{BC}(Q)]=pqK_{AC}(E_{zz}),
]
whose proposed pairwise spinor image is
[
-ipqZ_AI_BZ_C/2\ne0.
]
Therefore the naive overlapping-edge use of the isolated-pair lift is not a representation of that graph bracket. Edgewise sign choices cannot repair zero versus nonzero. This rejects only the obvious edgewise extension, not every possible graph-compatible quantum representation and not every one-event solution.

## Strongest justified conclusion

- Necessary mathematics: the direct marginal-vector identification fails on a valid full-rank input; a positivity-preserving isolated-pair spinor lift exists; its naive overlapping-edge extension fails the inherited graph composition identity.
- Physical identification: not earned. No source binds the lift, its factor, parameter, or effect to the actual provenance-bound P1 receiver.
- Verification: Grok reported a Class-D match for the arithmetic, pair brackets, and graph obstruction in T-365. That is independent algebraic verification, not a whole-argument external review.
- Native delivery remains `NOT_DERIVED`.

The first unsupported correspondence remains:
[
\text{actual P1 event}
\longrightarrow
\text{native selection of an admissible source-sensitive state/effect action}
\longrightarrow
\text{the same provenance-bound receiver's available effect contrast}.
]

## Review questions

1. Reconstruct Claims A-C and check every coefficient, sign, bracket, and quantifier.
2. Challenge whether (J) as written is a Lie-algebra homomorphism with the displayed conventions.
3. Challenge the zero-versus-nonzero graph counterexample and identify any silent embedding ambiguity.
4. State whether Claim A actually refutes only the direct marginal-vector interpretation.
5. Separate conditional mathematics from physical identification and native acquisition.
6. Preserve any adverse evidence. Do not invent a mechanism, receiver, tensor factor, clock, or probability law.

A valid review may accept the scoped mathematics while retaining native delivery as `NOT_DERIVED`.
