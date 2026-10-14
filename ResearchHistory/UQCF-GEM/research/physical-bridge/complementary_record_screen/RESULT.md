# What a retained algebra forces into a complete coherent complement

Date: 2026-10-14 UTC. Inspected parent: `cfc3f2f5434d2d5222d8d8ba67e2bc0b1b2c4483`.

**Disposition: exact conditional complementary-record criterion; physical realization and receiver access remain open.** For a supplied finite block-tensor retained algebra, its trace-preserving expectation determines the information in every complete pure isometric complement, up to an environment isometry. That information is exactly the input restriction to the algebra's commutant. A discarded factor can therefore give a forced complementary distinction, while a distinction confined to correlations can disappear from both output marginals. Neither conclusion identifies a native accessible receiver.

This is an application of standard finite-dimensional channel algebra. It is not a new no-hiding theorem, a claim of mathematical priority, or adoption of an environment as physical ontology. The isometric extension is an explicitly conditional test of a proposed record route. No physical primitive is added to the research model.

## 1. Why this is the next distinct test

The preceding pruning/current result derived a balance representation on the inherited lineage tree and proved that all its surviving-edge coordinates vanish. A coarse vertex amount can differ, but it denotes a larger fine fiber and does not establish a receiver write. Its remaining possibilities included a separately retained record. We now test a particular rationale for such a record: if a retained description loses a distinction, must a reversible realization place that distinction into a complementary output that could be read on its own?

The v15.11 reconciliation already establishes a supplied retained algebra (RAS), its canonical tracial expectation, a separately supplied actual record (RCR), and the difference between retained loss and loss in a complete coherent description. Its CNOT example preserves a phase distinction jointly while losing it in the retained system. The recent instrument classification covers classical labels for a supplied sharp pinching channel. It explicitly leaves general algebra multiplicities and complete coherent complements outside that classification.

The new result is the complete marginal-information criterion for the declared block-tensor expectation and all of its pure isometric realizations, including multiplicity factors. The old CNOT example is a consistency check, not a new discovery or rerun. We do not infer that the lineage grade is a quantum density matrix or identify the lineage carrier with the quantum tensor factors. Those native source/carrier bindings remain unearned.

| Premise | Standing in this test |
|---|---|
| Finite quantum carrier and retained algebra | Supplied RAS data, as in v15.11 |
| Canonical trace-preserving expectation for that algebra | Inherited conditional construction; explicit formula derived below |
| A complete pure isometric realization of the expectation on every input | Hypothetical realization class being tested; not a derived physical law or an actual event |
| Particular source states or a source-to-factor dictionary | Analytical preparations below; not native source acquisition |
| Actual central outcome, event occurrence and subsequent record retention | Not supplied by the dilation theorem; RCR boundary preserved |
| Access to the whole complement, its reference frame and a readout | Additional operational obligations, not a consequence of an abstract factorization |

## 2. A precise retained algebra and its expectation

Fix positive integers a_i,b_i and a supplied decomposition

    H = direct_sum_i (A_i tensor B_i),
    dim A_i = a_i,   dim B_i = b_i,
    A = direct_sum_i (B(A_i) tensor I_{B_i}).

Here B(A_i) denotes the full matrix algebra on A_i. These are mathematical factors of the declared representation; they are not automatically separately accessible physical subsystems. Let P_i project onto sector i and write X_ii=P_i X P_i, regarded as a matrix on A_i tensor B_i. Off-diagonal X_ij are allowed in a general input.

The ordinary-trace-preserving conditional expectation is

    Phi_A(X) = direct_sum_i [ Tr_{B_i}(X_ii) tensor I_{B_i}/b_i ].       (1)

To verify the formula, first discard off-diagonal sectors, then trace the B_i factor and replace it with its normalized identity. Each step is completely positive and their composition preserves trace. Its range is A, it fixes A pointwise, and it is the Hilbert-Schmidt orthogonal projection onto A: for every a in A,

    Tr[a^dagger Phi_A(X)] = Tr[a^dagger X].

This is the finite tracial expectation supplied by RAS. It does not select A, choose an actual event, or enact the map. The stated block-tensor form is the scope of the argument; no physical tensor-factor interpretation is inferred from it.

The commutant in B(H) is

    A' = direct_sum_i (I_{A_i} tensor B(B_i)).                         (2)

Indeed, commuting with all central P_i removes inter-sector blocks, and commuting with every matrix unit on A_i forces a block to be identity on A_i tensored with an arbitrary B_i matrix. The center, containing the sector weights, is shared by A and A'.

## 3. Derive a complete coherent complement

Choose bases |a> in A_i and |b>,|u> in B_i only to write matrices. Define

    E_min = direct_sum_i (U_i tensor B_i),   dim U_i=b_i,

with orthonormal environment labels |i,u,b>. The isometry V:H->H tensor E_min is

    V |i,a,b> = (1/sqrt(b_i)) sum_u |i,a,u> tensor |i,u,b>.             (3)

Its images of the input basis are orthonormal, so V^dagger V=I. Tracing the environment in V X V^dagger gives (1). Tracing the system gives the complementary channel

    Psi_A(X) = direct_sum_i [ I_{U_i}/b_i tensor Tr_{A_i}(X_ii) ].      (4)

For (4), the system trace requires the same sector, the same a, and the same u on the two sides of a matrix element. It eliminates inter-sector coherences and traces A_i, while retaining the B_i matrix indices. This calculation includes unequal a_i,b_i, nonnormalized blocks, and arbitrary off-diagonal inputs.

The Kraus operators associated with the environment basis are

    K_{i,u,b} = (1/sqrt(b_i)) [ I_{A_i} tensor |u><b| ] P_i.           (5)

They are linearly independent: different sectors or different matrix units are Hilbert-Schmidt orthogonal and every operator is nonzero. Consequently the Choi rank is sum_i b_i^2 and this environment is minimal.

**Proposition 1: every complete pure isometric realization has the same complementary information.** If another isometry V_tilde:H->H tensor K satisfies

    Tr_K(V_tilde X V_tilde^dagger) = Phi_A(X) for EVERY matrix X,

then there is an isometry U:E_min->K such that

    V_tilde=(I_H tensor U)V,
    Psi_tilde_A(X)=U Psi_A(X) U^dagger.                               (6)

Proof. Expand V_tilde in an environment basis to obtain Kraus operators L_alpha for the same channel. The Choi matrix is the sum of their vectorized outer products. Equality to the Choi matrix from (5) makes every L_alpha lie in the span of the independent K_{i,u,b}: a vector orthogonal to that span has zero positive quadratic form and hence zero overlap with every L_alpha. Expressing the L_alpha in that basis, equality of the two Choi matrices forces the coefficient columns to be orthonormal. Those columns define U, and substituting into the Kraus expansion gives (6). This is the finite minimal-dilation uniqueness argument. QED.

Changing the auxiliary basis or enlarging a pure isometric environment therefore cannot change which input pairs its COMPLETE state distinguishes. This is not a statement about a chosen subregister, a classical flag, a mixed unpurified apparatus, or an implementation specified only on one input pair.

## 4. Exact criterion for a complementary distinction

For two states rho_0,rho_1 let Delta=rho_0-rho_1 and define the unnormalized marginal differences

    S_i = Tr_{B_i}(Delta_ii),
    G_i = Tr_{A_i}(Delta_ii).

Use D(rho,sigma)=||rho-sigma||_1/2. Equations (1), (4), and (6) give

    D(Phi_A(rho_0), Phi_A(rho_1)) = (1/2) sum_i ||S_i||_1,           (7)
    D(Psi_tilde_A(rho_0), Psi_tilde_A(rho_1))
        = (1/2) sum_i ||G_i||_1                                  (8)

for every complete pure isometric realization. The proof uses additivity of trace norm over direct sums, ||M tensor I_d/d||_1=||M||_1, and invariance under isometric embedding.

Thus a nonzero complementary state distinction is forced across this whole realization class if and only if at least one G_i is nonzero. Equal retained outputs only say all S_i vanish; they do NOT imply that any G_i is nonzero. All quantities in (7)-(8) concern specified states and specified output interfaces. No numerical error margin or single-event outcome has been generated.

Equation (4) has a useful algebraic meaning. Expectations of every input observable in A' are determined exactly by the matrices Tr_{A_i}(rho_ii), and those matrices determine all of Psi_A(rho). The complement has precisely the information in the restriction of rho to A'. In matrix-state language it is mutually recoverable, by explicit mathematical channels, with

    Phi_{A'}(rho)=direct_sum_i [ I_{A_i}/a_i tensor Tr_{A_i}(rho_ii) ].

In each sector, trace out the normalized-identity factor and replace it with the other normalized identity. Sector pinching extends these maps to channels on their whole input spaces. For an enlarged embedding U, use its inverse on its range and any fixed replacement state on the unused orthogonal subspace. These are existence statements about recovery maps, not instructions available to a native event.

The joint coherent output preserves the entire input trace distance:

    D(V_tilde rho_0 V_tilde^dagger, V_tilde rho_1 V_tilde^dagger)
        = D(rho_0,rho_1).                                          (9)

If both (7) and (8) vanish while rho_0 differs from rho_1, the distinction remains in the joint state but is absent from either marginal alone. Saying it is in correlations does not mean it is inaccessible to every joint protocol, and does not supply such a protocol or its physical availability.

## 5. Positive and rejecting controls on the same retained algebra

Take a single sector H=A tensor B with a=b=2 and retained algebra B(A) tensor I_B. Its channel is

    Phi_A(rho)=Tr_B(rho) tensor I_B/2.

**Positive conditional transfer.** Fix the same state tau on A and set

    rho_0=tau tensor |0><0|_B,
    rho_1=tau tensor |1><1|_B.

The retained outputs are identical. The complementary outputs in (4) are

    (I_U/2) tensor |0><0|_B,
    (I_U/2) tensor |1><1|_B,

which have orthogonal support and distance one. Every complete pure isometric realization has this distance by (6), so no convenient choice of one dilation is responsible for the distinction. In the displayed realization, measuring the last B factor separates the pair exactly. A unitary implementation with a fixed pure initially independent auxiliary would begin with the same auxiliary state for both sources; that conditional realization would genuinely transfer a distinction. The physical source-to-factor binding, operation, complete auxiliary retention and calibrated readout are still assumptions, not achievements of this example.

**Correlation control with the SAME channel.** Instead use

    |Phi_+>=(|00>+|11>)/sqrt(2),
    |Phi_->=(|00>-|11>)/sqrt(2).

These orthogonal states have identical A and B marginals I_2/2. Their retained outputs both equal I_4/4, and their complete complementary outputs both equal I_4/4 in (4). These equalities hold for every realization in Proposition 1. Yet their joint coherent outputs have distance one. A loss from the retained system therefore does not force a stand-alone complementary record for this actual pair. The control changes only the preparations, not the retained algebra or its expectation.

The comparison is stronger than a zero-action example: the same nonidentity channel removes the entire source distinction from its retained output in both cases. Its complementary record distinguishes the product-state pair perfectly and fails completely for the correlation pair.

## 6. Pinching, full erasure and the no-hiding quantifier

When every b_i=1, (1) is exactly the sharp pinching from the earlier instrument assessment. Equation (4) reduces to

    Psi_A(rho)=sum_i Tr(P_i rho)|i><i|.

The complete coherent complement carries the sector weights, but no phase between sectors and no additional within-sector state. An arbitrary classical measurement or coarse flag of that complement need not preserve its distinction; the earlier zero guaranteed label-information floor remains intact. Conversely, changing sector weights already changes a retained central observable, so this pinching complement is not a new acquisition of a distinction erased from that retained algebra. The historical |+>/|-> dephasing control is now covered for every complete pure dilation, not only its displayed CNOT realization.

At the other extreme, one sector with a=1,b=d gives A=complex multiples of I and

    Phi_A(rho)=I_d/d,
    Psi_A(rho)=(I_d/d) tensor rho.

The full complement contains the entire arbitrary input state, including its correlations with an external reference; tracing the first factor recovers it. The equality extends to reference-entangled inputs because it is a channel identity on every matrix. This is the constant-channel no-hiding situation.

These two endpoints explain why equality of the retained output on TWO selected preparations is insufficient to invoke that arbitrary-state conclusion. Dephasing and full erasure both send the qubit |+>/|-> pair to I_2/2, but their complete complements distinguish that pair by distances zero and one respectively. Only the latter channel is constant on the whole qubit state space. This does not contradict no-hiding: its all-input hiding premise is load-bearing. The Bell-pair control in section 5 similarly concerns two selected states, not a channel constant on their entire coherent span.

## 7. A mixed auxiliary is not the complete pure complement

There is a second boundary even for full erasure. Let S be a qubit and K a four-valued quantum key initially in the mixed state I_4/4, independent of S. Take P_k in {I,X,Y,Z} and the controlled unitary

    C=sum_k P_k tensor |k><k|_K.

Its output on rho tensor I_4/4 is

    Omega_SK(rho)=(1/4) sum_k P_k rho P_k^dagger tensor |k><k|.

The Pauli average sends every qubit matrix X to Tr(X)I_2/2. Hence the system marginal is always I_2/2 and the key marginal is always I_4/4, for EVERY input state. The joint output still recovers rho by applying C^dagger and tracing K. For the |0>/|1> source pair the two marginals have distance zero and the joint output distance one.

This is not a counterexample to Proposition 1. The map from a pure input to Omega_SK is a mixed-state encoding, not a pure isometry into S tensor K. Purifying the initial key with another register F makes the complete map into S tensor K tensor F isometric; the full complement is then KF. Proposition 1 and the full-erasure conclusion apply to KF, not automatically to the actual accessible key K. We have not adopted F as a physically accessible hidden register. The calculation shows why access to a mathematical purification must not be silently assigned to a receiver.

Thus even supplying a unitary interaction does not, by itself, make every chosen auxiliary marginal a readable repository of the erased source. The initially available degrees of freedom, their state, and what remains accessible matter. This exact symbolic control is not a numerical campaign or a proposed native mechanism.

## 8. What follows scientifically

The new positive conditional statement does not select a microscopic dilation: for the declared retained algebra and actual pair, (8) is the same for every complete pure isometric realization. It identifies exactly when that enlarged interface must contain a distinction and when even that complete marginal cannot contain one. This advances the accounting of a possible record route, not the physical origin of the channel or receiver.

| Question | Result |
|---|---|
| Does a full pure complementary output have implementation-independent information content? | Yes, up to environment isometry; it is the restriction to A' |
| Does any loss from the retained description force a distinguishable complementary marginal? | No; the criterion is G_i nonzero for some i, and the fixed-channel Bell control has all G_i zero |
| Can a supplied erasure of a quantum factor force a complete complementary distinction? | Yes, for the specified product-state pair; the distance is one for every pure realization |
| Does global coherent recoverability select a stand-alone readable record? | No; joint correlations and inaccessible purification degrees must be distinguished from a receiver |
| Does an arbitrary classical label retain the complement's information? | No; its actual measurement and retention remain separate |
| Has a native event, source binding, receiver or physical force been derived? | No |

An invariant distance establishes the existence of a suitable distinguishing measurement on the declared complete output. It does not identify an implementation-independent named detector or give an event its environment embedding U. Even the positive case requires a justified output interface and reference, actual application, retained access and an error contract. An already derived probabilistic record law could qualify; no deterministic outcome, unique microscopic mechanism, guaranteed completion or full C3/gravity closure is imposed as a new gate.

For this route, the next admissible candidate must identify a native relation that supplies an actual complete complementary or joint interface, and show that its actual source pair has the required G_i or accessible correlation contrast. It must justify why that interface remains available through pruning. A source-to-quantum-factor dictionary cannot be inserted. Merely selecting the product-state example, choosing a convenient dilation, or appealing to no-hiding does not discharge those obligations. Other justified channels remain eligible.

**Native milestone: NOT ACHIEVED.** RAS/RCR, the conditional record-compatible order, retained source binding/grade, the earlier instrument results, and the lineage balance result remain preserved in their original scopes. There is no archive-wide impossibility claim. No scientific source module was executed, no test count increased, and no numerical preregistration, main merge or numbered-stage CLOSED/CERTIFIED status is claimed. Time remains pruning / ordered recoverability update. No clock, energy, metric, geometry, dark-matter primitive or gravity fit is introduced.

## 9. Sources and review boundary

Nine exact repository sources at the inspected parent are preserved in source_packet.json and source_identities.json: AGENTS.md; the v15.11 report and implementation; the record-compatibility, instrument-access and pruning/current reports; the physical-frontier decision; the native-event milestone; and the continuation index. The implementation's supplied projectors and explicit record argument were inspected, not executed. Historical results are not recertified here.

Primary mathematical context, consulted 2026-10-14:

- John Watrous, The Theory of Quantum Information, Chapter 2, especially the Choi/Kraus correspondence and Corollary 2.24 on equivalent Stinespring representations: https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.2.pdf . These support the standard representation machinery. The block formulas, criterion and proofs used here are written out above.
- Samuel L. Braunstein and Arun K. Pati, Quantum information cannot be completely hidden in correlations, arXiv:gr-qc/0603046, perfect-hiding discussion and equations (2)-(4): https://arxiv.org/pdf/gr-qc/0603046 . The all-input constant-output and complete-ancilla qualifications motivate the explicit scope checks. Its gravitational application is not used as evidence for this research program.

This report is an exposed analytical argument for whole-argument independent review and separate immutable publication auditing. Those reviews establish their stated scopes only; they do not turn conditional channel mathematics into native physics.
