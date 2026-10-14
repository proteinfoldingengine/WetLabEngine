# A declared record dependency does not force an interaction

Date: 2026-10-14 UTC. Inspected parent: `61aa5b5488170b223c1eabc033b49f6e23d81e69`.

**Disposition: scoped structural countermodel; native coupling not derived.** This note tests the existing adaptive-event lead directly, without requiring a C3 marker encoding. It identifies the supplied control operation, proves that the declared readiness/persistence/confluence conditions also admit a zero-coupling member with genuine selective events, and separates a controller effect from pre-existing conditional correlations. It is analytical work using elementary instrument identities, not a numerical campaign, mathematical priority claim, or physical milestone.

## 1. The concrete lead and its supplied input

In v15.14, `READS` declares that B2 requires previously realized A1 and B1 records. `instrument` checks those keys, then implements

    U_B2(a) = exp[-i (-1)^a 0.6 Y_4] U_old,
    K_b(a) = P_(4,b) U_B2(a),

where a is the A1 bit and qubit order is A1,A2,B1,B2. The coefficient, sign rule, Pauli axis, record wire and carrier are supplied. The outcome b is supplied separately to `advance`; it does not enter the instrument resolver. This is a genuine conditional feed-forward model, and its all-input branch completeness and order consistency remain positive results. The controller is not inferred by `enabled`, `missing`, or record persistence.

v15.15 does not remove this input. `controller_gate` constructs blocks by calling the same `prior.instrument`. `copy_gate` explicitly flips a fresh memory bit controlled by the corresponding system bit. `initial_joint` supplies blank memory. Its coherent realization reproduces the supplied instrument, including its controller choice; the copied registers are diagnostic model structure. These observations follow the function bodies and agree with both source reports.

## 2. Countermodel to deriving the coupling from structural conditions

Replace only the displayed controller extent by a real analytical parameter theta:

    R_a(theta) = exp[-i (-1)^a theta Y_4],
    U_a(theta) = R_a(theta) U_old,
    K_b^(a,theta) = P_(4,b) U_a(theta).

Keep the source carrier, initial state, other event unitaries, projectors, `READS` declaration, and supplied outcome semantics. The original model is theta=0.6. The family is a mathematical countermodel test, not a proposed physical law or a modification of the archived implementation.

**Claim.** For every real theta the family satisfies the following structural conditions:

1. Each ready B2 operation is a complete instrument: sum_b K_b^dagger K_b=I, because U_a is unitary and the outcome projections resolve I.
2. Every previously realized record is preserved. The inherited U_old is exp[-i 0.70(0.43 Y_4 + 0.13 Z_3 X_4)], which commutes with the earlier Z_1,Z_2,Z_3 record projections. R_a and the new P_(4,b) commute with them too.
3. The declared readiness interface is unchanged. Missing A1 or B1 still blocks B2; the same five declared schedules are accepted. At theta=0 this is a redundant A1 prerequisite, not a derived minimal causal dependency.
4. Permissible incomparable operations commute at the same realized control value. A1/B1 and A2/B1 use separate subsystem factors; after A1 is realized, A2 and B2 also act on separate factors. Adjacent allowed swaps therefore leave the complete history branch operator, its unnormalized state and its probability unchanged for matching record assignments. This uses exactly the declared partial order, not an elapsed clock.

These proofs depend on support and unitarity, not on theta being nonzero or equal to 0.6. They are all-parameter analytical statements, not sampled tests.

At theta=0 the B2 instrument is exactly P_(4,b) U_old for BOTH A1 values. Thus the same structural conditions permit no causal dependence of this operation on the A1 control bit. The original theta=0.6 and the zero-coupling member obey the listed conditions while differing as controlled instruments. Consequently those conditions do not derive the original controller or even require nonzero A1-to-B2 control influence.

**This is not a counterexample to the fixed theta=0.6 model.** That numerical control law is an additional explicit premise of the archived model, and theta=0 does not satisfy that premise. The conclusion is precisely that the readiness, record-preservation and confluence conditions listed above cannot supply the omitted control law. Nor is this a claim about every possible native event architecture.

## 3. Why the null member is not an all-NOOP example

The frozen initial state is a unitary conjugate of

    0.9 |+>^tensor4 <+|^tensor4 + 0.1 I_16/16,

so it is strictly positive. Along any allowed history, a selected branch is strictly positive on its current record sector. To see this inductively, let rho >= c P_done on that sector for some c>0. The next unitary preserves P_done. Projecting onto either next outcome therefore gives an operator >= c P_done P_new, which is positive on a nonzero half-dimensional sector. Normalization preserves strict positivity on that new sector.

Accordingly both next outcome weights are positive and a supplied actual branch reduces the record-sector rank by a factor of two. The chain is 16,8,4,2,1 for every allowed schedule, including theta=0. In particular, B2 still applies the inherited operation and forms its specified selective record; it is not the identity or a missing event. The nonselective B2 channel also has a nontrivial kernel on the current sector: conjugate an off-diagonal operator between its two outcome sectors by U_old^dagger.

These are conditional instrument/record facts. They do not derive occurrence or count density-matrix rank alone as physical entropy. Even if actual application and readout are granted for this countermodel, the A1-dependent part of the B2 action can be absent. This is the distinction from the already-known possibility of indefinitely choosing NOOP.

## 4. Separate the operation's influence from conditioned input correlations

Let sigma_a be the reduced B2 state immediately AFTER U_old and BEFORE R_a, in a fixed ready context with A1=a and the other prior record values fixed. Define

    x_a = Tr(X sigma_a),       z_a = Tr(Z sigma_a),
    c = cos(2 theta),         s = sin(2 theta).

Pauli multiplication gives R_a^dagger Z R_a = c Z - (-1)^a s X. Thus the exact probability of B2 outcome zero is

    p_theta(0 | a) = [1 + c z_a - (-1)^a s x_a]/2,
    p_theta(0 | 0) - p_theta(0 | 1)
        = c (z_0-z_1)/2 - s (x_0+x_1)/2.

For a matched receiver input sigma_0=sigma_1=sigma, this difference is -sin(2 theta) Tr(X sigma). At theta=0 it is zero for every matched receiver input. At theta=0.6 the EFFECT OPERATORS differ:

    F_0^(a=0) - F_0^(a=1)
        = -sin(1.2) U_old^dagger X_4 U_old != 0.

This proves that the supplied controller can change outcome probabilities on suitable inputs. It does not establish a signal for every input: sigma=I_2/2 gives equal probabilities even with the nonzero controller. The matched-input statement is an analytical diagnostic, not an assertion that the frozen trajectory provides that matched pair or that an event can physically reset its own history.

At theta=0, unequal conditional inputs instead give (z_0-z_1)/2. Such a conditional difference would not demonstrate A1-bit control of B2: the B2 operation is then identical for both bits. The source's pre-time preparation contains cross-stream generators Z_1 Z_3 and Z_2 Z_4, so equality of the conditional receiver inputs cannot be assumed from its event names or separate event supports. We do not assert a particular nonzero value for the archived pair without calculating it. No scientific code was run here.

The practical test is to identify both the actual conditioned receiver inputs AND the instrument's dependence on the supplied control. Comparing p(B2 | A1=0) with p(B2 | A1=1) alone does not separate prior correlation, conditioning and an explicit feed-forward effect. This is not a prohibition on physical source dependence or a demand for an observer to read hidden state; it prevents attributing an existing input correlation to a newly derived interaction.

## 5. Coherent realization does not select a nonzero coupling

For each theta the same block-control and copy construction yields history blocks K_r(theta), and hence an isometry

    V_theta = sum_r |r>_R tensor K_r(theta).

The branch-block identity and agreement after declared record pinching follow by the same gate-composition induction for every theta. Old-record control is block diagonal in the corresponding memory records; future records begin blank. At theta=0 the B2 controller reduces to I_R tensor U_old, although the subsequent B2 copy gate remains. Thus a reversible realization and its classical-record comparison do not eliminate the zero-coupling member or derive the physical origin/access of the memory wire. No new coherent carrier is adopted by writing this representation.

## 6. Assessment and next obligation

The lead contains an explicit mathematical interaction, but the source code locates it in the supplied signed rotation, not in record availability or preservation. This screen strengthens that source observation with an active-event countermodel and an exact response identity. The source's historical runs are preserved and not rerun or recertified. It does not improve the native milestone merely by reproducing a nonzero response at 0.6.

The previous pinching classification concerns instruments with one fixed nonselective channel. This theta comparison concerns a different question: whether the adaptive model's structural contracts determine its controlled operation. The channels may change with theta; the results are not silently combined as one fixed-channel theorem.

The next candidate must justify an actual cross-record update law or a constrained family of laws with a forced accessible consequence, including its carrier/reference relation and the actual receiver-input/output contract. A declared `READS` edge, preservation of earlier records, successful schedule confluence, or a supplied coherent copy circuit does not discharge that obligation. Requiring an edge to mean nonzero operational influence would add the influence as a premise; its native justification would still be needed. A derived probabilistic consequence may qualify, and neither unique outcomes nor a C3 marker implementation are prerequisites.

**Milestone: NOT ACHIEVED.** This is a bounded reason to stop promoting the v15.14/v15.15 controller as a native-origin candidate without new premise evidence. It is not an archive-wide impossibility claim. No numerical run, fundamental clock, inserted geometry, dark-matter primitive, physical force, main merge, or numbered-stage CLOSED/CERTIFIED claim follows. Time remains pruning / ordered recoverability update.

Nine exact repository inputs are pinned in source_packet.json and source_identities.json. The argument and controls are exposed analytical work, to receive independent whole-argument review and separate publication auditing. File/hash operations are provenance work, not scientific execution or a new test count.
