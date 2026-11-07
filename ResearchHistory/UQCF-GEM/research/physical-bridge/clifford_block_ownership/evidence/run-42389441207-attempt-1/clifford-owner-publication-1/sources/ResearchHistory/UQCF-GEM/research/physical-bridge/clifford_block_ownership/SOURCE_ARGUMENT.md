# Frozen so(9) Clifford graph-action argument

Status: review candidate; no native-bridge claim.

Authoritative research source commit: \`1a18308a026c06882b428fbe201b4634c34dfd8f\`.

Thread evidence:
- T-366-dot construction: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6698688224
- T-367 Grok verification: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6699475073
- Prior scoped pair review T-366-work: https://github.com/proteinfoldingengine/WetLabEngine/pull/111#issuecomment-6698675923

## Scope and premises

1. Actual atemporal measurement/pruning occurrence is accepted empirical input. Its event/state/record correspondence is not thereby supplied.
2. The three-block real graph algebra with block-skew generators \(K_{AB}(P)\), \(K_{BC}(Q)\), and
   \[
   [K_{AB}(P),K_{BC}(Q)]=K_{AC}(PQ)
   \]
   is a supplied historical conditional interface for this comparison, not an identification with the actual P1 event.
3. The four-qubit Clifford carrier below is a supplied mathematical construction. It is not inherited from P1, and the labels \(A,B,C\) partition nine Clifford-vector indices rather than defining three physical tensor subsystems.
4. Selection of the representation or its unitary as the actual event; the state preparation; the orbit parameter; and identification or availability of an owner-held effect are not derived.
5. No copy gate, READS graph, external reader, measurement instrument, probability law, clock, or receiver query is introduced.

## Claim A: the nine displayed strings form a Clifford family

On \(\mathcal H=(\mathbb C^2)^{\otimes4}\), define
\[
(\gamma_1,\ldots,\gamma_9)
=(XIII,YIII,ZXII,ZYII,ZZXI,ZZYI,ZZZX,ZZZY,ZZZZ).
\]

Each \(\gamma_i\) is Hermitian and squares to \(I\). For \(i\ne j\), the two Jordan-Wigner strings have exactly one tensor position at which their nonidentity Pauli factors anticommute, while all other contributions commute. Therefore
\[
\{\gamma_i,\gamma_j\}=2\delta_{ij}I.
\]

This is a statement about an operator representation on one 16-dimensional carrier. It does not identify the first, second, or third three-index block with a tensor factor or a native receiver.

## Claim B: the spin generators give a Lie representation of so(9)

For \(F_{ij}=E_{ij}-E_{ji}\), define
\[
J(F_{ij})=S_{ij}:=\frac14[\gamma_i,\gamma_j].
\]
For \(i<j\), this is \(S_{ij}=\gamma_i\gamma_j/2\), with \(S_{ji}=-S_{ij}\) and \(S_{ii}=0\). Clifford multiplication gives
\[
[S_{ij},\gamma_k]
=\delta_{jk}\gamma_i-\delta_{ik}\gamma_j
\]
and
\[
[S_{ij},S_{kl}]
=\delta_{jk}S_{il}-\delta_{ik}S_{jl}
-\delta_{jl}S_{ik}+\delta_{il}S_{jk}.
\]
These are the defining brackets of \(\mathfrak{so}(9)\). Thus the linear extension
\[
J:\mathfrak{so}(9)\longrightarrow\mathfrak u(16)
\]
is a Lie-algebra homomorphism. Each \(J(X)\) is anti-Hermitian.

The claim is representation-theoretic. It supplies neither a nonzero physical coupling nor a P1 selection rule.

## Claim C: the full graph path-product bracket is represented

Partition the vector indices as
\[
A=\{1,2,3\},\qquad B=\{4,5,6\},\qquad C=\{7,8,9\}.
\]
For real \(3\times3\) matrices \(P,Q\), set
\[
K_{AB}(P)=\sum_{i,j=1}^3P_{ij}F_{i,3+j},\qquad
K_{BC}(Q)=\sum_{j,k=1}^3Q_{jk}F_{3+j,6+k}.
\]
The \(\mathfrak{so}(9)\) bracket gives
\[
[K_{AB}(P),K_{BC}(Q)]
=\sum_{i,j,k}P_{ij}Q_{jk}F_{i,6+k}
=K_{AC}(PQ).
\]
Because \(J\) is a Lie homomorphism,
\[
[J(K_{AB}(P)),J(K_{BC}(Q))]
=J(K_{AC}(PQ)).
\]

This answers the abstract existence question left open by the failure of the naive overlapping two-qubit edge lift. It does not repair that particular lift, preserve its tensor factors, or select this different representation physically.

## Claim D: the same representation has an exact admissible effect action

Let
\[
X=\sum_{i<j}x_{ij}F_{ij}\in\mathfrak{so}(9),\qquad
J(X)=\sum_{i<j}x_{ij}S_{ij},
\]
and let \(\Gamma=(\gamma_1,\ldots,\gamma_9)^T\). From Claim B,
\[
[J(X),\Gamma]=-X\Gamma.
\]
Set
\[
V_X(\lambda)=e^{\lambda J(X)}.
\]
Then \(V_X(\lambda)\) is unitary. The Schrödinger action
\[
\Phi_{X,\lambda}(\rho)=V_X(\lambda)\rho V_X(\lambda)^\dagger
\]
preserves positivity, trace, and spectrum on the complete density-matrix domain. The dual effect action is
\[
E\longmapsto V_X(\lambda)^\dagger E V_X(\lambda).
\]

Differentiating the Heisenberg Clifford vector gives
\[
\frac{d}{d\lambda}\left(V_X^\dagger\Gamma V_X\right)
=X\left(V_X^\dagger\Gamma V_X\right),
\]
and therefore
\[
V_X(\lambda)^\dagger\Gamma V_X(\lambda)
=e^{\lambda X}\Gamma.
\]

Consequently, if
\[
r(\rho)_i=\operatorname{Tr}(\rho\gamma_i),
\]
then
\[
r(\Phi_{X,\lambda}(\rho))=e^{\lambda X}r(\rho).
\]
Thus the real graph action is realized exactly on this nine-dimensional family of operator expectations, not on marginal Bloch vectors. For any real unit vector \(u\), \((u\cdot\Gamma)^2=I\), so
\[
E_u=\frac{I+u\cdot\Gamma}{2}
\]
is a projection and its conjugate remains a valid effect.

This is a positive observable-action statement internal to the supplied Clifford carrier. A Clifford effect is not thereby a native receiver, an available owner effect, or the physical record of P1.

## Strongest justified conclusion

- Necessary mathematics: a graph-compatible, positivity-preserving quantum action exists for the full three-block conditional graph algebra. Unlike the rejected direct marginal interpretation, it realizes the real orthogonal action exactly on a Clifford-vector effect/expectation family.
- Physical identification: not earned. No inherited source binds the four-qubit carrier, \(J\), \(X\), \(\lambda\), a Clifford effect, or any block label to the actual P1 occurrence or its provenance-bound retained owner.
- Verification before this review: Grok reported analytical matches for the 81 Clifford identities, the 1296 basis commutators, and the path-product bracket in T-367. That is independent algebraic verification, not this whole-argument Gemini review.
- Native delivery remains \`NOT_DERIVED\`.

The first unsupported correspondence remains
\[
\text{actual P1 event}
\longrightarrow
\text{native selection of this or another admissible source-sensitive action}
\longrightarrow
\text{the same provenance-bound receiver's available effect contrast}.
\]

## Review questions

1. Reconstruct Claims A-D and check every coefficient, sign, transpose, factor of \(1/2\), and quantifier.
2. Check the nine Pauli strings really satisfy the Clifford relations on the stated carrier.
3. Check that \(J\) is a Lie homomorphism with the displayed conventions and that the graph bracket is \(PQ\) with no missing sign or transpose.
4. Check the exact Heisenberg identity and the induced expectation-vector transformation.
5. Check that \(E_u\) is a valid projection for unit \(u\).
6. Challenge whether the index partition silently supplies tensor subsystems, owner identity, effect availability, preparation, or event selection.
7. Separate conditional mathematics from physical identification and native acquisition.
8. Preserve all adverse evidence. Do not invent a mechanism, receiver, tensor factor, clock, probability law, or universal occurrence theorem.

A valid review may accept the scoped mathematics while retaining native delivery as \`NOT_DERIVED\`.
