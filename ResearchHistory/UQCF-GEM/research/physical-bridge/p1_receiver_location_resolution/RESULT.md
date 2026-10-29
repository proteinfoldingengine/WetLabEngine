# Exact P1 source correspondence does not determine an existing receiver's record

Date: 2026-10-29 America/Phoenix. Author: proteinfolding-gpt.
Inspected shared head: c5cefae1b1dd8d877d1a919c27f4196eb150e353.
Status: AUTHOR ANALYTICAL RESOLUTION of one implication; independent review pending.
Class C: application of the existing complementary-output boundary to the current P1 contract. Native bridge NOT_DERIVED. No mathematical priority or new physical law is claimed.

## 1. What is being resolved

The user asks whether the missing actual-event-to-owned-record connection can be resolved. The precise question addressed here is:

> If the current P1 event has exact physical source correspondence, faithful preparations and unchanged physical representations of retained states, does that force a distinction into one already designated, initially blind, accessible receiver R?

The answer to this implication is **no**. The proof below satisfies those source conditions in both cases, with the same R, its complete initial state and its available observations. R remains completely unchanged in one case and acquires a probability contrast of 1/5 in the other. Both implement the identical nonidentity source channel on every quantum input.

This is not a proof that UQCF-GEM cannot have interactions, that no receiver anywhere can change, or that an actual experiment has a blind receiver. It resolves an inference from source correspondence to nominated-receiver acquisition within the explicitly stated contract. A native rule constraining the joint event or identifying the actual owned record could exclude the blind case; no such rule is asserted absent from every possible extension.

## 2. Provenance and the stronger source contract

The inherited native tree has o->p, p->u, p->v. Let X=(o,p,u,v) and Y=(o,p,v). P1 is

    P(z_o,z_p,z_u,z_v) = (z_o,z_p+z_u,z_v).

P2 is the literal zero extension I from Y to X. These are the existing FCV operations. They do not themselves identify physical state factors with addresses.

Reuse the current conditional quantum benchmark, without treating its physical premises as native-derived:

    H_S = span{|o>,|p>,|u>,|v>},
    Q = I_S - |u><u|,
    C(rho) = Q rho Q + rho_uu |p><p|.

This is the existing completed reset, not a new finite-duration damping model. Actual occurrence of the relevant event is assumed in each comparison; absence of occurrence is not used as a counterexample.

Fix the SAME source encodings in both cases:

    Pi_X(z) = sum_(i in X) z_i |i><i|,
    Pi_Y(y) = sum_(i in Y) y_i |i><i|.

The grades here are normalized nonnegative vectors. Their interpretation as physical mixture weights remains a SUPPLIED benchmark premise. On the entire simplex both encodings are positive, normalized, affine and injective, and

    C Pi_X = Pi_Y P,
    Pi_X I = Pi_Y.

Thus physical retention of all retained atomic codes is imposed, not left free. C in fact fixes every density operator supported on span{|o>,|p>,|v>}, including its coherences. This goes beyond mere equality of the native output labels.

Use the same pair as the prior P1 correspondence result:

    z+ = (1,1,2,1)/5,   z- = (1,1,1,2)/5,
    rho+ = Pi_X(z+),    rho- = Pi_X(z-).

The four calibration states sigma_i=|i><i| satisfy all four source/preparation conditions of the prior positive proof, with a=<u|sigma_u|u>=1. No input code is swapped between the two implementations.

The comparison adds a fixed output interface: qubits E and R, initially in |0_E 0_R>, independent of the source preparation. R is the same existing receiver in both cases; E is outside its specified accessible interface. Give R its ENTIRE qubit observable algebra, including the same effect N_R=|1><1|. Thus the negative case is not caused by choosing a poor detector or hiding another available degree of freedom inside R. These factorization and access specifications are explicit conditional premises, not deductions from native addresses.

## 3. The strongest positive construction

Write output vectors in the order S,E,R. Define the fixed isometry W_R by

    W_R|j> = |j>|0>|0>  for j=o,p,v,
    W_R|u> = |p>|0>|1>.

Its four columns are orthonormal. The colliding source outputs p and u are distinguished by R. Tracing E and R gives C on every matrix, not just the two tested states: the retained block Q rho Q survives, the u population becomes |p><p|, and all coherences joining u to a retained basis state vanish.

For a diagonal source Pi_X(z), the complete receiver state is

    omega_R^write(z) = (1-z_u)|0><0| + z_u|1><1|.

Consequently

    omega_R^write(+) = diag(3,2)/5,
    omega_R^write(-) = diag(4,1)/5.

N_R has probability difference 1/5 and the two receiver states have trace distance 1/5. The initial complete receiver is |0><0| in both preparations. This realizes the earlier positive port argument with its explicit joint-operation premise. It is a supplied implementation, not the desired native derivation.

## 4. A blind receiver with every source condition retained

Define a second fixed isometry W_E on the SAME spaces and initial environment:

    W_E|j> = |j>|0>|0>  for j=o,p,v,
    W_E|u> = |p>|1>|0>.

Again the four columns are orthonormal, and tracing E,R gives exactly C on every matrix. Equivalently W_R=(I_S tensor SWAP_ER) W_E, so their reduced source channels are identical. Both isometries can be extended to unitaries on S,E,R with the same blank input subspace, by completing their orthonormal columns. No Hamiltonian, elapsed duration, energy conservation or physical implementation is inferred from that extension.

For W_E,

    omega_R^blind(z) = |0><0| for EVERY source state.

In particular omega_R^blind(+)=omega_R^blind(-), so every available receiver POVM has the same outcome distribution. A fixed subsequent receiver-only operation, including an instrument with its complete outcome record, cannot distinguish equal input states. This statement does not include later access to S or E, or source-informed postselection.

The source outputs are identical across the two implementations:

    C(rho+) = (|o><o|+3|p><p|+|v><v|)/5,
    C(rho-) = (|o><o|+2|p><p|+2|v><v|)/5.

They exactly represent the same P1 outputs. In the blind case E carries the record that R carries in the positive case. The full E,R outputs still distinguish the pair; nothing claims global destruction or contradicts complementary-record preservation.

What varies is the unresolved joint realization, not the source encoding, retained physical codes, source event channel, nominated receiver, its complete initial state, or its available measurements. Because both source channels agree on all matrices, adding a reference ancilla to a source-only characterization also cannot distinguish them: both induce C tensor identity on that interface. The joint event is distinguishable by observing the output interface; source-only correspondence does not determine it.

## 5. Exact receiver contrast range in this benchmark

The two constructions already disprove the proposed implication. A direct bound shows that they attain the extremes for the fixed diagonal pair.

Let W be ANY fixed isometry implementing C with environment E tensor R. Since C sends each basis state to a pure source state,

    W|j> = |j>|e_j> for j=o,p,v,
    W|u> = |p>|e_u>.

Preservation of every retained off-diagonal |j><k| forces <e_k|e_j>=1, so all retained environment vectors equal one normalized vector e_0. Orthogonality of W|p> and W|u> forces <e_0|e_u>=0. Let

    tau_0 = Tr_E |e_0><e_0|,
    tau_u = Tr_E |e_u><e_u|.

For the stipulated diagonal pair,

    omega_R(+) - omega_R(-) = (tau_u-tau_0)/5,
    D(omega_R(+),omega_R(-)) = D(tau_u,tau_0)/5 <= 1/5,

where D(A,B)=||A-B||_1/2. The last inequality follows from the triangle inequality and unit trace of the positive matrices tau_u,tau_0. W_E attains zero; W_R attains 1/5. Hence the exact minimum and maximum over this implementation class are 0 and 1/5. No parameter sweep or numerical evidence is needed.

For the COMPLETE environment, e_0 and e_u are orthogonal and its contrast is always 1/5. If R is independently established to be that complete environment, the blind construction is outside that stronger contract. The proof identifies exactly why full-complement statements cannot silently be applied to a nominated accessible part.

## 6. Relation to established work and decision

- The prior P1 event/source counterexample held one joint interaction fixed and varied the input code; its blind code violated physical retained-state correspondence. Here the code and physical retention are held fixed; the varied object is the joint realization left unspecified by its source channel. The earlier theorem and counterexample remain valid.
- The existing partial-complement result already establishes the general freedom to move record information between accessible factors, unread factors and correlations without changing a source channel. This note applies that known boundary to the exact current four-atom P1 contract. It is not a newly discovered general no-hiding or channel theorem.
- The corrected canonical P1 acquisition result still forces a change in the formal p-coordinate. Neither isometry identifies physical R with that coordinate. That missing ownership identification is the point under test, not a premise the blind example pretends to satisfy.
- The result does not quantify over every native operation or every physically accessible subsystem. It proves non-entailment for the explicitly strengthened source contract above. It does not show that every physical model compatible with the whole UQCF archive is noninteracting.

The current inference is therefore resolved negatively: even earning exact source event correspondence and retained source representation would not, by themselves, earn delivery to the nominated receiver. The required next connection is a source-backed relation between the actual joint event and that receiver's owned output, or an independently justified identification of the relevant retained factor with its accessible state. A derived law for one available effect can suffice; a full physical theory or unique microscopic dynamics is not required. Merely selecting W_R would assume the sought delivery.

This is a scoped logical resolution, not an achieved native physical prediction. No detector design, fundamental clock, geometry, new grading axiom, historical recertification, numerical campaign, branch merge or stage closure is claimed. Actual event occurrence remains ACCEPTED INPUT. Mathematical and physical identification claims remain separate.
