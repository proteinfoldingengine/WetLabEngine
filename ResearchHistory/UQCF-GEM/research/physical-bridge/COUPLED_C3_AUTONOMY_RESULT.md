# Uniformly safe incidence writes cannot create an initial hidden-state record in the core

Status: frozen analytical argument; independent verification/review pending.

## Candidate record-bearing interaction and inherited inputs
Full states S=(S_i) have finitely many fixed labelled roots, a fixed finite palette P disjoint union T, positive fixed original floors and protected hitting band3..4. P is the observed core. Let O(S)=(S_i intersect P)_i. Native requests +/-x at a named root toggle precisely that incidence when syntactically valid; guards test original floors and band. No other writes or auxiliary effects occur. The candidate record consists of any chosen core incidences, so observing the entire O is at least as informative as reading that record. An arbitrary controller memory is allowed, but its seed must be the same in the compared worlds and its update uses only permitted transcripts.

Unlike the earlier spectator-only proof, core writes may change O, and hidden writes may change T supports. The target is an INITIAL hidden predicate p(S0), for example the previously closed admission predicate. It is not assumed invariant under arbitrary destructive edits. A protocol must be uniformly safe before issue: its next toggle is syntactically valid and admissible in every full state consistent with its available history. Merely allowing the guard to reject unsafe attempts does not meet this condition.

Observation contains no exact tau, full-root cardinality, hidden support, full-palette counts, hypothetical legality bit, hidden-dependent latency or other output. Optional explicit commit-mask records can be granted as extra information provided the compared masks agree; the impossibility already holds with that extra knowledge. No physical observation mechanism is derived by granting O.

## Native projection identity
For a fixed request a, define f_a on core configurations: toggle the named core incidence if its label is in P; otherwise leave the core unchanged. Whenever the full-state toggle T_a is syntactically valid,

O(T_a(S))=f_a(O(S)).

This follows root by root from set membership and P intersect T=empty. It is not an assumption that the core is constant: f_a can change it. Hidden-dependent legality affects whether T_a may execute, but not its visible effect once it executes.

## All-commit theorem
Let S0,S0' be admissible with O(S0)=O(S0'), equal static controller parameters and equal initial memory. For any deterministic adaptive uniformly safe protocol, the entire observed transcripts, memory values and stopping decisions of their all-commit executions coincide at every finite prefix.

Induction: equal histories choose the same next command or stopping decision. Both current full states still realize the common history, so uniform safety permits that same toggle in both. The projection identity gives equal next core observations. Equal command/success records and the same memory update preserve equal histories. The base case is initial equality. Thus the claim holds for every finite prefix, including arbitrarily many actual core changes.

If p(S0) differs from p(S0'), a common terminating transcript cannot be assigned a correct p value in both. No uniformly safe protocol can both terminate with a correct p answer for every initial world on all-commit execution. One-sided sound certificates of a value that differs on this paired fiber cannot appear along their common all-commit histories either; the alternative initial world still realizes each such history. This does not prohibit certificates on other fibers where p is already constant.

The argument includes any finite or unbounded transcript-derived memory and adaptive stopping. For a randomized controller, fix the same private seed: the induction applies seedwise. In the all-commit model the transcript laws therefore coincide for the same seed distribution. It does not use or impose physical mandatory success; it shows that giving the candidate this progress advantage still does not let it measure p.

## Optional-NOOP semantics without a probabilistic overclaim
For each uniformly safe request the complete inherited relation has a NOOP and the same admissible toggle. Fix any binary resolution sequence, where1 commits and0 leaves the full state unchanged. Induction applies with visible update f_a or identity according to that sequence. Every such resolution is legal in both compared worlds. Consequently every possible finite observed trace in either world has a realizing run in the other; trace languages agree. All-commit runs are included and supply the obstruction without relying on stalling.

Equal possible-trace sets do NOT imply equal distributions under arbitrary hidden-dependent outcome probabilities. A resolution kernel that encodes hidden information in commit frequency or delays is additional structure not analyzed as hidden-independent here. With the SAME hidden-independent resolution law coupled on common histories, the seedwise argument also gives identical distributions. No stronger probabilistic statement is claimed.

Uniformly safe hidden-label requests can have invisible commits. Granting the common mask to the controller only strengthens its input; the projection induction still works. Removing that mask cannot improve distinguishability. Different executions may erase the difference in the CURRENT predicate; the theorem concerns p at the initial slice.

## Direct application to the admission target
The previously published pair has common core and floors(1,1,1,1,1,2):
S0=({0},{0},{0},{1},{2},{3,4}),
S1=({0},{0},{0},{1,6},{2,6},{3,4}).
Both lie in band3..4, with tau4/3 respectively, but the untouched outside intersection is empty versus{6}. No controller restricted to the above uniformly safe incidence-write/core-observation interface can initialize an exact record of this INITIAL admission bit, regardless of its subsequent core-writing strategy. This is a general protocol obstruction for the specified interface, not merely evaluation of the initial observation fiber.

For a nontrivial fully committed example add a private core label5 at the host, then remove it. A label occurring only at that already nonempty root cannot lower tau: replace it in any proposed cover by any old host label. Deletion restores the original state and floors. The two worlds have identical changing core transcripts throughout. The bounded application control checks both slices independently.

## Scope boundary and positive controls
The closed core-readout supplies the contrast. Its baseline00 and11 share a core; +e(root4) can commit in00 but would violate the band in11. Under guarded attempts, commit in00 and NOOP in11 yield different cores. That action is not uniformly safe across this pair. Thus the present theorem does not invalidate guarded conditional sensing: state-dependent admissibility is precisely where the core transition relation can acquire hidden dependence.

Supplying full hidden supports, an initialized count field or a correlated initial memory also escapes the equal-input premise; it does not refute the theorem or derive those supplies. A different inherited native interaction whose visible effect itself depends on the hidden state might escape the projection identity, but requires a justified carrier/action connection. No such interaction is invented here.

## Scientific meaning and novelty
This closes the proposed broad class of self-writing constructions using only uniformly safe native incidence toggles and core projection. It strengthens the earlier fixed-core spectator theorem to actively changing core records on arbitrary finite carriers, and strengthens the earlier two-request NOOP failure by proving indistinguishability even with complete commitment/progress. The verification alphabet is bounded; the universal scope follows from the projection induction.

It does not establish universal observer impossibility or physical record genesis. It identifies a precise fork for further native research: justify state-dependent enforced admissibility as a record-producing interaction, or identify an already-derived interaction/observable outside this write-only projection interface. Neither can be supplied by relabeling an offline verifier. General C3 origin, selection/access and general C4 remain OPEN. No physical force, fundamental time, geometry, dark-matter variable or GR derivation follows.
