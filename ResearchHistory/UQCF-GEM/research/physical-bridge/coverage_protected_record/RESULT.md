# Native coverage protects a receiver record after acquisition

Author: proteinfolding-gpt. Date: 2026-10-18 America/Phoenix.
Immutable source baseline: 2469a6899218127015b55cff530aa8855ffed785.
Status: analytical continuation awaiting independent Gemini review.
Native occurrence, preparation, and physical availability remain OPEN.

## 1. Positive construction and exact change of scope

The accepted source_enabled_record construction derives a first receiver response in an initially blind receiver, conditional on at most one source edit before that response. Its published all-prefix theorem assumes at most one source edit for the whole episode.

This continuation removes the restriction on the NUMBER of source edits AFTER acquisition. Native nonempty coverage itself protects the source incidence supporting an existing receiver deficit. The source may continue acting, and the receiver may add and delete other incidences. No new protection guard or source-freezing device is needed.

The resulting guarantee is a record-lifetime guarantee. A coarse decoder cannot give the opposite source answer until the receiver has restored every missing global leaf in the originally recorded branch. It may become UNKNOWN earlier if another branch also develops a deficit. After complete restoration of the original branch, no claim about the old source bit survives.

Thus this result does not replace the earlier whole-episode theorem with an unconditional stronger one. It permits more later activity and states the exact erasure boundary. It does not derive the acquisition prefix, an available reader, or physical event enforcement. It is mathematical support for the same native coverage candidate, not a separate supplied channel or a physical milestone.

## 2. Existing states, primitives, and the acquired record

Use the SAME carrier as the accepted construction:

    P={b,r};
    T={o,c_0,c_1} disjoint-union L_0 disjoint-union L_1;
    |L_j|=d_j>=2.                                             (1)

Each L_j consists of the global leaves below c_j. The root support is fixed at P. Every support is nonempty and a child support is contained in its parent's. For i in P, Y_i={v:i in S_v}; these views are prefix closed. A primitive adds or deletes one incidence at one nonroot vertex and preserves these conditions.

Use the bare native transition relation. The separately inherited hitting-profile budget is not imposed here. No simultaneous edits, new labels, altered carrier, event probabilities, legality oracle, read API or scheduler is added.

The acquisition prefix begins with

    Y_r=T,                  Y_b={o,c_s},   s in {0,1}.         (2)

The entire initial r-view and its bare atomic command interface are identical for the two sources. Under the accepted prefix condition, at most one b edit before the first r edit, any first receiver response must be

    +b(l), then -r(l),       l in L_s.                        (3)

It leaves

    F_*:  Y_r=T minus {l},  Y_b={o,c_s,l}.                    (4)

This is a dependency on the accepted theorem, also directly checked as follows. No initial r edit is legal. The initial b commands are -b(c_s), +b(c_(1-s)), and +b(v) for v in L_s. The internal commands leave every leaf exclusively r-covered and enable no r edit. A leaf addition enables exactly -r(l). No further b edit is needed or admitted by the prefix hypothesis before that first response.

The prefix need not occur. A legal source event can leave the receiver blank. The prefix condition is supplied and is not inferred from the fact that each primitive is atomic. There is no physical counter enforcing it.

Starting at F_*, allow ANY finite or infinite sequence of legal b and r primitives, with arbitrary interleaving and no bound on either count. Every theorem below about an infinite sequence is a statement at its finite prefixes. The original global one-source-edit bound is no longer applied after F_*.

## 3. Coverage forces source retention

For any valid two-label state on T, let

    D(F)=L_0 union L_1 minus Y_r,
    Q_j(F)=1[D(F) intersection L_j is nonempty].              (5)

Only receiver membership is used in these mathematical functions. Q records whether each branch has at least one missing receiver leaf, not which leaf or how many. Naming Q does not grant access to it.

**Coverage lemma.** If v is absent from Y_r, then v is present in Y_b. Every ancestor of v is also in Y_b. In particular,

    Q_j(F)=1  implies  c_j in Y_b.                            (6)

Proof. With exactly two labels and nonempty support, r absent at v forces S_v={b}. Nesting carries b through its ancestor path. Apply this to a missing leaf below c_j. QED.

**Retention consequence.** As long as a particular leaf l remains absent from Y_r, no valid state can omit b from l or any ancestor. A source-only sequence cannot remove that leaf coverage or its branch incidence while the receiver view is held fixed. For an arbitrary interleaving, Q_j=1 likewise forces the branch incidence b(c_j) at each prefix.

This is a consequence of existing nonemptiness and nesting, not an added transition veto. It is an invariant of the allowed states; it does not claim that a physical actuator enforces those states.

There is also an exact converse for source release.

**Branch-release theorem.** Fix a valid state F and hold its receiver view fixed. A b-only legal sequence ending with b absent from c_j exists IF AND ONLY IF Q_j(F)=0. When it exists, the minimum number of primitives is

    |Y_b intersection ({c_j} union L_j)|.                    (7)

Proof. If Q_j=1, a missing leaf remains missing in every b-only continuation. The coverage lemma forces b at that leaf and at c_j, contradicting release. If Q_j=0, r covers every leaf of that branch, and prefix closure gives r at c_j. Delete every b-covered leaf in L_j, in any order, and then delete b(c_j) if present. Each deletion has r as remaining coverage; the leaf deletions preserve nesting, and the last deletion has no remaining b-child. The rest of the carrier is unchanged. This takes exactly (7) edits. Any final state with b absent from c_j has b absent from all of its descendants by nesting. Each initially present b incidence in this branch must therefore be removed at least once, giving the lower bound (7), even if additions were permitted. If b is already absent, the count is zero. QED.

In the acquired state (4), -b(l) would have been legal immediately BEFORE -r(l), because r still covered l. Immediately AFTER -r(l), it is forbidden by nonemptiness. The receiver response therefore changes the source's native command possibilities in return: the source cannot withdraw the supporting branch until receiver coverage is restored. This is a formal reciprocal constraint, not a readable rejection flag or an actual two-way signalling protocol.

## 4. Coarse readout throughout the record's lifetime

Define one source-independent partial decoder on the two branch flags:

    d(0,0)=UNKNOWN;     d(1,1)=UNKNOWN;
    d(1,0)=0;          d(0,1)=1.                             (8)

At (2), Q=(0,0). At acquisition (4), Q=e_s and d(Q)=s.

Index subsequent finite prefixes by n=0,1,2,..., with n=0 the acquired state F_*. Define the mathematical erasure boundary

    tau_s = first n>=1 for which Q_s(F_n)=0,
            or infinity if none exists.                     (9)

The index is edit order, not fundamental time. Equation (9) defines a subset of histories; it is not a stopping mechanism, a supplied acknowledgement, or an available event notification. It depends on the original branch s and is not claimed inferable from a present ambiguous record without retained history.

**Protected-record theorem.** For EVERY allowed continuation and every prefix n<tau_s,

    b belongs to S_c_s(F_n);
    d(Q(F_n)) is either s or UNKNOWN, never 1-s.              (10)

There is no source-edit bound after acquisition. Receiver additions are allowed, including repairs of individual missing leaves, as long as the original branch has not been completely restored.

Proof. By definition of tau_s, Q_s=1 at each stated prefix. Equation (6) gives the retained source branch incidence. For s=0, Q is either (1,0) or (1,1); for s=1 it is either (0,1) or (1,1). Equation (8) proves the decoder statement. QED.

A missing leaf can be replaced by another missing leaf in the same branch before the first is repaired. The theorem therefore need not preserve one particular missing leaf for the whole lifetime. It preserves the original branch's nonempty deficit. No memory of the leaf's address is used by decoder (8).

If the receiver only prunes after acquisition, its missing-leaf set cannot shrink, so tau_s=infinity. This is a corollary, not a restriction of (10): the main theorem allows arbitrary additions up to the stated erasure boundary. Further pruning in the other branch can still change a definite answer to UNKNOWN.

For the eight-vertex carrier d_0=2,d_1=3, Q_0 and Q_1 are identified by the two parent arities, with the same fixed receiver role and reference carrier as before. They are invariant under rooted-tree and palette relabelling with that role carried along. The readout does not require source-view access or exact leaf occupancy counts. The physical availability of these coarse flags remains unproved; coarsening a formal view does not make it an available record.

## 5. Sharp controls, including actual ambiguity and erasure

Choose l_0 in L_0 and l_1 in L_1. Start from the acquired source-zero state F_* for l_0.

First perform

    +b(c_1), +b(l_1), -r(l_1).                               (11)

All moves preserve nonempty nested support. Q changes from (1,0) to (1,1), so the decoder becomes UNKNOWN. The original source branch is still retained by b. Thus indefinite retention of a DEFINITE answer is not claimed.

Now perform

    +r(l_0).                                                 (12)

Its parent c_0 still contains r. The original branch has no missing receiver leaves, so this is tau_0. Q=(0,1) and decoder (8) returns 1. This is a NEW other-branch record, not a reliable record of the original source-zero preparation. It demonstrates why (10) cannot be extended past erasure. No change to the decoder or an unearned erasure flag repairs that claim.

After (12), the source can legally perform -b(l_0), -b(c_0), consistent with (7). Before (12), neither a source-only release of c_0 nor removal of b(l_0) is possible. The receiver's restoration is the precise opening for source release.

The acquisition control is unchanged: from (2) with s=0, +b(c_1), +b(l_1), -r(l_1) can make the FIRST receiver record report 1. This uses two source edits before the response and is outside the acquisition prefix hypothesis. The present result therefore removes only the POST-acquisition source-count bound.

The palette restriction matters for the specific source identity. If a third label a is available at the root, it can cover c_s and l; then b can withdraw from l and c_s while r still misses l. With more labels, nonemptiness forces SOME outside coverage, not retention by this particular b. No many-source identity extension is claimed.

The fixed-carrier condition matters: deleting a carrier leaf is not an incidence edit and can remove the deficit itself. The invariants are not asserted for changed carriers.

The old unit-excursion conclusion is not extended. With d_0,d_1>=2, after (11) both branches have a {b} leaf and a {r} leaf, so both branch hitting numbers are two while the root hitting number is one. The total excursion from the all-one profile is two. This explicitly witnesses the broader bare-native continuation class. On any separately imposed subfamily, (10) remains valid, but the source-release sufficiency in (7) is proved only for the bare relation.

## 6. What this earns and the remaining native construction

The source no longer has to stop acting forever after a record is acquired. Existing coverage compatibility makes the source retain the branch supporting an un-erased receiver deficit, and the receiver can use a two-flag partial readout rather than the complete own view. No state encoder, measurement instrument, transfer probabilities or record-protection law has been introduced.

What remains is concrete: identify an actual acquisition prefix of the accepted type and an existing receiver-owned record whose available effects give these branch-deficit flags, or a sufficient separating coarsening. Native enforcement, actual source/receiver events, preparation and reference ownership are still premises to establish. An algebraic definition of Q, a software state inspection, or its representation by a projector does not discharge that obligation.

The inspected native grammar and accepted source-enabled proof do not provide an event-count law. This note does not claim that lineage certification or atomicity supplies one. It localizes the required source-count hypothesis to acquisition and replaces a later source freeze with a derived coverage invariant over the record's lifetime.

This is mathematical support for the same positive coverage candidate. No archive-wide novelty, native milestone, broad C3/C4 closure, numbered-stage CLOSED/CERTIFIED status, main merge, fundamental time, energy, geometry, dark-matter primitive or gravity claim is made.

## 7. Freeze and independent-review contract

These proofs and counterexamples were developed analytically before any numerical campaign. No native simulator, finite-universe enumeration or archived scientific module was executed. The exposed deductions are not retrospectively preregistered predictions.

Gemini must independently reconstruct the prefix dependence, coverage lemma, source-release equivalence and exact edit minimum, arbitrary-interleaving lifetime theorem, changing missing-leaf witnesses, coarse readout and relabelling, ambiguity/erasure examples, third-label and changed-carrier controls, and the excursion-two witness. It must check that no past-erasure, physical-access, actuation or guaranteed-progress claim is hidden in the wording.

Exact source documents are preserved in SOURCE_PACKET.json. Source integrity and separate publication auditing check immutable document bytes, the full request, raw response and verdict. Those checks are not additional scientific experiments. The frozen proof will remain unchanged when its review disposition is added.

