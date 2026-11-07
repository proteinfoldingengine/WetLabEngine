# One fixed effect across all source-channel realizations

Status: frozen author analytical argument for independent review. Native delivery NOT_DERIVED.
Source parent: 31f5c7f5f7d1153c3fce21d9cbd8f39070f68540.
Origin: T-371-work, PR111 comment 6709805291. This manuscript restates its proof with explicit compactness and scope; no discovery is retrospectively preregistered.

## 1. Supplied benchmark and question

Use the finite complex source Hilbert space H_S=C^4 with basis (o,p,u,v), Q=I-|u><u|, and C(rho)=Q rho Q+rho_uu |p><p|. The normalized source pair is rho_+=diag(1,1,2,1)/5 and rho_-=diag(1,1,1,2)/5. The carrier, diagonal encoding, channel's physical interpretation and preparations remain SUPPLIED benchmark hypotheses.

Let K=K_A tensor K_B be a fixed finite complex environment admitting a dilation of C. Let W(C,K) be ALL isometries W:H_S -> H_S tensor K implementing C on every source matrix. RD-0 in the source packet proves this is a single orbit W_U=(I_S tensor U)W_0 under U(K). No extra constraint reduces this orbit. The actual event's occurrence is ACCEPTED INPUT, but its identification with C or a particular W is not derived.

Fix a unital *-subalgebra A_S of B(H_S), and the same product interface
    A=A_S tensor B(K_A) tensor I_(K_B)
for every W. K_B is allowed to be one-dimensional. This is a SUPPLIED access class, not a native ownership theorem. Write Eff(A)={F in A: 0<=F<=I}; similarly Eff(A_S). Effects are chosen independently of the realized W and the source hypothesis.

Define Delta=rho_+-rho_-, D_W=W Delta W†, and
    d_S=max_(E in Eff(A_S)) Tr[E C(Delta)].
All quantities below are real. The zero effect and complement I-E are allowed, so d_S>=0. All effect sets and the unitary orbit are compact; the displayed maxima/minima exist.

The question is one fixed binary effect, not a realization-dependent choice of optimal readout:
    V_signed=max_(F in Eff(A)) min_(W in W(C,K)) Tr(F D_W),
    V_abs=max_(F in Eff(A)) min_(W in W(C,K)) |Tr(F D_W)|.

## 2. Claim 1: exact signed guarantee

    V_signed = d_S.

Lower bound. For any E in Eff(A_S), F=E tensor I_K lies in Eff(A). The defining reduced-channel identity gives Tr(F D_W)=Tr[E C(Delta)] for every W. A maximizing E attains d_S.

Upper bound. Fix F. Average conjugation over normalized Haar measure on the finite-dimensional compact unitary group U(K):
    integral (I tensor U†) F (I tensor U) dU = E_bar tensor I_K,
    E_bar=Tr_K(F)/dim K.
This is the ordinary matrix twirl identity, not a physical randomization assumption. One derivation expands F in source/environment matrix units: the environment average commutes with every unitary, hence is scalar, and trace preservation fixes the scalar to its normalized trace. Equivalently the generalized-Pauli finite unitary average gives the same operator.

Because F belongs to the stated product interface, E_bar belongs to A_S. Normalized partial trace is positive and unital, hence 0<=E_bar<=I. Therefore
    min_U Tr(F D_WU)
       <= integral Tr(F D_WU) dU
        = Tr[E_bar C(Delta)] <= d_S.
Maximizing F proves the upper bound.

No minimax interchange is assumed. Both inequalities are proved separately.

## 3. Claim 2: exact unsigned single-effect guarantee

    V_abs = d_S.

For fixed F set g(U)=Tr(F D_WU). This is continuous on connected compact U(K). If it vanishes somewhere, min_U |g(U)|=0<=d_S. Otherwise g has constant sign on the connected group. If positive, Claim 1's fixed-effect upper bound gives min |g|=min g<=d_S. If negative, replace F by I-F, which remains in Eff(A); since Tr D_W=Tr Delta=0, its contrast is -g and the same bound applies. The source-side maximizing E used in Claim 1 has constant nonnegative contrast d_S and attains it also in absolute value. This includes the degenerate case d_S=0.

The min of these uniformly continuous functions depends continuously on F on the compact effect set, justifying the maxima. The connectedness step is essential for the unsigned argument: a disconnected restricted realization set need not satisfy the sign argument. Such a restriction is outside the stated full-orbit class.

## 4. Comparison with the existing theorem

RD-2/RD-4 concern
    V_adaptive=min_W max_F Tr(F D_W),
which allows a different distinguishing effect for each W. Their OA* OR OC condition is not contradicted or amended here. OA* is d_S>0; OC grants the complete complement with a positive optimized contrast.

In the present product-interface/full-orbit class, a positive single-fixed-effect guarantee is equivalent to OA* alone, because Claims 1 and 2 equal d_S. This is a conditional interface criterion, not a universally minimal physical axiom.

For A_S=C I_S and full K access, the canonical pair has d_S=0. RD-0 gives
    Tr_S D_W=(|e_u><e_u|-|e_0><e_0|)/5,
with e_0 orthogonal to e_u. Thus the complete complement has trace-distance contrast 1/5 for every W: V_adaptive=1/5. But V_signed=V_abs=0. Swapping e_0,e_u reverses any fixed effect's contrast; a continuous unitary path between the original and swapped realization passes through zero while orthogonality and trace-distance contrast stay unchanged. This is blindness of that fixed effect, not equality of the complete output states.

If A_S=alg{pi_p}, pi_p=|p><p|, then Tr[pi_p C(Delta)]=1/5 and C(Delta)=(pi_p-pi_v)/5. Effects in that algebra have form alpha pi_p+beta(I-pi_p), 0<=alpha,beta<=1, so d_S=1/5, attained by pi_p before W is selected. The pi_p pre-event contrast is zero.

## 5. Physical scope and explicit nonclaims

A fixed effect's change is weaker than an initially blind complete receiver becoming informed. The full source already distinguishes this pair with trace distance 1/5 before the event. A whole-interface acquisition claim therefore still needs E6 (initial complete-interface blindness); the theorems here concern output contrast, not automatic acquisition or event-induced change in every interface.

The theorem does not rule out a fixed informationally complete multi-outcome POVM distinguishing all distinct complementary states, calibrated procedures, multiple effects with a realization-dependent useful component, or a covariant effect selected by an independently derived native operation. One binary-effect expectation is the specified contract. No new detector or measurement implementation is proposed.

The full unitary orbit, product interface, quantum encoding, actual-channel correspondence, preparations, and physical availability of effects remain supplied. The native P1 pushforward and formal owner coordinate do not by themselves imply any of these access identifications. No source-backed native producer has been obtained. No gravity, physical time, force, empirical prediction or native-delivery certification follows.

This is supporting conditional mathematics sharpening a quantifier distinction in an existing benchmark. Its general inequalities rest on the analytical proof, not finite enumeration. It is not a new channel or a new representation.

## 6. Review challenges

Check every quantifier and the compactness/connectedness steps. Attack the claim E_bar in A_S, including noncommutative A_S, proper K_A, trivial K_B and d_S=0. Check that the signed result uses no invalid minimax exchange and that absolute-value positivity cannot hide a sign change. Check the exact 1/5 benchmark and the full-complement distinction. Determine whether the mathematical assumptions suffice, whether claims exceed the sources, and whether the one-effect limitation is consistently respected. Any REVISE/FAIL must be preserved and addressed; earlier peer agreement is not proof.
