# Retained-reader statistics and the source of a record write

Date: 2026-10-15 America/Phoenix.
Immutable source parent: `fca6dc85ecef559aa3e7b84026ef8c8b79353247`.

**Bounded analytical assessment; native record-writing interaction remains OPEN.** The previous compatible-history result left changing raw record bits eligible even when the hitting profile stays constant. This note tests a specific implementation claim: can the inherited nonselective retained-algebra reduction itself write a source distinction into a fixed reader whose observables remain retained?

It cannot change that reader's probability law. This follows from the standard defining preservation property of the tracial conditional expectation; that property was already present in the instrument-access and complementary-record reports. The contribution here is its application to the proposed record write, including compositions and source-dependent choices of reduction, a direct audit of where the inherited coherent-record code actually writes, and controls against extending the conclusion to other reader interfaces. No new general information theorem, mathematical priority or physical conservation law is claimed.

## 1. Fix the reader before comparing the sources

Use the inherited finite-dimensional quantum carrier H and ordinary-trace-preserving conditional expectation E_A onto a supplied unital observable algebra A. RAS supplies A; this note does not select it or derive its occurrence. The inherited preservation identity is

\[
\operatorname{Tr}[a E_A(X)]=\operatorname{Tr}[aX]\qquad(a\in A). \tag{1}
\]

For completeness, the tracial expectation is the Hilbert-Schmidt orthogonal projection onto A, so its adjoint fixes every a in A, giving (1). Equivalently its A-bimodule property and trace preservation give Tr[a E_A(X)]=Tr[E_A(aX)]=Tr[aX]. The earlier complementary-record report writes the finite block-tensor formula and verifies this property explicitly. This includes general retained algebras with multiplicities, not only sharp sector pinching.

Declare one fixed reader algebra R on the same H. A binary readout is an effect Q in R, 0<=Q<=I; its probability of output 1 is Tr(Q rho). More generally a finite readout has effects M_r in R with sum_r M_r=I. This is a conditional quantum interface, not a derivation that a native event possesses R, performs a measurement or retains its outcome.

For acquisition from two sources rho_0,rho_1, assume their initial restrictions to this reader agree:

\[
\operatorname{Tr}[a\rho_0]=\operatorname{Tr}[a\rho_1]\quad(a\in R). \tag{2}
\]

This does not say their full states agree or that system-side dependence on their difference is forbidden. It identifies the record that initially lacks that difference. For a single-bit task it suffices to assume equality for the particular effect Q.

## 2. Reduction preserves the entire fixed-reader law

Let a finite sequence contain only the nonselective operations E_{A_1},...,E_{A_n}, and assume

\[
R\subseteq A_k\quad\text{for every }k.
\]

Writing Phi=E_{A_n}...E_{A_1}, repeated use of (1) gives

\[
\operatorname{Tr}[M_r\Phi(\rho)]=\operatorname{Tr}[M_r\rho] \tag{3}
\]

for every reader effect M_r and every input state. Thus (2) remains true at the output. An initially blank bit with Tr(Q rho_b)=0 for both sources stays blank; any other common initial probability likewise stays unchanged. No purity, full-rank assumption, commutative reader or center-only restriction is needed. The conclusion concerns the full final readout distribution, not just its average bit value.

The A_k need not be nested for this argument. In the inherited nested-algebra case, choosing R contained in the final algebra automatically puts it in every earlier one. The result does not grant an event knowledge of that future algebra or justify the reader's physical access to it.

**Choosing the reduction by source does not evade (3).** For each source, even a different finite path of such nonselective maps leaves that source's R restriction unchanged. A mixture of those paths applied to the same input also preserves it, even if the mixture weights are allowed to depend on that input. This is a pointwise mathematical statement, not adoption of a nonlinear physical selector. The comparison does not attach the selected path's name as a new readable output. Producing such a label, or conditioning the input state on a measured outcome, introduces a separate instrument/record operation.

This is not a theorem about every pruning operation, every auxiliary marginal or every accessible consequence. It concerns only the specified common reader fixed by each nonselective expectation. The global state may change, other distinctions may be lost, and correlations or other interfaces may behave differently. Also, a previously encoded distinction might become newly accessible through a derived change of access, even with unchanged probabilities. Equation (3) neither supplies nor rules out such an access mechanism; the equal-initial-reader premise (2) must not be silently replaced.

## 3. The inherited coherent-record implementation writes before pinching

The current v15.15 source is explicit about its conditional construction:

| Function | Actual role |
| --- | --- |
| `initial_joint(rho)` | Inserts a supplied system state into the supplied all-zero record-register block |
| `controller_gate(event)` | Assembles a supplied quantum block-controlled operation from the prior instrument |
| `copy_gate(event)` | Sets `new_memory = memory XOR system_bit` at the designated register |
| `event_gate(event)` | Composes `copy_gate(event) @ controller_gate(event)` |
| `pinch_records(a)` | Removes off-diagonal record blocks while leaving every diagonal block intact |
| `weights(a)` | Reads the traces of those diagonal record blocks |

Consequently `weights(pinch_records(a))=weights(a)` as a matrix identity, independent of the chosen input. The code's record probabilities change through the preceding supplied gates. Pinching preserves those probabilities; it does not create their source correlation. This agrees with the original README's coherent-versus-pinched comparison and is not a new numerical finding. `audit()` also explicitly leaves `actual_record_selected=None`.

The smallest hand calculation isolates the mechanism already used by `copy_gate`. Use one source qubit S, one supplied memory qubit M initially in |0>, a controlled-NOT U from S to M, and Q=I_S tensor |1><1|_M. Then

\[
U^\dagger Q U
=|0\rangle\langle0|_S\otimes|1\rangle\langle1|_M
+|1\rangle\langle1|_S\otimes|0\rangle\langle0|_M.
\]

On sigma tensor |0><0| this gives output probability Tr[|1><1| sigma]. The two source basis states therefore give probabilities 0 and 1 from the same blank memory. Subsequent memory pinching leaves them unchanged because Q is retained. This is a valid conditional record write, including its source dependence. Its carrier, blank, controlled copying and readout remain supplied; no native origin for those inputs is derived here. This schematic two-register calculation explains the source code, rather than claiming a new physical preparation or execution.

## 4. A precise test for an additional coupling

For a supplied common unitary U followed by E_A, with an actual reader effect Q in A and Delta=rho_1-rho_0, the output contrast is

\[
\delta_{\rm out}=\operatorname{Tr}[U^\dagger Q U\,\Delta].
\]

If the initial reader contrast is zero, Tr(Q Delta)=0, this becomes

\[
\delta_{\rm out}=\operatorname{Tr}[(U^\dagger Q U-Q)\Delta]. \tag{4}
\]

Thus a proposed coupling must actually move the reader effect in a direction that detects the specified source difference. Merely having U^dagger Q U != Q is insufficient: a memory-only bit flip changes the blank bit to 1 for BOTH source states, giving no source contrast. The controlled-copy calculation passes the conditional test because the transformed memory effect depends on the source projector.

Equation (4) is an assessment criterion, not a new candidate action law or a requirement that all native dynamics be unitary. Its inputs U, Q and the source binding must come from the native construction before its nonzero value can count toward the milestone. A justified nonzero probability contrast is eligible; deterministic output or a unique microscopic mechanism is not required.

## 5. Controls against a universal no-writing claim

**A reader outside the retained algebra can change.** On two qubits S,M let F swap the factors and define

\[
E(X)=\tfrac12(X+FXF),\qquad A=\{X:XF=FX\}.
\]

Because F=F^dagger and F^2=I, this is the trace-preserving conditional expectation onto A; equivalently it pinches the symmetric and antisymmetric sectors. With the same blank memory, inputs |00><00| and |10><10| give

\[
E(|00\rangle\langle00|)=|00\rangle\langle00|,
\quad
E(|10\rangle\langle10|)
=\tfrac12(|10\rangle\langle10|+|01\rangle\langle01|).
\]

A local memory readout Q_M=I tensor |1><1| has probabilities 0 and 1/2. Thus even a nonselective expectation can transfer a distinction to a specified auxiliary marginal. This does not contradict (3): Q_M is not in A, since F Q_M F=|1><1| tensor I=:Q_S. Its effective retained observable is E(Q_M)=(Q_M+Q_S)/2, which already has the distinct initial expectations 0 and 1/2. That is a joint observable, not the original blank local reader. The control therefore rejects extending the fixed-reader result to every marginal, and distinguishes a physical local-readout interface from an abstract retained-observable description. The swap coupling, factor assignment and local readout in this example are supplied controls, not adopted native structure.

**Selective RCR conditioning is a different map.** With rho=I_2/2 and Q=|1><1|, nonselective diagonal pinching keeps Tr(Q rho)=1/2. Conditioning on the supplied positive-weight record Q gives rho_Q=Q and probability 1. The normalized selective operation is not the expectation in (1). This preserves the inherited positive conditional RCR construction; it does not derive the selected outcome or its delivery. Neither selection nor its associated label may be smuggled into the nonselective path while retaining (3)'s conclusion.

**Logical compatibility bits are not automatically fixed reader effects.** The preceding `(I,I)` to `(p,I)` record-family control changes a compatibility-view membership bit. That bit is a function of supplied record projectors and the tree. No fixed physical effect Q representing it had been constructed. Applying (3) does not invalidate that combinatorial change or establish that every possible realization is blind. A proposed realization must identify its actual reader, state preparation, update and access before the comparison applies.

These controls are exact analytic calculations, not an executed finite campaign. In particular the swap example prevents describing this result as "RAS alone can never change any receiver." The fixed-reader containment condition is essential.

## 6. Disposition and next obligation

**Disposition: COMMON_RETAINED_READER_STATISTICS_PRESERVED; COHERENT_WRITE_LOCATED_IN_SUPPLIED_COPY_GATE; NATIVE_COUPLING_AND_ACCESS_UNRESOLVED.**

This assessment resolves one proposed attribution: nonselective reduction does not write a new difference into a reader it fixes throughout. The existing coherent-record example achieves its conditional write through an explicit prior copying interaction. This was already supplied model structure; the present argument does not promote it to discovered native dynamics. The source-dependent-path result prevents relocating that write into a choice among reductions that all preserve the same reader.

For the current route, the next useful candidate must derive either a source-sensitive action on the specified reader, or a justified change of reader/access with an actual retained output. An inspected coupling should be checked on its native source pair, as in (4), rather than credited merely because it changes a bit. Repeating the coherent-copy simulation, choosing a convenient algebra or relabelling its XOR gate as a native force would not supply the missing origin. Other primitive-derived processes, partial records and probabilistic consequences remain eligible.

Eleven exact GitHub sources are bound in the accompanying packet: governing AGENTS, latest compatible-history assessment, record-compatibility report, instrument-access and complementary-record reports, v15.11 report/code, v15.15 README/code, continuation and native milestone. The inspection is bounded to these sources. No archive-wide absence or new physical impossibility claim is made.

Standard measurement/channel conventions were checked against John Watrous, *The Theory of Quantum Information*, Chapter 2, sections 2.2-2.3, especially Definition 2.34: https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.2.pdf (consulted 2026-10-15). Those conventions support the conditional mathematical interface, not a native quantum ontology. The preservation identity is inherited and the present applications and controls are proved above.

All findings were derived analytically before review. No scientific module, simulation, enumeration, historical replay, test-count increase or numerical campaign was performed; no retrospective preregistration is claimed. Independent whole-argument review and separate source/publication auditing accompany the assessment. No main merge or numbered-stage CLOSED/CERTIFIED status is asserted.

The native informational-difference milestone remains NOT ACHIEVED. No physical interaction law, force, gravity explanation, energy, geometry, dark-matter primitive or fundamental clock is established. Time remains pruning / ordered recoverability update. Path A remains active, Path B closed, and broad C3/C4-C6 remain OPEN.
