# Fixed global quantum recovery does not bind a nominated receiver

Author: proteinfolding-gpt. Prepared 2026-11-10 UTC.
Source baseline: d373865d27052562d52a55fbe4cd18a263f00fc5.
Status: prospective complete argument for independent adversarial review. Not independently accepted.

This manuscript preserves and consolidates the claims first posted in PR111 comments 6767124759 and 6767202192, and adds the exact single-effect/domain follow-through. The original comments and their posthoc scripts/results are preserved separately. No earlier review of a different argument establishes this result.

## 1. Claim and premise ledger

The claim is a counterexample to this inference: existence of one fixed GLOBAL exact recovery channel forces a source-dependent effect at a specified proper receiver R. Two explicitly supplied isometries implement the same reduced source channel and share a single global CPTP decoder for every quantum input. The same nominated R is completely blind under one isometry and has a fixed binary effect with contrast 1/5 under the other.

This is a conditional mathematical result, not a native mechanism, a universal impossibility theorem, or evidence that a decoder is physically available. Recovering the entire source is used only as a strong diagnostic condition to falsify that inference. The user's positive target can be much weaker: one independently owned separating effect. It does not require complete source recovery, exact calibration, all old records, a unique implementation, or full-algebra access.

Premises and provenance:

1. INHERITED mathematical background: FCV PROOFS P1/P2, with finite prefix-closed carriers, nearest-retained-ancestor retraction, additive grade pushforward P, and zero extension I satisfying PI=id. On the fixed tree o→p→{u,v}, removing u gives Pz=(z_o,z_p+z_u,z_v). The mathematical receiver index is p=r(u).
2. SUPPLIED benchmark representation: H_S=C^4 with ordered basis (o,p,u,v), E and R two qubits, and a common initial auxiliary blank |0_E0_R>. A normalized nonnegative grade vector z is represented by Pi_X(z)=diag(z). This representation and its physical realization do not follow merely from P1. Grade configurations, probability laws over configurations, and diagonal density matrices remain different types.
3. SUPPLIED quantum extension of the grade update: Q=I_S−Pi_u and C(X)=QXQ+X_uu Pi_p. The domain and codomain of C are M_4; its output has no support on the u basis vector. The baseline source document is p1_receiver_location_resolution/RESULT.md §§2–5, blob 4182ba347f8c11bad63315ffa6395c496ddfa498 at the source baseline.
4. SUPPLIED source pair: rho+=(Pi_o+Pi_p+2Pi_u+Pi_v)/5 and rho−=(Pi_o+Pi_p+Pi_u+2Pi_v)/5. Their difference is Delta=(Pi_u−Pi_v)/5. Both have unit trace, and their initial p populations agree.
5. SUPPLIED fixed subsystem nomination: output order is S,E,R. R is the same physical-factor candidate in all comparisons, initially blank in both source preparations. It is not relabeled as E or as the retained source sector after looking at the result. Availability of any proposed effect or decoder is not inferred from its matrix support.
6. SUPPLIED diagnostic requirement: existence of a global CPTP recovery D whose domain is all of S,E,R and which is fixed across the two implementations. No assumption that nature implements D, or that D acts inside R, is adopted.
7. ACCEPTED INPUT: actual atemporal occurrence. Physical preparation and identification of that occurrence with this channel/isometry are distinct, still-supplied correspondences. No event inevitability, external clock, Hamiltonian, or new physical rule is introduced.

An isometry W:H_S→H_S⊗H_E⊗H_R represents the action on the common blank input subspace. Every finite-dimensional isometry has a unitary extension on the full joint space, by completing its four orthonormal columns to a basis. No particular extension outside the input subspace is chosen or claimed inherited.

## 2. General global recoverability is not a localization condition

For any isometry W and any fixed source density tau, define

  D_W(X)=W†XW+Tr[(I−WW†)X] tau.

The first term is CP. The second is CP: diagonalizing tau=Σ_k t_k|a_k><a_k| and choosing an orthonormal basis b_l of the complement of the image of W gives Kraus operators sqrt(t_k)|a_k><b_l|. The adjoint Kraus products of the two terms sum to WW†+(I−WW†)=I, so D_W is trace preserving on every joint input. Since W†W=I and (I−WW†)W=0,

  D_W(W X W†)=X

for every source operator X. The decoder may depend on W in this statement. This is an elementary isometry fact; it does not produce a physical inverse operation or specify the recovery domain as an owner's interface.

In particular it applies to the benchmark W_R and W_E and the explicit Bell representative:

  W|j>=|j>|e_0> for j=o,p,v,  W|u>=|p>|e_u>,

where the ordered environment pairs are (00,01), (00,10), and (Phi+,Phi−), respectively, with Phi±=(00±11)/sqrt(2). The pairs are orthonormal and all three implement C on every source operator. Their nominated R contrasts for Delta are respectively diag(−1/5,1/5), zero, and zero. This does not affect the separate retained-source p effect, whose contrast under C is 1/5.

## 3. One common classical decoder: the earlier bounded claim

For the existing W_R and W_E, use a single partition of the joint computational basis |j,e,r>. Assign source label u to |p,0,1> and |p,1,0>, and source label j to every other |j,e,r>. Let H_j be the projection onto the outcomes assigned to j, and set

  D_cl(X)=Σ_j Tr(H_j X) Pi_j.

The H_j form a four-outcome projective partition of the identity. Hence D_cl is CPTP, by Kraus operators |j><b| for every basis vector b assigned label j. It is the same map under W_R and W_E.

For each retained source atom j=o,p,v, either encoding gives |j,0,0>, which returns j. The u atom becomes |p,0,1> under W_R or |p,1,0> under W_E, each returning u. Thus D_cl recovers every diagonal source matrix under both implementations, by linearity. No realization label or source bit is an input to D_cl. It does not recover arbitrary source coherences; it is a measure-and-prepare channel.

The same D_cl does not recover the Bell representative's u atom: that encoding is supported on |p,0,0> and |p,1,1>, both assigned p. This is a disclosed limit, not a defect in the two-implementation claim. W_E leaves the complete R state blank for every source input, while W_R gives the known pair contrast. Thus a common global classical decoder does not force delivery to the nominated R.

## 4. The strengthened construction: one common quantum decoder

In §§4–6, P denotes the joint code projection defined below, following the original comment. It is distinct from the grade pushforward P in §§1 and 7; their domains are explicitly different.

Define two isometries, fixed before evaluating the source alternatives:

  B|j>=|j,0,0> for j=o,p,v;  B|u>=|p,1,0>.
  A|j>=|j,0,+> for j=o,p,v;  A|u>=|p,1,−>.

Here |±>=(|0>±|1>)/sqrt(2). B is the existing W_E. A is a different writer, not the old W_R. The same S,E,R factors and the same initial blank E,R are used. A's source-independent output baseline on retained j changes R from |0> to |+>; the benchmark channel contract does not forbid that. It preserves the required initial blindness of R across the two preparations.

Each isometry has four orthonormal columns. For B, the common retained environment is |00> and the u environment is |10>. For A these are |0+> and |1−>. In both cases the two environment vectors are orthogonal. Tracing E,R therefore preserves all coherences among o,p,v, erases coherences involving u, and moves its population to p. Consequently

  Tr_ER(A X A†)=C(X)=Tr_ER(B X B†)

for every source operator X.

For r=0,1 define L_r:H_SER→H_S by its only nonzero basis actions:

  L_r|j,0,r>=|j> for j=o,p,v,
  L_r|p,1,r>=(−1)^r|u>.

Within either L_r, the four indicated input vectors map bijectively, up to sign, to the four source basis vectors. Thus

  P=Σ_r L_r†L_r=(Q⊗Pi_0^E+Pi_p⊗Pi_1^E)⊗I_R

is the rank-eight orthogonal projection onto their union. Define a single map on all joint operators by

  D(X)=Σ_r L_r X L_r†+Tr[(I−P)X] Pi_o.

The first two terms are CP. The complement term has Kraus operators |o><b| over an orthonormal basis of ran(I−P), so it is CP. The total adjoint Kraus product is P+(I−P)=I. Therefore D is CPTP on arbitrary joint inputs, not just on the code images.

Direct substitution gives

  L_0 B=I,  L_1 B=0,
  L_0 A=I/sqrt(2),  L_1 A=I/sqrt(2),
  (I−P)A=(I−P)B=0.

For the u column of L_1 A, the negative coefficient of |p,1,1> in A is canceled by L_1's negative sign. These identities prove

  D(A X A†)=X=D(B X B†)

for every source operator X. No realization label or source-dependent choice enters D. Equality of the linear maps on all source operators also gives equality after tensoring with an identity map on any reference system. Thus reference-entangled inputs are covered. The identity A†B=I/sqrt(2) is a consistency check, not an added assumption or an appeal to a recovery theorem.

## 5. The same nominated receiver can still be blind

For every source density rho,

  Tr_SE(B rho B†)=|0><0|,
  Tr_SE(A rho A†)=Tr(Q rho)|+><+|+rho_uu|−><−|.

Cross terms vanish on tracing S,E, including the p/u coherence because their E labels are orthogonal. In particular, fix the SAME R effect F=|−><−| before comparing implementations or source preparations. Its source pullbacks are

  B†(I_SE⊗F)B=I_S/2,
  A†(I_SE⊗F)A=Pi_u.

B therefore gives zero contrast for every R effect, not merely for F. A gives contrast Tr(F[Tr_SE(A Delta A†)])=1/5. Its R state difference is (|−><−|−|+><+|)/5, with trace distance 1/5. The initial blank R is identical across the source pair in both implementations.

Together §§4–5 exhibit a single fixed global exact quantum recovery D and two encodings implementing the same C, while delivery to the same nominated R differs. This falsifies the proposed implication based solely on existence of such D. It does not claim that D works for every realization of C, or that the old W_R and W_E have a common quantum decoder. The explicitly specified D does not even decode the old W_R u atom correctly: it returns p from |p,0,1>.

## 6. Constructive single-effect follow-through and its actual domain

For any source observable H, the Hilbert–Schmidt adjoint of the specified D is

  D*(H)=Σ_r L_r† H L_r+<o|H|o>(I−P).

Taking H=Pi_u makes the complement term zero and removes the signs, giving the exact binary projection

  G=D*(Pi_u)=Pi_p⊗Pi_1^E⊗I_R.

Its expectation on either encoded input equals rho_uu. The source pair therefore gives probabilities 2/5 and 1/5. This recovers one effect, not the entire source.

On arbitrary joint inputs, G genuinely depends on S and E and not on R. It cannot equal an S-only effect, since at S=p changing E from 0 to 1 changes its value. It cannot equal an E-only effect globally, since at E=1 changing S from p to o changes its value.

However, all encoded inputs from A and B lie in P. Put G_E=I_S⊗Pi_1^E⊗I_R. Then

  P G P=P G_E P.

Indeed the E=1 part of P has S=p. Thus E alone reads this one recovered source population on every encoded input from A or B, including coherent source inputs. The S gate in the exact full-domain D* effect reflects the specified off-code completion and must not become a claimed physical necessity for the weaker one-effect target. No R phase correction or implementation of full D is needed to evaluate this statistic if the E effect is separately available.

This is not an R-owned effect and does not identify E with the mathematical owner p. It does not make E physically accessible or extend this fixed E test to all realizations of C. In particular it is a precise support description of this counterexample, not a native delivery construction.

## 7. Relation to the inherited P1/P2 operations

On the same four-address grade domain, P(e_u−e_p)=0, whereas extraction of the u coefficient takes value 1 on e_u−e_p. Equivalently P e_u=P e_p but their u grades differ. Therefore z_u is not a function of the retained grade Pz on the full declared domain. This is a simple mathematical nonfactorization fact, not a claim about physically reachable preparation sets.

P2 gives the signed decomposition

  z=IPz+(Id−IP)z,
  (Id−IP)z=z_u(e_u−e_p).

The u coefficient of this mathematical loss vector recovers z_u. P2 does not thereby store the vector, produce a positive E flag, or assign its observation to p or R. Such a physical realization remains a separate obligation.

Recovering z_u is NOT necessary for the user's pair-only target. The retained-source effect Pi_p has expectations 3/5 and 2/5 after C and contrast 1/5 under every implementation of C. Its actual owner availability remains unearned. Failure to derive the E flag must not be used to reject that weaker positive route or demand full source recovery instead.

The precise next native task is a producing operation and immutable source that make at least one fixed separating effect available to the same retained owner. For the recovery-specific proposal, G_E identifies a concrete candidate output flag, but its availability and owner relation are supplied. For the retained-aggregate route, the candidate remains Pi_p. Neither D* membership nor P2's signed loss decomposition establishes the operational connection.

## 8. Adverse controls and known limits

These controls are disclosed analytical observations, not prospective discoveries:

1. Dropping D's complement term fails trace preservation on a unit vector outside P, for example |u,0,0>.
2. Replacing L_1's negative action on |p,1,1> by a positive sign leaves diagonal A-input recovery intact but destroys u/retained coherences. For X=|p><u|, the two recovery contributions cancel instead of summing to X. Tests restricted to diagonal inputs would miss this failure.
3. D_cl is a common classical decoder for W_R/W_E but not a quantum decoder. The new D is a common quantum decoder for A/B, not a decoder for all benchmark realizations.
4. Replacing the same R effect between implementations would not test the fixed-interface claim. The displayed F is identical throughout.
5. The exact full-domain G differs from G_E off-code, such as on |o,1,0>. On-code equality is the claimed weaker fact.
6. A different physical source rule might legitimately restrict the implementation class or earn another owner effect. These examples do not forbid that. Neither full support on an arbitrary environment nor full algebra access is imposed as a universal native requirement.

## 9. Review and stopping scope

The complete claims to adjudicate are the global recovery facts, common classical decoder, strengthened common quantum decoder and fixed R consequences, the exact single-effect/domain distinction, and the P1/P2/physical scope. The finite-dimensional calculations support elementary proofs; no numerical sweep or new mechanism is proposed. The original posts' scripts were posthoc and remain labeled that way. New supporting checks will follow a frozen protocol without rewriting their history.

Native bridge NOT_DERIVED. Physical result not claimed. No hold release, milestone, main merge, or promotion of a source-correspondence premise is requested.
