# A source-derived profile reaches a blank receiver through an existing caller

Date: 2026-10-26 (America/Phoenix).
Research source: 3ceb814258f43774b4af1352379ffcd0bd079599.
Status at freeze: analytical construction with exact historical evidence; independent whole-argument review pending. Native physics bridge NOT_DERIVED.

## 1. Result and precise advance

The existing v16.53 `produce()` R branch already reads the hitting profile of its input and passes that computed target to the existing normalizer. Two rows in its archived campaign give a receiver-index distinction without a caller-supplied target, new wrapper, new gate, new label or engineered density matrix:

| Preparation | Initial state (a,b,c) | Caller-computed target | Completed state | Receiver b |
| --- | --- | --- | --- | --- |
| 0 | [15,1,31] | [1] | [31,1,1] | root only |
| 1 | [15,1,17] | [2] | [15,17,1] | root and fourth leaf |

These are exact existing production records, not newly generated numerical examples. The new contribution is their source-to-caller-to-receiver interpretation and the explicit identification of the retained target memory. It resolves the software target-producer question for this pair. It does not identify a physical measurement with this program or derive physical receiver access.

The entire program is not initially blind: it reads the global source state into `q` before writing the receiver. Initial blindness below is a statement about the complete b-membership restriction and the bare b-command interface. A global returned certificate is never counted as an initially blank receiver-owned record.

## 2. Native inputs, source preparation and receiver restriction

Use the inherited four-leaf star Q with ordered vertices (o,v1,v2,v3,v4), and the same ordered palette P=(a,b,c)=(0,1,2). A column mask has root bit1 and leaf bits2,4,8,16. A state lists the masks of a,b,c. The fixed receiver is index b; c carries the preparation contrast. This is the inherited incidence representation, not a quantum factorization.

Set a={o,v1,v2,v3} in both inputs and b={o} in both. In preparation0 c=T; in preparation1 c={o,v4}. Every support is nonempty, all three indices retain o, and each view is prefix-closed. Both are admitted native states on the same carrier and palette.

The contrast has a native preparation path:

    [15,1,31] -> [15,1,29] -> [15,1,25] -> [15,1,17].

These are the three proper source deletions -c(v1), -c(v2), -c(v3). They preserve the carrier because a retains those leaves. They leave b blank throughout. This is a legal preparation relation; actual physical enactment is not claimed. These preparation moves are not part of either archived normalization row, and no common exact target is asserted for the two different endpoints of the preparation path.

For the receiver-only interface, hold a,c fixed within each comparison and allow named b-additions/deletions under bare native admissibility. In both preparations a union c=T. Hence every root-containing b-subtree is admitted, and every allowed leaf addition or deletion of b depends only on b's own membership. The two b-only command transition systems are identical for all finite adaptive command sequences. This follows directly here and is also an application of receiver_move_interface sections2–3: the initial b view and external global-leaf coverage agree.

This interface excludes global state/profile reads, normalizer invocation or completion flags, run length, and physical timing. In particular, its equality does not extend to a hypothetical global profile sensor. The unit-band path budget is not part of the bare b-only relation. No physical legality oracle is derived.

## 3. The target is produced by the unchanged enclosing caller

Producer `specs()` includes every four-tuple of nonempty child supports for k=3. Our exact existing identities are

    I0 = ["R",3,[0,2],[0,2],[0,2],[2]],
    I1 = ["R",3,[0],[0],[0],[2]].

The identity contains no target q. The existing `produce()` R branch (producer.py lines312–317) performs:

    k=identity[1]; tree=Q
    start=encode_roots(k,identity[2:])
    q=[coordinate(start,layout(tree)[0])]
    end=canonical(tree,k,q)
    path=normalize(start,tree,k,q)

This is a transcription of the relevant existing data flow, not a newly installed wrapper. The complete source is frozen in SOURCE_PACKET.json.

`coordinate` computes the minimum number of labels whose leaf supports cover all four children. In input0, c alone covers them, so q0=1. In input1 neither a nor c alone does, while together they do, so q1=2. Thus the common caller derives different internal targets from the source incidence contrast. No source-bit argument or manually chosen q is added.

All children have width1. `feasibility.minimum` and its existing positional ordering yield the canonical leaf allocations (a,a,a,a) for q1 and (a,a,a,b) for q2. For the latter, two labels are necessary and sufficient; putting the first label on the first three leaves and the second on the last is the least positional tuple with two distinct singleton owners. `canonical` therefore returns E0=[31,1,1] and E1=[15,17,1].

The fixed order and canonical allocation rule are inherited software choices. Their physical ownership/selection meaning is not inferred from being present in code. Changing the palette order can move the output to another index; we do not claim an order-free singled-out receiver.

## 4. Exact producing paths and native validity

The normalizer takes its existing four-child q=1 or q=2 branch. Its initial and final recursive leaf calls make no incidence edits. It expands the child supports to P, then contracts them to the computed canonical supports. There are no proper descendants requiring clearance.

The following paths were reconstructed by hand from the code and independently located in the original compressed production certificate:

    Input0, q=1:
    [15,1,31], [15,3,31], [15,7,31], [15,15,31],
    [31,15,31], [31,31,31], [31,29,31], [31,29,29],
    [31,25,29], [31,25,25], [31,17,25], [31,17,17],
    [31,1,17], [31,1,1].

    Input1, q=2:
    [15,1,17], [15,3,17], [15,3,19], [15,7,19],
    [15,7,23], [15,15,23], [15,15,31], [31,15,31],
    [31,31,31], [31,29,31], [31,29,29], [31,25,29],
    [31,25,25], [31,17,25], [31,17,17], [15,17,17],
    [15,17,1].

Every adjacent pair toggles one nonroot incidence. Additions preserve admission. Every contraction leaves the designated canonical owner at that leaf, so supports stay nonempty. On the star there are no other nesting conditions beyond retaining the root. The carrier and palette never change.

For input0 the actual hitting number h is1 throughout: c covers all leaves until a becomes full, and a remains full afterward. There are five additions and eight deletions, giving13 moves and peak excursion0.

For input1 there are eight additions and eight deletions, giving16 moves. At zero-based path indices0–5 h=2; at6–14 h=1; at15–16 h=2. Before index6, c has not yet acquired all of a's three leaves and a lacks v4, so no singleton cover exists. At index6 c becomes full, then a becomes full, and a remains full until index15 removes its v4 incidence. The endpoint has two distinct singleton owners. There is only one internal coordinate, so the total inherited excursion is |h-q|<=1, with peak1. Both initial and final profiles equal their internally computed target.

This proves the mathematical path predicates independently of trusting an archived PASS label. No claim of a universal normalization theorem or fresh verification of the entire historical campaign is made.

## 5. Receiver signal, retention and load-bearing memory

At the completed endpoints, the same receiver index has

    Y_b(E0)={o},        Y_b(E1)={o,v4}.

Its full membership restrictions differ, and even their intrinsic cardinalities are1 versus2. A mathematical discriminator is D(Y_b)=|Y_b|-1 on these two endpoints. That formula is a proof of separation, not an implemented physical sensor or observation API.

The terminal incidence states provide a limited native retention fact: every global leaf has exactly one owner. Therefore no nonroot incidence can be deleted in either endpoint while keeping this same carrier and preserving nonempty supports. This includes all b-only prunings and all fixed-carrier deletion-only sequences. It proves neither a physical lifetime nor stability under additions, carrier changes or arbitrary dynamics.

For example, the two legal edits

    [15,17,1] -> [15,17,17] -> [15,1,17]

add c(v4) and then remove b(v4), erasing the b record while preserving native admission. Also, adding b(v4) to E0 makes its b restriction identical to that of E1. The distinction is assigned to the specified completion slice, not to arbitrary later states.

**The retained target is essential.** Both paths visit [31,31,31], where the entire incidence state, including b=T, is identical. They later visit [31,17,17] as well, but take different next edits. Their full software states are not identical: `q`, the canonical targets and the resulting root-path instructions retain the source-derived distinction. This is an existing stateful read-and-write caller, not a memoryless action of the current incidence state alone.

Restarting the profile-computing caller from the common full incidence state reads q=1 in both cases and gives E0 in both. That analytical control identifies exactly where the source distinction is stored while the incidence states coincide. The argument does not turn the global q variable into a receiver-owned record. A physical counterpart of this controller memory and its coupling to b would need justification.

Rereading the profile at E0 or E1, then completing this same normalization, returns the corresponding E0 or E1. Thus the composite endpoint map is idempotent on these two outputs. The repeated paths still have intermediate expansions, and no temporal or continuous-observation claim follows. In particular,13 versus16 primitive steps is not a derived physical clock or a permitted initial readout.

## 6. Historical execution evidence and exact source binding

All relevant artifacts below are under demos/v16.53-four-child-boundary at the research source commit. They are historical readbacks, not new experiments.

| Source | Git blob |
| --- | --- |
| producer.py | 0501a1b32c0a660646ff95ecbb8a37a8f2e04b80 |
| verifier.py | 54e23706c170d0bb82c1b78161290145b6b99af7 |
| feasibility.py | 9e995e21c9a477034a2fd4be615e28a2551b0bf9 |
| NATIVE_ADMISSIBILITY.md | ebc315f7f2f6423fe9f6861cc3b8a0cfcf8420f2 |
| evidence/science/scientific/CERTIFICATE.json.gz | 9dd2e4445bca36dfe59f10fc7b7debd1ee2bc81e |
| evidence/science/scientific/VERIFY.json | 2cc3155f3e8bdd943d6c19b0e5366fc215714869 |
| evidence/science/METADATA.json | 8127ad6e7e628f9b2e78a95e0f569faf8dfa83b5 |

The two raw certificate rows have status ok and exactly the starts, computed targets, paths and endpoints above. The corresponding independently produced VERIFY rows report13/16 moves and peak0/1. The historical file's overall VERIFIED/2863-record label is preserved as provenance; it is not a new test count or a claim that we freshly reproduced its universe.

METADATA records historical run36944252886, attempt1, scientific/workflow head433b3c2e9ffb34e08e34b425d5c56dc1b8a851cf. Direct reads of producer.py, verifier.py and feasibility.py at that head give the same Git blobs as the research source. The source packet includes those exact files at both identities, plus byte-exact excerpts of the two certificate and verification rows. The gzip source is bound to its original compressed bytes and to the decompressed byte sequence before excerpting. The independent review and separate publication audit verify these identities.

Only source reading, gzip/base64 decoding, JSON extraction, text/hashing and review plumbing were executed for this checkpoint. No scientific module was imported, simulated, sampled or enumerated. The pair was identified analytically before review; it is not called prospectively preregistered or a newly tested finite universe.

## 7. Relation to previous attempts and premise ledger

T-133's CALLER_ATTEMPT.md at1905a492669c777c1b4df5a53ecccd254b0f7de5, blob4c07bfe643418ab2eb0b80a6b6ab22040dd4d2a3, tested a different seven-vertex acquired pair against a common supplied target. Its exact-start mismatch and fixed-endpoint conclusions remain intact. It explicitly left open a justified producer of source-dependent targets. Here that software producer is the already implemented and archived R branch. We do not retrofit this caller onto T-131's original acquired r views.

The generic fact that different canonical targets can give different endpoints is not a new theorem. The added evidence is the concrete source-to-target producer, its unchanged complete operation, archived successful input rows, initially identical b interface, explicit target-memory location, and separate b output. This is positive mathematical/software support for investigating that operation's physical correspondence, not a completed native physical signal.

| Premise or consequence | Classification and scope |
| --- | --- |
| Fixed nonempty nested incidence grammar, native additions/deletions | INHERITED; NATIVE_ADMISSIBILITY and exact code sources above |
| Native source preparation relation | DERIVED HERE from those primitive rules; its physical enactment is not supplied by legality |
| Four-leaf carrier, three ordered labels and both input rows | INHERITED SOFTWARE/ARCHIVED INPUTS; physical roles and preparation remain SUPPLIED |
| Actual target producer, normalizer, canonical ordering and retained q/target memory | INHERITED SOFTWARE; physical controller/read/write identification remains SUPPLIED |
| Receiver b's initial bare interface equality | DERIVED HERE directly; consistent with inherited receiver_move_interface theorem |
| Distinct completed b restrictions and fixed-carrier pruning stability | DERIVED HERE within that operation and the stated observation slice |
| Invocation/completion on a physical source and a physical receiver, retained q access/coupling, ownership and observation of b | UNRESOLVED; would be SUPPLIED if this were interpreted as an actual physical signal |
| Actual atemporal measurement/pruning occurrence | ACCEPTED INPUT; no cause, fairness or inevitability proof is reopened |

No new physical assumption is adopted. No global returned path, q value, metadata field or certificate becomes physically accessible merely because it is computed. A physically established continuation would have to associate the accepted event with this same stateful operation, including the retained target and resulting b update, and justify the availability of the b consequence. The construction identifies that obligation concretely; it does not satisfy it by naming the normalizer a measurement.

Broad C3/C4, native acquisition and physical origin remain OPEN. No main merge or numbered-stage CLOSED/CERTIFIED claim is made. Author-side parallel checks are not independent review; Gemini via the established Actions integration reviews this exact argument and source packet separately.
